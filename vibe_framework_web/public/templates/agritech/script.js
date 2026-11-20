// AgriTech Pro Template Scripts

document.addEventListener('DOMContentLoaded', () => {
  initNav();
  initStats();
  initCategoryTabs();
  initScrollAnimations();
  initSmoothScroll();
  initForm();
});

// Navigation
function initNav() {
  const nav = document.querySelector('.nav');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav.style.background = 'rgba(248,250,252,0.98)';
      nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.06)';
    } else {
      nav.style.background = 'rgba(248,250,252,0.95)';
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

    element.textContent = current.toLocaleString('vi-VN');

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

// Category Tabs Filter
function initCategoryTabs() {
  const tabs = document.querySelectorAll('.cat-tab');
  const cards = document.querySelectorAll('.product-card');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const category = tab.dataset.category;

      cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
          card.style.display = 'block';
          setTimeout(() => card.style.opacity = '1', 10);
        } else {
          card.style.opacity = '0';
          setTimeout(() => card.style.display = 'none', 300);
        }
      });
    });
  });
}

// Scroll Animations
function initScrollAnimations() {
  const elements = document.querySelectorAll('.product-card, .solution-card, .support-card, .testimonial-card');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 60);
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
    
    btn.innerHTML = '<i class="ph ph-spinner"></i> Đang gửi...';
    btn.disabled = true;
    
    setTimeout(() => {
      btn.innerHTML = '<i class="ph ph-check"></i> Đã gửi thành công!';
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

// Quote button click
document.querySelectorAll('.btn-primary').forEach(btn => {
  if (btn.textContent.includes('Báo giá')) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const card = this.closest('.product-card');
      const name = card.querySelector('.pc-name').textContent;
      
      document.querySelector('#contact').scrollIntoView({ behavior: 'smooth' });
      
      setTimeout(() => {
        const textarea = document.querySelector('.contact-form textarea');
        if (textarea) {
          textarea.value = `Tôi quan tâm đến: ${name}`;
          textarea.focus();
        }
      }, 800);
    });
  }
});
