# Data Table

> Bảng dữ liệu cho contacts, deals, accounts. Density cao, sort được, multi-select, real semantic table.

## 1. Mục đích

Hiển thị danh sách records với sort, filter, multi-select, inline edit. Phải đọc nhanh qua 50+ rows.

## 2. Icon system

| Role | Icon Phosphor | Size |
|---|---|---|
| Sort asc | `CaretUp` | 11px |
| Sort desc | `CaretDown` | 11px |
| Sortable (unsorted) | `ArrowsDownUp` | 11px, tertiary |
| Filter | `Funnel` | 12px |
| Filtered | `FunnelSimple` (fill) | 12px, accent |
| Search | `MagnifyingGlass` | 12px |
| Bulk select | `CheckSquare` | 14px |
| Indeterminate | `MinusSquare` | 14px |
| Unchecked | `Square` | 14px |
| Owner | `UserCircle` | 14px |
| Company | `Buildings` | 14px |
| Email | `Envelope` | 12px |
| Phone | `Phone` | 12px |
| Status won | `CheckCircle` (fill) | 12px, mint |
| Status lost | `XCircle` (fill) | 12px, rose |
| Status open | `Circle` | 12px, slate |
| Status stalled | `Warning` (fill) | 12px, amber |
| Action menu | `DotsThreeVertical` | 14px |
| Edit inline | `PencilSimple` | 12px |
| Loading | `CircleNotch` (spin) | 14px |

## 3. Cấu trúc

```
┌──────────────────────────────────────────────────────────────────┐
│ [☐] NAME              COMPANY    OWNER   VALUE   STAGE   UPDATED│
├──────────────────────────────────────────────────────────────────┤
│ [☐] Aurora SaaS      Initech       Mira    $12,500 ● Won    2h ago │
│ [☐] Linear Clone     Stripe      Tom     $48,000 ● Open   1d ago │
│ ...                                                               │
└──────────────────────────────────────────────────────────────────┘
```

## 4. Tokens

| Token | Value |
|---|---|
| Header bg | `#f1f5f9` subtle |
| Row height | 48px |
| Border | 1px `#e2e8f0` between rows |
| Header sticky | `top: 56px` (under top nav) |
| Numeric column | right-aligned, tabular-nums |
| Hover row bg | `#f8fafc` |

## 5. Variants

| Variant | Padding | Use |
|---|---|---|
| `default` | 12/16 | Standard list |
| `compact` | 8/12 | Dense mode, 36px row height |
| `comfortable` | 16/24 | Accessible mode, 56px row height |

## 6. States

| Row state | Visual |
|---|---|
| default | base |
| hover | bg `#f8fafc` |
| selected | bg `#eef2ff` indigo tint |
| focused | outline 2px indigo on row left |
| editing | bg white, input field inline |
| loading | skeleton row 48px |
| error | bg `#fef2f2` rose tint, error message below |

## 7. Sort

- Click column header to sort asc.
- Click again to sort desc.
- `aria-sort="ascending|descending|none"` on `<th>`.
- Sort icon updates visually (`CaretUp` / `CaretDown` / `ArrowsDownUp`).
- Multi-column sort via Shift+click (planned).

## 8. Bulk select

- Header checkbox: `CheckSquare` if all selected, `MinusSquare` if partial, `Square` if none.
- Row checkbox: same.
- Selection state announced via `aria-live="polite"`: "5 contacts selected".

## 9. Code reference

```tsx
<div class="bg-white border border-[#e2e8f0] rounded-md overflow-hidden">
  <table class="w-full">
    <caption class="sr-only">Deals pipeline, showing 24 of 247</caption>
    <thead class="bg-[#f1f5f9] sticky top-14 z-10">
      <tr class="border-b border-[#e2e8f0]">
        <th scope="col" class="w-12 px-4 py-3">
          <input type="checkbox" aria-label="Select all visible rows" />
        </th>
        <th scope="col" class="px-4 py-3 text-left">
          <button class="inline-flex items-center gap-1 font-medium text-[12px] uppercase tracking-wider text-[#475569]">
            Name
            <Phosphor.CaretUp size={11} weight="bold" class="text-[#4f46e5]" aria-hidden="true" />
          </button>
        </th>
        <th scope="col" class="px-4 py-3 text-left">
          <button class="inline-flex items-center gap-1 font-medium text-[12px] uppercase tracking-wider text-[#475569]">
            Company
            <Phosphor.ArrowsDownUp size={11} weight="bold" class="text-[#94a3b8]" aria-hidden="true" />
          </button>
        </th>
        <th scope="col" class="px-4 py-3 text-left">
          <button class="inline-flex items-center gap-1 font-medium text-[12px] uppercase tracking-wider text-[#475569]">
            Value
            <Phosphor.ArrowsDownUp size={11} weight="bold" class="text-[#94a3b8]" aria-hidden="true" />
          </button>
        </th>
        <th scope="col" class="px-4 py-3 text-left">
          <button class="inline-flex items-center gap-1 font-medium text-[12px] uppercase tracking-wider text-[#475569]">
            Stage
            <Phosphor.ArrowsDownUp size={11} weight="bold" class="text-[#94a3b8]" aria-hidden="true" />
          </button>
        </th>
        <th scope="col" class="px-4 py-3 text-right w-12"></th>
      </tr>
    </thead>
    <tbody>
      {deals.map(deal => (
        <tr key={deal.id} class="border-b border-[#e2e8f0] hover:bg-[#f8fafc] focus-within:bg-[#eef2ff] transition-colors duration-150">
          <td class="px-4 py-3">
            <input type="checkbox" aria-label={`Select ${deal.name}`} />
          </td>
          <td class="px-4 py-3 font-medium text-[14px] text-[#0f172a]">
            <a href={`/deals/${deal.id}`} class="hover:text-[#4f46e5] focus-visible:outline-2 focus-visible:outline-[#4f46e5] focus-visible:outline-offset-2 rounded">
              {deal.name}
            </a>
          </td>
          <td class="px-4 py-3 text-[13px] text-[#475569] inline-flex items-center gap-1.5">
            <Phosphor.Buildings size={14} weight="regular" class="text-[#94a3b8]" aria-hidden="true" />
            {deal.company}
          </td>
          <td class="px-4 py-3 text-[14px] tabular-nums text-[#0f172a] text-right font-medium">
            {formatCurrency(deal.value)}
          </td>
          <td class="px-4 py-3">
            <span class={cn(
              'inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium uppercase tracking-wider',
              stageStyles[deal.stage]
            )}>
              {stageIcons[deal.stage]}
              {deal.stage}
            </span>
          </td>
          <td class="px-4 py-3 text-right">
            <button
              type="button"
              aria-label={`Actions for ${deal.name}`}
              class="text-[#94a3b8] hover:text-[#0f172a] rounded"
            >
              <Phosphor.DotsThreeVertical size={14} weight="bold" aria-hidden="true" />
            </button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```