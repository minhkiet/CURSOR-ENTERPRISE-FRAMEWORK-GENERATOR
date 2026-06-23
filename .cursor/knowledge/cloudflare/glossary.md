# Cloudflare Knowledge Base - Glossary

## Tổng quan

Document này cung cấp danh sách các thuật ngữ chuyên ngành liên quan đến Cloudflare trong Cursor Enterprise Framework. Các thuật ngữ được phân loại theo từng nhóm để dễ tra cứu.

## Nhóm 1: Core Cloudflare Concepts

### 1. Cloudflare

Nền tảng cloud computing cung cấp CDN (Content Delivery Network), bảo mật web, DNS, và các dịch vụ infrastructure. Cloudflare hoạt động như một reverse proxy giữa users và origin servers.

```bash
# Basic Cloudflare configuration
# Point your domain to Cloudflare nameservers
# ns1.cloudflare.com
# ns2.cloudflare.com
```

Cloudflare cung cấp các dịch vụ chính: Website optimization, Security (DDoS protection, WAF), Performance (CDN, caching), DNS management, và Developer platform (Workers, Pages, R2).

### 2. CDN (Content Delivery Network)

Mạng lưới các servers phân phối nội dung đến users dựa trên vị trí địa lý, giảm latency và tăng tốc độ tải trang.

```yaml
# Cloudflare Page Rules for caching
rules:
  - description: "Cache static assets"
    path: "*.assets.example.com/*"
    actions:
      - cache_level: "cache_everything"
      - edge_cache_ttl: 604800  # 7 days
```

Cloudflare có hơn 300 data centers trên toàn cầu, cho phép serve content từ edge locations gần users nhất.

### 3. DNS (Domain Name System)

Hệ thống phân giải tên miền của Cloudflare với hiệu suất cao và bảo mật. Cloudflare DNS sử dụng anycast để ensure low latency.

```bash
# Cloudflare DNS record types
# A record - IPv4 address
# AAAA record - IPv6 address
# CNAME - Alias to another domain
# MX - Mail exchange
# TXT - Text records for verification
# NS - Nameserver records
```

Cloudflare cung cấp DNS với 100% uptime SLA, automatic load balancing, và built-in DDoS protection.

### 4. Anycast

Phương pháp routing định tuyến traffic đến server gần nhất dựa trên vị trí địa lý. Cloudflare sử dụng Anycast cho tất cả các services của mình.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Anycast Routing                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    ┌─────────────────┐                          │
│                    │   User Request   │                          │
│                    └────────┬────────┘                          │
│                             │                                     │
│                             ▼                                     │
│              ┌───────────────────────────────────┐              │
│              │      Cloudflare Edge Network       │              │
│              │     (300+ locations worldwide)     │              │
│              └───────────────┬───────────────────┘              │
│                              │                                   │
│         ┌───────────────────┼───────────────────┐              │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│    ┌─────────┐        ┌─────────┐        ┌─────────┐          │
│    │ Frankfurt│        │   NYC   │        │  Tokyo  │          │
│    │  POP    │        │  POP    │        │  POP    │          │
│    └─────────┘        └─────────┘        └─────────┘          │
│                                                                     │
│    Request được định tuyến đến POP gần nhất                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Nhóm 2: Security Services

### 5. DDoS Protection

Bảo vệ chống lại các cuộc tấn công Distributed Denial of Service. Cloudflare's DDoS protection được tích hợp sẵn và hoạt động ở Layer 3, 4, và 7.

```yaml
# Cloudflare DDoS settings
security:
  ddos_protection:
    mode: "automatic"  # or "on", "off"
    sensitivity: "medium"  # "low", "medium", "high"
    
  rate_limiting:
    rules:
      - name: "API rate limit"
        path: "/api/*"
        requests_per_period: 100
        period: 60  # seconds
```

Cloudflare's DDoS protection có thể mitigate attacks lên đến 2 Tbps mà không ảnh hưởng đến legitimate traffic.

### 6. WAF (Web Application Firewall)

Tường lửa ứng dụng web giúp bảo vệ against common exploits như SQL injection, XSS, và other OWASP Top 10 threats.

```yaml
# Cloudflare WAF configuration
waf:
  # Managed rulesets
  rulesets:
    - owasp-modsecurity-crs:
        sensitivity: "medium"
        action: "block"
        
  # Custom rules
  custom_rules:
    - name: "Block suspicious requests"
      expression: "(cf.threat_score > 30)"
      action: "challenge"
```

WAF rules có thể được viết bằng Cloudflare's Rules language với expressions để match specific patterns.

