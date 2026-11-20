// ─── AUTOPRIME MOTORS JAVASCRIPT LOGIC ───
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
      navLinks.style.top = '68px';
      navLinks.style.left = '0';
      navLinks.style.right = '0';
      navLinks.style.background = '#070a12';
      navLinks.style.padding = '20px';
      navLinks.style.borderBottom = '1px solid var(--border-subtle)';
    });
  }

  // 2. Inventory Filtering by Tabs
  const tabBtns = document.querySelectorAll('.inventory-tabs .tab-btn');
  const carCards = document.querySelectorAll('.cars-grid .car-card');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');
      carCards.forEach(card => {
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

  // 3. Calculator State & Logic
  const calcCarSelect = document.getElementById('calcCarSelect');
  const calcCitySelect = document.getElementById('calcCitySelect');
  const loanPercentSlider = document.getElementById('loanPercentSlider');
  const loanTermSlider = document.getElementById('loanTermSlider');
  const loanRateSlider = document.getElementById('loanRateSlider');

  const loanPercentVal = document.getElementById('loanPercentVal');
  const loanTermVal = document.getElementById('loanTermVal');
  const loanRateVal = document.getElementById('loanRateVal');

  const resCarPrice = document.getElementById('resCarPrice');
  const resRegFee = document.getElementById('resRegFee');
  const resPlateFee = document.getElementById('resPlateFee');
  const resRoadFee = document.getElementById('resRoadFee');
  const resTotalPrice = document.getElementById('resTotalPrice');
  const resMonthlyPay = document.getElementById('resMonthlyPay');
  const resPrepayAmount = document.getElementById('resPrepayAmount');

  function formatVnd(num) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(num).replace('₫', '₫');
  }

  function updateCalculator() {
    if (!calcCarSelect) return;

    const carPrice = parseFloat(calcCarSelect.value) || 0;
    const city = calcCitySelect ? calcCitySelect.value : 'hanoi';
    const loanPercent = parseFloat(loanPercentSlider ? loanPercentSlider.value : 80);
    const loanTermMonths = parseInt(loanTermSlider ? loanTermSlider.value : 60);
    const loanRateAnnual = parseFloat(loanRateSlider ? loanRateSlider.value : 6.8);

    if (loanPercentVal) loanPercentVal.textContent = `${loanPercent}%`;
    if (loanTermVal) loanTermVal.textContent = `${loanTermMonths} Tháng (${(loanTermMonths / 12).toFixed(0)} Năm)`;
    if (loanRateVal) loanRateVal.textContent = `${loanRateAnnual.toFixed(1)}% / năm`;

    // Registration Tax: Hanoi 12%, others 10%
    const regFeeRate = (city === 'hanoi') ? 0.12 : 0.10;
    const regFee = Math.round(carPrice * regFeeRate);

    // Plate fee: Hanoi/HCM 20,000,000, others 1,000,000
    const plateFee = (city === 'hanoi' || city === 'hcm') ? 20000000 : 1000000;
    const inspectionFee = 340000;
    const roadMaintenanceFee = 1560000; // 1 year individual
    const civilInsurance = 480000; // 5-seat standard
    const otherFees = inspectionFee + roadMaintenanceFee + civilInsurance;

    const totalPrice = carPrice + regFee + plateFee + otherFees;

    // Loan calculations
    const loanAmount = carPrice * (loanPercent / 100);
    const monthlyRate = (loanRateAnnual / 100) / 12;
    // Monthly annuity payment: P * (r * (1 + r)^n) / ((1 + r)^n - 1)
    let monthlyPayment = 0;
    if (monthlyRate > 0 && loanTermMonths > 0) {
      monthlyPayment = loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, loanTermMonths)) / (Math.pow(1 + monthlyRate, loanTermMonths) - 1);
    } else {
      monthlyPayment = loanAmount / loanTermMonths;
    }

    const prepayAmount = (carPrice - loanAmount) + regFee + plateFee + otherFees;

    if (resCarPrice) resCarPrice.textContent = formatVnd(carPrice);
    if (resRegFee) resRegFee.textContent = formatVnd(regFee);
    if (resPlateFee) resPlateFee.textContent = formatVnd(plateFee + inspectionFee);
    if (resRoadFee) resRoadFee.textContent = formatVnd(roadMaintenanceFee + civilInsurance);
    if (resTotalPrice) resTotalPrice.textContent = formatVnd(totalPrice);
    if (resMonthlyPay) resMonthlyPay.textContent = `${formatVnd(Math.round(monthlyPayment))} / tháng`;
    if (resPrepayAmount) resPrepayAmount.textContent = formatVnd(Math.round(prepayAmount));
  }

  // Bind change events
  [calcCarSelect, calcCitySelect, loanPercentSlider, loanTermSlider, loanRateSlider].forEach(el => {
    if (el) el.addEventListener('input', updateCalculator);
  });
  updateCalculator();

  // Quick Action Buttons on Car Cards
  document.querySelectorAll('.btn-calc-loan').forEach(btn => {
    btn.addEventListener('click', () => {
      const price = btn.getAttribute('data-car-price');
      if (calcCarSelect && price) {
        calcCarSelect.value = price;
        updateCalculator();
        const calcSection = document.getElementById('calculator');
        if (calcSection) calcSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  document.querySelectorAll('.btn-open-drive').forEach(btn => {
    btn.addEventListener('click', () => {
      const carName = btn.getAttribute('data-car');
      const tdCar = document.getElementById('tdCar');
      if (tdCar && carName) {
        tdCar.value = carName;
      }
      const tdSection = document.getElementById('test-drive');
      if (tdSection) tdSection.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // 4. Hero Quick Filter Handler
  window.filterHeroSearch = function() {
    const brand = document.getElementById('heroBrandSelect')?.value || 'all';
    const body = document.getElementById('heroBodySelect')?.value || 'all';
    const price = document.getElementById('heroPriceSelect')?.value || 'all';

    let matchCount = 0;
    carCards.forEach(card => {
      const cBrand = card.getAttribute('data-brand') || '';
      const cBody = card.getAttribute('data-body') || '';
      const cPrice = card.getAttribute('data-price') || '';

      const matchBrand = (brand === 'all' || cBrand === brand);
      const matchBody = (body === 'all' || cBody === body);
      const matchPrice = (price === 'all' || cPrice === price);

      if (matchBrand && matchBody && matchPrice) {
        card.style.display = 'flex';
        matchCount++;
      } else {
        card.style.display = 'none';
      }
    });

    const invSection = document.getElementById('inventory');
    if (invSection) invSection.scrollIntoView({ behavior: 'smooth' });
    showToast(`Đã tìm thấy ${matchCount} xe phù hợp với tiêu chí của bạn!`);
  };

  // 5. Test Drive Submit Handler
  window.submitTestDrive = function() {
    const name = document.getElementById('tdName')?.value;
    const phone = document.getElementById('tdPhone')?.value;
    const car = document.getElementById('tdCar')?.value;
    const date = document.getElementById('tdDate')?.value;

    showToast(`Cảm ơn ${name}! AutoPrime đã ghi nhận lịch lái thử xe ${car} vào ngày ${date}. Hotline 1800 6969 sẽ liên hệ bạn ngay.`);
    document.getElementById('testDriveForm')?.reset();
  };

  // 6. Request Quote from Calculator
  const btnRequestQuote = document.getElementById('btnRequestQuote');
  if (btnRequestQuote) {
    btnRequestQuote.addEventListener('click', () => {
      const carName = calcCarSelect?.options[calcCarSelect.selectedIndex]?.getAttribute('data-name') || 'Xe bạn chọn';
      const total = resTotalPrice?.textContent || '';
      showToast(`Đã gửi bảng dự toán ${carName} (${total}) tới hệ thống. Chuyên viên tài chính sẽ liên hệ bạn trong 10 phút!`);
    });
  }

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
