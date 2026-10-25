// NeuralAI Template Scripts

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initStats();
  initSolutionTabs();
  initScrollAnimations();
  initSmoothScroll();
  initForm();
  initCodeAnimation();
});

// Navigation
function initNav() {
  const nav = document.querySelector('.nav');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav.style.background = 'rgba(15,23,42,0.98)';
      nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
    } else {
      nav.style.background = 'rgba(15,23,42,0.9)';
      nav.style.boxShadow = 'none';
    }
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

    if (target >= 1000000) {
      element.textContent = (current / 1000000).toFixed(1) + 'M';
    } else if (target >= 1000) {
      element.textContent = current.toLocaleString('vi-VN');
    } else {
      element.textContent = current;
    }

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Solution Tabs
function initSolutionTabs() {
  const tabs = document.querySelectorAll('.sol-tab');
  const contents = document.querySelectorAll('.solution-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const tabId = tab.dataset.tab;
      contents.forEach(content => {
        if (content.dataset.tab === tabId) {
          content.classList.add('active');
        } else {
          content.classList.remove('active');
        }
      });
    });
  });
}

// Scroll Animations
function initScrollAnimations() {
  const elements = document.querySelectorAll('.feature-card, .price-card, .doc-card, .testimonial-card');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

  elements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.5s cubic-bezier(0.23, 1, 0.32, 1)';
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

// Form Handler
function initForm() {
  const form = document.querySelector('.contact-form');
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '<i class="ph ph-spinner"></i> Đang xử lý...';
    btn.disabled = true;
    
    setTimeout(() => {
      btn.innerHTML = '<i class="ph ph-check"></i> Thành công!';
      btn.style.background = '#22c55e';
      
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = '';
        btn.disabled = false;
        form.reset();
      }, 2000);
    }, 1500);
  });
}

// Code Animation
function initCodeAnimation() {
  const codeBlock = document.querySelector('.code-content');
  if (!codeBlock) return;

  let isVisible = false;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !isVisible) {
        isVisible = true;
        animateCode();
      }
    });
  }, { threshold: 0.5 });

  observer.observe(codeBlock);
}

function animateCode() {
  const codeBlock = document.querySelector('.code-content');
  const lines = codeBlock.querySelectorAll('code');
  
  codeBlock.style.opacity = '0';
  
  setTimeout(() => {
    codeBlock.style.transition = 'opacity 0.5s ease';
    codeBlock.style.opacity = '1';
  }, 300);
}
