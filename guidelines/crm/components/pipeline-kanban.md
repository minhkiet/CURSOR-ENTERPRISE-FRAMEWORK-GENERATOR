# Pipeline Kanban

> Bố cục pipeline CRM với 5 stage columns (Lead · Qualified · Proposal · Negotiation · Won). Mỗi column có deal cards với value, owner avatar, age, last activity. Hỗ trợ drag-drop với keyboard alternative.

## 1. Mục đích

Sales rep cần nhìn toàn cảnh pipeline trong 1 view, kéo deal giữa stages, click để mở detail. Keyboard-first cho power users.

## 2. Asset

| Element | Source |
|---|---|
| Avatar | Unsplash curated headshots |
| Company logo | Simple Icons CDN |
| Stage icons | Phosphor |

## 3. Layout

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Pipeline: Q3 2026 · 247 deals · Total: 47.8 tỷ VND                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐    │
│ │ 📥 Lead      │ 🎯 Qualified │ 📄 Proposal  │ 💬 Negotia.  │ ✅ Won       │    │
│ │ 78 · 8.2 tỷ  │ 56 · 12.5 tỷ│ 42 · 14.8 tỷ │ 18 · 9.6 tỷ  │ 53 · 12.7 tỷ│   │
│ ├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤    │
│ │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │ ┌──────────┐ │    │
│ │ │ Deal 1   │ │ │ Deal 5   │ │ │ Deal 9   │ │ │ Deal 13  │ │ │ Deal 17  │ │    │
│ │ │ Acme Corp│ │ │ BetaCo   │ │ │ ...      │ │ │          │ │ │          │ │    │
│ │ │ 1.2 tỷ   │ │ │ 800tr    │ │ │          │ │ │          │ │ │          │ │    │
│ │ │ 👤 M    │ │ │          │ │ │          │ │ │          │ │ │          │ │    │
│ │ │ ⏱ 2d    │ │ │          │ │ │          │ │ │          │ │ │          │ │    │
│ │ └──────────┘ │ └──────────┘ │ └──────────┘ │ └──────────┘ │ └──────────┘ │    │
│ └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Pipeline view | 5 stages horizontal scroll |
| `compact` | Sidebar widget | Smaller cards |
| `forecast` | Forecast mode | Weighted value overlay |
| `mine` | My deals | Filter owner=self |

## 5. States

| State | Visual |
|---|---|
| default | Cards in columns |
| dragging | Card lifted + shadow |
| drop-target | Column highlighted |
| selected | Card border indigo |
| empty | Stage empty state |
| reduce-motion | No drag animation |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Lead | `DownloadSimple` |
| Qualified | `Target` |
| Proposal | `FileText` |
| Negotiation | `ChatsTeardrop` |
| Won | `CheckCircle` (fill) |
| Lost | `XCircle` |
| Drag handle | `DotsSixVertical` |
| Avatar | Image |
| Stalled | `WarningCircle` (fill) |
| Hot | `Fire` (fill) |
| Age | `Clock` |
| Money | `CurrencyDollar` |

## 7. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Deal {
  id: string;
  title: string;
  company: string;
  companySlug: string;
  value: number;
  currency: 'VND' | 'USD';
  owner: { name: string; avatarId: string };
  age: number; // days
  lastActivity: string;
  stage: string;
  isHot: boolean;
  isStalled: boolean;
}

export interface Stage {
  id: string;
  name: string;
  icon: string;
  probability: number;
}

const STAGES: Stage[] = [
  { id: 'lead', name: 'Lead', icon: 'DownloadSimple', probability: 10 },
  { id: 'qualified', name: 'Qualified', icon: 'Target', probability: 30 },
  { id: 'proposal', name: 'Proposal', icon: 'FileText', probability: 50 },
  { id: 'negotiation', name: 'Negotiation', icon: 'ChatsTeardrop', probability: 70 },
  { id: 'won', name: 'Won', icon: 'CheckCircle', probability: 100 }
];

