---
title: "Redis OM for Node.js"
description: "Hướng dẫn toàn diện về Redis OM (Object Mapper) cho Node.js/TypeScript bao gồm @redis/client, ioredis, index definitions, Hash models, full-text search với RediSearch, và best practices cho enterprise applications"
tags: ["redis", "redis-om", "ioredis", "nodejs", "typescript", "redis-search", "rediserach", "object-mapper"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis OM for Node.js

## 1. Tổng Quan (Overview)

Redis OM (Object Mapper) là một thư viện cho phép developers làm việc với Redis data structures sử dụng các abstraction level cao hơn, gần giống như làm việc với traditional ORM. Thay vì phải quản lý raw Redis commands, developers có thể define models, schemas, và relationships giống như trong các ORM quen thuộc.

Trong hệ sinh thái Node.js, có nhiều thư viện để làm việc với Redis:

1. **@redis/client** - Official Redis client từ Redis team
2. **ioredis** - Popular client với promise-based API và cluster support
3. **redis-om** - Object mapper cho Redis với repository pattern
4. **RediSearch module** - Module cho full-text search và secondary indexes

Bài viết này sẽ hướng dẫn chi tiết cách sử dụng các thư viện này để xây dựng enterprise applications với Redis.

## 2. @redis/client

### 2.1 Giới Thiệu

@redis/client là official Redis client được phát triển và maintain bởi Redis team. Nó cung cấp TypeScript support tuyệt vời và tuân thủ Redis API specification một cách chặt chẽ.

### 2.2 Installation và Setup

```bash
# Install @redis/client
npm install redis
# or
npm install @redis/client
```

### 2.3 Basic Connection

```typescript
import { createClient } from '@redis/client';

// Create client
const redis = createClient({
  url: 'redis://localhost:6379',
  // or for cluster mode
  // url: 'redis://localhost:6379,redis://localhost:6378',
});

// Event handlers
redis.on('error', (err) => {
  console.error('Redis Client Error:', err);
});

redis.on('connect', () => {
  console.log('Connected to Redis');
});

redis.on('ready', () => {
  console.log('Redis client ready');
});

// Connect
await redis.connect();

// Remember to disconnect on shutdown
process.on('SIGTERM', async () => {
  await redis.quit();
  process.exit(0);
});
```

### 2.4 Connection with TLS and Authentication

```typescript
import { createClient, RedisClientType } from '@redis/client';

interface RedisConfig {
  host: string;
  port: number;
  password?: string;
  tls?: boolean;
  database?: number;
}

async function createRedisClient(config: RedisConfig): Promise<RedisClientType> {
  const url = `${config.tls ? 'rediss' : 'redis'}://${
    config.password ? `:${config.password}@` : ''
  }${config.host}:${config.port}/${config.database || 0}`;

  const client = createClient({
    url,
    socket: {
      reconnectStrategy: (retries) => {
        if (retries > 10) {
          return new Error('Max reconnection attempts reached');
        }
        return Math.min(retries * 100, 3000);
      },
      keepAlive: 30000,
      connectTimeout: 10000,
    },
  });

  client.on('error', (err) => {
    console.error('Redis error:', err);
  });

  await client.connect();
  return client;
}

// Usage
const client = await createRedisClient({
  host: 'redis.example.com',
  port: 6379,
  password: process.env.REDIS_PASSWORD,
  tls: true,
  database: 0,
});
```

### 2.5 String Operations

```typescript
class StringOperations {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async set(key: string, value: string, options?: {
    ttlSeconds?: number;
    keepTTL?: boolean;
    setNX?: boolean;
    setXX?: boolean;
  }): Promise<void> {
    if (options?.ttlSeconds) {
      await this.redis.set(key, value, {
        EX: options.ttlSeconds,
        KEEPTTL: options.keepTTL,
        NX: options.setNX,
        XX: options.setXX,
      });
    } else {
      await this.redis.set(key, value);
    }
  }

  async get(key: string): Promise<string | null> {
    return this.redis.get(key);
  }

  async mSet(keyValues: Record<string, string>): Promise<void> {
    const args: string[] = [];
    for (const [key, value] of Object.entries(keyValues)) {
      args.push(key, value);
    }
    await this.redis.mSet(args);
  }

  async mGet(keys: string[]): Promise<(string | null)[]> {
    return this.redis.mGet(keys);
  }

  async setNX(key: string, value: string): Promise<boolean> {
    const result = await this.redis.setNX(key, value);
    return result === 'OK';
  }

  async incr(key: string): Promise<number> {
    return this.redis.incr(key);
  }

  async incrBy(key: string, increment: number): Promise<number> {
    return this.redis.incrBy(key, increment);
  }

  async incrByFloat(key: string, increment: number): Promise<number> {
    return this.redis.incrByFloat(key, increment);
  }

  async append(key: string, value: string): Promise<number> {
    return this.redis.append(key, value);
  }

  async getRange(key: string, start: number, end: number): Promise<string> {
    return this.redis.getRange(key, start, end);
  }

  async setRange(key: string, offset: number, value: string): Promise<number> {
    return this.redis.setRange(key, offset, value);
  }

  async strlen(key: string): Promise<number> {
    return this.redis.strlen(key);
  }
}
```

### 2.6 Hash Operations

```typescript
class HashOperations {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async hSet(key: string, fieldValues: Record<string, string | number>): Promise<number> {
    const args: string[] = [];
    for (const [field, value] of Object.entries(fieldValues)) {
      args.push(field, String(value));
    }
    return this.redis.hSet(key, args);
  }

  async hGet(key: string, field: string): Promise<string | null> {
    return this.redis.hGet(key, field);
  }

  async hGetAll(key: string): Promise<Record<string, string>> {
    const result = await this.redis.hGetAll(key);
    return result as Record<string, string>;
  }

  async hMSet(key: string, fieldValues: Record<string, string>): Promise<string> {
    const args: string[] = [];
    for (const [field, value] of Object.entries(fieldValues)) {
      args.push(field, value);
    }
    return this.redis.hMSet(key, args);
  }

  async hMGet(key: string, fields: string[]): Promise<(string | null)[]> {
    return this.redis.hMGet(key, fields);
  }

  async hExists(key: string, field: string): Promise<boolean> {
    return this.redis.hExists(key, field);
  }

  async hDel(key: string, ...fields: string[]): Promise<number> {
    return this.redis.hDel(key, fields);
  }

  async hLen(key: string): Promise<number> {
    return this.redis.hLen(key);
  }

  async hKeys(key: string): Promise<string[]> {
    return this.redis.hKeys(key);
  }

  async hVals(key: string): Promise<string[]> {
    return this.redis.hVals(key);
  }

  async hIncrBy(key: string, field: string, increment: number): Promise<number> {
    return this.redis.hIncrBy(key, field, increment);
  }

  async hIncrByFloat(key: string, field: string, increment: number): Promise<string> {
    return this.redis.hIncrByFloat(key, field, increment);
  }

  async hScan(
    key: string,
    cursor: number,
    options?: { MATCH?: string; COUNT?: number }
  ): Promise<[cursor: number, fields: string[]]> {
    const args: (string | number)[] = [key, cursor];
    if (options?.MATCH) {
      args.push('MATCH', options.MATCH);
    }
    if (options?.COUNT) {
      args.push('COUNT', options.COUNT);
    }
    return this.redis.hScan(args) as Promise<[cursor: number, fields: string[]]>;
  }
}
```

