import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
        display: ['"Archivo Black"', '"Inter"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace']
      },
      colors: {
        ink: {
          950: '#0a0f1a',
          900: '#0f1729',
          800: '#162033',
          700: '#1e293f'
        },
        electric: {
          DEFAULT: '#84cc16',
          50: '#f7fee7',
          100: '#ecfccb',
          200: '#d9f99d',
          300: '#bef264',
          400: '#a3e635',
          500: '#84cc16',
          600: '#65a30d',
          700: '#4d7c0f',
          800: '#3f6212',
          900: '#365314'
        },
        blood: {
          DEFAULT: '#dc2626',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c'
        }
      },
      boxShadow: {
        'card-soft': '0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
        'card-lift': '0 8px 24px rgba(0, 0, 0, 0.4), 0 2px 6px rgba(0, 0, 0, 0.2)',
        'glow-electric': '0 0 0 4px rgba(132, 204, 22, 0.18), 0 0 30px rgba(132, 204, 22, 0.18)'
      }
    }
  },
  plugins: []
};

export default config;