---
title: "Redis Persistence (RDB và AOF)"
description: "Hướng dẫn toàn diện về Redis persistence mechanisms bao gồm RDB snapshots, AOF (Append-Only File), fsync policies, hybrid persistence, fork COW, và performance monitoring trong production environments"
tags: ["redis", "persistence", "rdb", "aof", "fsync", "fork", "snapshot", "appendonly", "bgrewriteaof", "bgsave"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis Persistence (RDB và AOF)

## 1. Tổng Quan (Overview)

Redis persistence là cơ chế cho phép Redis lưu trữ dữ liệu từ memory xuống disk để đảm bảo durability. Trong môi trường enterprise, việc hiểu và configure persistence đúng cách là yếu tố then chốt để đảm bảo data integrity và system reliability.

Redis cung cấp hai cơ chế persistence chính:

**RDB (Redis Database)**: Tạo point-in-time snapshots của toàn bộ dataset tại các intervals đã định sẵn. RDB files nhỏ gọn và phù hợp cho backups và disaster recovery.

**AOF (Append-Only File)**: Ghi log tất cả write operations vào một file theo thứ tự thời gian. AOF cung cấp durability cao hơn và có thể được configured để fsync theo các policies khác nhau.

Cả hai cơ chế có thể được sử dụng đồng thời (hybrid persistence) để tận dụng ưu điểm của cả hai.

## 2. RDB Snapshots

### 2.1 Giới Thiệu

RDB là cơ chế persistence truyền thống của Redis. Nó tạo ra binary snapshot của toàn bộ dataset tại một thời điểm. File RDB có đuôi `.rdb` và có thể được nén để tiết kiệm disk space.

### 2.2 RDB Configuration

```conf
# redis.conf - RDB Configuration

# Enable RDB persistence
save 900 1        # Save if at least 1 key changed in 15 minutes
save 300 10       # Save if at least 10 keys changed in 5 minutes
save 60 10000     # Save if at least 10000 keys changed in 1 minute

# Disable RDB (if using AOF only)
# save ""

# RDB file settings
dbfilename dump.rdb
dir /var/lib/redis
rdbcompression yes
rdbchecksum yes

# On crash, use copy of RDB file
stop-writes-on-bgsave-error yes

# For replica, synchronize RDB in background
replica-serve-stale-data yes
replica-read-only yes
```

### 2.3 RDB Commands

```redis
# Trigger manual save (synchronous - blocks Redis)
SAVE

# Trigger background save (non-blocking)
BGSAVE

# Check last save status
LASTSAVE

# Get RDB info
DEBUG OBJECT ENCODING dump.rdb
INFO persistence

# Load RDB file on startup
# Redis automatically loads RDB on startup if persistence is enabled
# AOF takes precedence if both are present

# Copy RDB file
# Useful for creating backups
COPY dump.rdb dump_backup_$(date +%Y%m%d).rdb
```

### 2.4 RDB Generation Process

```typescript
/**
 * RDB bgsave process:
 * 
 * 1. Redis fork() một child process
 * 2. Child process bắt đầu write RDB file
 * 3. Parent process tiếp tục xử lý requests
 * 4. Khi complete, child process exit
 * 
 * Timeline:
 * Parent process (Redis)
 *    |
 *    +-- fork() --> Child process (RDB writer)
 *    |                   |
 *    |                   +-- Write RDB to disk
 *    |                   |
 *    |                   +-- Exit (0 for success)
 *    |
 *    +-- Continue serving requests
 */

interface RdbSaveStatus {
  status: 'running' | 'completed' | 'failed';
  startTime?: number;
  endTime?: number;
  duration?: number;
  rdbSaveAllowedCurrentChildren?: number;
}

async function checkRdbSaveStatus(redis: Redis): Promise<RdbSaveStatus> {
  const info = await redis.info('persistence');
  
  const rdbSaving = info.includes('rdb_bgsave_in_progress:1');
  const rdbLastSaveTime = parseInt(info.match(/rdb_last_save_time:(\d+)/)?.[1] || '0');
  const rdbLastSaveDuration = parseInt(info.match(/rdb_last_save_time_elapsed:(\d+)/)?.[1] || '0');
  
  return {
    status: rdbSaving ? 'running' : 'completed',
    startTime: rdbSaving ? Date.now() - rdbLastSaveDuration * 1000 : undefined,
    endTime: rdbSaving ? undefined : Date.now(),
    duration: rdbLastSaveDuration * 1000,
  };
}
```

### 2.5 RDB Use Cases

```typescript
// 1. Scheduled backup
class RedisBackupScheduler {
  private redis: Redis;
  private backupDir: string;
  private retentionDays: number;

  constructor(redis: Redis, backupDir: string, retentionDays = 7) {
    this.redis = redis;
    this.backupDir = backupDir;
    this.retentionDays = retentionDays;
  }

  async performBackup(): Promise<BackupResult> {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `redis_backup_${timestamp}.rdb`;
    const destPath = `${this.backupDir}/${filename}`;
    
    console.log(`Starting backup: ${filename}`);
    
    // Trigger BGSAVE
    await this.redis.bgsave();
    
    // Wait for completion
    const status = await this.waitForSaveComplete();
    
    if (status === 'completed') {
      // Copy RDB file
      await this.copyRdbFile(destPath);
      
      // Clean old backups
      await this.cleanOldBackups();
      
      return { success: true, filename, timestamp };
    }
    
    return { success: false, error: 'Save did not complete' };
  }

  private async waitForSaveComplete(): Promise<'completed' | 'failed'> {
    const maxWaitMs = 300000; // 5 minutes
    const checkInterval = 1000;
    let waited = 0;
    
    while (waited < maxWaitMs) {
      const info = await this.redis.info('persistence');
      const isRunning = info.includes('rdb_bgsave_in_progress:1');
      
      if (!isRunning) {
        return 'completed';
      }
      
      await this.sleep(checkInterval);
      waited += checkInterval;
    }
    
    return 'failed';
  }

  private async copyRdbFile(destPath: string): Promise<void> {
    const sourcePath = '/var/lib/redis/dump.rdb'; // From config
    await fs.promises.copyFile(sourcePath, destPath);
  }

  private async cleanOldBackups(): Promise<void> {
    const files = await fs.promises.readdir(this.backupDir);
    const cutoff = Date.now() - this.retentionDays * 24 * 60 * 60 * 1000;
    
    for (const file of files) {
      if (file.startsWith('redis_backup_') && file.endsWith('.rdb')) {
        const stats = await fs.promises.stat(`${this.backupDir}/${file}`);
        if (stats.mtimeMs < cutoff) {
          await fs.promises.unlink(`${this.backupDir}/${file}`);
          console.log(`Deleted old backup: ${file}`);
        }
      }
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 2. Point-in-time restore
class PointInTimeRestore {
  async restore(redis: Redis, backupPath: string): Promise<void> {
    // 1. Stop Redis
    console.log('Stopping Redis...');
    
    // 2. Replace current RDB with backup
    console.log('Replacing RDB file...');
    const dumpPath = '/var/lib/redis/dump.rdb';
    await fs.promises.copyFile(backupPath, dumpPath);
    
    // 3. Start Redis
    console.log('Starting Redis...');
    // Redis will automatically load the RDB file
    
    // 4. Verify data
    const keys = await redis.dbsize();
    console.log(`Restored ${keys} keys`);
  }
}
```

### 2.6 Python RDB Implementation

```python
import redis
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class RedisBackup:
    """
    Redis backup utilities using RDB snapshots
    """
    
    def __init__(self, redis_client: redis.Redis, backup_dir: str):
        self.redis = redis_client
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def trigger_bgsave(self) -> bool:
        """
        Trigger background save
        Returns True if save was started
        """
        # Check if save is already in progress
        info = self.redis.info('persistence')
        if info.get('rdb_bgsave_in_progress', 0):
            print("Background save already in progress")
            return False
        
        # Trigger save
        self.redis.bgsave()
        print("Background save triggered")
        return True
    
    def wait_for_save_complete(self, timeout: int = 300) -> bool:
        """
        Wait for background save to complete
        Returns True if completed, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            info = self.redis.info('persistence')
            if not info.get('rdb_bgsave_in_progress', 0):
                return True
            time.sleep(1)
        
        return False
    
    def create_backup(self, name: Optional[str] = None) -> str:
        """
        Create a backup and return the backup filename
        """
        if not name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"backup_{timestamp}.rdb"
        
        backup_path = os.path.join(self.backup_dir, name)
        
        # Trigger save and wait
        self.trigger_bgsave()
        self.wait_for_save_complete()
        
        # Copy RDB file
        rdb_source = self.redis.config_get('dir')['dir']
        rdb_file = os.path.join(rdb_source, 'dump.rdb')
        
        if os.path.exists(rdb_file):
            shutil.copy2(rdb_file, backup_path)
            print(f"Backup created: {backup_path}")
        else:
            raise FileNotFoundError(f"RDB file not found: {rdb_file}")
        
        return backup_path
    
    def list_backups(self) -> list:
        """List all backup files"""
        backups = []
        for filename in os.listdir(self.backup_dir):
            if filename.endswith('.rdb'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'path': filepath,
                    'size_bytes': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'age_hours': (datetime.now() - datetime.fromtimestamp(stat.st_ctime)).total_seconds() / 3600
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def restore_backup(self, backup_filename: str) -> None:
        """
        Restore from backup
        WARNING: This will replace current data!
        """
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        
        # Get current RDB path
        rdb_source = self.redis.config_get('dir')['dir']
        rdb_dest = os.path.join(rdb_source, 'dump.rdb')
        
        # Stop Redis (would need to be done externally or via systemctl)
        # For now, just copy the file
        shutil.copy2(backup_path, rdb_dest)
        print(f"Restored backup to: {rdb_dest}")
    
    def cleanup_old_backups(self, keep_days: int = 7) -> int:
        """
        Delete backups older than keep_days
        Returns number of deleted backups
        """
        cutoff = datetime.now() - timedelta(days=keep_days)
        deleted = 0
        
        for backup in self.list_backups():
            if backup['created'] < cutoff:
                os.remove(backup['path'])
                print(f"Deleted old backup: {backup['filename']}")
                deleted += 1
        
        return deleted
```

## 3. AOF (Append-Only File)

### 3.1 Giới Thiệu

AOF là cơ chế persistence ghi tất cả write operations vào một file theo thứ tự thời gian. Khi Redis restart, nó sẽ replay tất cả commands từ AOF file để khôi phục dataset.

### 3.2 AOF Configuration

```conf
# redis.conf - AOF Configuration

# Enable AOF
appendonly yes
appendfilename "appendonly.aof"

# AOF file location
dir /var/lib/redis

# fsync policies
# everysec: fsync once per second (default, recommended)
# always: fsync after every write (safest, slowest)
# no: fsync when OS decides (risky)
appendfsync everysec

# Rewrite policies
# Rewrite when AOF grows by 100%
auto-aof-rewrite-percentage 100
# Minimum size 64MB before rewrite
auto-aof-rewrite-min-size 64mb

# Handle incomplete commands on restart
aof-load-truncated yes

# Enable Redis 7+ multi-part AOF
aof-use-rdb-preamble yes
```

### 3.3 AOF Commands

```redis
# Check if AOF is enabled
CONFIG GET appendonly

# Enable/disable AOF at runtime
CONFIG SET appendonly yes
CONFIG SET appendonly no

# Force AOF rewrite
BGREWRITEAOF

# Check AOF rewrite status
INFO persistence | grep aof

# Check AOF file size
ls -lh appendonly.aof

# Check number of AOF rewrites
INFO persistence
# aof_rewrite_scheduled
# aof_last_rewrite_time_sec
# aof_current_size
# aof_base_size
```

### 3.4 fsync Policies Chi Tiết

```typescript
/**
 * fsync Policies:
 * 
 * 1. always (安全性最高, 性能最差)
 *    - Mỗi operation đều được fsync trước khi trả về
 *    - Đảm bảo không mất data, nhưng rất chậm
 *    - Chỉ phù hợp với các use cases cực kỳ sensitive
 * 
 * 2. everysec (default, cân bằng)
 *    - fsync một lần mỗi giây
 *    - Có thể mất tối đa 1 giây data
 *    - Đủ an toàn cho hầu hết use cases
 *    - Performance tốt
 * 
 * 3. no (性能最好, 安全性最差)
 *    - Để OS quyết định khi nào fsync
 *    - Có thể mất nhiều data
 *    - Không recommended cho production
 */

interface AofStats {
  enabled: boolean;
  currentSize: number;
  baseSize: number;
  rewriteInProgress: boolean;
  lastRewriteDuration: number;
  lastBgRewriteStatus: string;
}

async function getAofStats(redis: Redis): Promise<AofStats> {
  const info = await redis.info('persistence');
  
  return {
    enabled: info.includes('aof_enabled:1'),
    currentSize: parseInt(info.match(/aof_current_size:(\d+)/)?.[1] || '0'),
    baseSize: parseInt(info.match(/aof_base_size:(\d+)/)?.[1] || '0'),
    rewriteInProgress: info.includes('aof_rewrite_in_progress:1'),
    lastRewriteDuration: parseInt(info.match(/aof_last_rewrite_time_sec:([-\d]+)/)?.[1] || '0'),
    lastBgRewriteStatus: info.match(/aof_last_write_status:(\w+)/)?.[1] || 'unknown',
  };
}

// Choose appropriate fsync policy
function selectFsyncPolicy(workload: string): string {
  const policies: Record<string, string> = {
    // Write-heavy, data-critical
    financial: 'always',
    
    // Balanced workloads
    web_app: 'everysec',
    api: 'everysec',
    cache: 'no',
    
    // Read-heavy, can tolerate data loss
    analytics: 'no',
    session_store: 'everysec',
    
    // Default for most cases
    default: 'everysec',
  };
  
  return policies[workload] || policies.default;
}
```

### 3.5 AOF Rewrite

```typescript
/**
 * AOF Rewrite Process (BGREWRITEAOF):
 * 
 * 1. Redis fork() một child process
 * 2. Child process write một phiên bản mới của AOF
 *    dựa trên current dataset state
 * 3. Parent process tiếp tục ghi vào AOF cũ
 * 4. Khi complete, child process exit
 * 5. Parent process replace old AOF với new AOF
 * 
 * Auto-rewrite triggers when:
 * - AOF size > base_size * (1 + auto-aof-rewrite-percentage/100)
 * - AOF size > auto-aof-rewrite-min-size
 */

class AofRewriteManager {
  private redis: Redis;
  private minSizeMB = 64;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async triggerRewrite(): Promise<boolean> {
    const stats = await getAofStats(this.redis);
    
    if (stats.rewriteInProgress) {
      console.log('AOF rewrite already in progress');
      return false;
    }

    console.log('Triggering AOF rewrite...');
    await this.redis.bgrewriteaof();
    return true;
  }

  async waitForRewriteComplete(timeoutMs = 300000): Promise<boolean> {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeoutMs) {
      const stats = await getAofStats(this.redis);
      
      if (!stats.rewriteInProgress) {
        console.log('AOF rewrite completed');
        return true;
      }
      
      await this.sleep(1000);
    }
    
    console.error('AOF rewrite timed out');
    return false;
  }

  async forceRewriteIfNeeded(): Promise<void> {
    const stats = await getAofStats(this.redis);
    const sizeMB = stats.currentSize / (1024 * 1024);
    
    if (sizeMB > this.minSizeMB) {
      const growthPercent = ((stats.currentSize - stats.baseSize) / stats.baseSize) * 100;
      
      if (growthPercent > 50) {
        console.log(`AOF growing significantly (${growthPercent.toFixed(1)}%), triggering rewrite`);
        await this.triggerRewrite();
        await this.waitForRewriteComplete();
      }
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### 3.6 AOF Recovery

```python
import redis
import os
from typing import Optional

class AofRecovery:
    """
    AOF recovery utilities
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def verify_aof_integrity(self, aof_path: str) -> bool:
        """
        Verify AOF file integrity by checking for valid commands
        """
        try:
            with open(aof_path, 'rb') as f:
                while True:
                    # Read length prefix
                    length_bytes = f.read(1)
                    if not length_bytes:
                        break
                    
                    # Simple check - if we can read the file without error,
                    # it's likely valid
                    
            return True
        except Exception as e:
            print(f"AOF verification failed: {e}")
            return False
    
    def trim_incomplete_commands(self, aof_path: str) -> bool:
        """
        Redis 5+ automatically handles this with aof-load-truncated yes
        For older versions, manually trim incomplete commands
        """
        try:
            # Read AOF file
            with open(aof_path, 'rb') as f:
                content = f.read()
            
            # Find last complete command
            # This is a simplified approach
            lines = content.split(b'\n')
            complete_commands = []
            
            for line in lines:
                # Check if line is a complete Redis command
                if line.startswith(b'*') and b'\r\n' in content:
                    # Count command arguments
                    complete_commands.append(line)
            
            # Write back complete commands
            with open(aof_path, 'wb') as f:
                f.write(b'\n'.join(complete_commands))
            
            return True
        except Exception as e:
            print(f"Failed to trim AOF: {e}")
            return False
    
    def get_aof_stats(self) -> dict:
        """Get AOF statistics"""
        info = self.redis.info('persistence')
        
        return {
            'aof_enabled': info.get('aof_enabled', 0) == 1,
            'aof_current_size': info.get('aof_current_size', 0),
            'aof_base_size': info.get('aof_base_size', 0),
            'aof_pending_rewrite': info.get('aof_rewrite_buffer_length', 0),
            'aof_rewrite_in_progress': info.get('aof_rewrite_in_progress', 0),
            'aof_last_rewrite_time': info.get('aof_last_rewrite_time_sec', 0),
            'aof_write_error': info.get('aof_last_write_error', ''),
        }
    
    def recover_from_aof(self) -> bool:
        """
        Ensure Redis loads from AOF file
        """
        # Ensure AOF is enabled
        self.redis.config_set('appendonly', 'yes')
        
        # Ensure truncated AOF is loaded
        self.redis.config_set('aof-load-truncated', 'yes')
        
        # Restart Redis (needs to be done externally)
        print("Please restart Redis for AOF recovery")
        
        return True
```

## 4. Fork COW (Copy-On-Write)

### 4.1 Giới Thiệu

Khi Redis thực hiện BGSAVE hoặc BGREWRITEAOF, nó sử dụng fork() để tạo một child process. Child process sử dụng COW (Copy-On-Write) memory pages từ parent process để minimize memory usage.

### 4.2 Fork Mechanics

```typescript
/**
 * Fork COW Process:
 * 
 * 1. Parent process memory: 10GB
 * 2. fork() called -> Child process created
 * 3. Initially: Child shares all memory pages with Parent (0 extra memory)
 * 4. As Child writes data:
 *    - Pages that change are duplicated
 *    - Only changed pages consume extra memory
 * 
 * For RDB save:
 * - Child process reads and writes RDB file
 * - Parent continues serving requests
 * 
 * Memory Impact:
 * - Peak memory = Parent + Child changed pages
 * - Typically 2-3x memory usage during save
 */

interface ForkStats {
  latestForkUsec: number;  // Time taken for last fork (microseconds)
  moduleForkedChildren: number;
  moduleForkedChildrenStatus: number;
}

async function getForkStats(redis: Redis): Promise<ForkStats> {
  const info = await redis.info('fork_child');
  
  return {
    latestForkUsec: parseInt(info.match(/latest_fork_usec:(\d+)/)?.[1] || '0'),
    moduleForkedChildren: parseInt(info.match(/module_forked_children:(\d+)/)?.[1] || '0'),
    moduleForkedChildrenStatus: parseInt(info.match(/module_forked_children_status:(\d+)/)?.[1] || '0'),
  };
}

// Estimate memory needed for fork
function estimateForkMemory(redisMemoryMB: number): {
  minExtraMemoryMB: number;
  maxExtraMemoryMB: number;
  recommendedFreeMemoryMB: number;
} {
  // COW memory overhead is typically 1-2x of memory changes during fork
  const overheadFactor = 0.3; // Assume 30% of memory changes
  
  const minExtra = redisMemoryMB * overheadFactor * 0.5;
  const maxExtra = redisMemoryMB * overheadFactor * 2;
  
  return {
    minExtraMemoryMB: Math.round(minExtra),
    maxExtraMemoryMB: Math.round(maxExtra),
    recommendedFreeMemoryMB: Math.round(redisMemoryMB * 0.5 + maxExtra),
  };
}
```

### 4.3 Memory Configuration for Fork

```conf
# redis.conf - Memory settings for persistence

# Set maxmemory
maxmemory 4gb

# Memory policy when maxmemory reached
maxmemory-policy allkeys-lru

# Overcommit memory for fork operations
# Important for avoiding OOM during fork
vm.overcommit_memory 1

# Disable transparent huge pages (THP)
# THP can cause memory spikes during fork
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# In /etc/sysctl.conf
# vm.overcommit_memory = 1
# vm.max_map_count = 655360
```

### 4.4 Monitoring Fork Performance

```typescript
class ForkMonitor {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async getPersistenceStats(): Promise<PersistenceStats> {
    const info = await this.redis.info('persistence');
    
    return {
      rdbBgsaveInProgress: info.includes('rdb_bgsave_in_progress:1'),
      rdbLastSaveTime: parseInt(info.match(/rdb_last_save_time:(\d+)/)?.[1] || '0'),
      rdbLastSaveDuration: parseInt(info.match(/rdb_last_save_time_elapsed:(\d+)/)?.[1] || '0'),
      aofEnabled: info.includes('aof_enabled:1'),
      aofRewriteInProgress: info.includes('aof_rewrite_in_progress:1'),
      aofCurrentSize: parseInt(info.match(/aof_current_size:(\d+)/)?.[1] || '0'),
      aofBaseSize: parseInt(info.match(/aof_base_size:(\d+)/)?.[1] || '0'),
      latestForkUsec: parseInt(info.match(/latest_fork_usec:(\d+)/)?.[1] || '0'),
    };
  }

  async checkForkHealth(): Promise<ForkHealthReport> {
    const stats = await this.getPersistenceStats();
    const memoryInfo = await this.redis.info('memory');
    
    const usedMemoryMB = parseInt(memoryInfo.match(/used_memory:(\d+)/)?.[1] || '0') / (1024 * 1024);
    const latestForkMs = stats.latestForkUsec / 1000;
    
    const issues: string[] = [];
    const warnings: string[] = [];
    
    // Check fork time
    if (latestForkMs > 1000) {
      issues.push(`Fork took ${latestForkMs.toFixed(0)}ms - very slow`);
    } else if (latestForkMs > 500) {
      warnings.push(`Fork took ${latestForkMs.toFixed(0)}ms - consider optimizing`);
    }
    
    // Check AOF growth
    const aofGrowthMB = (stats.aofCurrentSize - stats.aofBaseSize) / (1024 * 1024);
    if (stats.aofEnabled && aofGrowthMB > 1000) {
      warnings.push(`AOF has grown by ${aofGrowthMB.toFixed(0)}MB - consider rewriting`);
    }
    
    // Check memory
    if (usedMemoryMB > 8000) {
      warnings.push(`Memory usage ${usedMemoryMB.toFixed(0)}MB - ensure enough free memory for fork`);
    }
    
    return {
      stats,
      issues,
      warnings,
      healthScore: issues.length === 0 ? 'good' : 'poor',
    };
  }

  async logPersistenceStatus(): Promise<void> {
    const stats = await this.getPersistenceStats();
    const memory = await this.redis.info('memory');
    const usedMemory = parseInt(memory.match(/used_memory:(\d+)/)?.[1] || '0') / (1024 * 1024);
    
    console.log('=== Redis Persistence Status ===');
    console.log(`RDB Save: ${stats.rdbBgsaveInProgress ? 'IN PROGRESS' : 'idle'}`);
    console.log(`AOF Rewrite: ${stats.aofRewriteInProgress ? 'IN PROGRESS' : 'idle'}`);
    console.log(`Memory Used: ${usedMemory.toFixed(0)}MB`);
    console.log(`Fork Time: ${(stats.latestForkUsec / 1000).toFixed(0)}ms`);
    console.log(`AOF Size: ${(stats.aofCurrentSize / 1024 / 1024).toFixed(0)}MB`);
  }
}
```

## 5. Hybrid Persistence

### 5.1 Giới Thiệu

Redis 7+ hỗ trợ hybrid persistence với RDB preamble trong AOF. Điều này có nghĩa là AOF file bắt đầu với một RDB snapshot, sau đó là các commands thay đổi kể từ đó.

### 5.2 Hybrid Configuration

```conf
# Enable AOF với RDB preamble
appendonly yes
aof-use-rdb-preamble yes

# Combined with RDB saves
save 900 1
save 300 10
save 60 10000

# Benefits:
# - Faster AOF rewrite (start from RDB snapshot)
# - Smaller AOF files
# - Faster restart (load RDB + replay AOF)
```

### 5.3 Performance Impact Analysis

```typescript
/**
 * Persistence Performance Impact:
 * 
 * No Persistence:
 * - Fastest performance
 * - No durability guarantees
 * 
 * RDB Only:
 * - Periodic performance spikes during BGSAVE
 * - Memory spike due to COW
 * - Potential data loss between saves
 * 
 * AOF Only (everysec):
 * - Slight write latency increase
 * - Better durability than RDB
 * - AOF rewrite causes periodic spikes
 * 
 * Hybrid (RDB + AOF):
 * - Best of both worlds
 * - Faster restart
 * - Higher storage requirements
 */

interface PerformanceImpact {
  readLatency: 'no_change' | 'slight_increase' | 'moderate_increase';
  writeLatency: 'no_change' | 'slight_increase' | 'moderate_increase' | 'significant_increase';
  memoryOverhead: 'none' | 'low' | 'moderate' | 'high';
  diskIO: 'minimal' | 'moderate' | 'high';
  dataLossWindow: string;
}

function analyzePersistenceConfig(config: PersistenceConfig): PerformanceImpact {
  const impacts: PerformanceImpact = {
    readLatency: 'no_change',
    writeLatency: 'no_change',
    memoryOverhead: 'none',
    diskIO: 'minimal',
    dataLossWindow: 'none',
  };

  if (!config.enabled) {
    impacts.dataLossWindow = 'all data at risk';
    return impacts;
  }

  if (config.rdbEnabled && config.aofEnabled) {
    impacts.writeLatency = 'slight_increase';
    impacts.memoryOverhead = 'moderate';
    impacts.diskIO = 'moderate';
    impacts.dataLossWindow = 'max 1 second (AOF) or last save (RDB)';
    return impacts;
  }

  if (config.aofEnabled) {
    impacts.writeLatency = 'slight_increase';
    impacts.diskIO = 'moderate';
    impacts.dataLossWindow = 'max 1 second';
    
    if (config.aofFsync === 'always') {
      impacts.writeLatency = 'significant_increase';
      impacts.diskIO = 'high';
      impacts.dataLossWindow = 'no data loss';
    }
    
    return impacts;
  }

  if (config.rdbEnabled) {
    impacts.memoryOverhead = 'moderate'; // During BGSAVE
    impacts.dataLossWindow = 'last save interval';
  }

  return impacts;
}
```

## 6. Production Configuration Examples

### 6.1 High Performance Configuration

```conf
# redis-highperf.conf
# Optimized for maximum performance with reasonable durability

# Network
bind 0.0.0.0
port 6379
timeout 300
tcp-keepalive 60

# Memory
maxmemory 8gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# RDB - less frequent saves
save 3600 1
save 300 100
save 60 10000

# Disable BGSAVE during peak hours
# save ""

# AOF for durability
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-use-rdb-preamble yes

# Disable AOF rewrite during peak hours
# Use cron to trigger BGREWRITEAOF during off-peak

# Performance
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no

# System
vm.overcommit_memory 1
```

### 6.2 Maximum Durability Configuration

```conf
# redis-maxdurability.conf
# Optimized for maximum data safety

# RDB as backup
save 3600 1
save 1800 10
save 300 100

# AOF with maximum safety
appendonly yes
appendfilename "appendonly.aof"
appendfsync always
auto-aof-rewrite-percentage 200
auto-aof-rewrite-min-size 512mb
aof-use-rdb-preamble yes
aof-load-truncated yes

# Prevent writes on disk errors
stop-writes-on-bgsave-error yes

# Replication for additional safety
replicaof <master-ip> 6379
min-replicas-to-write 1
min-replicas-max-lag 10
```

### 6.3 Container/Kubernetes Configuration

```yaml
# Kubernetes deployment for Redis with persistence
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  serviceName: redis
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        args:
          - redis-server
          - --appendonly yes
          - --appendfsync everysec
          - --rdb-snapshotting-enabled yes
          - --save 900 1
          - --save 300 10
          - --save 60 10000
          - --maxmemory 2gb
          - --maxmemory-policy allkeys-lru
          - --appendfilename appendonly.aof
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "3Gi"
            cpu: "1000m"
        volumeMounts:
        - name: redis-data
          mountPath: /data
        - name: redis-config
          mountPath: /usr/local/etc/redis
      volumes:
      - name: redis-config
        configMap:
          name: redis-config
```

## 7. Persistence Monitoring

### 7.1 Key Metrics to Monitor

```typescript
interface PersistenceMetrics {
  // RDB metrics
  rdbBgsaveInProgress: boolean;
  rdbLastSaveTime: number;
  rdbLastSaveDuration: number;
  rdbLastBgsaveStatus: string;
  
  // AOF metrics
  aofEnabled: boolean;
  aofCurrentSize: number;
  aofBaseSize: number;
  aofRewriteInProgress: boolean;
  aofLastRewriteDuration: number;
  aofPendingRewriteBuffer: number;
  aofLastWriteStatus: string;
  
  // Fork metrics
  latestForkUsec: number;
  
  // Memory
  usedMemory: number;
  usedMemoryPeak: number;
  memFragmentationRatio: number;
}

class PersistenceMonitor {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async collectMetrics(): Promise<PersistenceMetrics> {
    const [persistence, memory] = await Promise.all([
      this.redis.info('persistence'),
      this.redis.info('memory'),
    ]);

    return {
      rdbBgsaveInProgress: persistence.includes('rdb_bgsave_in_progress:1'),
      rdbLastSaveTime: parseInt(persistence.match(/rdb_last_save_time:(\d+)/)?.[1] || '0'),
      rdbLastSaveDuration: parseInt(persistence.match(/rdb_last_save_time_elapsed:(\d+)/)?.[1] || '0'),
      rdbLastBgsaveStatus: persistence.match(/rdb_bgsave_status:(\w+)/)?.[1] || 'unknown',
      aofEnabled: persistence.includes('aof_enabled:1'),
      aofCurrentSize: parseInt(persistence.match(/aof_current_size:(\d+)/)?.[1] || '0'),
      aofBaseSize: parseInt(persistence.match(/aof_base_size:(\d+)/)?.[1] || '0'),
      aofRewriteInProgress: persistence.includes('aof_rewrite_in_progress:1'),
      aofLastRewriteDuration: parseInt(persistence.match(/aof_last_rewrite_time_sec:([-\d]+)/)?.[1] || '0'),
      aofPendingRewriteBuffer: parseInt(persistence.match(/aof_rewrite_buffer_length:(\d+)/)?.[1] || '0'),
      aofLastWriteStatus: persistence.match(/aof_last_write_status:(\w+)/)?.[1] || 'unknown',
      latestForkUsec: parseInt(persistence.match(/latest_fork_usec:(\d+)/)?.[1] || '0'),
      usedMemory: parseInt(memory.match(/used_memory:(\d+)/)?.[1] || '0'),
      usedMemoryPeak: parseInt(memory.match(/used_memory_peak:(\d+)/)?.[1] || '0'),
      memFragmentationRatio: parseFloat(memory.match(/mem_fragmentation_ratio:([\d.]+)/)?.[1] || '0'),
    };
  }

  async getAlerts(): Promise<Alert[]> {
    const metrics = await this.collectMetrics();
    const alerts: Alert[] = [];

    // Check RDB save failures
    if (metrics.rdbLastBgsaveStatus === 'err') {
      alerts.push({
        severity: 'critical',
        message: 'RDB background save failed',
      });
    }

    // Check AOF write failures
    if (metrics.aofLastWriteStatus === 'err') {
      alerts.push({
        severity: 'critical',
        message: 'AOF write failed',
      });
    }

    // Check for long fork times
    if (metrics.latestForkUsec > 1000000) { // > 1 second
      alerts.push({
        severity: 'warning',
        message: `Fork took ${metrics.latestForkUsec / 1000}ms - may indicate memory pressure`,
      });
    }

    // Check AOF growth
    if (metrics.aofCurrentSize > metrics.aofBaseSize * 2) {
      alerts.push({
        severity: 'info',
        message: 'AOF file growing significantly - rewrite may be needed',
      });
    }

    // Check for ongoing saves
    if (metrics.rdbBgsaveInProgress || metrics.aofRewriteInProgress) {
      alerts.push({
        severity: 'info',
        message: 'Persistence operation in progress',
      });
    }

    return alerts;
  }

  async generateReport(): Promise<string> {
    const metrics = await this.collectMetrics();
    const alerts = await this.getAlerts();

    const formatBytes = (bytes: number) => {
      const mb = bytes / (1024 * 1024);
      return mb >= 1024 
        ? `${(mb / 1024).toFixed(2)} GB` 
        : `${mb.toFixed(2)} MB`;
    };

    const lines = [
      '=== Redis Persistence Report ===',
      `Generated: ${new Date().toISOString()}`,
      '',
      'RDB Status:',
      `  - Background Save: ${metrics.rdbBgsaveInProgress ? 'IN PROGRESS' : 'idle'}`,
      `  - Last Save: ${new Date(metrics.rdbLastSaveTime * 1000).toLocaleString()}`,
      `  - Last Duration: ${metrics.rdbLastSaveDuration}s`,
      `  - Last Status: ${metrics.rdbLastBgsaveStatus}`,
      '',
      'AOF Status:',
      `  - Enabled: ${metrics.aofEnabled ? 'Yes' : 'No'}`,
      `  - Current Size: ${formatBytes(metrics.aofCurrentSize)}`,
      `  - Base Size: ${formatBytes(metrics.aofBaseSize)}`,
      `  - Rewrite: ${metrics.aofRewriteInProgress ? 'IN PROGRESS' : 'idle'}`,
      `  - Last Status: ${metrics.aofLastWriteStatus}`,
      '',
      'Performance:',
      `  - Latest Fork: ${(metrics.latestForkUsec / 1000).toFixed(0)}ms`,
      `  - Memory Used: ${formatBytes(metrics.usedMemory)}`,
      `  - Memory Peak: ${formatBytes(metrics.usedMemoryPeak)}`,
      `  - Fragmentation: ${metrics.memFragmentationRatio.toFixed(2)}`,
    ];

    if (alerts.length > 0) {
      lines.push('', 'Alerts:');
      for (const alert of alerts) {
        lines.push(`  [${alert.severity.toUpperCase()}] ${alert.message}`);
      }
    }

    return lines.join('\n');
  }
}
```

### 7.2 Prometheus Metrics

```yaml
# Prometheus exporter configuration for Redis persistence
groups:
- name: redis_persistence
  interval: 15s
  rules:
  # RDB metrics
  - record: redis:rdb:bgsave:progress:rate
    expr: |
      rate(redis_rdb_changes_since_last_save_total[5m])
  
  # AOF metrics  
  - record: redis:aof:size:bytes
    expr: redis_aof_current_size
  
  - record: redis:aof:growth:rate
    expr: |
      rate(redis_aof_current_size[1h])
  
  # Fork metrics
  - record: redis:fork:duration:seconds
    expr: redis_latest_fork_usec / 1000000
  
  # Alert rules
  - alert: RedisRdbSaveFailing
    expr: redis_rdb_last_bgsave_status == 'err'
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis RDB save failing"
  
  - alert: RedisAofWriteFailing
    expr: redis_aof_last_write_status == 'err'
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis AOF write failing"
  
  - alert: RedisSlowFork
    expr: redis_latest_fork_usec > 1000000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Redis fork taking longer than 1 second"
  
  - alert: RedisAofGrowingFast
    expr: |
      rate(redis_aof_current_size[1h]) > 1073741824  # 1GB/hour
    for: 30m
    labels:
      severity: warning
    annotations:
      summary: "Redis AOF growing faster than 1GB/hour"
```

## 8. Troubleshooting

### 8.1 Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Fork OOM | Redis crash during BGSAVE | Increase memory, reduce maxmemory, disable THP |
| Slow fork | High latency during save | Use faster disk (SSD), reduce data size |
| AOF corruption | Redis won't start | Enable aof-load-truncated, check disk health |
| AOF too large | Disk space issues | Increase rewrite threshold, use RDB+AOF hybrid |
| Write errors | Persistence failures | Check disk space, disk health, permissions |
| Data loss | Missing data after restart | Review fsync policy, enable AOF |

### 8.2 Diagnostic Commands

```redis
# Check persistence status
INFO persistence
INFO replication

# Check memory info
INFO memory
MEMORY STATS

# Check disk I/O stats
INFO stats | grep -E "(disk|fsync)"

# Check for slow operations
SLOWLOG GET 10

# Check key statistics
INFO keyspace

# Debug commands
DEBUG SLEEP 1
DEBUG OBJECT ENCODING <key>
DEBUG OBJECT FREQUENCY <key>
```

### 8.3 Recovery Procedures

```typescript
class PersistenceRecovery {
  /**
   * Recovery procedures for various failure scenarios
   */

  async recoverFromDiskFull(): Promise<void> {
    // 1. Disable AOF temporarily
    // redis-cli CONFIG SET appendonly no
    
    // 2. Remove old backups or logs
    // rm /var/log/redis/*.log
    
    // 3. Free up disk space
    // docker system prune -a
    
    // 4. Re-enable AOF
    // redis-cli CONFIG SET appendonly yes
  }

  async recoverFromCorruptedAof(): Promise<void> {
    // 1. Enable truncated loading
    // redis-cli CONFIG SET aof-load-truncated yes
    
    // 2. Try starting Redis
    // systemctl start redis
    
    // 3. If still failing, rebuild AOF from RDB
    // redis-cli BGREWRITEAOF
  }

  async rebuildAofFromRdb(): Promise<void> {
    // 1. Stop Redis
    // systemctl stop redis
    
    // 2. Move old AOF
    // mv appendonly.aof appendonly.aof.old
    
    // 3. Start Redis (will create new AOF)
    // systemctl start redis
    
    // 4. Wait for data to load from RDB
    // sleep 10
    
    // 5. Trigger AOF rewrite
    // redis-cli BGREWRITEAOF
  }
}
```

## 9. Best Practices

### 9.1 Configuration Checklist

```conf
# Persistence Configuration Checklist

# 1. Choose persistence strategy based on requirements:
# - Pure cache: No persistence
# - Moderate durability: AOF everysec
# - High durability: AOF always + RDB backup
# - Maximum safety: AOF always + replication

# 2. Memory configuration
maxmemory <50% of available RAM>
maxmemory-policy allkeys-lru
maxmemory-samples 5

# 3. System tuning
vm.overcommit_memory = 1
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# 4. Disk configuration
# Use SSD for persistence
# Separate disk for data and logs
# Monitor disk I/O

# 5. Monitoring
# - Persistence errors
# - Fork duration
# - AOF/RDB sizes
# - Memory fragmentation
```

### 9.2 Backup Strategy

```typescript
class BackupStrategy {
  /**
   * Recommended backup schedule:
   * 
   * Hourly: (optional) Quick RDB for recent data
   * Daily: RDB backup + AOF preserved
   * Weekly: Full RDB + AOF backup
   * 
   * Retention:
   * - Hourly: Keep 24 hours
   * - Daily: Keep 7 days
   * - Weekly: Keep 4 weeks
   * - Monthly: Keep 12 months
   */

  async createBackupStrategy(redis: Redis): Promise<BackupSchedule> {
    return {
      hourly: {
        enabled: false, // Optional for busy systems
        type: 'RDB',
        retention: 24,
      },
      daily: {
        enabled: true,
        type: 'RDB',
        time: '02:00', // Off-peak hours
        retention: 7,
      },
      weekly: {
        enabled: true,
        type: 'RDB + AOF',
        day: 'Sunday',
        time: '03:00',
        retention: 4,
      },
      monthly: {
        enabled: true,
        type: 'RDB + AOF',
        day: 1,
        time: '04:00',
        retention: 12,
      },
    };
  }
}
```

## 10. References

- [Redis Persistence Documentation](https://redis.io/docs/management/persistence/)
- [Redis Persistence Explained](https://redis.io/topics/persistence)
- [RDB Internals](https://redis.io/topics/internals-rdb)
- [AOF Internals](https://redis.io/topics/internals-aof)
- [Redis Persistence Patterns](https://redis.io/docs/management/optimization/persistence/)
- [Redis Best Practices - Persistence](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/RedisPersistence.html)
