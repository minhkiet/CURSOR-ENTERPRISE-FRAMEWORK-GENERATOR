<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { templates as defaultTemplates, type Template } from '../data/templates'
import TemplatePreviewSvg from '../components/TemplatePreviewSvg.vue'
import { useCmsAuth } from '../composables/useCmsAuth'

const router = useRouter()

// Authentication & Session
const { isAuthenticated, currentUser, checkAuth, login, logout, CREDENTIALS_HINT } = useCmsAuth()

const loginForm = ref({
  username: '',
  password: ''
})
const showPassword = ref(false)
const rememberMe = ref(true)
const loginError = ref('')
const isLoggingIn = ref(false)
const isCardShaking = ref(false)

function handleLoginSubmit() {
  loginError.value = ''
  isLoggingIn.value = true

  setTimeout(() => {
    const res = login(loginForm.value.username, loginForm.value.password, rememberMe.value)
    isLoggingIn.value = false
    if (res.success) {
      showToast(res.message)
      loginForm.value.password = ''
    } else {
      loginError.value = res.message
      isCardShaking.value = true
      setTimeout(() => {
        isCardShaking.value = false
      }, 600)
    }
  }, 250)
}

function handleLogout() {
  logout()
  showToast('Đã đăng xuất thành công khỏi hệ thống CMS.')
}

function fillCredentialsQuickly() {
  loginForm.value.username = CREDENTIALS_HINT.user
  loginForm.value.password = CREDENTIALS_HINT.pass
  loginError.value = ''
}

// Local storage key for persistent edits
const STORAGE_KEY = 'cef_cms_templates_v1'

// State
const activeTab = ref<'templates' | 'analytics' | 'deploy' | 'logs'>('templates')
const viewMode = ref<'grid' | 'table'>('grid')
const searchQuery = ref('')
const selectedIndustry = ref('all')
const statusFilter = ref<'all' | 'featured' | 'active'>('all')
const sortBy = ref<'name' | 'pages' | 'size' | 'industry'>('name')

// Loaded templates (with reactive persistence)
const templateList = ref<Template[]>([])

// Featured ids stored in local storage
const featuredIds = ref<Set<string>>(new Set(['crm', 'sale', 'insurance', 'bazi', 'realestate']))

// Active/Draft toggle map
const activeStatusMap = ref<Record<string, boolean>>({})

// Modals state
const isEditModalOpen = ref(false)
const isPreviewModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const editingTemplate = ref<Partial<Template>>({})
const isCreatingNew = ref(false)
const previewingTemplate = ref<Template | null>(null)
const previewViewport = ref<'desktop' | 'tablet' | 'mobile'>('desktop')
const templateToDelete = ref<Template | null>(null)

// Toast State
const toastMessage = ref('')
const toastVisible = ref(false)

function showToast(msg: string) {
  toastMessage.value = msg
  toastVisible.value = true
  setTimeout(() => {
    toastVisible.value = false
  }, 3500)
}

// Initialize templates from localStorage or defaults
onMounted(() => {
  // Check auth session
  checkAuth()

  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      templateList.value = JSON.parse(saved)
    } else {
      templateList.value = JSON.parse(JSON.stringify(defaultTemplates))
    }
  } catch (_e) {
    templateList.value = JSON.parse(JSON.stringify(defaultTemplates))
  }

  // initialize active status
  templateList.value.forEach(t => {
    if (activeStatusMap.value[t.id] === undefined) {
      activeStatusMap.value[t.id] = true
    }
  })
})

function saveToLocalStorage() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(templateList.value))
  } catch (e) {
    console.error('Failed to save to localStorage', e)
  }
}

// Computed categories & industries
const industries = computed(() => {
  const set = new Set<string>(templateList.value.map((t) => t.industry))
  return ['all', ...Array.from(set).sort()]
})

// Filtered and sorted templates
const filteredTemplates = computed(() => {
  let list = templateList.value.filter((t) => {
    const matchesIndustry = selectedIndustry.value === 'all' || t.industry === selectedIndustry.value
    const q = searchQuery.value.toLowerCase().trim()
    const matchesSearch =
      !q ||
      t.name.toLowerCase().includes(q) ||
      t.slug.toLowerCase().includes(q) ||
      t.tagline.toLowerCase().includes(q) ||
      t.category.toLowerCase().includes(q) ||
      t.tags.some((tag) => tag.toLowerCase().includes(q))

    const isFeatured = featuredIds.value.has(t.id)
    const matchesStatus =
      statusFilter.value === 'all' ||
      (statusFilter.value === 'featured' && isFeatured) ||
      (statusFilter.value === 'active' && activeStatusMap.value[t.id])

    return matchesIndustry && matchesSearch && matchesStatus
  })

  // Sort
  list.sort((a, b) => {
    if (sortBy.value === 'name') return a.name.localeCompare(b.name)
    if (sortBy.value === 'pages') return b.pages - a.pages
    if (sortBy.value === 'industry') return a.industry.localeCompare(b.industry)
    if (sortBy.value === 'size') {
      const sizeA = parseInt(a.fileSize) || 0
      const sizeB = parseInt(b.fileSize) || 0
      return sizeB - sizeA
    }
    return 0
  })

  return list
})

// KPI Metrics
const totalTemplatesCount = computed(() => templateList.value.length)
const totalPagesCount = computed(() => templateList.value.reduce((acc, t) => acc + (t.pages || 0), 0))
const featuredCount = computed(() => templateList.value.filter(t => featuredIds.value.has(t.id)).length)
const activeCount = computed(() => templateList.value.filter(t => activeStatusMap.value[t.id] !== false).length)

// Actions
function toggleFeatured(id: string) {
  if (featuredIds.value.has(id)) {
    featuredIds.value.delete(id)
    showToast(`Đã bỏ đánh dấu nổi bật`)
  } else {
    featuredIds.value.add(id)
    showToast(`Đã thêm vào danh sách nổi bật ★`)
  }
}

function toggleStatus(id: string) {
  activeStatusMap.value[id] = !activeStatusMap.value[id]
  const status = activeStatusMap.value[id] ? 'Hoạt động' : 'Bản nháp (Tạm ẩn)'
  showToast(`Template ${id} chuyển sang: ${status}`)
}

function openCreateModal() {
  isCreatingNew.value = true
  editingTemplate.value = {
    id: `tpl-${Date.now().toString().slice(-4)}`,
    slug: 'new-template',
    name: 'Template Mới',
    category: 'Doanh Nghiệp & Dịch Vụ',
    tagline: 'Khẩu hiệu ngắn gọn ấn tượng',
    description: 'Mô tả chi tiết về tính năng và giá trị của template này...',
    industry: 'BUSINESS',
    accent: '#0284c7',
    accentSecondary: '#f59e0b',
    bgGradient: 'linear-gradient(135deg, #07192f 0%, #0369a1 100%)',
    icon: 'sparkles',
    features: ['Thiết kế chuẩn conversion', 'Tối ưu tốc độ tải 100/100', 'Mobile-first responsive'],
    highlights: [
      { label: 'Tỉ lệ chuyển đổi', value: '+35%' },
      { label: 'Lượt tải', value: '1.2K' }
    ],
    tags: ['Landing Page', 'Responsive', 'Modern'],
    fileSize: '240 KB',
    pages: 5,
    techStack: ['HTML5', 'CSS3', 'Vanilla JS']
  }
  isEditModalOpen.value = true
}

function openEditModal(template: Template) {
  isCreatingNew.value = false
  editingTemplate.value = JSON.parse(JSON.stringify(template))
  isEditModalOpen.value = true
}

function saveTemplate() {
  if (!editingTemplate.value.name || !editingTemplate.value.slug) {
    alert('Vui lòng nhập Tên và Slug cho template')
    return
  }

  if (isCreatingNew.value) {
    const newTpl = editingTemplate.value as Template
    templateList.value.unshift(newTpl)
    activeStatusMap.value[newTpl.id] = true
    showToast(`Đã tạo thành công template: ${newTpl.name}`)
  } else {
    const idx = templateList.value.findIndex(t => t.id === editingTemplate.value.id)
    if (idx !== -1) {
      templateList.value[idx] = editingTemplate.value as Template
      showToast(`Đã cập nhật template: ${editingTemplate.value.name}`)
    }
  }

  saveToLocalStorage()
  isEditModalOpen.value = false
}

