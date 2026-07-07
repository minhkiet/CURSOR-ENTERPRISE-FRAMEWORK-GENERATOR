import { ref, computed } from 'vue'
import JSZip from 'jszip'

export type DownloadFormat = 'html' | 'nextjs' | 'vue'

export type DownloadStatus = 'idle' | 'preparing' | 'ready' | 'error'

export interface Template {
  id: string
  slug: string
  name: string
  industry: string
  tagline: string
  description: string
}

export function useDownload() {
  const downloadStatus = ref<DownloadStatus>('idle')
  const downloadFormat = ref<DownloadFormat>('html')
  const downloadProgress = ref(0)
  const errorMessage = ref('')

  const statusLabel = computed(() => {
    switch (downloadStatus.value) {
      case 'idle': return 'Tải về'
      case 'preparing': return 'Đang chuẩn bị...'
      case 'ready': return 'Đã tải'
      case 'error': return 'Lỗi'
    }
  })

  async function downloadTemplate(
    template: Template,
    format: DownloadFormat = 'html'
  ) {
    if (downloadStatus.value === 'preparing') return

    downloadStatus.value = 'preparing'
    downloadFormat.value = format
    downloadProgress.value = 0
    errorMessage.value = ''

    try {
      // Fetch template files
      const basePath = `/templates/${template.id}`
      const [htmlRes, cssRes, jsRes] = await Promise.all([
        fetch(`${basePath}/index.html`),
        fetch(`${basePath}/styles.css`),
        fetch(`${basePath}/script.js`)
      ])

      if (!htmlRes.ok || !cssRes.ok || !jsRes.ok) {
        throw new Error('Không thể tải các file template')
      }

      const [htmlContent, cssContent, jsContent] = await Promise.all([
        htmlRes.text(),
        cssRes.text(),
        jsRes.text()
      ])

      downloadProgress.value = 40

      const zip = new JSZip()
      const folderName = `${template.id}-landing`

      if (format === 'html') {
        // Pure HTML/CSS/JS format
        const folder = zip.folder(folderName)!
        folder.file('index.html', htmlContent)
        folder.file('styles.css', cssContent)
        folder.file('script.js', jsContent)
        folder.file('README.md', generateHtmlReadme(template))
      } else if (format === 'nextjs') {
        // Next.js format
        const folder = zip.folder(folderName)!

        // Main component
        folder.file('components/LandingPage.tsx', convertToNextJS(htmlContent, cssContent, jsContent, template))

        // Page file
        folder.file('app/page.tsx', generateNextJSPage(template))

        // Layout
        folder.file('app/layout.tsx', generateNextJSLayout())

        // Config
        folder.file('package.json', generateNextJSPackage(template))
        folder.file('tailwind.config.ts', generateTailwindConfig())
        folder.file('next.config.js', generateNextConfig())
        folder.file('README.md', generateNextJSReadme(template))
        folder.file('tsconfig.json', generateTSConfig())

        // Global styles
        folder.file('app/globals.css', generateGlobalCSS())
      } else if (format === 'vue') {
        // Vue 3 format
        const folder = zip.folder(folderName)!

        // Main component
        folder.file('components/LandingPage.vue', convertToVue(htmlContent, cssContent, template))

        // Script
        folder.file('components/useLandingPage.ts', convertToVueComposable(jsContent, template))

        // App entry
        folder.file('App.vue', generateVueApp(template))
        folder.file('main.ts', generateVueMain())
        folder.file('vite.config.ts', generateVueViteConfig())
        folder.file('package.json', generateVuePackage(template))
        folder.file('index.html', generateVueIndexHtml(template))
        folder.file('README.md', generateVueReadme(template))
        folder.file('tsconfig.json', generateVueTSConfig())
        folder.file('env.d.ts', generateVueEnvTypes())
      }

      downloadProgress.value = 70

      const blob = await zip.generateAsync({
        type: 'blob',
        compression: 'DEFLATE',
        compressionOptions: { level: 9 }
      }, (metadata) => {
        downloadProgress.value = 70 + Math.round(metadata.percent * 0.3)
      })

      downloadProgress.value = 100

      // Trigger download
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `${folderName}.zip`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(link.href)

      downloadStatus.value = 'ready'
      setTimeout(() => {
        downloadStatus.value = 'idle'
        downloadProgress.value = 0
      }, 2000)
    } catch (err) {
      console.error('Download error:', err)
      downloadStatus.value = 'error'
      errorMessage.value = err instanceof Error ? err.message : 'Lỗi không xác định'
      setTimeout(() => {
        downloadStatus.value = 'idle'
        errorMessage.value = ''
      }, 3000)
    }
  }

  return {
    downloadStatus,
    downloadFormat,
    downloadProgress,
    errorMessage,
    statusLabel,
    downloadTemplate
  }
}

