<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)

type MethodKey = 'gui' | 'powershell' | 'python' | 'manual'
const activeMethod = ref<MethodKey>('gui')

type Tone = 'success' | 'warning' | 'danger' | 'info'
interface FaqItem {
  q: string
  a: string
}
interface VerifyItem {
  ok: boolean
  label: string
  hint?: string
}
interface InstallMethod {
  key: MethodKey
  badge: string
  badgeTone: Tone
  title: string
  oneLiner: string
  forWho: string
  duration: string
  difficulty: 'Easy' | 'Medium' | 'Advanced'
  os: string[]
  steps: { title: string; detail: string; code?: string; codeLabel?: string; tip?: string }[]
  verify: VerifyItem[]
  troubleshooting: { problem: string; solution: string }[]
}

const methods: InstallMethod[] = [
  {
    key: 'gui',
    badge: 'Recommended',
    badgeTone: 'success',
    title: 'Windows GUI installer',
    oneLiner: 'Tải 2 file, double-click, bấm Install. Dành cho người mới trên Windows.',
    forWho: 'Người mới, không quen PowerShell, dùng Windows 10/11.',
    duration: '3 phút',
    difficulty: 'Easy',
    os: ['Windows 10', 'Windows 11'],
    steps: [
      {
        title: 'Truy cập trang Release mới nhất',
        detail: 'Mở trình duyệt và vào GitHub Releases. Tìm bản Latest (ví dụ v1.3.0).',
        code: 'https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/releases/latest',
        codeLabel: 'URL'
      },
      {
        title: 'Tải 2 file về cùng một thư mục',
        detail: 'Trong phần Assets, tải cả hai file và đặt chung một folder (ví dụ Downloads\\cef).',
        code: 'cursor-setup.exe    (~162 MB, self-contained, không cần .NET)\ncursor-setup.zip    (~22 MB, payload framework)',
        codeLabel: 'Files'
      },
      {
        title: 'Chạy cursor-setup.exe',
        detail: 'Double-click file exe. Nếu Windows SmartScreen hỏi, chọn "More info" → "Run anyway".',
        tip: 'SmartScreen cảnh báo là bình thường vì file chưa được code-sign. Bạn có thể kiểm tra checksum trên trang Release.'
      },
      {
        title: 'Chọn thư mục đích',
        detail: 'GUI mặc định đề xuất %USERPROFILE%\\.cursor (đúng chuẩn Cursor IDE). Bạn có thể đổi nếu muốn.',
        code: '%USERPROFILE%\\.cursor',
        codeLabel: 'Đường dẫn mặc định'
      },
      {
        title: 'Bấm Install và chờ',
        detail: 'GUI sẽ hiển thị thanh tiến trình và log extract. Khi xong, một thông báo xác nhận sẽ hiện ra cùng với file-count sanity check.',
        tip: 'Quá trình thường mất 10-30 giây tùy tốc độ ổ đĩa.'
      },
      {
        title: 'Restart Cursor IDE',
        detail: 'Đóng hoàn toàn Cursor (File → Exit) rồi mở lại. Cursor sẽ tự động load các rule và skill mới từ .cursor/.'
      }
    ],
    verify: [
      { ok: true, label: 'Thư mục .cursor tồn tại và chứa file', hint: 'Mở File Explorer → %USERPROFILE%\\.cursor' },
      { ok: true, label: 'Cursor hiển thị danh sách Rules/Skills', hint: 'Trong Cursor: Settings → Rules, hoặc mở chat và gõ /' },
      { ok: true, label: 'Không có lỗi trong log install', hint: 'GUI hiển thị "Extracted 605 files" khi thành công' }
    ],
    troubleshooting: [
      {
        problem: 'Windows SmartScreen chặn file exe',
        solution: 'Click "More info" → "Run anyway". Đây là cảnh báo bình thường vì file chưa được code-sign công khai.'
      },
      {
        problem: 'Lỗi "Permission denied" khi extract',
        solution: 'Chuột phải exe → "Run as administrator". Tránh cài vào Program Files.'
      },
      {
        problem: 'Cursor không nhận rules sau khi cài',
        solution: 'Đảm bảo đã đóng hoàn toàn Cursor (kill process trong Task Manager). Cursor chỉ đọc .cursor/ khi khởi động.'
      },
      {
        problem: 'File zip báo "corrupted"',
        solution: 'Tải lại file zip. Có thể mạng bị ngắt giữa chừng. Kiểm tra dung lượng phải đúng ~22 MB.'
      }
    ]
  },
  {
    key: 'powershell',
    badge: 'One-liner',
    badgeTone: 'info',
    title: 'PowerShell one-liner',
    oneLiner: 'Một lệnh duy nhất, tự động tải và cài. Dành cho người dùng PowerShell.',
    forWho: 'Dev quen terminal, Windows / PowerShell 5.1+ / PowerShell 7.',
    duration: '2 phút',
    difficulty: 'Easy',
    os: ['Windows 10', 'Windows 11', 'PowerShell 7'],
    steps: [
      {
        title: 'Mở PowerShell với quyền user thường',
        detail: 'Bấm Win + X → chọn "Windows PowerShell" hoặc "Terminal". KHÔNG cần Administrator.',
        tip: 'Lệnh install cố tình KHÔNG yêu cầu admin để tránh cài đặt hệ thống. Nó chỉ ghi vào thư mục user.'
      },
      {
        title: 'Dán lệnh sau và Enter',
        detail: 'Lệnh này sẽ tải script install.ps1 từ repo chính thức rồi thực thi nó. Bạn có thể xem source trước tại link URL bên dưới.',
        code: 'irm https://raw.githubusercontent.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/main/install.ps1 | iex',
        codeLabel: 'Lệnh cài đặt'
      },
      {
        title: 'Đợi script chạy xong',
        detail: 'Script sẽ tải zip, giải nén vào %USERPROFILE%\\.cursor, và in thông báo kết quả. Nếu thành công sẽ thấy dòng "Framework installed successfully".',
        tip: 'Nếu PowerShell báo lỗi "running scripts is disabled", chạy lệnh này một lần rồi thử lại: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned'
      },
      {
        title: 'Restart Cursor IDE',
        detail: 'Đóng và mở lại Cursor để nó nạp các rule và skill mới.'
      }
    ],
    verify: [
      { ok: true, label: 'Terminal in "Framework installed successfully"', hint: 'Dòng cuối cùng của script' },
      { ok: true, label: 'Thư mục .cursor có file', hint: 'ls $env:USERPROFILE\\.cursor' },
      { ok: true, label: 'Cursor load rules bình thường', hint: 'Mở chat trong Cursor và gõ /, sẽ thấy slash commands' }
    ],
    troubleshooting: [
      {
        problem: 'Lỗi "irm : The term \'irm\' is not recognized"',
        solution: 'Bạn đang dùng PowerShell quá cũ. Cập nhật lên PowerShell 7 (pwsh) hoặc dùng cách GUI.'
      },
      {
        problem: 'Lỗi "running scripts is disabled on this system"',
        solution: 'Một lần: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned. Đây là chính sách bảo mật mặc định của Windows.'
      },
      {
        problem: 'Tải về chậm hoặc timeout',
        solution: 'Kiểm tra mạng. Nếu repo chính bị chặn, mirror còn lại: thay đổi main → mirror trong URL.'
      },
      {
        problem: 'Không thấy file .cursor sau khi cài',
        solution: 'Folder ẩn? Bật "Show hidden files" trong Explorer, hoặc gõ echo $env:USERPROFILE trong PowerShell để xem đường dẫn thật.'
      }
    ]
  },
  {
    key: 'python',
    badge: 'For devs',
    badgeTone: 'info',
    title: 'Python package (cursor_framework)',
    oneLiner: 'Cài pip package, chạy Dashboard, scan & index. Cho dev muốn inspect / customize',
    forWho: 'Dev Python, muốn dùng CLI, dashboard, indexer, hoặc TDAM.',
    duration: '4 phút',
    difficulty: 'Medium',
    os: ['Windows', 'macOS', 'Linux'],
    steps: [
      {
        title: 'Yêu cầu môi trường',
        detail: 'Python 3.10+ (3.11 / 3.12 khuyến nghị). pip có sẵn. Khuyến nghị dùng virtualenv hoặc uv để cô lập dependency.',
        code: 'python --version\npip --version',
        codeLabel: 'Kiểm tra'
      },
      {
        title: 'Clone repo và cài dependencies',
        detail: 'Khác với cài Cursor IDE: lần này bạn clone repo để lấy Python package ở source. Sau đó cài requirements. Tất cả subcommands CLI dùng được ngay.',
        code: 'git clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR.git\ncd CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR\npip install -r cursor_framework/requirements.txt',
        codeLabel: 'Terminal',
        tip: 'Repo đặt ở đâu cũng được — không bắt buộc phải là C:\\.cursor. Đây là tool cho dev, không phải rules cho IDE.'
      },
      {
        title: 'Cài đặt package ở chế độ editable',
        detail: 'Editable mode (-e) giúp bạn sửa source code trong cursor_framework/ mà không cần reinstall. Phù hợp khi bạn muốn customize framework.',
        code: 'pip install -e ./cursor_framework',
        codeLabel: 'Terminal'
      },
      {
        title: 'Verify CLI hoạt động',
        detail: 'Sau khi cài, lệnh cursor-framework và python -m cursor_framework đều khả dụng. Version phải khớp với __version__ trong package.',
        code: 'cursor-framework --version\n# hoặc\npython -m cursor_framework --version\n# Cursor Enterprise Framework 1.3.0',
        codeLabel: 'Verify'
      },
      {
        title: 'Khởi động Dashboard',
        detail: 'Chạy serve trong thư mục repo vừa clone. Server stdlib không cần thư viện ngoài. Mở trình duyệt theo URL in trên terminal.',
        code: 'python -m cursor_framework serve --root .cursor --port 8765',
        codeLabel: 'CLI',
        tip: 'Mặc định bind 127.0.0.1 (localhost). Đổi sang --host 0.0.0.0 để truy cập từ máy khác. Production: đặt --auth-token để bảo vệ /api/*.'
      },
      {
        title: 'Thử một số lệnh CLI',
        detail: 'cursor_framework CLI có 11 subcommands. Phổ biến nhất: warm (preload cache), stats (xem số liệu), scan (INDEX khô), ask (one-shot Workflow).',
        code: 'python -m cursor_framework --help\npython -m cursor_framework stats\npython -m cursor_framework ask "summarize the framework"',
        codeLabel: 'Khám phá'
      },
      {
        title: 'Restart Cursor IDE để reload rules',
        detail: 'Package Python là dev tool riêng. Nó KHÔNG tự động cài rules .cursor/ vào Cursor IDE. Nếu bạn muốn dùng rules trong IDE, làm theo 1 trong 3 cách ở tab đầu (GUI / PowerShell / manual).'
      }
    ],
    verify: [
      { ok: true, label: 'cursor-framework --version in đúng số version', hint: 'Hiện tại là 1.3.0' },
      { ok: true, label: 'python -m cursor_framework --help liệt kê 11 subcommands', hint: 'serve, ask, warm, stats, scan, index, graph, clear-cache, serve-graph, tdam' },
      { ok: true, label: 'python -m cursor_framework serve mở được dashboard', hint: 'Truy cập http://127.0.0.1:8765' },
      { ok: true, label: 'python -m cursor_framework stats in JSON số liệu', hint: 'Phải có keys: assets, memory, cache' }
    ],
    troubleshooting: [
      {
        problem: 'ModuleNotFoundError: No module named \'cursor_framework\'',
        solution: 'Bạn quên bước pip install -e ./cursor_framework. Hoặc venv đang không active. Kiểm tra: which python và which pip phải cùng venv.'
      },
      {
        problem: 'pydantic VersionConflict hoặc ImportError pydantic',
        solution: 'Cài đúng phiên bản: pip install "pydantic>=2.0.0". Pydantic v1 và v2 không tương thích — framework yêu cầu v2.'
      },
      {
        problem: 'Lỗi "Permission denied" khi pip install trên Linux/macOS',
        solution: 'KHÔNG dùng sudo pip. Dùng venv: python -m venv .venv && source .venv/bin/activate rồi pip install như bình thường.'
      },
      {
        problem: 'Serve báo "Address already in use"',
        solution: 'Port 8765 đã bị chiếm. Đổi: --port 8766. Hoặc tìm process: netstat -ano | findstr 8765 (Windows), lsof -i :8765 (macOS/Linux).'
      },
      {
        problem: 'tdam subcommand báo "rich not installed"',
        solution: 'TDAM là tùy chọn. Cài thêm: pip install rich. Hoặc bỏ qua nếu không dùng TencentDB Agent Memory.'
      },
      {
        problem: 'Sau khi sửa source code, CLI vẫn chạy code cũ',
        solution: 'Editable mode tự reload khi import. Nếu không: pip install -e ./cursor_framework --force-reinstall --no-deps.'
      }
    ]
  },
  {
    key: 'manual',
    badge: 'For control',
    badgeTone: 'warning',
    title: 'Cài thủ công từ source',
    oneLiner: 'Clone repo, tự build hoặc copy file. Cho dev muốn kiểm soát hoàn toàn.',
    forWho: 'Dev muốn inspect trước khi dùng, muốn modify, hoặc không dùng Windows.',
    duration: '5 phút',
    difficulty: 'Medium',
    os: ['Windows', 'macOS', 'Linux'],
    steps: [
      {
        title: 'Clone repository về máy',
        detail: 'Cần Git cài sẵn. Clone vào một thư mục tạm, KHÔNG clone thẳng vào .cursor/.',
        code: 'git clone https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR.git',
        codeLabel: 'Terminal'
      },
      {
        title: 'Điều hướng vào repo vừa clone',
        detail: 'Mở terminal ở thư mục vừa clone và kiểm tra cấu trúc.',
        code: 'cd CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR\nls .cursor/',
        codeLabel: 'Terminal'
      },
      {
        title: 'Tạo thư mục đích .cursor',
        detail: 'Tạo thư mục .cursor trong thư mục user. Đây là nơi Cursor đọc rules và skills.',
        code: '# Windows PowerShell\nNew-Item -ItemType Directory -Path $env:USERPROFILE\\.cursor -Force\n\n# macOS / Linux\nmkdir -p ~/.cursor',
        codeLabel: 'Terminal'
      },
      {
        title: 'Copy nội dung .cursor từ repo sang',
        detail: 'Copy TOÀN BỘ thư mục .cursor từ repo clone vào thư mục đích. Quan trọng: phải copy cả subfolder, không phải chỉ file lẻ.',
        code: '# Windows PowerShell\nCopy-Item -Path .\\.cursor\\* -Destination $env:USERPROFILE\\.cursor\\ -Recurse -Force\n\n# macOS / Linux\ncp -r ./.cursor/* ~/.cursor/',
        codeLabel: 'Terminal',
        tip: 'Nếu dùng Finder hoặc Explorer thủ công: mở repo/.cursor/, chọn tất cả, kéo thả vào ~/.cursor/.'
      },
      {
        title: 'Kiểm tra file đã copy đủ',
        detail: 'Verify cấu trúc thư mục đích có đầy đủ các folder con (rules, skills, agents, knowledge, ...).',
        code: '# Windows PowerShell\nGet-ChildItem $env:USERPROFILE\\.cursor\n\n# macOS / Linux\nls ~/.cursor/',
        codeLabel: 'Verify'
      },
      {
        title: 'Restart Cursor IDE',
        detail: 'Đóng và mở lại Cursor. Các rule và skill sẽ xuất hiện ngay.'
      }
    ],
    verify: [
      { ok: true, label: 'Folder .cursor có subfolder rules, skills, agents', hint: 'Dùng ls hoặc Get-ChildItem' },
      { ok: true, label: 'Cursor load rules bình thường', hint: 'Mở chat trong Cursor, gõ / sẽ thấy slash commands' },
      { ok: true, label: 'Không bị overwrite rules cũ của bạn', hint: 'Cursor ưu tiên project .cursor/ trước global' }
    ],
    troubleshooting: [
      {
        problem: 'Sau khi copy, Cursor không thấy rules mới',
        solution: 'Đảm bảo copy cả thư mục con (recursive). Cursor yêu cầu đúng cấu trúc: .cursor/rules/*.mdc mới hoạt động.'
      },
      {
        problem: 'Conflict với project .cursor/ hiện có',
        solution: 'Cursor ưu tiên project-level .cursor/ hơn global. Để dùng global, bạn phải xóa hoặc merge với project .cursor/.'
      },
      {
        problem: 'Trên macOS/Linux, ls thấy nhưng Cursor không load',
        solution: 'Kiểm tra quyền đọc: ls -la ~/.cursor. Đảm bảo user hiện tại có quyền read các file .mdc.'
      },
      {
        problem: 'Muốn cập nhật khi có phiên bản mới',
        solution: 'Pull repo mới (git pull), rồi copy lại. Hoặc dùng cách PowerShell one-liner cho các bản sau.'
      }
    ]
  }
]

