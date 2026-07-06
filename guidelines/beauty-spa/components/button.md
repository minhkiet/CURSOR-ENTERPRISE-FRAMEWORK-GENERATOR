# Button

> Nút bấm cho booking flow. Đọc như rose-gold fixture trên nền sand: tinh tế, phản hồi xúc giác rõ.

## 1. Mục đích

Trigger: đặt lịch (book), xem treatment, thanh toán, chia sẻ, lưu yêu thích. Phản hồi trong 0.3s, không micro-animation thừa.

## 2. Icon system

Phosphor Regular (`@phosphor-icons/react`), `weight="regular"` cho mood icons, `weight="bold"` cho action icons.

| Role | Icon | Size |
|---|---|---|
| Đặt lịch | `CalendarPlus` | 14/16/18/20px |
| Tiếp tục | `ArrowRight` | tương tự |
| Quay lại | `ArrowLeft` | tương tự |
| Yêu thích | `Heart` | 14px |
| Chia sẻ | `ShareNetwork` | 14px |
| Thanh toán | `CreditCard` | 16px |
| Thành công | `CheckCircle` (fill) | 16px, sage |
| Loading | `CircleNotch` (spin) | 14px, tertiary |
| Đóng | `X` | 16px |
| Filter | `Funnel` | 14px |
| Membership tier | `Crown` (fill) | 14px, gold |
| Spa wellness | `Flower` | 14px |

## 3. Cấu trúc

```
[icon-left?]  label  [icon-right?]
```

| Slot | Bắt buộc | Ghi chú |
|---|---|---|
| icon-left | không | 14–22px |
| label | có | Tiếng Việt sentence case, ALL CAPS cho premium CTAs |
| icon-right | không | 14–22px, chevron / arrow |
| focus ring | có | Bao toàn bộ |

## 4. Variants

| Variant | Nền | Chữ | Viền | Cách dùng |
|---|---|---|---|---|
| `primary` | `#a07749` rose-gold deep | `#f8f4ec` | không | "Đặt lịch", main booking CTA |
| `secondary` | `#2c2620` walnut | `#f8f4ec` | không | Secondary CTAs |
| `ghost` | transparent | `#2c2620` | `1px solid #d4c7b3` | Tertiary actions |
| `ghost-inverse` | transparent | `#f8f4ec` | `1px solid rgba(212, 165, 116, 0.25)` | Walnut surface |
| `link-cta` | transparent | `#a07749` | không, underline on hover | Inline CTA |
| `icon-only` | matches ghost variants | none | matches | Heart, share, close |
| `membership` | `#2c2620` walnut + `Crown` (fill) gold | `#f8f4ec` | `1px solid #d4a574` | Member-only actions |

## 5. Sizes

| Token | Padding (x/y) | Font | Min height |
|---|---|---|---|
| `sm` | 14/8 | 13px | 36px |
| `md` | 18/14 | 14px | 44px (default) |
| `lg` | 24/18 | 15.5px | 52px (hero CTA) |
| `xl` | 32/20 | 16.5px | 56px |

## 6. States

| State | Visual | Motion |
|---|---|---|
| default | base |. |
| hover | bg sẫm 3%, shadow lifted | 180ms breath |
| focus-visible | outline 2px rose-gold offset 2px | none |
| active | bg sẫm 6%, translateY(1px) | 80ms |
| disabled | opacity 0.45, cursor not-allowed | none |
| loading | label → spinner + "Đang xử lý...", giữ width | 800ms linear |
| success | bg → sage, label → "Đã đặt", `CheckCircle` icon | 240ms |

## 7. Code reference

```tsx
{/* Primary book CTA với CalendarPlus */}
<button
  type="button"
  class="group inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-[#a07749] text-[#f8f4ec] font-medium uppercase text-[14px] tracking-[0.12em] shadow-[0_4px_16px_rgba(160,119,73,0.18)] hover:-translate-y-px hover:shadow-[0_8px_24px_rgba(160,119,73,0.25)] active:translate-y-0 active:shadow-[0_2px_8px_rgba(160,119,73,0.18)] transition-all duration-180 rounded-full"
>
  <Phosphor.CalendarPlus size={16} weight="bold" aria-hidden="true" />
  <span>Đặt lịch</span>
</button>

{/* Heart favorite icon-only */}
<button
  type="button"
  aria-label="Yêu thích"
  aria-pressed={isFavorited}
  class="inline-flex items-center justify-center w-11 h-11 text-[#a07749] hover:bg-[rgba(212,165,116,0.10)] focus-visible:outline-2 focus-visible:outline-[#a07749] focus-visible:outline-offset-2 transition-colors duration-180 rounded-full"
>
  <Phosphor.Heart size={20} weight={isFavorited ? 'fill' : 'regular'} aria-hidden="true" />
</button>

{/* Ghost "Xem chi tiết" */}
<a
  href="/treatments/hydrafacial"
  class="group inline-flex items-center gap-1.5 px-5 py-2.5 text-[#2c2620] border border-[#d4c7b3] font-medium text-[13px] rounded-full hover:border-[#a07749] hover:bg-[rgba(212,165,116,0.06)] transition-all duration-180"
>
  <span>Xem chi tiết</span>
  <Phosphor.ArrowRight size={13} weight="bold" class="transition-transform duration-180 group-hover:translate-x-0.5" aria-hidden="true" />
</a>
```