// HTML conversion helpers
function convertToNextJS(_html: string, _css: string, _js: string, template: Template): string {
  // Extract sections from HTML
  const navMatch = _html.match(/<nav[^>]*>[\s\S]*?<\/nav>/)
  const heroMatch = _html.match(/<header[^>]*>[\s\S]*?<\/header>/)
  const sections = _html.match(/<section[^>]*>[\s\S]*?<\/section>/g) || []
  const footerMatch = _html.match(/<footer[^>]*>[\s\S]*?<\/footer>/)
  const floatingContact = _html.match(/<div class="floating-contact">[\s\S]*?<\/div>/)

  // Components extracted (for future enhancement with more sophisticated parsing)
  void navMatch
  void heroMatch
  void sections
  void footerMatch
  void floatingContact

  return `import { useState, useEffect } from 'react'

interface Props {
  template?: {
    id: string
    name: string
    industry: string
  }
}

export default function LandingPage({ template }: Props) {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className={\`fixed top-0 left-0 right-0 z-50 transition-all duration-300 \${scrolled ? 'bg-white/95 backdrop-blur-md shadow-sm' : 'bg-transparent'}\`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            <a href="#" className="flex items-center gap-2">
              <span className="text-xl lg:text-2xl font-bold text-emerald-600">{template?.name || 'Brand'}</span>
            </a>
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors">Tính năng</a>
              <a href="#pricing" className="text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors">Bảng giá</a>
              <a href="#" className="text-sm font-medium text-gray-700 hover:text-emerald-600 transition-colors">Liên hệ</a>
              <button className="px-4 py-2 text-sm font-medium text-emerald-600 border border-emerald-600 rounded-lg hover:bg-emerald-50 transition-colors">
                Đăng nhập
              </button>
              <button className="px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors">
                Bắt đầu ngay
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative pt-20 lg:pt-24 pb-16 lg:pb-24 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 to-teal-50" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <span className="inline-flex items-center gap-2 px-3 py-1 text-sm font-medium text-emerald-700 bg-emerald-100 rounded-full mb-6">
              <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
              {template?.industry || 'Industry'} Template
            </span>
            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
              Build faster with <span className="text-emerald-600">Cursor Enterprise</span>
            </h1>
            <p className="text-lg lg:text-xl text-gray-600 mb-8">
              Professional landing page template with modern design, responsive layout, and optimized performance.
            </p>
            <div className="flex flex-wrap gap-4">
              <button className="px-6 py-3 text-lg font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors flex items-center gap-2">
                Bắt đầu ngay
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
              <button className="px-6 py-3 text-lg font-medium text-emerald-700 border border-emerald-600 rounded-lg hover:bg-emerald-50 transition-colors">
                Xem demo
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section id="features" className="py-16 lg:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12 lg:mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Tính năng nổi bật</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">Everything you need to build a professional landing page quickly</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: '🚀', title: 'Performance First', desc: 'Optimized for Core Web Vitals with minimal JS and CSS' },
              { icon: '📱', title: 'Fully Responsive', desc: 'Perfect on all devices from mobile to large screens' },
              { icon: '🎨', title: 'Modern Design', desc: 'Clean, professional design following latest trends' },
              { icon: '♿', title: 'Accessible', desc: 'WCAG 2.1 AA compliant with proper semantics' },
              { icon: '⚡', title: 'Fast Loading', desc: 'Lazy loading images and optimized assets' },
              { icon: '🔧', title: 'Easy to Customize', desc: 'Well-structured code with CSS variables' }
            ].map((feature, i) => (
              <div key={i} className="p-6 bg-gray-50 rounded-xl hover:shadow-lg transition-shadow">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
              <p className="text-xl font-bold">{template?.name || 'Brand'}</p>
              <p className="text-gray-400 text-sm mt-1">Professional landing page template</p>
            </div>
            <div className="flex gap-6 text-sm text-gray-400">
              <a href="#" className="hover:text-white transition-colors">Privacy</a>
              <a href="#" className="hover:text-white transition-colors">Terms</a>
              <a href="#" className="hover:text-white transition-colors">Contact</a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm text-gray-500">
            © ${new Date().getFullYear()} ${template?.name || 'Brand'}. Built with Cursor Enterprise Framework.
          </div>
        </div>
      </footer>

      {/* Floating Contact */}
      <div className="fixed bottom-6 right-6 flex flex-col gap-3 z-50">
        <button className="w-12 h-12 bg-green-600 rounded-full shadow-lg hover:scale-110 transition-transform flex items-center justify-center" aria-label="Hotline">
          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
          </svg>
        </button>
        <button className="w-12 h-12 bg-blue-600 rounded-full shadow-lg hover:scale-110 transition-transform flex items-center justify-center" aria-label="Zalo">
          <span className="text-white font-bold text-sm">Z</span>
        </button>
      </div>
    </div>
  )
}
`
}