function confirmDelete(template: Template) {
  templateToDelete.value = template
  isDeleteModalOpen.value = true
}

function executeDelete() {
  if (!templateToDelete.value) return
  const id = templateToDelete.value.id
  templateList.value = templateList.value.filter(t => t.id !== id)
  saveToLocalStorage()
  showToast(`Đã xóa template: ${templateToDelete.value.name}`)
  isDeleteModalOpen.value = false
  templateToDelete.value = null
}

function duplicateTemplate(t: Template) {
  const copy: Template = JSON.parse(JSON.stringify(t))
  copy.id = `${t.id}-copy-${Date.now().toString().slice(-4)}`
  copy.slug = `${t.slug}-copy`
  copy.name = `${t.name} (Bản sao)`
  templateList.value.unshift(copy)
  activeStatusMap.value[copy.id] = true
  saveToLocalStorage()
  showToast(`Đã nhân bản template: ${copy.name}`)
}

function openQuickPreview(t: Template) {
  previewingTemplate.value = t
  previewViewport.value = 'desktop'
  isPreviewModalOpen.value = true
}

function exportCatalogJson() {
  const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(templateList.value, null, 2))
  const downloadAnchor = document.createElement('a')
  downloadAnchor.setAttribute('href', dataStr)
  downloadAnchor.setAttribute('download', `cef-templates-catalog-${new Date().toISOString().slice(0, 10)}.json`)
  document.body.appendChild(downloadAnchor)
  downloadAnchor.click()
  downloadAnchor.remove()
  showToast('Đã xuất file catalog JSON thành công!')
}

function triggerImport() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  input.onchange = (e) => {
    const file = (e.target as HTMLInputElement).files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (event) => {
      try {
        const parsed = JSON.parse(event.target?.result as string)
        if (Array.isArray(parsed) && parsed.length > 0) {
          templateList.value = parsed
          saveToLocalStorage()
          showToast(`Nhập thành công ${parsed.length} templates!`)
        } else {
          alert('File JSON không đúng định dạng mảng templates.')
        }
      } catch (err) {
        alert('Lỗi đọc file JSON: ' + err)
      }
    }
    reader.readAsText(file)
  }
  input.click()
}

function resetToDefaults() {
  if (confirm('Bạn có chắc muốn khôi phục danh sách templates gốc từ mã nguồn? Mọi thay đổi chưa export sẽ bị ghi đè.')) {
    templateList.value = JSON.parse(JSON.stringify(defaultTemplates))
    saveToLocalStorage()
    showToast('Đã khôi phục danh sách templates về mặc định!')
  }
}

// Helpers for editing feature tags
function addFeature() {
  if (!editingTemplate.value.features) editingTemplate.value.features = []
  editingTemplate.value.features.push('Tính năng mới...')
}

function removeFeature(idx: number) {
  editingTemplate.value.features?.splice(idx, 1)
}

function addTag() {
  if (!editingTemplate.value.tags) editingTemplate.value.tags = []
  editingTemplate.value.tags.push('Tag')
}

function removeTag(idx: number) {
  editingTemplate.value.tags?.splice(idx, 1)
}

function viewFullPreview(id: string) {
  router.push(`/templates/${id}`)
}
</script>

