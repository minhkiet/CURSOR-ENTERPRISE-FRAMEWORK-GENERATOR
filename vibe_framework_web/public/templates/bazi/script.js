/* TỨ TRỤ BAZI — Enhanced Script
   Mobile nav · reveal observer · form states · count-up · nav active state
   Enhanced with parallax, magnetic hover, smooth scroll, and micro-interactions
*/

(function () {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isLargeScreen = window.matchMedia('(min-width: 1025px)');

  /* ─── MOBILE NAV ─── */
  const navToggle = document.querySelector('.nav-toggle');
  const mobileNav = document.getElementById('mobile-nav');

  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      const nextState = !expanded;
      navToggle.setAttribute('aria-expanded', String(nextState));
      navToggle.setAttribute('aria-label', nextState ? 'Đóng menu' : 'Mở menu');
      if (nextState) {
        mobileNav.hidden = false;
        mobileNav.setAttribute('data-open', 'true');
      } else {
        mobileNav.removeAttribute('data-open');
        setTimeout(() => { mobileNav.hidden = true; }, 400);
      }
    });

    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.setAttribute('aria-label', 'Mở menu');
        mobileNav.removeAttribute('data-open');
        setTimeout(() => { mobileNav.hidden = true; }, 400);
      });
    });
  }

  /* ─── NAV SCROLL STATE ─── */
  const nav = document.querySelector('.nav');
  if (nav) {
    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          nav.classList.toggle('scrolled', window.scrollY > 20);
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ─── ACTIVE NAV LINK (scroll spy) ─── */
  const sections = ['about', 'master', 'process', 'pricing', 'testimonials', 'faq', 'booking']
    .map(id => document.getElementById(id))
    .filter(Boolean);
  const navLinks = document.querySelectorAll('.nav-menu a');

  if (sections.length && navLinks.length) {
    const setActive = () => {
      const offset = window.innerHeight * 0.35;
      let current = sections[0].id;
      sections.forEach(sec => {
        const top = sec.getBoundingClientRect().top;
        if (top <= offset) current = sec.id;
      });
      navLinks.forEach(link => {
        link.classList.toggle(
          'active',
          link.getAttribute('href') === '#' + current
        );
      });
    };
    if (isLargeScreen.matches) {
      window.addEventListener('scroll', setActive, { passive: true });
      setActive();
    }
  }

  /* ─── REVEAL ON SCROLL ─── */
  const revealTargets = document.querySelectorAll(
    '.section-head, .about-left, .about-card, .pillar, .el-card, .step, ' +
    '.pc, .t-card, .faq-item, .booking-info, .booking-form, .meta-item, ' +
    '.hero-text > *, .hero-visual, .trust-cell, .master-image, .master-content, ' +
    '.credential, .master-quote, .stat-card, .case-card'
  );

  revealTargets.forEach(el => el.classList.add('reveal'));

  if (!reduceMotion && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const siblings = Array.from(entry.target.parentElement.children)
            .filter(el => el.classList.contains('reveal'));
          const idx = siblings.indexOf(entry.target);
          entry.target.style.transitionDelay = `${Math.min((idx % 6) * 70, 350)}ms`;
          entry.target.classList.add('revealed');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    revealTargets.forEach(el => revealObserver.observe(el));
  } else {
    revealTargets.forEach(el => el.classList.add('revealed'));
  }

  /* ─── COUNT-UP (trust bar & stats) ─── */
  const countTargets = document.querySelectorAll('.trust-num[data-count], .trust-num[data-decimal], .stat-number[data-count]');

  const formatNumber = (n, suffix) => {
    if (n >= 1000) {
      return n.toLocaleString('vi-VN').replace(/,/g, '.') + suffix;
    }
    return Math.round(n) + suffix;
  };

  const formatDecimal = (n, suffix) => {
    return n.toFixed(2) + suffix;
  };

  const animateCount = (el) => {
    const target = parseFloat(el.dataset.count);
    const decimal = parseFloat(el.dataset.decimal);
    const suffix = el.dataset.suffix || '';
    if (isNaN(target) && isNaN(decimal)) return;
    const isDecimal = !isNaN(decimal);
    const finalVal = isDecimal ? decimal : target;
    const duration = 1800;
    const start = performance.now();

    const step = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 4);
      const current = eased * finalVal;
      el.textContent = isDecimal
        ? formatDecimal(current, suffix)
        : formatNumber(current, suffix);
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  if (countTargets.length && 'IntersectionObserver' in window) {
    const countObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    countTargets.forEach(el => countObserver.observe(el));
  } else {
    countTargets.forEach(el => {
      const t = el.dataset.count;
      const d = el.dataset.decimal;
      const s = el.dataset.suffix || '';
      if (d) el.textContent = parseFloat(d) + s;
      else if (t) el.textContent = formatNumber(parseFloat(t), s);
    });
  }

  /* ─── BAGUA WHEEL: pause on hover ─── */
  const bagua = document.querySelector('.bagua-svg');
  if (bagua && !reduceMotion) {
    bagua.addEventListener('mouseenter', () => {
      bagua.querySelectorAll('.ring-dots, .ring-dashed').forEach(el => {
        el.style.animationPlayState = 'paused';
      });
    });
    bagua.addEventListener('mouseleave', () => {
      bagua.querySelectorAll('.ring-dots, .ring-dashed').forEach(el => {
        el.style.animationPlayState = 'running';
      });
    });
  }

  /* ─── SMOOTH SCROLL OFFSET for sticky nav ─── */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href');
      if (id === '#' || id === '#top') return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

  /* ─── MAGNETIC HOVER EFFECT for buttons ─── */
  if (!reduceMotion && 'PointerEvent' in window) {
    document.querySelectorAll('.btn, .nav-cta').forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  /* ─── INTERSECTION OBSERVER for staggered animations ─── */
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const staggerContainers = document.querySelectorAll('.pillars, .elements-grid, .stats-grid, .case-grid, .testimonials-bento');
    
    staggerContainers.forEach(container => {
      const items = container.querySelectorAll(':scope > *');
      items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = `opacity 0.6s ${index * 0.08}s ease, transform 0.6s ${index * 0.08}s ease`;
      });

      const staggerObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const items = entry.target.querySelectorAll(':scope > *');
            items.forEach((item, index) => {
              setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
              }, index * 80);
            });
            staggerObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });

      staggerObserver.observe(container);
    });
  }

  /* ─── PARALLAX EFFECT for hero ─── */
  if (!reduceMotion && isLargeScreen.matches) {
    const hero = document.querySelector('.hero');
    const heroVisual = document.querySelector('.hero-visual');
    
    if (hero && heroVisual) {
      let ticking = false;
      window.addEventListener('scroll', () => {
        if (!ticking) {
          window.requestAnimationFrame(() => {
            const scrolled = window.scrollY;
            const heroHeight = hero.offsetHeight;
            if (scrolled < heroHeight) {
              const parallax = scrolled * 0.15;
              heroVisual.style.transform = `translateY(${parallax}px)`;
            }
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });
    }
  }

  /* ─── CARD TILT EFFECT ─── */
  if (!reduceMotion && 'PointerEvent' in window) {
    document.querySelectorAll('.stat-card, .case-card, .t-card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  /* ─── BOOKING FORM ─── */
  const bookingForm = document.querySelector('.booking-form');
  if (bookingForm) {
    const inputs = bookingForm.querySelectorAll('input, select, textarea');
    
    // Add focus animations
    inputs.forEach(input => {
      input.addEventListener('focus', () => {
        input.parentElement.classList.add('focused');
      });
      input.addEventListener('blur', () => {
        input.parentElement.classList.remove('focused');
      });
    });

    // Form validation styling
    inputs.forEach(input => {
      input.addEventListener('invalid', () => {
        input.classList.add('error');
      });
      input.addEventListener('input', () => {
        if (input.validity.valid) {
          input.classList.remove('error');
        }
      });
    });

    bookingForm.addEventListener('submit', e => {
      e.preventDefault();

      if (!bookingForm.checkValidity()) {
        bookingForm.reportValidity();
        return;
      }

      const btn = bookingForm.querySelector('button[type="submit"]');
      const original = btn.innerHTML;
      btn.disabled = true;
      btn.classList.add('is-success');
      btn.innerHTML = `
        <span class="btn-ornament" aria-hidden="true">*</span>
        <span class="btn-label">Đã gửi yêu cầu thành công</span>
        <span class="btn-ornament" aria-hidden="true">*</span>
      `;

      setTimeout(() => {
        btn.innerHTML = original;
        btn.disabled = false;
        btn.classList.remove('is-success');
        bookingForm.reset();
      }, 3500);
    });
  }

  /* ─── FAQ ACCORDION ANIMATION ─── */
  document.querySelectorAll('.faq-item').forEach(item => {
    const summary = item.querySelector('summary');
    const body = item.querySelector('.faq-body');
    
    if (summary && body) {
      summary.addEventListener('click', (e) => {
        e.preventDefault();
        const isOpen = item.hasAttribute('open');
        
        // Close all other items
        document.querySelectorAll('.faq-item[open]').forEach(openItem => {
          if (openItem !== item) {
            openItem.removeAttribute('open');
          }
        });
        
        // Toggle current item
        if (isOpen) {
          item.removeAttribute('open');
        } else {
          item.setAttribute('open', '');
        }
      });
    }
  });

  /* ─── FLOATING BUTTON CLICK ─── */
  const floatingBtn = document.querySelector('.floating-btn');
  if (floatingBtn) {
    floatingBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // Pulse animation on click
      floatingBtn.style.transform = 'scale(0.95)';
      setTimeout(() => {
        floatingBtn.style.transform = '';
      }, 150);
    });
  }

  /* ─── CURSOR FOLLOWER for desktop ─── */
  if (!reduceMotion && isLargeScreen.matches && window.innerWidth > 1200) {
    const cursor = document.createElement('div');
    cursor.className = 'cursor-follower';
    cursor.style.cssText = `
      position: fixed;
      width: 20px;
      height: 20px;
      border: 2px solid var(--accent);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      transition: transform 0.15s ease, width 0.2s, height 0.2s, border-color 0.2s;
      mix-blend-mode: difference;
    `;
    document.body.appendChild(cursor);

    let cursorX = 0, cursorY = 0;
    let targetX = 0, targetY = 0;

    document.addEventListener('mousemove', (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
    });

    function animateCursor() {
      cursorX += (targetX - cursorX) * 0.15;
      cursorY += (targetY - cursorY) * 0.15;
      cursor.style.left = cursorX - 10 + 'px';
      cursor.style.top = cursorY - 10 + 'px';
      requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Grow cursor on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .btn, input, select, textarea, summary');
    interactiveElements.forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.style.width = '40px';
        cursor.style.height = '40px';
        cursor.style.borderColor = 'var(--gold)';
        cursor.style.marginLeft = '-10px';
        cursor.style.marginTop = '-10px';
      });
      el.addEventListener('mouseleave', () => {
        cursor.style.width = '20px';
        cursor.style.height = '20px';
        cursor.style.borderColor = 'var(--accent)';
        cursor.style.marginLeft = '0';
        cursor.style.marginTop = '0';
      });
    });

    // Hide cursor on mobile
    if (window.matchMedia('(pointer: coarse)').matches) {
      cursor.style.display = 'none';
    }
  }

  /* ─── PRELOAD CRITICAL IMAGES ─── */
  const criticalImages = document.querySelectorAll('img[loading="lazy"]');
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
          }
          observer.unobserve(img);
        }
      });
    });
    criticalImages.forEach(img => imageObserver.observe(img));
  }

  /* ─── PERFORMANCE: Lazy load reveal animations ─── */
  const lazySections = document.querySelectorAll('section');
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          sectionObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.05 });
    lazySections.forEach(section => sectionObserver.observe(section));
  }

  /* ─── LOG NOISE (anti-noisy devtools) ─── */
  const noop = () => {};
  window.console = window.console || { log: noop, warn: noop, error: noop };

})();