function convertToVue(_html: string, _css: string, template: Template): string {
  return `<template>
  <div class="landing-page">
    <!-- Navigation -->
    <nav 
      class="nav"
      :class="{ scrolled: isScrolled }"
    >
      <div class="container nav-inner">
        <a href="#" class="logo">
          <span>{{ title }}</span>
        </a>
        <ul class="nav-menu">
          <li><a href="#features">Tính năng</a></li>
          <li><a href="#pricing">Bảng giá</a></li>
          <li><a href="#contact">Liên hệ</a></li>
        </ul>
        <div class="nav-actions">
          <button class="nav-ghost">Đăng nhập</button>
          <a href="#pricing" class="nav-cta">
            Bắt đầu ngay
            <span>→</span>
          </a>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header class="hero">
      <div class="container">
        <div class="hero-content">
          <span class="eyebrow">
            <span class="eyebrow-dot"></span>
            {{ industry }} Template
          </span>
          <h1 class="hero-title">
            Build faster with <span class="highlight">Cursor Enterprise</span>
          </h1>
          <p class="hero-desc">
            Professional landing page template with modern design, 
            responsive layout, and optimized performance.
          </p>
          <div class="hero-cta">
            <button class="btn btn-primary" @click="onCtaClick">
              Bắt đầu ngay
            </button>
            <button class="btn btn-ghost" @click="onDemoClick">
              Xem demo
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Features Section -->
    <section id="features" class="features">
      <div class="container">
        <div class="section-header">
          <h2>Tính năng nổi bật</h2>
          <p>Everything you need to build a professional landing page</p>
        </div>
        <div class="features-grid">
          <article v-for="(feature, index) in features" :key="index" class="feature-card">
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="pricing">
      <div class="container">
        <div class="section-header">
          <h2>Bảng giá</h2>
          <p>Choose the plan that fits your needs</p>
        </div>
        <div class="pricing-grid">
          <article v-for="plan in pricingPlans" :key="plan.name" class="pricing-card">
            <h3>{{ plan.name }}</h3>
            <div class="price">
              <span class="amount">{{ plan.price }}</span>
              <span class="period">/tháng</span>
            </div>
            <ul class="plan-features">
              <li v-for="(f, i) in plan.features" :key="i">{{ f }}</li>
            </ul>
            <button class="btn" :class="plan.popular ? 'btn-primary' : 'btn-outline'">
              {{ plan.cta }}
            </button>
          </article>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <h3>{{ title }}</h3>
            <p>Professional landing page template</p>
          </div>
          <div class="footer-links">
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
            <a href="#">Contact</a>
          </div>
        </div>
        <div class="footer-bottom">
          © {{ currentYear }} {{ title }}. Built with Cursor Enterprise Framework.
        </div>
      </div>
    </footer>

    <!-- Floating Contact -->
    <div class="floating-contact">
      <a href="tel:0901234567" class="float-btn hotline" aria-label="Hotline">
        <span class="pulse"></span>
      </a>
      <a href="https://zalo.me" target="_blank" class="float-btn zalo" aria-label="Zalo">
        <span class="pulse"></span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  title?: string
  industry?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '${template.name}',
  industry: '${template.industry}'
})

const isScrolled = ref(false)
const currentYear = new Date().getFullYear()

const features = [
  { icon: '🚀', title: 'Performance First', description: 'Optimized for Core Web Vitals' },
  { icon: '📱', title: 'Fully Responsive', description: 'Perfect on all devices' },
  { icon: '🎨', title: 'Modern Design', description: 'Clean and professional' },
  { icon: '♿', title: 'Accessible', description: 'WCAG 2.1 AA compliant' },
  { icon: '⚡', title: 'Fast Loading', description: 'Lazy loading images' },
  { icon: '🔧', title: 'Easy to Customize', description: 'Well-structured code' }
]

const pricingPlans = [
  {
    name: 'Basic',
    price: '199K',
    features: ['Responsive Design', 'Basic Components', 'Email Support'],
    cta: 'Chọn Basic',
    popular: false
  },
  {
    name: 'Pro',
    price: '499K',
    features: ['All Basic features', 'Advanced Components', 'Priority Support', 'Custom Domain'],
    cta: 'Chọn Pro',
    popular: true
  },
  {
    name: 'Enterprise',
    price: 'Liên hệ',
    features: ['All Pro features', 'Custom Solutions', '24/7 Support', 'SLA'],
    cta: 'Liên hệ',
    popular: false
  }
]

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}

function onCtaClick() {
  document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' })
}

function onDemoClick() {
  // Handle demo click
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Navigation */
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 1rem 0;
  transition: all 0.3s ease;
}
.nav.scrolled {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #10b981;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.nav-menu a {
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-menu a:hover {
  color: #10b981;
}

.nav-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.nav-ghost {
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  color: #10b981;
  font-weight: 500;
  cursor: pointer;
}

.nav-cta {
  padding: 0.5rem 1rem;
  background: #10b981;
  color: white;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

/* Hero */
.hero {
  padding: 8rem 0 4rem;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
}

.hero-content {
  max-width: 48rem;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #059669;
  margin-bottom: 1rem;
}

.eyebrow-dot {
  width: 0.5rem;
  height: 0.5rem;
  background: #10b981;
  border-radius: 50%;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.hero-title .highlight {
  color: #10b981;
}

.hero-desc {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 2rem;
  line-height: 1.75;
}

.hero-cta {
  display: flex;
  gap: 1rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: #10b981;
  color: white;
}

.btn-primary:hover {
  background: #059669;
}

.btn-ghost {
  background: transparent;
  color: #10b981;
  border: 1px solid #10b981;
}

.btn-outline {
  background: transparent;
  color: #10b981;
  border: 1px solid #10b981;
}

/* Features */
.features {
  padding: 5rem 0;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
}

.section-header p {
  color: #6b7280;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 1rem;
  transition: all 0.3s;
}

.feature-card:hover {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #6b7280;
}

/* Pricing */
.pricing {
  padding: 5rem 0;
  background: #f9fafb;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.pricing-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.pricing-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1rem;
}

.price {
  margin-bottom: 1.5rem;
}

.price .amount {
  font-size: 2.5rem;
  font-weight: 800;
  color: #10b981;
}

.price .period {
  color: #6b7280;
}

.plan-features {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
}

.plan-features li {
  padding: 0.5rem 0;
  color: #6b7280;
  border-bottom: 1px solid #f3f4f6;
}

/* Footer */
.footer {
  padding: 3rem 0;
  background: #111827;
  color: white;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.footer-brand h3 {
  font-size: 1.25rem;
  font-weight: 700;
}

.footer-brand p {
  color: #9ca3af;
  font-size: 0.875rem;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  color: #9ca3af;
  text-decoration: none;
}

.footer-links a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #374151;
  color: #9ca3af;
  font-size: 0.875rem;
}

/* Floating Contact */
.floating-contact {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 50;
}

.float-btn {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}

.float-btn.hotline {
  background: #00884a;
}

.float-btn.zalo {
  background: #0068FF;
}

.pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.3); }
  70% { box-shadow: 0 0 0 15px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}
</style>
`
}