<template>
  <div class="cms-page">
    <!-- ─── CMS LOGIN GATE (Shown when unauthenticated) ─── -->
    <div v-if="!isAuthenticated" class="cms-login-wrapper">
      <div class="login-bg-glow"></div>
      <div class="login-bg-grid"></div>

      <div class="cms-login-card" :class="{ 'shake-card': isCardShaking }">
        <!-- Top Security Badge -->
        <div class="login-security-badge">
          <span class="badge-dot pulse"></span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0110 0v4"/>
          </svg>
          <span>Khu Vực Quản Trị Hệ Thống (Restricted)</span>
        </div>

        <!-- Brand Icon & Header -->
        <div class="login-header">
          <div class="login-logo-glow">
            <div class="login-logo-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="28" height="28">
                <rect x="3" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="3" width="7" height="7" rx="1.5"/>
                <rect x="14" y="14" width="7" height="7" rx="1.5"/>
                <rect x="3" y="14" width="7" height="7" rx="1.5"/>
              </svg>
            </div>
          </div>
          <h2 class="login-title">Cổng Đăng Nhập CMS Dashboard</h2>
          <p class="login-subtitle">
            Nhập tài khoản quản trị viên để truy cập catalog, chỉnh sửa templates và kiểm định hệ thống.
          </p>
        </div>

        <!-- Quick Demo Account Banner -->
        <div class="login-demo-bar">
          <div class="demo-bar-left">
            <span class="demo-label">Tài khoản cố định:</span>
            <span class="demo-code">user: <strong>admin</strong></span>
            <span class="demo-sep">•</span>
            <span class="demo-code">pass: <strong>admin@123</strong></span>
          </div>
          <button type="button" class="btn-demo-fill" @click="fillCredentialsQuickly" title="Nhấn để tự động điền tài khoản">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="12" height="12">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            <span>Điền nhanh</span>
          </button>
        </div>

        <!-- Error Alert -->
        <div v-if="loginError" class="login-alert-error" role="alert">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <span>{{ loginError }}</span>
        </div>

        <!-- Form -->
        <form class="login-form" @submit.prevent="handleLoginSubmit">
          <!-- Username Input -->
          <div class="login-field">
            <label class="login-label" for="login-username">Tên Đăng Nhập</label>
            <div class="login-input-wrap">
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <input
                id="login-username"
                v-model="loginForm.username"
                type="text"
                class="login-input"
                placeholder="Nhập tên đăng nhập (admin)"
                autocomplete="username"
                required
                :disabled="isLoggingIn"
              />
            </div>
          </div>

          <!-- Password Input -->
          <div class="login-field">
            <div class="login-label-row">
              <label class="login-label" for="login-password">Mật Khẩu</label>
              <span class="security-indicator">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="11" height="11">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                Xác thực bảo vệ
              </span>
            </div>
            <div class="login-input-wrap">
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
              </div>
              <input
                id="login-password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="login-input with-toggle"
                placeholder="Nhập mật khẩu (admin@123)"
                autocomplete="current-password"
                required
                :disabled="isLoggingIn"
              />
              <button
                type="button"
                class="btn-toggle-password"
                @click="showPassword = !showPassword"
                :title="showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'"
                tabindex="-1"
              >
                <!-- Eye icon when hidden -->
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <!-- Eye-off icon when visible -->
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
                  <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Options row -->
          <div class="login-options-row">
            <label class="remember-checkbox-label">
              <input v-model="rememberMe" type="checkbox" class="remember-checkbox" />
              <span>Ghi nhớ phiên đăng nhập</span>
            </label>
            <span class="login-session-info">Session Token</span>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="btn btn-primary btn-login-submit" :disabled="isLoggingIn">
            <span v-if="!isLoggingIn" class="btn-submit-inner">
              <span>Đăng Nhập CMS Dashboard</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" width="15" height="15">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </span>
            <span v-else class="btn-loading-inner">
              <span class="spinner-sm"></span>
              <span>Đang xác thực thông tin...</span>
            </span>
          </button>
        </form>

        <!-- Footer Links -->
        <div class="login-footer">
          <router-link to="/templates" class="login-back-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            <span>Quay lại Thư Viện Templates</span>
          </router-link>
          <span class="footer-sep">•</span>
          <router-link to="/" class="login-back-link">
            <span>Trang Chủ</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- ─── CMS DASHBOARD (Shown when authenticated) ─── -->
    <template v-else>
      <!-- ─── CMS HEADER BAR ─── -->
      <header class="cms-header">
        <div class="container cms-header-inner">
          <div class="cms-brand-block">
            <!-- Breadcrumb navigation -->
            <nav class="cms-breadcrumbs" aria-label="Breadcrumb">
              <router-link to="/" class="crumb-link">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13">
                  <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/>
                  <polyline points="9 22 9 12 15 12 15 22"/>
                </svg>
                <span>Trang Chủ</span>
              </router-link>
              <span class="crumb-sep">/</span>
              <router-link to="/templates" class="crumb-link">Thư Viện Templates</router-link>
              <span class="crumb-sep">/</span>
              <span class="crumb-current">Quản Trị CMS</span>
            </nav>

            <div class="cms-title-wrapper">
              <div class="cms-logo-badge">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="7" height="7" rx="1.5"/>
                  <rect x="14" y="3" width="7" height="7" rx="1.5"/>
                  <rect x="14" y="14" width="7" height="7" rx="1.5"/>
                  <rect x="3" y="14" width="7" height="7" rx="1.5"/>
                </svg>
              </div>
              <div class="cms-title-meta">
                <div class="cms-title-row">
                  <h1 class="cms-title">Trung Tâm Quản Trị Templates</h1>
                  <span class="cms-counter-pill">
                    <span class="pill-pulse-dot"></span>
                    {{ totalTemplatesCount }} Mẫu Giao Diện
                  </span>
                </div>
                <p class="cms-subtitle">
                  Hệ thống quản lý catalog, chỉnh sửa metadata, phân tích hiệu suất chuyển đổi và kiểm định chất lượng toàn bộ mẫu web doanh nghiệp.
                </p>
              </div>
            </div>
          </div>

          <div class="cms-header-actions">
            <!-- Admin user badge & Logout -->
            <div class="cms-user-badge">
              <span class="user-avatar-dot"></span>
              <div class="user-badge-text">
                <span class="user-badge-name">{{ currentUser || 'admin' }}</span>
                <span class="user-badge-role">Super Admin</span>
              </div>
            </div>

            <button class="btn btn-secondary btn-sm btn-logout" @click="handleLogout" title="Đăng xuất khỏi CMS">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14">
                <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              <span>Đăng xuất</span>
            </button>

            <router-link to="/templates" class="btn btn-secondary btn-sm" title="Mở thư viện giao diện công khai">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14">
                <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/>
                <polyline points="15 3 21 3 21 9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
              <span>Xem Thư Viện</span>
            </router-link>
            <button class="btn btn-secondary btn-sm" @click="exportCatalogJson" title="Tải file catalog JSON">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
              </svg>
              <span>Xuất JSON</span>
            </button>
            <button class="btn btn-secondary btn-sm" @click="triggerImport" title="Nhập file catalog JSON">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
              </svg>
              <span>Nhập JSON</span>
            </button>
            <button class="btn btn-primary btn-sm btn-create-accent" @click="openCreateModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" width="14" height="14">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>+ Thêm Template</span>
            </button>
          </div>
        </div>
      </header>

    <!-- ─── KPI OVERVIEW BAR ─── -->
    <section class="cms-kpi-section">
      <div class="container">
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-icon accent-emerald">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 016.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-value">{{ totalTemplatesCount }} <span class="kpi-sub">gói</span></div>
              <div class="kpi-label">{{ totalPagesCount }} trang landing pages</div>
            </div>
            <div class="kpi-badge success">+1 Mẫu Bảo Hiểm</div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon accent-blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-value">148.2K</div>
              <div class="kpi-label">Lượt xem & tương tác</div>
            </div>
            <div class="kpi-badge info">+18.4% tháng này</div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon accent-amber">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-value">34.8K</div>
              <div class="kpi-label">Lượt tải & Git clone</div>
            </div>
            <div class="kpi-badge success">23.5% Chuyển đổi</div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon accent-purple">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </div>
            <div class="kpi-content">
              <div class="kpi-value">99.2<span class="kpi-sub">/100</span></div>
              <div class="kpi-label">Lighthouse Performance</div>
            </div>
            <div class="kpi-badge success">100% Core Vitals</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── NAVIGATION TABS ─── -->
    <div class="cms-nav-tabs">
      <div class="container tabs-inner">
        <button
          class="tab-link"
          :class="{ active: activeTab === 'templates' }"
          @click="activeTab = 'templates'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
            <rect x="3" y="3" width="7" height="7"/>
            <rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/>
          </svg>
          <span>Kho Templates</span>
          <span class="tab-badge">{{ totalTemplatesCount }}</span>
        </button>
        <button
          class="tab-link"
          :class="{ active: activeTab === 'analytics' }"
          @click="activeTab = 'analytics'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
          <span>Phân Tích & Hiệu Suất</span>
        </button>
        <button
          class="tab-link"
          :class="{ active: activeTab === 'deploy' }"
          @click="activeTab = 'deploy'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
            <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          <span>Đóng Gói & Triển Khai</span>
        </button>
        <button
          class="tab-link"
          :class="{ active: activeTab === 'logs' }"
          @click="activeTab = 'logs'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          <span>Nhật Ký & Audit</span>
        </button>
      </div>
    </div>

    <!-- ─── TAB 1: TEMPLATE DIRECTORY & CRUD ─── -->
    <main v-if="activeTab === 'templates'" class="cms-main-content">
      <div class="container">
        <!-- Filter Toolbar -->
        <div class="cms-toolbar">
          <div class="toolbar-search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="16" height="16">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21l-4.35-4.35"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Tìm theo tên, slug, từ khóa, tag..."
              aria-label="Tìm kiếm template"
            />
            <button v-if="searchQuery" class="clear-search" @click="searchQuery = ''" title="Xóa tìm kiếm">&times;</button>
          </div>

          <div class="toolbar-actions-wrap">
            <!-- Industry filter -->
            <select v-model="selectedIndustry" class="toolbar-select">
              <option value="all">Mọi ngành nghề ({{ industries.length - 1 }})</option>
              <option v-for="ind in industries.filter(i => i !== 'all')" :key="ind" :value="ind">
                {{ ind }}
              </option>
            </select>

            <!-- Status filter -->
            <select v-model="statusFilter" class="toolbar-select">
              <option value="all">Tất cả trạng thái</option>
              <option value="featured">★ Nổi bật ({{ featuredCount }})</option>
              <option value="active">Đang kích hoạt</option>
            </select>

            <!-- Sort By -->
            <select v-model="sortBy" class="toolbar-select">
              <option value="name">Sắp xếp: Tên A-Z</option>
              <option value="pages">Sắp xếp: Số trang</option>
              <option value="size">Sắp xếp: Dung lượng</option>
              <option value="industry">Sắp xếp: Ngành nghề</option>
            </select>

            <!-- View Switcher -->
            <div class="view-switcher" role="group" aria-label="Kiểu hiển thị">
              <button
                class="view-btn"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                title="Dạng lưới thẻ"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <rect x="3" y="3" width="7" height="7"/>
                  <rect x="14" y="3" width="7" height="7"/>
                  <rect x="14" y="14" width="7" height="7"/>
                  <rect x="3" y="14" width="7" height="7"/>
                </svg>
              </button>
              <button
                class="view-btn"
                :class="{ active: viewMode === 'table' }"
                @click="viewMode = 'table'"
                title="Dạng bảng dữ liệu"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <line x1="8" y1="6" x2="21" y2="6"/>
                  <line x1="8" y1="12" x2="21" y2="12"/>
                  <line x1="8" y1="18" x2="21" y2="18"/>
                  <line x1="3" y1="6" x2="3.01" y2="6"/>
                  <line x1="3" y1="12" x2="3.01" y2="12"/>
                  <line x1="3" y1="18" x2="3.01" y2="18"/>
                </svg>
              </button>
            </div>

            <!-- Reset to defaults -->
            <button class="btn btn-ghost btn-sm" @click="resetToDefaults" title="Khôi phục lại templates gốc">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14">
                <path d="M3 12a9 9 0 109-9 9.75 9.75 0 00-6.74 2.74L3 8"/>
                <path d="M3 3v5h5"/>
              </svg>
              <span>Reset</span>
            </button>
          </div>
        </div>

        <!-- Results Counter & Status Summary Bar -->
        <div class="cms-results-bar">
          <div class="results-count">
            <span>Hiển thị <strong>{{ filteredTemplates.length }}</strong> / <strong>{{ totalTemplatesCount }}</strong> templates</span>
            <span v-if="searchQuery || selectedIndustry !== 'all' || statusFilter !== 'all'" class="results-filtered-pill">
              Bộ lọc đang áp dụng
            </span>
          </div>
          <div class="results-badge-group">
            <span class="badge-stat active-stat">
              <span class="dot-sm"></span>
              {{ activeCount }} Hoạt động
            </span>
            <span class="badge-stat featured-stat">
              ★ {{ featuredCount }} Nổi bật
            </span>
          </div>
        </div>

        <!-- ─── VIEW 1: GRID MODE ─── -->
        <div v-if="viewMode === 'grid'" class="cms-grid">
          <div
            v-for="t in filteredTemplates"
            :key="t.id"
            class="cms-card"
            :class="{ 'is-featured': featuredIds.has(t.id), 'is-draft': !activeStatusMap[t.id] }"
          >
            <!-- Card Header Preview -->
            <div class="cms-card-preview">
              <TemplatePreviewSvg :slug="t.slug" />
              <div class="preview-hover-overlay">
                <button class="overlay-action" @click="openQuickPreview(t)" title="Xem demo nhanh trong modal">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  <span>Quick View</span>
                </button>
                <button class="overlay-action" @click="viewFullPreview(t.id)" title="Mở trang chi tiết">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
                  <span>Toàn Màn Hình</span>
                </button>
              </div>

              <!-- Top badges inside card preview -->
              <div class="card-preview-badges">
                <span class="preview-tag-industry">{{ t.industry }}</span>
                <button
                  class="preview-star-btn"
                  :class="{ active: featuredIds.has(t.id) }"
                  @click.stop="toggleFeatured(t.id)"
                  :title="featuredIds.has(t.id) ? 'Bỏ nổi bật' : 'Đánh dấu nổi bật'"
                >
                  ★
                </button>
              </div>
            </div>

            <!-- Card Body -->
            <div class="cms-card-body">
              <div class="cms-card-topline">
                <h3 class="cms-card-name">{{ t.name }}</h3>
                <span class="cms-card-badge" :style="{ backgroundColor: t.accent + '22', color: t.accent }">
                  {{ t.category }}
                </span>
              </div>
              <p class="cms-card-tagline">{{ t.tagline }}</p>

              <!-- Tags -->
              <div class="cms-card-tags">
                <span v-for="tag in t.tags.slice(0, 3)" :key="tag" class="cms-tag-pill">
                  {{ tag }}
                </span>
                <span v-if="t.tags.length > 3" class="cms-tag-more">+{{ t.tags.length - 3 }}</span>
              </div>

              <!-- Metrics Row -->
              <div class="cms-card-metrics">
                <div class="metric-item">
                  <span class="m-val">{{ t.pages }}</span>
                  <span class="m-lbl">Trang</span>
                </div>
                <div class="metric-sep"></div>
                <div class="metric-item">
                  <span class="m-val">{{ t.fileSize }}</span>
                  <span class="m-lbl">Dung lượng</span>
                </div>
                <div class="metric-sep"></div>
                <div class="metric-item">
                  <span class="m-val" :class="activeStatusMap[t.id] ? 'text-success' : 'text-muted'">
                    {{ activeStatusMap[t.id] ? 'Active' : 'Draft' }}
                  </span>
                  <span class="m-lbl">Trạng thái</span>
                </div>
              </div>

              <!-- Actions Toolbar -->
              <div class="cms-card-actions">
                <button class="btn btn-ghost btn-sm card-act-btn" @click="openEditModal(t)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="13" height="13"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  <span>Chỉnh sửa</span>
                </button>
                <button class="btn btn-ghost btn-sm card-act-btn" @click="duplicateTemplate(t)" title="Nhân bản">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="13" height="13"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
                </button>
                <button class="btn btn-ghost btn-sm card-act-btn" @click="toggleStatus(t.id)" :title="activeStatusMap[t.id] ? 'Tạm ẩn' : 'Kích hoạt'">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="13" height="13">
                    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/>
                  </svg>
                </button>
                <button class="btn btn-ghost btn-sm card-act-btn text-danger" @click="confirmDelete(t)" title="Xóa template">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="13" height="13"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ─── VIEW 2: TABLE MODE ─── -->
        <div v-else class="cms-table-wrapper">
          <table class="cms-table">
            <thead>
              <tr>
                <th width="40">★</th>
                <th>Template & Khẩu Hiệu</th>
                <th>Ngành Nghề</th>
                <th>Màu Accent</th>
                <th>Số Trang</th>
                <th>Dung Lượng</th>
                <th>Tech Stack</th>
                <th>Trạng Thái</th>
                <th width="160">Thao Tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in filteredTemplates" :key="t.id">
                <td>
                  <button
                    class="table-star-btn"
                    :class="{ active: featuredIds.has(t.id) }"
                    @click="toggleFeatured(t.id)"
                  >
                    ★
                  </button>
                </td>
                <td>
                  <div class="table-tpl-info">
                    <div class="tpl-dot" :style="{ backgroundColor: t.accent }"></div>
                    <div>
                      <strong class="table-name">{{ t.name }}</strong>
                      <span class="table-slug">/templates/{{ t.slug }}</span>
                      <p class="table-tagline">{{ t.tagline }}</p>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="pill-industry">{{ t.industry }}</span>
                </td>
                <td>
                  <div class="accent-swatch-box">
                    <span class="swatch" :style="{ backgroundColor: t.accent }"></span>
                    <span class="swatch-code">{{ t.accent }}</span>
                  </div>
                </td>
                <td>{{ t.pages }} trang</td>
                <td>{{ t.fileSize }}</td>
                <td>
                  <span class="tech-tags-condensed">{{ t.techStack.join(', ') }}</span>
                </td>
                <td>
                  <button
                    class="status-toggle-pill"
                    :class="activeStatusMap[t.id] ? 'status-active' : 'status-draft'"
                    @click="toggleStatus(t.id)"
                  >
                    {{ activeStatusMap[t.id] ? 'Active' : 'Draft' }}
                  </button>
                </td>
                <td>
                  <div class="table-actions">
                    <button class="tbl-action-btn" @click="openQuickPreview(t)" title="Quick View">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                    </button>
                    <button class="tbl-action-btn" @click="openEditModal(t)" title="Sửa thông tin">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    </button>
                    <button class="tbl-action-btn" @click="duplicateTemplate(t)" title="Nhân bản">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
                    </button>
                    <button class="tbl-action-btn text-danger" @click="confirmDelete(t)" title="Xóa">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty Results Message -->
        <div v-if="filteredTemplates.length === 0" class="cms-empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <h3>Không tìm thấy template nào</h3>
          <p>Thử tìm kiếm với từ khóa khác hoặc thay đổi bộ lọc ngành nghề.</p>
          <button class="btn btn-outline btn-sm" @click="searchQuery = ''; selectedIndustry = 'all'; statusFilter = 'all'">Xóa bộ lọc</button>
        </div>
      </div>
    </main>

    <!-- ─── TAB 2: ANALYTICS & METRICS ─── -->
    <main v-else-if="activeTab === 'analytics'" class="cms-main-content">
      <div class="container">
        <div class="analytics-grid">
          <div class="analytics-card">
            <h3 class="card-heading">Lượt Tải & Xem Theo Danh Mục Hot</h3>
            <div class="chart-bars-list">
              <div class="chart-row">
                <span class="cr-label">INSURANCE (Bảo Hiểm)</span>
                <div class="cr-track"><div class="cr-fill emerald" style="width: 95%;"></div></div>
                <span class="cr-val">28.4K (Mới ra mắt)</span>
              </div>
              <div class="chart-row">
                <span class="cr-label">CRM & Pipeline</span>
                <div class="cr-track"><div class="cr-fill blue" style="width: 86%;"></div></div>
                <span class="cr-val">24.2K</span>
              </div>
              <div class="chart-row">
                <span class="cr-label">E-COMMERCE (Sale Pro)</span>
                <div class="cr-track"><div class="cr-fill amber" style="width: 78%;"></div></div>
                <span class="cr-val">21.8K</span>
              </div>
              <div class="chart-row">
                <span class="cr-label">REALESTATE (BĐS Nhà Tốt)</span>
                <div class="cr-track"><div class="cr-fill purple" style="width: 71%;"></div></div>
                <span class="cr-val">19.5K</span>
              </div>
              <div class="chart-row">
                <span class="cr-label">BAZI & Numerology</span>
                <div class="cr-track"><div class="cr-fill blue" style="width: 64%;"></div></div>
                <span class="cr-val">17.9K</span>
              </div>
              <div class="chart-row">
                <span class="cr-label">FOOD & F&B (Lẩu Đêm)</span>
                <div class="cr-track"><div class="cr-fill amber" style="width: 55%;"></div></div>
                <span class="cr-val">15.1K</span>
              </div>
            </div>
          </div>

          <div class="analytics-card">
            <h3 class="card-heading">Phân Bổ Thiết Bị Khách Hàng</h3>
            <div class="device-pie-mock">
              <div class="device-item">
                <div class="di-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
                <div class="di-info">
                  <strong>Máy tính bàn (Desktop)</strong>
                  <span>58.4% tổng truy cập</span>
                </div>
                <div class="di-val text-success">98.5% Awwwards score</div>
              </div>
              <div class="device-item">
                <div class="di-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg></div>
                <div class="di-info">
                  <strong>Điện thoại (Mobile)</strong>
                  <span>36.2% tổng truy cập</span>
                </div>
                <div class="di-val text-success">100% Touch target pass</div>
              </div>
              <div class="device-item">
                <div class="di-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg></div>
                <div class="di-info">
                  <strong>Máy tính bảng (Tablet)</strong>
                  <span>5.4% tổng truy cập</span>
                </div>
                <div class="di-val text-muted">Fluid grid OK</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- ─── TAB 3: DEPLOYMENT & BUNDLER ─── -->
    <main v-else-if="activeTab === 'deploy'" class="cms-main-content">
      <div class="container">
        <div class="deploy-card">
          <div class="deploy-header">
            <div>
              <h3>Tình Trạng Triển Khai & Kiểm Định Bộ Mã Nguồn</h3>
              <p>Mỗi template được kiểm tra static health check trước khi đóng gói phân phối.</p>
            </div>
            <button class="btn btn-primary" @click="showToast('Đã đồng bộ kiểm tra toàn bộ 20 templates!')">
              Chạy Kiểm Định Toàn Diện
            </button>
          </div>

          <div class="check-list">
            <div class="check-item">
              <span class="ci-badge pass">PASS</span>
              <div class="ci-text">
                <strong>Static Asset Zero-Dependency</strong>
                <p>100% templates chạy trực tiếp từ browser mà không cần npm build phức tạp.</p>
              </div>
            </div>
            <div class="check-item">
              <span class="ci-badge pass">PASS</span>
              <div class="ci-text">
                <strong>UTF-8 Tiếng Việt Có Dấu & Chuẩn Typography</strong>
                <p>Đã rà soát cập nhật ngôn ngữ, dấu câu tự nhiên, font Geist / Plus Jakarta Sans chuẩn.</p>
              </div>
            </div>
            <div class="check-item">
              <span class="ci-badge pass">PASS</span>
              <div class="ci-text">
                <strong>Đóng gói ZIP Đa Nền Tảng (HTML, Next.js, Vue 3)</strong>
                <p>Tương thích hệ thống useDownload.ts của framework qua JSZip.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- ─── TAB 4: AUDIT LOGS ─── -->
    <main v-else-if="activeTab === 'logs'" class="cms-main-content">
      <div class="container">
        <div class="logs-card">
          <h3 class="logs-title">Nhật Ký Hoạt Động Cập Nhật Framework</h3>
          <div class="log-timeline">
            <div class="log-item">
              <span class="log-time">Vừa xong</span>
              <div class="log-dot"></div>
              <div class="log-desc">
                <strong>Phát hành Template Bảo Hiểm (Aegis Bảo An)</strong>
                <p>Thêm trang web bán bảo hiểm toàn diện: Sức khỏe CarePlus, Nhân thọ An Thịnh, Xe cơ giới AutoCare, Du lịch quốc tế, công cụ tính phí 30s và mạng lưới 680+ bệnh viện.</p>
              </div>
            </div>
            <div class="log-item">
              <span class="log-time">10 phút trước</span>
              <div class="log-dot"></div>
              <div class="log-desc">
                <strong>Xây dựng CMS Dashboard Quản Trị Templates</strong>
                <p>Thêm trang CMS Dashboard với CRUD, modal preview, export/import JSON, kiểm tra hiệu suất và quản lý trạng thái.</p>
              </div>
            </div>
            <div class="log-item">
              <span class="log-time">25 phút trước</span>
              <div class="log-dot"></div>
              <div class="log-desc">
                <strong>Rà soát & Chuẩn Hóa Typography Toàn Bộ 19 Templates Cũ</strong>
                <p>Sửa lỗi chính tả tiếng Việt (Trường Mầm Non, Thánh Quang Parish, TechHub PC Gaming) và chuẩn hóa bảng mã.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- ─── MODAL: CREATE / EDIT TEMPLATE ─── -->
    <div v-if="isEditModalOpen" class="cms-modal-backdrop" @click.self="isEditModalOpen = false">
      <div class="cms-modal-dialog">
        <div class="cms-modal-header">
          <div>
            <span class="modal-sub">{{ isCreatingNew ? 'Thêm mới' : 'Chỉnh sửa metadata' }}</span>
            <h2 class="modal-title">{{ isCreatingNew ? 'Tạo Template Mới' : editingTemplate.name }}</h2>
          </div>
          <button class="modal-close-btn" @click="isEditModalOpen = false">&times;</button>
        </div>

        <div class="cms-modal-body">
          <div class="form-grid-2">
            <div class="form-col">
              <label>Tên Template *</label>
              <input v-model="editingTemplate.name" type="text" placeholder="Ví dụ: Aegis Bảo An" />
            </div>
            <div class="form-col">
              <label>Slug (Mã thư mục URL) *</label>
              <input v-model="editingTemplate.slug" type="text" placeholder="vi-du: insurance" />
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-col">
              <label>Danh Mục</label>
              <input v-model="editingTemplate.category" type="text" placeholder="Ví dụ: Bảo Hiểm Toàn Diện" />
            </div>
            <div class="form-col">
              <label>Ngành Nghề (Industry Code)</label>
              <input v-model="editingTemplate.industry" type="text" placeholder="Ví dụ: INSURANCE" />
            </div>
          </div>

          <div class="form-col">
            <label>Khẩu Hiệu (Tagline)</label>
            <input v-model="editingTemplate.tagline" type="text" placeholder="Ví dụ: An tâm tương lai, vững bước hiện tại" />
          </div>

          <div class="form-col">
            <label>Mô Tả Chi Tiết</label>
            <textarea v-model="editingTemplate.description" rows="3" placeholder="Mô tả các giá trị và tính năng của template..."></textarea>
          </div>

          <div class="form-grid-2">
            <div class="form-col">
              <label>Màu Accent Chính</label>
              <div class="color-picker-row">
                <input v-model="editingTemplate.accent" type="color" class="color-box" />
                <input v-model="editingTemplate.accent" type="text" placeholder="#0284c7" />
              </div>
            </div>
            <div class="form-col">
              <label>Màu Accent Phụ</label>
              <div class="color-picker-row">
                <input v-model="editingTemplate.accentSecondary" type="color" class="color-box" />
                <input v-model="editingTemplate.accentSecondary" type="text" placeholder="#f59e0b" />
              </div>
            </div>
          </div>

          <div class="form-grid-2">
            <div class="form-col">
              <label>Số Trang</label>
              <input v-model.number="editingTemplate.pages" type="number" min="1" max="20" />
            </div>
            <div class="form-col">
              <label>Dung Lượng Bundle</label>
              <input v-model="editingTemplate.fileSize" type="text" placeholder="Ví dụ: 312 KB" />
            </div>
          </div>

          <!-- Features List Editor -->
          <div class="form-col">
            <div class="section-label-row">
              <label>Tính Năng Nổi Bật (Features)</label>
              <button class="btn btn-ghost btn-sm" @click="addFeature">+ Thêm tính năng</button>
            </div>
            <div class="dynamic-inputs-list">
              <div v-for="(_feat, idx) in editingTemplate.features" :key="idx" class="dynamic-input-row">
                <input v-model="editingTemplate.features![idx]" type="text" />
                <button class="btn-remove" @click="removeFeature(idx)">&times;</button>
              </div>
            </div>
          </div>

          <!-- Tags Editor -->
          <div class="form-col">
            <div class="section-label-row">
              <label>Thẻ Phân Loại (Tags)</label>
              <button class="btn btn-ghost btn-sm" @click="addTag">+ Thêm tag</button>
            </div>
            <div class="dynamic-tags-list">
              <div v-for="(_tag, idx) in editingTemplate.tags" :key="idx" class="dynamic-tag-row">
                <input v-model="editingTemplate.tags![idx]" type="text" />
                <button class="btn-remove" @click="removeTag(idx)">&times;</button>
              </div>
            </div>
          </div>
        </div>

        <div class="cms-modal-footer">
          <button class="btn btn-ghost" @click="isEditModalOpen = false">Hủy</button>
          <button class="btn btn-primary" @click="saveTemplate">Lưu Thay Đổi</button>
        </div>
      </div>
    </div>

    <!-- ─── MODAL: QUICK VIEW PREVIEW ─── -->
    <div v-if="isPreviewModalOpen && previewingTemplate" class="cms-modal-backdrop" @click.self="isPreviewModalOpen = false">
      <div class="cms-modal-dialog modal-preview-wide">
        <div class="cms-modal-header preview-header">
          <div class="prev-info">
            <span class="preview-badge">{{ previewingTemplate.industry }}</span>
            <h3 class="preview-title">{{ previewingTemplate.name }}</h3>
          </div>

          <div class="viewport-toggles">
            <button
              class="vp-btn"
              :class="{ active: previewViewport === 'desktop' }"
              @click="previewViewport = 'desktop'"
              title="Desktop (100%)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            </button>
            <button
              class="vp-btn"
              :class="{ active: previewViewport === 'tablet' }"
              @click="previewViewport = 'tablet'"
              title="Tablet (768px)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
            </button>
            <button
              class="vp-btn"
              :class="{ active: previewViewport === 'mobile' }"
              @click="previewViewport = 'mobile'"
              title="Mobile (375px)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
            </button>
          </div>

          <div class="prev-actions">
            <button class="btn btn-ghost btn-sm" @click="viewFullPreview(previewingTemplate.id)">
              Mở Trang Toàn Màn Hình
            </button>
            <button class="modal-close-btn" @click="isPreviewModalOpen = false">&times;</button>
          </div>
        </div>

        <div class="preview-iframe-wrapper" :class="previewViewport">
          <iframe
            :src="`/templates/${previewingTemplate.id}/index.html`"
            class="preview-iframe"
            frameborder="0"
          ></iframe>
        </div>
      </div>
    </div>

    <!-- ─── MODAL: DELETE CONFIRMATION ─── -->
    <div v-if="isDeleteModalOpen && templateToDelete" class="cms-modal-backdrop" @click.self="isDeleteModalOpen = false">
      <div class="cms-modal-dialog modal-confirm-delete">
        <h3 class="del-title">Xác Nhận Xóa Template</h3>
        <p class="del-desc">
          Bạn có chắc chắn muốn xóa template <strong>"{{ templateToDelete.name }}"</strong> khỏi catalog quản trị? Thao tác này có thể khôi phục bằng nút Reset.
        </p>
        <div class="del-actions">
          <button class="btn btn-ghost" @click="isDeleteModalOpen = false">Hủy</button>
          <button class="btn btn-primary" style="background: #ef4444;" @click="executeDelete">Xác Nhận Xóa</button>
        </div>
      </div>
    </div>
    </template>

    <!-- ─── TOAST NOTIFICATION ─── -->
    <div class="cms-toast" :class="{ show: toastVisible }">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<style scoped>
