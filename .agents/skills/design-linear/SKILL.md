---
name: design-linear
description: "Linear Design System - thiết kế UI/UX dark mode cao cấp, hairline borders, lavender accent #5e6ad2 từ awesome-design-md"
---

# Linear Design System Skill

> **Preset Origin:** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — `linear.app`
> **Phạm vi:** Tạo mới hoặc refactor giao diện web (React, Vue, Tailwind CSS, HTML) sang phong cách thiết kế Linear: Dark mode điện ảnh, viền hairline siêu mảnh, điểm nhấn lavender `#5e6ad2`.

---

## 1. Khi nào kích hoạt Skill này?

Kích hoạt skill này khi:
- Người dùng yêu cầu thiết kế giao diện theo phong cách **Linear**, **Linear-like**, hoặc **SaaS dark mode cao cấp**.
- Cần tạo các component như: B2B dashboard, issue tracker, Kanban board, command palette (⌘K), settings panel, code review interface.
- Cần chuẩn hóa màu sắc, border radius, typography theo chuẩn `DESIGN.md`.

---

## 2. Token Palette Nhanh (Cheat Sheet)

```css
/* Nền & Bề mặt */
Canvas:     #08090a
Surface 1:  #0f1011  (Card, Panel)
Surface 2:  #141516  (Hover, Dropdown)
Surface 3:  #1c1d1f  (Modal, Dialog)
Inset:      #050506  (Code block, Input)

/* Viền (Hairline 1px) */
Border:     rgba(255, 255, 255, 0.08)
Hover:      rgba(255, 255, 255, 0.16)
Focus:      rgba(94, 106, 210, 0.5)

/* Chữ */
Primary:    #f7f8f8
Secondary:  #8a8f98
Tertiary:   #62666d

/* Accent */
Lavender:   #5e6ad2  (Hover: #717de0, Sub: rgba(94,106,210,0.15))
```

---

## 3. Các Component Mẫu Chuẩn (Ready-to-use)

### A. Command Bar / Search Input (⌘K Style)
```tsx
<div className="relative flex items-center w-full max-w-lg rounded-[8px] bg-[#0f1011] border border-white/[0.08] px-3 py-2 shadow-[0_4px_16px_rgba(0,0,0,0.4)] focus-within:border-[#5e6ad2]/50 focus-within:ring-1 focus-within:ring-[#5e6ad2]/50 transition-all">
  <svg className="w-4 h-4 text-[#8a8f98] mr-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
  <input 
    type="text" 
    placeholder="Search issues, projects, or type a command..." 
    className="w-full bg-transparent text-[13px] text-[#f7f8f8] placeholder-[#62666d] focus:outline-none"
  />
  <kbd className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-[4px] bg-[#191b1d] border border-white/[0.1] text-[10px] font-mono text-[#8a8f98]">
    ⌘K
  </kbd>
</div>
```

### B. Status Indicator Pill & Badge
```tsx
<div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/[0.04] border border-white/[0.08] text-[12px] font-medium text-[#8a8f98]">
  <span className="w-1.5 h-1.5 rounded-full bg-[#5e6ad2] animate-pulse" />
  <span>Linear Sync Active</span>
</div>
```

### C. Kanban Card / List Item
```tsx
<div className="group flex flex-col gap-2 rounded-[8px] bg-[#0f1011] p-3.5 border border-white/[0.08] hover:border-white/[0.16] hover:bg-[#141516] transition-all duration-150 cursor-pointer">
  <div className="flex items-center justify-between">
    <span className="text-[11px] font-mono text-[#62666d]">LIN-409</span>
    <span className="text-[11px] text-[#8a8f98]">Updated 2h ago</span>
  </div>
  <p className="text-[13px] font-medium text-[#f7f8f8] leading-snug group-hover:text-white">
    Implement declarative routing & nested transitions
  </p>
  <div className="flex items-center gap-2 mt-1">
    <span className="px-1.5 py-0.5 rounded-[4px] bg-[#5e6ad2]/15 text-[#5e6ad2] text-[10px] font-medium">
      Frontend
    </span>
  </div>
</div>
```

---

## 4. Quy trình áp dụng vào Dự án

1. **Khởi tạo token:** Sao chép file mẫu `vibe-code-framework/06-templates/design-md-linear.md` vào thư mục gốc dự án dưới tên `DESIGN.md`.
2. **Cấu hình Tailwind:** Thêm các màu `linear-*` vào file `tailwind.config.ts`.
3. **Kiểm tra Rule:** Đảm bảo file `.cursor/rules/design-linear.mdc` đã sẵn sàng hỗ trợ các gợi ý code.
4. **Audit Anti-slop:** Kiểm tra độ tương phản, đảm bảo không có viền dày hoặc gradient lòe loẹt.
