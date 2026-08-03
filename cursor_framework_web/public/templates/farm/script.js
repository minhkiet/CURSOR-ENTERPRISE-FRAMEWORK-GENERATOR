// Farm Template Scripts

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initStats();
  initFilterTabs();
  initScrollAnimations();
  initSmoothScroll();
});

// Navigation
function initNav() {
  const nav = document.querySelector('.nav');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > 100) {
      nav.style.background = 'rgba(250,250,249,0.98)';
      nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
    } else {
      nav.style.background = 'rgba(250,250,249,0.9)';
      nav.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
  });
}

// Stats Counter Animation
function initStats() {
  const stats = document.querySelectorAll('.si-num[data-target]');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  stats.forEach(stat => observer.observe(stat));
}

function animateCounter(element) {
  const target = parseInt(element.dataset.target);
  const duration = 2000;
  const start = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(easeOut * target);

    element.textContent = current.toLocaleString('vi-VN');

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Filter Tabs
function initFilterTabs() {
  const tabs = document.querySelectorAll('.filter-tab');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });
}

// Scroll Animations
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.product-card, .farm-feature, .timeline-item, .price-card, .review-card');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        entry.target.style.animationDelay = `${index * 100}ms`;
        entry.target.classList.add('animated');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  animatedElements.forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });
}

// Smooth Scroll
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

// Add to cart animation
document.querySelectorAll('.btn-outline').forEach(btn => {
  if (btn.querySelector('.ph-plus')) {
    btn.addEventListener('click', function() {
      const icon = this.querySelector('.ph') || this.querySelector('i');
      if (icon) {
        icon.classList.add('ph-check');
        icon.classList.remove('ph-plus');
        setTimeout(() => {
          icon.classList.remove('ph-check');
          icon.classList.add('ph-plus');
        }, 1500);
      }
    });
  }
});