### 2.7 List Operations

```typescript
class ListOperations {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async lPush(key: string, ...values: string[]): Promise<number> {
    return this.redis.lPush(key, values);
  }

  async rPush(key: string, ...values: string[]): Promise<number> {
    return this.redis.rPush(key, values);
  }

  async lPop(key: string): Promise<string | null> {
    return this.redis.lPop(key);
  }

  async rPop(key: string): Promise<string | null> {
    return this.redis.rPop(key);
  }

  async bLPop(key: string, timeoutSeconds: number): Promise<[string, string] | null> {
    return this.redis.bLPop(key, timeoutSeconds);
  }

  async bRPop(key: string, timeoutSeconds: number): Promise<[string, string] | null> {
    return this.redis.bRPop(key, timeoutSeconds);
  }

  async lRange(key: string, start: number, stop: number): Promise<string[]> {
    return this.redis.lRange(key, start, stop);
  }

  async lIndex(key: string, index: number): Promise<string | null> {
    return this.redis.lIndex(key, index);
  }

  async lInsert(
    key: string,
    pivot: string,
    value: string,
    where: 'BEFORE' | 'AFTER'
  ): Promise<number> {
    return this.redis.lInsert(key, where, pivot, value);
  }

  async lLen(key: string): Promise<number> {
    return this.redis.lLen(key);
  }

  async lRem(key: string, count: number, value: string): Promise<number> {
    return this.redis.lRem(key, count, value);
  }

  async lSet(key: string, index: number, value: string): Promise<string> {
    return this.redis.lSet(key, index, value);
  }

  async lTrim(key: string, start: number, stop: number): Promise<string> {
    return this.redis.lTrim(key, start, stop);
  }

  async rPopLPush(source: string, destination: string): Promise<string | null> {
    return this.redis.rPopLPush(source, destination);
  }
}
```

### 2.8 Set Operations

```typescript
class SetOperations {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async sAdd(key: string, ...members: string[]): Promise<number> {
    return this.redis.sAdd(key, members);
  }

  async sRem(key: string, ...members: string[]): Promise<number> {
    return this.redis.sRem(key, members);
  }

  async sMembers(key: string): Promise<string[]> {
    return this.redis.sMembers(key);
  }

  async sIsMember(key: string, member: string): Promise<boolean> {
    return this.redis.sIsMember(key, member);
  }

  async sCard(key: string): Promise<number> {
    return this.redis.sCard(key);
  }

  async sRandMember(key: string, count?: number): Promise<string | string[]> {
    return this.redis.sRandMember(key, count);
  }

  async sPop(key: string, count?: number): Promise<string | string[]> {
    return this.redis.sPop(key, count);
  }

  async sMove(source: string, destination: string, member: string): Promise<number> {
    return this.redis.sMove(source, destination, member);
  }

  async sInter(...keys: string[]): Promise<string[]> {
    return this.redis.sInter(keys);
  }

  async sUnion(...keys: string[]): Promise<string[]> {
    return this.redis.sUnion(keys);
  }

  async sDiff(...keys: string[]): Promise<string[]> {
    return this.redis.sDiff(keys);
  }

  async sInterStore(destination: string, ...keys: string[]): Promise<number> {
    return this.redis.sInterStore(destination, keys);
  }

  async sUnionStore(destination: string, ...keys: string[]): Promise<number> {
    return this.redis.sUnionStore(destination, keys);
  }

  async sDiffStore(destination: string, ...keys: string[]): Promise<number> {
    return this.redis.sDiffStore(destination, keys);
  }
}
```

### 2.9 Sorted Set Operations

```typescript
class SortedSetOperations {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async zAdd(key: string, members: Array<{ score: number; value: string }>): Promise<number> {
    const args: (string | number)[] = [];
    for (const { score, value } of members) {
      args.push(score, value);
    }
    return this.redis.zAdd(key, args);
  }

  async zScore(key: string, member: string): Promise<number | null> {
    const score = await this.redis.zScore(key, member);
    return score !== null ? Number(score) : null;
  }

  async zRank(key: string, member: string): Promise<number | null> {
    return this.redis.zRank(key, member);
  }

  async zRevRank(key: string, member: string): Promise<number | null> {
    return this.redis.zRevRank(key, member);
  }

  async zRange(key: string, start: number, stop: number, options?: { BY?: 'SCORE' | 'LEX'; REV?: boolean; LIMIT?: { offset: number; count: number } }): Promise<string[]> {
    return this.redis.zRange(key, start, stop, options);
  }

  async zRangeWithScores(
    key: string,
    start: number,
    stop: number,
    options?: { BY?: 'SCORE' | 'LEX'; REV?: boolean; LIMIT?: { offset: number; count: number } }
  ): Promise<Array<{ value: string; score: number }>> {
    const result = await this.redis.zRangeWithScores(key, start, stop, options);
    return result.map((item: any) => ({
      value: item.value,
      score: Number(item.score),
    }));
  }

  async zRevRange(key: string, start: number, stop: number): Promise<string[]> {
    return this.redis.zRevRange(key, start, stop);
  }

  async zRevRangeWithScores(key: string, start: number, stop: number): Promise<Array<{ value: string; score: number }>> {
    const result = await this.redis.zRangeWithScores(key, start, stop, { REV: true });
    return result.map((item: any) => ({
      value: item.value,
      score: Number(item.score),
    }));
  }

  async zCard(key: string): Promise<number> {
    return this.redis.zCard(key);
  }

  async zCount(key: string, min: number, max: number): Promise<number> {
    return this.redis.zCount(key, min, max);
  }

  async zIncrBy(key: string, increment: number, member: string): Promise<string> {
    return this.redis.zIncrBy(key, increment, member);
  }

  async zRem(key: string, ...members: string[]): Promise<number> {
    return this.redis.zRem(key, members);
  }

  async zRemRangeByRank(key: string, start: number, stop: number): Promise<number> {
    return this.redis.zRemRangeByRank(key, start, stop);
  }

  async zRemRangeByScore(key: string, min: number | string, max: number | string): Promise<number> {
    return this.redis.zRemRangeByScore(key, min, max);
  }

  async zLexCount(key: string, min: string, max: string): Promise<number> {
    return this.redis.zLexCount(key, min, max);
  }

  async zRangeByLex(key: string, min: string, max: string, options?: { LIMIT?: { offset: number; count: number } }): Promise<string[]> {
    return this.redis.zRangeByLex(key, min, max, options);
  }

  async zUnion(destination: string, keys: string[], options?: { WEIGHTS?: number[]; AGGREGATE?: 'SUM' | 'MIN' | 'MAX' }): Promise<string> {
    return this.redis.zUnion(destination, keys, options);
  }

  async zInter(destination: string, keys: string[], options?: { WEIGHTS?: number[]; AGGREGATE?: 'SUM' | 'MIN' | 'MAX' }): Promise<string> {
    return this.redis.zInter(destination, keys, options);
  }
}
```