const faqs: FaqItem[] = [
  {
    q: 'Framework có tương thích với Cursor IDE miễn phí không?',
    a: 'Có. Framework chỉ cần Cursor đọc được thư mục .cursor/ ở user-level. Mọi gói Cursor (Free, Pro, Business) đều dùng được. Tương tự với Claude Code, Windsurf, Cline, Roo Code, Vibe Code.'
  },
  {
    q: 'Cài framework có làm chậm máy không?',
    a: 'Không. Framework là các file .mdc (Markdown) và .md - văn bản thuần. Cursor chỉ load chúng khi cần, nhờ cơ chế context router. Tổng dung lượng khoảng 22 MB sau khi giải nén.'
  },
  {
    q: 'Có cần cài Python hay Node.js để dùng framework không?',
    a: 'Không. Framework là tập rules và skills cho AI agent, không phải phần mềm chạy trên máy bạn. Chỉ cần Cursor IDE đọc file là đủ. Repo Python (cursor_framework) chỉ dùng nếu bạn muốn customize framework.'
  },
  {
    q: 'Làm sao để gỡ cài đặt?',
    a: 'Đơn giản xóa thư mục %USERPROFILE%\\.cursor (Windows) hoặc ~/.cursor (macOS/Linux). Restart Cursor. Không có registry, không có background service.'
  },
  {
    q: 'Có cần backup rules cũ của tôi trước khi cài không?',
    a: 'Cài đặt không ghi đè rules cũ nếu bạn cài vào thư mục user-level (mặc định). Tuy nhiên nếu bạn đã có .cursor/ trong một project, Cursor sẽ merge - project-level ưu tiên.'
  },
  {
    q: 'Tôi có thể dùng framework cho nhiều máy không?',
    a: 'Được. Mỗi máy cài một lần là xong. Nếu muốn đồng bộ rules giữa nhiều máy, hãy fork repo rồi trỏ URL ở bước cài về fork của bạn.'
  }
]

