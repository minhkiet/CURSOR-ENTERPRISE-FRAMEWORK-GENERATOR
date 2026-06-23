# Cloudflare Knowledge Base - Decision Tree

## Tổng quan

Document này cung cấp cây quyết định chi tiết để hướng dẫn việc lựa chọn các Cloudflare services và configurations phù hợp trong Cursor Enterprise Framework.

## 1. SSL/TLS Mode Selection Tree

```
Bạn cần configure SSL như thế nào?
│
├── Production environment?
│   ├── Có → "Strict" mode
│   │   └── Yêu cầu valid certificate trên origin
│   │
│   └── Không (Development)?
│       ├── Cần HTTPS cho users? → "Full" mode
│       │   └── Origin có certificate nhưng không valid
│       │
│       └── Testing only → "Flexible" (TẠM THỜI)
│           └── ⚠️ Cảnh báo: Không encrypt giữa CF và origin
│
└── Origin có valid SSL certificate không?
    ├── Có → "Strict" mode (Recommended)
    └── Không → "Full" mode +尽快 get valid certificate

QUYẾT ĐỊNH CUỐI CÙNG:
┌─────────────────────────────────────────────────────────────┐
│ Production + Valid cert    → Strict                        │
│ Production + Self-signed   → Full (upgrade cert!)         │
│ Development/Testing        → Full hoặc Flexible          │
└─────────────────────────────────────────────────────────────┘
```

## 2. Caching Strategy Selection Tree

```
Bạn cần configure caching như thế nào?
│
├── Content type?
│   │
│   ├── Static assets (CSS, JS, images)?
│   │   ├── Cache everything
│   │   ├── Edge TTL: 7+ days
│   │   └── Browser TTL: 1-7 days
│   │
│   ├── HTML pages?
│   │   ├── Cache with origin headers
│   │   ├── Edge TTL: 1-24 hours
│   │   └── Depends on update frequency
│   │
│   ├── API responses?
│   │   ├── Public/Shared data → Cache with short TTL
│   │   │   └── Edge TTL: 30-300 seconds
│   │   │
│   │   └── Personalized data → Bypass cache
│   │       └── cache_level: "bypass"
│   │
│   └── Authenticated content?
│       └── Bypass cache
│           └── cache_level: "bypass"
│
└── Cache level nào?
    ├── "Cache everything" → All content cached
    ├── "Basic" → Only static assets
    ├── "Simplified" → Aggressive caching
    └── "Bypass" → No caching
```

## 3. Load Balancer Type Selection Tree

```
Bạn cần loại Load Balancer nào?
│
├── Traffic type?
│   │
│   ├── HTTP/HTTPS traffic?
│   │   ├── Full control → Cloudflare Load Balancer
│   │   │   ├── Multiple pools
│   │   │   ├── Health checks
│   │   │   └── Geo-routing
│   │   │
│   │   └── Simple round-robin → DNS-only LB
│   │       └── A records with multiple IPs
│   │
│   └── TCP/UDP traffic?
│       └── Cloudflare Load Balancer
│           └── L4 load balancing
│
└── Steering policy?
    ├── "Performance" → Route to fastest pool
    ├── "Geo" → Route based on geography
    ├── "Weighted" → Route based on weights
    └── "Random" → Random distribution
```

## 4. Worker Type Selection Tree

```
Bạn cần Worker type nào?
│
├── Cần maintain state không?
│   ├── Không (Stateless) → Regular Worker
│   │   ├── Request/Response transformation
│   │   ├── Authentication/Authorization
│   │   ├── A/B testing
│   │   └── Caching logic
│   │
│   └── Có (Stateful) → Durable Objects
│       ├── Real-time collaboration
│       ├── WebSocket handling
│       ├── Game state
│       └── Distributed locking
│
└── Execution trigger?
    ├── HTTP request → fetch event
    ├── Cron schedule → scheduled event
    └── Queue message → queue event
```

## 5. Security Feature Selection Tree

```
Bạn cần security features nào?
│
├── DDoS protection?
│   ├── Có → Cloudflare DDoS protection
│   │   ├── Automatic (recommended)
│   │   └── Always on cho high-risk sites
│   └── Không → Not recommended!
│
├── Web Application Firewall (WAF)?
│   ├── Có → Enable WAF
│   │   ├── Cloudflare Managed Rules
│   │   ├── OWASP Ruleset
│   │   └── Custom rules
│   └── Không → Not recommended for production!
│
├── Bot Management?
│   ├── Có → Enable Bot Management
│   │   ├── ML-based detection
│   │   ├── Verified bots handling
│   │   └── Challenge bad bots
│   │
│   └── Basic protection only → Free Bot Management
│
└── Additional security?
    ├── Firewall Rules → Custom IP/country blocking
    ├── Zone Lockdown → Restrict access by IP range
    └── Access → Zero Trust access control
```

## 6. Image Optimization Selection Tree

```
Bạn cần image optimization nào?
│
├── Host images trên Cloudflare?
│   ├── Có → Cloudflare Images
│   │   ├── Automatic resizing
│   │   ├── Format conversion (WebP, AVIF)
│   │   ├── Quality optimization
│   │   └── Variant generation
│   │
│   └── Không → Image Resizing on-demand
│       ├── Worker transforms images
│       ├── Cache transformed versions
│       └── Supports remote URLs
│
└── Polish service?
    ├── Lossy → Smaller files, lower quality
    ├── Lossless → Smaller files, same quality
    └── Off → No optimization
```

## 7. DNS Record Type Selection Tree