### 2.10 Pipeline và Transactions

```typescript
class PipelineOperations {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async executePipeline(commands: Array<[command: string, ...args: any[]]>): Promise<any[]> {
    const pipeline = this.redis.multi();
    
    for (const [command, ...args] of commands) {
      (pipeline as any)[command](...args);
    }
    
    return pipeline.exec();
  }

  async batchGet(keys: string[]): Promise<(string | null)[]> {
    const pipeline = this.redis.multi();
    
    for (const key of keys) {
      pipeline.get(key);
    }
    
    const results = await pipeline.exec();
    return results?.map(([err, value]) => {
      if (err) throw err;
      return value as string | null;
    }) || [];
  }

  async batchSet(keyValues: Record<string, string>): Promise<void> {
    const pipeline = this.redis.multi();
    
    for (const [key, value] of Object.entries(keyValues)) {
      pipeline.set(key, value);
    }
    
    await pipeline.exec();
  }

  async executeTransaction(
    operations: Array<[command: string, ...args: any[]]>
  ): Promise<any[]> {
    const transaction = this.redis.multi();
    
    for (const [command, ...args] of operations) {
      (transaction as any)[command](...args);
    }
    
    return transaction.exec();
  }

  async watchAndSet(
    key: string,
    value: string,
    condition: (currentValue: string | null) => boolean
  ): Promise<boolean> {
    return new Promise(async (resolve, reject) => {
      const watch = this.redis.watch(key);
      
      try {
        const currentValue = await this.redis.get(key);
        
        if (!condition(currentValue)) {
          await watch.unwatch();
          resolve(false);
          return;
        }
        
        const multi = this.redis.multi();
        multi.set(key, value);
        
        const result = await multi.exec();
        
        if (result === null) {
          // Transaction failed due to watched key change
          resolve(false);
        } else {
          resolve(true);
        }
      } catch (error) {
        await watch.unwatch();
        reject(error);
      }
    });
  }
}
```

## 3. ioredis

### 3.1 Giới Thiệu

ioredis là một Redis client phổ biến với promise-based API và nhiều features nâng cao như cluster support, sentinel support, và Lua scripting. Nó được sử dụng rộng rãi trong production.

### 3.2 Installation và Setup

```bash
npm install ioredis
```

### 3.3 Basic Connection

```typescript
import Redis from 'ioredis';

class RedisConnection {
  private client: Redis;

  constructor(options?: {
    host?: string;
    port?: number;
    password?: string;
    db?: number;
    tls?: boolean;
  }) {
    this.client = new Redis({
      host: options?.host || 'localhost',
      port: options?.port || 6379,
      password: options?.password,
      db: options?.db || 0,
      tls: options?.tls ? {} : undefined,
      retryStrategy: (times) => {
        const delay = Math.min(times * 50, 2000);
        return delay;
      },
      maxRetriesPerRequest: 3,
      enableReadyCheck: true,
      lazyConnect: false,
    });

    this.client.on('error', (err) => {
      console.error('Redis connection error:', err);
    });

    this.client.on('connect', () => {
      console.log('Redis connected');
    });

    this.client.on('ready', () => {
      console.log('Redis ready');
    });

    this.client.on('reconnecting', () => {
      console.log('Redis reconnecting...');
    });
  }

  getClient(): Redis {
    return this.client;
  }

  async disconnect(): Promise<void> {
    await this.client.quit();
  }

  async isConnected(): Promise<boolean> {
    return this.client.status === 'ready';
  }
}
```

### 3.4 Cluster Connection

```typescript
import Redis from 'ioredis';

class RedisClusterConnection {
  private cluster: Redis.Cluster;

  constructor(startupNodes: Array<{ host: string; port: number }>) {
    this.cluster = new Redis.Cluster(startupNodes, {
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
      scaleReads: 'master',
      maxRedirections: 16,
      enableAutoDiscovery: true,
    });

    this.cluster.on('error', (err) => {
      console.error('Redis cluster error:', err);
    });

    this.cluster.on('reconnecting', () => {
      console.log('Redis cluster reconnecting...');
    });
  }

  getCluster(): Redis.Cluster {
    return this.cluster;
  }

  async disconnect(): Promise<void> {
    await this.cluster.close();
  }
}

// Usage
const cluster = new RedisClusterConnection([
  { host: 'redis-1.example.com', port: 6379 },
  { host: 'redis-2.example.com', port: 6379 },
  { host: 'redis-3.example.com', port: 6379 },
]);
```

### 3.5 Sentinel Connection

```typescript
import Redis from 'ioredis';

class RedisSentinelConnection {
  private sentinel: Redis;
  private readonly masterName = 'mymaster';

  constructor() {
    this.sentinel = new Redis({
      sentinels: [
        { host: 'sentinel-1.example.com', port: 26379 },
        { host: 'sentinel-2.example.com', port: 26379 },
        { host: 'sentinel-3.example.com', port: 26379 },
      ],
      name: this.masterName,
      password: process.env.REDIS_PASSWORD,
      enableReadyCheck: true,
      updateSentinels: true,
      usePasswordInCommand: true,
      retryStrategy: (times) => {
        return Math.min(times * 100, 3000);
      },
    });

    this.sentinel.on('error', (err) => {
      console.error('Sentinel error:', err);
    });

    this.sentinel.on('ready', () => {
      console.log('Connected to Redis master via Sentinel');
    });
  }

  getClient(): Redis {
    return this.sentinel;
  }

  async disconnect(): Promise<void> {
    await this.sentinel.quit();
  }
}
```

### 3.6 ioredis Pipeline