const activeFaq = ref<number | null>(null)
function toggleFaq(i: number) {
  activeFaq.value = activeFaq.value === i ? null : i
}

const currentMethod = computed(() => methods.find((m) => m.key === activeMethod.value)!)

// Sidebar nav
const navItems = computed(() => [
  { id: 'overview', label: 'Tổng quan' },
  { id: 'choose', label: 'Chọn cách cài' },
  { id: 'prerequisites', label: 'Yêu cầu trước' },
  { id: 'install', label: 'Cài đặt' },
  { id: 'verify', label: 'Xác minh' },
  { id: 'troubleshoot', label: 'Xử lý lỗi' },
  { id: 'faq', label: 'FAQ' }
])

const activeSection = ref<string>('overview')

function setMethod(key: MethodKey) {
  activeMethod.value = key
  nextTick(() => {
    document.getElementById('install')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

let observer: IntersectionObserver | null = null

function setupScrollSpy() {
  const sections = navItems.value.map((n) => document.getElementById(n.id)).filter(Boolean) as HTMLElement[]
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) activeSection.value = e.target.id
      })
    },
    { rootMargin: '-30% 0px -60% 0px', threshold: 0 }
  )
  sections.forEach((s) => observer!.observe(s))
}

function scrollToSection(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const { observe } = useIntersectionObserver()

onMounted(() => {
  if (sectionRef.value) {
    observe(sectionRef.value, () => {
      isVisible.value = true
    }, { threshold: 0.05 })
  }
  setupScrollSpy()
})

onUnmounted(() => {
  observer?.disconnect()
})

// Syntax highlight tokens (lightweight regex-based for PowerShell + bash)
function highlightCode(code: string): string {
  // Escape HTML
  let s = code
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  // Comments (# ...)
  s = s.replace(/(#[^\n]*)/g, '<span class="t-comment">$1</span>')
  // Strings ("...")
  s = s.replace(/("[^"]*")/g, '<span class="t-string">$1</span>')
  // Commands (PowerShell verbs + common shell commands)
  s = s.replace(
    /\b(irm|iex|cd|ls|cp|mkdir|git|New-Item|Copy-Item|Get-ChildItem|Set-ExecutionPolicy|curl|wget|node|npm|npx|pip|python3|python)\b/g,
    '<span class="t-cmd">$1</span>'
  )
  // Flags
  s = s.replace(/(\s)(-{1,2}[\w-]+)/g, '$1<span class="t-flag">$2</span>')
  // URLs
  s = s.replace(/(https?:\/\/[^\s]+)/g, '<span class="t-string">$1</span>')
  return s
}

async function copyCode(text: string) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    return false
  }
}

const copiedKey = ref<string | null>(null)
async function handleCopy(code: string, key: string) {
  const ok = await copyCode(code)
  if (ok) {
    copiedKey.value = key
    setTimeout(() => {
      if (copiedKey.value === key) copiedKey.value = null
    }, 1800)
  }
}
</script>

<template>
  <div class="install-view" ref="sectionRef">
    <!-- HERO ────────────────────────────────────────────────────────────── -->
    <section class="ins-hero">
      <div class="container">
        <div class="ins-hero-content">
          <div class="section-label">Installation Guide</div>
          <h1 class="ins-title">
            Cài framework trong vài phút.<br />
            <span class="ins-title-accent">Ba cách, tùy bạn chọn.</span>
          </h1>
          <p class="ins-subtitle">
            Hướng dẫn đầy đủ cho cả người mới và dev có kinh nghiệm.     Mỗi bước đều có screenshot mô tả,
    lệnh copy được, và mục kiểm tra xác minh. Không cần dò code cũng làm được.
          </p>

          <div class="ins-quickstats">
            <div class="ins-quickstat">
              <div class="ins-quickstat-value">3 phút</div>
              <div class="ins-quickstat-label">Thời gian trung bình</div>
            </div>
          <div class="ins-quickstat">
            <div class="ins-quickstat-value">4</div>
            <div class="ins-quickstat-label">Cách cài đặt</div>
          </div>
            <div class="ins-quickstat">
              <div class="ins-quickstat-value">3 OS</div>
              <div class="ins-quickstat-label">Win / macOS / Linux</div>
            </div>
            <div class="ins-quickstat">
              <div class="ins-quickstat-value">0</div>
              <div class="ins-quickstat-label">Phụ thuộc hệ thống</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- MAIN LAYOUT ──────────────────────────────────────────────────────── -->
    <section class="ins-main">
      <div class="container">
        <div class="ins-grid">
          <!-- SIDEBAR NAV (sticky) -->
          <aside class="ins-sidebar">
            <div class="ins-sidebar-inner">
              <div class="ins-sidebar-label">Mục lục</div>
              <nav class="ins-sidenav" aria-label="Installation sections">
                <button
                  v-for="item in navItems"
                  :key="item.id"
                  class="ins-sidenav-item"
                  :class="{ active: activeSection === item.id }"
                  @click="scrollToSection(item.id)"
                >
                  <span class="ins-sidenav-dot"></span>
                  {{ item.label }}
                </button>
              </nav>

              <div class="ins-sidebar-card">
                <div class="ins-sidebar-card-label">Cần trợ giúp?</div>
                <p class="ins-sidebar-card-text">
                  Mở issue trên GitHub hoặc xem FAQ bên dưới.
                </p>
                <a
                  href="https://github.com/minhkiet/CURSOR-ENTERPRISE-FRAMEWORK-GENERATOR/issues"
                  target="_blank"
                  rel="noopener"
                  class="ins-sidebar-card-link"
                >
                  GitHub Issues
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M7 17L17 7M17 7H8M17 7V16" />
                  </svg>
                </a>
              </div>
            </div>
          </aside>

          <!-- CONTENT -->
          <div class="ins-content">
            <!-- 1. OVERVIEW -->
            <article id="overview" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">01</div>
                <div>
                  <h2 class="ins-section-title">Tổng quan</h2>
                  <p class="ins-section-sub">
                    Bạn sẽ cài framework Cursor Enterprise vào thư mục <code>~/.cursor/</code>.
                    Framework chỉ là tập file văn bản (rules, skills, agents) mà Cursor IDE
                    tự động đọc. Không cần Python, Node, hay service nào chạy nền.
                  </p>
                </div>
              </header>

              <div class="ins-callout">
                <div class="ins-callout-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10" />
                    <path d="M12 8v4M12 16h.01" />
                  </svg>
                </div>
                <div>
                  <div class="ins-callout-title">Quan trọng</div>
                  <p class="ins-callout-text">
                    Framework cài vào <strong>user-level</strong> (<code>%USERPROFILE%\.cursor\</code>
                    trên Windows, <code>~/.cursor/</code> trên macOS/Linux). Nó áp dụng cho tất cả
                    project bạn mở trong Cursor, nhưng project-level <code>.cursor/</code> (nếu có)
                    sẽ được ưu tiên hơn.
                  </p>
                </div>
              </div>

              <div class="ins-callout ins-callout-dev">
                <div class="ins-callout-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <polyline points="16 18 22 12 16 6" />
                    <polyline points="8 6 2 12 8 18" />
                  </svg>
                </div>
                <div>
                  <div class="ins-callout-title">Bạn là dev Python? Bạn cần thêm bước này.</div>
                  <p class="ins-callout-text">
                    Framework có 2 phần: <strong>rules/skills</strong> (file văn bản, đọc bằng Cursor)
                    và <strong>Python package <code>cursor_framework</code></strong> (CLI &
                    dashboard cho dev muốn build / scan / index). 3 cách cài bên dưới (GUI / PowerShell
                    / manual) chỉ cài phần rules. Để cài thêm Python package, chuyển sang tab
                    <strong>Python package (cursor_framework)</strong> ở mục 02.
                  </p>
                </div>
              </div>
            </article>

            <!-- 2. CHOOSE METHOD -->
            <article id="choose" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">02</div>
                <div>
                  <h2 class="ins-section-title">Chọn cách cài</h2>
                  <p class="ins-section-sub">
                    Chọn cách phù hợp với bạn. Bạn có thể đổi ý giữa chừng - không có gì bị khóa.
                  </p>
                </div>
              </header>

              <div class="ins-method-grid">
                <button
                  v-for="m in methods"
                  :key="m.key"
                  class="ins-method-card"
                  :class="{ active: activeMethod === m.key }"
                  @click="setMethod(m.key)"
                >
                  <div class="ins-method-card-top">
                    <span class="ins-method-badge" :class="'tone-' + m.badgeTone">
                      {{ m.badge }}
                    </span>
                    <span class="ins-method-difficulty" :class="'diff-' + m.difficulty.toLowerCase()">
                      {{ m.difficulty }}
                    </span>
                  </div>
                  <h3 class="ins-method-title">{{ m.title }}</h3>
                  <p class="ins-method-oneliner">{{ m.oneLiner }}</p>
                  <div class="ins-method-meta">
                    <div class="ins-method-meta-row">
                      <span class="ins-method-meta-label">Dành cho</span>
                      <span class="ins-method-meta-value">{{ m.forWho }}</span>
                    </div>
                    <div class="ins-method-meta-row">
                      <span class="ins-method-meta-label">Thời gian</span>
                      <span class="ins-method-meta-value">{{ m.duration }}</span>
                    </div>
                    <div class="ins-method-meta-row">
                      <span class="ins-method-meta-label">Hệ điều hành</span>
                      <span class="ins-method-meta-value">{{ m.os.join(' · ') }}</span>
                    </div>
                  </div>
                  <div class="ins-method-cta">
                    Chọn cách này
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M5 12h14M13 6l6 6-6 6" />
                    </svg>
                  </div>
                </button>
              </div>
            </article>

            <!-- 3. PREREQUISITES -->
            <article id="prerequisites" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">03</div>
                <div>
                  <h2 class="ins-section-title">Yêu cầu trước khi cài</h2>
                  <p class="ins-section-sub">
                    Đa số bạn đã có sẵn. Kiểm tra nhanh trong 30 giây.
                  </p>
                </div>
              </header>

              <div class="ins-prereq-grid">
                <div class="ins-prereq">
                  <div class="ins-prereq-check">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </div>
                  <div class="ins-prereq-body">
                    <div class="ins-prereq-title">Cursor IDE (bất kỳ gói nào)</div>
                    <p class="ins-prereq-desc">Free, Pro, Business đều được. Tương tự: Claude Code, Windsurf, Cline, Roo Code, Vibe Code.</p>
                  </div>
                </div>

                <div class="ins-prereq">
                  <div class="ins-prereq-check">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </div>
                  <div class="ins-prereq-body">
                    <div class="ins-prereq-title">Quyền ghi vào thư mục user</div>
                    <p class="ins-prereq-desc">Không cần admin. Mặc định user thường đã có quyền ghi vào <code>~/.cursor/</code>.</p>
                  </div>
                </div>

                <div class="ins-prereq">
                  <div class="ins-prereq-check">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </div>
                  <div class="ins-prereq-body">
                    <div class="ins-prereq-title">Ổ đĩa trống ~50 MB</div>
                    <p class="ins-prereq-desc">Sau khi giải nén framework chiếm khoảng 22 MB. Dư sức cho mọi máy.</p>
                  </div>
                </div>

                <div class="ins-prereq">
                  <div class="ins-prereq-check ins-prereq-check-optional">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="9" />
                      <path d="M12 8v8" />
                    </svg>
                  </div>
                  <div class="ins-prereq-body">
                    <div class="ins-prereq-title">Git <span class="ins-prereq-optional">(chỉ cần cho cách thủ công)</span></div>
                    <p class="ins-prereq-desc">Nếu dùng GUI hoặc PowerShell one-liner thì không cần Git. Còn không thì Git đi kèm Cursor.</p>
                  </div>
                </div>
              </div>
            </article>

            <!-- 4. INSTALL STEPS -->
            <article id="install" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">04</div>
                <div>
                  <h2 class="ins-section-title">Cài đặt: {{ currentMethod.title }}</h2>
                  <p class="ins-section-sub">
                    Làm theo từng bước. Không bỏ qua - mỗi bước dựa trên bước trước.
                  </p>
                </div>
              </header>

              <div class="ins-method-switch">
                <span class="ins-method-switch-label">Đang xem:</span>
                <button
                  v-for="m in methods"
                  :key="m.key"
                  class="ins-method-switch-btn"
                  :class="{ active: activeMethod === m.key }"
                  @click="activeMethod = m.key"
                >
                  {{ m.title }}
                </button>
              </div>

              <ol class="ins-steps">
                <li
                  v-for="(step, i) in currentMethod.steps"
                  :key="i"
                  class="ins-step"
                >
                  <div class="ins-step-num">{{ String(i + 1).padStart(2, '0') }}</div>
                  <div class="ins-step-body">
                    <h3 class="ins-step-title">{{ step.title }}</h3>
                    <p class="ins-step-detail">{{ step.detail }}</p>

                    <div v-if="step.code" class="ins-code-wrap">
                      <div class="ins-code-bar">
                        <span class="ins-code-label">{{ step.codeLabel || 'code' }}</span>
                        <button
                          class="ins-code-copy"
                          :class="{ copied: copiedKey === currentMethod.key + '-step-' + i }"
                          @click="handleCopy(step.code!, currentMethod.key + '-step-' + i)"
                        >
                          <svg v-if="copiedKey !== currentMethod.key + '-step-' + i" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <rect x="9" y="9" width="13" height="13" rx="2" />
                            <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
                          </svg>
                          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="20 6 9 17 4 12" />
                          </svg>
                          <span>{{ copiedKey === currentMethod.key + '-step-' + i ? 'Đã copy' : 'Copy' }}</span>
                        </button>
                      </div>
                      <pre class="ins-code-block"><code v-html="highlightCode(step.code)"></code></pre>
                    </div>

                    <div v-if="step.tip" class="ins-tip">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10" />
                        <path d="M12 16v-4M12 8h.01" />
                      </svg>
                      <span>{{ step.tip }}</span>
                    </div>
                  </div>
                </li>
              </ol>
            </article>

            <!-- 5. VERIFY -->
            <article id="verify" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">05</div>
                <div>
                  <h2 class="ins-section-title">Xác minh cài đặt thành công</h2>
                  <p class="ins-section-sub">
                    Sau khi cài xong, làm 3 bước sau để chắc chắn mọi thứ hoạt động.
                  </p>
                </div>
              </header>

              <div class="ins-verify-card">
                <div class="ins-verify-head">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                  <span>Checklist xác minh</span>
                </div>
                <ul class="ins-verify-list">
                  <li v-for="(item, i) in currentMethod.verify" :key="i" class="ins-verify-item">
                    <span class="ins-verify-bullet">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </span>
                    <div class="ins-verify-body">
                      <div class="ins-verify-label">{{ item.label }}</div>
                      <div v-if="item.hint" class="ins-verify-hint">{{ item.hint }}</div>
                    </div>
                  </li>
                </ul>
              </div>

              <div class="ins-success-callout">
                <div class="ins-success-callout-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
                <div>
                  <div class="ins-success-callout-title">Hoàn tất! Framework đã sẵn sàng.</div>
                  <p class="ins-success-callout-text">
                    Mở Cursor và gõ <code>/</code> trong chat để xem tất cả slash commands mới.
                    Thử <code>/spec</code> hoặc <code>/plan</code> để bắt đầu task đầu tiên.
                  </p>
                </div>
              </div>
            </article>

            <!-- 6. TROUBLESHOOTING -->
            <article id="troubleshoot" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">06</div>
                <div>
                  <h2 class="ins-section-title">Xử lý lỗi thường gặp</h2>
                  <p class="ins-section-sub">
                    Các vấn đề phổ biến nhất cho cách <strong>{{ currentMethod.title }}</strong>.
                  </p>
                </div>
              </header>

              <div class="ins-trouble-list">
                <div
                  v-for="(t, i) in currentMethod.troubleshooting"
                  :key="i"
                  class="ins-trouble"
                >
                  <div class="ins-trouble-head">
                    <span class="ins-trouble-num">{{ String(i + 1).padStart(2, '0') }}</span>
                    <span class="ins-trouble-problem">{{ t.problem }}</span>
                  </div>
                  <div class="ins-trouble-solution">
                    <span class="ins-trouble-solution-label">Cách xử lý</span>
                    <p>{{ t.solution }}</p>
                  </div>
                </div>
              </div>
            </article>

            <!-- 7. FAQ -->
            <article id="faq" class="ins-section">
              <header class="ins-section-head">
                <div class="ins-section-num">07</div>
                <div>
                  <h2 class="ins-section-title">Câu hỏi thường gặp</h2>
                  <p class="ins-section-sub">
                    Nếu câu hỏi của bạn không có ở đây, mở issue trên GitHub.
                  </p>
                </div>
              </header>

              <div class="ins-faq-list">
                <div
                  v-for="(f, i) in faqs"
                  :key="i"
                  class="ins-faq"
                  :class="{ open: activeFaq === i }"
                >
                  <button class="ins-faq-head" @click="toggleFaq(i)" :aria-expanded="activeFaq === i">
                    <span class="ins-faq-q">{{ f.q }}</span>
                    <span class="ins-faq-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M6 9l6 6 6-6" />
                      </svg>
                    </span>
                  </button>
                  <div v-if="activeFaq === i" class="ins-faq-body">
                    <p>{{ f.a }}</p>
                  </div>
                </div>
              </div>
            </article>

            <!-- BOTTOM CTA -->
            <article class="ins-section">
              <div class="ins-bottom-cta">
                <div>
                  <h3 class="ins-bottom-cta-title">Cài xong rồi? Bắt đầu khám phá.</h3>
                  <p class="ins-bottom-cta-desc">
                    Xem framework library để hiểu từng rule, skill, và agent. Hoặc thử chạy prompt ngay trong prompt runner.
                  </p>
                </div>
                <div class="ins-bottom-cta-actions">
                  <router-link to="/learn" class="btn btn-primary">
                    Framework Library
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M5 12h14M13 6l6 6-6 6" />
                    </svg>
                  </router-link>
                  <router-link to="/prompts" class="btn btn-secondary">
                    Prompt Runner
                  </router-link>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.install-view {
  width: 100%;
}

/* ─── HERO ───────────────────────────────────────────────────────────── */
.ins-hero {
  position: relative;
  padding: 140px 0 64px;
  border-bottom: 1px solid var(--border-subtle);
}

.ins-hero-content {
  max-width: 820px;
}

.ins-title {
  font-size: clamp(34px, 5vw, 56px);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin: 16px 0 20px;
}

.ins-title-accent {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.78em;
  font-weight: 500;
}

.ins-subtitle {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 720px;
  margin: 0 0 36px;
}

.ins-quickstats {
  display: inline-flex;
  align-items: stretch;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-surface);
}

.ins-quickstat {
  padding: 16px 28px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-right: 1px solid var(--border-hairline);
  min-width: 130px;
}

.ins-quickstat:last-child {
  border-right: 0;
}

.ins-quickstat-value {
  font-family: var(--font-mono);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.ins-quickstat-label {
  font-size: 10.5px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-family: var(--font-mono);
}

/* ─── MAIN LAYOUT ────────────────────────────────────────────────────── */
.ins-main {
  padding: 64px 0 100px;
}

.ins-grid {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 56px;
  align-items: start;
}

/* ─── SIDEBAR ────────────────────────────────────────────────────────── */
.ins-sidebar {
  position: sticky;
  top: 80px;
}

.ins-sidebar-inner {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.ins-sidebar-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  padding-left: 14px;
  margin-bottom: 8px;
}

.ins-sidenav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-left: 1px solid var(--border-subtle);
}

.ins-sidenav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0 8px 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-tertiary);
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: color var(--t-fast);
  position: relative;
}

