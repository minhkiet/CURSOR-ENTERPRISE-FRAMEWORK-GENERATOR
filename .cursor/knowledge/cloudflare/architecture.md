# Cloudflare Architecture - Kiến Trúc Cloudflare

## Tổng quan

Cloudflare là edge computing platform cung cấp CDN, serverless, và security services.

## Kiến trúc chi tiết

### 1. Edge Computing

- **Workers**: Serverless JavaScript
- **Pages**: Static site hosting
- **R2**: Object storage

### 2. Database

- **D1**: SQLite at edge
- **KV**: Key-value store
- **Durable Objects**: Stateful objects

## Kết luận

Cloudflare architecture enables global, low-latency applications.