```typescript
class IoredisPipeline {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async batchOperations(operations: RedisCommand[]): Promise<any[]> {
    const pipeline = this.redis.pipeline();
    
    for (const op of operations) {
      if (op.type === 'string') {
        pipeline.set(op.key, op.value);
      } else if (op.type === 'hash') {
        pipeline.hset(op.key, op.field, op.value);
      } else if (op.type === 'list') {
        pipeline.lpush(op.key, op.value);
      } else if (op.type === 'set') {
        pipeline.sadd(op.key, op.value);
      }
    }
    
    const results = await pipeline.exec();
    return results || [];
  }

  async atomicIncrementCounters(
    keys: string[],
    increment = 1
  ): Promise<Map<string, number>> {
    const pipeline = this.redis.pipeline();
    
    for (const key of keys) {
      pipeline.incrby(key, increment);
    }
    
    const results = await pipeline.exec();
    const counters = new Map<string, number>();
    
    results?.forEach((result, index) => {
      const [err, value] = result;
      if (!err && value !== undefined) {
        counters.set(keys[index], value as number);
      }
    });
    
    return counters;
  }

  async batchGetWithCache(
    keys: string[],
    ttlSeconds = 3600
  ): Promise<Map<string, string>> {
    const pipeline = this.redis.pipeline();
    
    for (const key of keys) {
      pipeline.get(key);
    }
    
    const results = await pipeline.exec();
    const values = new Map<string, string>();
    
    results?.forEach((result, index) => {
      const [err, value] = result;
      if (!err && value) {
        values.set(keys[index], value as string);
      }
    });
    
    return values;
  }
}

interface RedisCommand {
  type: 'string' | 'hash' | 'list' | 'set';
  key: string;
  field?: string;
  value: string;
}
```

### 3.7 ioredis Lua Scripts

```typescript
class IoredisLuaScripts {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async registerScripts(): Promise<void> {
    // Define custom Lua scripts
    this.redis.defineCommand('incrementIfExists', {
      numberOfKeys: 1,
      lua: `
        local exists = redis.call('EXISTS', KEYS[1])
        if exists == 1 then
          return redis.call('INCR', KEYS[1])
        else
          return -1
        end
      `,
    });

    this.redis.defineCommand('setNXWithExpiry', {
      numberOfKeys: 1,
      lua: `
        local result = redis.call('SETNX', KEYS[1], ARGV[1])
        if result == 1 then
          redis.call('EXPIRE', KEYS[1], ARGV[2])
          return 1
        else
          return 0
        end
      `,
    });

    this.redis.defineCommand('getOrSet', {
      numberOfKeys: 1,
      lua: `
        local value = redis.call('GET', KEYS[1])
        if value then
          return value
        else
          return 'NOT_FOUND'
        end
      `,
    });
  }

  async incrementIfExists(key: string): Promise<number> {
    return (this.redis as any).incrementIfExists(key);
  }

  async setNXWithExpiry(key: string, value: string, ttlSeconds: number): Promise<boolean> {
    const result = await (this.redis as any).setNXWithExpiry(key, value, ttlSeconds);
    return result === 1;
  }
}
```

## 4. redis-om (Object Mapper)

### 4.1 Giới Thiệu

redis-om cung cấp một layer abstraction cao hơn, cho phép define models với schemas và tự động handle serialization/deserialization. Nó sử dụng Hash data structures cho data storage.

### 4.2 Installation và Setup

```bash
npm install redis-om
```

### 4.3 Schema Definition

```typescript
import { Client, Entity, Schema, Repository } from 'redis-om';

class User extends Entity {
  id!: string;
  name!: string;
  email!: string;
  age!: number;
  roles!: string[];
  createdAt!: Date;
  updatedAt!: Date;
}

const userSchema = new Schema(User, {
  id: { type: 'string' },
  name: { type: 'string', field: 'name' },
  email: { type: 'string', field: 'email' },
  age: { type: 'number', field: 'age' },
  roles: { type: 'array', field: 'roles' },
  createdAt: { type: 'date', field: 'createdAt' },
  updatedAt: { type: 'date', field: 'updatedAt' },
});

// Client setup
const client = new Client();
await client.open('redis://localhost:6379');

// Create repository
const userRepository = new Repository(userSchema, client);
```

### 4.4 CRUD Operations với redis-om

```typescript
class UserService {
  private repository: Repository<User>;

  constructor(repository: Repository<User>) {
    this.repository = repository;
  }

  async create(userData: Partial<User>): Promise<User> {
    const user = this.repository.createEntity({
      id: this.generateId(),
      name: userData.name,
      email: userData.email,
      age: userData.age,
      roles: userData.roles || [],
      createdAt: new Date(),
      updatedAt: new Date(),
    });

    await this.repository.save(user);
    return user;
  }

  async findById(id: string): Promise<User | null> {
    return this.repository.fetch(id);
  }

  async findByEmail(email: string): Promise<User | null> {
    const users = await this.repository.search()
      .where('email').eq(email)
      .return.all();
    return users.length > 0 ? users[0] : null;
  }

  async findAll(options?: {
    limit?: number;
    offset?: number;
  }): Promise<User[]> {
    let query = this.repository.search();
    
    if (options?.limit) {
      query = query.return.page(options.offset || 0, options.limit);
    } else {
      query = query.return.all();
    }
    
    return query;
  }

  async update(id: string, updates: Partial<User>): Promise<User | null> {
    const user = await this.repository.fetch(id);
    
    if (!user) return null;

    Object.assign(user, {
      ...updates,
      updatedAt: new Date(),
    });

    await this.repository.save(user);
    return user;
  }

  async delete(id: string): Promise<boolean> {
    const deleted = await this.repository.remove(id);
    return deleted;
  }

  async count(): Promise<number> {
    return this.repository.search().return.count();
  }

  private generateId(): string {
    return `user:${Date.now()}:${Math.random().toString(36).substring(2, 9)}`;
  }
}
```

### 4.5 Search với redis-om

```typescript
class AdvancedUserSearch {
  private repository: Repository<User>;

  constructor(repository: Repository<User>) {
    this.repository = repository;
  }

  async searchByName(name: string): Promise<User[]> {
    return this.repository.search()
      .where('name').match(name)
      .return.all();
  }

  async searchByAgeRange(minAge: number, maxAge: number): Promise<User[]> {
    return this.repository.search()
      .where('age').between(minAge, maxAge)
      .return.all();
  }

  async searchByRole(role: string): Promise<User[]> {
    return this.repository.search()
      .where('roles').contains(role)
      .return.all();
  }

  async searchByMultipleRoles(roles: string[]): Promise<User[]> {
    return this.repository.search()
      .where('roles').containsAny(...roles)
      .return.all();
  }

  async searchByCreatedDate(startDate: Date, endDate: Date): Promise<User[]> {
    return this.repository.search()
      .where('createdAt').between(startDate, endDate)
      .return.all();
  }

  async paginatedSearch(
    page: number,
    pageSize: number,
    sortBy?: keyof User,
    ascending = true
  ): Promise<{ users: User[]; total: number; page: number; pageSize: number }> {
    const offset = (page - 1) * pageSize;
    
    let query = this.repository.search();
    
    if (sortBy) {
      if (ascending) {
        query = query.sortBy(sortBy as string);
      } else {
        query = query.sortBy(`-${sortBy}`);
      }
    }
    
    const [users, total] = await Promise.all([
      query.return.page(offset, pageSize),
      query.return.count(),
    ]);
    
    return {
      users,
      total,
      page,
      pageSize,
    };
  }

  async fullTextSearch(searchTerm: string): Promise<User[]> {
    // For full-text search, use RediSearch module
    return this.repository.search()
      .where('name').match(`*${searchTerm}*`)
      .or('email').match(`*${searchTerm}*`)
      .return.all();
  }
}
```

