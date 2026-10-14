# Cursor Enterprise Framework Generator

> A universal framework for AI coding agents & Vibe Coding tools — built around **Memory First**, **Retrieval First**, **Token Optimization**, **Knowledge Reuse**, and **Anti-AI-Slop Aesthetics**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Latest Release](https://img.shields.io/badge/release-v1.3.0-blue)](https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/releases)
[![Vibe Code](https://img.shields.io/badge/Vibe_Code-Universal_Support-10b981)](vibe-code-framework/)
[![Templates](https://img.shields.io/badge/Templates-22_Production_Ready-f59e0b)](cursor_framework_web/public/templates/)
[![Themes](https://img.shields.io/badge/Themes-6_Aesthetics-6366f1)](#themes--uiux-system)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

---

## What is it?

**Cursor Enterprise Framework (CEF)** is a production-grade configuration and tooling suite that turns any AI coding agent — **Cursor**, **Windsurf**, **Claude Code**, **GitHub Copilot**, **Roo Code**, **Cline**, **Google Antigravity**, **Trae**, **Devin / OpenHands**, **Aider**, or **Bolt.new / v0** — into a context-aware, token-efficient, memory-backed senior full-stack engineer.

Instead of starting every coding session from zero and falling into generic "AI slop", the framework:

1. **Routes requests** to the right domain knowledge via a fast `ContextRouter`.
2. **Stores architectural decisions and bug history** in a SQLite-backed memory layer (`~/.cursor/memory/decisions.sqlite`).
3. **Reuses 50+ curated skills and 43 strict rules** (`.mdc`), enforcing surgical code edits and YAGNI discipline.
4. **Integrates ECC Universal v2.2.2** (68 agents, 292 skills, 94 commands) and **REA v6.4.0** (Reverse Engineer Anything).
5. **Provides 22 production-grade landing & SaaS templates** with zero dependencies, rich interactive logic, and human-crafted aesthetics.
6. **Supports 6 distinctive design themes** with an instant theme switcher and a secure CMS Dashboard (`admin` / `admin@123`).

---

## What's in the Box

| Components | Count / Details | Location |
|---|--:|---|
| **Rules** (`.mdc`) | 43 rule files | `.cursor/rules/` |
| **Skills** | 50 specialized skills | `.cursor/skills/` & `.agents/skills/` |
| **Templates** | 22 production-ready web apps | `cursor_framework_web/public/templates/` |
| **Vibe Code Tools** | 10+ popular IDEs & CLIs supported | `vibe-code-framework/07-adapters/` |
| **Themes** | 6 custom visual themes | `cursor_framework_web/src/styles/main.css` |
| **Agent Personas** | 18 specialized roles | `.cursor/AGENTS.md` |
| **ECC Integration** | 68 agents, 292 skills, 94 commands | [ECC v2.2.2](https://github.com/affaan-m/ECC) |
| **REA Integration** | Universal reverse engineering & decompilation | [morluto/rea v6.4.0](https://github.com/morluto/rea) |
| **VBS Security Scanner** | 21 cross-language vulnerability rules + SCA | `.cursor/skills/sec_reverse-engineer-anything/` |
| **Python Library** | 14 modules + 6 utility suites | `cursor_framework/` |
| **Web Dashboard & CMS** | Vue 3 + Vite 6 + TypeScript + CMS Auth Gate | `cursor_framework_web/` |
| **Windows GUI Installer** | `cursor-setup.exe` (~162 MB), `cursor-setup.zip` (~22 MB) | `dist/` |

---

## Multi-Tool Vibe Code Support Matrix

Framework cung cấp giải pháp **One Source — Universal Adapters**. Chỉ cần duy trì một bộ quy tắc và kỹ năng duy nhất, bạn có thể đồng bộ sang tất cả các công cụ Vibe Coding phổ biến nhất hiện nay:

| Vibe Code Tool | Configuration Path | Sync Script / Adapter | Agent Modes & Hotkeys |
|---|---|---|---|
| **Cursor IDE** | `%USERPROFILE%\.cursor\` or `~/.cursor/` | Native drop-in (`setup.bat`) | Composer (`Ctrl+I`), Chat (`Ctrl+L`), Agent Mode |
| **Windsurf (Codeium)** | `.windsurfrules`, `.windsurf/rules/` | `sync-adapters.ps1 -Tool Windsurf` | Cascade Flow (`Ctrl+L`), Supercomplete |
| **Claude Code** | `CLAUDE.md`, `.claude/skills/`, `.claude/rules/` | `npx ecc-universal@2.2.2 install --target claude` | Terminal pair programmer, headless CI/CD, hooks |
| **GitHub Copilot** | `.github/copilot-instructions.md`, `.github/prompts/` | `sync-adapters.ps1 -Tool Copilot` | Copilot Edits (`Ctrl+Shift+I`), Workspace agent |
| **Roo Code & Cline** | `.roomodes`, `.clinerules`, `.roomodes.json` | Native mode files in `07-adapters/` | Custom autonomous roles (Architect, Reviewer, Coder) |
| **Google Antigravity** | `~/.gemini/antigravity/` & `.agents/skills/` | `sync-adapters.ps1 -Tool Antigravity` | AGY CLI, Agentic workflows, sidecars, tool loops |
| **Trae (ByteDance)** | `.trae/rules/`, `AGENTS.md` | `sync-adapters.ps1 -Tool Cursor` | Claude 3.5 Sonnet / GPT-4o builder mode |
| **Devin / OpenHands** | `AGENTS.md`, `.openhands/instructions.md` | Copy `AGENTS.md` to workspace root | Autonomous issue solver, automated PR creator |
| **Aider** | `.aider.conf.yml`, `.cursor/rules/*.mdc` | `aider --read .cursor/rules/coding-standards.mdc` | Terminal Git pair programming, auto git-commits |
| **Bolt.new / v0.dev** | Export templates from `public/templates/` | Copy component spec & zero-skeleton HTML/JS | Instant web sandbox scaffolding |

### Quick Sync All Adapters

```powershell
# Windows PowerShell (sync toàn bộ adapters cho Cursor, Windsurf, Claude Code, Copilot, Codex, Antigravity)
.\vibe-code-framework\08-scripts\sync-adapters.ps1

# Đồng bộ riêng cho một công cụ cụ thể
.\vibe-code-framework\08-scripts\sync-adapters.ps1 -Tool Windsurf
.\vibe-code-framework\08-scripts\sync-adapters.ps1 -Tool Copilot
```

```bash
# macOS / Linux (Bash)
./vibe-code-framework/08-scripts/sync-adapters.sh --tool all
```

---

## Installation Guide (Hướng Dẫn Cài Đặt)

Bạn có thể lựa chọn 1 trong các phương thức cài đặt thuận tiện dưới đây:

### Cách 1: Windows GUI Installer (Khuyến nghị cho người mới)

1. Tải 2 file từ [Latest Release](https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/releases):
   - `cursor-setup.exe` (Self-contained, không yêu cầu cài .NET runtime)
   - `cursor-setup.zip` (Bộ payload framework ~22 MB)
2. Đặt cả 2 file vào cùng một thư mục.
3. Chạy `cursor-setup.exe`, chọn đường dẫn đích (mặc định `%USERPROFILE%\.cursor`).
4. Bấm **Install** và đợi 15 giây. Khởi động lại Cursor IDE / Windsurf.

### Cách 2: PowerShell One-Liner (Windows Tự Động 100%)

Mở PowerShell và dán lệnh sau để tự động tải và cài đặt bản mới nhất:

```powershell
irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex
```

Để cập nhật phiên bản mới sau này:
```powershell
& {irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1} -Update
```

### Cách 3: macOS / Linux Universal Script

```bash
curl -fsSL https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.sh | bash
```

### Cách 4: Cài đặt cho Claude Code / Codex qua NPX (ECC Universal)

```bash
# Cài đặt profile core cho Claude Code
npx ecc-universal@2.2.2 install --profile core --target claude

# Hoặc cài đặt qua trình hướng dẫn tương tác đa công cụ
npx ecc-universal@2.2.2 install --guided
```

### Cách 5: Clone & Cài Đặt Thủ Công từ Source

```powershell
git clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR.git
cd "CURSOR ENTERPRISE FRAMEWORK GENERATOR"

# Chạy script cài đặt
.\setup.bat                    # Cài đặt vào %USERPROFILE%\.cursor
.\setup.bat --force            # Ghi đè cài đặt cũ
.\setup.bat --gui-picker       # Bật hộp thoại chọn thư mục
```

### Cách 6: Cài đặt Thư Viện Python `cursor_framework`

```bash
cd "CURSOR ENTERPRISE FRAMEWORK GENERATOR"
pip install -e ".[all]"
```

*(Lưu ý: Không dùng `pip install cursor-framework` trên PyPI vì đó là package cũ của bên thứ 3. Luôn cài đặt từ mã nguồn repo này).*

---

## Usage Guide (Hướng Dẫn Sử Dụng)

### 1. Vibe Coding Lifecycle (agent-skills)

Framework vận hành theo chu trình 5 bước nghiêm ngặt:

```
DEFINE          PLAN           BUILD          VERIFY         SHIP
┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
│ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  Go  │
│Refine│      │  PRD │      │ Impl │      │Debug │      │ Live │
└──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /ship
```

### 2. Danh Sách Slash Commands Thông Dụng Trong IDE

Khi mở Composer (`Ctrl+I`) hoặc Chat (`Ctrl+L`) trong Cursor / Windsurf / Claude Code, bạn chỉ cần gõ `/` để kích hoạt:

| Slash Command | Persona / Action | Công Dụng Chi Tiết |
|---|---|---|
| `/spec` | Product Architect | Biến ý tưởng 1 dòng thành bản PRD đầy đủ, có tiêu chí nghiệm thu |
| `/plan` | Task Decomposer | Chia nhỏ bài toán thành các subtask độc lập, có checklist kiểm định |
| `/build` | Senior Developer | Sinh mã nguồn hoàn chỉnh, áp dụng `frontend-taste` và `full-output` |
| `/test` | Test Engineer | Viết unit test, integration test, kiểm tra biên độ lỗi và race condition |
| `/review` | Code Reviewer | Đánh giá 5 trục: Tính đúng đắn, Thiết kế, Bảo mật, Hiệu năng, Tiếp cận |
| `/security` | Security Auditor | Kiểm tra lỗ hổng OWASP, rò rỉ secret, CORS, CSRF |
| `/vbs-scan` | VBS Security Scanner | Quét 21 rule bảo mật chuyên sâu với AST taint analysis & SCA CVE |
| `/rea` | Reverse Engineer | Dịch ngược tệp nhị phân PE/ELF/.NET/APK/WASM thành code sạch |
| `/fullstack` | Fullstack Engineer | Xây dựng API ASP.NET Core / NestJS + React / Vue 3 đồng bộ contract |
| `/cms` | CMS Navigator | Quản trị, xem trước và chỉnh sửa 22 template trên CMS Dashboard |

---

## 22 Production-Ready Templates Catalog

Toàn bộ **22 templates** nằm tại thư mục [`cursor_framework_web/public/templates/`](file:///d:/PROJECTS/CURSORS/CURSOR%20ENTERPRISE%20FRAMEWORK%20GENERATOR/cursor_framework_web/public/templates/). Tất cả đều là **zero-dependency static code** (HTML5 + CSS3 + Vanilla JS), mở lên là chạy ngay trong trình duyệt hoặc iframe, không phụ thuộc server nặng nề:

| STT | Slug / Thư mục | Tên Mẫu Template | Ngành Nghề | Tính Năng Nổi Bật Thực Tế | Phong Cách Giao Diện |
|---|---|---|---|---|---|
| **1** | `auto-showroom` | **AutoPrime Motors** | Showroom Ô Tô Đa Hãng | • Lọc kho xe đa hãng (Porsche, Mercedes, BMW, Audi, Lexus, VinFast)<br>• **Công cụ tính giá lăn bánh** tự động áp thuế trước bạ địa phương (10-12%)<br>• **Bảng dự toán trả góp ngân hàng** (20%-80%, lãi suất giảm dần)<br>• Form đặt lịch lái thử tận nhà & cam kết kiểm định 176 hạng mục | Dark Slate Luxury Automotive (`#090d16` & Royal Amber Gold) |
| **2** | `viet-restaurant` | **Vị Xưa Quán** | Ẩm Thực Truyền Thống Việt | • Câu chuyện 38 năm gìn giữ hạt ngọc làng quê trên niêu đất Bát Tràng<br>• Menu 8 món biểu tượng 3 miền (Bắc - Trung - Nam)<br>• **Hệ thống E-Voucher 1 chạm sao chép** (`GIAM15`, `SUMVAY25`)<br>• Hướng dẫn 4 chi nhánh & Form đặt bàn online (phòng VIP, tiệc gia đình) | Heritage Warm Wood & Terracotta (`#180e0a` & Gold) |
| **3** | `insurance` | **Aegis Bảo An** | Bảo Hiểm Toàn Diện 4.0 | • Bộ công cụ **tính phí bảo hiểm tức thì trong 30s**<br>• Quy trình bồi thường trực tuyến e-Claim giải ngân trong 24h<br>• Bản đồ liên kết bảo lãnh viện phí **680+ bệnh viện** toàn quốc<br>• Hướng dẫn 4 bước mua bảo hiểm & đánh giá khách hàng | High-Trust Royal Navy Blue (`#041224` & Radiant Cyan) |
| **4** | `crm` | **SaaS CRM Platform** | CRM Doanh Nghiệp | Quản lý khách hàng tiềm năng, đường ống bán hàng Kanban, phân quyền vai trò | Dark Zinc & Emerald Minimalist |
| **5** | `sale` | **Flash Sale & Black Friday** | Thương Mại Điện Tử | Đồng hồ đếm ngược Flash Deal, thông báo đơn mua theo thời gian thực | High-Energy Crimson & Amber |
| **6** | `bazi` | **Tứ Trụ Mệnh Lý** | Phong Thủy & Bát Tự Á Đông | Bảng tra Can Chi, tính thập thần, luận giải cung mệnh học thuật | Á Đông Huyền Bí & Chu Sa |
| **7** | `numerology` | **Thần Số Học Pythagore** | Khám Phá Bản Thân | Tính con số chủ đạo, 4 đỉnh cao cuộc đời, biểu đồ ngày sinh | Neo Tokyo Cosmic Obsidian & Violet |
| **8** | `realestate` | **Bất Động Sản Nghỉ Dưỡng** | Bất Động Sản Cao Cấp | Bộ lọc phân khúc biệt thự biển, dự toán vay mua nhà, bản đồ tiện ích 360° | Warm Ivory & Emerald Gold |
| **9** | `food-delivery` | **Giao Đồ Ăn Nhanh** | Giao Hàng & F&B | Theo dõi đơn hàng theo thời gian thực, combo bữa trưa văn phòng, mã freeship | Fresh Tangerine & Warm Charcoal |
| **10** | `travel` | **Tour Trải Nghiệm & Du Lịch** | Du Lịch & Lữ Hành | Lịch trình tour theo ngày, chọn ngày khởi hành, đánh giá hướng dẫn viên | Tropical Azure & Sea Green |
| **11** | `beauty-spa` | **Viện Thẩm Mỹ & Spa** | Sức Khỏe & Làm Đẹp | Bảng giá dịch vụ chăm sóc da chuyên sâu, đặt lịch hẹn chuyên gia trị liệu | Rose Champagne & Soft Nude |
| **12** | `fitness` | **Phòng Gym & Huấn Luyện Viên** | Thể Thao & Fitness | Tính chỉ số BMI/TDEE, lịch tập luyện theo tuần, đăng ký gói tập PT 1-kèm-1 | High-Contrast Acid Lime & Charcoal |
| **13** | `edu-tutor` | **Gia Sư & Luyện Thi** | Giáo Dục Trực Tuyến | Tìm gia sư theo môn học, thi thử trực tuyến, lộ trình đỗ đại học điểm cao | Trustworthy Indigo & Golden Badge |
| **14** | `agritech` | **Nông Nghiệp Công Nghệ Cao** | Nông Nghiệp & IoT | Giám sát độ ẩm đất cảm biến IoT, truy xuất nguồn gốc nông sản Blockchain | Eco Leaf Green & Slate |
| **15** | `farm` | **Nông Trại Hữu Cơ** | Nông Nghiệp Sinh Thái | Gói rau sạch định kỳ hàng tuần, quy trình canh tác thuận tự nhiên | Earthy Olive & Terracotta |
| **16** | `orchard` | **Vườn Cây Ăn Quả Sinh Thái** | Trang Trại Sinh Thái | Đặt vé trải nghiệm thu hoạch trái cây tại vườn, đặc sản sấy dẻo OCOP | Sunny Citrus Orange & Mint |
| **17** | `church` | **Giáo Xứ & Mục Vụ** | Cộng Đoàn Tôn Giáo | Giờ lễ các ngày trong tuần, tin mục vụ giáo xứ, đóng góp thiện nguyện | Sacred Gold & Deep Stone Grey |
| **18** | `preschool` | **Mầm Non Song Ngữ** | Mầm Non & Giáo Dục Sớm | Thực đơn dinh dưỡng mỗi ngày, camera trực tuyến lớp học, phương pháp Montessori | Playful Pastel Sky & Sunny Yellow |
| **19** | `aitech` | **AI SaaS Platform** | Công Nghệ & Trí Tuệ Nhân Tạo | Bảng so sánh token LLM, playground thử nghiệm prompt, sandbox API | Deep Space Obsidian & Cyan Pulse |
| **20** | `computech` | **Thiết Bị Công Nghệ** | Phần Cứng & Laptop | Bộ lọc cấu hình gaming PC, build case máy tính tự động kiểm tra tương thích | Stealth Gunmetal & Cyberpunk Amber |
| **21** | `blog` | **Tạp Chí Công Nghệ** | Blog & Truyền Thông | Ước tính thời gian đọc, thanh tiến trình đọc bài, chế độ ban đêm tối ưu mắt | Editorial Typography & Clean Grey |
| **22** | `portfolio` | **Hồ Sơ Năng Lực Sáng Tạo** | Portfolio Cá Nhân | Thư viện dự án dạng lưới bẻ trục, timeline kinh nghiệm, biểu mẫu liên hệ | Monochromatic Minimalist & High Contrast |

---

## Sample Prompts (Mẫu Prompts Vibe Coding Chuẩn Mực)

Để AI sinh code chuẩn xác, không bịa đặt và không để lại skeleton placeholder, hãy sử dụng **Công Thức Prompt 5 Thành Phần (Golden Formula)**:

$$\text{Prompt} = \text{Vai Trò (Role)} + \text{Bối Cảnh & Mục Tiêu (Context)} + \text{Ràng Buộc Nghiêm Ngặt (Constraints)} + \text{Kiểm Định (Dual Gates)} + \text{Đầu Ra Hoàn Chỉnh (Full Output)}$$

### Mẫu 1: Xây Dựng Showroom Ô Tô Đa Hãng
```markdown
Bạn là Kiến trúc sư giải pháp frontend cao cấp theo chuẩn /evondev-ui-ux và /ui_landing-page-pro.
Hãy xây dựng sàn giao dịch ô tô cao cấp AutoPrime Motors:
1. Nền tảng xe đa hãng (Porsche, Mercedes-Benz, BMW, Audi, Lexus, VinFast, Volvo).
2. Tích hợp bộ công cụ tính giá lăn bánh tức thì: Tự động cộng thuế trước bạ địa phương (Hà Nội 12%, TP.HCM 10%, tỉnh khác 10%), phí biển số và bảo hiểm bắt buộc.
3. Bảng dự toán trả góp ngân hàng: Người dùng kéo chọn tỉ lệ trả trước (20%-80%) và số năm vay (1-8 năm), tự động tính số tiền gốc + lãi trả hàng tháng.
4. Cam kết kiểm định 176 hạng mục, đặt lịch lái thử tại nhà (Home Test Drive), hệ thống 5 showroom.
5. Phong cách Dark Slate Luxury Automotive (#090d16 viền vàng kim #f59e0b). Zero placeholder, mã HTML5/CSS/JS thuần độc lập.
```

### Mẫu 2: Xây Dựng Nhà Hàng Ẩm Thực Truyền Thống Việt
```markdown
Đóng vai trò UX Designer & Content Creator theo chuẩn /frontend-taste.
Thiết kế trang web nhà hàng ẩm thực di sản Vị Xưa Quán:
1. Thể hiện câu chuyện 38 năm gìn giữ cơm niêu đất nung Bát Tràng và triết lý ngũ hành ẩm thực 3 miền.
2. Thực đơn 8 món ăn biểu tượng chia theo tabs (Món Bắc, Món Trung, Món Nam, Tráng Miệng & Trà Sen).
3. Trải nghiệm dịch vụ 5 sao: Phòng VIP tiếp khách riêng tư, hòa tấu nhạc dân tộc, bãi đỗ xe ô tô.
4. Hệ thống voucher e-coupon (GIAM15, SUMVAY25) bấm 1 chạm sao chép ngay vào clipboard.
5. Form đặt bàn trực tuyến chọn chi nhánh và ghi chú dị ứng/yêu cầu đặc biệt.
6. Phong cách Gỗ mun gụ ấm áp (#180e0a) kết hợp đỏ đất nung và vàng rơm hoàng cung. Font Playfair Display thanh tao.
```

### Mẫu 3: Quét Lỗ Hổng Bảo Mật & Tự Động Vá (vbsec)
```markdown
Thực hiện quét bảo mật toàn diện dự án theo kỹ năng /vbs-scan-security:
1. Phân tích luồng dữ liệu L1-L4 từ các nguồn untrusted inputs (req.body, query, params) tới các sinks nhạy cảm (SQL query, command execution, SSRF).
2. Kiểm tra các thư viện bên thứ 3 phát hiện CVE tồn đọng qua OSV.dev database (--sca).
3. Xuất file báo cáo chuẩn SARIF và sinh các bản vá lỗi (git diff) tối thiểu, không gây breaking changes logic ứng dụng.
```

### Mẫu 4: Dịch Ngược Nhị Phân & Tái Tạo Mã Nguồn Sạch (REA)
```markdown
Sử dụng công cụ /reverse-engineer-anything để kiểm tra file nhị phân target:
1. Trích xuất symbol table, import/export APIs và control flow graph.
2. Tách biệt hoàn toàn phần logic kinh doanh (Cleanroom Spec), vẽ sơ đồ tuần tự Sequence Diagram.
3. Viết lại module tương đương bằng TypeScript/C# hoàn toàn sạch (cleanroom replacement), có bộ test case xác nhận độ tương thích 1:1.
```

---

## Essential Commands Reference (Bảng Tổng Hợp Lệnh Cần Thiết)

### 1. Lệnh Phát Triển & Web Dashboard

```bash
# Di chuyển vào thư mục web dashboard
cd cursor_framework_web

# Cài đặt thư viện Node
npm install

# Khởi chạy server phát triển (Vite 6)
npm run dev                     # Mở http://localhost:5173

# Sinh lại toàn bộ 22 thumbnail preview PNGs
node scripts/generate-previews.js

# Kiểm tra TypeScript & Đóng gói sản phẩm sản xuất
npm run build                   # Tự động chạy prebuild sinh PNGs + vue-tsc + vite build

# Chạy thử bản production
npm run preview
```

### 2. Lệnh Đồng Bộ Adapters & Vibe Code

```powershell
# Đồng bộ tất cả adapters (.cursor, .claude, .windsurf, .agents, .github)
.\vibe-code-framework\08-scripts\sync-adapters.ps1

# Đồng bộ riêng từng tool
.\vibe-code-framework\08-scripts\sync-adapters.ps1 -Tool Cursor
.\vibe-code-framework\08-scripts\sync-adapters.ps1 -Tool Windsurf
.\vibe-code-framework\08-scripts\sync-adapters.ps1 -Tool Copilot
.\vibe-code-framework\08-scripts\sync-adapters.ps1 -Tool Antigravity

# Kiểm tra tính toàn vẹn của framework
.\vibe-code-framework\08-scripts\validate.ps1
```

### 3. Lệnh Thư Viện Python & Trí Nhớ SQLite

```bash
# Cài đặt thư viện ở chế độ editable
pip install -e ".[all]"

# Khởi chạy Dashboard HTTP local
python -c "from cursor_framework import Dashboard, Workflow; dash = Dashboard(root='.cursor', workflow=Workflow(root='.cursor')); dash.serve(port=8765)"

# Tạo lại chỉ mục INDEX.json và INDEX.md
python -m cursor_framework.indexer .cursor

# Chạy toàn bộ test suites (136+ unit tests)
pytest
```

### 4. Lệnh Reverse Engineering (REA)

```powershell
# Kiểm tra phiên bản REA CLI
node tools/rea/scripts/rea.mjs --version

# Khởi chạy REA MCP Server (stdio)
node tools/rea/scripts/rea.mjs mcp

# Chạy sanity test REA
.\tools\rea\setup-rea.ps1
```

### 5. Lệnh Build Trình Cài Đặt Windows GUI

```powershell
cd cursor-setup-gui-wpf
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true -o ../dist
```

---

## Themes & UI/UX System

Để đảm bảo giao diện **"Không thuần AI, nhìn wow"**, toàn bộ hệ thống áp dụng triết lý thiết kế từ:
- **`frontend-taste` & `hallmark`**: 57 cổng kiểm định slop-test (loại bỏ gradient tím/hồng vô nghĩa, tránh layout 3 card cân xứng sáo rỗng, không dùng ảnh stock AI chung chung).
- **`evondev-ui-ux`**: Chuẩn khoảng cách 8px scale, nhịp thở typography tương phản cao, chuyển động vi mô tự nhiên `cubic-bezier(0.16, 1, 0.3, 1)`.

### 6 Theme Giao Diện Tích Hợp Sẵn

Người dùng có thể chuyển đổi giao diện tức thì qua nút chọn Theme trên thanh điều hướng (`NavBar.vue`):

1. **Emerald Engine** (`theme-emerald` - Mặc định): Dark Zinc tối tân kết hợp sắc xanh ngọc Acid Emerald, phong cách Linear/Vercel.
2. **Indigo Linear** (`theme-indigo`): Tím đêm điện tử kết hợp ánh sáng Neon Indigo huyền ảo.
3. **Cyber Amber** (`theme-cyberpunk`): Sắc đen Obsidian bóng bẩy điểm xuyết hổ phách hoàng kim và cyan công nghệ cao.
4. **Slate Luxury** (`theme-slate`): Titanium xám nhám cao cấp kết hợp ánh vàng Champagne, chuẩn thiết kế xe hơi & tài chính xa xỉ.
5. **Warm Heritage** (`theme-heritage`): Gỗ mun gụ ấm áp, đất nung đỏ và vàng rơm di sản Á Đông.
6. **Clean Editorial** (`theme-light`): Nền giấy trắng tuyết thanh lịch, độ tương phản cao, tối ưu cho môi trường ánh sáng ban ngày.

---

## CMS Dashboard & Quản Trị Hệ Thống

Hệ thống tích hợp trang quản trị CMS Dashboard chuyên nghiệp tại đường dẫn `/#/cms`:
- **Cổng xác thực an toàn cố định**:
  - **Tài khoản:** `admin`
  - **Mật khẩu:** `admin@123`
- **Các tính năng quản trị chính**:
  - Theo dõi KPI tổng quan (22 gói templates, 137 trang landing pages, 148K+ tương tác, Lighthouse 99.2/100).
  - Tìm kiếm & lọc đa chiều theo ngành nghề, trạng thái hiển thị (Active/Draft) và đánh dấu nổi bật (Featured).
  - Chuyển đổi linh hoạt giữa giao diện **Lưới (Grid)** và **Bảng dữ liệu (Table)**.
  - Xem trước tức thì (Quick View Modal) và mở toàn màn hình (Full Preview).
  - Form thêm mới / chỉnh sửa metadata, tính năng, tags và xuất file ZIP triển khai.

---

## License & Conventions

- **License:** MIT License — Xem chi tiết tại [LICENSE](LICENSE).
- **Versioning:**
  - Repo Releases: `v1.3.0`
  - Framework Payload: `4.2.0`
  - ECC Universal: `2.2.2`
  - REA Engine: `6.4.0`
