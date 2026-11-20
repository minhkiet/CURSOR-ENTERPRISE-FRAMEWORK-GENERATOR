// ─── VỊ XƯA QUÁN JAVASCRIPT LOGIC ───
document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const menuToggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      const isOpen = navLinks.style.display === 'flex';
      navLinks.style.display = isOpen ? 'none' : 'flex';
      navLinks.style.flexDirection = 'column';
      navLinks.style.position = 'absolute';
      navLinks.style.top = '72px';
      navLinks.style.left = '0';
      navLinks.style.right = '0';
      navLinks.style.background = '#120b07';
      navLinks.style.padding = '20px';
      navLinks.style.borderBottom = '1px solid var(--border-subtle)';
    });
  }

  // 2. Menu Filtering by Category Tabs
  const menuTabs = document.querySelectorAll('.menu-tabs .m-tab-btn');
  const dishCards = document.querySelectorAll('.menu-grid .dish-card');

  menuTabs.forEach(btn => {
    btn.addEventListener('click', () => {
      menuTabs.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');
      dishCards.forEach(card => {
        if (filter === 'all') {
          card.style.display = 'flex';
        } else {
          const categories = card.getAttribute('data-category') || '';
          if (categories.includes(filter)) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        }
      });
    });
  });

  // 3. Copy Voucher Code Action
  document.querySelectorAll('.btn-copy-code').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.getAttribute('data-code');
      if (code) {
        navigator.clipboard.writeText(code).then(() => {
          showToast(`Đã sao chép mã ưu đãi "${code}" vào bộ nhớ tạm!`);
        }).catch(() => {
          showToast(`Mã ưu đãi của bạn: ${code}`);
        });
      }
    });
  });

  // 4. Quick Dish Order Action
  document.querySelectorAll('.btn-dish-order').forEach(btn => {
    btn.addEventListener('click', () => {
      const dish = btn.getAttribute('data-dish');
      const bNote = document.getElementById('bNote');
      if (bNote) {
        bNote.value = `Muốn gọi trước món: ${dish}`;
      }
      const bookingSection = document.getElementById('booking');
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth' });
      }
      showToast(`Đã thêm món "${dish}" vào ghi chú đặt bàn của bạn!`);
    });
  });

  // 5. Voucher Claim Form Submission
  window.claimVoucher = function() {
    const name = document.getElementById('vName')?.value;
    const phone = document.getElementById('vPhone')?.value;
    const branch = document.getElementById('vBranch')?.options[document.getElementById('vBranch').selectedIndex]?.text;

    showToast(`Chúc mừng ${name}! Mã E-Voucher GIAM15 đã được gửi tới số điện thoại ${phone} (Chi nhánh: ${branch}).`);
    document.getElementById('voucherClaimForm')?.reset();
  };

  // 6. Reservation Form Submission
  window.submitReservation = function() {
    const name = document.getElementById('bName')?.value;
    const phone = document.getElementById('bPhone')?.value;
    const guests = document.getElementById('bGuests')?.value;
    const date = document.getElementById('bDate')?.value;
    const time = document.getElementById('bTime')?.value;
    const branch = document.getElementById('bBranch')?.options[document.getElementById('bBranch').selectedIndex]?.text;

    showToast(`Cảm ơn quý khách ${name}! Vị Xưa Quán đã nhận yêu cầu đặt bàn ${guests} người vào lúc ${time} ngày ${date} tại ${branch}. Lễ tân sẽ gọi ${phone} xác nhận ngay!`);
    document.getElementById('reservationForm')?.reset();
  };

  // 7. Toast Notification Utility
  window.showToast = function(msg) {
    const toast = document.getElementById('toastNotif');
    const msgEl = document.getElementById('toastMsg');
    if (!toast || !msgEl) return;

    msgEl.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 4500);
  };
});