## 5. RediSearch Integration

### 5.1 Giới Thiệu

RediSearch là một Redis module cung cấp full-text search, secondary indexes, và query capabilities vượt trội so với basic Redis commands. Khi sử dụng với Node.js, bạn có thể tận dụng các features này qua các clients.

### 5.2 Index Creation với RediSearch

```typescript
import { createClient, RedisClientType } from '@redis/client';

class RediSearchService {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async createProductIndex(): Promise<void> {
    // Create index for products
    await this.redis.ft.create(
      'idx:products',
      {
        name: { type: 'TEXT', weight: 5, sortable: true },
        description: { type: 'TEXT', weight: 1 },
        category: { type: 'TAG', sortable: true },
        price: { type: 'NUMERIC', sortable: true },
        stock: { type: 'NUMERIC', sortable: true },
        tags: { type: 'TAG' },
        createdAt: { type: 'NUMERIC', sortable: true },
        rating: { type: 'NUMERIC', sortable: true },
      },
      {
        ON: 'HASH',
        PREFIX: 'product:',
      }
    );
  }

  async createUserIndex(): Promise<void> {
    await this.redis.ft.create(
      'idx:users',
      {
        name: { type: 'TEXT', weight: 3, sortable: true },
        email: { type: 'TEXT', sortable: true },
        bio: { type: 'TEXT' },
        role: { type: 'TAG', sortable: true },
        age: { type: 'NUMERIC', sortable: true },
        createdAt: { type: 'NUMERIC', sortable: true },
        isActive: { type: 'TAG' },
      },
      {
        ON: 'HASH',
        PREFIX: 'user:',
      }
    );
  }

  async createArticleIndex(): Promise<void> {
    await this.redis.ft.create(
      'idx:articles',
      {
        title: { type: 'TEXT', weight: 10, sortable: true },
        content: { type: 'TEXT', weight: 1 },
        author: { type: 'TEXT', sortable: true },
        category: { type: 'TAG', sortable: true },
        tags: { type: 'TAG' },
        publishedAt: { type: 'NUMERIC', sortable: true },
        views: { type: 'NUMERIC', sortable: true },
        likes: { type: 'NUMERIC', sortable: true },
      },
      {
        ON: 'HASH',
        PREFIX: 'article:',
      }
    );
  }

  async dropIndex(indexName: string): Promise<void> {
    await this.redis.ft.dropIndex(indexName);
  }

  async getIndexInfo(indexName: string): Promise<any> {
    return this.redis.ft.info(indexName);
  }
}
```

### 5.3 RediSearch Queries

```typescript
interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  stock: number;
  tags: string[];
  rating: number;
}

class RediSearchQueries {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async searchProducts(
    query: string,
    options?: {
      category?: string;
      minPrice?: number;
      maxPrice?: number;
      tags?: string[];
      sortBy?: 'price' | 'rating' | 'createdAt';
      sortOrder?: 'ASC' | 'DESC';
      limit?: number;
      offset?: number;
    }
  ): Promise<Product[]> {
    let searchQuery = `@name:${query} | @description:${query}`;

    if (options?.category) {
      searchQuery += ` @category:{${options.category}}`;
    }

    if (options?.minPrice !== undefined || options?.maxPrice !== undefined) {
      const min = options.minPrice ?? '-inf';
      const max = options.maxPrice ?? '+inf';
      searchQuery += ` @price:[${min} ${max}]`;
    }

    if (options?.tags && options.tags.length > 0) {
      searchQuery += ` @tags:{${options.tags.join('|')}}`;
    }

    let sortBy = '';
    if (options?.sortBy) {
      const order = options.sortOrder === 'ASC' ? 'ASC' : 'DESC';
      sortBy = ` SORTBY ${options.sortBy} ${order}`;
    }

    const limit = options?.limit ?? 20;
    const offset = options?.offset ?? 0;

    const redisQuery = `FT.SEARCH idx:products "${searchQuery}"${sortBy} LIMIT ${offset} ${limit}`;

    // Execute using raw command
    const result = await (this.redis as any).call('FT.SEARCH', 
      'idx:products',
      query,
      'LIMIT', offset, limit,
      ...(sortBy ? [sortBy.split(' ')] : [])
    );

    return this.parseSearchResults(result);
  }

  async searchUsers(
    nameQuery: string,
    options?: {
      role?: string;
      minAge?: number;
      maxAge?: number;
      isActive?: boolean;
    }
  ): Promise<any[]> {
    let searchQuery = `@name:${nameQuery}`;

    if (options?.role) {
      searchQuery += ` @role:{${options.role}}`;
    }

    if (options?.isActive !== undefined) {
      searchQuery += ` @isActive:{${options.isActive ? 'true' : 'false'}}`;
    }

    const result = await (this.redis as any).call('FT.SEARCH',
      'idx:users',
      searchQuery,
      'LIMIT', 0, 20
    );

    return this.parseSearchResults(result);
  }

  async aggregateProducts(
    category: string
  ): Promise<{ category: string; count: number; avgPrice: number }[]> {
    const query = `@category:{${category}}`;

    const result = await (this.redis as any).call(
      'FT.AGGREGATE',
      'idx:products',
      query,
      'GROUPBY', '1', '@category',
      'REDUCE', 'COUNT', '0', 'AS', 'count',
      'REDUCE', 'AVG', '1', '@price', 'AS', 'avgPrice'
    );

    return this.parseAggregateResults(result);
  }

  async getProductSuggestions(prefix: string, limit = 10): Promise<string[]> {
    const result = await (this.redis as any).call(
      'FT.SUGADD',
      'product:suggestions',
      prefix,
      1.0
    );

    const suggestions = await (this.redis as any).call(
      'FT.SUGGET',
      'product:suggestions',
      prefix,
      'MAX', limit
    );

    return suggestions || [];
  }

  private parseSearchResults(result: any[]): any[] {
    if (!result || result.length < 2) return [];

    const products: any[] = [];
    const total = result[0];

    for (let i = 1; i < result.length; i += 2) {
      const id = result[i];
      const fields = result[i + 1];

      const product: any = { id };
      for (let j = 0; j < fields.length; j += 2) {
        const field = fields[j];
        const value = fields[j + 1];
        product[field] = this.parseValue(value);
      }
      products.push(product);
    }

    return products;
  }

  private parseAggregateResults(result: any[]): any[] {
    const results: any[] = [];

    for (let i = 0; i < result.length; i++) {
      const row = result[i];
      results.push({
        category: row[1],
        count: parseInt(row[3]),
        avgPrice: parseFloat(row[5]),
      });
    }

    return results;
  }

  private parseValue(value: any): any {
    if (typeof value === 'string') {
      if (!isNaN(parseFloat(value))) {
        return parseFloat(value);
      }
      if (value === 'true') return true;
      if (value === 'false') return false;
    }
    return value;
  }
}
```

