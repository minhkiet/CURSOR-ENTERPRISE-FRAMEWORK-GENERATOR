# Cloudflare Knowledge Base - FAQ

## Tổng quan

Document này cung cấp 10 câu hỏi thường gặp và câu trả lời chi tiết về Cloudflare trong Cursor Enterprise Framework.

## Câu hỏi 1: Làm thế nào để configure Cloudflare Workers?

### Câu trả lời

Cloudflare Workers cho phép chạy code tại edge locations. Dưới đây là hướng dẫn chi tiết:

```javascript
// Basic Worker structure
export default {
  async fetch(request, env, ctx) {
    // Handle the request
    const url = new URL(request.url);
    
    // Route handling
    if (url.pathname === '/api/users') {
      return handleUsersAPI(request, env);
    }
    
    if (url.pathname === '/') {
      return handleHome(request, env);
    }
    
    // Default: fetch from origin
    return fetch(request);
  }
};

// Environment variables in wrangler.toml
// wrangler.toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-01-01"

[vars]
API_URL = "https://api.example.com"

[[env.production.secrets]]
name = "API_KEY"
```

```yaml
# Deploy via GitHub Actions
# .github/workflows/deploy.yml
name: Deploy Worker

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Cloudflare
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          environment: production
```

## Câu hỏi 2: Sự khác biệt giữa các SSL modes là gì?

### Câu trả lời

| Mode | User → Cloudflare | Cloudflare → Origin | Use Case |
|------|-------------------|---------------------|----------|
| Off | No encryption | No encryption | **Never use in production** |
| Flexible | HTTPS optional | HTTP only | Development only |
| Full | Encrypted | HTTPS (any cert) | Legacy origins |
| Strict | Encrypted | HTTPS (valid cert) | **Recommended** |

```yaml
# SSL Configuration
ssl:
  # Recommended for production
  mode: "strict"
  
  # Settings
  min_tls_version: "1.2"
  tls_1_3: "on"
  
  # Certificate settings
  always_use_https: true
  opportunistic_encryption: true
```

```bash
# Verify SSL configuration
# Should show proper certificate
curl -v https://example.com 2>&1 | grep -E "(SSL|TLS|certificate)"
```

## Câu hỏi 3: Làm thế nào để configure caching cho một application?

### Câu trả lời

```yaml
# Cache configuration via Page Rules or Workers
cache:
  rules:
    # Static assets - cache aggressively
    - path: "*.{css,js,png,jpg,jpeg,gif,ico,svg,woff,woff2,ttf,eot}"
      actions:
        cache_level: "cache_everything"
        edge_cache_ttl: 604800  # 7 days
        browser_cache_ttl: 86400  # 1 day
        
    # HTML pages - cache with validation
    - path: "*.html"
      actions:
        cache_level: "cache_everything"
        edge_cache_ttl: 3600  # 1 hour
        origin_cache_control: true  # Respect origin headers
        
    # API - don't cache
    - path: "/api/*"
      actions:
        cache_level: "bypass"
        
    # Authenticated content - don't cache
    - path: "/dashboard/*"
      actions:
        cache_level: "bypass"
```

```javascript
// Cache API responses selectively via Worker
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Only cache GET requests
    if (request.method !== 'GET') {
      return fetch(request);
    }
    
    // Check cache
    const cache = caches.default;
    const cached = await cache.match(request);
    
    if (cached) {
      // Return cached response
      return cached;
    }
    
    // Fetch from origin
    const response = await fetch(request);
    
    // Only cache successful responses
    if (response.ok) {
      const newResponse = new Response(response.body, response);
      
      // Set cache headers
      if (url.pathname.startsWith('/api/public/')) {
        newResponse.headers.set('Cache-Control', 'public, max-age=300');
      }
      
      // Cache the response
      ctx.waitUntil(cache.put(request, newResponse.clone()));
      
      return newResponse;
    }
    
    return response;
  }
};
```

## Câu hỏi 4: Làm thế nào để implement rate limiting?

### Câu trả lời

```yaml
# Rate limiting rules
rate_limiting:
  rules:
    # Global rate limit
    - name: "Global rate limit"
      expression: "true"
      characteristics:
        - "ip.src"
      mitigation:
        requests_per_period: 1000
        period: 60
        action: "simulate"
        
    # API rate limit
    - name: "API rate limit"
      expression: '(http.request.uri.path contains "/api/")'
      characteristics:
        - "ip.src"
      mitigation:
        requests_per_period: 100
        period: 60
        action: "block"
        
    # Login rate limit
    - name: "Login rate limit"
      expression: '(http.request.uri.path contains "/login")'
      characteristics:
        - "ip.src"
      mitigation:
        requests_per_period: 5
        period: 300  # 5 attempts per 5 minutes
        action: "block"
```

