# Cloudflare Knowledge Base - Anti-Patterns

## Tổng quan

Document này liệt kê các anti-patterns phổ biến khi sử dụng Cloudflare và đề xuất giải pháp thay thế. Mỗi anti-pattern được mô tả chi tiết với ví dụ về cách phát hiện và khắc phục.

## Anti-Pattern 1: Using Flexible SSL Mode

### Mô tả

Sử dụng "Flexible" SSL mode cho phép HTTP traffic giữa Cloudflare và origin, tạo ra security gap nơi data có thể bị intercept.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Flexible SSL
ssl:
  mode: "flexible"  # INSECURE!
  
# Traffic flow:
# User ──HTTPS──► Cloudflare ──HTTP──► Origin
#                          ▲
#                    Unencrypted!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Use Strict SSL
ssl:
  mode: "strict"  # Required for production
  
  # Ensures:
  # User ──HTTPS──► Cloudflare ──HTTPS──► Origin
  #                     Both ends encrypted!
```

```bash
# Verify SSL configuration
# Should show "strict" or "full"
curl -s -o /dev/null -w "%{ssl_verify_result}" https://example.com
```

## Anti-Pattern 2: Disabling Security Features

### Mô tả

Tắt WAF, DDoS protection, hoặc các security features khác để "reduce complexity" có thể expose website đến attacks.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Disabled security
security:
  waf:
    enabled: false  # SECURITY RISK!
    
  ddos_protection:
    mode: "off"    # VULNERABLE!
    
  bot_management:
    enabled: false
```

### Giải pháp

```yaml
# ✅ SOLUTION: Enable all security features
security:
  waf:
    enabled: true
    rulesets:
      - owasp_ruleset:
          sensitivity: "medium"
          
  ddos_protection:
    mode: "automatic"
    sensitivity: "medium"
    
  bot_management:
    enabled: true
    challenge_passport: "10m"
```

## Anti-Pattern 3: Caching Dynamic Content

### Mô tả

Cache những content không nên be cached như personalized pages, API responses, hoặc real-time data, dẫn đến data leakage và stale content.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Cache everything
cache:
  rules:
    - path: "/*"
      cache_level: "cache_everything"  # WRONG for dynamic content!
      
# Results in:
# - User A sees User B's data
# - Stale account information
# - Personal data leakage
```

### Giải pháp

```yaml
# ✅ SOLUTION: Selective caching
cache:
  rules:
    - description: "Static assets - cache aggressively"
      path: "*.{css,js,png,jpg,svg,woff,woff2}"
      cache_level: "cache_everything"
      edge_cache_ttl: 604800  # 7 days
      
    - description: "HTML pages - cache with validation"
      path: "*.html"
      cache_level: "cache_everything"
      edge_cache_ttl: 3600
      origin_cache_control: true
      
    - description: "API endpoints - don't cache"
      path: "/api/*"
      cache_level: "bypass"
      
    - description: "Authenticated content - don't cache"
      path: "/dashboard/*"
      cache_level: "bypass"
```

## Anti-Pattern 4: Not Using Cloudflare Workers Properly

### Mô tả

Implement Workers logic trong origin thay vì edge, miss opportunity để reduce latency và origin load.

### Ví dụ xấu

```javascript
// ❌ ANTI-PATTERN: Origin-based A/B testing
// In your origin server:
app.get('/', async (req, res) => {
  // Expensive variant selection at origin
  const variant = await selectVariant(); // Takes 100ms!
  
  // This logic should be at edge!
  const html = await renderPage(variant);
  res.send(html);
});
```

### Giải pháp

```javascript
// ✅ SOLUTION: Edge-based Workers
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Fast variant selection at edge (1-5ms)
    if (!url.searchParams.has('variant')) {
      const variant = Math.random() < 0.5 ? 'A' : 'B';
      url.searchParams.set('variant', variant);
      
      // Redirect with variant (super fast!)
      return Response.redirect(url.toString(), 302);
    }
    
    // Fetch from origin (variant already set)
    const response = await fetch(request);
    
    // Modify content based on variant at edge
    if (response.headers.get('Content-Type')?.includes('text/html')) {
      const html = await response.text();
      const variant = url.searchParams.get('variant');
      const modifiedHtml = html.replace('<body>', `<body data-variant="${variant}">`);
      
      return new Response(modifiedHtml, {
        headers: {
          ...Object.fromEntries(response.headers),
          'Content-Type': 'text/html'
        }
      });
    }
    
    return response;
  }
};
```

## Anti-Pattern 5: Overly Permissive CORS

### Mô tả

Allowing all origins (Access-Control-Allow-Origin: *) cho API endpoints có thể allow malicious sites to access protected resources.

### Ví dụ xấu

```javascript
// ❌ ANTI-PATTERN: Allow all origins
export default {
  async fetch(request) {
    const response = await fetch(request);
    
    // SECURITY RISK!
    response.headers.set('Access-Control-Allow-Origin', '*');
    
    return response;
  }
};
```

### Giải pháp

```javascript
// ✅ SOLUTION: Explicit allowed origins
const ALLOWED_ORIGINS = [
  'https://app.example.com',
  'https://admin.example.com',
  'https://staging.example.com'
];

