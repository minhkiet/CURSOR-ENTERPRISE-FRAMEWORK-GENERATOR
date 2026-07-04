/* COSMOS NUMEROLOGY — script */

// Starfield canvas
const canvas = document.getElementById('starfield');
if (canvas) {
  const ctx = canvas.getContext('2d');
  let stars = [];

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    initStars();
  }

  function initStars() {
    stars = [];
    const count = Math.floor((canvas.width * canvas.height) / 8000);
    for (let i = 0; i < count; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.4 + 0.3,
        vx: (Math.random() - 0.5) * 0.05,
        vy: (Math.random() - 0.5) * 0.05,
        a: Math.random() * Math.PI * 2,
        alpha: Math.random() * 0.6 + 0.2,
        speed: Math.random() * 0.02 + 0.005
      });
    }
  }

  function draw(time) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    stars.forEach(s => {
      s.a += s.speed;
      const twinkle = (Math.sin(s.a) + 1) / 2;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(212,175,55,${s.alpha * (0.4 + twinkle * 0.6)})`;
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw(0);
}

// Reveal on scroll
const reveal = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      e.target.style.transitionDelay = `${(i % 6) * 80}ms`;
      e.target.classList.add('revealed');
      reveal.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.num-card, .story, .pc, .how-step, .calc-form').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity .6s cubic-bezier(.16,1,.3,1), transform .6s cubic-bezier(.16,1,.3,1)';
  reveal.observe(el);
});

// Calculator form (mock calculation - deterministic based on inputs)
const calcForm = document.querySelector('.calc-form');
const resultEl = document.getElementById('result');
if (calcForm && resultEl) {
  calcForm.addEventListener('submit', e => {
    e.preventDefault();
    const name = calcForm.querySelector('#fullname').value.trim();
    const dob = calcForm.querySelector('#dob').value;
    if (!name || !dob) return;

    // Deterministic pseudo-random based on inputs
    const seed = (name + dob).split('').reduce((a, c) => a + c.charCodeAt(0), 0);
    const rand = (n) => Math.abs(Math.sin(seed + n)) % 1;
    const masterNumbers = [11, 22, 33];

    function reduce(n) {
      while (n > 9 && !masterNumbers.includes(n)) {
        n = String(n).split('').reduce((a, d) => a + parseInt(d), 0);
      }
      return n;
    }

    const lifePath = reduce(dob.replace(/-/g, '').split('').reduce((a, d) => a + parseInt(d), 0));
    const r = resultEl.querySelectorAll('.r-num');
    r[0].textContent = lifePath;
    r[1].textContent = reduce(Math.floor(rand(1) * 9) + 1);
    r[2].textContent = reduce(Math.floor(rand(2) * 9) + 1) + '/' + reduce(Math.floor(rand(2) * 9) + 1);
    r[3].textContent = reduce(Math.floor(rand(3) * 9) + 1);
    r[4].textContent = reduce(Math.floor(rand(4) * 9) + 1);
    r[5].textContent = parseInt(dob.split('-')[2]);

    resultEl.hidden = false;
    resultEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}