.ins-sidenav-item:hover {
  color: var(--text-primary);
}

.ins-sidenav-item.active {
  color: var(--accent);
  font-weight: 600;
}

.ins-sidenav-item.active .ins-sidenav-dot {
  background: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-dim);
}

.ins-sidenav-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-faint);
  flex-shrink: 0;
  margin-left: -17px;
  transition: all var(--t-fast);
}

.ins-sidebar-card {
  padding: 18px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  margin-top: 12px;
}

.ins-sidebar-card-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.ins-sidebar-card-text {
  font-size: 12.5px;
  color: var(--text-tertiary);
  line-height: 1.5;
  margin: 0 0 10px;
}

.ins-sidebar-card-link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--accent);
  transition: color var(--t-fast);
}

.ins-sidebar-card-link:hover {
  color: var(--accent-bright);
}

.ins-sidebar-card-link svg {
  width: 11px;
  height: 11px;
}

/* ─── SECTIONS ───────────────────────────────────────────────────────── */
.ins-content {
  min-width: 0;
}

.ins-section {
  margin-bottom: 72px;
  scroll-margin-top: 80px;
}

.ins-section:last-child {
  margin-bottom: 0;
}

.ins-section-head {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  padding-bottom: 28px;
  margin-bottom: 32px;
  border-bottom: 1px solid var(--border-hairline);
}