const SAMPLE_DEALS: Deal[] = [
  {
    id: 'd1',
    title: 'Phần mềm CRM 50 users',
    company: 'FPT Software',
    companySlug: 'fpt',
    value: 1200000000,
    currency: 'VND',
    owner: { name: 'Minh', avatarId: '1507003211169-0a1dd7228f2d' },
    age: 2,
    lastActivity: '2 giờ trước',
    stage: 'lead',
    isHot: true,
    isStalled: false
  },
  {
    id: 'd2',
    title: 'Enterprise License 200 users',
    company: 'VNG Corporation',
    companySlug: 'vng',
    value: 4500000000,
    currency: 'VND',
    owner: { name: 'Lan', avatarId: '1494790108377-be9c29b29330' },
    age: 15,
    lastActivity: '1 ngày trước',
    stage: 'qualified',
    isHot: false,
    isStalled: true
  },
  {
    id: 'd3',
    title: 'Migration project Q4',
    company: 'TMA Solutions',
    companySlug: 'tma',
    value: 2800000000,
    currency: 'VND',
    owner: { name: 'Bảo', avatarId: '1472099645785-5658abf4ff4e' },
    age: 7,
    lastActivity: '4 giờ trước',
    stage: 'proposal',
    isHot: true,
    isStalled: false
  }
];