```javascript
# Custom rate limiting via Worker
const RATE_LIMIT = 100;
const RATE_WINDOW = 60; // seconds

// Using KV store for distributed rate limiting
export default {
  async fetch(request, env) {
    const ip = request.headers.get('CF-Connecting-IP');
    const key = `rate:${ip}`;
    
    // Get current count
    const current = await env.RATE_LIMIT.get(key);
    const count = current ? parseInt(current) : 0;
    
    if (count >= RATE_LIMIT) {
      return new Response('Rate limit exceeded', {
        status: 429,
        headers: {
          'Retry-After': RATE_WINDOW.toString()
        }
      });
    }
    
    // Increment counter
    await env.RATE_LIMIT.put(key, (count + 1).toString(), {
      expirationTtl: RATE_WINDOW
    });
    
    // Continue with request
    return fetch(request);
  }
};
```

## Câu hỏi 5: Làm thế nào để configure Cloudflare Load Balancer?

### Câu trả lời

```yaml
# Load Balancer configuration
load_balancer:
  name: "production-lb"
  steering_policy: "performance"  # or "geo", "random", "weighted"
  
  # Primary pool
  pools:
    - name: "primary-pool"
      origins:
        - name: "web-1-us"
          address: "us.web1.example.com"
          weight: 2
          enabled: true
        - name: "web-2-us"
          address: "us.web2.example.com"
          weight: 1
          enabled: true
        - name: "web-3-eu"
          address: "eu.web1.example.com"
          weight: 1
          enabled: true
      health_check:
        path: "/health"
        port: 443
        protocol: "HTTPS"
        interval: 30
        timeout: 10
        retries: 3
        unhealthy_threshold: 3
        expected_codes: "200-299"
        
    - name: "fallback-pool"
      origins:
        - name: "backup"
          address: "backup.example.com"
          enabled: true
      health_check:
        path: "/health"
        port: 443
        
  # Failover configuration
  fallback_pool: "fallback-pool"
  
  # Session affinity
  session_affinity:
    enabled: true
    ttl: 3600
```

## Câu hỏi 6: Làm thế nào để secure một API với Cloudflare?

### Câu trả lời

```yaml
# Security configuration for API
security:
  # WAF rules
  waf:
    rules:
      - name: "Block SQL injection"
        expression: '(sql_signature_match)'
        action: "block"
        
      - name: "Block XSS"
        expression: '(xss_signature_match)'
        action: "block"
        
  # Rate limiting
  rate_limiting:
    rules:
      - name: "API rate limit"
        expression: '(http.request.uri.path contains "/api/")'
        mitigation:
          requests_per_period: 100
          period: 60
          action: "block"
          
  # Bot management
  bot_management:
    enabled: true
```

```javascript
// JWT validation at edge
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Skip auth for public endpoints
    if (url.pathname.startsWith('/api/public/')) {
      return fetch(request);
    }
    
    // Get token from header
    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }
    
    const token = authHeader.substring(7);
    
    try {
      // Verify JWT at edge
      const payload = await verifyJWT(token, env.JWT_SECRET);
      
      // Add user context to request
      const newRequest = new Request(request, {
        headers: {
          ...Object.fromEntries(request.headers),
          'X-User-ID': payload.sub,
          'X-User-Role': payload.role
        }
      });
      
      return fetch(newRequest);
      
    } catch (err) {
      return new Response('Invalid token', { status: 401 });
    }
  }
};

async function verifyJWT(token, secret) {
  // Implementation using jose or similar
  const secretKey = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['verify']
  );
  
  const { payload } = await jwtVerify(token, secretKey);
  return payload;
}
```

## Câu hỏi 7: Làm thế nào để monitor Cloudflare performance?

### Câu trả lời

```yaml
# Logpush configuration for analytics
logpush:
  enabled: true
  
  destination:
    type: "s3"
    bucket: "cf-logs-bucket"
    prefix: "logs/"
    
  fields:
    - "ZoneID"
    - "RayID"
    - "ClientRequestURL"
    - "ClientRequestMethod"
    - "EdgeStartTimestamp"
    - "CacheResponseStatus"
    - "OriginResponseStatus"
    - "ClientCountry"
    - "cf.cache.status"
    - "cf.bot.score"
    - "EdgeResponseBytes"
    - "OriginResponseTime"
    
  # Filter for specific patterns
  filter: '(not cf.colo.id eq 1234)'
```