### 5.4 RediSearch Aggregation

```typescript
class RediSearchAggregation {
  private redis: RedisClientType;

  constructor(redis: RedisClientType) {
    this.redis = redis;
  }

  async analyzeUserRegistrations(
    startDate: number,
    endDate: number
  ): Promise<any> {
    const query = `@createdAt:[${startDate} ${endDate}]`;

    const result = await (this.redis as any).call(
      'FT.AGGREGATE',
      'idx:users',
      query,
      'GROUPBY', '1', '@role',
      'REDUCE', 'COUNT', '0', 'AS', 'total_users',
      'REDUCE', 'AVG', '1', '@age', 'AS', 'avg_age',
      'SORTBY', '2', '@total_users', 'DESC'
    );

    return this.parseAggregationResult(result);
  }

  async getProductPriceDistribution(): Promise<any[]> {
    const result = await (this.redis as any).call(
      'FT.AGGREGATE',
      'idx:products',
      '*',
      'APPLY', 'floor(@price/10)*10', 'AS', 'price_range',
      'GROUPBY', '1', '@price_range',
      'REDUCE', 'COUNT', '0', 'AS', 'count',
      'SORTBY', '2', '@price_range', 'ASC'
    );

    return result.map((row: any[]) => ({
      priceRange: `${row[1]}-${parseInt(row[1]) + 9}`,
      count: parseInt(row[3]),
    }));
  }

  async getTopRatedProductsByCategory(
    limit = 10
  ): Promise<any[]> {
    const result = await (this.redis as any).call(
      'FT.AGGREGATE',
      'idx:products',
      '*',
      'GROUPBY', '1', '@category',
      'REDUCE', 'TOPK', '3', '@rating', 'AS', 'top_rated',
      'REDUCE', 'AVG', '1', '@rating', 'AS', 'avg_rating',
      'SORTBY', '2', '@avg_rating', 'DESC',
      'LIMIT', 0, limit
    );

    return this.parseAggregationResult(result);
  }

  async calculateDailySalesTrend(
    days = 30
  ): Promise<any[]> {
    const endDate = Date.now();
    const startDate = endDate - days * 24 * 60 * 60 * 1000;

    const query = `@createdAt:[${startDate} ${endDate}]`;

    const result = await (this.redis as any).call(
      'FT.AGGREGATE',
      'idx:orders',
      query,
      'APPLY', 'floor(@createdAt/86400000)*86400000', 'AS', 'day',
      'GROUPBY', '1', '@day',
      'REDUCE', 'COUNT', '0', 'AS', 'order_count',
      'REDUCE', 'SUM', '1', '@total', 'AS', 'daily_revenue',
      'SORTBY', '2', '@day', 'ASC'
    );

    return result.map((row: any[]) => ({
      date: new Date(parseInt(row[1])),
      orderCount: parseInt(row[3]),
      dailyRevenue: parseFloat(row[5]),
    }));
  }

  private parseAggregationResult(result: any[]): any[] {
    if (!result || result.length === 0) return [];

    const columns = result[0];
    const rows: any[] = [];

    for (let i = 1; i < result.length; i++) {
      const row: any = {};
      for (let j = 0; j < columns.length; j += 2) {
        row[columns[j]] = this.parseValue(columns[j + 1]);
        row[columns[j + 1]] = this.parseValue(result[i][j + 1]);
      }
      rows.push(row);
    }

    return rows;
  }

  private parseValue(value: any): any {
    if (typeof value === 'string') {
      const num = parseFloat(value);
      if (!isNaN(num)) return num;
    }
    return value;
  }
}
```

## 6. Connection Pooling

### 6.1 Connection Pool Pattern

```typescript
import { createClient, RedisClientType } from '@redis/client';

class RedisPool {
  private pool: RedisClientType[] = [];
  private readonly minConnections: number;
  private readonly maxConnections: number;
  private readonly redisUrl: string;
  private waitingRequests: Array<(client: RedisClientType) => void> = [];
  private connectionCount = 0;

  constructor(options: {
    url: string;
    minConnections?: number;
    maxConnections?: number;
  }) {
    this.redisUrl = options.url;
    this.minConnections = options.minConnections ?? 5;
    this.maxConnections = options.maxConnections ?? 20;
  }

  async initialize(): Promise<void> {
    // Create minimum connections on startup
    const promises: Promise<void>[] = [];
    for (let i = 0; i < this.minConnections; i++) {
      promises.push(this.createConnection());
    }
    await Promise.all(promises);
  }

  private async createConnection(): Promise<RedisClientType> {
    if (this.connectionCount >= this.maxConnections) {
      throw new Error('Connection pool exhausted');
    }

    const client = createClient({ url: this.redisUrl });

    client.on('error', (err) => {
      console.error('Redis client error:', err);
    });

    await client.connect();
    this.connectionCount++;
    this.pool.push(client);

    return client;
  }

  async getConnection(): Promise<RedisClientType> {
    // Try to get existing connection
    if (this.pool.length > 0) {
      return this.pool.pop()!;
    }

    // Try to create new connection
    if (this.connectionCount < this.maxConnections) {
      return this.createConnection();
    }

    // Wait for available connection
    return new Promise((resolve) => {
      this.waitingRequests.push(resolve);
    });
  }

  async releaseConnection(client: RedisClientType): Promise<void> {
    // Check if there are waiting requests
    if (this.waitingRequests.length > 0) {
      const resolve = this.waitingRequests.shift()!;
      resolve(client);
      return;
    }

    // Return to pool
    this.pool.push(client);
  }

  async execute<T>(
    operation: (client: RedisClientType) => Promise<T>
  ): Promise<T> {
    const client = await this.getConnection();

    try {
      return await operation(client);
    } finally {
      await this.releaseConnection(client);
    }
  }

  async close(): Promise<void> {
    // Close all connections
    await Promise.all(
      this.pool.map((client) => client.quit())
    );
    this.pool = [];
    this.connectionCount = 0;
  }
}

// Usage
const pool = new RedisPool({
  url: 'redis://localhost:6379',
  minConnections: 5,
  maxConnections: 20,
});

await pool.initialize();

// Execute operations
const result = await pool.execute(async (client) => {
  return client.get('my-key');
});

await pool.close();
```

