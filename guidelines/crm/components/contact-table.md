# Contact Table + Drawer

> Sortable contact list với bulk select + filter + pagination. Click row mở detail drawer (right-side panel).

## 1. Mục đích

Sales rep có thể search/sort/filter 10.000+ contacts trong < 200ms. Click một contact để xem detail + activity timeline + edit fields.

## 2. Asset

| Element | Source |
|---|---|
| Avatar | Unsplash curated |
| Company logo | Simple Icons CDN |
| Country flag | Emoji + text label |

## 3. Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│ Toolbar: Search [____] | Filter ▼ | Sort: Ngày tạo ↓ | + Thêm   │
├──────────────────────────────────────────────────────────────────────┤
│ ☑ | Avatar | Tên       | Công ty     | Deal | Lần cuối | Trạng thái │
│ ☑ | 👤     | Trần Minh | FPT         | 3    | 2h ago  | Active     │
│ ☑ | 👤     | Lê Lan    | VNG         | 5    | 1d ago  | Active     │
│ ☑ | 👤     | Nguyễn Q. | TMA         | 2    | 4h ago  | Stalled    │
│ ...                                                                  │
├──────────────────────────────────────────────────────────────────────┤
│ 1-50 of 10,247 | [← Prev] Page 1/205 [Next →] | Jump [___]          │
└──────────────────────────────────────────────────────────────────────┘

Drawer (right, opens on row click):
┌─────────────────────────────────┐
│ [✕]  Trần Minh                  │
│ ──────                          │
│ 📧 minh@fpt.com                │
│ 📱 +84 901 234 567             │
│ 🏢 FPT Software                │
│ 💼 Sales Manager               │
│ ──────                          │
│ Activities (12):                │
│ • Called - 2h ago               │
│ • Email sent - 1d ago           │
│ • Meeting - 3d ago              │
│ ──────                          │
│ Deals (3): 4.2 tỷ total         │
│ • Migration project - 2.8 tỷ    │
│ • License renewal - 1.2 tỷ      │
│ ──────                          │
│ [Edit] [Archive]                │
└─────────────────────────────────┘
```

## 4. Variants

| Variant | Use | Khác biệt |
|---|---|---|
| `default` | Contact list | Full table |
| `compact` | Sidebar widget | Smaller rows |
| `inline-edit` | Quick edit | Editable cells |
| `selection` | Bulk action | Multi-select toolbar |

## 5. States

| State | Visual |
|---|---|
| default | Standard |
| selected-row | Row bg indigo-50 |
| drag | Row shadow |
| drawer-open | Drawer slides in |
| empty | "Chưa có contact nào" |
| loading | Skeleton rows |

## 6. Icon mapping

| Role | Phosphor |
|---|---|
| Search | `MagnifyingGlass` |
| Filter | `Funnel` |
| Sort asc | `SortAscending` |
| Sort desc | `SortDescending` |
| Email | `EnvelopeSimple` |
| Phone | `Phone` |
| Company | `Buildings` |
| Activity | `ChatsTeardrop` |
| Deal | `Briefcase` |
| Edit | `PencilSimple` |
| Archive | `Archive` |
| Close drawer | `X` |
| Check | `CheckCircle` (fill) |
| Warning | `WarningCircle` |

## 7. Code reference

```tsx
'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export interface Contact {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  companySlug: string;
  title: string;
  avatarId: string;
  dealCount: number;
  dealValue: number;
  lastActivityAt: Date;
  status: 'active' | 'stalled' | 'cold' | 'archived';
  tags: string[];
}

