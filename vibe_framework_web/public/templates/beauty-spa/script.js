/* SEN SPA — script.js */

// Smooth count-up for meta stats
function countUp(el, target, duration = 1200, suffix = '') {
  const start = 0;
  const startTime = performance.now();
  const isFloat = String(target).includes('.') || target < 100 && target % 1 !== 0;

  function step(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (target - start) * eased;

    if (isFloat) {
      el.textContent = current.toFixed(1) + suffix;
    } else {
      el.textContent = Math.floor(current) + suffix;
    }

    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// Trigger count-up when hero visible
const heroObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      document.querySelectorAll('.ms-num').forEach((el) => {
        const raw = el.textContent;
        const numeric = parseFloat(raw.replace(/[^\d.]/g, ''));
        if (!isNaN(numeric)) {
          const suffix = raw.replace(/[\d.]/g, '');
          countUp(el, numeric, 1100, suffix);
          el.dataset.animated = '1';
        }
      });
      heroObserver.disconnect();
    }
  });
}, { threshold: 0.3 });

const hero = document.querySelector('.hero');
if (hero) heroObserver.observe(hero);

// Stagger reveal for bento cards & flow steps
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, idx) => {
    if (entry.isIntersecting) {
      entry.target.style.transitionDelay = `${(idx % 6) * 60}ms`;
      entry.target.classList.add('is-revealed');
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.bento-card, .flow-step, .price-card, .t-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(12px)';
  el.style.transition = 'opacity .55s cubic-bezier(.16,1,.3,1), transform .55s cubic-bezier(.16,1,.3,1), border-color .25s';
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
if (hero) navObserver.observe(heroSentinel);
