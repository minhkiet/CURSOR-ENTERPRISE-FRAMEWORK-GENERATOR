---
name: pinterest-scraper
description: 'Tìm kiếm, duyệt và trích xuất ảnh chất lượng cao từ Pinterest (https://www.pinterest.com/) qua MCP server và Python API. Keywords: pinterest, pinterest scraper, pinterest mcp, tìm ảnh pinterest, lấy ảnh pinterest, crawl pinterest, pin image.'
---

# Pinterest Scraper & Image Browser Skill

Kỹ năng tìm kiếm, duyệt bảng, trích xuất và tải ảnh chất lượng gốc (`orig`, `736x`, `474x`, `236x`) từ **Pinterest** (https://www.pinterest.com/) không cần tài khoản hay API key.

Được hỗ trợ bởi **Pinterest MCP Server** (`mcp/pinterest_server.py`) và tích hợp trực tiếp vào **ImageSearchSkill**.

---

## 1. Khi nào sử dụng

- Cần tìm kiếm ảnh ý tưởng thiết kế, moodboard, UI/UX, kiến trúc, thời trang từ Pinterest.
- Cần lấy ảnh chất lượng cao gốc từ một đường link Pin cụ thể (`pinterest.com/pin/...` hoặc link rút gọn `pin.it/...`).
- Cần duyệt toàn bộ ảnh từ một Board hoặc Profile người dùng Pinterest.
- Tự động tải ảnh về thư mục dự án với cơ chế kiểm tra an toàn (chống SSRF và path-traversal).

---

## 2. MCP Tools được cung cấp

| Tool | Mô tả | Tham số chính |
|------|-------|---------------|
| `search_pins` | Tìm kiếm Pins theo từ khóa | `query` (str), `limit` (int, mặc định 25), `resolution` ('orig', '736x', '474x', '236x') |
| `get_board_pins` | Lấy Pins từ một Board công khai | `username` (str), `board` (str), `limit` (int), `resolution` (str) |
| `get_user_pins` | Lấy Pins mới nhất của một User | `username` (str), `limit` (int), `resolution` (str) |
| `get_pin_details` | Chi tiết Pin & ảnh gốc chất lượng cao | `pin_id_or_url` (str - Pin ID, URL đầy đủ hoặc short link `pin.it`) |
| `extract_from_url` | Bộ định tuyến thông minh từ URL bất kỳ | `url` (str), `limit` (int) |
| `download_images` | Tải an toàn danh sách ảnh về máy | `image_urls` (list), `output_folder` (str), `filename_prefix` (str) |

---

## 3. Cách sử dụng qua MCP JSON-RPC / Antigravity / Cursor

Khi MCP Server `pinterest` được kích hoạt (cấu hình trong `mcp/mcp_config.json`):

### Tìm kiếm Pins theo từ khóa
```json
{
  "name": "search_pins",
  "arguments": {
    "query": "minimalist portfolio website design",
    "limit": 10,
    "resolution": "orig"
  }
}
```

### Trích xuất từ một liên kết Pin hoặc pin.it
```json
{
  "name": "extract_from_url",
  "arguments": {
    "url": "https://www.pinterest.com/pin/424605071146368277/"
  }
}
```

### Tải ảnh về thư mục cục bộ
```json
{
  "name": "download_images",
  "arguments": {
    "image_urls": [
      "https://i.pinimg.com/originals/89/60/1a/89601a78a992d2618ba24e7f99417b92.jpg"
    ],
    "output_folder": "assets/images/hero",
    "filename_prefix": "hero_bg"
  }
}
```

---

## 4. Cách sử dụng qua Python API

### Sử dụng PinterestClient trực tiếp
```python
from mcp.pinterest_server import PinterestClient

client = PinterestClient()

# 1. Tìm kiếm ảnh
pins = client.search_pins("modern architecture house", limit=10)
for pin in pins:
    print(pin["title"], pin["orig_image_url"])

# 2. Lấy chi tiết Pin từ ID hoặc URL
pin_info = client.get_pin_details("424605071146368277")
print("High-res:", pin_info["orig_image_url"])

# 3. Lấy ảnh từ Board
board_pins = client.get_board_pins(username="canva", board="design-trends", limit=15)

# 4. Tải ảnh an toàn
download_result = client.download_image(
    image_url=pins[0]["orig_image_url"],
    output_path="assets/pinterest/sample.jpg"
)
print(download_result["path"], download_result["size_bytes"])
```

### Sử dụng qua ImageSearchSkill (Tích hợp Multi-Provider)
```python
import asyncio
from cursor_framework.skills.image_search import ImageSearchSkill

async def main():
    skill = ImageSearchSkill()
    # Tự động dùng PinterestProvider mà không cần cấu hình API key
    result = await skill.search("minimalist logo", limit=10)
    for img in result.images:
        print(f"[{img.provider}] {img.url}")

asyncio.run(main())
```

---

## 5. Dòng lệnh CLI

```bash
# Kiểm tra tìm kiếm trực tiếp
python mcp/pinterest_server.py --test-search "modern interior"

# Kiểm tra lấy thông tin Pin trực tiếp
python mcp/pinterest_server.py --test-pin 424605071146368277

# Khởi chạy MCP Server chế độ stdio
python mcp/pinterest_server.py
```

---

## 6. Tiêu chuẩn an toàn & Bảo mật

1. **SSRF Guard**: Chỉ cho phép tải từ các tên miền CDN tin cậy của Pinterest (`i.pinimg.com`, `s-media-cache-ak0.pinimg.com`, `*.pinimg.com`).
2. **Path Traversal Protection**: Kiểm tra đường dẫn đích tuyệt đối để ngăn chặn các tệp tin lưu ngoài thư mục `output_folder`.
3. **Decompression Bomb / Size Limit Guard**: Giới hạn kích thước tải xuống tối đa 25MB cho mỗi ảnh.
4. **Zero Third-Party Dependency**: Toàn bộ hệ thống MCP client hoạt động dựa trên thư viện chuẩn của Python (`urllib`, `http.cookiejar`, `json`, `re`), không phát sinh xung đột gói hoặc lỗi phiên bản.