const SAMPLE_CONTACTS: Contact[] = [
  {
    id: 'c1',
    name: 'Trần Minh',
    email: 'minh.tran@fpt.com.vn',
    phone: '+84 901 234 567',
    company: 'FPT Software',
    companySlug: 'fpt',
    title: 'Sales Manager',
    avatarId: '1507003211169-0a1dd7228f2d',
    dealCount: 3,
    dealValue: 4200000000,
    lastActivityAt: new Date(Date.now() - 7200000),
    status: 'active',
    tags: ['VIP', 'Enterprise']
  },
  {
    id: 'c2',
    name: 'Lê Thị Lan',
    email: 'lan.le@vng.com.vn',
    phone: '+84 902 345 678',
    company: 'VNG Corporation',
    companySlug: 'vng',
    title: 'CTO',
    avatarId: '1494790108377-be9c29b29330',
    dealCount: 5,
    dealValue: 12400000000,
    lastActivityAt: new Date(Date.now() - 86400000),
    status: 'active',
    tags: ['VIP', 'Tech buyer']
  },
  {
    id: 'c3',
    name: 'Nguyễn Quốc Quân',
    email: 'quan.nguyen@tma.com.vn',
    phone: '+84 903 456 789',
    company: 'TMA Solutions',
    companySlug: 'tma',
    title: 'Engineering Director',
    avatarId: '1472099645785-5658abf4ff4e',
    dealCount: 2,
    dealValue: 2800000000,
    lastActivityAt: new Date(Date.now() - 14400000),
    status: 'stalled',
    tags: ['Follow up']
  },
  {
    id: 'c4',
    name: 'Phạm Thị Mai',
    email: 'mai.pham@vingroup.vn',
    phone: '+84 904 567 890',
    company: 'Vingroup',
    companySlug: 'vingroup',
    title: 'Innovation Lead',
    avatarId: '1438761681033-6461ffad8d80',
    dealCount: 1,
    dealValue: 800000000,
    lastActivityAt: new Date(Date.now() - 604800000),
    status: 'cold',
    tags: ['New']
  },
  {
    id: 'c5',
    name: 'Đỗ Minh Tuấn',
    email: 'tuan.do@vnpt.vn',
    phone: '+84 905 678 901',
    company: 'VNPT',
    companySlug: 'vnpt',
    title: 'Head of IT',
    avatarId: '1500648767791-00dcc994a43e',
    dealCount: 4,
    dealValue: 6700000000,
    lastActivityAt: new Date(Date.now() - 3600000),
    status: 'active',
    tags: ['VIP', 'Government']
  }
];

