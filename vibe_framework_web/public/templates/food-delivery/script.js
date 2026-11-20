/* FoodNhanh — script.js */

// ─── HAMBURGER MENU ───────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

if (hamburger && navMenu) {
  hamburger.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('mobile-open');
    hamburger.innerHTML = isOpen
      ? '<i class="ph ph-x"></i>'
      : '<i class="ph ph-list"></i>';
  });

  // Close menu when a nav link is clicked
  navMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('mobile-open');
      hamburger.innerHTML = '<i class="ph ph-list"></i>';
    });
  });
}

// ─── SMOOTH SCROLL ────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const id = this.getAttribute('href');
    if (id === '#') return;
    const target = document.querySelector(id);
    if (target) {
      e.preventDefault();
      const offset = 72;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ─── FAQ ACCORDION — one open at a time ──────────────────
const faqItems = document.querySelectorAll('.faq-item');
faqItems.forEach(item => {
  item.addEventListener('toggle', () => {
    if (item.open) {
      faqItems.forEach(other => {
        if (other !== item && other.open) {
          other.open = false;
        }
      });
    }
  });
});

// ─── SCROLL REVEAL (IntersectionObserver) ─────────────────
const revealEls = document.querySelectorAll(
  '.bento-card, .flow-step, .price-card, .testi-card, .trust-item, .faq-item'
);
revealEls.forEach(el => {
  el.classList.add('reveal');
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, idx) => {
    if (entry.isIntersecting) {
      const delay = idx % 6;
      entry.target.style.transitionDelay = `${delay * 60}ms`;
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

revealEls.forEach(el => revealObserver.observe(el));

// ─── CART COUNTER ─────────────────────────────────────────
const checkoutBtn = document.getElementById('checkoutBtn');
const cartCount = document.getElementById('cartCount');

if (checkoutBtn && cartCount) {
  checkoutBtn.addEventListener('click', () => {
    const count = parseInt(cartCount.textContent, 10) || 0;
    cartCount.textContent = count + 1;
    cartCount.style.transform = 'scale(1.4)';
    cartCount.style.transition = 'transform .2s cubic-bezier(.34,1.56,.64,1)';
    setTimeout(() => {
      cartCount.style.transform = 'scale(1)';
    }, 200);
  });
}

// ─── NAV SCROLL BEHAVIOR ──────────────────────────────────
const nav = document.getElementById('nav');
if (nav) {
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const current = window.scrollY;
    if (current > 80) {
      nav.style.boxShadow = '0 2px 16px rgba(124,45,18,.08)';
    } else {
      nav.style.boxShadow = 'none';
    }
    lastScroll = current;
  }, { passive: true });
}

// ─── COUNT-UP ANIMATION FOR HERO STATS ───────────────────
function countUp(el, target, duration = 1200) {
  const start = performance.now();
  function step(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(target * eased);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

const heroStats = document.querySelectorAll('.ms-num');
heroStats.forEach(el => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const raw = el.textContent;
        const match = raw.match(/[\d,.]+/);
        if (match) {
          const num = parseFloat(match[0].replace(/,/g, ''));
          if (!isNaN(num) && num > 0) {
            el.textContent = '0';
            countUp(el, num, 1000);
          }
        }
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  observer.observe(el);
});
