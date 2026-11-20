---
name: pinterest-scraper
description: 'Tìm kiếm, duyệt và trích xuất ảnh & video chất lượng cao từ Pinterest (https://www.pinterest.com/) qua MCP server và Python API. Keywords: pinterest, pinterest scraper, pinterest mcp, tìm ảnh pinterest, lấy ảnh pinterest, lấy video pinterest, tải video pinterest, pinterest video downloader, crawl pinterest.'
---

# Pinterest Scraper & Media Browser Skill (Images & Videos)

Kỹ năng tìm kiếm, duyệt bảng, trích xuất và tải **ảnh & video** chất lượng gốc (`orig`, `736x`, direct MP4, HLS `.m3u8`) từ **Pinterest** (https://www.pinterest.com/) không cần tài khoản hay API key.

Được hỗ trợ bởi **Pinterest MCP Server** (`mcp/pinterest_server.py`) và tích hợp trực tiếp vào **ImageSearchSkill**.

---

## 1. Khi nào sử dụng

- Cần tìm kiếm ảnh hoặc **video chuyển động (motion graphics, UI animation, reels, shorts)** từ Pinterest.
- Cần lấy liên kết video MP4 gốc trực tiếp hoặc HLS stream từ một Pin video (`pinterest.com/pin/...` hoặc link rút gọn `pin.it/...`).
- Cần lấy ảnh chất lượng cao gốc từ một đường link Pin cụ thể (`orig`, `736x`).
- Cần duyệt toàn bộ ảnh/video từ một Board hoặc Profile người dùng Pinterest.
- Tự động tải ảnh & video về thư mục dự án với cơ chế kiểm tra an toàn (chống SSRF, whitelist CDN Pinterest, path-traversal và size guard).

---

## 2. MCP Tools được cung cấp

| Tool | Mô tả | Tham số chính |
|------|-------|---------------|
| `search_pins` | Tìm kiếm Pins ảnh/video theo từ khóa | `query` (str), `limit` (int, mặc định 25), `resolution` ('orig', '736x', '474x', '236x') |
| `search_videos` | **Tìm kiếm chuyên biệt các Pin video** | `query` (str), `limit` (int, mặc định 15) |
| `get_pin_video` | **Trích xuất thông tin & stream video của một Pin** | `pin_id_or_url` (str - Pin ID hoặc URL) |
| `download_video` | **Tải an toàn video MP4/stream về máy** | `video_url` (str), `output_folder` (str), `filename` (str) |
| `get_board_pins` | Lấy Pins từ một Board công khai | `username` (str), `board` (str), `limit` (int), `resolution` (str) |
| `get_user_pins` | Lấy Pins mới nhất của một User | `username` (str), `limit` (int), `resolution` (str) |
| `get_pin_details` | Chi tiết Pin (bao gồm cả ảnh gốc & metadata video nếu có) | `pin_id_or_url` (str - Pin ID, URL đầy đủ hoặc short link `pin.it`) |
| `extract_from_url` | Bộ định tuyến thông minh từ URL bất kỳ (Pin, Board, Search) | `url` (str), `limit` (int) |
| `download_images` | Tải an toàn danh sách ảnh về máy | `image_urls` (list), `output_folder` (str), `filename_prefix` (str) |

---

## 3. Cách sử dụng qua MCP JSON-RPC / Antigravity / Cursor

Khi MCP Server `pinterest` được kích hoạt (cấu hình trong `mcp/mcp_config.json`):

### Tìm kiếm video chuyên biệt
```json
{
  "name": "search_videos",
  "arguments": {
    "query": "motion graphic 3d animation",
    "limit": 5
  }
}
```

### Trích xuất video từ một Pin
```json
{
  "name": "get_pin_video",
  "arguments": {
    "pin_id_or_url": "https://www.pinterest.com/pin/1234567890/"
  }
}
```

### Tải video MP4 về thư mục dự án
```json
{
  "name": "download_video",
  "arguments": {
    "video_url": "https://v1.pinimg.com/videos/mc/expMp4/example_t1.mp4",
    "output_folder": "assets/videos",
    "filename": "hero_background.mp4"
  }
}
```

### Tìm kiếm Pins ảnh theo từ khóa
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

# 1. Tìm kiếm video
videos = client.search_videos("ui motion design", limit=5)
for vid in videos:
    v_data = vid["video"]
    print(f"Title: {vid['title']}")
    print(f"Duration: {v_data['duration_seconds']}s")
    print(f"Direct MP4 / Stream: {v_data['best_video_url']}")

# 2. Lấy thông tin video của một Pin
pin_details = client.get_pin_details("https://www.pinterest.com/pin/1234567890/")
if pin_details.get("video"):
    print("Video available:", pin_details["video"]["best_video_url"])

# 3. Tải video MP4 an toàn (tối đa 250MB, kiểm tra whitelist domain)
dl_info = client.download_video(
    video_url=videos[0]["video"]["best_video_url"],
    output_path="assets/videos/sample.mp4"
)
print("Saved to:", dl_info["path"], "Size:", dl_info["size_bytes"])

# 4. Tìm kiếm ảnh tĩnh gốc
pins = client.search_pins("modern architecture house", limit=10)
for pin in pins:
    print(pin["title"], pin["orig_image_url"])
```

---

## 5. Dòng lệnh CLI

```bash
# Kiểm tra tìm kiếm video trực tiếp
python mcp/pinterest_server.py --test-search-video "motion graphic animation"

# Kiểm tra tìm kiếm ảnh trực tiếp
python mcp/pinterest_server.py --test-search "modern interior"

# Kiểm tra lấy thông tin Pin trực tiếp
python mcp/pinterest_server.py --test-pin 424605071146368277

# Khởi chạy MCP Server chế độ stdio
python mcp/pinterest_server.py
```

---

## 6. Tiêu chuẩn an toàn & Bảo mật

1. **SSRF Guard**:
   - Ảnh: Chỉ cho phép tải từ CDN ảnh của Pinterest (`i.pinimg.com`, `s-media-cache-ak0.pinimg.com`, `*.pinimg.com`).
   - Video: Chỉ cho phép tải từ CDN video của Pinterest (`v.pinimg.com`, `v1.pinimg.com`, `v2.pinimg.com`, `v3.pinimg.com`, `*.pinimg.com`).
2. **Path Traversal Protection**: Kiểm tra đường dẫn đích tuyệt đối để ngăn chặn các tệp tin lưu ngoài thư mục `output_folder`.
3. **Size Limit Guard**:
   - Ảnh: Tối đa 25MB cho mỗi ảnh.
   - Video: Tối đa 250MB cho mỗi tệp video.
4. **Zero Third-Party Dependency**: Toàn bộ hệ thống MCP client hoạt động dựa trên thư viện chuẩn của Python (`urllib`, `http.cookiejar`, `json`, `re`), không phát sinh xung đột gói hoặc lỗi phiên bản.
