/* TỨ TRỤ BAZI — Script */

// Reveal on scroll
const reveal = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      e.target.style.transitionDelay = `${(i % 6) * 90}ms`;
      e.target.classList.add('revealed');
      reveal.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.pillar, .el-card, .step, .pc, .t-card, .booking-info, .booking-form').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity .65s cubic-bezier(.16,1,.3,1), transform .65s cubic-bezier(.16,1,.3,1)';
  reveal.observe(el);
});

// Booking form submission (mock)
const bookingForm = document.querySelector('.booking-form');
if (bookingForm) {
  bookingForm.addEventListener('submit', e => {
    e.preventDefault();
    const btn = bookingForm.querySelector('button[type="submit"]');
    const original = btn.innerHTML;
    btn.innerHTML = '<span>✓</span> Đã gửi yêu cầu thành công <span>✓</span>';
    btn.style.background = '#2c5e2a';
    btn.style.borderColor = '#2c5e2a';
    setTimeout(() => {
      btn.innerHTML = original;
      btn.style.background = '';
      btn.style.borderColor = '';
      bookingForm.reset();
    }, 3500);
  });
}
