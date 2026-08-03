// Little Stars Preschool Template Scripts

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initStats();
  initScrollAnimations();
  initSmoothScroll();
  initForm();
});

// Navigation
function initNav() {
  const nav = document.querySelector('.nav');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav.style.background = 'rgba(255,251,235,0.98)';
      nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.06)';
    } else {
      nav.style.background = 'rgba(255,251,235,0.95)';
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

    element.textContent = current;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Scroll Animations
function initScrollAnimations() {
  const elements = document.querySelectorAll('.program-card, .teacher-card, .testimonial-card, .av-item');
  
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
      const href = this.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

// Form Handler
function initForm() {
  const form = document.querySelector('.contact-form');
  if (!form) return;
  
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '<i class="ph ph-spinner"></i> Đang gửi...';
    btn.disabled = true;
    
    setTimeout(() => {
      btn.innerHTML = '<i class="ph ph-check"></i> Đã đăng ký thành công!';
      btn.style.background = '#10b981';
      
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.background = '';
        btn.disabled = false;
        form.reset();
      }, 3000);
    }, 1500);
  });
}

// Image hover effect for facility gallery
document.querySelectorAll('.fg-item').forEach(item => {
  item.addEventListener('mouseenter', () => {
    item.style.zIndex = '10';
  });
  item.addEventListener('mouseleave', () => {
    item.style.zIndex = '1';
  });
});
