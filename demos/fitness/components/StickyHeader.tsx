'use client';
import { useState } from 'react';
import * as Phosphor from '@phosphor-icons/react';

export function StickyHeader() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-ink-950/85 backdrop-blur-md border-b border-ink-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <a href="#" className="flex items-center gap-2">
            <div className="w-9 h-9 bg-gradient-to-br from-electric-500 to-electric-700 rounded-lg flex items-center justify-center">
              <Phosphor.Barbell size={20} weight="fill" className="text-ink-950" />
            </div>
            <span className="text-[17px] font-display text-ink-50">IRONPATH</span>
          </a>

          <nav className="hidden lg:flex items-center gap-7 text-[13px] font-semibold text-slate-300">
            <a href="#features" className="hover:text-electric-400">Tính năng</a>
            <a href="#workout" className="hover:text-electric-400">Workout</a>
            <a href="#programs" className="hover:text-electric-400">Chương trình</a>
            <a href="#stats" className="hover:text-electric-400">PR & Volume</a>
            <a href="#" className="hover:text-electric-400">Cộng đồng</a>
          </nav>

          <div className="hidden lg:flex items-center gap-2">
            <a href="/login" className="px-3 py-2 text-[13px] font-semibold text-slate-300 hover:text-electric-400">Đăng nhập</a>
            <a href="/signup" className="inline-flex items-center gap-1.5 px-4 py-2 bg-electric-500 hover:bg-electric-400 text-ink-950 text-[13px] font-extrabold rounded-lg">
              <Phosphor.Download size={13} weight="bold" />
              Tải app
            </a>
          </div>

          <button onClick={() => setOpen(!open)} className="lg:hidden w-10 h-10 inline-flex items-center justify-center text-slate-300" aria-label="Menu">
            <Phosphor.List size={20} weight="bold" />
          </button>
        </div>
      </div>

      {open && (
        <div className="lg:hidden border-t border-ink-800 bg-ink-950">
          <nav className="px-4 py-3 space-y-1 text-[14px] font-semibold">
            <a href="#features" className="block px-3 py-2 text-slate-300 hover:bg-ink-800 rounded-lg">Tính năng</a>
            <a href="#workout" className="block px-3 py-2 text-slate-300 hover:bg-ink-800 rounded-lg">Workout</a>
            <a href="#programs" className="block px-3 py-2 text-slate-300 hover:bg-ink-800 rounded-lg">Chương trình</a>
            <a href="#stats" className="block px-3 py-2 text-slate-300 hover:bg-ink-800 rounded-lg">PR & Volume</a>
            <div className="pt-2 border-t border-ink-800 flex gap-2">
              <a href="/login" className="flex-1 py-2 text-center bg-ink-800 text-slate-300 rounded-lg">Đăng nhập</a>
              <a href="/signup" className="flex-1 py-2 text-center bg-electric-500 text-ink-950 font-extrabold rounded-lg">Tải app</a>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}