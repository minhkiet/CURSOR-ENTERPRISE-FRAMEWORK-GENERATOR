# Cloudflare Knowledge Base - Best Practices

## Tổng quan

Document này cung cấp 10+ best practices cho việc sử dụng Cloudflare trong Cursor Enterprise Framework, kèm theo code examples cụ thể cho từng practice.

## Practice 1: Enable Full SSL/TLS Encryption

### Mô tả

Luôn sử dụng "Full" hoặc "Strict" SSL mode để đảm bảo end-to-end encryption giữa users, Cloudflare, và origin server.

```yaml
# Cloudflare SSL/TLS configuration
ssl:
  mode: "strict"  # Preferred over "full"
  
  # TLS settings
  tls_1_2_only: false
  tls_1_3: "on"
  
  # Certificate transparency
  certificate_transparency: true
  
  # TLS minimum version
  min_tls_version: "1.2"
```

```bash
# Verify SSL configuration
curl -I https://example.com
# Should show:
# strict-transport-security: max-age=63072000
# x-content-type-options: nosniff
```

### Tại sao quan trọng

- **Data protection**: Mã hóa tất cả traffic
- **SEO benefits**: Google ưu tiên HTTPS sites
- **Browser warnings**: Users sẽ thấy warnings nếu không có SSL
- **Compliance**: Nhiều standards yêu cầu encryption

## Practice 2: Configure Aggressive Caching for Static Assets

### Mô tả

Cấu hình cache cho static assets với long TTLs để giảm origin load và improve performance.

```yaml
# Page Rules for static asset caching
cache:
  rules:
    - description: "Cache all static assets"
      path: "*.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)"
      actions:
        cache_level: "cache_everything"
        edge_cache_ttl: 604800  # 7 days
        browser_cache_ttl: 86400  # 1 day
        
    - description: "Cache HTML pages"
      path: "*.html"
      actions:
        cache_level: "cache_everything"
        edge_cache_ttl: 3600  # 1 hour
        origin_cache_control: true
        
    - description: "Don't cache API responses"
      path: "/api/*"
      actions:
        cache_level: "bypass"
```

```javascript
// Worker to set optimal cache headers
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const response = await fetch(request);
    
    // Clone response to modify headers
    const newResponse = new Response(response.body, response);
    
    // Set cache headers based on content type
    if (response.headers.get('Content-Type')?.includes('text/html')) {
      newResponse.headers.set('Cache-Control', 'public, max-age=300, stale-while-revalidate=600');
    } else if (response.headers.get('Content-Type')?.includes('image')) {
      newResponse.headers.set('Cache-Control', 'public, max-age=86400, immutable');
    }
    
    return newResponse;
  }
};
```

## Practice 3: Use Cloudflare Workers for Edge Computing

### Mô tả

Di chuyển logic xử lý ra edge để giảm latency và improve user experience.

```javascript
// Worker for authentication at edge
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Check for API requests
    if (url.pathname.startsWith('/api/')) {
      // Verify JWT at edge
      const token = request.headers.get('Authorization')?.replace('Bearer ', '');
      
      if (!token) {
        return new Response('Unauthorized', { status: 401 });
      }
      
      try {
        const payload = await verifyJWT(token, env.JWT_SECRET);
        request.headers.set('X-User-ID', payload.sub);
      } catch (err) {
        return new Response('Invalid token', { status: 401 });
      }
    }
    
    return fetch(request);
  }
};

// A/B testing at edge
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/' && !url.searchParams.has('variant')) {
      // Assign variant
      const variant = Math.random() < 0.5 ? 'A' : 'B';
      url.searchParams.set('variant', variant);
      
      // Redirect with variant
      return Response.redirect(url.toString(), 302);
    }
    
    // Modify response based on variant
    const response = await fetch(request);
    const variant = url.searchParams.get('variant');
    
    // Modify HTML based on variant
    if (response.headers.get('Content-Type')?.includes('text/html')) {
      const html = await response.text();
      const modifiedHtml = html.replace(
        '<title>',
        `<title>[Variant ${variant}] `
      );
      
      return new Response(modifiedHtml, response);
    }
    
    return response;
  }
};
```

## Practice 4: Implement Rate Limiting

### Mô tả

Configure rate limiting để protect against abuse và ensure fair resource allocation.

