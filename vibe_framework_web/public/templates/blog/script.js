/* THE EDITORIAL — Blog magazine script */

// Live date
const dateEl = document.getElementById('date');
if (dateEl) {
  const d = new Date();
  const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  dateEl.textContent = `${days[d.getDay()]}, ${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
}

// Theme toggle
const themeBtn = document.querySelector('.theme-toggle');
if (themeBtn) {
  const saved = localStorage.getItem('editorial-theme');
  if (saved) document.documentElement.dataset.theme = saved;
  themeBtn.addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme;
    const next = cur === 'dark' ? '' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('editorial-theme', next);
    themeBtn.querySelector('i').className = next === 'dark' ? 'ph ph-sun' : 'ph ph-moon';
  });
}

// Reading progress
const progress = document.querySelector('.reading-progress');
window.addEventListener('scroll', () => {
  const doc = document.documentElement.scrollHeight - window.innerHeight;
  const w = doc > 0 ? (window.scrollY / doc) * 100 : 0;
  if (progress) progress.style.width = w + '%';
}, { passive: true });

// Reveal on scroll
const reveal = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      e.target.style.transitionDelay = `${(i % 5) * 80}ms`;
      e.target.classList.add('revealed');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.feat-lead, .side-card, .post-card, .topic, .note-body p').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(14px)';
  el.style.transition = 'opacity .55s cubic-bezier(.16,1,.3,1), transform .55s cubic-bezier(.16,1,.3,1)';
  reveal.observe(el);
});

// Newsletter form (no-op, just feedback)
const nlForm = document.querySelector('.nl-form');
if (nlForm) {
  nlForm.addEventListener('submit', e => {
    e.preventDefault();
    const input = nlForm.querySelector('input');
    if (input.value) {
      const btn = nlForm.querySelector('button');
      const original = btn.innerHTML;
      btn.innerHTML = '<i class="ph ph-check"></i> Đã đăng ký';
      btn.style.background = '#10b981';
      input.value = '';
      setTimeout(() => {
        btn.innerHTML = original;
        btn.style.background = '';
      }, 2400);
    }
  });
}
