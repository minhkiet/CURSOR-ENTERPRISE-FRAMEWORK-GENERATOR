# Spec-Driven Development (SDD) Workflow

> **Version:** 1.0.0 | **Framework:** Vibe Enterprise Framework & GitHub Spec Kit Compatible
> **Core Principle:** Specification Before Implementation | Test-Driven Discipline

---

## 1. Mục đích

Chuẩn hóa toàn diện quy trình phát triển phần mềm bằng AI theo phương pháp **Spec-Driven Development (SDD)** lấy cảm hứng từ GitHub Spec Kit (`github/spec-kit`). Thay vì prompt tùy hứng ("vibe coding"), mọi tính năng quan trọng đều được dẫn dắt bởi quy chuẩn bất biến, đặc tả nghiệp vụ, kiến trúc kỹ thuật và kiểm thử tự động.

---

## 2. Chu trình 7 Giai đoạn (The 7 Phases)

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Constitution  ➔ Thiết lập nguyên tắc & ràng buộc bất biến    │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 2: Specify       ➔ Đặc tả yêu cầu nghiệp vụ & kịch bản BDD      │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 3: Clarify       ➔ Phản biện & giải tỏa mơ hồ, làm rõ edge-case │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 4: Plan          ➔ Thiết kế kiến trúc, API contract, data schema │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 5: Checklist     ➔ Kiểm duyệt Quality Gates (CEF CX.1 - CX.7)   │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 6: Tasks         ➔ Bẻ nhỏ plan thành atomic tasks có test command│
├────────────────────────────────────────────────────────────────────────┤
│ Phase 7: Implement     ➔ Thực thi TDD Red-Green-Refactor & cập nhật log │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Chi tiết từng bước thực hiện

### Bước 1: Khởi tạo Constitution (`.specify/constitution.md`)
- Chạy lệnh khởi tạo:
  ```bash
  python -m vibe_framework spec constitution
  ```
- Định hình các nguyên tắc bất biến: phiên bản runtime, tiêu chuẩn zero unvetted dependencies, quy định TDD bắt buộc.

### Bước 2: Khởi tạo gói Spec cho Feature
- Tạo khung thư mục đặc tả:
  ```bash
  python -m vibe_framework spec init <feature-name>
  ```
- Cấu trúc sinh ra tại `.specify/specs/<feature-name>/`:
  - `spec.md`: Đặc tả nghiệp vụ (User stories, BDD Scenarios, In/Out Scope).
  - `plan.md`: Kiến trúc kỹ thuật, Data models, API contracts, Risk assessment.
  - `tasks.md`: Danh sách task nguyên tử kèm file path và test command.
  - `checklist.md`: Bảng kiểm soát chất lượng theo CEF Quality Gates.

### Bước 3: Soạn thảo Specification (`spec.md`)
- Kích hoạt skill: `speckit-specify` hoặc slash command `/speckit.specify`.
- Trả lời rõ câu hỏi: *Vấn đề gì cần giải quyết?* và *Tại sao?*
- Viết Acceptance Criteria theo định dạng Gherkin:
  ```gherkin
  Scenario: Xử lý thanh toán thành công
    Given Người dùng có số dư khả dụng >= 100.000 VNĐ
    When Thực hiện thanh toán đơn hàng mã "ORD-123"
    Then Số dư bị trừ đúng 100.000 VNĐ và trạng thái đơn chuyển sang "PAID"
  ```

### Bước 4: Làm rõ & Phản biện (`speckit-clarify`)
- Rà soát các tình huống biên:
  - Network timeout khi gọi payment gateway?
  - Dữ liệu rỗng hoặc sai định dạng?
  - Race condition khi người dùng bấm thanh toán 2 lần liên tiếp?

### Bước 5: Lập kế hoạch kỹ thuật (`plan.md`)
- Kích hoạt skill: `speckit-plan` hoặc slash command `/speckit.plan`.
- Xác định rõ:
  - Data models và kiểu dữ liệu.
  - Danh sách endpoint, request/response schema.
  - File impact map: các file cụ thể sẽ tạo mới hoặc chỉnh sửa.
  - Chiến lược kiểm thử tự động (Unit test, Integration test).

### Bước 6: Chia nhỏ Task nguyên tử (`tasks.md`)
- Kích hoạt skill: `speckit-tasks` hoặc slash command `/speckit.tasks`.
- Chia theo 4 Phase:
  - **Phase 1 (RED):** Viết test harness và test case thất bại.
  - **Phase 2 (GREEN):** Hiện thực logic nghiệp vụ tối thiểu để test pass.
  - **Phase 3:** Tích hợp API routes hoặc UI.
  - **Phase 4 (REFACTOR):** Tối ưu code, loại bỏ mã thừa, kiểm tra docstrings.

### Bước 7: Thực thi TDD & Cập nhật tiến độ (`speckit-implement`)
- Kích hoạt skill: `speckit-implement` hoặc slash command `/speckit.implement`.
- Agent tuân thủ nghiêm ngặt chu trình Red-Green-Refactor.
- Sau mỗi task hoàn thành, cập nhật `[x]` trong `tasks.md`.
- Theo dõi tiến độ bất kỳ lúc nào:
  ```bash
  python -m vibe_framework spec status <feature-name>
  ```
- Kiểm tra toàn diện chất lượng trước khi đóng task:
  ```bash
  python -m vibe_framework spec validate <feature-name>
  ```

---

## 4. Tương thích Multi-Tool Adapters

Workflow này hoạt động nhất quán trên mọi IDE & Agent công cụ:
- **Cursor IDE**: Tương thích qua `.cursor/skills/` và prompt commands.
- **Claude Code**: Tương thích qua `.claude/skills/`.
- **GitHub Copilot**: Tương thích qua `.github/prompts/` & prompt files.
- **Google Antigravity / Gemini CLI**: Tương thích qua `.agents/skills/`.
- **Windsurf**: Tương thích qua Flow cascades và `.windsurf/rules/`.
