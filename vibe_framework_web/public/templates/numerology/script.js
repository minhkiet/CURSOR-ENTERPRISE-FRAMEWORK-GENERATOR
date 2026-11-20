/* COSMOS NUMEROLOGY — Enhanced Script */

// ─── Starfield Canvas ───
const canvas = document.getElementById('starfield');
if (canvas) {
  const ctx = canvas.getContext('2d');
  let stars = [];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    initStars();
  }

  function initStars() {
    stars = [];
    const count = Math.floor((canvas.width * canvas.height) / 6000);
    for (let i = 0; i < count; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.2 + 0.2,
        a: Math.random() * Math.PI * 2,
        alpha: Math.random() * 0.5 + 0.15,
        speed: Math.random() * 0.015 + 0.003,
        twinkle: Math.random() > 0.7
      });
    }
  }

  function drawStatic() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    stars.forEach(s => {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(212, 168, 83, ${s.alpha})`;
      ctx.fill();
    });
  }

  let rafId = null;
  
  function draw(time) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    stars.forEach(s => {
      s.a += s.speed;
      const twinkleVal = s.twinkle ? (Math.sin(s.a * 2) + 1) / 2 : 1;
      const pulseAlpha = s.alpha * (0.5 + twinkleVal * 0.5);
      
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(212, 168, 83, ${pulseAlpha})`;
      ctx.fill();
    });

    rafId = requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();

  if (reducedMotion) {
    drawStatic();
  } else {
    rafId = requestAnimationFrame(draw);
  }

  window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', e => {
    if (e.matches) {
      if (rafId) cancelAnimationFrame(rafId);
      drawStatic();
    } else {
      rafId = requestAnimationFrame(draw);
    }
  });
}

// ─── Navigation Scroll Effect ───
const nav = document.getElementById('nav');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;
  
  if (currentScroll > 50) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
  
  lastScroll = currentScroll;
}, { passive: true });

// ─── Scroll Reveal Animation ───
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      const delay = (index % 6) * 80;
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, delay);
      revealObserver.unobserve(entry.target);
    }
  });
}, { 
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
});

document.querySelectorAll('.reveal').forEach(el => {
  revealObserver.observe(el);
});

// ─── Calculator Form ───
const calcForm = document.getElementById('calcForm');
const calcResult = document.getElementById('calcResult');

if (calcForm && calcResult) {
  calcForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = calcForm.querySelector('#fullname').value.trim();
    const dob = calcForm.querySelector('#dob').value;
    
    if (!name || !dob) return;
    
    // Calculate numerology numbers
    const masterNumbers = [11, 22, 33];
    
    function reduceNumber(n) {
      while (n > 9 && !masterNumbers.includes(n)) {
        n = String(n).split('').reduce((a, d) => a + parseInt(d), 0);
      }
      return n;
    }
    
    // Life Path - from birthdate
    const birthNums = dob.replace(/-/g, '').split('').map(d => parseInt(d));
    const birthSum = birthNums.reduce((a, d) => a + d, 0);
    const lifePath = reduceNumber(birthSum);
    
    // Expression - from name (simplified)
    const nameSum = name.split('').reduce((a, c) => a + c.charCodeAt(0), 0);
    const expression = reduceNumber(nameSum % 9 || 9);
    
    // Soul Urge - simplified calculation
    const soulUrge = reduceNumber((nameSum + birthSum) % 99 + 1);
    const soulUrgeDisplay = masterNumbers.includes(soulUrge) ? soulUrge : `${soulUrge}/2`;
    
    // Personality
    const personality = reduceNumber((name.length * 3 + birthSum) % 9 + 1);
    
    // Maturity
    const maturity = reduceNumber((nameSum + birthNums[0] * 2) % 9 + 1);
    
    // Birthday (day of month)
    const birthday = parseInt(dob.split('-')[2]);
    
    // Update UI
    document.getElementById('r-lifePath').textContent = lifePath;
    document.getElementById('r-expression').textContent = expression;
    document.getElementById('r-soulUrge').textContent = soulUrgeDisplay;
    document.getElementById('r-personality').textContent = personality;
    document.getElementById('r-maturity').textContent = maturity;
    document.getElementById('r-birthday').textContent = birthday;
    
    // Show result with animation
    calcResult.classList.add('show');
    calcResult.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Add entrance animation to result items
    const resultItems = calcResult.querySelectorAll('.result-item');
    resultItems.forEach((item, i) => {
      item.style.opacity = '0';
      item.style.transform = 'translateY(16px)';
      setTimeout(() => {
        item.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        item.style.opacity = '1';
        item.style.transform = 'translateY(0)';
      }, 100 + i * 80);
    });
  });
}