```
Bạn cần DNS record type nào?
│
├── Record type?
│   │
│   ├── IPv4 address? → A record
│   │
│   ├── IPv6 address? → AAAA record
│   │
│   ├── Another domain? → CNAME
│   │   └── Cloudflare: CNAME flatten or proxy
│   │
│   ├── Mail server? → MX record
│   │   └── Proxy: Off (DNS only)
│   │
│   ├── Verification/TXT? → TXT record
│   │
│   ├── Subdomain delegation? → NS record
│   │
│   └── Service location? → SRV record
│
└── Proxy hay DNS only?
    ├── Proxy (Orange cloud) → Performance + Security
    │   └── DDoS protection, caching, WAF
    │
    └── DNS only (Grey cloud) → Direct connection
        └── Required for:
            - MX records
            - Some third-party services
            - When origin IP needed
```

## 8. Storage Selection Tree

```
Bạn cần storage solution nào?
│
├── S3-compatible API?
│   ├── Có → Cloudflare R2
│   │   ├── S3-compatible
│   │   ├── No egress fees
│   │   └── Perfect for media storage
│   │
│   └── Không → Consider other options
│
├── Key-Value storage?
│   ├── Có → Cloudflare KV
│   │   ├── Global, low-latency reads
│   │   ├── High-latency writes
│   │   └── Good for config, caching
│   │
│   └── Không → Consider Durable Objects
│
├── Durable storage with strong consistency?
│   ├── Có → Durable Objects
│   │   ├── Single instance per key
│   │   ├── Strong consistency
│   │   └── Good for stateful workloads
│   │
│   └── Không → KV (eventual consistency OK)
│
└── Relational database?
    └── Use external service (Turso, PlanetScale, etc.)
```

## 9. Logpush Destination Selection Tree

```
Bạn cần log destination nào?
│
├── Cloud provider?
│   ├── AWS → S3 bucket
│   ├── GCP → Cloud Storage bucket
│   └── Azure → Blob Storage
│
├── SIEM/Logging platform?
│   ├── Datadog → Datadog Logpush
│   ├── Splunk → Splunk Cloud
│   ├── Elastic → Elastic Cloud
│   └── Sumo Logic → Sumo Logic
│
├── Custom destination?
│   ├── HTTPS endpoint → Custom HTTPS destination
│   └── Cloudflare Logs → Logpull API
│
└── Dataset nào?
    ├── HTTP requests → http_requests
    ├── Firewall events → firewall_events
    ├── Audit logs → audit_logs
    └── Workers logs → workers_trace_events
```

## 10. CDN vs Edge Computing Selection Tree

```
Bạn cần CDN hay Edge Computing?
│
├── Chỉ cần cache static content?
│   └── CDN (Automatic)
│       ├── Static assets cached globally
│       ├── No code needed
│       └── Configure via Page Rules
│
├── Cần modify/transform content?
│   └── Edge Computing (Workers)
│       ├── A/B testing
│       ├── Request/Response manipulation
│       ├── Authentication at edge
│       └── Custom caching logic
│
├── Cần persist state?
│   ├── Short-lived → KV
│   └── Long-lived/Consistent → Durable Objects
│
└── Cần real-time?
    └── Durable Objects
        ├── WebSocket handling
        ├── Real-time collaboration
        └── Gaming
```

## 11. Always Online vs Cache-Only Selection Tree

```
Bạn cần gì khi origin down?
│
├── Serve stale content?
│   ├── Có → Enable Always Online
│   │   └── Requires cached content
│   │       ├── Not cached → 502 error
│   │       └── Cached pages → Served
│   │
│   └── Custom error page → Cache Error behavior
│       └── Configure custom error page
│
└── No fallback?
    └── Origin Shield + Health checks
        └── Minimize origin failures
```

## 12. Quick Reference Decision Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION GUIDE                            │
├─────────────────────────────────┬──────────────────────────────────────┤
│ SITUATION                       │ DECISION                              │
├─────────────────────────────────┼──────────────────────────────────────┤
│ SSL mode (production)           │ Strict                                │
│ SSL mode (development)           │ Full                                  │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Static assets caching            │ Cache everything, 7+ days            │
│ HTML pages                      │ Origin headers, 1-24 hours           │
│ API responses                   │ Bypass or short cache                │
│ Authenticated content           │ Bypass                                │
├─────────────────────────────────┼──────────────────────────────────────┤
│ DDoS protection                  │ Automatic                             │
│ WAF                            │ Enable + Custom rules                 │
│ Bot management                  │ Enable for production                │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Stateless processing            │ Regular Workers                       │
│ Stateful workloads              │ Durable Objects                       │
│ Key-value storage              │ Cloudflare KV                         │
│ Object storage                  │ Cloudflare R2                         │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Global load balancing           │ Cloudflare Load Balancer             │
│ Health checks                   │ Yes, always                           │
│ Failover pools                  │ Yes, always                           │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Internal apps (no VPN)         │ Cloudflare Access                     │
│ Auth at edge                   │ Workers + JWT                         │
│ Rate limiting                  │ Both built-in and Worker-based        │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Image optimization              │ Cloudflare Images hoặc Polish        │
│ Image resizing                 │ Workers + Image Resizing              │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Log destination                 │ S3, BigQuery, hoặc SIEM              │
│ Performance monitoring          │ Cloudflare Analytics + Logpush       │
│ Cost control                    │ Cache optimization + alerts           │
└─────────────────────────────────┴──────────────────────────────────────┘
```

## Related Documents

- [Cloudflare Glossary](../glossary.md)
- [Cloudflare Architecture](../architecture.md)
- [Cloudflare Best Practices](../best-practice.md)
- [Cloudflare Anti-Patterns](../anti-pattern.md)
- [Cloudflare Checklist](../checklist.md)
- [Cloudflare FAQ](../faq.md)