.ins-section-num {
  font-family: var(--font-mono);
  font-size: 32px;
  font-weight: 600;
  color: var(--text-faint);
  letter-spacing: -0.02em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  flex-shrink: 0;
  margin-top: 4px;
}

.ins-section-title {
  font-size: clamp(24px, 3vw, 32px);
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.ins-section-sub {
  font-size: 14.5px;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 640px;
  margin: 0;
}

.ins-section-sub code,
.ins-callout-text code,
.ins-success-callout-text code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  padding: 1px 6px;
  border-radius: var(--radius-sm);
  color: var(--accent);
}

/* ─── CALLOUT ────────────────────────────────────────────────────────── */
.ins-callout {
  display: flex;
  gap: 14px;
  padding: 18px 20px;
  background: rgba(96, 165, 250, 0.04);
  border: 1px solid rgba(96, 165, 250, 0.2);
  border-radius: var(--radius-lg);
}

.ins-callout-icon {
  width: 20px;
  height: 20px;
  color: var(--color-info);
  flex-shrink: 0;
  margin-top: 2px;
}

.ins-callout-icon svg {
  width: 100%;
  height: 100%;
}

.ins-callout-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.ins-callout-text {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.ins-callout-dev {
  margin-top: 12px;
  background: rgba(251, 191, 36, 0.04);
  border-color: rgba(251, 191, 36, 0.22);
}

.ins-callout-dev .ins-callout-icon {
  color: var(--color-warning);
}

/* ─── METHOD GRID ────────────────────────────────────────────────────── */
.ins-method-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.ins-method-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  text-align: left;
  cursor: pointer;
  transition: all var(--t-base);
  font-family: inherit;
  color: inherit;
  min-width: 0;
}