## 7. Error Handling và Retry

### 7.1 Retry Logic

```typescript
import { createClient, RedisClientType } from '@redis/client';

interface RetryOptions {
  maxRetries: number;
  initialDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  retryableErrors?: (error: Error) => boolean;
}

const DEFAULT_RETRY_OPTIONS: RetryOptions = {
  maxRetries: 3,
  initialDelayMs: 100,
  maxDelayMs: 5000,
  backoffMultiplier: 2,
  retryableErrors: (error) => {
    // Retry on connection errors
    if (error.message.includes('ECONNREFUSED')) return true;
    if (error.message.includes('ETIMEDOUT')) return true;
    if (error.message.includes('Connection is closed')) return true;
    return false;
  },
};

class RedisRetryClient {
  private client: RedisClientType;
  private options: RetryOptions;

  constructor(url: string, options: Partial<RetryOptions> = {}) {
    this.client = createClient({ url });
    this.options = { ...DEFAULT_RETRY_OPTIONS, ...options };

    this.client.on('error', (err) => {
      console.error('Redis error:', err);
    });
  }

  async connect(): Promise<void> {
    await this.client.connect();
  }

  async executeWithRetry<T>(
    operation: () => Promise<T>,
    options?: Partial<RetryOptions>
  ): Promise<T> {
    const opts = { ...this.options, ...options };
    let lastError: Error | undefined;
    let delay = opts.initialDelayMs;

    for (let attempt = 0; attempt <= opts.maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error as Error;

        // Check if we should retry
        if (attempt >= opts.maxRetries) break;
        if (!opts.retryableErrors!(lastError)) break;

        // Wait before retry
        console.log(`Redis operation failed, retrying in ${delay}ms... (attempt ${attempt + 1}/${opts.maxRetries})`);
        await this.sleep(delay);

        // Apply exponential backoff
        delay = Math.min(delay * opts.backoffMultiplier, opts.maxDelayMs);
      }
    }

    throw lastError!;
  }

  async get(key: string): Promise<string | null> {
    return this.executeWithRetry(() => this.client.get(key));
  }

  async set(key: string, value: string, ttlSeconds?: number): Promise<void> {
    return this.executeWithRetry(() => {
      if (ttlSeconds) {
        return this.client.set(key, value, { EX: ttlSeconds });
      }
      return this.client.set(key, value);
    });
  }

  async hGetAll(key: string): Promise<Record<string, string>> {
    return this.executeWithRetry(() => this.client.hGetAll(key));
  }

  async mGet(keys: string[]): Promise<(string | null)[]> {
    return this.executeWithRetry(() => this.client.mGet(keys));
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async disconnect(): Promise<void> {
    await this.client.quit();
  }
}
```

## 8. Testing

### 8.1 Mock Redis for Tests

```typescript
import { jest } from '@jest/globals';

// Mock Redis client for testing
class MockRedisClient {
  private store: Map<string, string> = new Map();
  private hashes: Map<string, Map<string, string>> = new Map();
  private lists: Map<string, string[]> = new Map();
  private sets: Map<string, Set<string>> = new Map();
  private sortedSets: Map<string, Map<string, number>> = new Map();
  private ttls: Map<string, number> = new Map();

  async get(key: string): Promise<string | null> {
    this.checkTTL(key);
    return this.store.get(key) || null;
  }

  async set(key: string, value: string): Promise<string> {
    this.store.set(key, value);
    return 'OK';
  }

  async setex(key: string, seconds: number, value: string): Promise<string> {
    this.store.set(key, value);
    this.ttls.set(key, Date.now() + seconds * 1000);
    return 'OK';
  }

  async del(...keys: string[]): Promise<number> {
    let deleted = 0;
    for (const key of keys) {
      if (this.store.delete(key)) deleted++;
      this.hashes.delete(key);
      this.lists.delete(key);
      this.sets.delete(key);
      this.sortedSets.delete(key);
      this.ttls.delete(key);
    }
    return deleted;
  }

  async hset(key: string, ...fieldValues: string[]): Promise<number> {
    if (!this.hashes.has(key)) {
      this.hashes.set(key, new Map());
    }
    const hash = this.hashes.get(key)!;
    let added = 0;
    for (let i = 0; i < fieldValues.length; i += 2) {
      if (!hash.has(fieldValues[i])) added++;
      hash.set(fieldValues[i], fieldValues[i + 1]);
    }
    return added;
  }

  async hgetall(key: string): Promise<Record<string, string>> {
    const hash = this.hashes.get(key);
    if (!hash) return {};
    return Object.fromEntries(hash.entries());
  }

  async llen(key: string): Promise<number> {
    return this.lists.get(key)?.length || 0;
  }

  async lpush(key: string, ...values: string[]): Promise<number> {
    const list = this.lists.get(key) || [];
    this.lists.set(key, [...values, ...list]);
    return this.lists.get(key)!.length;
  }

  async rpush(key: string, ...values: string[]): Promise<number> {
    const list = this.lists.get(key) || [];
    this.lists.set(key, [...list, ...values]);
    return this.lists.get(key)!.length;
  }

  async lrange(key: string, start: number, stop: number): Promise<string[]> {
    const list = this.lists.get(key) || [];
    const end = stop === -1 ? list.length : stop + 1;
    return list.slice(start, end);
  }

  async sadd(key: string, ...members: string[]): Promise<number> {
    if (!this.sets.has(key)) {
      this.sets.set(key, new Set());
    }
    const set = this.sets.get(key)!;
    let added = 0;
    for (const member of members) {
      if (set.add(member)) added++;
    }
    return added;
  }

  async smembers(key: string): Promise<string[]> {
    return Array.from(this.sets.get(key) || []);
  }

  async sismember(key: string, member: string): Promise<number> {
    return this.sets.get(key)?.has(member) ? 1 : 0;
  }

  async zadd(key: string, ...scoreMembers: (string | number)[]): Promise<number> {
    if (!this.sortedSets.has(key)) {
      this.sortedSets.set(key, new Map());
    }
    const zset = this.sortedSets.get(key)!;
    let added = 0;
    for (let i = 0; i < scoreMembers.length; i += 2) {
      const score = scoreMembers[i] as number;
      const member = scoreMembers[i + 1] as string;
      if (!zset.has(member)) added++;
      zset.set(member, score);
    }
    return added;
  }

  async zrange(key: string, start: number, stop: number): Promise<string[]> {
    const zset = this.sortedSets.get(key);
    if (!zset) return [];
    const sorted = Array.from(zset.entries())
      .sort((a, b) => a[1] - b[1])
      .map(([member]) => member);
    const end = stop === -1 ? sorted.length : stop + 1;
    return sorted.slice(start, end);
  }

  async zrangebyscore(
    key: string,
    min: number | string,
    max: number | string
  ): Promise<string[]> {
    const zset = this.sortedSets.get(key);
    if (!zset) return [];
    return Array.from(zset.entries())
      .filter(([_, score]) => score >= (min as number) && score <= (max as number))
      .sort((a, b) => a[1] - b[1])
      .map(([member]) => member);
  }

  private checkTTL(key: string): void {
    const ttl = this.ttls.get(key);
    if (ttl && Date.now() > ttl) {
      this.store.delete(key);
      this.hashes.delete(key);
      this.lists.delete(key);
      this.sets.delete(key);
      this.sortedSets.delete(key);
      this.ttls.delete(key);
    }
  }

  async ttl(key: string): Promise<number> {
    const expiry = this.ttls.get(key);
    if (!expiry) return -1;
    const remaining = Math.ceil((expiry - Date.now()) / 1000);
    return remaining > 0 ? remaining : -2;
  }

  async flushdb(): Promise<string> {
    this.store.clear();
    this.hashes.clear();
    this.lists.clear();
    this.sets.clear();
    this.sortedSets.clear();
    this.ttls.clear();
    return 'OK';
  }

  async dbsize(): Promise<number> {
    return this.store.size;
  }
}

// Export for testing
export { MockRedisClient };
```

