// ─── Computech Template Scripts ───

// Brand filter tabs
document.querySelectorAll('.brand-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.brand-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    // In real implementation, filter product grid
  });
});

// Smooth scroll for nav links
document.querySelectorAll('.nav-menu a, .nav-cta, .cat-item').forEach(link => {
  link.addEventListener('click', e => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });
});

// Add to cart animation
document.querySelectorAll('.btn-sm').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.style.transform = 'scale(0.9)';
    setTimeout(() => {
      btn.style.transform = '';
    }, 150);
  });
});