.ins-method-card:hover {
  border-color: var(--border-default);
  transform: translateY(-2px);
  background: var(--bg-raised);
}

.ins-method-card.active {
  border-color: var(--accent-line);
  background: var(--bg-raised);
  box-shadow: var(--shadow-glow);
}

.ins-method-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.ins-method-badge {
  display: inline-flex;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid;
}

.tone-success {
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.3);
}

.tone-info {
  color: var(--color-info);
  background: rgba(96, 165, 250, 0.08);
  border-color: rgba(96, 165, 250, 0.3);
}

.tone-warning {
  color: var(--color-warning);
  background: rgba(251, 191, 36, 0.08);
  border-color: rgba(251, 191, 36, 0.3);
}

.ins-method-difficulty {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 2px 7px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
  background: var(--bg-elevated);
  color: var(--text-tertiary);
}

.diff-easy {
  color: var(--color-success);
}

.diff-medium {
  color: var(--color-warning);
}

.ins-method-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.012em;
  line-height: 1.3;
}

.ins-method-oneliner {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0;
}

.ins-method-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 14px;
  border-top: 1px solid var(--border-hairline);
  margin-top: auto;
}

.ins-method-meta-row {
  display: grid;
  grid-template-columns: 80px 1fr;
  gap: 12px;
  align-items: baseline;
  font-size: 12px;
}