### 8.2 Integration Test Setup

```typescript
import Redis from 'ioredis';

// Skip integration tests if Redis is not available
const SKIP_INTEGRATION = process.env.SKIP_REDIS_TESTS === 'true';

interface TestContext {
  redis: Redis;
  beforeAll: () => Promise<void>;
  afterAll: () => Promise<void>;
  beforeEach: () => Promise<void>;
  afterEach: () => Promise<void>;
}

function createRedisTestContext(): TestContext {
  const redis = new Redis({
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
    lazyConnect: true,
  });

  return {
    redis,
    beforeAll: async () => {
      if (!SKIP_INTEGRATION) {
        await redis.connect();
        await redis.flushdb();
      }
    },
    afterAll: async () => {
      if (!SKIP_INTEGRATION) {
        await redis.quit();
      }
    },
    beforeEach: async () => {
      if (!SKIP_INTEGRATION) {
        await redis.flushdb();
      }
    },
    afterEach: async () => {
      if (!SKIP_INTEGRATION) {
        await redis.flushdb();
      }
    },
  };
}

// Example test
describe('UserService', () => {
  const ctx = createRedisTestContext();

  beforeAll(ctx.beforeAll);
  afterAll(ctx.afterAll);
  beforeEach(ctx.beforeEach);
  afterEach(ctx.afterEach);

  it('should create and retrieve user', async () => {
    if (SKIP_INTEGRATION) {
      console.log('Skipping Redis integration test');
      return;
    }

    await ctx.redis.hset('user:1', 'name', 'John', 'email', 'john@example.com');
    const user = await ctx.redis.hgetall('user:1');

    expect(user.name).toBe('John');
    expect(user.email).toBe('john@example.com');
  });
});
```

## 9. Best Practices

### 9.1 Connection Management

```typescript
// Good: Use connection pooling and proper lifecycle management
class RedisService {
  private pool: RedisPool;
  private static instance: RedisService;

  static getInstance(): RedisService {
    if (!RedisService.instance) {
      RedisService.instance = new RedisService();
    }
    return RedisService.instance;
  }

  async initialize(): Promise<void> {
    this.pool = new RedisPool({
      url: process.env.REDIS_URL!,
      minConnections: 5,
      maxConnections: 20,
    });
    await this.pool.initialize();
  }

  async getClient(): Promise<RedisClientType> {
    return this.pool.getConnection();
  }

  async shutdown(): Promise<void> {
    await this.pool.close();
  }
}

// Bad: Creating new connection for each operation
async function badExample(key: string) {
  const client = createClient({ url: 'redis://localhost:6379' });
  await client.connect();
  const value = await client.get(key);
  await client.quit();
  return value;
}
```

### 9.2 Error Handling

```typescript
// Good: Comprehensive error handling with retries
async function safeRedisOperation<T>(
  operation: () => Promise<T>,
  options = { retries: 3, backoff: 1000 }
): Promise<T> {
  let lastError: Error | undefined;

  for (let i = 0; i <= options.retries; i++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;
      
      if (i < options.retries && isRetryableError(error)) {
        await sleep(options.backoff * Math.pow(2, i));
        continue;
      }
      
      break;
    }
  }

  throw lastError;
}

// Bad: No error handling
async function unsafeRedisOperation(key: string): Promise<string> {
  return redis.get(key); // Can throw and crash application
}
```

### 9.3 Performance Tips

```typescript
// Use pipelining for batch operations
async function batchGet(keys: string[]): Promise<Map<string, string>> {
  const pipeline = redis.pipeline();
  
  for (const key of keys) {
    pipeline.get(key);
  }
  
  const results = await pipeline.exec();
  const map = new Map<string, string>();
  
  results?.forEach(([err, value], i) => {
    if (!err && value) {
      map.set(keys[i], value as string);
    }
  });
  
  return map;
}

// Use Lua scripts for atomic operations
const INCREMENT_IF_LESS_THAN = `
  local current = tonumber(redis.call('GET', KEYS[1]) or 0)
  local limit = tonumber(ARGV[1])
  if current < limit then
    redis.call('INCR', KEYS[1])
    return 1
  end
  return 0
`;

// Use appropriate data structures
// Bad: Store JSON as string
await redis.set('user:1', JSON.stringify(userData));
const user = JSON.parse(await redis.get('user:1'));

// Good: Use Hash for structured data
await redis.hset('user:1', 'name', user.name, 'email', user.email);
const user = await redis.hgetall('user:1');
```

## 10. References

- [@redis/client Documentation](https://redis.js.org/)
- [ioredis Documentation](https://github.com/luin/ioredis)
- [redis-om Documentation](https://github.com/redis/redis-om-node)
- [RediSearch Documentation](https://redis.io/docs/stack/search/)
- [Redis Commands Reference](https://redis.io/commands/)
- [Redis Node.js Client Best Practices](https://redis.io/docs/clients/nodejs/)
