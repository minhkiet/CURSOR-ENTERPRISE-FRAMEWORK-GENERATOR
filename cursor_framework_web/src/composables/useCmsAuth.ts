import { ref } from 'vue'

const AUTH_STORAGE_KEY = 'cef_cms_auth_session'
const FIXED_USER = 'admin'
const FIXED_PASS = 'admin@123'

export interface CmsAuthSession {
  isAuthenticated: boolean
  user: string
  role: string
  loginTime: string
}

// Global reactive state shared across components
const isAuthenticated = ref(false)
const currentUser = ref<string | null>(null)
const sessionInfo = ref<CmsAuthSession | null>(null)

export function useCmsAuth() {
  function checkAuth(): boolean {
    try {
      const stored = localStorage.getItem(AUTH_STORAGE_KEY) || sessionStorage.getItem(AUTH_STORAGE_KEY)
      if (stored) {
        const parsed: CmsAuthSession = JSON.parse(stored)
        if (parsed.isAuthenticated && parsed.user === FIXED_USER) {
          isAuthenticated.value = true
          currentUser.value = parsed.user
          sessionInfo.value = parsed
          return true
        }
      }
    } catch (_e) {
      // Ignore JSON parse errors
    }
    isAuthenticated.value = false
    currentUser.value = null
    sessionInfo.value = null
    return false
  }

  function login(user: string, pass: string, remember: boolean = true): { success: boolean; message: string } {
    const cleanUser = user.trim()
    const cleanPass = pass.trim()

    if (!cleanUser || !cleanPass) {
      return { success: false, message: 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.' }
    }

    if (cleanUser !== FIXED_USER || cleanPass !== FIXED_PASS) {
      return { success: false, message: 'Tên đăng nhập hoặc mật khẩu không chính xác! Vui lòng thử lại.' }
    }

    const session: CmsAuthSession = {
      isAuthenticated: true,
      user: FIXED_USER,
      role: 'Super Admin',
      loginTime: new Date().toLocaleString('vi-VN')
    }

    try {
      const serialized = JSON.stringify(session)
      if (remember) {
        localStorage.setItem(AUTH_STORAGE_KEY, serialized)
        sessionStorage.removeItem(AUTH_STORAGE_KEY)
      } else {
        sessionStorage.setItem(AUTH_STORAGE_KEY, serialized)
        localStorage.removeItem(AUTH_STORAGE_KEY)
      }
    } catch (e) {
      console.warn('Storage quota error', e)
    }

    isAuthenticated.value = true
    currentUser.value = FIXED_USER
    sessionInfo.value = session
    return { success: true, message: `Chào mừng trở lại, ${FIXED_USER}!` }
  }

  function logout(): void {
    try {
      localStorage.removeItem(AUTH_STORAGE_KEY)
      sessionStorage.removeItem(AUTH_STORAGE_KEY)
    } catch (_e) {}
    isAuthenticated.value = false
    currentUser.value = null
    sessionInfo.value = null
  }

  return {
    isAuthenticated,
    currentUser,
    sessionInfo,
    checkAuth,
    login,
    logout,
    CREDENTIALS_HINT: {
      user: FIXED_USER,
      pass: FIXED_PASS
    }
  }
}
