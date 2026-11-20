/* MIRA PHAM — Portfolio script */

// Sticky nav scroll state
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {
  if (window.scrollY > 16) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
}, { passive: true });

// Live local time (Hà Nội)
function updateTime() {
  const el = document.getElementById('time');
  if (!el) return;
  const time = new Date().toLocaleTimeString('en-GB', {
    timeZone: 'Asia/Ho_Chi_Minh',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  el.textContent = `Hà Nội · ${time}`;
}
updateTime();
setInterval(updateTime, 1000);

// Reveal on scroll
const reveal = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      e.target.style.transitionDelay = `${(i % 6) * 70}ms`;
      e.target.classList.add('revealed');
      reveal.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.w-card, .p-step, .press-card, .cm, .about-portrait, .stat, .work-grid, .process-list').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity .65s cubic-bezier(.16,1,.3,1), transform .65s cubic-bezier(.16,1,.3,1)';
  reveal.observe(el);
});

// Skill hover effect
document.querySelectorAll('.sk li').forEach(li => {
  li.style.cursor = 'default';
  li.addEventListener('mouseenter', () => {
    li.style.paddingLeft = '12px';
    li.style.transition = 'padding-left .15s';
  });
  li.addEventListener('mouseleave', () => {
    li.style.paddingLeft = '0';
  });
});
