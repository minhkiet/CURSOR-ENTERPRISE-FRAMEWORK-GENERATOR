---
name: site-crawler
description: Site crawler cho phát hiện toàn bộ URLs, routes, links trong website. Dùng cho clone toàn bộ site. Keywords: crawl site, sitemap, discover URLs, find all pages, site scanner, link checker.
---

# Site Crawler Skill

Crawl toàn bộ website để phát hiện tất cả URLs, pages, và routes cho full-site clone.

## Khi nào dùng

- Clone toàn bộ website (không chỉ 1 page)
- Phát hiện tất cả pages/routes của một site
- Tạo sitemap cho site cần clone
- Kiểm tra broken links
- Discovery tất cả assets (images, CSS, JS)

## Công cụ Crawler

### 1. crawl4ai (Recommended - AI-friendly)

```bash
# Install
pip install crawl4ai

# Basic crawl - single URL
crawl4ai https://example.com

# Crawl with link discovery
crawl4ai https://example.com --extract-links --max-depth 3

# Full site crawl
crawl4ai https://example.com \
  --extract-links \
  --max-depth 10 \
  --max-pages 500 \
  --output-json site_crawl.json
```

### 2. playwright (Browser-based)

```bash
# Install
pip install playwright
playwright install chromium

# Crawl with Playwright
python << 'EOF'
from playwright.sync_api import sync_playwright
import json

def crawl_site(start_url, max_pages=100, max_depth=5):
    visited = set()
    queue = [(start_url, 0)]
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        while queue and len(visited) < max_pages:
            url, depth = queue.pop(0)
            if url in visited or depth > max_depth:
                continue
            
            try:
                page.goto(url, wait_until='networkidle')
                links = page.query_selector_all('a[href]')
                
                for link in links:
                    href = link.get_attribute('href')
                    if href and href.startswith('http'):
                        queue.append((href, depth + 1))
                
                results.append({
                    'url': url,
                    'title': page.title(),
                    'links': [l.get_attribute('href') for l in links]
                })
                visited.add(url)
            except:
                pass
        
        browser.close()
    return results

crawl = crawl_site('https://example.com')
print(json.dumps(crawl, indent=2))
EOF
```

### 3. httrack (Website Downloader)

```bash
# Install (Windows)
# Download from: https://www.httrack.com/

# Basic clone
httrack "https://example.com" -O "./clone-output" "+*.example.com/*" -r3

# Full site mirror
httrack "https://example.com" \
  --mirror \
  --robots=0 \
  --max-depth=10 \
  --urldepth=15 \
  -O "./site-mirror"
```

### 4. wget (CLI)

```bash
# Recursive download
wget --mirror --convert-links --adjust-extension \
  --page-requisites --no-parent \
  --no-host-directories \
  -e robots=off \
  -U "Mozilla/5.0" \
  https://example.com/

# With limits
wget -r -l 10 -np -R "*.pdf,*.zip" \
  --reject-regex ".*\\?(utm_|fb_|ref=)" \
  -e robots=off \
  https://example.com/
```

---

## Site Discovery Strategies

### 1. Sitemap Discovery (Fastest)

```bash
# Check sitemap.xml
curl -s https://example.com/sitemap.xml | grep -o '<loc>[^<]*</loc>'

# Or sitemap-index
curl -s https://example.com/sitemap-index.xml

# Tools
npx sitemap-cli https://example.com
```

### 2. robots.txt Discovery

```bash
# Check allowed paths
curl -s https://example.com/robots.txt

# Common paths to check
https://example.com/sitemap.xml
https://example.com/sitemap-index.xml
https://example.com/sitemap.xml.gz
https://example.com/robots.txt
```

### 3. Link Crawling (Comprehensive)

```bash
# Start from homepage, follow all internal links
# Use sitemap + link crawling combined
```

### 4. API Discovery (For SPAs)

```bash
# Check for API endpoints
curl -s https://api.example.com/swagger.json
curl -s https://example.com/api/docs

# GraphQL introspection
curl -X POST https://example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name}}}"}'
```

---

## Full Site Clone Workflow

### Phase 1: Discovery

```bash
# 1. Check sitemap
curl -s https://example.com/sitemap.xml > sitemap.xml

# 2. Parse all URLs
grep -oP '(?<=<loc>)[^<]+' sitemap.xml > urls.txt

# 3. Count URLs
wc -l urls.txt
```

### Phase 2: Crawl All Pages

```bash
# Using crawl4ai
crawl4ai https://example.com \
  --extract-links \
  --max-depth 10 \
  --max-pages 1000 \
  --output-json all_pages.json

# Extract URLs from result
cat all_pages.json | jq -r '.[].url' > all_urls.txt
```

### Phase 3: Categorize Pages

```bash
# Group by path pattern
cat all_urls.txt | grep -E '/blog/' > blog_urls.txt
cat all_urls.txt | grep -E '/product/' > product_urls.txt
cat all_urls.txt | grep -E '/pricing' > pricing_urls.txt
```

### Phase 4: Generate Clone Prompts

```bash
# For each URL, generate clone prompt
# See web-cloner skill
```

---

## Output Format

### URL List
```json
{
  "site": "https://example.com",
  "total_urls": 150,
  "urls": [
    {
      "url": "https://example.com/",
      "type": "homepage",
      "priority": "high"
    },
    {
      "url": "https://example.com/blog/",
      "type": "listing",
      "priority": "medium"
    },
    {
      "url": "https://example.com/blog/post-1",
      "type": "post",
      "priority": "high"
    }
  ]
}
```

### Site Map (Markdown)
```markdown
# Site Map: example.com

## Pages (150 total)

### High Priority
- [ ] Homepage (`/`)
- [ ] Pricing (`/pricing`)
- [ ] Features (`/features`)

### Medium Priority
- [ ] Blog Listing (`/blog`)
- [ ] About (`/about`)
- [ ] Contact (`/contact`)

### Low Priority
- [ ] Blog Post 1 (`/blog/post-1`)
- [ ] Blog Post 2 (`/blog/post-2`)
...
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Sitemap missing | Use link crawling |
| JavaScript-rendered | Use Playwright |
| Cloudflare protection | Use crawl4ai with bypass |
| Rate limiting | Add delays, use proxies |
| Large site (>10k pages) | Focus on priority pages |

## Tips

1. **Always check sitemap.xml first** - fastest way to get all URLs
2. **Use Playwright for SPAs** - JavaScript-rendered content
3. **Respect robots.txt** - unless explicitly told to ignore
4. **Categorize pages** - helps prioritize clone work
5. **Check for pagination** - `/blog?page=2`, `/blog/page/2/`
