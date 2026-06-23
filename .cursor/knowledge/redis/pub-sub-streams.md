---
title: "Redis Pub/Sub and Streams"
description: "Hướng dẫn toàn diện về Redis Pub/Sub messaging patterns và Redis Streams cho event-driven architecture, real-time data processing, và message queuing trong enterprise applications"
tags: ["redis", "pub-sub", "streams", "xadd", "xread", "xgroup", "consumer-groups", "event-driven", "messaging"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Redis Pub/Sub and Streams

## 1. Tổng Quan (Overview)

Redis cung cấp hai cơ chế messaging mạnh mẽ: Pub/Sub (Publish/Subscribe) và Streams. Mỗi cơ chế phục vụ các use cases khác nhau và có những trade-offs riêng. Hiểu rõ sự khác biệt giữa chúng là chìa khóa để thiết kế hệ thống messaging hiệu quả.

**Pub/Sub** là cơ chế fire-and-forget, phù hợp cho real-time notifications, broadcast messages, và các use cases không đòi hỏi message persistence. Khi subscriber không online, messages sẽ bị mất.

**Redis Streams** là cơ chế message queue hoàn chỉnh với persistence, consumer groups, acknowledgment, và replay capabilities. Phù hợp cho event sourcing, job queues, và các use cases cần message durability.

## 2. Redis Pub/Sub

### 2.1 Giới Thiệu

Pub/Sub (Publish/Subscribe) là pattern cho phép publishers gửi messages đến channels mà không cần biết subscribers nào đang lắng nghe. Subscribers đăng ký nhận messages từ channels mà không cần biết ai đang publish.

### 2.2 Core Concepts

```typescript
/**
 * Pub/Sub Concepts:
 * 
 * Publisher: Gửi messages đến channels
 * Subscriber: Nhận messages từ channels
 * Channel: Đường dẫn truyền messages
 * Pattern: Wildcard matching cho channels
 */

// Channel naming conventions
const CHANNEL_CONVENTIONS = {
  // User events
  'user:{userId}:events',
  'user:{userId}:notifications',
  
  // System events
  'system:notifications',
  'system:alerts',
  
  # Real-time data
  'stock:{symbol}:quotes',
  'sensor:{sensorId}:data',
  
  # Application events
  'app:{appId}:events',
  'app:{appId}:logs',
};
```

### 2.3 Basic Pub/Sub Operations

```redis
# Subscribe to channel
SUBSCRIBE notifications
SUBSCRIBE notifications alerts

# Pattern subscribe (wildcard)
PSUBSCRIBE notifications.*
PSUBSCRIBE user:*

# Publish to channel
PUBLISH notifications "Hello subscribers!"
PUBLISH user:123:events '{"type":"login","timestamp":1234567890}'

# Unsubscribe
UNSUBSCRIBE notifications
PUNSUBSCRIBE notifications.*

# Check subscription info
PUBSUB NUMSUB notifications
PUBSUB CHANNELS
PUBSUB NUMPAT
```

### 2.4 Node.js Pub/Sub Implementation

```typescript
import Redis from 'ioredis';

class RedisPubSub {
  private publisher: Redis;
  private subscriber: Redis;
  private handlers: Map<string, Function[]>;
  private patternHandlers: Map<string, Function[]>;

  constructor(redisConfig: RedisConfig) {
    this.publisher = new Redis(redisConfig);
    this.subscriber = new Redis(redisConfig);
    this.handlers = new Map();
    this.patternHandlers = new Map();
    
    this.setupListeners();
  }

  private setupListeners(): void {
    // Handle message events
    this.subscriber.on('message', (channel, message) => {
      this.handleMessage(channel, message);
    });

    // Handle pattern message events
    this.subscriber.on('pmessage', (pattern, channel, message) => {
      this.handlePatternMessage(pattern, channel, message);
    });
  }

  private handleMessage(channel: string, message: string): void {
    const handlers = this.handlers.get(channel) || [];
    handlers.forEach(handler => {
      try {
        handler(channel, message, this.parseMessage(message));
      } catch (error) {
        console.error(`Handler error for channel ${channel}:`, error);
      }
    });
  }

  private handlePatternMessage(pattern: string, channel: string, message: string): void {
    const handlers = this.patternHandlers.get(pattern) || [];
    handlers.forEach(handler => {
      try {
        handler(pattern, channel, message, this.parseMessage(message));
      } catch (error) {
        console.error(`Pattern handler error for ${pattern}:`, error);
      }
    });
  }

  private parseMessage(message: string): any {
    try {
      return JSON.parse(message);
    } catch {
      return message;
    }
  }

  async publish(channel: string, data: any): Promise<number> {
    const message = typeof data === 'string' ? data : JSON.stringify(data);
    return this.publisher.publish(channel, message);
  }

  async subscribe(channel: string, handler: Function): Promise<void> {
    if (!this.handlers.has(channel)) {
      this.handlers.set(channel, []);
      await this.subscriber.subscribe(channel);
    }
    this.handlers.get(channel)!.push(handler);
  }

  async psubscribe(pattern: string, handler: Function): Promise<void> {
    if (!this.patternHandlers.has(pattern)) {
      this.patternHandlers.set(pattern, []);
      await this.subscriber.psubscribe(pattern);
    }
    this.patternHandlers.get(pattern)!.push(handler);
  }

  async unsubscribe(channel: string, handler?: Function): Promise<void> {
    if (handler) {
      const handlers = this.handlers.get(channel) || [];
      const index = handlers.indexOf(handler);
      if (index > -1) handlers.splice(index, 1);
      if (handlers.length === 0) {
        await this.subscriber.unsubscribe(channel);
        this.handlers.delete(channel);
      }
    } else {
      await this.subscriber.unsubscribe(channel);
      this.handlers.delete(channel);
    }
  }
}

// Usage Example
const pubsub = new RedisPubSub({ host: 'localhost', port: 6379 });

// Subscribe to user notifications
await pubsub.subscribe('notifications', (channel, message, data) => {
  console.log(`Notification: ${message}`);
  // Send push notification
});

// Subscribe to user events using pattern
await pubsub.psubscribe('user:*:events', (pattern, channel, message, data) => {
  const userId = channel.split(':')[1];
  console.log(`User ${userId} event:`, data);
});

// Publish events
await pubsub.publish('notifications', {
  title: 'New order',
  message: 'Order #12345 has been placed',
  timestamp: Date.now(),
});
```

### 2.5 Python Pub/Sub Implementation

```python
import redis
import json
import threading
from typing import Callable, Dict, List, Any, Optional
from datetime import datetime

class RedisPubSub:
    """
    Redis Pub/Sub wrapper với pattern matching và auto-reconnect
    """
    
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client = redis.from_url(redis_url)
        self.pubsub = self.redis_client.pubsub()
        self.handlers: Dict[str, List[Callable]] = {}
        self.pattern_handlers: Dict[str, List[Callable]] = {}
        self.listener_thread: Optional[threading.Thread] = None
        self.running = False
    
    def publish(self, channel: str, data: Any) -> int:
        """
        Publish message to channel
        Returns number of subscribers received the message
        """
        if isinstance(data, (dict, list)):
            message = json.dumps(data)
        else:
            message = str(data)
        
        return self.redis_client.publish(channel, message)
    
    def subscribe(self, channel: str, handler: Callable[[str, Any], None]) -> None:
        """
        Subscribe to a channel
        handler receives (channel, message) arguments
        """
        if channel not in self.handlers:
            self.handlers[channel] = []
            self.pubsub.subscribe(channel)
        
        self.handlers[channel].append(handler)
    
    def psubscribe(self, pattern: str, handler: Callable[[str, str, Any], None]) -> None:
        """
        Subscribe to pattern (e.g., 'user:*:events')
        handler receives (pattern, channel, message) arguments
        """
        if pattern not in self.pattern_handlers:
            self.pattern_handlers[pattern] = []
            self.pubsub.psubscribe(pattern)
        
        self.pattern_handlers[pattern].append(handler)
    
    def unsubscribe(self, channel: str, handler: Optional[Callable] = None) -> None:
        """Unsubscribe from channel"""
        if handler and channel in self.handlers:
            self.handlers[channel].remove(handler)
            if not self.handlers[channel]:
                del self.handlers[channel]
                self.pubsub.unsubscribe(channel)
        elif channel in self.handlers:
            del self.handlers[channel]
            self.pubsub.unsubscribe(channel)
    
    def start_listening(self) -> None:
        """Start listening for messages in background thread"""
        if self.running:
            return
        
        self.running = True
        self.listener_thread = threading.Thread(target=self._listen, daemon=True)
        self.listener_thread.start()
    
    def _listen(self) -> None:
        """Background listener loop"""
        for message in self.pubsub.listen():
            if not self.running:
                break
            
            try:
                if message['type'] == 'message':
                    channel = message['channel']
                    data = self._parse_message(message['data'])
                    for handler in self.handlers.get(channel, []):
                        handler(channel, data)
                
                elif message['type'] == 'pmessage':
                    pattern = message['pattern']
                    channel = message['channel']
                    data = self._parse_message(message['data'])
                    for handler in self.pattern_handlers.get(pattern, []):
                        handler(pattern, channel, data)
            
            except Exception as e:
                print(f"Error processing message: {e}")
    
    def _parse_message(self, data: Any) -> Any:
        """Parse message, try JSON first"""
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        return data
    
    def stop(self) -> None:
        """Stop listening and cleanup"""
        self.running = False
        self.pubsub.close()
        if self.listener_thread:
            self.listener_thread.join(timeout=1)


# Usage Example
if __name__ == "__main__":
    pubsub = RedisPubSub("redis://localhost:6379")
    
    # Define handlers
    def notification_handler(channel: str, data: dict):
        print(f"Notification on {channel}: {data}")
        # Send push notification, email, etc.
    
    def user_event_handler(pattern: str, channel: str, data: dict):
        user_id = channel.split(':')[1]
        print(f"User {user_id} event: {data['type']}")
    
    # Subscribe
    pubsub.subscribe('notifications', notification_handler)
    pubsub.psubscribe('user:*:events', user_event_handler)
    
    # Start listening
    pubsub.start_listening()
    
    # Publish
    pubsub.publish('notifications', {
        'title': 'System Alert',
        'message': 'High CPU usage detected',
        'severity': 'warning'
    })
    
    # Keep running
    import time
    time.sleep(60)
```

## 3. Redis Streams

### 3.1 Giới Thiệu

Redis Streams là data structure mới được giới thiệu trong Redis 5.0, cung cấp message queue với các tính năng:
- **Persistence**: Messages được lưu trữ cho đến khi explicitly deleted
- **Consumer Groups**: Nhiều consumers có thể nhóm lại để xử lý messages
- **Acknowledgment**: Messages có thể được ACK sau khi xử lý
- **Replay**: Có thể đọc lại messages từ bất kỳ điểm nào
- **Range Queries**: Đọc messages theo ID ranges

### 3.2 Stream Entry Structure

```
┌─────────────────────────────────────────────────────────────┐
│                     Redis Stream                             │
│  Stream ID: 1704064200000-0                                 │
├─────────────────────────────────────────────────────────────┤
│ Entry ID    │ Field 1    │ Field 2    │ Field 3    │ ...  │
├─────────────┼────────────┼────────────┼────────────┼──────┤
│ 1704064200000-0 │ sensor   │ 25.5      │ temp      │ ...  │
│ 1704064201000-0 │ sensor   │ 26.1      │ temp      │ ...  │
│ 1704064202000-0 │ sensor   │ 24.8      │ temp      │ ...  │
└─────────────┴────────────┴────────────┴────────────┴──────┘

Entry ID Format: <timestamp>-<sequence>
- timestamp: Milliseconds since epoch
- sequence: Sequence number within that millisecond
- Special IDs: 0-0 (oldest), $ (newest only), > (new entries only)
```

### 3.3 Basic Stream Commands

```redis
# XADD - Add entry to stream
XADD mystream * field1 value1 field2 value2
XADD mystream 1704064200000-0 sensor temp humidity
XADD mystream MAXLEN ~ 1000 * field value  # With approximate trimming

# XLEN - Get stream length
XLEN mystream

# XRANGE - Read range of entries
XRANGE mystream 1704064200000 1704064300000
XRANGE mystream - + COUNT 10
XRANGE mystream 1704064200000-0 +

# XREAD - Read new entries
XREAD STREAMS mystream $
XREAD COUNT 10 STREAMS mystream 0

# XREADGROUP - Read with consumer group
XREADGROUP GROUP group1 consumer1 STREAMS mystream >
XREADGROUP GROUP group1 consumer1 COUNT 10 STREAMS mystream >

# XGROUP - Manage consumer groups
XGROUP CREATE mystream mygroup $ MKSTREAM
XGROUP CREATECONSUMER mystream mygroup consumer2
XGROUP DELCONSUMER mystream mygroup consumer1

# XACK - Acknowledge processed entries
XACK mystream mygroup 1704064200000-0 1704064200001-0

# XPENDING - Check pending entries
XPENDING mystream mygroup
XPENDING mystream mygroup - + 10 consumer1

# XCLAIM - Claim pending entries from another consumer
XCLAIM mystream mygroup consumer2 60000 1704064200000-0

# XDEL - Delete entries
XDEL mystream 1704064200000-0

# XTRIM - Trim stream length
XTRIM mystream MAXLEN 1000
XTRIM mystream MINID 1704064200000
```

### 3.4 Stream Producer Implementation

```typescript
import Redis from 'ioredis';

interface StreamEntry {
  [field: string]: string;
}

interface StreamOptions {
  maxLen?: number;         // Exact length limit
  approximate?: boolean;   // Use MAXLEN ~ for approximate trimming
  nomkstream?: boolean;    // Don't create stream if not exists
}

class StreamProducer {
  private redis: Redis;
  private streamName: string;

  constructor(redis: Redis, streamName: string) {
    this.redis = redis;
    this.streamName = streamName;
  }

  async add(
    entry: StreamEntry,
    id?: string,
    options: StreamOptions = {}
  ): Promise<string> {
    const { maxLen, approximate = true, nomkstream = false } = options;
    
    let key = this.streamName;
    
    // Add MAXLEN trimming if specified
    if (maxLen) {
      key += approximate ? ` MAXLEN ~ ${maxLen}` : ` MAXLEN ${maxLen}`;
    }
    
    // Use * for auto-generated ID, or specify custom ID
    const entryId = id || '*';
    
    // Flatten entry to args
    const args: string[] = [key, entryId];
    for (const [field, value] of Object.entries(entry)) {
      args.push(field, String(value));
    }
    
    return this.redis.xadd(...args);
  }

  async addBatch(entries: StreamEntry[]): Promise<string[]> {
    const pipeline = this.redis.pipeline();
    
    for (const entry of entries) {
      const args: string[] = [this.streamName, '*'];
      for (const [field, value] of Object.entries(entry)) {
        args.push(field, String(value));
      }
      pipeline.xadd(...args);
    }
    
    const results = await pipeline.exec();
    return results?.map(([err, id]) => id as string) || [];
  }

  async getLength(): Promise<number> {
    return this.redis.xlen(this.streamName);
  }

  async trim(maxLen: number, approximate = true): Promise<number> {
    const modifier = approximate ? 'MAXLEN' : 'MAXLEN';
    const operator = approximate ? '~' : '';
    return this.redis.xtrim(this.streamName, `${operator} ${maxLen}`);
  }

  // Event-specific methods
  async emitEvent(eventType: string, payload: object): Promise<string> {
    return this.add({
      type: eventType,
      timestamp: Date.now().toString(),
      payload: JSON.stringify(payload),
    });
  }

  async emitUserEvent(userId: string, eventType: string, data: object): Promise<string> {
    return this.add({
      userId,
      type: eventType,
      timestamp: Date.now().toString(),
      data: JSON.stringify(data),
    });
  }
}

// Usage
const redis = new Redis({ host: 'localhost', port: 6379 });
const producer = new StreamProducer(redis, 'events:user-actions');

// Add single entry
const entryId = await producer.add({
  userId: '12345',
  action: 'purchase',
  productId: 'SKU001',
  amount: '99.99',
});

// Add with auto-trimming to 10000 entries
await producer.add({
  event: 'page_view',
  url: '/products',
}, undefined, { maxLen: 10000, approximate: true });

// Emit business events
await producer.emitEvent('user.purchased', {
  orderId: 'ORD-001',
  total: 199.99,
  items: 3,
});
```

### 3.5 Stream Consumer Implementation

```typescript
interface ConsumerOptions {
  groupName: string;
  consumerName: string;
  count?: number;
  blockMs?: number;
  autoAck?: boolean;
}

interface ConsumedMessage {
  id: string;
  stream: string;
  group: string;
  consumer: string;
  fields: Record<string, string>;
  parsed?: Record<string, any>;
}

class StreamConsumer {
  private redis: Redis;
  private streamName: string;
  private groupName: string;
  private consumerName: string;

  constructor(
    redis: Redis,
    streamName: string,
    groupName: string,
    consumerName: string
  ) {
    this.redis = redis;
    this.streamName = streamName;
    this.groupName = groupName;
    this.consumerName = consumerName;
  }

  async initializeGroup(startId = '$'): Promise<void> {
    try {
      // Create group starting from new messages only
      await this.redis.xgroup(
        'CREATE',
        this.streamName,
        this.groupName,
        startId,
        'MKSTREAM'
      );
      console.log(`Created consumer group: ${this.groupName}`);
    } catch (error: any) {
      if (error.message.includes('BUSYGROUP')) {
        console.log(`Consumer group ${this.groupName} already exists`);
      } else {
        throw error;
      }
    }
  }

  async read(options: Partial<ConsumerOptions> = {}): Promise<ConsumedMessage[]> {
    const {
      count = 10,
      blockMs = 5000,
      autoAck = false,
    } = options;

    const result = await this.redis.xreadgroup(
      'GROUP', this.groupName, this.consumerName,
      'COUNT', count,
      'BLOCK', blockMs,
      'STREAMS', this.streamName, '>'
    );

    return this.parseReadResult(result, autoAck);
  }

  private parseReadResult(
    result: any,
    autoAck: boolean
  ): ConsumedMessage[] {
    if (!result) return [];

    const messages: ConsumedMessage[] = [];
    
    // Result format: [[stream, [[id, [field, value, ...]]]]]
    for (const [stream, entries] of result) {
      for (const [id, fields] of entries) {
        const fieldObj: Record<string, string> = {};
        for (let i = 0; i < fields.length; i += 2) {
          fieldObj[fields[i]] = fields[i + 1];
        }

        messages.push({
          id,
          stream: stream as string,
          group: this.groupName,
          consumer: this.consumerName,
          fields: fieldObj,
          parsed: this.tryParseFields(fieldObj),
        });

        if (autoAck) {
          this.ack(id);
        }
      }
    }

    return messages;
  }

  private tryParseFields(fields: Record<string, string>): Record<string, any> {
    const parsed: Record<string, any> = {};
    for (const [key, value] of Object.entries(fields)) {
      try {
        parsed[key] = JSON.parse(value);
      } catch {
        parsed[key] = value;
      }
    }
    return parsed;
  }

  async ack(messageId: string): Promise<number> {
    return this.redis.xack(this.streamName, this.groupName, messageId);
  }

  async ackMultiple(messageIds: string[]): Promise<number> {
    return this.redis.xack(this.streamName, this.groupName, ...messageIds);
  }

  async getPending(): Promise<PendingInfo[]> {
    const result = await this.redis.xpending(this.streamName, this.groupName);
    
    if (!result || result.length < 4) return [];
    
    const [, count, firstId, lastId, consumers] = result;
    return (consumers as any[]).map((c: any) => ({
      consumer: c[0],
      pendingCount: c[1],
      lastDeliveryId: c[2],
    }));
  }

  async claimStaleMessages(
    minIdleTimeMs: number,
    minClaims = 1
  ): Promise<ConsumedMessage[]> {
    // Get pending messages
    const pending = await this.redis.xpending(
      this.streamName,
      this.groupName,
      '-',
      '+',
      minClaims
    );

    const staleIds: string[] = [];
    for (const entry of pending as any[]) {
      const [, idle] = entry;
      if (idle >= minIdleTimeMs) {
        staleIds.push(entry[0]);
      }
    }

    if (staleIds.length === 0) return [];

    // Claim messages
    const result = await this.redis.xclaim(
      this.streamName,
      this.groupName,
      this.consumerName,
      minIdleTimeMs,
      ...staleIds
    );

    return this.parseReadResult(result, false);
  }

  async processMessages(
    handler: (msg: ConsumedMessage) => Promise<void>,
    options: Partial<ConsumerOptions> = {}
  ): Promise<{ processed: number; failed: number }> {
    let processed = 0;
    let failed = 0;

    while (true) {
      const messages = await this.read(options);

      for (const msg of messages) {
        try {
          await handler(msg);
          await this.ack(msg.id);
          processed++;
        } catch (error) {
          console.error(`Failed to process message ${msg.id}:`, error);
          failed++;
        }
      }

      // If no messages, exit loop (caller can call again)
      if (messages.length === 0) {
        break;
      }
    }

    return { processed, failed };
  }
}

// Usage
async function processOrders() {
  const consumer = new StreamConsumer(
    redis,
    'orders:processing',
    'order-processors',
    `worker-${process.pid}`
  );

  // Initialize consumer group
  await consumer.initializeGroup('$');

  console.log('Starting order processor...');

  while (true) {
    const messages = await consumer.read({ blockMs: 10000, count: 10 });

    for (const msg of messages) {
      const { id, parsed } = msg;
      console.log(`Processing order ${id}:`, parsed);

      try {
        // Process the order
        await processOrder(parsed);
        
        // Acknowledge success
        await consumer.ack(id);
        console.log(`Order ${id} processed successfully`);
      } catch (error) {
        console.error(`Failed to process order ${id}:`, error);
        // Message stays pending for retry
      }
    }
  }
}
```

### 3.6 Python Stream Implementation

```python
import redis
import json
import time
import threading
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class StreamMessage:
    """Represents a consumed stream message"""
    id: str
    stream: str
    group: str
    consumer: str
    fields: Dict[str, Any]
    
    @property
    def parsed_payload(self) -> Optional[Any]:
        """Try to parse 'payload' or 'data' field as JSON"""
        for key in ('payload', 'data', 'json'):
            if key in self.fields:
                try:
                    return json.loads(self.fields[key])
                except (json.JSONDecodeError, TypeError):
                    pass
        return None


class StreamProducer:
    """
    Producer for Redis Streams
    """
    
    def __init__(self, redis_client: redis.Redis, stream_name: str):
        self.redis = redis_client
        self.stream = stream_name
    
    def xadd(
        self, 
        fields: Dict[str, Any], 
        maxlen: Optional[int] = None,
        approximate: bool = True,
        entry_id: str = '*'
    ) -> str:
        """
        Add entry to stream
        
        Args:
            fields: Dictionary of field-value pairs
            maxlen: Maximum stream length (None for unlimited)
            approximate: Use ~ for approximate trimming
            entry_id: Entry ID, use '*' for auto-generate
        
        Returns:
            Entry ID of the added message
        """
        args = [self.stream]
        
        # Add trimming option
        if maxlen:
            modifier = 'MAXLEN' if not approximate else 'MAXLEN~'
            args.append(f'{modifier} {maxlen}')
        
        args.append(entry_id)
        
        # Add field-value pairs
        for field, value in fields.items():
            args.append(field)
            if isinstance(value, (dict, list)):
                args.append(json.dumps(value))
            else:
                args.append(str(value))
        
        return self.redis.execute_command('XADD', *args)
    
    def xadd_batch(
        self, 
        entries: List[Dict[str, Any]], 
        maxlen: Optional[int] = None
    ) -> List[str]:
        """Add multiple entries in a pipeline"""
        pipe = self.redis.pipeline()
        
        for fields in entries:
            args = [self.stream]
            if maxlen:
                args.append(f'MAXLEN~ {maxlen}')
            args.append('*')
            for field, value in fields.items():
                args.append(field)
                if isinstance(value, (dict, list)):
                    args.append(json.dumps(value))
                else:
                    args.append(str(value))
            pipe.execute_command('XADD', *args)
        
        results = pipe.execute()
        return [r.decode() if isinstance(r, bytes) else r for r in results]


class StreamConsumer:
    """
    Consumer for Redis Streams với Consumer Groups support
    """
    
    def __init__(
        self, 
        redis_client: redis.Redis, 
        stream_name: str,
        group_name: str,
        consumer_name: str
    ):
        self.redis = redis_client
        self.stream = stream_name
        self.group = group_name
        self.consumer = consumer_name
    
    def create_group(self, start_id: str = '$') -> bool:
        """
        Create consumer group if not exists
        
        Args:
            start_id: '$' for new messages only, '0' for all messages
        
        Returns:
            True if created, False if already exists
        """
        try:
            self.redis.xgroup(
                'CREATE', 
                self.stream, 
                self.group, 
                start_id, 
                'MKSTREAM'
            )
            return True
        except redis.ResponseError as e:
            if 'BUSYGROUP' in str(e):
                return False
            raise
    
    def read(
        self, 
        count: int = 10, 
        block_ms: int = 5000,
        auto_ack: bool = False
    ) -> List[StreamMessage]:
        """
        Read new messages from stream
        
        Returns:
            List of StreamMessage objects
        """
        result = self.redis.xreadgroup(
            self.group,
            self.consumer,
            {self.stream: '>'},
            count=count,
            block=block_ms
        )
        
        return self._parse_result(result, auto_ack)
    
    def _parse_result(
        self, 
        result: Any, 
        auto_ack: bool
    ) -> List[StreamMessage]:
        """Parse XREADGROUP response"""
        messages = []
        
        if not result:
            return messages
        
        # Result format: [(stream, [(id, fields)])]
        for stream, entries in result:
            for entry_id, fields in entries:
                # Convert fields list to dict
                field_dict = {}
                for i in range(0, len(fields), 2):
                    key = fields[i].decode() if isinstance(fields[i], bytes) else fields[i]
                    value = fields[i+1]
                    value = value.decode() if isinstance(value, bytes) else value
                    
                    # Try to parse JSON
                    if isinstance(value, str):
                        try:
                            value = json.loads(value)
                        except json.JSONDecodeError:
                            pass
                    
                    field_dict[key] = value
                
                msg = StreamMessage(
                    id=entry_id,
                    stream=stream,
                    group=self.group,
                    consumer=self.consumer,
                    fields=field_dict
                )
                
                if auto_ack:
                    self.ack(entry_id)
                
                messages.append(msg)
        
        return messages
    
    def ack(self, message_id: str) -> int:
        """Acknowledge a message"""
        return self.redis.xack(self.stream, self.group, message_id)
    
    def ack_multiple(self, message_ids: List[str]) -> int:
        """Acknowledge multiple messages"""
        return self.redis.xack(self.stream, self.group, *message_ids)
    
    def pending(
        self, 
        start: str = '-', 
        end: str = '+', 
        count: int = 100
    ) -> List[Dict]:
        """Get pending messages info"""
        result = self.redis.xpending(self.stream, self.group, start, end, count)
        
        if not result:
            return []
        
        # Parse pending info
        _, count, min_id, max_id, consumers = result
        
        pending_list = []
        for consumer_data in consumers:
            pending_list.append({
                'consumer': consumer_data[0],
                'pending_count': consumer_data[1],
                'last_delivery_id': consumer_data[2],
            })
        
        return pending_list
    
    def claim(
        self, 
        min_idle_ms: int, 
        start: str = '-', 
        end: str = '+', 
        count: int = 10
    ) -> List[StreamMessage]:
        """
        Claim pending messages that have been idle for min_idle_ms
        Useful for recovering from crashed consumers
        """
        result = self.redis.xautoclaim(
            self.stream,
            self.group,
            self.consumer,
            min_idle_ms,
            start,
            count=count
        )
        
        return self._parse_result([(self.stream, result[1])], False)
    
    def process_loop(
        self,
        handler: Callable[[StreamMessage], Any],
        count: int = 10,
        block_ms: int = 5000,
        on_error: Optional[Callable[[Exception, StreamMessage], None]] = None
    ) -> None:
        """
        Process messages in a loop
        
        Args:
            handler: Function to process each message
            count: Max messages per read
            block_ms: Block timeout
            on_error: Optional error handler
        """
        while True:
            try:
                messages = self.read(count=count, block_ms=block_ms)
                
                for msg in messages:
                    try:
                        handler(msg)
                        self.ack(msg.id)
                    except Exception as e:
                        if on_error:
                            on_error(e, msg)
                        else:
                            raise
                
                # If no messages, sleep briefly before next poll
                if not messages:
                    time.sleep(0.1)
            
            except KeyboardInterrupt:
                print("Shutting down consumer...")
                break
            except Exception as e:
                print(f"Error in consumer loop: {e}")
                time.sleep(1)  # Back off on error


# Usage Example
if __name__ == "__main__":
    client = redis.Redis(host='localhost', port=6379, decode_responses=False)
    
    # Producer
    producer = StreamProducer(client, 'events:orders')
    
    producer.xadd({
        'type': 'order.created',
        'order_id': 'ORD-001',
        'customer_id': 'CUST-123',
        'total': 99.99,
        'items': json.dumps([{'sku': 'SKU1', 'qty': 2}])
    })
    
    # Consumer
    consumer = StreamConsumer(client, 'events:orders', 'order-processors', 'worker-1')
    consumer.create_group('$')
    
    def handle_order(msg: StreamMessage):
        print(f"Processing order: {msg.id}")
        print(f"Fields: {msg.fields}")
        # Process the order...
    
    consumer.process_loop(handle_order, count=10, block_ms=5000)
```

## 4. Consumer Groups Chi Tiết

### 4.1 Consumer Group Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Redis Stream                                │
│                      events:orders                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
│  │ msg:1   │ │ msg:2   │ │ msg:3   │ │ msg:4   │ │ msg:5   │  │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘  │
└───────┼───────────┼───────────┼───────────┼───────────┼───────┘
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Consumer Group: order-processors                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Pending Entries List (PEL) - Messages delivered but not  │  │
│  │ acknowledged                                               │  │
│  │ [msg:1(worker-1), msg:3(worker-2), msg:4(worker-1)]        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
        │               │               │
        ▼               ▼               ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │Consumer 1 │   │Consumer 2 │   │Consumer 3 │
  │(worker-1)│   │(worker-2)│   │(worker-3) │
  └──────────┘   └──────────┘   └──────────┘
```

### 4.2 Consumer Group Management

```typescript
class ConsumerGroupManager {
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async createGroups(
    streamName: string,
    groups: Array<{ name: string; startId: string }>
  ): Promise<void> {
    for (const { name, startId } of groups) {
      try {
        await this.redis.xgroup(
          'CREATE',
          streamName,
          name,
          startId,
          'MKSTREAM'
        );
        console.log(`Created group: ${name}`);
      } catch (error: any) {
        if (!error.message.includes('BUSYGROUP')) {
          throw error;
        }
        console.log(`Group ${name} already exists`);
      }
    }
  }

  async listGroups(streamName: string): Promise<GroupInfo[]> {
    const info = await this.redis.xinfo('GROUPS', streamName);
    
    return info.map((group: any[]) => ({
      name: group[1],
      consumers: group[3],
      pending: group[4],
      lastDeliveredId: group[5],
    }));
  }

  async deleteGroup(streamName: string, groupName: string): Promise<void> {
    await this.redis.xgroup('DELGROUP', streamName, groupName);
  }

  async showStreamInfo(streamName: string): Promise<StreamInfo> {
    const info = await this.redis.xinfo('STREAM', streamName);
    
    return {
      length: info[1],
      firstEntry: info[3],
      lastEntry: info[5],
      maxEntryId: info[7],
      groups: info[9],
      consumers: info[11],
      memoryUsage: info[13],
      lastGeneratedId: info[15],
    };
  }
}
```

## 5. Stream Trimming và Maintenance

### 5.1 Trimming Strategies

```typescript
class StreamMaintenance {
  private redis: Redis;

  async trimByLength(
    streamName: string,
    maxLength: number,
    approximate = true
  ): Promise<number> {
    const modifier = approximate ? 'MAXLEN ~' : 'MAXLEN';
    return this.redis.xtrim(streamName, `${modifier} ${maxLength}`);
  }

  async trimById(
    streamName: string,
    minId: string
  ): Promise<number> {
    return this.redis.xtrim(streamName, 'MINID', minId);
  }

  async getStreamInfo(streamName: string): Promise<StreamStats> {
    const [length, radixTreeNodes, groups, consumers, range] = await Promise.all([
      this.redis.xlen(streamName),
      this.redis.xinfo('GROUPS', streamName),
      Promise.resolve(0), // Will be populated
      Promise.resolve(0),
      this.redis.xrange(streamName, '-', '+', 'COUNT', 1),
    ]);

    return {
      length,
      firstEntryId: range[0]?.[0] || null,
      lastEntryId: range[range.length - 1]?.[0] || null,
      groupCount: groups.length,
      consumerCount: groups.reduce((sum, g: any) => sum + g[3], 0),
    };
  }

  async cleanup(streamName: string, maxLength: number): Promise<void> {
    console.log(`Cleaning up stream ${streamName} to ${maxLength} entries`);
    const trimmed = await this.trimByLength(streamName, maxLength);
    console.log(`Trimmed ${trimmed} entries`);
  }
}
```

### 5.2 Automated Maintenance

```typescript
class StreamMaintenanceScheduler {
  private redis: Redis;
  private intervals: Map<string, NodeJS.Timeout>;

  constructor(redis: Redis) {
    this.redis = redis;
    this.intervals = new Map();
  }

  scheduleMaintenance(
    streamName: string,
    maxLength: number,
    intervalMs: number = 3600000 // 1 hour
  ): void {
    // Initial cleanup
    this.doMaintenance(streamName, maxLength);

    // Schedule periodic cleanup
    const interval = setInterval(
      () => this.doMaintenance(streamName, maxLength),
      intervalMs
    );

    this.intervals.set(streamName, interval);
  }

  private async doMaintenance(streamName: string, maxLength: number): Promise<void> {
    try {
      const currentLength = await this.redis.xlen(streamName);
      
      if (currentLength > maxLength * 1.1) {
        await this.redis.xtrim(streamName, 'MAXLEN ~', maxLength);
        console.log(`[${new Date().toISOString()}] ${streamName}: trimmed ${currentLength - maxLength} entries`);
      }
    } catch (error) {
      console.error(`Maintenance error for ${streamName}:`, error);
    }
  }

  stopAll(): void {
    this.intervals.forEach((interval, streamName) => {
      clearInterval(interval);
      console.log(`Stopped maintenance for ${streamName}`);
    });
    this.intervals.clear();
  }
}
```

## 6. Real-World Patterns

### 6.1 Event Sourcing

```typescript
interface Event {
  id: string;
  aggregateId: string;
  type: string;
  version: number;
  payload: object;
  metadata: {
    userId?: string;
    correlationId?: string;
    timestamp: number;
  };
}

class EventStore {
  private redis: Redis;
  private readonly STREAM_PREFIX = 'events:';
  private readonly CONSUMER_GROUP = 'event-handlers';

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async appendEvent(event: Event): Promise<string> {
    const streamName = `${this.STREAM_PREFIX}${event.aggregateId}`;
    
    return this.redis.xadd(streamName, '*',
      'type', event.type,
      'version', event.version.toString(),
      'payload', JSON.stringify(event.payload),
      'metadata', JSON.stringify(event.metadata),
      'timestamp', event.metadata.timestamp.toString()
    );
  }

  async getEvents(
    aggregateId: string,
    fromVersion?: number
  ): Promise<Event[]> {
    const streamName = `${this.STREAM_PREFIX}${aggregateId}`;
    
    let startId = '0-0';
    if (fromVersion !== undefined) {
      // Estimate ID based on version (simplified)
      startId = fromVersion.toString() + '-0';
    }

    const entries = await this.redis.xrange(streamName, startId, '+');
    
    return entries.map(([id, fields]) => {
      const event: any = { id };
      for (let i = 0; i < fields.length; i += 2) {
        const key = fields[i] as string;
        const value = fields[i + 1] as string;
        
        if (key === 'payload' || key === 'metadata') {
          event[key] = JSON.parse(value);
        } else if (key === 'version' || key === 'timestamp') {
          event[key] = parseInt(value);
        } else {
          event[key] = value;
        }
      }
      return event as Event;
    });
  }

  async subscribeToAllEvents(
    handler: (event: Event) => Promise<void>
  ): Promise<void> {
    // Subscribe to pattern matching all aggregate streams
    const consumer = new StreamConsumer(
      this.redis,
      'events:*', // Pattern stream name
      this.CONSUMER_GROUP,
      `handler-${process.pid}`
    );

    // Note: This requires using XREADGROUP with pattern
    // For actual pattern streams, use PSUBSCRIBE approach
  }
}
```

### 6.2 Job Queue

```typescript
interface Job {
  id: string;
  type: string;
  payload: object;
  priority?: number;
  retryCount?: number;
  maxRetries?: number;
}

class JobQueue {
  private redis: Redis;
  private readonly QUEUE_STREAM = 'jobs:queue';
  private readonly DEAD_LETTER = 'jobs:dead';
  private readonly CONSUMER_GROUP = 'job-workers';

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async enqueue(job: Job): Promise<string> {
    const fields: string[] = [
      'id', job.id,
      'type', job.type,
      'payload', JSON.stringify(job.payload),
      'createdAt', Date.now().toString(),
    ];

    if (job.priority !== undefined) {
      fields.push('priority', job.priority.toString());
    }
    if (job.retryCount !== undefined) {
      fields.push('retryCount', job.retryCount.toString());
    }
    if (job.maxRetries !== undefined) {
      fields.push('maxRetries', job.maxRetries.toString());
    }

    return this.redis.xadd(this.QUEUE_STREAM, '*', ...fields);
  }

  async enqueueBatch(jobs: Job[]): Promise<string[]> {
    const pipeline = this.redis.pipeline();
    
    for (const job of jobs) {
      const fields: string[] = [
        'id', job.id,
        'type', job.type,
        'payload', JSON.stringify(job.payload),
        'createdAt', Date.now().toString(),
      ];
      pipeline.xadd(this.QUEUE_STREAM, '*', ...fields);
    }

    const results = await pipeline.exec();
    return results?.map(([_, id]) => id as string) || [];
  }

  async processJob(
    workerId: string,
    handler: (job: Job) => Promise<void>
  ): Promise<{ processed: number; failed: number }> {
    const consumer = new StreamConsumer(
      this.redis,
      this.QUEUE_STREAM,
      this.CONSUMER_GROUP,
      workerId
    );

    await consumer.createGroup('$');

    let processed = 0;
    let failed = 0;

    while (true) {
      const messages = await consumer.read({ count: 1, blockMs: 5000 });

      for (const msg of messages) {
        const job: Job = {
          id: msg.fields.id,
          type: msg.fields.type,
          payload: JSON.parse(msg.fields.payload),
          retryCount: parseInt(msg.fields.retryCount || '0'),
          maxRetries: parseInt(msg.fields.maxRetries || '3'),
        };

        try {
          await handler(job);
          await consumer.ack(msg.id);
          processed++;
        } catch (error) {
          console.error(`Job ${job.id} failed:`, error);
          await this.handleJobFailure(job, msg.id);
          failed++;
        }
      }

      if (messages.length === 0) break;
    }

    return { processed, failed };
  }

  private async handleJobFailure(job: Job, messageId: string): Promise<void> {
    if (job.retryCount! < job.maxRetries!) {
      // Requeue with incremented retry count
      await this.redis.xadd(this.QUEUE_STREAM, '*',
        'id', job.id,
        'type', job.type,
        'payload', JSON.stringify(job.payload),
        'retryCount', (job.retryCount! + 1).toString(),
        'maxRetries', job.maxRetries!.toString(),
        'failedAt', Date.now().toString()
      );
    } else {
      // Move to dead letter queue
      await this.redis.xadd(this.DEAD_LETTER, '*',
        'originalId', job.id,
        'type', job.type,
        'payload', JSON.stringify(job.payload),
        'failedAt', Date.now().toString(),
        'originalMessageId', messageId
      );
    }
  }
}
```

## 7. Best Practices

### 7.1 Naming Conventions

```typescript
// Stream naming
const STREAM_CONVENTIONS = {
  // Events
  'events:{entity}:{aggregateId}',  // events:orders:ORD-001
  'events:{entity}:{action}',        // events:user:login
  
  // Jobs/Queue
  'jobs:{queueName}:pending',        // jobs:email:pending
  'jobs:{queueName}:dead',           // jobs:email:dead
  
  // Real-time data
  'realtime:{type}:{id}',           // realtime:stock:AAPL
  'sensors:{sensorId}:data',        // sensors:temp-001:data
  
  // Logs/Audit
  'logs:{service}:{level}',          // logs:api:error
  'audit:{entity}:{action}',        // audit:user:update
};

// Consumer group naming
const GROUP_CONVENTIONS = {
  '{service}:{component}:processors', // order-service:fulfillment:processors
  '{service}:{queue}:workers',         // notification-service:email:workers
  '{application}:{purpose}:handlers',   // analytics:event:handlers
};
```

### 7.2 Performance Tips

```typescript
// 1. Use pipelining for batch operations
async function batchAdd(producer: StreamProducer, items: any[]) {
  const pipeline = producer.redis.pipeline();
  
  for (const item of items) {
    pipeline.xadd(producer.streamName, '*', ...flatten(item));
  }
  
  return pipeline.exec();
}

// 2. Use approximate trimming
await redis.xtrim(stream, 'MAXLEN ~', 10000); // Faster than exact

// 3. Use blocking reads for consumers
const messages = await redis.xreadgroup(
  'GROUP', group, consumer,
  'BLOCK', 5000,  // Block 5 seconds
  'COUNT', 10,
  'STREAMS', stream, '>'
);

// 4. Limit consumer group size
// Don't have too many consumers in one group
// Each consumer needs to track its own PEL

// 5. Clean up pending entries
// Use XCLAIM for stale messages
// Use XACK promptly to reduce PEL size
```

### 7.3 Monitoring

```redis
# Monitor stream health
XINFO STREAM mystream FULL

# Check consumer groups
XINFO GROUPS mystream

# Check consumers in group
XINFO CONSUMERS mystream mygroup

# Monitor pending entries
XPENDING mystream mygroup - + 100

# Stream statistics
XLEN mystream

# Memory usage
DEBUG OBJECT ENCODING mystream
```

## 8. Troubleshooting

### 8.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Messages not consumed | Wrong start ID | Use '>' for new messages only |
| Duplicate processing | No ACK after processing | Always ACK after successful processing |
| Messages lost | Consumer group not created MKSTREAM | Create group with MKSTREAM flag |
| Pending queue growing | Handler failing silently | Check error logs, implement DLQ |
| Memory growth | Stream not trimmed | Implement XTRIM maintenance |
| Consumer not receiving | Block timeout too short | Increase block timeout |

### 8.2 Debug Commands

```redis
# Stream information
XINFO STREAM streamName FULL
XINFO GROUPS streamName
XINFO CONSUMERS streamName groupName

# Pending entries
XPENDING streamName groupName - + 10

# Read specific entries
XRANGE streamName 1704064200000-0 1704064300000-0

# Check message fields
XRANGE streamName MESSAGE_ID MESSAGE_ID
```

## 9. References

- [Redis Streams Documentation](https://redis.io/docs/data-types/streams/)
- [Redis Pub/Sub Documentation](https://redis.io/docs/data-types/pubsub/)
- [Stream Tutorial](https://redis.io/docs/data-types/streams-tutorial/)
- [Redis Streams vs Kafka](https://redis.io/blog/streams/)
- [Building Event Sourcing with Redis](https://redis.io/blog/event-sourcing-with-redis-streams/)