/* ─── CMS DASHBOARD LAYOUT & DESIGN SYSTEM V6 ─── */
.cms-page {
  min-height: 100vh;
  background-color: var(--bg-base);
  color: var(--text-primary);
  padding-top: 56px; /* Crucial: clearance for fixed navbar (height: 56px) */
  padding-bottom: 80px;
}

.cms-header {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  padding: 24px 0 20px;
  position: relative;
}

.cms-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.cms-brand-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cms-breadcrumbs {
  font-size: 12px;
  color: var(--text-tertiary);
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.crumb-link {
  color: var(--text-secondary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: color var(--t-fast);
}

.crumb-link:hover {
  color: var(--accent);
}

.crumb-sep {
  color: var(--text-faint);
  font-size: 11px;
}

.crumb-current {
  color: var(--text-primary);
  font-weight: 500;
}

.cms-title-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.cms-logo-badge {
  width: 44px;
  height: 44px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.35);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  flex-shrink: 0;
  margin-top: 2px;
  box-shadow: 0 4px 14px -2px rgba(16, 185, 129, 0.25);
}

.cms-logo-badge svg {
  width: 22px;
  height: 22px;
}

.cms-title-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cms-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.cms-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.2;
}

.cms-counter-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: var(--accent);
  font-size: 12px;
  font-weight: 600;
  font-family: var(--font-mono);
}