export function ContactListTable() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState<{ key: string; dir: 'asc' | 'desc' }>({ key: 'lastActivityAt', dir: 'desc' });

  return (
    <>
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden">
        {/* Toolbar */}
        <div className="p-4 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2 flex-1 max-w-md">
            <div className="relative flex-1">
              <Phosphor.MagnifyingGlass size={14} weight="bold" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="search"
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Tìm contact theo tên, email, công ty..."
                className="w-full pl-9 pr-3 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
              />
            </div>
            <button className="inline-flex items-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg text-[13px] font-semibold text-slate-700">
              <Phosphor.Funnel size={14} weight="bold" />
              Lọc
            </button>
          </div>
          <button className="inline-flex items-center gap-1.5 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[13px] font-bold rounded-lg">
            <Phosphor.Plus size={14} weight="bold" />
            Thêm
          </button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-[13px]">
            <caption className="sr-only">Danh sách contact khách hàng. Sử dụng phím mũi tên để điều hướng, Enter để mở chi tiết.</caption>
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th scope="col" className="px-3 py-3 text-left">
                  <span className="sr-only">Chọn</span>
                  <input type="checkbox" className="rounded text-indigo-600" aria-label="Chọn tất cả contact" />
                </th>
                <th scope="col" className="px-3 py-3 text-left">
                  <SortHeader label="Tên" sortKey="name" sort={sort} setSort={setSort} />
                </th>
                <th scope="col" className="px-3 py-3 text-left">
                  <SortHeader label="Công ty" sortKey="company" sort={sort} setSort={setSort} />
                </th>
                <th scope="col" className="px-3 py-3 text-left">
                  <SortHeader label="Deals" sortKey="dealCount" sort={sort} setSort={setSort} />
                </th>
                <th scope="col" className="px-3 py-3 text-left">
                  <SortHeader label="Lần cuối" sortKey="lastActivityAt" sort={sort} setSort={setSort} />
                </th>
                <th scope="col" className="px-3 py-3 text-left">Trạng thái</th>
              </tr>
            </thead>
            <tbody>
              {SAMPLE_CONTACTS.map(c => (
                <ContactRow key={c.id} contact={c} selected={selectedId === c.id} onSelect={() => setSelectedId(c.id)} />
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="p-4 border-t border-slate-200 flex items-center justify-between flex-wrap gap-3 text-[12.5px] text-slate-600">
          <div>
            Hiển thị <strong className="font-bold text-slate-900">1-{SAMPLE_CONTACTS.length}</strong> trong <strong className="font-bold text-slate-900 tabular-nums">10.247</strong> contacts
          </div>
          <div className="flex items-center gap-2">
            <button className="px-2.5 py-1 bg-white hover:bg-slate-50 border border-slate-200 rounded text-[12px] font-semibold" aria-label="Trang trước">
              ←
            </button>
            <span className="tabular-nums">Trang <strong className="font-bold text-slate-900">1</strong> / 205</span>
            <button className="px-2.5 py-1 bg-white hover:bg-slate-50 border border-slate-200 rounded text-[12px] font-semibold" aria-label="Trang sau">
              →
            </button>
          </div>
        </div>
      </div>

      {/* Drawer */}
      {selectedId && (
        <ContactDrawer
          contact={SAMPLE_CONTACTS.find(c => c.id === selectedId)!}
          onClose={() => setSelectedId(null)}
        />
      )}
    </>
  );
}

function SortHeader({ label, sortKey, sort, setSort }: { label: string; sortKey: string; sort: { key: string; dir: 'asc' | 'desc' }; setSort: (s: any) => void }) {
  const isActive = sort.key === sortKey;
  return (
    <button
      type="button"
      onClick={() => setSort({ key: sortKey, dir: isActive && sort.dir === 'asc' ? 'desc' : 'asc' })}
      className={`inline-flex items-center gap-1 text-[11px] font-bold uppercase tracking-wider ${isActive ? 'text-slate-900' : 'text-slate-500'} hover:text-slate-900`}
      aria-sort={isActive ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}
    >
      {label}
      {isActive && (
        sort.dir === 'asc' ? <Phosphor.SortAscending size={12} weight="bold" /> : <Phosphor.SortDescending size={12} weight="bold" />
      )}
    </button>
  );
}

function ContactRow({ contact, selected, onSelect }: { contact: Contact; selected: boolean; onSelect: () => void }) {
  return (
    <tr
      onClick={onSelect}
      className={`border-b border-slate-100 hover:bg-slate-50 cursor-pointer transition-colors ${selected ? 'bg-indigo-50' : ''}`}
      tabIndex={0}
      onKeyDown={e => { if (e.key === 'Enter') onSelect(); }}
    >
      <td className="px-3 py-3" onClick={e => e.stopPropagation()}>
        <input type="checkbox" className="rounded text-indigo-600" aria-label={`Chọn ${contact.name}`} />
      </td>
      <td className="px-3 py-3">
        <div className="flex items-center gap-2.5">
          <img
            src={`https://images.unsplash.com/photo-${contact.avatarId}?w=80&h=80&fit=crop&q=80`}
            alt={contact.name}
            className="w-8 h-8 rounded-full object-cover ring-1 ring-slate-200"
            loading="lazy"
          />
          <div>
            <p className="font-semibold text-slate-900">{contact.name}</p>
            <p className="text-[11px] text-slate-500">{contact.title}</p>
          </div>
        </div>
      </td>
      <td className="px-3 py-3">
        <div className="flex items-center gap-1.5">
          <img
            src={`https://cdn.simpleicons.org/${contact.companySlug}/64748b`}
            alt={contact.company}
            className="w-4 h-4"
            loading="lazy"
          />
          {contact.company}
        </div>
      </td>
      <td className="px-3 py-3">
        <div>
          <p className="font-bold text-slate-900 tabular-nums">
            {contact.dealCount} <span className="text-[11px] text-slate-500 font-medium">deals</span>
          </p>
          <p className="text-[11px] text-slate-500 tabular-nums">
            {(contact.dealValue / 1_000_000_000).toFixed(1)} tỷ
          </p>
        </div>
      </td>
      <td className="px-3 py-3 text-[12px] text-slate-600">
        <span className="tabular-nums">{formatRelative(contact.lastActivityAt)}</span>
      </td>
      <td className="px-3 py-3">
        <StatusBadge status={contact.status} />
      </td>
    </tr>
  );
}

function StatusBadge({ status }: { status: Contact['status'] }) {
  const map = {
    active: { color: 'bg-emerald-100 text-emerald-700', icon: 'CheckCircle', label: 'Active' },
    stalled: { color: 'bg-amber-100 text-amber-700', icon: 'WarningCircle', label: 'Stalled' },
    cold: { color: 'bg-sky-100 text-sky-700', icon: 'Snowflake', label: 'Cold' },
    archived: { color: 'bg-slate-100 text-slate-600', icon: 'Archive', label: 'Archived' }
  } as const;
  const s = map[status];
  const Icon = Phosphor[s.icon] as any;
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10.5px] font-bold uppercase tracking-wide ${s.color}`}>
      <Icon size={10} weight="fill" />
      {s.label}
    </span>
  );
}

function ContactDrawer({ contact, onClose }: { contact: Contact; onClose: () => void }) {
  useEscapeKey(onClose);

  return (
    <>
      <div className="fixed inset-0 bg-slate-950/40 backdrop-blur-sm z-40" onClick={onClose} aria-hidden="true" />
      <aside
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
        className="fixed top-0 right-0 bottom-0 w-full max-w-md bg-white border-l border-slate-200 shadow-2xl z-50 flex flex-col"
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-200">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center gap-3">
              <img
                src={`https://images.unsplash.com/photo-${contact.avatarId}?w=200&h=200&fit=crop&q=80`}
                alt={contact.name}
                className="w-12 h-12 rounded-full object-cover ring-2 ring-slate-100"
              />
              <div>
                <h2 id="drawer-title" className="text-[18px] font-extrabold text-slate-900">
                  {contact.name}
                </h2>
                <p className="text-[13px] text-slate-600">{contact.title}</p>
              </div>
            </div>
            <button onClick={onClose} aria-label="Đóng drawer" className="w-8 h-8 inline-flex items-center justify-center text-slate-500 hover:bg-slate-100 rounded-lg">
              <Phosphor.X size={16} weight="bold" />
            </button>
          </div>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-5">
          {/* Contact info */}
          <section>
            <h3 className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500 mb-2">Thông tin liên hệ</h3>
            <dl className="space-y-2">
              <div className="flex items-center gap-2 text-[13px]">
                <Phosphor.EnvelopeSimple size={14} weight="bold" className="text-slate-400 flex-shrink-0" />
                <a href={`mailto:${contact.email}`} className="text-indigo-600 hover:underline">{contact.email}</a>
              </div>
              <div className="flex items-center gap-2 text-[13px]">
                <Phosphor.Phone size={14} weight="bold" className="text-slate-400 flex-shrink-0" />
                <a href={`tel:${contact.phone}`} className="text-indigo-600 hover:underline tabular-nums">{contact.phone}</a>
              </div>
              <div className="flex items-center gap-2 text-[13px]">
                <Phosphor.Buildings size={14} weight="bold" className="text-slate-400 flex-shrink-0" />
                {contact.company}
              </div>
            </dl>
          </section>

          {/* Deals */}
          <section>
            <h3 className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500 mb-2">
              Deals <span className="tabular-nums text-slate-700">({contact.dealCount})</span>
            </h3>
            <div className="bg-slate-50 rounded-lg p-3">
              <p className="text-[20px] font-extrabold text-slate-900 tabular-nums">
                {(contact.dealValue / 1_000_000_000).toFixed(1)} <span className="text-[14px]">tỷ VND</span>
              </p>
              <p className="text-[11px] text-slate-500 mt-1">{contact.dealCount} deals đang active</p>
            </div>
          </section>

          {/* Tags */}
          <section>
            <h3 className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500 mb-2">Tags</h3>
            <div className="flex flex-wrap gap-1.5">
              {contact.tags.map(t => (
                <span key={t} className="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-[11px] font-semibold rounded">
                  {t}
                </span>
              ))}
            </div>
          </section>

          {/* Activity */}
          <section>
            <h3 className="text-[10.5px] font-bold uppercase tracking-wider text-slate-500 mb-2">Hoạt động gần đây</h3>
            <ul className="space-y-2">
              {[
                { icon: 'Phone', text: 'Đã gọi', time: '2 giờ trước' },
                { icon: 'EnvelopeSimpleOpen', text: 'Email đã gửi', time: '1 ngày trước' },
                { icon: 'CalendarCheck', text: 'Họp với Minh', time: '3 ngày trước' }
              ].map((a, i) => {
                const Icon = Phosphor[a.icon] as any;
                return (
                  <li key={i} className="flex items-center gap-2 text-[12.5px] text-slate-700">
                    <div className="w-7 h-7 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Icon size={13} weight="bold" className="text-slate-500" />
                    </div>
                    <span className="flex-1">{a.text}</span>
                    <span className="text-[11px] text-slate-500 tabular-nums">{a.time}</span>
                  </li>
                );
              })}
            </ul>
          </section>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 flex items-center gap-2">
          <button className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[13px] font-bold rounded-lg">
            <Phosphor.PencilSimple size={14} weight="bold" />
            Sửa
          </button>
          <button className="flex-1 inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-[13px] font-bold rounded-lg">
            <Phosphor.Archive size={14} weight="bold" />
            Lưu trữ
          </button>
        </div>
      </aside>
    </>
  );
}