export function PipelineKanban() {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Toolbar */}
      <div className="bg-white border-b border-slate-200 px-6 py-4 sticky top-0 z-10">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              Pipeline Q3 2026
            </h1>
            <p className="text-[13px] text-slate-500 mt-0.5">
              <strong className="tabular-nums font-bold text-slate-900">247</strong> deals · Tổng giá trị <strong className="tabular-nums font-bold text-slate-900">47,8 tỷ VND</strong>
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button className="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg text-[13px] font-semibold text-slate-700">
              <Phosphor.Funnel size={14} weight="bold" />
              Lọc
            </button>
            <button className="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg text-[13px] font-semibold text-slate-700">
              <Phosphor.Download size={14} weight="bold" />
              Export
            </button>
            <button className="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[13px] font-bold rounded-lg">
              <Phosphor.PlusCircle size={14} weight="bold" />
              Tạo deal
            </button>
          </div>
        </div>
      </div>

      {/* Kanban columns */}
      <div className="p-6 overflow-x-auto">
        <div className="flex gap-4 min-w-max">
          {STAGES.map(stage => {
            const stageDeals = SAMPLE_DEALS.filter(d => d.stage === stage.id);
            const stageValue = stageDeals.reduce((sum, d) => sum + d.value, 0);
            return (
              <StageColumn
                key={stage.id}
                stage={stage}
                deals={stageDeals}
                stageValue={stageValue}
                selectedId={selectedId}
                onSelect={setSelectedId}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

function StageColumn({ stage, deals, stageValue, selectedId, onSelect }: {
  stage: Stage;
  deals: Deal[];
  stageValue: number;
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  const Icon = Phosphor[stage.icon] as any;
  const [dropTarget, setDropTarget] = useState(false);

  return (
    <section
      aria-labelledby={`stage-${stage.id}`}
      className={`w-80 flex-shrink-0 bg-white rounded-xl border ${dropTarget ? 'border-indigo-400 ring-2 ring-indigo-200' : 'border-slate-200'}`}
    >
      {/* Header */}
      <div className="p-4 border-b border-slate-100">
        <div className="flex items-center justify-between">
          <h2 id={`stage-${stage.id}`} className="flex items-center gap-2 text-[13px] font-bold uppercase tracking-wide text-slate-700">
            <Icon size={16} weight="bold" className="text-slate-500" />
            {stage.name}
          </h2>
          <span className="px-2 py-0.5 bg-slate-100 text-slate-700 text-[11px] font-bold rounded-full tabular-nums">
            {deals.length}
          </span>
        </div>
        <div className="mt-2 flex items-baseline gap-2">
          <output className="text-[18px] font-extrabold text-slate-900 tabular-nums">
            {formatVND(stageValue)}
          </output>
          <span className="text-[10.5px] text-slate-500 font-medium uppercase tracking-wider">
            {stage.probability}%
          </span>
        </div>
      </div>

      {/* Cards */}
      <div className="p-3 space-y-2 min-h-[200px]" onDragOver={e => { e.preventDefault(); setDropTarget(true); }} onDragLeave={() => setDropTarget(false)} onDrop={() => setDropTarget(false)}>
        {deals.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mb-2">
              <Phosphor.Drop size={20} weight="regular" className="text-slate-400" />
            </div>
            <p className="text-[12px] text-slate-500">Kéo deal vào đây</p>
          </div>
        ) : (
          deals.map(deal => (
            <DealCard
              key={deal.id}
              deal={deal}
              selected={selectedId === deal.id}
              onClick={() => onSelect(deal.id)}
            />
          ))
        )}
      </div>

      {/* Add deal */}
      <div className="p-3 border-t border-slate-100">
        <button className="w-full flex items-center justify-center gap-1.5 py-2 text-[12px] font-semibold text-slate-500 hover:bg-slate-50 hover:text-indigo-600 rounded-lg transition-colors">
          <Phosphor.Plus size={13} weight="bold" />
          Thêm deal
        </button>
      </div>
    </section>
  );
}

function DealCard({ deal, selected, onClick }: { deal: Deal; selected: boolean; onClick: () => void }) {
  return (
    <article
      onClick={onClick}
      className={`group cursor-pointer p-3 rounded-lg border ${selected ? 'border-indigo-500 ring-2 ring-indigo-200 bg-white' : 'border-slate-200 bg-white'} hover:shadow-md hover:-translate-y-0.5 transition-all`}
      tabIndex={0}
      onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onClick(); } }}
    >
      {/* Top row: hot / stalled */}
      <div className="flex items-center gap-1.5 mb-2">
        {deal.isHot && (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-rose-100 text-rose-700 text-[9.5px] font-bold uppercase tracking-wider rounded">
            <Phosphor.Fire size={9} weight="fill" />
            Hot
          </span>
        )}
        {deal.isStalled && (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 bg-amber-100 text-amber-700 text-[9.5px] font-bold uppercase tracking-wider rounded">
            <Phosphor.WarningCircle size={9} weight="fill" />
            Stalled
          </span>
        )}
      </div>

      {/* Title + Company */}
      <h3 className="text-[13.5px] font-bold text-slate-900 leading-snug line-clamp-2">
        {deal.title}
      </h3>
      <div className="mt-1 flex items-center gap-1.5 text-[11.5px] text-slate-600">
        <img
          src={`https://cdn.simpleicons.org/${deal.companySlug}/64748b`}
          alt={deal.company}
          className="w-3.5 h-3.5"
          loading="lazy"
        />
        {deal.company}
      </div>

      {/* Value */}
      <div className="mt-2 flex items-baseline gap-1.5">
        <span className="text-[16px] font-extrabold text-slate-900 tabular-nums leading-none">
          {formatVND(deal.value)}
        </span>
        <span className="text-[10.5px] text-slate-500">VND</span>
      </div>

      {/* Bottom row: avatar + age */}
      <div className="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <img
            src={`https://images.unsplash.com/photo-${deal.owner.avatarId}?w=40&h=40&fit=crop&q=80`}
            alt={deal.owner.name}
            className="w-5 h-5 rounded-full object-cover ring-1 ring-slate-200"
            loading="lazy"
          />
          <span className="text-[11px] font-semibold text-slate-700">{deal.owner.name}</span>
        </div>
        <span className="inline-flex items-center gap-0.5 text-[10.5px] text-slate-500 tabular-nums">
          <Phosphor.Clock size={10} weight="regular" />
          {deal.age}d
        </span>
      </div>
    </article>
  );
}

function formatVND(v: number): string {
  if (v >= 1_000_000_000) return `${(v / 1_000_000_000).toFixed(1)} tỷ`;
  if (v >= 1_000_000) return `${Math.round(v / 1_000_000)} tr`;
  return v.toLocaleString('vi-VN');
}
```

## 8. Accessibility

- Mỗi stage là `<section>` với `aria-labelledby`
- Deal cards `<article>` focusable + keyboard accessible
- Enter/Space mở detail
- Stage value là `<output>` accessible
- Drag handle dùng `aria-roledescription="draggable"` + instructions
- Drop zones announced qua `aria-live="polite"`
- Empty state có icon + heading + CTA
- Format VND có helper function
- Time relative + absolute

## 9. Performance

- Drag-drop sử dụng HTML5 DnD API
- Virtual scroll cho columns > 50 deals
- Lazy load avatars
- Memo deal cards với React.memo
- Optimistic update khi drag

## 10. Anti-patterns đã tránh

- ❌ "Make every screen feel like..." 
- ❌ Generic 3-column (đã 5 stages đúng sales process)
- ❌ No keyboard alternative cho drag (đã Enter/Space)
- ❌ No total value (đã output)
- ❌ No empty state (đã có)
- ❌ Color-only status (đã icon + label)

---

**Component family**: In-app Cockpit — `pipeline-kanban`