export default {
  async fetch(request) {
    const origin = request.headers.get('Origin');
    
    // Validate origin
    if (!ALLOWED_ORIGINS.includes(origin)) {
      return new Response('Forbidden', { status: 403 });
    }
    
    const response = await fetch(request);
    
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Access-Control-Allow-Origin', origin);
    newResponse.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    newResponse.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    newResponse.headers.set('Access-Control-Max-Age', '86400');
    
    return newResponse;
  }
};
```

## Anti-Pattern 6: Not Purging Cache Properly

### Mô tả

Sau khi deploy changes, không purge cache dẫn đến users seeing stale content.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No cache purge after deploy
# Deploy new version of CSS file
# But Cloudflare still serves old cached version!

curl -X POST "https://api.cloudflare.com/client/v4/zones/{id}/purge_cache" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  # Forgot to actually send purge request!
```

### Giải pháp

```bash
# ✅ SOLUTION: Purge cache after deploy
# 1. Purge entire cache (when necessary)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{id}/purge_cache" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything": true}'

# 2. Purge specific files (preferred)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{id}/purge_cache" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"files": [
    "https://example.com/css/main.css",
    "https://example.com/js/app.js"
  ]}'

# 3. Purge by tags
curl -X POST "https://api.cloudflare.com/client/v4/zones/{id}/purge_cache" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["css", "js", "homepage"]}'
```

```yaml
# CI/CD integration for automatic cache purge
deploy:
  steps:
    - name: Deploy to origin
      run: ./deploy.sh
      
    - name: Purge Cloudflare cache
      run: |
        curl -X POST "https://api.cloudflare.com/client/v4/zones/{id}/purge_cache" \
          -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
          -H "Content-Type: application/json" \
          -d '{"purge_everything": true}'
```

## Anti-Pattern 7: Ignoring Bot Traffic

### Mô tả

Không distinguish giữa good bots (search engines) và bad bots (scrapers), dẫn đến origin overload từ malicious traffic.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No bot management
bot_management:
  enabled: false  # All bots treated equally!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Enable bot management
bot_management:
  enabled: true
  
  # Allow verified bots (Google, Bing, etc.)
  verified_bot:
    enable: true
    
  # Challenge suspicious traffic
  challenge:
    score_threshold: 30
    action: "challenge"
    
# Custom rules for known bad bots
firewall:
  rules:
    - name: "Block scrapers"
      expression: '(client.bot && not client.verifiedBot)'
      action: "block"
```

## Anti-Pattern 8: Not Using Load Balancing Failover

### Mô tả

Không configure health checks và failover cho origin servers, dẫn đến prolonged downtime khi primary origin fails.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Single origin, no failover
dns:
  records:
    - name: "@"
      type: "A"
      content: "192.0.2.1"  # Single point of failure!
      proxied: true
        
# If 192.0.2.1 goes down, site is down!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Load balancer with failover
load_balancer:
  name: "production-lb"
  steering_policy: "performance"
  
  pools:
    - name: "primary-pool"
      origins:
        - name: "web-1"
          address: "web1.example.com"
          weight: 1
        - name: "web-2"
          address: "web2.example.com"
          weight: 1
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
      health_check:
        path: "/health"
        port: 443
        
  fallback_pool: "fallback-pool"
```

## Anti-Pattern 9: Not Configuring Response Headers

### Mô tả

Không set security headers properly, miss opportunity để enhance security.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No security headers configured
# Missing:
# - Strict-Transport-Security
# - X-Content-Type-Options
# - X-Frame-Options
# - Content-Security-Policy
```

### Giải pháp

```yaml
# ✅ SOLUTION: Configure security headers
response_headers:
  rules:
    - name: "Security headers"
      path: "*"
      headers:
        Strict-Transport-Security:
          value: "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options:
          value: "nosniff"
        X-Frame-Options:
          value: "SAMEORIGIN"
        X-XSS-Protection:
          value: "1; mode=block"
        Referrer-Policy:
          value: "strict-origin-when-cross-origin"
        Permissions-Policy:
          value: "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
