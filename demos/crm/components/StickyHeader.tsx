'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export function StickyHeader() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white/85 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <a href="#" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <Phosphor.Compass size={18} weight="fill" className="text-white" />
            </div>
            <span className="text-[16px] font-extrabold text-slate-900">Northwind</span>
            <span className="hidden sm:inline-block ml-1 text-[10.5px] font-bold uppercase tracking-wider text-slate-400 border-l border-slate-200 pl-2">CRM</span>
          </a>

          <nav className="hidden lg:flex items-center gap-7 text-[13px] font-semibold text-slate-700">
            <a href="#features" className="hover:text-indigo-600">Sản phẩm</a>
            <a href="#dashboard" className="hover:text-indigo-600">Dashboard</a>
            <a href="#pricing" className="hover:text-indigo-600">Bảng giá</a>
            <a href="#testimonials" className="hover:text-indigo-600">Khách hàng</a>
            <a href="#" className="hover:text-indigo-600">Tài nguyên</a>
          </nav>

          <div className="hidden lg:flex items-center gap-2">
            <a href="/login" className="px-3 py-2 text-[13px] font-semibold text-slate-700 hover:text-indigo-600">Đăng nhập</a>
            <a href="/signup" className="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-[13px] font-bold rounded-lg">
              Dùng thử miễn phí
            </a>
          </div>

          <button onClick={() => setOpen(!open)} className="lg:hidden w-10 h-10 inline-flex items-center justify-center text-slate-700" aria-label="Menu">
            <Phosphor.List size={20} weight="bold" />
          </button>
        </div>
      </div>

      {open && (
        <div className="lg:hidden border-t border-slate-200 bg-white">
          <nav className="px-4 py-3 space-y-1 text-[14px] font-semibold">
            <a href="#features" className="block px-3 py-2 text-slate-700 hover:bg-slate-50 rounded-lg">Sản phẩm</a>
            <a href="#dashboard" className="block px-3 py-2 text-slate-700 hover:bg-slate-50 rounded-lg">Dashboard</a>
            <a href="#pricing" className="block px-3 py-2 text-slate-700 hover:bg-slate-50 rounded-lg">Bảng giá</a>
            <a href="#testimonials" className="block px-3 py-2 text-slate-700 hover:bg-slate-50 rounded-lg">Khách hàng</a>
            <div className="pt-2 border-t border-slate-100 flex gap-2">
              <a href="/login" className="flex-1 py-2 text-center bg-slate-100 text-slate-700 rounded-lg">Đăng nhập</a>
              <a href="/signup" className="flex-1 py-2 text-center bg-indigo-600 text-white rounded-lg">Dùng thử</a>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}