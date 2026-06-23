# Cloudflare Knowledge Base - Architecture

## Tổng quan

Document này mô tả chi tiết kiến trúc hệ thống Cloudflare trong Cursor Enterprise Framework, bao gồm các components, interactions, và design patterns cho production-ready deployments.

## 1. Cloudflare Global Network Architecture

### 1.1 Edge Network Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  Cloudflare Global Edge Network                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    300+ Data Centers                        │  │
│  │                                                            │  │
│  │    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│  │    │   PoP   │  │   PoP   │  │   PoP   │  │   PoP   │    │  │
│  │    │ Frankfurt│  │  Tokyo  │  │   NYC   │  │ Sydney  │    │  │
│  │    └─────────┘  └─────────┘  └─────────┘  └─────────┘    │  │
│  │                                                            │  │
│  │    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│  │    │   PoP   │  │   PoP   │  │   PoP   │  │   PoP   │    │  │
│  │    │  London │  │Singapore│  │  Paris  │  │ Mumbai  │    │  │
│  │    └─────────┘  └─────────┘  └─────────┘  └─────────┘    │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Core Infrastructure                       │  │
│  │                                                            │  │
│  │    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│  │    │   API   │  │ Workers │  │   R2    │  │ Images │    │  │
│  │    │ Gateway │  │ Runtime │  │ Storage │  │  CDN   │    │  │
│  │    └─────────┘  └─────────┘  └─────────┘  └─────────┘    │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      Request Flow                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [User] ──► [Closest PoP] ──► [Cloudflare Network] ──► [Origin] │
│                                                                     │
│  Step 1: DNS Resolution                                           │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Cloudflare DNS → Returns proxied IP (Anycast)           │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Step 2: Edge Processing                                          │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  - DDoS protection                                       │     │
│  │  - WAF evaluation                                       │     │
│  │  - Bot detection                                        │     │
│  │  - Cache check                                         │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Step 3: Origin Request (if not cached)                          │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  - Origin Shield (optional)                             │     │
│  │  - Argo Smart Routing                                   │     │
│  │  - SSL/TLS to origin                                   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Cloudflare Workers Architecture

### 2.1 Workers Runtime

```
┌─────────────────────────────────────────────────────────────────┐
│                   Workers Runtime Architecture                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    V8 JavaScript Engine                    │  │
│  │                                                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │  │
│  │  │   Worker A   │  │   Worker B   │  │   Worker C   │       │  │
│  │  │  (fetch)    │  │  (fetch)    │  │  (fetch)    │       │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Services Runtime                         │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │  │
│  │  │   KV    │  │  R2    │  │ Durable │  │  Cache  │       │  │
│  │  │ Storage │  │Storage │  │Objects  │  │  API   │       │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Features:                                                         │
│  - 0ms cold starts (pre-warmed)                                   │
│  - Up to 50ms CPU time per request                                │
│  - Up to 128MB memory per Worker                                  │
│  - Automatic global deployment                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Worker Execution Context

```javascript
// Worker lifecycle
export default {
  async fetch(request, env, ctx) {
    // Request phase
    const url = new URL(request.url);
    
    // Process request
    const response = await handleRequest(request, env);
    
    // Response phase with waitUntil for background tasks
    ctx.waitUntil(backgroundTask(env));
    
    return response;
  }
};

// Scheduled Worker (Cron Trigger)
export default {
  async scheduled(event, env, ctx) {
    // Runs on cron schedule
    await processScheduledTask();
  }
};
```

## 3. Cloudflare Cache Architecture

### 3.1 Multi-Tier Caching

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cache Architecture                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Browser Cache                           │  │
│  │  - Set via Cache-Control headers                           │  │
│  │  - browser_cache_ttl configuration                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Edge Cache (PoP)                        │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│  │  │  L1     │  │  L1     │  │  L1     │  │  L1     │      │  │
│  │  │ Cache   │  │ Cache   │  │ Cache   │  │ Cache   │      │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  L2 Cache (Regional)                  │  │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐              │  │  │
│  │  │  │  L2     │  │  L2     │  │  L2     │              │  │  │
│  │  │  │ Cache   │  │ Cache   │  │ Cache   │              │  │  │
│  │  │  └─────────┘  └─────────┘  └─────────┘              │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Origin Shield                            │  │
│  │  - Single cache point per region                           │  │
│  │  - Reduces origin load                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Origin Server                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Cache Key Configuration

```yaml
# Cache Key configuration
cache:
  # Custom cache key
  cache_key:
    include:
      - protocol
      - host
      - uri
      - query_string
      
    exclude:
      - cf_cache_status
      - cf_ray
      
    forward_parameters:  # Include specific query params
      - "page"
      - "limit"
      
  # Query string settings
  query_string_config:
    include_all: false
    include: ["search", "filter"]