// ─── Smooth Scroll for Anchor Links ───
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    if (href === '#') return;
    
    e.preventDefault();
    const target = document.querySelector(href);
    
    if (target) {
      const navHeight = nav.offsetHeight;
      const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  });
});

// ─── Number Card Hover Effect ───
document.querySelectorAll('.number-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    const icon = card.querySelector('.number-card-icon');
    if (icon) {
      icon.style.transform = 'scale(1.1) rotate(5deg)';
    }
  });
  
  card.addEventListener('mouseleave', () => {
    const icon = card.querySelector('.number-card-icon');
    if (icon) {
      icon.style.transform = 'scale(1) rotate(0deg)';
    }
  });
});

// ─── Pricing Card Hover ───
document.querySelectorAll('.price-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    const badge = card.querySelector('.price-badge');
    if (badge) {
      badge.style.transform = 'translateX(-50%) scale(1.05)';
    }
  });
  
  card.addEventListener('mouseleave', () => {
    const badge = card.querySelector('.price-badge');
    if (badge) {
      badge.style.transform = 'translateX(-50%) scale(1)';
    }
  });
});

// ─── Testimonial Image Lazy Load ───
document.querySelectorAll('.testimonial-avatar').forEach(img => {
  img.loading = 'lazy';
});

// ─── Insight Image Lazy Load ───
document.querySelectorAll('.insight-image').forEach(img => {
  img.loading = 'lazy';
});

// ─── Cosmic Orbit Animation Enhancement ───
const cosmicOrbit = document.querySelector('.cosmic-orbit');
if (cosmicOrbit) {
  cosmicOrbit.addEventListener('mouseenter', () => {
    cosmicOrbit.style.transform = 'scale(1.02)';
  });
  
  cosmicOrbit.addEventListener('mouseleave', () => {
    cosmicOrbit.style.transform = 'scale(1)';
  });
}

// ─── Counter Animation for Stats ───
function animateCounter(element, target, duration = 1500) {
  const start = 0;
  const startTime = performance.now();
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (reducedMotion) {
    element.textContent = target.toLocaleString();
    return;
  }
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(start + (target - start) * easeOut);
    
    element.textContent = current.toLocaleString();
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}

// Observe stats for counter animation
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const statNumbers = entry.target.querySelectorAll('.stat-number');
      statNumbers.forEach(stat => {
        const text = stat.textContent;
        const num = parseInt(text.replace(/[^\d]/g, ''));
        if (num) {
          animateCounter(stat, num);
        }
      });
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
  statsObserver.observe(heroStats);
}

// ─── Mobile Menu Toggle ───
const mobileToggle = document.querySelector('.nav-mobile-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileToggle && navLinks) {
  mobileToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    const icon = mobileToggle.querySelector('i');
    if (navLinks.classList.contains('active')) {
      icon.className = 'ph ph-x';
    } else {
      icon.className = 'ph ph-list';
    }
  });
}

// ─── Add CSS for mobile menu ───
const style = document.createElement('style');
style.textContent = `
  @media (max-width: 1024px) {
    .nav-links {
      position: fixed;
      top: 64px;
      left: 0;
      right: 0;
      background: rgba(8, 8, 12, 0.98);
      backdrop-filter: blur(20px);
      flex-direction: column;
      padding: 24px;
      gap: 16px;
      border-bottom: 1px solid var(--rule);
      transform: translateY(-100%);
      opacity: 0;
      pointer-events: none;
      transition: all 0.3s ease;
    }
    
    .nav-links.active {
      transform: translateY(0);
      opacity: 1;
      pointer-events: auto;
    }
    
    .nav-links a {
      font-size: 16px;
      padding: 12px 0;
      border-bottom: 1px solid var(--rule);
    }
  }
`;
document.head.appendChild(style);

// ─── Page Load Animation ───
window.addEventListener('load', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.5s ease';
  
  requestAnimationFrame(() => {
    document.body.style.opacity = '1';
  });
});
