import { Dumbbell, Phone, Mail, MapPin, ArrowRight, Globe, Heart, Lock, ShieldCheck, Apple, Instagram, Youtube } from 'lucide-react';

const COLUMNS = [
  {
    title: 'Chương trình',
    links: [
      { label: 'Push Pull Legs (PPL)', href: '/programs/ppl' },
      { label: 'StrongLifts 5×5', href: '/programs/stronglifts' },
      { label: 'Calisthenics Beginner', href: '/programs/calisthenics' },
      { label: 'Powerbuilding 4-day', href: '/programs/powerbuilding' },
      { label: 'Powerlifting', href: '/programs/powerlifting' },
      { label: 'Bodybuilding', href: '/programs/bodybuilding' },
      { label: 'Crossfit-style', href: '/programs/crossfit' }
    ]
  },
  {
    title: 'Thiết bị',
    links: [
      { label: 'Hướng dẫn mua tạ đòn', href: '/guides/barbell' },
      { label: 'Tạ đôi — Top 10', href: '/guides/dumbbells' },
      { label: 'Kettlebell', href: '/guides/kettlebell' },
      { label: 'Resistance band', href: '/guides/band' },
      { label: 'Cardio machines', href: '/guides/cardio' },
      { label: 'Yoga mat + foam roller', href: '/guides/recovery' },
      { label: 'Apple Watch + Garmin', href: '/guides/wearables' }
    ]
  },
  {
    title: 'Cộng đồng',
    links: [
      { label: 'Strava club', href: 'https://strava.com/clubs/ironpath' },
      { label: 'Forum', href: '/community' },
      { label: '1-1 Coaching', href: '/coaching' },
      { label: 'Podcast', href: '/podcast' },
      { label: 'YouTube channel', href: '/youtube' },
      { label: 'Local meetups', href: '/meetups' },
      { label: 'Charity events', href: '/events' }
    ]
  },
  {
    title: 'Pháp lý',
    links: [
      { label: 'Điều khoản dịch vụ', href: '/terms' },
      { label: 'Chính sách bảo mật', href: '/privacy' },
      { label: 'GDPR', href: '/gdpr' },
      { label: 'Cookie', href: '/cookies' },
      { label: 'Refund policy', href: '/refund' },
      { label: 'Liên hệ', href: '/contact' },
      { label: 'Báo lỗi', href: '/report' }
    ]
  }
];

