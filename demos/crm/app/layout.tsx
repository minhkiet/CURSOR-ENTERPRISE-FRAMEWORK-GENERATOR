import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Northwind CRM — Chốt deal nhanh hơn 47%',
  description: 'CRM platform cho sales rep Việt Nam. Pipeline visibility, workflow automation, advanced reporting. Dùng thử 14 ngày miễn phí.',
  keywords: ['CRM', 'CRM Việt Nam', 'sales pipeline', 'pipeline management', 'doanh nghiệp'],
  openGraph: {
    title: 'Northwind CRM — Chốt deal nhanh hơn 47%',
    description: '247+ doanh nghiệp Việt Nam đang dùng Northwind CRM để quản lý pipeline.',
    type: 'website',
    locale: 'vi_VN'
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className="bg-slate-50 antialiased">{children}</body>
    </html>
  );
}