```yaml
# Rate limiting configuration
rate_limiting:
  rules:
    - name: "Global rate limit"
      description: "Limit requests per IP"
      expression: "true"
      characteristics:
        - "cf.colo.id"
        - "ip.src"
      mitigation:
        requests_per_period: 1000
        period: 60
        action: "simulate"
        
    - name: "API rate limit"
      description: "Strict limit for API endpoints"
      expression: '(http.request.uri.path contains "/api/")'
      characteristics:
        - "ip.src"
      mitigation:
        requests_per_period: 100
        period: 60
        action: "block"
        
    - name: "Login rate limit"
      description: "Protect login endpoint"
      expression: '(http.request.uri.path contains "/login")'
      characteristics:
        - "ip.src"
      mitigation:
        requests_per_period: 5
        period: 300  # 5 attempts per 5 minutes
        action: "block"
```

## Practice 5: Use Bot Management

### Mô tả

Enable Cloudflare Bot Management để phát hiện và block malicious bots.

```yaml
# Bot Management configuration
bot_management:
  # Enable bot detection
  enabled: true
  
  # Verified bots
  verified_bot:
    enable: true
    allow_google_cloud: true
    
  # Challenge settings
  challenge:
    prefer_challenge: "interactive"
    score_threshold: 30  # Challenge if bot score < 30
    
  # IAB / CBAF
  use_ibi_client_scores: true
  use_ibeu_client_scores: true
```

```javascript
// Worker to check bot score and take action
export default {
  async fetch(request, env) {
    const cf = request.cf;
    const botScore = cf.botScore;
    const isVerifiedBot = cf.verifiedBot;
    
    // Allow verified bots
    if (isVerifiedBot) {
      return fetch(request);
    }
    
    // Challenge suspicious traffic
    if (botScore < 30) {
      return new Response('Access denied', { 
        status: 403,
        headers: {
          'CF-Bot-Score': botScore.toString()
        }
      });
    }
    
    // Continue with request
    return fetch(request);
  }
};
```

## Practice 6: Configure Proper Cache Keys

### Mô tả

Sử dụng custom cache keys để optimize caching behavior và avoid cache misses.

```yaml
# Custom cache key configuration
cache:
  cache_key:
    include:
      - protocol
      - host
      - uri
      
    # Include specific query parameters
    forward_parameters:
      - "page"
      - "sort"
      - "filter"
      
    # Ignore specific parameters
    ignore_query_strings:
      - "utm_source"
      - "utm_medium"
      - "utm_campaign"
      - "fbclid"
```

```javascript
// Worker to normalize cache key
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Remove tracking parameters for better caching
    const trackingParams = ['utm_source', 'utm_medium', 'utm_campaign', 'fbclid'];
    trackingParams.forEach(param => url.searchParams.delete(param));
    
    // Create normalized request
    const normalizedRequest = new Request(url.toString(), request);
    
    // Fetch with normalized URL
    return fetch(normalizedRequest);
  }
};
```

## Practice 7: Set Up Proper CORS Headers

### Mô tả

Configure CORS headers properly để allow legitimate cross-origin requests.

```yaml
# CORS configuration via Page Rules
cors:
  # Allow specific origins
  allowed_origins:
    - "https://app.example.com"
    - "https://admin.example.com"
    
  # Allow credentials
  allow_credentials: true
  
  # Preflight cache time
  max_age: 86400
```

```javascript
// Worker for CORS handling
export default {
  async fetch(request, env) {
    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': 'https://app.example.com',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400'
        }
      });
    }
    
    // Process request
    const response = await fetch(request);
    
    // Add CORS headers to response
    const newResponse = new Response(response.body, response);
    newResponse.headers.set('Access-Control-Allow-Origin', 'https://app.example.com');
    
    return newResponse;
  }
};
```

## Practice 8: Use Origin Shield

### Mô tả

Enable Origin Shield để reduce origin load và improve cache hit ratios.

```yaml
# Origin Shield configuration
origin_shield:
  enabled: true
  
  # Shield location (closest to origin)
  shield: "iad1"  # US East, adjust based on origin location
```

```bash
# Verify Origin Shield is working
curl -I https://example.com
# Should show:
# cf-cache-status: HIT (from-IAD1)
```

Origin Shield ensures that only one Cloudflare PoP contacts the origin for a cached object, reducing origin load significantly.

## Practice 9: Configure Always Online

### Mô tả

Enable Always Online để serve cached content khi origin is unavailable.

```yaml
# Always Online configuration
always_online:
  enabled: true
  
  # Include additional pages
  include_only:
    - "*.html"
    - "*.css"
    - "*.js"
```

