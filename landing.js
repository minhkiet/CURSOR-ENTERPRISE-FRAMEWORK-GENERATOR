/* ═══════════════════════════════════════════════════════════════════════════
   CURSOR ENTERPRISE FRAMEWORK — LANDING PAGE JAVASCRIPT
   Interactive Explorer + Scroll Animations + UI Interactions
   ═══════════════════════════════════════════════════════════════════════════ */

'use strict';

/* ─── NAVBAR SCROLL ─────────────────────────────────────────────────────── */
(function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  let ticking = false;

  function updateNavbar() {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateNavbar);
      ticking = true;
    }
  }, { passive: true });
})();

/* ─── MOBILE MENU ─────────────────────────────────────────────────────── */
(function initMobileMenu() {
  const btn = document.getElementById('mobileMenuBtn');
  const menu = document.getElementById('mobileMenu');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(isOpen));
  });

  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    });
  });
})();

/* ─── INTERSECTION OBSERVER ─────────────────────────────────────────────── */
(function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.08,
    rootMargin: '0px 0px -40px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Principle cards
  document.querySelectorAll('.principle-card').forEach(card => {
    observer.observe(card);
  });

  // Rule items and skill items
  document.querySelectorAll('.rule-item, .skill-item').forEach(item => {
    observer.observe(item);
  });

  // Principle card delays
  document.querySelectorAll('.principle-card').forEach(card => {
    const delay = parseInt(card.getAttribute('data-delay') || '0', 10);
    card.style.transitionDelay = `${delay}ms`;
  });

  // Fade-in-up for section headers
  const fadeElements = document.querySelectorAll(
    '.section-header, .section-label, .section-title, .section-desc'
  );

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  fadeElements.forEach(el => {
    el.classList.add('fade-in-up');
    fadeObserver.observe(el);
  });
})();

/* ─── EXPLORER: SIDEBAR NAVIGATION ────────────────────────────────────── */
(function initExplorerNav() {
  const navBtns = document.querySelectorAll('.explorer-nav-btn');
  const rulesList = document.getElementById('rulesList');
  const skillsGrid = document.getElementById('skillsGrid');
  const emptyState = document.getElementById('explorerEmpty');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const category = btn.getAttribute('data-category');

      // Update active state
      navBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Reset filter tags
      document.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
      const allTag = document.querySelector('.filter-tag[data-filter="all"]');
      if (allTag) allTag.classList.add('active');

      // Reset search
      const searchInput = document.getElementById('explorerSearch');
      if (searchInput) searchInput.value = '';

      // Show correct content
      if (category === 'skills') {
        rulesList.style.display = 'none';
        skillsGrid.style.display = 'grid';
        emptyState.style.display = 'none';
        // Re-trigger visibility animation for skills
        skillsGrid.querySelectorAll('.skill-item').forEach(item => {
          item.classList.remove('visible');
          void item.offsetWidth; // force reflow
          setTimeout(() => item.classList.add('visible'), 50);
        });
      } else {
        rulesList.style.display = 'flex';
        skillsGrid.style.display = 'none';
        emptyState.style.display = 'none';
        // Re-trigger visibility animation for rules
        rulesList.querySelectorAll('.rule-item').forEach(item => {
          item.classList.remove('visible');
          void item.offsetWidth;
          setTimeout(() => item.classList.add('visible'), 50);
        });
      }
    });
  });
})();

/* ─── EXPLORER: FILTER TAGS ────────────────────────────────────────────── */
(function initExplorerFilters() {
  const filterBtns = document.querySelectorAll('.filter-tag');
  const rulesList = document.getElementById('rulesList');
  const skillsGrid = document.getElementById('skillsGrid');
  const emptyState = document.getElementById('explorerEmpty');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');

      // Update active
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter rules
      const ruleItems = rulesList.querySelectorAll('.rule-item');
      let visibleCount = 0;

      ruleItems.forEach(item => {
        const domain = item.getAttribute('data-domain') || '';
        if (filter === 'all' || domain === filter) {
          item.style.display = 'flex';
          // Trigger animation
          item.classList.remove('visible');
          void item.offsetWidth;
          setTimeout(() => item.classList.add('visible'), visibleCount * 40);
          visibleCount++;
        } else {
          item.classList.remove('visible');
          item.style.display = 'none';
        }
      });

      // Show empty state if no rules visible
      if (visibleCount === 0 && ruleItems.length > 0) {
        emptyState.style.display = 'block';
      } else {
        emptyState.style.display = 'none';
      }
    });
  });
})();