// File generators
function generateHtmlReadme(template: Template): string {
  return `# ${template.name} Landing Page

A professional landing page template for ${template.industry}.

## Features
- Fully responsive design
- Modern UI with smooth animations
- SEO optimized
- Performance focused

## Usage
1. Extract the files
2. Open \`index.html\` in your browser
3. Customize content as needed

## Files
- \`index.html\` - Main HTML file
- \`styles.css\` - All CSS styles
- \`script.js\` - JavaScript functionality

## License
MIT License
`
}

function generateNextJSPackage(template: Template): string {
  return JSON.stringify({
    name: `${template.id}-landing-nextjs`,
    version: '1.0.0',
    private: true,
    scripts: {
      dev: 'next dev',
      build: 'next build',
      start: 'next start',
      lint: 'next lint'
    },
    dependencies: {
      next: '^14.0.0',
      react: '^18.2.0',
      'react-dom': '^18.2.0'
    },
    devDependencies: {
      '@types/node': '^20.0.0',
      '@types/react': '^18.2.0',
      '@types/react-dom': '^18.2.0',
      autoprefixer: '^10.4.16',
      postcss: '^8.4.31',
      tailwindcss: '^3.3.5',
      typescript: '^5.0.0'
    }
  }, null, 2)
}

function generateNextJSPage(template: Template): string {
  return `import LandingPage from '@/components/LandingPage'

export default function Home() {
  return (
    <main>
      <LandingPage 
        template={{
          id: '${template.id}',
          name: '${template.name}',
          industry: '${template.industry}'
        }}
      />
    </main>
  )
}
`
}