### 7. SSL/TLS

Mã hóa kết nối giữa users và Cloudflare, và giữa Cloudflare và origin server. Cloudflare cung cấp free SSL certificates.

```yaml
# SSL/TLS encryption mode
ssl:
  mode: "full"  # Options: off, flexible, full, strict
  
  # Certificate transparency
  certificate_transparency:
    enabled: true
    
  # TLS versions
  min_tls_version: "1.2"
  tls_1_3: "on"
```

| Encryption Mode | Client ↔ Cloudflare | Cloudflare ↔ Origin |
|----------------|---------------------|----------------------|
| Off | No encryption | No encryption |
| Flexible | HTTPS optional | HTTP only |
| Full | Encrypted | HTTPS required |
| Strict | Encrypted | HTTPS + valid cert |

### 8. Bot Management

Hệ thống phát hiện và quản lý bots bao gồm machine learning để identify malicious bots và allow legitimate traffic.

```yaml
# Bot Management configuration
bot_management:
  # Bot scoring
  bot_signals:
    - bot_score_threshold: 30
      action: "challenge"
      
  # Known bot handling
  verified_bot:
    enable: true
    
  # Challenge settings
  challenge:
    passthrough: true
    score_threshold: 0
```

Bot scores range từ 1-100, với lower scores indicating higher likelihood of bot traffic.

## Nhóm 3: Performance Services

### 9. Cloudflare Workers

Serverless computing platform cho phép chạy JavaScript, Rust, C++, và Python code tại Cloudflare's edge locations.

```javascript
// Cloudflare Worker example
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith('/api/')) {
      // Process API requests
      const response = await fetch(request);
      return new Response(response.body, {
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=60'
        }
      });
    }
    
    // Serve static content
    return fetch(request);
  }
};
```

Workers có thể be deployed globally trong seconds với automatic scaling và 0ms cold starts.

### 10. Caching

Cloudflare's caching system lưu trữ static content tại edge để reduce latency và origin load.

```yaml
# Cache configuration
cache:
  # Cache levels
  level: "cache_everything"  # ignore_origin, basic, simplified, cache_everything
  
  # TTL settings
  browser_cache_ttl: 14400  # 4 hours
  edge_cache_ttl: 7200      # 2 hours
  
  # Purge settings
  purge:
    method: "individual"  # or "tag", "host"
    
  # Always cache
  rules:
    - description: "Cache static assets"
      path: "*.{css,js,png,jpg,svg}"
      cache: true
      edge_ttl: 604800  # 7 days
```

### 11. Argo Smart Routing

Dịch vụ tự động route traffic qua con đường nhanh nhất giữa Cloudflare và origin, tránh congestion và packet loss.

```yaml
# Argo configuration
argo:
  smart_routing:
    enabled: true
    
  # Tiered caching
  tiered_caching:
    enabled: true
```

Argo sử dụng real-time network intelligence để optimize routing và reduce latency lên đến 30%.

### 12. Load Balancing

Cloudflare's global load balancer phân phối traffic across multiple origin servers với health checks và failover.

```yaml
# Load Balancer configuration
load_balancer:
  name: "production-lb"
  steering_policy: "performance"  # or "geo", "random", "weighted"
  
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
        interval: 30
        timeout: 10
        healthy_threshold: 3
        unhealthy_threshold: 3
  
  # Failover configuration
  fallback_pool: "backup-pool"
  description: "Production load balancer"
```

## Nhóm 4: Developer Platform

### 13. Cloudflare Pages

Static website hosting platform với JAMstack support, continuous deployment, và global edge network.

```yaml
# Cloudflare Pages configuration
pages:
  build:
    command: "npm run build"
    output_directory: "public"
    
  # Environment variables
  env_vars:
    NODE_ENV: "production"
    
  # Wrangler configuration
  wrangler:
    kv_namespaces:
      - binding: "CACHE"
        id: "xxxxxxxxxxxxxxxx"
```

Pages hỗ trợ deploy từ Git repositories (GitHub, GitLab) với automatic preview deployments.

### 14. Cloudflare R2

Object storage tương thích với S3 API cho lưu trữ unstructured data như images, videos, và documents.

```yaml
# R2 configuration
r2:
  bucket: "my-bucket"
  
  # Access
  permissions:
    - s3:GetObject
    - s3:PutObject
    
  # CORS
  cors:
    - allowedOrigins:
        - "https://example.com"
      allowedMethods:
        - GET
        - PUT
```

R2 cung cấp egress-free storage, nghĩa là không có charges cho data transfer ra khỏi R2.

