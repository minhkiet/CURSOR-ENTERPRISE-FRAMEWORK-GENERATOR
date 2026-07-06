import * as Phosphor from '@phosphor-icons/react';

export interface Integration {
  slug: string;
  name: string;
  description: string;
}

export const INTEGRATIONS: Integration[] = [
  { slug: 'slack', name: 'Slack', description: 'Channel notifications' },
  { slug: 'gmail', name: 'Gmail', description: 'Email sync' },
  { slug: 'microsoft', name: 'Outlook', description: 'Office 365' },
  { slug: 'zoom', name: 'Zoom', description: 'Meeting links' },
  { slug: 'google', name: 'Google Calendar', description: 'Event sync 2 chiều' },
  { slug: 'misa', name: 'MISA', description: 'Invoice + accounting' },
  { slug: 'hubspot', name: 'HubSpot', description: 'CRM migration' },
  { slug: 'pipedrive', name: 'Pipedrive', description: 'Import deals' },
  { slug: 'zapier', name: 'Zapier', description: '5.000+ apps' },
  { slug: 'jira', name: 'Jira', description: 'Task from deal' },
  { slug: 'quickbooks', name: 'QuickBooks', description: 'Revenue sync' },
  { slug: 'trello', name: 'Trello', description: 'Project boards' }
];

export function IntegrationsSection() {
  return (
    <section className="bg-slate-50 py-16 lg:py-20 border-y border-slate-200" aria-labelledby="integrations-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <span className="inline-block text-[11px] font-bold uppercase tracking-[0.18em] text-indigo-600 mb-2">
            Tích hợp
          </span>
          <h2 id="integrations-heading" className="text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight">
            Kết nối với công cụ bạn đang dùng
          </h2>
          <p className="mt-3 text-[15px] text-slate-600 max-w-2xl mx-auto">
            Native integration với 47+ công cụ phổ biến. Không cần code. Setup trong 5 phút.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 lg:gap-4 mb-8">
          {INTEGRATIONS.map(integration => (
            <article
              key={integration.slug}
              className="group bg-white border border-slate-200 rounded-xl p-4 hover:shadow-card-lift hover:-translate-y-0.5 transition-all text-center"
            >
              <div className="w-12 h-12 mx-auto mb-3">
                <img
                  src={`https://cdn.simpleicons.org/${integration.slug}/64748b`}
                  alt={integration.name}
                  className="w-full h-full object-contain group-hover:scale-110 transition-transform"
                  loading="lazy"
                />
              </div>
              <p className="text-[13px] font-bold text-slate-900">{integration.name}</p>
              <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-1">{integration.description}</p>
            </article>
          ))}
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 text-[13px]">
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 text-indigo-700 rounded-full font-bold">
            <Phosphor.Plugs size={13} weight="bold" />
            47+ tích hợp
          </div>
          <a href="/docs/api" className="inline-flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-lg transition-colors">
            API Documentation
            <Phosphor.ArrowRight size={12} weight="bold" />
          </a>
          <a href="/request-integration" className="inline-flex items-center gap-1.5 px-4 py-2 border border-slate-300 hover:border-indigo-500 text-slate-700 hover:text-indigo-700 font-semibold rounded-lg transition-colors">
            Request integration
            <Phosphor.Plus size={12} weight="bold" />
          </a>
        </div>
      </div>
    </section>
  );
}