function generateNextJSLayout(): string {
  return `import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Landing Page - Cursor Enterprise',
  description: 'Professional landing page built with Cursor Enterprise Framework',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi">
      <body className="antialiased">{children}</body>
    </html>
  )
}
`
}

function generateGlobalCSS(): string {
  return `@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --emerald: #10b981;
  --emerald-dark: #059669;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
`
}

function generateTailwindConfig(): string {
  return `import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        emerald: {
          50: '#ecfdf5',
          100: '#d1fae5',
          500: '#10b981',
          600: '#059669',
          700: '#047857',
        },
      },
    },
  },
  plugins: [],
}
export default config
`
}

function generateNextConfig(): string {
  return `/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
`
}

function generateTSConfig(): string {
  return JSON.stringify({
    "compilerOptions": {
      "lib": ["dom", "dom.iterable", "esnext"],
      "allowJs": true,
      "skipLibCheck": true,
      "strict": true,
      "noEmit": true,
      "esModuleInterop": true,
      "module": "esnext",
      "moduleResolution": "bundler",
      "resolveJsonModule": true,
      "isolatedModules": true,
      "jsx": "preserve",
      "incremental": true,
      "plugins": [{ "name": "next" }],
      "paths": { "@/*": ["./*"] }
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
  }, null, 2)
}

function generateNextJSReadme(template: Template): string {
  return `# ${template.name} - Next.js

A professional landing page built with Next.js and Tailwind CSS.

## Tech Stack
- Next.js 14 (App Router)
- React 18
- Tailwind CSS
- TypeScript

## Getting Started

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
\`\`\`

## Project Structure
\`\`\`
├── app/
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/
│   └── LandingPage.tsx # Main component
├── package.json
├── tailwind.config.ts
└── tsconfig.json
\`\`\`

## Customization
Edit the \`components/LandingPage.tsx\` file to customize content, colors, and sections.

## License
MIT
`
}

function generateVuePackage(template: Template): string {
  return JSON.stringify({
    name: `${template.id}-landing-vue`,
    version: '1.0.0',
    private: true,
    type: 'module',
    scripts: {
      dev: 'vite',
      build: 'vue-tsc -b && vite build',
      preview: 'vite preview'
    },
    dependencies: {
      vue: '^3.4.0',
      'vue-router': '^4.2.0'
    },
    devDependencies: {
      '@vitejs/plugin-vue': '^5.0.0',
      typescript: '^5.0.0',
      'vue-tsc': '^2.0.0',
      vite: '^5.0.0'
    }
  }, null, 2)
}

function generateVueApp(template: Template): string {
  return `<template>
  <LandingPage 
    title="${template.name}"
    industry="${template.industry}"
  />
</template>

<script setup lang="ts">
import LandingPage from './components/LandingPage.vue'
</script>
`
}

function generateVueMain(): string {
  return `import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

createApp(App).mount('#app')
`
}

function generateVueViteConfig(): string {
  return `import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
`
}

function generateVueIndexHtml(template: Template): string {
  return `<!DOCTYPE html>
<html lang="vi">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${template.name} - Vue Landing Page</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
`
}

function generateVueTSConfig(): string {
  return JSON.stringify({
    "compilerOptions": {
      "target": "ES2020",
      "useDefineForClassFields": true,
      "module": "ESNext",
      "lib": ["ES2020", "DOM", "DOM.Iterable"],
      "skipLibCheck": true,
      "moduleResolution": "bundler",
      "allowImportingTsExtensions": true,
      "resolveJsonModule": true,
      "isolatedModules": true,
      "noEmit": true,
      "jsx": "preserve",
      "strict": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noFallthroughCasesInSwitch": true
    },
    "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
    "references": [{ "path": "./tsconfig.node.json" }]
  }, null, 2)
}

function generateVueEnvTypes(): string {
  return `/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
`
}

function generateVueReadme(template: Template): string {
  return `# ${template.name} - Vue 3

A professional landing page built with Vue 3 and Vite.

## Tech Stack
- Vue 3 (Composition API)
- Vite
- TypeScript

## Getting Started

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
\`\`\`

## Project Structure
\`\`\`
├── src/
│   ├── components/
│   │   ├── LandingPage.vue  # Main component
│   │   └── useLandingPage.ts # Composable
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── index.html
├── package.json
├── vite.config.ts
└── tsconfig.json
\`\`\`

## License
MIT
`
}

function convertToVueComposable(_js: string, template: Template): string {
  return `// Composable for ${template.name} landing page
import { ref, onMounted, onUnmounted } from 'vue'

export function useLandingPage() {
  const isScrolled = ref(false)
  const isMenuOpen = ref(false)

  function handleScroll() {
    isScrolled.value = window.scrollY > 50
  }

  function toggleMenu() {
    isMenuOpen.value = !isMenuOpen.value
  }

  function scrollToSection(id: string) {
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
      isMenuOpen.value = false
    }
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return {
    isScrolled,
    isMenuOpen,
    toggleMenu,
    scrollToSection
  }
}
`
}