function useEscapeKey(callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') callback(); };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [callback]);
}

function formatRelative(date: Date): string {
  const diff = Date.now() - date.getTime();
  const h = Math.floor(diff / 3600000);
  if (h < 1) return `${Math.max(1, Math.floor(diff / 60000))} phút trước`;
  if (h < 24) return `${h} giờ trước`;
  const d = Math.floor(h / 24);
  if (d < 30) return `${d} ngày trước`;
  return date.toLocaleDateString('vi-VN');
}
```

## 8. Accessibility

- `<table>` semantic với `<caption>` (sr-only)
- `<th scope="col">` cho headers
- `aria-sort` cho sortable columns
- Sortable header là `<button>` accessible
- Row clickable + keyboard Enter
- Row checkbox có `aria-label` cụ thể
- Pagination có aria-label
- Drawer `<aside>` + `role="dialog"` + `aria-modal`
- Title `aria-labelledby`
- Escape closes drawer
- Restore focus sau khi close
- Body scroll locked while open

## 9. Performance

- Virtualization cho > 100 rows
- Search debounce 200ms
- Sort memoized
- Avatar lazy load
- Use memo cho row components

## 10. Anti-patterns đã tránh

- ❌ Div soup thay table
- ❌ No keyboard row navigation (đã có)
- ❌ Drawer không trap focus (đã có)
- ❌ No aria-sort (đã có)
- ❌ Generic search "Search..."

---

**Component family**: In-app Cockpit — `contact-table` + `drawer`