.pill-pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  animation: pulseDotAnim 2s infinite ease-in-out;
}

@keyframes pulseDotAnim {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}

.cms-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  max-width: 640px;
  line-height: 1.5;
}

.cms-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-create-accent {
  background: var(--accent) !important;
  color: #041429 !important;
  font-weight: 700 !important;
  border-color: var(--accent) !important;
  box-shadow: 0 4px 14px -2px rgba(16, 185, 129, 0.4) !important;
  transition: all var(--t-fast) !important;
}

.btn-create-accent:hover {
  background: var(--accent-bright) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px -2px rgba(16, 185, 129, 0.5) !important;
}

/* CMS User Badge in Header */
.cms-user-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  padding: 5px 12px;
  border-radius: var(--radius-pill);
}

.user-avatar-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  animation: pulseDotAnim 2s infinite ease-in-out;
}

.user-badge-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.user-badge-name {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.user-badge-role {
  font-size: 10px;
  color: var(--accent);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.btn-logout {
  color: #f87171 !important;
  border-color: rgba(239, 68, 68, 0.25) !important;
  background: rgba(239, 68, 68, 0.05) !important;
}

.btn-logout:hover {
  background: rgba(239, 68, 68, 0.15) !important;
  border-color: rgba(239, 68, 68, 0.45) !important;
  color: #fca5a5 !important;
}

/* ─── CMS LOGIN GATE ─── */
.cms-login-wrapper {
  position: relative;
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  overflow: hidden;
}

.login-bg-glow {
  position: absolute;
  top: 15%;
  left: 50%;
  transform: translateX(-50%);
  width: 560px;
  height: 560px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.02) 45%, transparent 70%);
  pointer-events: none;
  filter: blur(40px);
}