export function MegaFooter() {
  return (
    <footer className="bg-ink-950 text-slate-300 border-t border-ink-800">
      <div className="bg-gradient-to-r from-electric-600 via-electric-500 to-electric-400 border-b border-electric-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-12">
          <div className="flex flex-wrap items-center justify-between gap-6">
            <div>
              <h2 className="text-2xl lg:text-3xl font-display text-ink-950 tracking-tight">
                Sẵn sàng squat 200kg?
              </h2>
              <p className="mt-1 text-ink-900/80 text-[14px] font-semibold">
                Tải app miễn phí · Đồng bộ Apple Watch · Strava · Garmin · Apple Health
              </p>
            </div>
            <div className="flex items-center gap-2 flex-wrap">
              <a href="#" className="inline-flex items-center gap-1.5 px-5 py-3 bg-ink-950 hover:bg-ink-900 text-electric-400 text-[13.5px] font-extrabold rounded-lg transition-colors" aria-label="Tải Ironpath trên App Store">
                <Apple size={16} strokeWidth={2.5} />
                App Store
              </a>
              <a href="/programs" className="inline-flex items-center gap-1.5 px-5 py-3 bg-electric-700 hover:bg-electric-800 text-white text-[13.5px] font-extrabold rounded-lg transition-colors">
                Xem 47 chương trình
                <ArrowRight size={14} strokeWidth={2.5} />
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 lg:gap-10">
          <div className="col-span-2 md:col-span-3 lg:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-9 h-9 bg-gradient-to-br from-electric-500 to-electric-700 rounded-lg flex items-center justify-center">
                <Dumbbell size={20} strokeWidth={2.5} className="text-ink-950" />
              </div>
              <span className="text-[18px] font-display text-ink-50">IRONPATH</span>
            </div>
            <p className="text-[12.5px] text-slate-400 leading-relaxed mb-4">
              Fitness tracker cho người Việt Nam tập gym nghiêm túc. Log workouts, theo dõi PR, đồng bộ Apple Watch + Strava + Garmin.
            </p>
            <div className="space-y-1.5 text-[12.5px]">
              <a href="tel:19006868" className="flex items-center gap-1.5 hover:text-electric-400 transition-colors">
                <Phone size={12} strokeWidth={2.5} />
                Hotline: 1900 6868
              </a>
              <a href="mailto:hello@ironpath.vn" className="flex items-center gap-1.5 hover:text-electric-400 transition-colors">
                <Mail size={12} strokeWidth={2.5} />
                hello@ironpath.vn
              </a>
              <p className="flex items-center gap-1.5 text-slate-400">
                <MapPin size={12} strokeWidth={2.5} />
                Tầng 8, Bitexco Tower, Quận 1, TP.HCM
              </p>
            </div>

            <div className="mt-5">
              <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2">Tải ứng dụng</p>
              <div className="flex items-center gap-2 flex-wrap">
                <a href="#" className="block h-10" aria-label="Tải trên App Store">
                  <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg" alt="App Store" className="h-10" loading="lazy" />
                </a>
                <a href="#" className="block h-10" aria-label="Tải trên Google Play">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play" className="h-10" loading="lazy" />
                </a>
                <a href="#" className="px-3 py-2 bg-ink-800 hover:bg-ink-700 text-ink-50 rounded-lg text-[11px] font-extrabold flex items-center gap-1.5 transition-colors" aria-label="Tải cho Apple Watch">
                  <Apple size={14} strokeWidth={2.5} />
                  Watch
                </a>
              </div>
            </div>
          </div>

          {COLUMNS.map(col => (
            <div key={col.title}>
              <h3 className="text-[12px] font-bold uppercase tracking-wider text-ink-50 mb-4">{col.title}</h3>
              <ul className="space-y-2">
                {col.links.map(link => (
                  <li key={link.label}>
                    <a href={link.href} className="text-[12.5px] text-slate-400 hover:text-electric-400 transition-colors">{link.label}</a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 pt-8 border-t border-ink-800 flex flex-wrap items-center justify-between gap-6">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-3">Tích hợp</p>
            <div className="flex items-center gap-2">
              {['strava', 'garmin', 'whoop', 'fitbit', 'spotify'].map(s => (
                <img key={s} src={`https://cdn.simpleicons.org/${s}/64748b`} alt={s} className="h-6 w-auto opacity-70 hover:opacity-100 transition-opacity" loading="lazy" />
              ))}
            </div>
          </div>

          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-3">Mạng xã hội fitness</p>
            <div className="flex items-center gap-2">
              <a href="#" aria-label="Instagram" className="w-9 h-9 inline-flex items-center justify-center bg-ink-800 hover:bg-electric-500 hover:text-ink-950 rounded-lg text-slate-300 transition-colors">
                <Instagram size={16} strokeWidth={2.5} />
              </a>
              <a href="#" aria-label="YouTube" className="w-9 h-9 inline-flex items-center justify-center bg-ink-800 hover:bg-electric-500 hover:text-ink-950 rounded-lg text-slate-300 transition-colors">
                <Youtube size={16} strokeWidth={2.5} />
              </a>
              <a href="#" aria-label="Strava" className="w-9 h-9 inline-flex items-center justify-center bg-ink-800 hover:bg-electric-500 hover:text-ink-950 rounded-lg text-slate-300 transition-colors">
                <span className="text-[10px] font-extrabold">S</span>
              </a>
              <a href="#" aria-label="TikTok" className="w-9 h-9 inline-flex items-center justify-center bg-ink-800 hover:bg-electric-500 hover:text-ink-950 rounded-lg text-slate-300 transition-colors">
                <span className="text-[10px] font-extrabold">T</span>
              </a>
            </div>
          </div>

          <div>
            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-3">Ngôn ngữ</p>
            <button className="px-3 py-2 bg-ink-800 hover:bg-ink-700 text-ink-50 rounded-lg text-[12px] font-extrabold flex items-center gap-1.5 transition-colors">
              <Globe size={13} strokeWidth={2.5} />
              Tiếng Việt ↓
            </button>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-ink-800 flex flex-wrap items-center justify-between gap-3 text-[11.5px] text-slate-500">
          <p>© 2026 Ironpath Vietnam. Mã số: <strong className="text-slate-400">0123456789</strong> cấp tại TP.HCM.</p>
          <div className="flex items-center gap-4 flex-wrap">
            <span className="inline-flex items-center gap-1.5"><Heart size={12} strokeWidth={0} fill="currentColor" className="text-rose-500" />HealthKit enabled</span>
            <span className="inline-flex items-center gap-1.5"><Lock size={12} strokeWidth={0} fill="currentColor" className="text-emerald-500" />End-to-end encrypted</span>
            <span className="inline-flex items-center gap-1.5"><ShieldCheck size={12} strokeWidth={0} fill="currentColor" className="text-emerald-500" />GDPR Compliant</span>
          </div>
        </div>
      </div>
    </footer>
  );
}