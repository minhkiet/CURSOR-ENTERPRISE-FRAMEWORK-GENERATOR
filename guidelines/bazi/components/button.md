# Button

> Nút bấm kích hoạt hành động. Đọc như triện ấn lên giấy rice: phản hồi xúc giác rõ, không animation thừa.

## 1. Mục đích

Trigger actions: tạo bát tự (create chart), xem luận giải (view reading), so sánh chart (compare), chia sẻ (share). Mỗi nút có phản hồi rõ ràng trong 0.3s.

## 2. Hệ thống icon

Phosphor Regular (`@phosphor-icons/react`), `weight="bold"` cho icon stroke.

| Role | Icon | Size theo button size |
|---|---|---|
| Tạo bát tự | `YinYang` (fill) | 14/16/18/20px |
| Xem luận giải | `Scroll` | tương tự |
| So sánh chart | `ArrowsHorizontal` | tương tự |
| Chia sẻ | `ShareNetwork` | 14px |
| Bookmark | `BookmarkSimple` | 14px |
| Loading | `CircleNotch` (spin) | 14px |
| Success | `CheckCircle` (fill) | 14px, cinnabar |
| External | `ArrowUpRight` | 12px |
| Continue | `ArrowRight` | 14px |
| Back | `ArrowLeft` | 14px |
| Close | `X` | 16px |

## 3. Cấu trúc

```
[icon-left?]  label  [icon-right?]
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| icon-left | không | 14–22px Phosphor bold. |
| label | có | Hán tự + bính âm tuỳ chọn. Sentence case cho actions, ALL CAPS cho premium CTAs. |
| icon-right | không | 14–22px. Chevron / arrow. |
| focus ring | có | Bao quanh toàn bộ. |

## 4. Biến thể

| Variant | Nền | Chữ | Viền | Cách dùng |
|---|---|---|---|---|
| `primary-on-dark` | `#1a1410` sumi | `#ede4cf` | không | CTA chính |
| `primary-on-light` | `#a8331f` cinnabar | `#ede4cf` | không | Featured CTA, "Tạo bát tự" |
| `ghost` | transparent | `#3d2e1f` | `1px solid rgba(122, 93, 47, 0.18)` | Nav links dạng nút |
| `ghost-inverse` | transparent | `#ede4cf` | `1px solid rgba(176, 154, 90, 0.25)` | Bề mặt tối |
| `seal-disc` | `#a8331f` | `#ede4cf` | không, shape tròn 44px | Icon-only "印" |
| `link-cta` | transparent | `#a8331f` | không, underline on hover | Inline CTA |

## 5. Sizes

| Token | Padding (x/y) | Font | Min height |
|---|---|---|---|
| `sm` | 14/8 | 13px | 36px |
| `md` | 18/14 | 14px | 44px (mặc định) |
| `lg` | 24/18 | 15.5px | 52px (hero CTA) |
| `xl` | 32/20 | 16.5px | 56px |

## 6. Trạng thái

| Trạng thái | Thay đổi thị giác | Motion | Ghi chú a11y |
|---|---|---|---|
| default | base |. |. |
| hover | bg sẫm 3%, shadow nâng | 150ms ease-out | phải đạt qua `:focus-visible` |
| focus-visible | outline 2px cinnabar offset 2px | không | bắt buộc |
| active | bg sẫm 6%, translateY(1px) | 80ms | xúc giác ấn |
| disabled | opacity 0.45, cursor not-allowed | không | aria-disabled + tooltip |
| loading | label thay bằng spinner + "正在载入...", giữ width | 800ms linear | aria-busy="true" |
| success | bg sang cinnabar sáng, "成功", `CheckCircle` icon | 200ms | role="status" |

## 7. Touch targets và accessibility

- Hit area ≥44×44px.
- Tương phản đã verify trong tokens.json.
- Tab order, Enter/Space, Escape đều theo pattern chuẩn.

## 8. Code reference

```tsx
{/* CTA tạo bát tự với YinYang icon */}
<button
  type="button"
  class="group inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-[#a8331f] text-[#ede4cf] font-bold uppercase text-[14px] tracking-[0.1em] shadow-[0_4px_0_rgba(122,36,21,0.4),0_12px_24px_rgba(168,51,31,0.18)] hover:-translate-y-px hover:shadow-[0_5px_0_rgba(122,36,21,0.4),0_16px_32px_rgba(168,51,31,0.25)] active:translate-y-0 active:shadow-[0_2px_0_rgba(122,36,21,0.4)] transition-all duration-150 rounded-[2px]"
>
  <Phosphor.YinYang size={16} weight="fill" aria-hidden="true" />
  <span>排盘</span>
  <Phosphor.ArrowRight size={16} weight="bold" class="transition-transform duration-150 group-hover:translate-x-0.5" aria-hidden="true" />
</button>

{/* Ghost nav link */}
<a
  href="/charts"
  class="inline-flex items-center gap-1.5 px-4 py-2 text-[#3d2e1f] border border-[rgba(122,93,47,0.18)] font-medium text-[14px] rounded-[2px] hover:border-[#7a5d2f] hover:bg-[rgba(122,93,47,0.05)] transition-all duration-150"
>
  <Phosphor.Scroll size={14} weight="bold" aria-hidden="true" />
  <span>历代命盘</span>
</a>

{/* Seal disc icon button */}
<button
  type="button"
  aria-label="印 · Lưu chart"
  class="inline-flex items-center justify-center w-11 h-11 bg-[#a8331f] text-[#ede4cf] rounded-full shadow-[0_0_0_1px_rgba(168,51,31,0.25),0_6px_18px_rgba(168,51,31,0.30)] hover:-translate-y-0.5 active:translate-y-0 transition-transform duration-150"
>
  <Phosphor.Seal size={20} weight="bold" aria-hidden="true" />
</button>
```