.login-bg-grid {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(to right, rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
}

.cms-login-card {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 460px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px 28px;
  box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(16, 185, 129, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cms-login-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 24px 48px -12px rgba(0, 0, 0, 0.8), 0 0 30px -10px rgba(16, 185, 129, 0.15);
}

/* Shake Animation on Wrong Login */
.shake-card {
  animation: shakeKeyframes 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes shakeKeyframes {
  10%, 90% { transform: translate3d(-2px, 0, 0); }
  20%, 80% { transform: translate3d(4px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-6px, 0, 0); }
  40%, 60% { transform: translate3d(6px, 0, 0); }
}

.login-security-badge {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 4px 10px;
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.02em;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

.badge-dot.pulse {
  animation: pulseDotAnim 2s infinite ease-in-out;
}

.login-header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.login-logo-glow {
  width: 58px;
  height: 58px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 78, 59, 0.4));
  border: 1px solid rgba(16, 185, 129, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
  box-shadow: 0 0 20px -5px rgba(16, 185, 129, 0.4);
}

.login-logo-icon {
  color: var(--accent);
}

.login-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.02em;
}

.login-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

/* Quick Demo Bar */
.login-demo-bar {
  background: rgba(16, 185, 129, 0.05);
  border: 1px dashed rgba(16, 185, 129, 0.3);
  border-radius: var(--radius-md);
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.demo-bar-left {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
  flex-wrap: wrap;
}

.demo-label {
  font-weight: 500;
  color: var(--text-tertiary);
}

.demo-code {
  font-family: var(--font-mono);
  background: rgba(255, 255, 255, 0.06);
  padding: 1px 5px;
  border-radius: 4px;
}

.demo-code strong {
  color: var(--accent);
}

.demo-sep {
  color: var(--text-tertiary);
}

.btn-demo-fill {
  background: var(--accent);
  color: #041429;
  border: none;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 9px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-demo-fill:hover {
  background: var(--accent-bright);
  transform: translateY(-1px);
}

/* Error Alert */
.login-alert-error {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: var(--radius-md);
  padding: 10px 12px;
  color: #fca5a5;
  font-size: 12.5px;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: fadeIn 0.2s ease-out;
}

.login-alert-error svg {
  flex-shrink: 0;
  color: #ef4444;
}

/* Form inputs */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.login-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.login-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.login-label {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-secondary);
}

.security-indicator {
  font-size: 11px;
  color: var(--text-tertiary);
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.security-indicator svg {
  color: var(--accent);
}

.login-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  color: var(--text-tertiary);
  pointer-events: none;
  display: flex;
  align-items: center;
}

.login-input {
  width: 100%;
  padding: 10px 14px 10px 38px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 13.5px;
  transition: all 0.15s ease;
}

.login-input.with-toggle {
  padding-right: 38px;
}

.login-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
  background: var(--bg-surface);
}

.btn-toggle-password {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease;
}

.btn-toggle-password:hover {
  color: var(--text-primary);
}

/* Options */
.login-options-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
}

.remember-checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.remember-checkbox {
  accent-color: var(--accent);
  cursor: pointer;
}

.login-session-info {
  color: var(--text-tertiary);
  font-size: 11px;
}

/* Submit button */
.btn-login-submit {
  width: 100%;
  height: 44px;
  background: var(--accent) !important;
  color: #041429 !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  border-radius: var(--radius-md) !important;
  border: none !important;
  box-shadow: 0 4px 16px -2px rgba(16, 185, 129, 0.45) !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease !important;
  margin-top: 4px;
}

.btn-login-submit:hover:not(:disabled) {
  background: var(--accent-bright) !important;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px -2px rgba(16, 185, 129, 0.55) !important;
}

.btn-login-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-submit-inner,
.btn-loading-inner {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.spinner-sm {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(4, 20, 41, 0.3);
  border-top-color: #041429;
  border-radius: 50%;
  animation: spinAnim 0.7s infinite linear;
}

@keyframes spinAnim {
  to { transform: rotate(360deg); }
}

/* Footer */
.login-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px solid var(--border-subtle);
  font-size: 12px;
}

.login-back-link {
  color: var(--text-tertiary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: color 0.15s ease;
}

.login-back-link:hover {
  color: var(--accent);
}

.footer-sep {
  color: var(--border-default);
}

/* ─── KPI OVERVIEW BAR ─── */
.cms-kpi-section {
  padding: 24px 0 16px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
}

.kpi-card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  transition: all 0.2s ease;
}

.kpi-card:hover {
  border-color: var(--border-default);
  background: var(--bg-surface);
}

.kpi-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-icon.accent-emerald { background: rgba(16, 185, 129, 0.1); color: var(--accent); }
.kpi-icon.accent-blue { background: rgba(56, 189, 248, 0.1); color: #38bdf8; }
.kpi-icon.accent-amber { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.kpi-icon.accent-purple { background: rgba(168, 85, 247, 0.1); color: #c084fc; }

.kpi-content {
  flex-grow: 1;
}

.kpi-value {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
  line-height: 1.1;
  color: var(--text-primary);
}

.kpi-sub {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-tertiary);
}

.kpi-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.kpi-badge {
  font-size: 10.5px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: var(--radius-pill);
  align-self: flex-start;
}

.kpi-badge.success {
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent);
}

.kpi-badge.info {
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
}

/* ─── NAVIGATION TABS ─── */
.cms-nav-tabs {
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(9, 9, 11, 0.94);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  position: sticky;
  top: 56px;
  z-index: 40;
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.4);
}

.tabs-inner {
  display: flex;
  gap: 4px;
  overflow-x: auto;
}

.tab-link {
  background: transparent;
  color: var(--text-secondary);
  font-size: 13.5px;
  font-weight: 500;
  padding: 13px 18px;
  border-bottom: 2px solid transparent;
  border-top: none;
  border-left: none;
  border-right: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.tab-link:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.03);
}

