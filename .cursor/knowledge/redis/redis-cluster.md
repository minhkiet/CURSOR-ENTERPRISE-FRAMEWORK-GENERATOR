---
title: "Redis Cluster"
description: "Hướng dẫn toàn diện về Redis Cluster mode bao gồm hash slots, sharding, failover, resharding, replica propagation và cluster management trong môi trường enterprise"
tags: ["redis", "cluster", "hash-slots", "sharding", "failover", "replication", "high-availability"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis Cluster

## 1. Tổng Quan (Overview)

Redis Cluster là giải pháp sharding tự động của Redis, cho phép phân chia data across multiple Redis nodes mà không cần external sharding logic hoặc proxy. Đây là giải pháp lý tưởng cho các hệ thống enterprise cần horizontal scalability và high availability.

Trong kiến trúc Redis Cluster, dữ liệu được chia thành 16,384 hash slots (0-16383). Mỗi master node trong cluster chịu trách nhiệm cho một tập hợp các slots, và Redis tự động phân phối slots này across cluster. Khi một node fail, replicas sẽ tự động promote để đảm bảo availability mà không cần manual intervention.

Redis Cluster cung cấp khả năng chịu lỗi tự động thông qua replica promotion, đồng thời cho phép read scaling thông qua việc redirect reads đến replicas. Tuy nhiên, đổi lại, cluster yêu cầu client phải hỗ trợ cluster-aware operations và hiểu cách routing keys đến đúng nodes.

## 2. Mục Đích (Purpose)

### 2.1 Horizontal Scalability

Redis Cluster cho phép mở rộng cluster bằng cách thêm nodes mới. Data được automatically redistributed across new nodes mà không cần downtime. Điều này đặc biệt quan trọng khi data volume tăng theo thời gian.

### 2.2 High Availability

Với built-in replica promotion, Redis Cluster có thể tự động recover từ node failures mà không cần manual intervention. Cluster tiếp tục operate ở degraded mode cho đến khi failed node được repair hoặc replaced.

### 2.3 Performance

Bằng cách sharding data across nhiều nodes, Redis Cluster cho phép:
- Linear write scalability: Writes được distribute across cluster
- Read scaling: Reads có thể được serve từ replicas
- Reduced latency: Data được place gần users/ applications

### 2.4 Data Distribution

Cluster đảm bảo mỗi key được store trên chính xác một master node (không có cross-slot transactions trong cluster mode). Điều này đơn giản hóa data model nhưng đòi hỏi application phải design data access patterns phù hợp.

## 3. Kiến Trúc Cluster (Cluster Architecture)

### 3.1 Hash Slot Calculation

```typescript
/**
 * Redis Cluster sử dụng CRC16 modulo 16384 để determine slot cho mỗi key
 * Slot = CRC16(key) % 16384
 */

function getHashSlot(key: string): number {
  // CRC16 implementation for Redis
  let crc = 0;
  for (let i = 0; i < key.length; i++) {
    crc = (crc << 8) ^ crc16Table[(crc >> 8) ^ key.charCodeAt(i)];
  }
  return crc % 16384;
}

// Ví dụ: Key routing
// Key: "user:12345:profile"
// Slot: CRC16("user:12345:profile") % 16384 = 1234 (ví dụ)
```

### 3.2 Cluster Topology

```
                    ┌─────────────────────────────────┐
                    │      Cluster Topology            │
                    │    6 Nodes (3M + 3S)             │
                    └─────────────────────────────────┘

    ┌───────────────┐                    ┌───────────────┐
    │  Master Node A │◄─────replica──────│  Slave Node A' │
    │  Slots: 0-5460 │                    │  (Read-only)  │
    └───────────────┘                    └───────────────┘
            ▲                                    ▲
            │                                    │
            ▼                                    ▼
    ┌───────────────┐                    ┌───────────────┐
    │  Master Node B │◄─────replica──────│  Slave Node B' │
    │ Slots: 5461-10922│                  │  (Read-only)  │
    └───────────────┘                    └───────────────┘
            ▲                                    ▲
            │                                    │
            ▼                                    ▼
    ┌───────────────┐                    ┌───────────────┐
    │  Master Node C │◄─────replica──────│  Slave Node C' │
    │ Slots: 10923-16383│                │  (Read-only)  │
    └───────────────┘                    └───────────────┘
```

### 3.3 Node Communication

```redis
# Các node giao tiếp qua TCP port (base port + 10000)
# Ví dụ: Master on 6379, Cluster bus on 16379

# Node gửi PING messages mỗi interval để detect failures
CLUSTER MEET <ip> <port> <bus-port>

# Thông tin cluster qua CLI
CLUSTER NODES
CLUSTER INFO
CLUSTER SLOTS
```

## 4. Hash Slots Chi Tiết

### 4.1 Slot Distribution

```typescript
// Ví dụ về cách Redis Cluster distribute slots
interface SlotAssignment {
  slotNumber: number;
  masterNode: string;
  replicaNodes: string[];
}

// 16,384 slots được chia đều cho các masters
// Với 3 masters: mỗi master ~5461 slots
// Với 6 masters: mỗi master ~2730 slots

class SlotDistribution {
  calculateSlotsPerNode(numMasters: number): number {
    return Math.floor(16384 / numMasters);
  }
  
  getSlotRange(masterIndex: number, numMasters: number): [number, number] {
    const slotsPerNode = this.calculateSlotsPerNode(numMasters);
    const start = masterIndex * slotsPerNode;
    const end = start + slotsPerNode - 1;
    return [start, Math.min(end, 16383)];
  }
}

// Ví dụ với 3 masters
// Master 0: slots 0-5460
// Master 1: slots 5461-10922
// Master 2: slots 10923-16383
```

### 4.2 Key Tagging

```typescript
/**
 * Key tagging cho phép multi-key operations trong cluster
 * Chỉ có tag trong dấu {} được sử dụng để tính slot
 */

class KeyTagging {
  // Tag extraction regex
  private static TAG_REGEX = /\{([^}]+)\}/;
  
  static getSlot(key: string): number {
    const match = key.match(this.TAG_REGEX);
    const tag = match ? match[1] : key;
    return this.calculateCRC16(tag) % 16384;
  }
  
  // Examples:
  // "user:{123}:profile" -> tag: "123" -> slot calculated from "123"
  // "user:123:profile" -> no tag -> slot calculated from full key
  // "{user}:profile:sessions" -> tag: "user" -> slot calculated from "user"
  
  // Multi-key operation với same tag:
  // MSET user:{123}:name "John" user:{123}:email "john@example.com"
  // Cả hai keys đều cùng slot, nên operation thành công
}

// Bad pattern - keys across different slots
// MSET user:123:profile "John" user:456:profile "Jane"
// Key tags khác nhau -> slots khác nhau -> ERROR in cluster mode

// Good pattern - keys across different slots  
// MSET user:profile:123 "John" user:profile:456 "Jane"
// Cùng prefix nhưng khác IDs
```

### 4.3 Cross-Slot Operations

```typescript
/**
 * Redis Cluster có hạn chế với cross-slot operations
 * Một số operations được phép, một số không
 */

// Operations được phép (single-slot):
// GET, SET, MGET (nếu cùng slot), MSET (nếu cùng slot)
// HGET, HSET, HMGET, HMSET (nếu cùng slot)

// Operations không được phép (multi-slot):
// KEYS pattern (scan toàn bộ cluster)
// FLUSHDB (xóa toàn bộ cluster)
// SUNION, SINTER, SDIFF của keys từ slots khác nhau

// Giải pháp: Sử dụng pipeline với hash tags
class ClusterAwareClient {
  async msetWithSameTag(
    redis: Redis.Cluster,
    keyTag: string,
    pairs: Record<string, string>
  ): Promise<void> {
    const keys = Object.keys(pairs).map(k => `{${keyTag}}:${k}`);
    const values = Object.values(pairs);
    
    // All keys có cùng tag -> cùng slot
    await redis.mset(...keys.flatMap((k, i) => [k, values[i]]));
  }
}
```

## 5. Replication

### 5.1 Replication Architecture

```typescript
interface ReplicationConfig {
  masterHost: string;
  masterPort: number;
  masterPassword?: string;
  replicaOf?: { host: string; port: number }; // For replica mode
}

class RedisReplication {
  private role: 'master' | 'replica';
  private connectedSlaves: number;
  private replOffset: number;
  
  async configureReplication(config: ReplicationConfig): Promise<void> {
    if (config.replicaOf) {
      // Configure as replica
      await this.redis.replicaof(
        config.replicaOf.host, 
        config.replicaOf.port
      );
    } else {
      // Configure as master
      await this.redis.replicaof('NO', 'ONE');
    }
  }
  
  async getReplicationInfo(): Promise<ReplicationInfo> {
    const info = await this.redis.info('replication');
    return this.parseReplicationInfo(info);
  }
}

interface ReplicationInfo {
  role: string;
  connectedSlaves: number;
  masterReplOffset: number;
  replBacklogActive: number;
  replBacklogSize: number;
  replBacklogHistLen: number;
  replBacklogFirstByteOffset: number;
}
```

### 5.2 Replica Configuration

```redis
# Trong redis.conf - Replica configuration

# Master configuration (on master node)
bind 0.0.0.0
port 6379
requirepass "master_password_here"

# Replica configuration (on replica nodes)
replicaof 10.0.1.1 6379
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-ping-replica-period 10
repl-timeout 60
repl-disable-tcp-nodelay no
replica-priority 100
```

### 5.3 Replication Sync Types

```typescript
/**
 * Redis replication supports two sync types:
 * 1. Full sync (SYNC): Master creates RDB snapshot, sends to replica
 * 2. Partial sync (PSYNC): Master sends only incremental changes
 */

enum SyncType {
  FULL_SYNC = 'FULL',
  PARTIAL_SYNC = 'PARTIAL',
  NONE = 'NONE'
}

interface SyncStatus {
  type: SyncType;
  masterRunId: string;
  offset: number;
}

// Full sync happens when:
// - Replica connects for first time
// - Replica lost connection and PSYNC fails
// - Master was restarted without persistence

// Partial sync happens when:
// - Replica disconnected briefly
// - Repl backlog buffer has enough history
```

### 5.4 Replica Promotion

```typescript
/**
 * Khi master fail, replica được promote tự động
 * Quá trình này được gọi là failover
 */

class ClusterFailover {
  async initiateFailover(failedMaster: string): Promise<void> {
    // 1. Replica detects master failure
    const isMasterReachable = await this.checkMasterHealth(failedMaster);
    
    if (!isMasterReachable) {
      // 2. Wait for failover timeout
      const failoverTimeout = 5000; // ms
      await this.delay(failoverTimeout);
      
      // 3. Verify no other replica will promote
      const promotionClaimed = await this.claimPromotion();
      
      if (!promotionClaimed) {
        // Wait and retry
        return;
      }
      
      // 4. Promote self to master
      await this.promoteToMaster();
      
      // 5. Update cluster configuration
      await this.broadcastNewConfiguration();
    }
  }
  
  private async claimPromotion(): Promise<boolean> {
    // Sử dụng CLUSTER FAILOVER với CHOOSE option
    // Hoặc đợi election timeout và win election
    return true;
  }
}
```

## 6. Cluster Management

### 6.1 Creating a Cluster

```bash
# Sử dụng redis-cli để tạo cluster
redis-cli --cluster create \
  10.0.1.1:6379 \
  10.0.1.2:6379 \
  10.0.1.3:6379 \
  10.0.1.4:6379 \
  10.0.1.5:6379 \
  10.0.1.6:6379 \
  --cluster-replicas 1

# Output:
# >>> Creating cluster
# >>> Performing hash slots allocation on 6 nodes...
# >>> Master[0] -> Slots[0-5460]
# >>> Master[1] -> Slots[5461-10922]
# >>> Master[2] -> Slots[10923-16383]
# >>> Adding replica 10.0.1.4:6379 to Master[0]
# >>> Adding replica 10.0.1.5:6379 to Master[1]
# >>> Adding replica 10.0.1.6:6379 to Master[2]
# >>> Can I set the above configuration? (type 'yes' to accept): yes
```

### 6.2 Cluster Node Management

```redis
# Add new node to cluster
CLUSTER MEET 10.0.1.7 6379

# Remove node from cluster (gracefully)
CLUSTER FORGET <node-id>

# Shutdown node
CLUSTER SAVECONFIG

# Reshard slots between nodes
CLUSTER SETSLOT <slot> <node-id>
CLUSTER SETSLOT <slot> MIGRATING <node-id>
CLUSTER SETSLOT <slot> IMPORTING <node-id>

# Check cluster status
CLUSTER INFO
# cluster_state:ok
# cluster_slots_assigned:16384
# cluster_slots_ok:16384
# cluster_slots_pfail:0
# cluster_size:3
# cluster_known_nodes:6
# cluster_my_epoch:0
# cluster_stats_messages_ping_sent:12345
# cluster_stats_messages_pong_sent:12345
```

### 6.3 Python Cluster Client

```python
import redis
from redis.cluster import RedisCluster

class RedisClusterManager:
    """
    Manager for Redis Cluster operations
    """
    
    def __init__(self, startup_nodes: list):
        self.rc = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True,
            skip_full_coverage_check=True
        )
    
    def get_node_for_key(self, key: str) -> str:
        """Get the node that holds the slot for this key"""
        return self.rc.get_node(key)
    
    def get_slot_for_key(self, key: str) -> int:
        """Calculate slot for a key"""
        return self.rc.keyslot(key)
    
    def get_all_slots(self) -> dict:
        """Get all slots and their master nodes"""
        return self.rc.slots()
    
    def execute_across_slots(self, command: str, keys: list) -> dict:
        """
        Execute command across multiple slots
        Returns results grouped by slot
        """
        # Group keys by slot
        slot_groups = {}
        for key in keys:
            slot = self.get_slot_for_key(key)
            if slot not in slot_groups:
                slot_groups[slot] = []
            slot_groups[slot].append(key)
        
        # Execute per slot
        results = {}
        for slot, slot_keys in slot_groups.items():
            if command.upper() == 'MGET':
                results[slot] = self.rc.mget(slot_keys)
            elif command.upper() == 'MSET':
                results[slot] = self.rc.mset(*slot_keys)
            else:
                results[slot] = [self.rc.execute_command(command, k) for k in slot_keys]
        
        return results
    
    def migrate_keys(
        self, 
        source_node: str, 
        target_node: str, 
        slots: list
    ) -> dict:
        """
        Migrate slots from source to target node
        """
        migrated = {'success': [], 'failed': []}
        
        for slot in slots:
            try:
                # Set slot to importing state on target
                self.rc.set_slot(slot, 'importing', source_node)
                
                # Move keys
                self.move_slot(slot, source_node, target_node)
                
                # Set slot to node on target
                self.rc.set_slot(slot, 'node', target_node)
                
                migrated['success'].append(slot)
            except Exception as e:
                migrated['failed'].append({'slot': slot, 'error': str(e)})
        
        return migrated


# Usage
if __name__ == "__main__":
    manager = RedisClusterManager([
        {'host': '10.0.1.1', 'port': 6379},
        {'host': '10.0.1.2', 'port': 6379},
        {'host': '10.0.1.3', 'port': 6379},
    ])
    
    # Get slot for a key
    slot = manager.get_slot_for_key("user:123:profile")
    print(f"Key 'user:123:profile' is in slot {slot}")
    
    # Get node for a key
    node = manager.get_node_for_key("user:123:profile")
    print(f"Key 'user:123:profile' is on node {node}")
```

### 6.4 TypeScript Cluster Client

```typescript
import Redis from 'ioredis';

class RedisClusterClient {
  private cluster: Redis.Cluster;
  private readonly startupNodes = [
    { host: '10.0.1.1', port: 6379 },
    { host: '10.0.1.2', port: 6379 },
    { host: '10.0.1.3', port: 6379 },
  ];

  constructor() {
    this.cluster = new Redis.Cluster(this.startupNodes, {
      redisOptions: {
        password: process.env.REDIS_PASSWORD,
        enableReadyCheck: true,
        maxRetriesPerRequest: 3,
      },
      slotsRefreshTimeout: 60000,
      slotsRefreshInterval: 60000,
      clusterRetryStrategy: (times) => {
        const delay = Math.min(times * 100, 3000);
        return delay;
      },
    });

    this.cluster.on('error', (err) => {
      console.error('Cluster error:', err);
    });

    this.cluster.on('reconnecting', () => {
      console.log('Reconnecting to cluster...');
    });
  }

  async getSlotForKey(key: string): Promise<number> {
    return this.cluster.keyslot(key);
  }

  async getNodeForKey(key: string): Promise<string> {
    const node = this.cluster.getNodeByKey(key);
    return node ? `${node.host}:${node.port}` : 'unknown';
  }

  async executePipeline(
    commands: Array<[string, ...any[]]>
  ): Promise<any[]> {
    const pipeline = this.cluster.pipeline();
    
    commands.forEach(([command, ...args]) => {
      pipeline[command](...args);
    });

    return pipeline.exec();
  }

  async msetSafe(keyValuePairs: Record<string, string>): Promise<void> {
    // Group keys by slot
    const slotGroups = new Map<number, [string, string][]>();
    
    for (const [key, value] of Object.entries(keyValuePairs)) {
      const slot = await this.getSlotForKey(key);
      if (!slotGroups.has(slot)) {
        slotGroups.set(slot, []);
      }
      slotGroups.get(slot)!.push([key, value]);
    }

    // Execute MSET per slot
    for (const [, pairs] of slotGroups) {
      const flatArgs = pairs.flatMap(([k, v]) => [k, v]);
      await this.cluster.mset(...flatArgs);
    }
  }

  async healthCheck(): Promise<ClusterHealth> {
    const nodes = await this.cluster.nodes('master');
    const results = await Promise.all(
      nodes.map(async (node) => {
        try {
          const info = await node.info();
          return { node: `${node.host}:${node.port}`, status: 'ok', info };
        } catch (error) {
          return { 
            node: `${node.host}:${node.port}`, 
            status: 'error', 
            error: String(error) 
          };
        }
      })
    );

    return {
      timestamp: new Date().toISOString(),
      nodes: results,
      healthyCount: results.filter(r => r.status === 'ok').length,
      totalCount: results.length,
    };
  }
}

interface ClusterHealth {
  timestamp: string;
  nodes: Array<{
    node: string;
    status: 'ok' | 'error';
    info?: string;
    error?: string;
  }>;
  healthyCount: number;
  totalCount: number;
}
```

## 7. Failover và High Availability

### 7.1 Automatic Failover

```typescript
/**
 * Redis Cluster automatic failover process:
 * 
 * 1. Failure Detection:
 *    - Node sends PINGs to other nodes
 *    - If no PONG received for (node-timeout * failover-timeout-factor) / 2
 *    - Node marked as PFAIL (possible failure)
 * 
 * 2. Election:
 *    - Replicas with PFAIL masters participate in election
 *    - Replica sends FAILOVER_AUTH_REQUEST to all masters
 *    - Masters vote with FAILOVER_AUTH_ACK
 *    - Quorum: (cluster_nodes / 2) + 1 votes needed
 * 
 * 3. Failover Execution:
 *    - New epoch increased
 *    - Wait for replication offset to catch up
 *    - Promote self as new master
 *    - Broadcast PONG to cluster
 */

interface FailoverConfig {
  clusterNodeTimeout: number;
  clusterReplicaValidityFunc: string;
  clusterMigrationBarrier: number;
  clusterFailoverTimeout: number;
}

class AutomaticFailover {
  async detectAndFailover(
    cluster: Redis.Cluster,
    failedNodeId: string
  ): Promise<void> {
    // 1. Verify failure is confirmed
    const clusterInfo = await cluster.cluster('info');
    const pfailNodes = clusterInfo.match(/cluster_slots_pfail:(\d+)/)?.[1];
    
    if (parseInt(pfailNodes || '0') > 0) {
      console.log('Possible failure detected, initiating failover');
    }

    // 2. Check if replica is eligible
    const replicaInfo = await cluster.cluster('nodes');
    // Parse replica info to verify master is down

    // 3. Wait for failover timeout (default 5s)
    await this.delay(5000);

    // 4. Initiate failover
    const replicaNodes = await cluster.nodes('replica', failedNodeId);
    if (replicaNodes.length > 0) {
      const electedReplica = replicaNodes[0];
      await electedReplica.cluster('failover', 'force');
    }
  }
}
```

### 7.2 Manual Failover

```redis
# Manual failover - graceful promotion
# Useful for maintenance windows

# On replica node, initiate manual failover
CLUSTER FAILOVER [TIMEOUT <ms>] [FORCE] [TAKEOVER]

# TIMEOUT: Max time to wait for replicas to sync (default 5s)
# FORCE: Skip confirmation from other masters
# TAKEOVER: Skip election (use for manual interventions)

# Example: Graceful failover during maintenance
# 1. Replicate latest data to replica
# 2. On replica: CLUSTER FAILOVER
# 3. Old master becomes replica
# 4. Perform maintenance on old master
# 5. After maintenance: CLUSTER FAILOVER to promote back
```

### 7.3 Cluster Monitoring

```typescript
class ClusterMonitor {
  private redis: Redis;
  private alertThresholds = {
    minSlaves: 1,
    maxLatency: 100, // ms
    minMemoryAvailable: 1024 * 1024 * 1024, // 1GB
  };

  async monitor(): Promise<MonitoringReport> {
    const [clusterInfo, nodes, slots] = await Promise.all([
      this.redis.cluster('info'),
      this.redis.cluster('nodes'),
      this.redis.cluster('slots'),
    ]);

    const nodeReports = await this.analyzeNodes(nodes);
    const slotReports = await this.analyzeSlots(slots);

    return {
      timestamp: new Date().toISOString(),
      clusterState: this.extractField(clusterInfo, 'cluster_state'),
      slotsAssigned: this.extractField(clusterInfo, 'cluster_slots_assigned'),
      slotsOk: this.extractField(clusterInfo, 'cluster_slots_ok'),
      nodes: nodeReports,
      slots: slotReports,
      alerts: this.generateAlerts(nodeReports, slotReports),
    };
  }

  private async analyzeNodes(nodesOutput: string): Promise<NodeReport[]> {
    const lines = nodesOutput.split('\n').filter(l => l.trim());
    
    return Promise.all(lines.map(async (line) => {
      const parts = line.split(' ');
      const [nodeId, address, flags, masterId, pingSent, pongRecv, epoch, connected] = parts;
      
      return {
        nodeId,
        address,
        role: flags.includes('master') ? 'master' : 'replica',
        masterId: masterId !== '-' ? masterId : null,
        connected: connected === 'connected',
        latency: parseInt(pongRecv) - parseInt(pingSent),
      };
    }));
  }

  private generateAlerts(
    nodes: NodeReport[],
    slots: SlotReport[]
  ): Alert[] {
    const alerts: Alert[] = [];

    // Check for disconnected nodes
    const disconnected = nodes.filter(n => !n.connected);
    if (disconnected.length > 0) {
      alerts.push({
        severity: 'critical',
        message: `${disconnected.length} node(s) disconnected`,
        affectedNodes: disconnected.map(n => n.address),
      });
    }

    // Check for slots without masters
    const orphanedSlots = slots.filter(s => !s.master);
    if (orphanedSlots.length > 0) {
      alerts.push({
        severity: 'critical',
        message: `${orphanedSlots.length} slots have no master`,
        affectedSlots: orphanedSlots.map(s => s.slot),
      });
    }

    return alerts;
  }
}
```

## 8. Resharding và Migration

### 8.1 Online Resharding

```typescript
/**
 * Redis Cluster hỗ trợ online resharding - không cần downtime
 * Sử dụng MIGRATE command và slot state management
 */

class ClusterResharder {
  private cluster: Redis.Cluster;

  async moveSlot(
    slot: number,
    sourceNodeId: string,
    targetNodeId: string
  ): Promise<void> {
    // 1. Set slot to MIGRATING state on source
    await this.cluster.cluster('setslot', slot, 'MIGRATING', targetNodeId);

    // 2. Set slot to IMPORTING state on target
    await this.cluster.cluster('setslot', slot, 'IMPORTING', sourceNodeId);

    // 3. Migrate all keys in the slot
    await this.migrateSlotKeys(slot, sourceNodeId, targetNodeId);

    // 4. Set slot to NODE state on target
    await this.cluster.cluster('setslot', slot, 'node', targetNodeId);
  }

  private async migrateSlotKeys(
    slot: number,
    sourceId: string,
    targetId: string
  ): Promise<void> {
    // Get all keys in this slot
    const keys = await this.getKeysInSlot(slot);
    
    for (const key of keys) {
      // MIGRATE is atomic and handles key deletion from source
      await this.cluster.migrate(
        this.getNodeHost(targetId),
        this.getNodePort(targetId),
        key,
        0, // destination db
        5000 // timeout ms
      );
    }
  }

  private async getKeysInSlot(slot: number): Promise<string[]> {
    const keys: string[] = [];
    let cursor = '0';
    
    do {
      const [newCursor, batch] = await this.cluster.cluster('scan', cursor, 'MATCH', '*', 'COUNT', '1000');
      cursor = newCursor;
      
      // Filter keys belonging to this slot
      for (const key of batch) {
        if (this.getSlotForKey(key) === slot) {
          keys.push(key);
        }
      }
    } while (cursor !== '0');
    
    return keys;
  }
}
```

### 8.2 Automatic Rebalancing

```bash
# Sử dụng redis-cli để rebalance cluster
redis-cli --cluster rebalance \
  --cluster-use-empty-masters \
  10.0.1.1:6379

# Rebalance với weight cho từng node
redis-cli --cluster rebalance \
  --cluster-weight node1=5 node2=3 node3=2 \
  10.0.1.1:6379

# Check slot distribution
redis-cli --cluster info 10.0.1.1:6379
redis-cli --cluster slots 10.0.1.1:6379
```

### 8.3 Migration Best Practices

```typescript
/**
 * Best practices cho cluster migration:
 * 
 * 1. Always use odd number of masters (3, 5, 7)
 * 2. Each master should have at least 1 replica
 * 3. Spread replicas across availability zones
 * 4. Test failover scenarios before production
 * 5. Monitor cluster during migration
 */

class MigrationBestPractices {
  // Recommended cluster sizes
  static readonly CLUSTER_SIZES = {
    MINIMAL: { masters: 3, replicasPerMaster: 1 },
    STANDARD: { masters: 6, replicasPerMaster: 1 },
    HIGH_AVAILABILITY: { masters: 6, replicasPerMaster: 2 },
    ENTERPRISE: { masters: 9, replicasPerMaster: 2 },
  };

  // Cross-AZ distribution
  static getNodeDistribution(
    clusterSize: 'STANDARD' | 'HIGH_AVAILABILITY' | 'ENTERPRISE'
  ): Map<string, number[]> {
    const azs = ['us-east-1a', 'us-east-1b', 'us-east-1c'];
    
    if (clusterSize === 'STANDARD') {
      // 3 masters, 3 replicas
      return new Map([
        ['us-east-1a', [0, 1]], // Masters 0,1; Replica for 2
        ['us-east-1b', [2]],    // Master 2; Replicas for 0,1
        ['us-east-1c', []],     // Replicas for all
      ]);
    }
    
    // Similar logic for other sizes
    return new Map();
  }
}
```

## 9. Cluster Configuration

### 9.1 Production Configuration

```conf
# redis.conf - Production Cluster Configuration

# Cluster mode
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 15000
cluster-replica-validity-factor 10
cluster-migration-barrier 1
cluster-require-full-coverage yes
cluster-preferred-endpoint-type ip

# Network
bind 0.0.0.0
protected-mode no
port 6379
tcp-backlog 511
timeout 300

# Memory
maxmemory 8gb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Persistence
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data

# Replication
min-replicas-to-write 1
min-replicas-max-lag 10

# Security
requirepass "your-password-here"
masterauth "your-password-here"

# Logging
loglevel notice
logfile /var/log/redis/redis.log

# Performance
tcp-keepalive 300
```

### 9.2 Client Configuration

```typescript
// ioredis cluster options
const clusterOptions = {
  // Seed nodes
  redisOptions: {
    host: '10.0.1.1',
    port: 6379,
    password: process.env.REDIS_PASSWORD,
    
    // Connection pool
    connectTimeout: 10000,
    maxRetriesPerRequest: 3,
    
    // TLS
    tls: {
      cert: fs.readFileSync('./client.crt'),
      key: fs.readFileSync('./client.key'),
      ca: fs.readFileSync('./ca.crt'),
    },
  },
  
  // Cluster settings
  clusterRetryStrategy: (times: number) => {
    const delay = Math.min(times * 100, 3000);
    const jitter = Math.random() * 100;
    return delay + jitter;
  },
  
  slotsRefreshTimeout: 60000,
  slotsRefreshInterval: 60000,
  enableReadyCheck: true,
  scaleReads: 'master', // or 'replicas', 'all'
  maxRedirection: 16,
  
  // Discovery
  enableAutoDiscovery: true,
};
```

## 10. Troubleshooting

### 10.1 Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Cluster not forming | Nodes can't meet | Check network connectivity, ports (6379, 16379) |
| Slot migration stuck | Key not accessible | Check MIGRATE timeout, restart migration |
| Failover not working | Replica not promoting | Check election quorum, replica priority |
| MOVED error loop | Client routing issues | Verify cluster configuration, client version |
| Memory full | OOM errors | Adjust maxmemory, eviction policy |

### 10.2 Diagnostic Commands

```redis
# Cluster health
CLUSTER INFO
CLUSTER NODES
CLUSTER SLOTS
CLUSTER KEYSINSLOT <slot> <count>

# Node diagnostics
PING
ECHO "test"
DEBUG SLEEP 1
DEBUG SEGFAULT

# Key diagnostics
DUMP <key>
TYPE <key>
TTL <key>
OBJECT ENCODING <key>

# Slow operations
SLOWLOG GET 10
COMMAND INFO GET *
```

### 10.3 Recovery Procedures

```typescript
/**
 * Recovery procedures for various failure scenarios
 */

class ClusterRecovery {
  
  /**
   * Recover from split-brain scenario
   * When cluster partitions into multiple sub-clusters
   */
  async recoverSplitBrain(): Promise<void> {
    // 1. Identify the largest partition (should be primary)
    // 2. Shutdown nodes in smaller partitions
    // 3. Restart nodes and join primary cluster
    // 4. Use CLUSTER MEET to rejoin
    // 5. Verify data integrity
  }

  /**
   * Recover from total cluster failure
   * When all nodes are down
   */
  async recoverTotalFailure(snapshotPath: string): Promise<void> {
    // 1. Restore from latest RDB/AOF backup
    // 2. Start masters first
    // 3. Start replicas with --appendonly yes
    // 4. Verify replication
    // 5. Gradually restart applications
  }

  /**
   * Add new node to replace failed node
   */
  async replaceNode(failedNodeId: string, newNodeAddress: string): Promise<void> {
    // 1. Add new node to cluster
    // 2. Configure as replica of failed node's master
    // 3. Wait for sync
    // 4. Update slot assignment if needed
    // 5. Remove failed node from cluster
  }
}
```

## 11. Best Practices

### 11.1 Design Guidelines

```typescript
// 1. Data Model Design
class DataModelGuidelines {
  // Use hash tags for related keys
  static GOOD_PATTERNS = [
    'session:{userId}:data',
    'session:{userId}:tokens',
    'cart:{userId}:items',
  ];
  
  // Avoid keys without tags when using multi-key ops
  static BAD_PATTERNS = [
    'user_{userId}_profile',
    'product-{productId}-details',
  ];
  
  // Multi-key operations only when necessary
  static shouldUseMultiKey(keyCount: number): boolean {
    return keyCount <= 100; // Limit for cluster
  }
}

// 2. Connection Management
class ConnectionGuidelines {
  // Use connection pooling per node
  static recommendedPoolSize = 50;
  
  // Max commands in pipeline
  static maxPipelineCommands = 1000;
  
  // Retry configuration
  static maxRetries = 3;
  static retryDelay = 100; // ms
}

// 3. Monitoring Checklist
const MONITORING_CHECKLIST = {
  daily: [
    'cluster_slots_assigned',
    'cluster_slots_ok',
    'connected_slaves',
    'keyspace_hits/misses',
  ],
  weekly: [
    'memory fragmentation',
    'slowlog analysis',
    'command stats',
    'network latency',
  ],
  monthly: [
    'capacity planning',
    'backup verification',
    'disaster recovery test',
    'security audit',
  ],
};
```

### 11.2 Capacity Planning

```typescript
interface CapacityPlan {
  currentNodes: number;
  currentMemoryGB: number;
  expectedGrowth: number; // per month
  peakLoadMultiplier: number;
  redundancyFactor: number;
}

function calculateClusterSize(plan: CapacityPlan): ClusterPlan {
  const monthlyGrowthRate = plan.expectedGrowth / 100;
  const projectedDataGB = plan.currentMemoryGB * (1 + monthlyGrowthRate * 12);
  const peakMemoryGB = projectedDataGB * plan.peakLoadMultiplier;
  const totalWithRedundancy = peakMemoryGB * plan.redundancyFactor;
  
  // Each node: 8GB memory, ~2700 slots (with 6 nodes)
  const memoryPerNodeGB = 8;
  const nodesNeeded = Math.ceil(totalWithRedundancy / memoryPerNodeGB);
  
  // Round up to odd number
  const mastersNeeded = nodesNeeded % 2 === 0 ? nodesNeeded + 1 : nodesNeeded;
  
  return {
    totalNodes: mastersNeeded * 2, // With replicas
    masters: mastersNeeded,
    replicas: mastersNeeded,
    estimatedMemoryPerNode: totalWithRedundancy / mastersNeeded,
    projectedCapacityGB: totalWithRedundancy,
  };
}
```

## 12. References

- [Redis Cluster Specification](https://redis.io/docs/management/scaling/)
- [Redis Cluster Tutorial](https://redis.io/docs/getting-started/cluster/)
- [Redis Cluster Security](https://redis.io/docs/management/security/)
- [Redis Topology](https://redis.io/docs/management/optimization/cluster-tutorial/)
- [Redis Sentinel vs Cluster](https://redis.io/docs/management/replication/)