/* ─── EXPLORER: SEARCH ─────────────────────────────────────────────────── */
(function initExplorerSearch() {
  const searchInput = document.getElementById('explorerSearch');
  const rulesList = document.getElementById('rulesList');
  const skillsGrid = document.getElementById('skillsGrid');
  const emptyState = document.getElementById('explorerEmpty');

  if (!searchInput) return;

  let debounceTimer;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const query = searchInput.value.toLowerCase().trim();

      // Check which view is active
      const rulesVisible = rulesList.style.display !== 'none';

      if (rulesVisible) {
        const ruleItems = rulesList.querySelectorAll('.rule-item');
        let visibleCount = 0;

        ruleItems.forEach(item => {
          const name = item.querySelector('.rule-item-name')
            ? item.querySelector('.rule-item-name').textContent.toLowerCase()
            : '';
          const tags = Array.from(item.querySelectorAll('.rule-tag'))
            .map(t => t.textContent.toLowerCase())
            .join(' ');
          const domain = item.getAttribute('data-domain') || '';

          const matches = query === '' ||
            name.includes(query) ||
            tags.includes(query) ||
            domain.includes(query);

          if (matches) {
            item.style.display = 'flex';
            item.classList.remove('visible');
            void item.offsetWidth;
            setTimeout(() => item.classList.add('visible'), visibleCount * 30);
            visibleCount++;
          } else {
            item.classList.remove('visible');
            item.style.display = 'none';
          }
        });

        emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
      } else {
        // Search skills
        const skillItems = skillsGrid.querySelectorAll('.skill-item');
        let visibleCount = 0;

        skillItems.forEach(item => {
          const name = item.querySelector('.skill-name')
            ? item.querySelector('.skill-name').textContent.toLowerCase()
            : '';
          const platform = item.querySelector('.skill-platform')
            ? item.querySelector('.skill-platform').textContent.toLowerCase()
            : '';

          const matches = query === '' ||
            name.includes(query) ||
            platform.includes(query);

          if (matches) {
            item.style.display = 'flex';
            item.classList.remove('visible');
            void item.offsetWidth;
            setTimeout(() => item.classList.add('visible'), visibleCount * 30);
            visibleCount++;
          } else {
            item.classList.remove('visible');
            item.style.display = 'none';
          }
        });
      }
    }, 200);
  });

  // Keyboard shortcut Ctrl+K / Cmd+K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });
})();

/* ─── EXPLORER: RULE ITEM HOVER — show detail tooltip ────────────────── */
(function initRuleItems() {
  const ruleItems = document.querySelectorAll('.rule-item');
  const tooltip = document.getElementById('ruleTooltip');

  ruleItems.forEach(item => {
    item.addEventListener('click', () => {
      // Visual feedback — already handled by CSS hover
      item.style.transform = 'scale(0.98)';
      setTimeout(() => {
        item.style.transform = '';
      }, 150);
    });
  });
})();

