/* VIETTRAVEL — script.js */

// Smooth count-up animation for stats
function countUp(el, target, duration = 1200, prefix = '', suffix = '') {
  const start = 0;
  const startTime = performance.now();
  const isFloat = String(target).includes('.') || (target < 100 && target % 1 !== 0);

  function step(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (target - start) * eased;

    let formatted;
    if (isFloat) {
      formatted = current.toFixed(1);
    } else {
      formatted = Math.floor(current).toLocaleString('vi-VN');
    }

    el.textContent = prefix + formatted + suffix;

    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// Trigger count-up when stats visible
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      const raw = el.dataset.target;
      const prefix = el.dataset.prefix || '';
      const suffix = el.dataset.suffix || '';
      const numeric = parseInt(raw, 10);
      if (!isNaN(numeric)) {
        countUp(el, numeric, 1100, prefix, suffix);
        el.dataset.animated = '1';
      }
      statsObserver.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.si-num').forEach(el => {
  if (!el.dataset.animated) statsObserver.observe(el);
});

// Stagger reveal for cards
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, idx) => {
    if (entry.isIntersecting) {
      entry.target.style.transitionDelay = `${(idx % 6) * 60}ms`;
      entry.target.classList.add('is-revealed');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.bento-card, .flow-step, .price-card, .review-card, .guide-card, .dest-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity .55s cubic-bezier(.16,1,.3,1), transform .55s cubic-bezier(.16,1,.3,1), border-color .25s, box-shadow .25s';
  revealObserver.observe(el);
});

// Add CSS for is-revealed state
const style = document.createElement('style');
style.textContent = `.is-revealed { opacity: 1 !important; transform: translateY(0) !important; }`;
document.head.appendChild(style);

// Nav border on scroll
const nav = document.querySelector('.nav');
const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      nav.style.borderBottomColor = 'transparent';
    } else {
      nav.style.borderBottomColor = 'var(--border)';
    }
  });
}, { rootMargin: '-64px 0px 0px 0px' });

const heroSentinel = document.createElement('div');
heroSentinel.style.height = '1px';
heroSentinel.style.marginTop = '-1px';
document.querySelector('.hero')?.prepend(heroSentinel);
if (heroSentinel) navObserver.observe(heroSentinel);