```

## 4. Load Balancer Architecture

### 4.1 Global Load Balancing

```
┌─────────────────────────────────────────────────────────────────┐
│                Global Load Balancer Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Traffic Manager                           │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                 Steering Policies                      │  │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │  │  │
│  │  │  │ Perfor- │  │   Geo   │  │ Weighted│             │  │  │
│  │  │  │ mance   │  │Routing  │  │ Routing │             │  │  │
│  │  │  └─────────┘  └─────────┘  └─────────┘             │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      Health Monitor                         │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │  │
│  │  │Health   │  │Health   │  │Health   │                  │  │
│  │  │Check #1 │  │Check #2 │  │Check #3 │                  │  │
│  │  │ Pool A  │  │ Pool B  │  │ Pool C  │                  │  │
│  │  └─────────┘  └─────────┘  └─────────┘                  │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                        Origin Pools                        │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│  │  │ Primary │  │Secondary│  │ Backup  │  │ Failover│      │  │
│  │  │ Pool    │  │ Pool    │  │ Pool    │  │ Pool    │      │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Health Check Configuration

```yaml
# Health check configuration
load_balancer:
  pools:
    - name: "api-pool"
      origins:
        - name: "api-1"
          address: "api1.example.com"
          weight: 1
        - name: "api-2"
          address: "api2.example.com"
          weight: 1
          
      health_check:
        # HTTP/HTTPS check
        path: "/health"
        port: 443
        protocol: "HTTPS"
        method: "GET"
        
        # Timing
        interval: 30
        timeout: 10
        retries: 3
        
        # Expected response
        expected_body: "healthy"
        expected_codes: "200-299"
        
        # Headers
        headers:
          X-Custom-Header: "value"
```

## 5. Cloudflare Security Architecture

### 5.1 Security Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Stack                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Layer 1: DDoS Protection (L3/L4)                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  - Volumetric attack mitigation                            │  │
│  │  - Protocol anomalies detection                            │  │
│  │  - Rate limiting                                          │  │
│  │  - Traffic scrubing (up to 2 Tbps)                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  Layer 2: WAF (L7)                                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  - OWASP Top 10 protection                                 │  │
│  │  - Custom rules                                           │  │
│  │  - Rate limiting rules                                    │  │
│  │  - Zone Lockdown                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  Layer 3: Bot Management                                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  - ML-based bot scoring                                   │  │
│  │  - Verified bots handling                                   │  │
│  │  - Challenge responses                                     │  │
│  │  - CAPTCHA integration                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  Layer 4: SSL/TLS                                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  - End-to-end encryption                                  │  │
│  │  - Certificate management                                  │  │
│  │  - TLS 1.3                                               │  │
│  │  - TLS inspection (Enterprise)                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 WAF Rule Processing

```yaml
# WAF configuration
waf:
  # Managed rule sets
  rulesets:
    - name: "Cloudflare Managed Rules"
      version: "latest"
      
    - name: "OWASP ModSecurity Core Rule Set"
      version: "latest"
      sensitivity: "medium"
      
  # Custom firewall rules
  firewall:
    rules:
      - id: "block-sql-injection"
        description: "Block SQL injection attempts"
        expression: '(sql_signature_match)'
        action: "block"
        
      - id: "challenge-suspicious"
        description: "Challenge suspicious traffic"
        expression: '(cf.threat_score > 30)'
        action: "challenge"
        
      - id: "rate-limit-api"
        description: "Rate limit API endpoints"
        expression: '(http.request.uri.path contains "/api/")'
        action: "rate_limit"
        ratelimit:
          requests_per_period: 100
          period: 60
```

## 6. Durable Objects Architecture

### 6.1 State Synchronization

```
┌─────────────────────────────────────────────────────────────────┐
│                Durable Objects Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Global Coordinator                       │  │
│  │                                                            │  │
│  │  - Routes requests to correct instance                      │  │
│  │  - Manages instance lifecycle                               │  │
│  │  - Ensures single-instance-per-key semantics                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Durable Object Instance                  │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                   Object State                        │  │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │  │  │
│  │  │  │Storage  │  │ WebSocket│  │ Sessions │            │  │  │
│  │  │  │  API   │  │ Handler  │  │  Store   │            │  │  │
│  │  │  └─────────┘  └─────────┘  └─────────┘             │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Use Cases:                                                         │
│  - Real-time collaboration (documents, games)                     │
│  - Consistent caching                                              │
│  - Distributed locks                                               │
│  - Stateful compute                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Durable Object Example

```javascript
export class Counter {
  constructor(state, env) {
    this.state = state;
  }
  