```

```javascript
// Or via Worker
export default {
  async fetch(request, env) {
    const response = await fetch(request);
    
    const newResponse = new Response(response.body, response);
    
    // Add security headers
    newResponse.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    newResponse.headers.set('X-Content-Type-Options', 'nosniff');
    newResponse.headers.set('X-Frame-Options', 'SAMEORIGIN');
    newResponse.headers.set('X-XSS-Protection', '1; mode=block');
    newResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    
    return newResponse;
  }
};
```

## Anti-Pattern 10: Overlapping Page Rules

### Mô tả

Tạo Page Rules với overlapping patterns có thể dẫn đến unpredictable behavior.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Overlapping rules
page_rules:
  # Rule 1: Cache everything
  - url: "example.com/*"
    cache_level: "cache_everything"
    
  # Rule 2: Don't cache /api/*
  - url: "example.com/api/*"
    cache_level: "bypass"
    
  # Rule 3: Don't cache /dashboard/*
  - url: "example.com/dashboard/*"
    cache_level: "bypass"
    
# Which rule applies to example.com/api/user/123 ?
# Unclear! May depend on rule order.
```

### Giải pháp

```yaml
# ✅ SOLUTION: Specific rules first
page_rules:
  # Most specific first
  - url: "example.com/api/*"
    priority: 1
    cache_level: "bypass"
    
  - url: "example.com/dashboard/*"
    priority: 1
    cache_level: "bypass"
    
  - url: "example.com/*.json"
    priority: 2
    cache_level: "cache_everything"
    edge_cache_ttl: 3600
    
  # Least specific last
  - url: "example.com/*"
    priority: 10
    cache_level: "cache_everything"
    edge_cache_ttl: 7200
```

## Anti-Pattern 11: Not Using Workers for Authentication

### Mô tả

Implement authentication logic entirely at origin thay vì edge, causing unnecessary latency.

### Ví dụ xấu

```javascript
// ❌ ANTI-PATTERN: All auth at origin
// Origin handles everything:
// 1. User → Cloudflare (10ms)
// 2. Cloudflare → Origin (50ms)
// 3. Origin validates token (20ms)
// 4. Origin generates response (10ms)
// 5. Response back to user (50ms)

// Total: ~130ms, with origin doing all work
```

### Giải pháp

```javascript
// ✅ SOLUTION: Edge authentication
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Protected routes
    if (url.pathname.startsWith('/dashboard')) {
      const token = request.headers.get('Authorization')?.replace('Bearer ', '');
      
      if (!token) {
        return Response.redirect('/login', 302);
      }
      
      try {
        // Fast JWT verification at edge
        const payload = await verifyJWT(token, env.JWT_SECRET);
        
        // Add user context
        request.headers.set('X-User-ID', payload.sub);
        request.headers.set('X-User-Role', payload.role);
        
      } catch (err) {
        return new Response('Unauthorized', { status: 401 });
      }
    }
    
    // Origin only receives authenticated requests
    return fetch(request);
  }
};

// Total: ~60ms, origin does less work
```

## Anti-Pattern 12: Ignoring Cloudflare Analytics

### Mô tả

Không monitoring Cloudflare analytics, miss valuable insights về traffic patterns và potential threats.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No logging or monitoring
# Never check:
# - Traffic patterns
# - Security events
# - Cache hit ratios
# - Origin response times
# - Bot traffic

# Blind to issues until users complain!
```

### Giải phól

```yaml
# ✅ SOLUTION: Enable comprehensive logging
logpush:
  enabled: true
  destination:
    type: "s3"
    bucket: "cf-logs-bucket"
    
  # Comprehensive fields
  fields:
    - "ZoneID"
    - "RayID"
    - "ClientRequestURL"
    - "ClientRequestMethod"
    - "EdgeStartTimestamp"
    - "CacheResponseStatus"
    - "OriginResponseStatus"
    - "ClientCountry"
    - "ClientIP"
    - "cf.bot.score"
    - "cf.threat.score"
```

```yaml
# Also configure alerts
alerts:
  - name: "High traffic spike"
    condition: "requests > 10000"
    threshold: 1
    
  - name: "Security spike"
    condition: "cf.threat_score > 50"
    threshold: 10
    
  - name: "Origin errors"
    condition: "origin_response_status >= 500"
    threshold: 5
```

## Related Documents

- [Cloudflare Glossary](../glossary.md)
- [Cloudflare Architecture](../architecture.md)
- [Cloudflare Best Practices](../best-practice.md)
- [Cloudflare Checklist](../checklist.md)
- [Cloudflare FAQ](../faq.md)
- [Cloudflare Decision Tree](../decision-tree.md)