```yaml
# In Workers, handle origin errors
export default {
  async fetch(request, env) {
    try {
      const response = await fetch(request);
      
      // Cache successful responses
      if (response.ok) {
        const cache = caches.default;
        await cache.put(request, response.clone());
      }
      
      return response;
    } catch (error) {
      // Try to serve from cache
      const cache = caches.default;
      const cached = await cache.match(request);
      
      if (cached) {
        return new Response(cached.body, {
          ...cached,
          headers: {
            ...Object.fromEntries(cached.headers),
            'X-Served-From': 'cache',
            'X-Cache-Status': 'STALE'
          }
        });
      }
      
      return new Response('Service unavailable', { status: 503 });
    }
  }
};
```

## Practice 10: Set Up Real-time Logs

### Mô tả

Configure Logpush để stream logs đến external destinations cho analysis.

```yaml
# Logpush configuration
logpush:
  enabled: true
  
  destination:
    type: "s3"
    bucket: "my-cloudflare-logs"
    prefix: "logs/"
    
  # Fields to include
  fields:
    - "ZoneID"
    - "RayID"
    - "ClientRequestURL"
    - "ClientRequestMethod"
    - "EdgeStartTimestamp"
    - "CacheResponseStatus"
    - "OriginResponseStatus"
    - "ClientSSLClass"
    - "ClientCountry"
    
  # Filters
  filter: "(not cf.colo.id eq 1234)"
  
  # Dataset
  dataset: "http_requests"
```

```bash
# Create Logpush job via API
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/logpush/jobs" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "access-logs",
    "destination_conf": "s3://my-bucket/logs?region=us-east-1",
    "dataset": "http_requests",
    "enabled": true
  }'
```

## Practice 11: Configure Automatic HTTPS Rewrites

### Mô tả

Enable Automatic HTTPS Rewrites để fix mixed content issues.

```yaml
# Automatic HTTPS Rewrites
https_rewrites:
  enabled: true
  
# Or via Page Rules
page_rules:
  - url: "example.com/*"
    settings:
      automatic_https_rewrites: "on"
```

## Practice 12: Use Cloudflare Access for Zero Trust

### Mô tả

Implement Cloudflare Access để secure internal resources without VPN.

```yaml
# Cloudflare Access configuration
access:
  application:
    name: "Internal API"
    domain: "api.internal.example.com"
    
    # Identity providers
    idp_integration:
      - google_workspace
      - github
      
    # Policy
    policies:
      - name: "Engineering team"
        include:
          - email_domain: "example.com"
        require:
          - group: "engineering"
        action: "allow"
        
      - name: " contractors"
        include:
          - email_domain: "contractor.com"
        action: "block"
```

```bash
# Deploy Access application via API
curl -X POST "https://api.cloudflare.com/client/v4/access/applications" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Internal Dashboard",
    "domain": "dashboard.internal.example.com",
    "type": "daemon"
  }'
```

## Practice 13: Monitor Core Web Vitals

### Mô tả

Track Core Web Vitals metrics để ensure optimal user experience.

```yaml
# Analytics Engine for Web Vitals
analytics:
  metrics:
    - name: "lcp"  # Largest Contentful Paint
      type: "web_vital"
    - name: "fid"  # First Input Delay
      type: "web_vital"
    - name: "cls"  # Cumulative Layout Shift
      type: "web_vital"
```

```javascript
// Worker to collect Core Web Vitals
export default {
  async fetch(request, env) {
    const response = await fetch(request);
    
    // Inject performance observer script
    if (response.headers.get('Content-Type')?.includes('text/html')) {
      const html = await response.text();
      
      const observerScript = `
        <script>
          if ('PerformanceObserver' in window) {
            // Collect LCP
            new PerformanceObserver((list) => {
              const entries = list.getEntries();
              const lastEntry = entries[entries.length - 1];
              fetch('/__metrics', {
                method: 'POST',
                body: JSON.stringify({
                  metric: 'LCP',
                  value: lastEntry.startTime
                })
              });
            }).observe({ entryTypes: ['largest-contentful-paint'] });
          }
        </script>
      `;
      
      const modifiedHtml = html.replace('</body>', `${observerScript}</body>`);
      return new Response(modifiedHtml, response);
    }
    
    return response;
  }
};
```

## Related Documents

- [Cloudflare Glossary](../glossary.md)
- [Cloudflare Architecture](../architecture.md)
- [Cloudflare Anti-Patterns](../anti-pattern.md)
- [Cloudflare Checklist](../checklist.md)
- [Cloudflare FAQ](../faq.md)
- [Cloudflare Decision Tree](../decision-tree.md)