  async fetch(request) {
    const url = new URL(request.url);
    
    if (url.pathname === '/increment') {
      const current = await this.state.storage.get('count') || 0;
      await this.state.storage.put('count', current + 1);
      return new Response(current + 1);
    }
    
    if (url.pathname === '/get') {
      const current = await this.state.storage.get('count') || 0;
      return new Response(current);
    }
    
    return new Response('Not found', { status: 404 });
  }
}

// WebSocket handling example
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.sessions = new Set();
  }
  
  async webSocketMessage(ws, message) {
    // Broadcast to all connected clients
    for (const client of this.sessions) {
      if (client !== ws) {
        client.send(message);
      }
    }
  }
  
  async webSocketClose(ws, code, reason, wasClean) {
    this.sessions.delete(ws);
  }
  
  async acceptWebSocket(ws, request) {
    this.sessions.add(ws);
    ws.send('Welcome to chat!');
  }
}
```

## 7. Cloudflare R2 Architecture

### 7.1 Object Storage

```
┌─────────────────────────────────────────────────────────────────┐
│                    R2 Storage Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      R2 API Gateway                         │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                   S3 Compatible API                  │  │  │
│  │  │  - GET, PUT, DELETE operations                     │  │  │
│  │  │  - Multipart uploads                               │  │  │
│  │  │  - Presigned URLs                                  │  │  │
│  │  │  - CORS configuration                              │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Storage Layer                            │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│  │  │ Bucket 1 │  │ Bucket 2 │  │ Bucket 3 │  │ Bucket N │      │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Key Features:                                                       │
│  - S3-compatible API                                                │
│  - No egress charges                                               │
│  - Automatic global replication                                     │
│  - Object versioning                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 8. Cloudflare Images Architecture

### 8.1 Image Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Image Processing Pipeline                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐                                               │
│  │ Upload Image │                                               │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    Variant Generation                        │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │  │
│  │  │Original │  │Thumbnail│  │ Preview │  │ Optimized│       │  │
│  │  │  Image  │  │  (100px)│  │ (800px) │  │  WebP   │       │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                              │                                    │
│                              ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    Edge Delivery                            │  │
│  │                                                            │  │
│  │  - Automatic format selection (WebP, AVIF)               │  │
│  │  - Resize on-the-fly                                      │  │
│  │  - Quality optimization                                    │  │
│  │  - Global CDN delivery                                     │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 9. Integration Architecture

### 9.1 Cloudflare with Kubernetes

```
┌─────────────────────────────────────────────────────────────────┐
│              Cloudflare + Kubernetes Integration                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Cloudflare Edge                           │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │  │
│  │  │   WAF   │  │   CDN   │  │ Workers │                  │  │
│  │  └─────────┘  └─────────┘  └─────────┘                  │  │
│  │                                                            │  │
│  └────────────────────────────┬──────────────────────────────┘  │
│                               │                                 │
│                               │ HTTPS                           │
│                               ▼                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Cloudflare Load Balancer                 │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │  │
│  │  │Health   │  │Geo      │  │ Failover│                  │  │
│  │  │Checks   │  │Routing  │  │         │                  │  │
│  │  └─────────┘  └─────────┘  └─────────┘                  │  │
│  │                                                            │  │
│  └────────────────────────────┬──────────────────────────────┘  │
│                               │                                 │
│                               │ Internal network                 │
│                               ▼                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Kubernetes Cluster                       │  │
│  │                                                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│  │  │  Node 1 │  │  Node 2 │  │  Node 3 │  │  Node 4 │      │  │
│  │  │┌───────┐│  │┌───────┐│  │┌───────┐│  │┌───────┐│      │  │
│  │  ││  Pod  ││  ││  Pod  ││  ││  Pod  ││  ││  Pod  ││      │  │
│  │  │└───────┘│  │└───────┘│  │└───────┘│  │└───────┘│      │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│  │                                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Related Documents

- [Cloudflare Glossary](../glossary.md)
- [Cloudflare Best Practices](../best-practice.md)
- [Cloudflare Anti-Patterns](../anti-pattern.md)
- [Cloudflare Checklist](../checklist.md)
- [Cloudflare FAQ](../faq.md)
- [Cloudflare Decision Tree](../decision-tree.md)
