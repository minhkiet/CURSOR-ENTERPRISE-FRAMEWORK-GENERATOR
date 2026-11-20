// ─── GYMZONE — Fitness Template Interactions ───

// Animate stat numbers on scroll
function animateStats() {
  const els = document.querySelectorAll('.stat-num');
  els.forEach(el => {
    const target = parseInt(el.dataset.target || '0');
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    if (target === 0) { el.textContent = prefix || '0%'; return; }
    let current = 0;
    const step = Math.ceil(target / 40);
    const t = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(t); }
      el.textContent = prefix + current.toLocaleString('vi-VN') + suffix;
    }, 30);
  });
}

// Smooth scroll for anchors
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const href = a.getAttribute('href');
    if (href.length > 1) {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });
});

// Init
document.addEventListener('DOMContentLoaded', animateStats);