/* ─── EXPLORER: INIT VISIBILITY ───────────────────────────────────────── */
(function initExplorerVisibility() {
  // Trigger initial visibility animation for rule items
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const items = entry.target.querySelectorAll('.rule-item, .skill-item');
        items.forEach((item, i) => {
          setTimeout(() => item.classList.add('visible'), i * 50);
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  const rulesList = document.getElementById('rulesList');
  if (rulesList) observer.observe(rulesList);

  const skillsGrid = document.getElementById('skillsGrid');
  if (skillsGrid) observer.observe(skillsGrid);
})();

/* ─── STAT COUNTER ANIMATION ──────────────────────────────────────────── */
(function initStatCounters() {
  const statNumbers = document.querySelectorAll('.stat-number');
  if (!statNumbers.length) return;

  const animateCounter = (el) => {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const duration = 1800;
    const startTime = performance.now();
    const easeOutExpo = t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

    const update = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOutExpo(progress);
      const current = Math.round(easedProgress * target);
      el.textContent = current.toLocaleString('en-US');

      if (progress < 1) {
        requestAnimationFrame(update);
      }
    };

    requestAnimationFrame(update);
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const numberEls = entry.target.querySelectorAll('.stat-number');
        numberEls.forEach(el => animateCounter(el));
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  const statsBar = document.querySelector('.stats-bar');
  if (statsBar) observer.observe(statsBar);
})();

/* ─── COPY TO CLIPBOARD ───────────────────────────────────────────────── */
(function initCopyButtons() {
  document.querySelectorAll('.step-copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.getAttribute('data-code') || '';
      navigator.clipboard.writeText(code).then(() => {
        const originalHTML = btn.innerHTML;
        btn.innerHTML = `
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
          Copied!
        `;
        btn.style.color = 'var(--color-success)';
        setTimeout(() => {
          btn.innerHTML = originalHTML;
          btn.style.color = '';
        }, 2000);
      }).catch(() => {
        const textarea = document.createElement('textarea');
        textarea.value = code;
        textarea.style.cssText = 'position:fixed;opacity:0;';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      });
    });
  });
})();

/* ─── TOKEN CHART ANIMATION ─────────────────────────────────────────────── */
(function initTokenChart() {
  const chart = document.querySelector('.token-chart');
  if (!chart) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fills = chart.querySelectorAll('.tc-bar-fill');
        fills.forEach(bar => {
          const target = bar.closest('.tc-bar').style.getPropertyValue('--h');
          bar.style.width = '0%';
          setTimeout(() => {
            bar.style.width = target;
          }, 200);
        });
        observer.unobserve(chart);
      }
    });
  }, { threshold: 0.3 });

  observer.observe(chart);
})();

/* ─── TERMINAL BLINKING CURSOR ─────────────────────────────────────────── */
(function initTerminalCursor() {
  const cursor = document.getElementById('terminalCursor');
  if (!cursor) return;

  let visible = true;
  const blink = () => {
    if (cursor) {
      cursor.style.opacity = visible ? '1' : '0';
      visible = !visible;
    }
  };
  setInterval(blink, 530);
})();

/* ─── SMOOTH SCROLL ────────────────────────────────────────────────────── */
(function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      const targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#') return;

      const targetEl = document.querySelector(targetId);
      if (!targetEl) return;

      e.preventDefault();
      const navbarHeight = 60;
      const targetPosition = targetEl.getBoundingClientRect().top + window.scrollY - navbarHeight;

      window.scrollTo({ top: targetPosition, behavior: 'smooth' });
    });
  });
})();

/* ─── KEYBOARD NAVIGATION ───────────────────────────────────────────────── */
(function initKeyboardNav() {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.mobile-menu.open').forEach(menu => {
        menu.classList.remove('open');
      });
    }
  });
})();

/* ─── REDUCE MOTION ────────────────────────────────────────────────────── */
(function initReduceMotion() {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (prefersReducedMotion.matches) {
    document.documentElement.style.setProperty('--t-fast', '0ms');
    document.documentElement.style.setProperty('--t-base', '0ms');
    document.documentElement.style.setProperty('--t-slow', '0ms');
  }
})();

/* ─── PROGRESS BARS ANIMATION ──────────────────────────────────────────── */
(function initProgressBars() {
  const fills = document.querySelectorAll('.cef-progress-fill');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fill = entry.target;
        const targetWidth = fill.style.width;
        fill.style.width = '0%';
        setTimeout(() => { fill.style.width = targetWidth; }, 200);
        observer.unobserve(fill);
      }
    });
  }, { threshold: 0.3 });

  fills.forEach(fill => observer.observe(fill));
})();

console.log('[CEF Landing] Script initialized — Cursor Enterprise Framework v4.0.0');
