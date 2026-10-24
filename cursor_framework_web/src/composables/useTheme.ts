import { ref } from 'vue'

export type ThemeName = 'emerald' | 'indigo' | 'cyberpunk' | 'slate' | 'heritage' | 'light'

export interface ThemeOption {
  id: ThemeName
  name: string
  labelVi: string
  accentColor: string
  bgPreview: string
  icon: string
  vibe: string
}

export const THEME_OPTIONS: ThemeOption[] = [
  {
    id: 'emerald',
    name: 'Emerald Engine',
    labelVi: 'Ngọc Lục Bảo AI',
    accentColor: '#10b981',
    bgPreview: '#09090b',
    icon: '⚡',
    vibe: 'Linear / Vercel Dark Zinc & Acid Emerald'
  },
  {
    id: 'indigo',
    name: 'Indigo Linear',
    labelVi: 'Tím Đêm Điện Tử',
    accentColor: '#6366f1',
    bgPreview: '#0b0c16',
    icon: '🔮',
    vibe: 'Deep Midnight & Neon Indigo Glow'
  },
  {
    id: 'cyberpunk',
    name: 'Cyber Amber',
    labelVi: 'Neo Tokyo Hổ Phách',
    accentColor: '#f59e0b',
    bgPreview: '#0c0a09',
    icon: '🔥',
    vibe: 'Obsidian Noir & Vibrant Amber / Cyan'
  },
  {
    id: 'slate',
    name: 'Slate Luxury',
    labelVi: 'Titanium & Hoàng Kim',
    accentColor: '#eab308',
    bgPreview: '#090d16',
    icon: '🏎️',
    vibe: 'Automotive Gunmetal & Champagne Gold'
  },
  {
    id: 'heritage',
    name: 'Warm Heritage',
    labelVi: 'Gỗ Mộc Di Sản',
    accentColor: '#d97706',
    bgPreview: '#140c07',
    icon: '🏺',
    vibe: 'Espresso Wood & Terracotta Earth'
  },
  {
    id: 'light',
    name: 'Clean Editorial',
    labelVi: 'Tạp Chí Trắng Giấy',
    accentColor: '#059669',
    bgPreview: '#f8fafc',
    icon: '☀️',
    vibe: 'Crisp High-Contrast Paper White'
  }
]

const THEME_STORAGE_KEY = 'cef_theme_preference'
const currentTheme = ref<ThemeName>('emerald')

export function useTheme() {
  function applyTheme(theme: ThemeName) {
    currentTheme.value = theme
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', theme)
      try {
        localStorage.setItem(THEME_STORAGE_KEY, theme)
      } catch (e) {
        // Ignore localStorage quota or private mode issues
      }
    }
  }

  function initTheme() {
    if (typeof window === 'undefined') return
    try {
      const saved = localStorage.getItem(THEME_STORAGE_KEY) as ThemeName | null
      if (saved && THEME_OPTIONS.some((t) => t.id === saved)) {
        applyTheme(saved)
        return
      }
    } catch (e) {
      // Fallback
    }
    applyTheme('emerald')
  }

  return {
    currentTheme,
    themes: THEME_OPTIONS,
    applyTheme,
    initTheme
  }
}
