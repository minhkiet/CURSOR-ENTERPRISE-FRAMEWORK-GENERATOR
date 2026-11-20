/* AURA — Sale template script */

// Countdown timers
function startCountdown(hoursEl, minutesEl, secondsEl, totalSeconds) {
  let remaining = totalSeconds;
  function tick() {
    const h = Math.floor(remaining / 3600);
    const m = Math.floor((remaining % 3600) / 60);
    const s = remaining % 60;
    if (hoursEl) hoursEl.textContent = String(h).padStart(2, '0');
    if (minutesEl) minutesEl.textContent = String(m).padStart(2, '0');
    if (secondsEl) secondsEl.textContent = String(s).padStart(2, '0');
    remaining = remaining > 0 ? remaining - 1 : totalSeconds;
  }
  tick();
  setInterval(tick, 1000);
}

// Header & final countdown
const initialSeconds = 23 * 3600 + 47 * 60 + 12;
const headerH = document.getElementById('h');
const headerM = document.getElementById('m');
const headerS = document.getElementById('s');
if (headerH && headerM && headerS) {
  startCountdown(headerH, headerM, headerS, initialSeconds);
}
const fh = document.getElementById('fh');
const fm = document.getElementById('fm');
const fs = document.getElementById('fs');
if (fh && fm && fs) {
  startCountdown(fh, fm, fs, initialSeconds);
}

// Variant color picker
document.querySelectorAll('.variant-opts').forEach(group => {
  group.querySelectorAll('.opt').forEach(opt => {
    opt.addEventListener('click', () => {
      group.querySelectorAll('.opt').forEach(o => o.classList.remove('active'));
      opt.classList.add('active');
      const labelEl = group.parentElement.querySelector('.variant-label span');
      const colorName = opt.dataset.color;
      const map = { '#1a1a1a':'Onyx Black', '#f5f5f4':'Cloud White', '#1e3a8a':'Ocean Blue', '#7c2d12':'Terra Cotta' };
      if (labelEl && map[colorName]) labelEl.textContent = '— ' + map[colorName];
    });
  });
});

// Thumbs (visual switch)
document.querySelectorAll('.thumbs .thumb').forEach(thumb => {
  thumb.addEventListener('click', () => {
    document.querySelectorAll('.thumbs .thumb').forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
  });
});

// Reading progress bar (track scroll)
const progress = document.createElement('div');
progress.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:#ff4500;width:0;z-index:200;transition:width .1s';
document.body.appendChild(progress);
window.addEventListener('scroll', () => {
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const width = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0;
  progress.style.width = width + '%';
}, { passive: true });

// Reveal on scroll
const reveal = new IntersectionObserver(entries => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      entry.target.style.transitionDelay = `${(i % 5) * 80}ms`;
      entry.target.classList.add('revealed');
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.feat-cell, .rev-card, .spec-row, .faq-item').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(12px)';
  el.style.transition = 'opacity .55s cubic-bezier(.16,1,.3,1), transform .55s cubic-bezier(.16,1,.3,1)';
  reveal.observe(el);
});

const revealStyle = document.createElement('style');
revealStyle.textContent = `.revealed { opacity: 1 !important; transform: translateY(0) !important; }`;
document.head.appendChild(revealStyle);