### 15. Cloudflare Images

Dịch vụ quản lý images với transformation, resizing, và delivery optimization.

```yaml
# Cloudflare Images
images:
  variants:
    - name: "thumbnail"
      width: 100
      height: 100
      fit: "cover"
    - name: "preview"
      width: 800
      fit: "contain"
```

Images có thể be uploaded qua API và delivered qua Cloudflare's global network với automatic optimization.

### 16. Durable Objects

Stateful serverless objects cho real-time collaboration và consistent state management.

```javascript
// Durable Object example
export class GameRoom {
  constructor(state, env) {
    this.state = state;
  }
  
  async handleWebSocket(message) {
    const players = await this.state.storage.get('players') || [];
    players.push(message.player);
    await this.state.storage.put('players', players);
    
    // Broadcast to all connected clients
    this.webSocketBroadcast(message);
  }
}
```

Durable Objects cung cấp strong consistency và can be used cho games, collaborative apps, và real-time features.

## Nhóm 5: DNS Records

### 17. A Record

DNS record trỏ một hostname đến IPv4 address.

```yaml
dns:
  records:
    - name: "@"
      type: "A"
      content: "192.0.2.1"
      proxied: true  # Cloudflare proxy enabled
```

### 18. AAAA Record

DNS record trỏ một hostname đến IPv6 address.

```yaml
dns:
  records:
    - name: "@"
      type: "AAAA"
      content: "2001:db8::1"
      proxied: true
```

### 19. CNAME Record

DNS record tạo alias từ một domain đến another domain.

```yaml
dns:
  records:
    - name: "www"
      type: "CNAME"
      content: "example.com"
      proxied: true
```

### 20. MX Record

DNS record xác định mail servers cho một domain.

```yaml
dns:
  records:
    - name: "@"
      type: "MX"
      content: "mail.example.com"
      priority: 10
      proxied: false  # Mail should not be proxied
```

## Nhóm 6: Traffic Management

### 21. Traffic Steering

Cơ chế định tuyến traffic dựa trên various criteria như geography, latency, hoặc weights.

```yaml
# Traffic steering options
load_balancer:
  steering_policy:
    # Performance-based
    performance:
      description: "Route to fastest pool"
      
    # Geo-based
    geo:
      description: "Route based on user's location"
      regions:
        - name: "APAC"
          pools: ["apac-pool"]
        - name: "EU"
          pools: ["eu-pool"]
          
    # Weighted
    weighted:
      description: "Route based on pool weights"
      pools:
        - pool: "primary-pool"
          weight: 3
        - pool: "secondary-pool"
          weight: 1
```

### 22. Health Checks

Monitoring origins để đảm bảo traffic chỉ được gửi đến healthy servers.

```yaml
load_balancer:
  pools:
    - name: "api-pool"
      health_check:
        path: "/health"
        port: 443
        protocol: "HTTPS"
        interval: 30
        timeout: 10
        retries: 3
        response_body: "OK"
        expected_codes: "200-299"
```

Health checks có thể be configured với specific paths, ports, và expected responses.

## Nhóm 7: Analytics và Monitoring

### 23. Cloudflare Analytics

Dashboard cung cấp insights về traffic, security events, và performance metrics.

```yaml
# Analytics configuration
analytics:
  # Real-time logs
  logpush:
    enabled: true
    destination: "s3://my-bucket/logs"
    dataset: "http_requests"
    
  # Log filters
  filters:
    - zone: "example.com"
      since: "2024-01-01"
```

Analytics data có thể be exported đến external destinations như S3, BigQuery, hoặc Datadog.

### 24. Logpush

Dịch vụ push Cloudflare logs đến external destinations cho long-term storage và analysis.

```yaml
logpush:
  name: "access-logs"
  destination: "s3://my-bucket/cloudflare-logs"
  
  # Fields to include
  fields:
    - RayID
    - EdgeStartTimestamp
    - ClientRequestURL
    - ClientRequestMethod
    - OriginResponseStatus
    - CacheResponseStatus
    
  # Filters
  filter: "(not cf.colo.id eq 1234)"
```

Logpush cung cấp granular control over which fields và records được exported.

## Related Documents

- [Cloudflare Architecture](../architecture.md)
- [Cloudflare Best Practices](../best-practice.md)
- [Cloudflare Anti-Patterns](../anti-pattern.md)
- [Cloudflare Checklist](../checklist.md)
- [Cloudflare FAQ](../faq.md)
- [Cloudflare Decision Tree](../decision-tree.md)