```javascript
# Worker to track custom metrics
export default {
  async fetch(request, env) {
    const start = Date.now();
    
    const response = await fetch(request);
    
    const duration = Date.now() - start;
    const cf = request.cf;
    
    // Log to external service
    await sendMetrics({
      url: request.url,
      method: request.method,
      status: response.status,
      duration,
      cacheStatus: cf.cacheStatus,
      botScore: cf.botScore,
      country: cf.country,
      colo: cf.colo
    }, env);
    
    return response;
  }
};

async function sendMetrics(data, env) {
  // Send to analytics service
  await fetch('https://analytics.example.com/metrics', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${env.ANALYTICS_TOKEN}`
    },
    body: JSON.stringify(data)
  });
}
```

## Câu hỏi 8: Làm thế nào để configure Cloudflare Access cho internal applications?

### Câu trả lời

```yaml
# Cloudflare Access configuration
access:
  application:
    name: "Internal Dashboard"
    domain: "dashboard.internal.example.com"
    type: "ssh"  # or "app", "browse", "self-hosted"
    
    # Identity provider
    idp:
      - name: "Google Workspace"
        type: "google"
        config:
          client_id: "${GOOGLE_CLIENT_ID}"
          client_secret: "${GOOGLE_CLIENT_SECRET}"
          
    # Access policy
    policies:
      - name: "Engineering team"
        decision: "allow"
        include:
          - email_domain: "example.com"
        require:
          - group: "engineering"
        exclude:
          - email: "intern@example.com"
          
      - name: "Contractors"
        decision: "block"
        include:
          - email_domain: "contractor.com"
```

```bash
# Create Access application via API
curl -X POST "https://api.cloudflare.com/client/v4/access/applications" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Internal API",
    "domain": "api.internal.example.com",
    "type": "api"
  }'
```

## Câu hỏi 9: Sự khác biệt giữa Cloudflare Workers và Durable Objects là gì?

### Câu trả lời

| Feature | Workers | Durable Objects |
|---------|---------|-----------------|
| State | Stateless | Stateful |
| Instance | One per request | Single per key |
| Persistence | None | Durable storage |
| Use Case | Transformations, routing | Real-time, sessions |
| Scaling | Per-request | Per-key |
| Consistency | None | Strong |

```javascript
// Worker - stateless, scaled per request
export default {
  async fetch(request, env) {
    // No state, creates fresh for each request
    return fetch(request);
  }
};

// Durable Object - stateful, single instance per key
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.sessions = new Set();
  }
  
  async fetch(request) {
    const url = new URL(request.url);
    
    if (url.pathname === '/join') {
      // Get WebSocket from request
      const webSocketPair = new WebSocketPair();
      const [client, server] = webSocketPair;
      
      // Accept WebSocket
      await server.accept();
      this.sessions.add(server);
      
      return new Response(null, {
        status: 101,
        webSocket: client
      });
    }
    
    return new Response('Not found', { status: 404 });
  }
  
  // Called when WebSocket message received
  async webSocketMessage(ws, message) {
    // Broadcast to all clients
    for (const client of this.sessions) {
      client.send(message);
    }
  }
}
```

## Câu hỏi 10: Làm thế nào để optimize costs với Cloudflare?

### Câu trả lời

```yaml
# Cost optimization strategies

# 1. Cache aggressively to reduce origin requests
cache:
  rules:
    - path: "*"
      cache_level: "cache_everything"
      edge_cache_ttl: 7200
      
# 2. Enable Argo only when needed
argo:
  smart_routing:
    enabled: true  # Monitor costs
  tiered_caching:
    enabled: true

# 3. Optimize Workers usage
workers:
  # Use smaller Workers
  # Minimize CPU time
  # Use KV efficiently
```

```javascript
// Optimize Workers for cost
export default {
  async fetch(request, env) {
    // 1. Cache at edge to avoid origin requests
    const cache = caches.default;
    const cached = await cache.match(request);
    
    if (cached) {
      return cached;
    }
    
    // 2. Minimize fetch calls
    const response = await fetch(request);
    
    // 3. Cache response if appropriate
    if (response.ok) {
      ctx.waitUntil(cache.put(request, response.clone()));
    }
    
    return response;
  }
};

// Use KV efficiently
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/config') {
      // Cache KV reads with expiration
      const config = await env.KV.get('config', 'json', {
        cacheTtl: 3600  // Cache for 1 hour
      });
      
      return new Response(JSON.stringify(config), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    return fetch(request);
  }
};
```

```bash
# Monitor costs
# Use Cloudflare Analytics to track:
# - Bandwidth
# - Requests
# - Workers invocations
# - Logpush usage

# Set up billing alerts
curl -X POST "https://api.cloudflare.com/client/v4/billing/alerts" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High bandwidth alert",
    "threshold": 1000000000000,
    "condition": "above",
    "alert_type": "bandwidth"
  }'
```

## Related Documents

- [Cloudflare Glossary](../glossary.md)
- [Cloudflare Architecture](../architecture.md)
- [Cloudflare Best Practices](../best-practice.md)
- [Cloudflare Anti-Patterns](../anti-pattern.md)
- [Cloudflare Checklist](../checklist.md)
- [Cloudflare Decision Tree](../decision-tree.md)