.tab-link.active {
  color: var(--accent);
  font-weight: 600;
  border-bottom-color: var(--accent);
  background: rgba(16, 185, 129, 0.04);
}

.tab-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-secondary);
  font-family: var(--font-mono);
}

.tab-link.active .tab-badge {
  background: rgba(16, 185, 129, 0.2);
  color: var(--accent);
}

/* ─── TOOLBAR & FILTERS ─── */
.cms-main-content {
  padding-top: 24px;
}

.cms-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
  flex-wrap: wrap;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  padding: 12px 16px;
  border-radius: var(--radius-lg);
}

.toolbar-search-wrap {
  position: relative;
  min-width: 280px;
  flex-grow: 1;
}

.toolbar-search-wrap svg {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
  pointer-events: none;
}

.toolbar-search-wrap input {
  width: 100%;
  padding: 9px 36px 9px 38px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 13.5px;
  transition: border-color 0.15s;
}

.toolbar-search-wrap input:focus {
  outline: none;
  border-color: var(--accent);
}

.clear-search {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  font-size: 18px;
  cursor: pointer;
  line-height: 1;
}

.clear-search:hover {
  color: var(--text-primary);
}

.toolbar-actions-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.toolbar-select {
  padding: 9px 14px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
}

.toolbar-select:focus {
  outline: none;
  border-color: var(--accent);
  color: var(--text-primary);
}

.view-switcher {
  display: flex;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.view-btn {
  padding: 8px 12px;
  background: transparent;
  border: none;
  color: var(--text-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.view-btn.active {
  background: var(--bg-surface);
  color: var(--accent);
}

/* Results Counter Bar */
.cms-results-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  padding: 2px 4px;
  font-size: 12.5px;
  color: var(--text-tertiary);
  flex-wrap: wrap;
}

.results-count strong {
  color: var(--text-primary);
}

.results-filtered-pill {
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  font-size: 11px;
  font-weight: 500;
}

.results-badge-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge-stat {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 9px;
  border-radius: var(--radius-pill);
  font-size: 11.5px;
  font-weight: 500;
}

.badge-stat.active-stat {
  background: rgba(16, 185, 129, 0.12);
  color: var(--accent);
}

.dot-sm {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

.badge-stat.featured-stat {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
}

/* ─── GRID VIEW ─── */
.cms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
}

.cms-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.25s ease;
  position: relative;
}

.cms-card:hover {
  border-color: var(--border-default);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cms-card.is-featured {
  border-color: rgba(245, 158, 11, 0.4);
}

.cms-card.is-draft {
  opacity: 0.7;
}

.cms-card-preview {
  position: relative;
  height: 180px;
  background: #09090b;
  overflow: hidden;
  border-bottom: 1px solid var(--border-subtle);
}

.cms-card-preview:hover .thumbnail-inner {
  transform: scale(1.03) translateY(-2px);
}

.preview-hover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(12, 12, 14, 0.88) 0%,
    rgba(12, 12, 14, 0.35) 50%,
    rgba(12, 12, 14, 0.15) 100%
  );
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0;
  transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 5;
  pointer-events: none;
}

.cms-card-preview:hover .preview-hover-overlay {
  opacity: 1;
  pointer-events: auto;
}

.overlay-action {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s;
}

.overlay-action:hover {
  background: var(--accent);
  color: #000;
  border-color: var(--accent);
}

.card-preview-badges {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 4;
}

.preview-tag-industry {
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  color: #ffffff;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.preview-star-btn {
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(6px);
  color: #71717a;
  border: 1px solid rgba(255, 255, 255, 0.15);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.2s;
}

.preview-star-btn.active {
  color: #f59e0b;
}

.cms-card-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.cms-card-topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.cms-card-name {
  font-size: 17px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.25;
}

.cms-card-badge {
  font-size: 10.5px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}

.cms-card-tagline {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.45;
  margin-bottom: 14px;
  flex-grow: 1;
}

.cms-card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.cms-tag-pill {
  font-size: 11px;
  color: var(--text-tertiary);
  background: var(--bg-elevated);
  padding: 2px 7px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-hairline);
}

.cms-tag-more {
  font-size: 11px;
  color: var(--text-muted);
}

