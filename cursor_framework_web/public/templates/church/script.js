document.addEventListener('DOMContentLoaded', function() {
  // ─── Sticky Navigation ───
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  });

  // ─── Mobile Navigation ───
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');
  const navLinks = document.querySelectorAll('.nav-link');
  let navOverlay = null;

  function ensureOverlay() {
    if (!navOverlay) {
      navOverlay = document.createElement('div');
      navOverlay.className = 'nav-overlay';
      navOverlay.id = 'nav-overlay';
      document.body.appendChild(navOverlay);
      navOverlay.addEventListener('click', closeMobileMenu);
    }
  }

  function openMobileMenu() {
    ensureOverlay();
    navMenu.classList.add('active');
    navToggle.classList.add('active');
    navOverlay.classList.add('active');
    navToggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    navMenu.classList.remove('active');
    navToggle.classList.remove('active');
    if (navOverlay) navOverlay.classList.remove('active');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  function toggleMobileMenu() {
    if (navMenu.classList.contains('active')) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  }

  if (navToggle) {
    navToggle.addEventListener('click', toggleMobileMenu);
  }

  // Close menu when clicking a link (on mobile)
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      if (window.innerWidth <= 1024) {
        closeMobileMenu();
      }
    });
  });

  // Close on resize to desktop
  window.addEventListener('resize', function() {
    if (window.innerWidth > 1024 && navMenu.classList.contains('active')) {
      closeMobileMenu();
    }
  });

  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
      closeMobileMenu();
    }
  });

  // ─── Smooth Scroll ───
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#' || !href) return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const navHeight = 72;
        const targetPos = target.getBoundingClientRect().top + window.scrollY - navHeight;
        window.scrollTo({ top: targetPos, behavior: 'smooth' });
      }
    });
  });

  // ─── Active Section Tracking ───
  const sections = document.querySelectorAll('section[id]');
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          if (link.getAttribute('href') === '#' + id) {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
          }
        });
      }
    });
  }, { threshold: 0.3, rootMargin: '-72px 0px -50% 0px' });

  sections.forEach(section => sectionObserver.observe(section));

  // ─── Scroll Reveal Animations ───
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Add reveal animation to sections
  const animatedElements = document.querySelectorAll(
    '.stat-item, .value-item, .timeline-item, .priest-card, .mass-card, ' +
    '.sacrament-card, .word-card, .word-mini, .activity-card, .news-card, ' +
    '.contact-card, .contact-form, .gallery-item'
  );
  
  animatedElements.forEach((el, index) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(40px)';
    el.style.transition = `all 0.7s cubic-bezier(0.16, 1, 0.3, 1) ${index * 0.06}s`;
    observer.observe(el);
  });

  // Add revealed styles dynamically
  const revealStyle = document.createElement('style');
  revealStyle.textContent = `
    .revealed {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  `;
  document.head.appendChild(revealStyle);

  // ─── Activity Filter Tabs ───
  const activityTabs = document.querySelectorAll('.act-tab');
  const activityCards = document.querySelectorAll('.activity-card');

  activityTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      const filter = this.dataset.filter;
      
      // Update active tab
      activityTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      
      // Filter cards
      activityCards.forEach(card => {
        const category = card.querySelector('.ac-category');
        if (filter === 'all' || category.classList.contains(filter)) {
          card.style.display = '';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 50);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(20px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 300);
        }
      });
    });
  });

  // ─── Gallery Lightbox ───
  const galleryItems = document.querySelectorAll('.gallery-item');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxClose = document.getElementById('lightbox-close');

  galleryItems.forEach(item => {
    item.addEventListener('click', function() {
      const src = this.dataset.src;
      if (src && lightboxImg) {
        lightboxImg.src = src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  if (lightboxClose) {
    lightboxClose.addEventListener('click', closeLightbox);
  }

  if (lightbox) {
    lightbox.addEventListener('click', function(e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
    setTimeout(() => {
      if (lightboxImg) lightboxImg.src = '';
    }, 300);
  }

  // Close lightbox on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && lightbox && lightbox.classList.contains('active')) {
      closeLightbox();
    }
  });

  // ─── Form Handling ───
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      const originalHTML = btn.innerHTML;
      
      // Loading state
      btn.innerHTML = '<i class="ph ph-circle-notch" style="animation:spin 1s linear infinite"></i> Đang gửi...';
      btn.disabled = true;
      
      // Simulate form submission
      setTimeout(() => {
        btn.innerHTML = '<i class="ph ph-check"></i> Đã gửi thành công!';
        btn.style.background = '#059669';
        
        setTimeout(() => {
          btn.innerHTML = originalHTML;
          btn.style.background = '';
          btn.disabled = false;
          this.reset();
        }, 2500);
      }, 1500);
    });
  }

  // ─── Hero Parallax Effect ───
  const heroContent = document.querySelector('.hero-content');
  const heroBg = document.querySelector('.hero-bg img');
  if (heroContent && heroBg) {
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY;
      if (scrolled < window.innerHeight) {
        heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
        heroContent.style.opacity = 1 - (scrolled / (window.innerHeight * 0.7));
        heroBg.style.transform = `scale(${1 + scrolled * 0.0002}) translateY(${scrolled * 0.1}px)`;
      }
    });
  }

  // ─── Image Lazy Loading ───
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');
  lazyImages.forEach(img => {
    img.addEventListener('load', function() {
      this.classList.add('loaded');
    });
  });

  // ─── Counter Animation for Stats ───
  const statNums = document.querySelectorAll('.stat-num');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.textContent.replace(/[^0-9]/g, ''));
        const suffix = el.textContent.replace(/[0-9]/g, '');
        let current = 0;
        const increment = target / 40;
        const timer = setInterval(() => {
          current += increment;
          if (current >= target) {
            el.textContent = target.toLocaleString('vi-VN') + suffix;
            clearInterval(timer);
          } else {
            el.textContent = Math.floor(current).toLocaleString('vi-VN') + suffix;
          }
        }, 30);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statNums.forEach(num => counterObserver.observe(num));

  // ─── Add spin animation for loading ───
  const spinStyle = document.createElement('style');
  spinStyle.textContent = `
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(40px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes heroZoom {
      from { transform: scale(1); }
      to { transform: scale(1.1); }
    }
    .hero-bg img {
      animation: heroZoom 20s ease-in-out infinite alternate;
    }
  `;
  document.head.appendChild(spinStyle);

  // ─── Console Branding ───
  console.log('%c🕊️ Giáo Xứ Thánh Quang', 'font-size: 24px; font-weight: bold; color: #8B2635;');
  console.log('%cNơi ánh sáng Đức Chúa chiếu vào lòng người', 'font-size: 14px; color: #D4A853;');
});