.ins-method-meta-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.ins-method-meta-value {
  color: var(--text-secondary);
  line-height: 1.4;
}

.ins-method-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-top: 4px;
  transition: color var(--t-fast);
}

.ins-method-card:hover .ins-method-cta,
.ins-method-card.active .ins-method-cta {
  color: var(--accent);
}

.ins-method-cta svg {
  width: 12px;
  height: 12px;
}

/* ─── PREREQUISITES ──────────────────────────────────────────────────── */
.ins-prereq-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.ins-prereq {
  display: flex;
  gap: 14px;
  padding: 18px 20px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

.ins-prereq-check {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ins-prereq-check-optional {
  background: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-tertiary);
}

.ins-prereq-check svg {
  width: 14px;
  height: 14px;
}

.ins-prereq-body {
  min-width: 0;
}

.ins-prereq-title {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  letter-spacing: -0.005em;
}

.ins-prereq-optional {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 400;
  color: var(--text-tertiary);
}

.ins-prereq-desc {
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

.ins-prereq-desc code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: var(--bg-elevated);
  padding: 1px 5px;
  border-radius: 4px;
  color: var(--accent);
}

/* ─── METHOD SWITCH + STEPS ──────────────────────────────────────────── */
.ins-method-switch {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.ins-method-switch-label {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-right: 4px;
}

.ins-method-switch-btn {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  padding: 6px 12px;
  background: transparent;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-family: inherit;
  transition: all var(--t-fast);
}

.ins-method-switch-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-subtle);
}

.ins-method-switch-btn.active {
  color: var(--accent);
  background: var(--accent-dim);
  border-color: var(--accent-line);
}