.cms-card-metrics {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-base);
  border-radius: var(--radius-md);
  padding: 10px 14px;
  border: 1px solid var(--border-hairline);
  margin-bottom: 16px;
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.m-val {
  font-family: var(--font-mono);
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-primary);
}

.m-lbl {
  font-size: 10px;
  color: var(--text-tertiary);
}

.metric-sep {
  width: 1px;
  height: 20px;
  background: var(--border-hairline);
}

.text-success { color: var(--accent) !important; }
.text-muted { color: var(--text-muted) !important; }
.text-danger { color: #f87171 !important; }

.cms-card-actions {
  display: flex;
  gap: 8px;
  border-top: 1px solid var(--border-hairline);
  padding-top: 14px;
}

.card-act-btn {
  flex: 1;
  padding: 7px 10px;
  font-size: 12px;
}

/* ─── TABLE VIEW ─── */
.cms-table-wrapper {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow-x: auto;
}

.cms-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}

.cms-table th {
  background: var(--bg-elevated);
  color: var(--text-tertiary);
  font-weight: 600;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.cms-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-hairline);
  color: var(--text-secondary);
}

.cms-table tr:hover td {
  background: rgba(255, 255, 255, 0.015);
}

.table-star-btn {
  background: transparent;
  color: var(--text-muted);
  font-size: 15px;
  cursor: pointer;
}

.table-star-btn.active {
  color: #f59e0b;
}

.table-tpl-info {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.tpl-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-top: 4px;
  flex-shrink: 0;
}

.table-name {
  color: var(--text-primary);
  font-size: 14px;
  display: block;
}

.table-slug {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.table-tagline {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.pill-industry {
  font-family: var(--font-mono);
  font-size: 11px;
  padding: 2px 7px;
  background: var(--bg-elevated);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
}

.accent-swatch-box {
  display: flex;
  align-items: center;
  gap: 8px;
}

.swatch {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.swatch-code {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-tertiary);
}

.tech-tags-condensed {
  font-size: 11.5px;
  color: var(--text-tertiary);
}

.status-toggle-pill {
  padding: 3px 9px;
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.status-active {
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent);
}

.status-draft {
  background: rgba(113, 113, 122, 0.2);
  color: var(--text-muted);
}

.table-actions {
  display: flex;
  gap: 6px;
}

.tbl-action-btn {
  background: var(--bg-elevated);
  border: 1px solid var(--border-hairline);
  color: var(--text-secondary);
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tbl-action-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-default);
}

/* ─── EMPTY STATE ─── */
.cms-empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-tertiary);
}

.cms-empty-state svg {
  width: 48px;
  height: 48px;
  opacity: 0.3;
  margin-bottom: 14px;
}

.cms-empty-state h3 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.cms-empty-state p {
  font-size: 13.5px;
  margin-bottom: 18px;
}

/* ─── ANALYTICS TAB STYLES ─── */
.analytics-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
}

.analytics-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 28px;
}

.card-heading {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.chart-bars-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-row {
  display: grid;
  grid-template-columns: 180px 1fr 140px;
  align-items: center;
  gap: 16px;
  font-size: 12.5px;
}

.cr-label {
  color: var(--text-secondary);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cr-track {
  height: 8px;
  background: var(--bg-elevated);
  border-radius: var(--radius-pill);
  overflow: hidden;
}

.cr-fill {
  height: 100%;
  border-radius: var(--radius-pill);
}

.cr-fill.emerald { background: var(--accent); }
.cr-fill.blue { background: #38bdf8; }
.cr-fill.amber { background: #f59e0b; }
.cr-fill.purple { background: #c084fc; }

.cr-val {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-primary);
  text-align: right;
}

.device-pie-mock {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.device-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px;
  background: var(--bg-elevated);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-hairline);
}

.di-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: var(--bg-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.di-info {
  flex-grow: 1;
}

.di-info strong {
  display: block;
  font-size: 13.5px;
  color: var(--text-primary);
}

.di-info span {
  font-size: 11.5px;
  color: var(--text-tertiary);
}

.di-val {
  font-size: 11.5px;
  font-weight: 600;
}

/* ─── DEPLOY TAB ─── */
.deploy-card, .logs-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 32px;
}

.deploy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 16px;
}

.deploy-header h3 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.deploy-header p {
  font-size: 13px;
  color: var(--text-secondary);
}

.check-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.check-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 20px;
  background: var(--bg-elevated);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-hairline);
}

.ci-badge {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
}

.ci-badge.pass {
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent);
}

.ci-text strong {
  display: block;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.ci-text p {
  font-size: 12.5px;
  color: var(--text-secondary);
}

/* ─── LOGS TAB ─── */
.logs-title {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 24px;
}

.log-timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  padding-left: 20px;
}

.log-timeline::before {
  content: '';
  position: absolute;
  top: 10px;
  bottom: 10px;
  left: 5px;
  width: 2px;
  background: var(--border-subtle);
}

.log-item {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.log-dot {
  position: absolute;
  left: -20px;
  top: 6px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 4px var(--bg-surface);
}

.log-time {
  font-size: 11px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
}

.log-desc strong {
  font-size: 14px;
  color: var(--text-primary);
}

.log-desc p {
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-top: 2px;
}

/* ─── MODALS ─── */
.cms-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.cms-modal-dialog {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 680px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
}

.cms-modal-dialog.modal-preview-wide {
  max-width: 1180px;
  height: 88vh;
}

.cms-modal-dialog.modal-confirm-delete {
  max-width: 440px;
  padding: 28px;
}

.cms-modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-sub {
  font-size: 11.5px;
  color: var(--accent);
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.modal-close-btn {
  background: transparent;
  color: var(--text-tertiary);
  font-size: 24px;
  cursor: pointer;
  line-height: 1;
}

.modal-close-btn:hover {
  color: var(--text-primary);
}

.cms-modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-col {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-col label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.form-col input[type="text"],
.form-col input[type="number"],
.form-col textarea {
  width: 100%;
  padding: 9px 12px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 13px;
}

.form-col input:focus, .form-col textarea:focus {
  border-color: var(--accent);
}

.color-picker-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-box {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  background: transparent;
}

.section-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dynamic-inputs-list, .dynamic-tags-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dynamic-input-row, .dynamic-tag-row {
  display: flex;
  gap: 8px;
}

.btn-remove {
  background: rgba(248, 113, 113, 0.15);
  color: #f87171;
  border: none;
  width: 32px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 16px;
}

.cms-modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Preview Modal Specifics */
.preview-header {
  padding: 12px 20px;
}

.prev-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.preview-badge {
  font-family: var(--font-mono);
  font-size: 10.5px;
  padding: 2px 8px;
  background: var(--bg-elevated);
  border-radius: var(--radius-pill);
  color: var(--accent);
}

.preview-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.viewport-toggles {
  display: flex;
  gap: 4px;
  background: var(--bg-elevated);
  padding: 3px;
  border-radius: var(--radius-md);
}

.vp-btn {
  padding: 6px 10px;
  background: transparent;
  color: var(--text-tertiary);
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.vp-btn.active {
  background: var(--bg-surface);
  color: var(--accent);
}

.prev-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.preview-iframe-wrapper {
  flex-grow: 1;
  background: #09090b;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  padding: 16px;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  background: #ffffff;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  transition: width 0.3s ease;
}

.preview-iframe-wrapper.tablet .preview-iframe {
  width: 768px;
}

.preview-iframe-wrapper.mobile .preview-iframe {
  width: 375px;
}

/* Delete Confirm Modal */
.del-title {
  font-size: 18px;
  font-weight: 700;
  color: #f87171;
  margin-bottom: 10px;
}

.del-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 24px;
}

.del-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ─── CMS TOAST ─── */
.cms-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--accent);
  border-radius: var(--radius-md);
  padding: 12px 18px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  transform: translateY(80px);
  opacity: 0;
  transition: all 0.25s var(--ease-out-quart);
  z-index: 1100;
}

.cms-toast svg {
  color: var(--accent);
}

.cms-toast.show {
  transform: translateY(0);
  opacity: 1;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .analytics-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .cms-header-inner {
    flex-direction: column;
    align-items: flex-start;
  }
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  .cms-toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  .toolbar-filters {
    flex-direction: column;
    align-items: stretch;
  }
  .form-grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