.ins-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
  list-style: none;
  padding: 0;
  margin: 0;
  counter-reset: step;
}

.ins-step {
  display: grid;
  grid-template-columns: 56px 1fr;
  gap: 20px;
  padding: 24px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  transition: border-color var(--t-base);
}

.ins-step:hover {
  border-color: var(--border-default);
}

.ins-step-num {
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: -0.02em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  padding-top: 2px;
}

.ins-step-body {
  min-width: 0;
}

.ins-step-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.012em;
  margin-bottom: 8px;
  line-height: 1.3;
}

.ins-step-detail {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0 0 14px;
}

/* Code blocks */
.ins-code-wrap {
  margin: 14px 0;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--bg-canvas);
}

.ins-code-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
}

.ins-code-label {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
}

.ins-code-copy {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  font-family: inherit;
  transition: all var(--t-fast);
}

.ins-code-copy:hover {
  color: var(--text-primary);
  background: var(--bg-elevated);
  border-color: var(--border-subtle);
}

.ins-code-copy.copied {
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.3);
}

.ins-code-copy svg {
  width: 12px;
  height: 12px;
}

.ins-code-block {
  margin: 0;
  padding: 14px 16px;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 12.5px;
  line-height: 1.65;
  color: var(--text-primary);
  white-space: pre;
}

.ins-code-block code {
  font-family: inherit;
  background: transparent;
  padding: 0;
  border: none;
  color: inherit;
}

/* Syntax tokens */
:deep(.t-cmd) {
  color: var(--accent);
  font-weight: 500;
}

:deep(.t-string) {
  color: #a5d6a7;
}

:deep(.t-comment) {
  color: var(--text-muted);
  font-style: italic;
}

:deep(.t-flag) {
  color: #fbbf24;
}

/* Tip box */
.ins-tip {
  display: flex;
  gap: 10px;
  padding: 12px 14px;
  background: rgba(16, 185, 129, 0.04);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: var(--radius-md);
  font-size: 12.5px;
  color: var(--text-secondary);
  line-height: 1.55;
}

.ins-tip svg {
  width: 14px;
  height: 14px;
  color: var(--accent);
  flex-shrink: 0;
  margin-top: 2px;
}

/* ─── VERIFY ─────────────────────────────────────────────────────────── */
.ins-verify-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 24px;
}

.ins-verify-head {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  padding-bottom: 14px;
  margin-bottom: 14px;
  border-bottom: 1px solid var(--border-hairline);
}

.ins-verify-head svg {
  width: 14px;
  height: 14px;
}

.ins-verify-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.ins-verify-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.ins-verify-bullet {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--accent-dim);
  border: 1px solid var(--accent-line);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ins-verify-bullet svg {
  width: 12px;
  height: 12px;
}

.ins-verify-body {
  min-width: 0;
  flex: 1;
}

.ins-verify-label {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.ins-verify-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  margin-top: 3px;
}

.ins-success-callout {
  display: flex;
  gap: 14px;
  margin-top: 20px;
  padding: 20px 24px;
  background: rgba(52, 211, 153, 0.05);
  border: 1px solid rgba(52, 211, 153, 0.25);
  border-radius: var(--radius-lg);
}

.ins-success-callout-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-success);
  color: var(--bg-canvas);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ins-success-callout-icon svg {
  width: 14px;
  height: 14px;
  stroke-width: 3;
}

.ins-success-callout-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.ins-success-callout-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.55;
  margin: 0;
}

/* ─── TROUBLESHOOTING ────────────────────────────────────────────────── */
.ins-trouble-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ins-trouble {
  padding: 18px 22px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  transition: border-color var(--t-fast);
}

.ins-trouble:hover {
  border-color: var(--border-default);
}

.ins-trouble-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 10px;
}

.ins-trouble-num {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-faint);
  font-variant-numeric: tabular-nums;
}

.ins-trouble-problem {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.ins-trouble-solution {
  padding-left: 32px;
  border-left: 2px solid var(--border-subtle);
  margin-left: 4px;
}

.ins-trouble-solution-label {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-success);
  margin-bottom: 4px;
}

.ins-trouble-solution p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* ─── FAQ ────────────────────────────────────────────────────────────── */
.ins-faq-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ins-faq {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: border-color var(--t-fast);
}

.ins-faq.open {
  border-color: var(--border-default);
}

.ins-faq-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  width: 100%;
  padding: 16px 20px;
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  font-family: inherit;
  transition: background var(--t-fast);
}

.ins-faq-head:hover {
  background: var(--bg-elevated);
}

.ins-faq-q {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.4;
}

.ins-faq-icon {
  width: 18px;
  height: 18px;
  color: var(--text-tertiary);
  flex-shrink: 0;
  transition: transform var(--t-fast);
}

.ins-faq.open .ins-faq-icon {
  transform: rotate(180deg);
  color: var(--accent);
}

.ins-faq-icon svg {
  width: 100%;
  height: 100%;
}

.ins-faq-body {
  padding: 0 20px 18px;
  border-top: 1px solid var(--border-hairline);
}

.ins-faq-body p {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 14px 0 0;
  max-width: 64ch;
}

/* ─── BOTTOM CTA ─────────────────────────────────────────────────────── */
.ins-bottom-cta {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 32px;
  align-items: center;
  padding: 36px 40px;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.ins-bottom-cta-title {
  font-size: 22px;
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.ins-bottom-cta-desc {
  font-size: 13.5px;
  color: var(--text-secondary);
  line-height: 1.65;
  max-width: 540px;
  margin: 0;
}

.ins-bottom-cta-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* ─── RESPONSIVE ─────────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .ins-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .ins-sidebar {
    position: static;
  }

  .ins-method-grid {
    grid-template-columns: 1fr;
  }

  .ins-prereq-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .ins-hero {
    padding: 120px 0 48px;
  }

  .ins-quickstats {
    flex-wrap: wrap;
  }

  .ins-quickstat {
    flex: 1;
    min-width: 50%;
    border-right: 0;
    border-bottom: 1px solid var(--border-hairline);
    text-align: center;
  }

  .ins-quickstat:last-child {
    border-bottom: 0;
  }

  .ins-step {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .ins-step-num {
    font-size: 16px;
  }

  .ins-bottom-cta {
    grid-template-columns: 1fr;
    padding: 28px;
  }

  .ins-section-head {
    flex-direction: column;
    gap: 12px;
  }

  .ins-section-num {
    font-size: 24px;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
</style>