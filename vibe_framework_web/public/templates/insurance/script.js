/**
 * Aegis Bảo An — Enterprise Insurance Interactive Engine
 * Handles Quote Calculator, Hospital Finder, Product Tabs, Modals & Leads
 */

document.addEventListener('DOMContentLoaded', () => {
  initQuickCalculator();
  initProductTabs();
  initProductModal();
  initHospitalFinder();
  initFaqAccordion();
  initLeadForm();
  initMobileMenu();
});

/* ─── 1. QUICK QUOTE CALCULATOR ─── */
function initQuickCalculator() {
  const insType = document.getElementById('insType');
  const insAge = document.getElementById('insAge');
  const insGender = document.getElementById('insGender');
  const coverageLimit = document.getElementById('coverageLimit');
  const coverageValueLabel = document.getElementById('coverageValueLabel');
  const estimatedPrice = document.getElementById('estimatedPrice');
  const btnConsultNow = document.getElementById('btnConsultNow');

  if (!insType || !coverageLimit || !estimatedPrice) return;

  function formatVND(val) {
    return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function calculateEstimate() {
    const type = insType.value;
    const age = insAge.value;
    const gender = insGender.value;
    const coverage = parseInt(coverageLimit.value, 10); // in millions, e.g. 1000 = 1 Tỷ

    // Base rate per million of coverage per month
    let baseRate = 0.35; // default 350.000 for 1000 mil

    if (type === 'health') {
      baseRate = 0.38;
      if (age === 'child') baseRate *= 0.85;
      else if (age === 'young') baseRate *= 1.0;
      else if (age === 'mid') baseRate *= 1.35;
      else if (age === 'senior') baseRate *= 2.1;
      if (gender === 'female') baseRate *= 1.05; // thai san benefits inclusion
    } else if (type === 'life') {
      baseRate = 0.95;
      if (age === 'child') baseRate *= 0.6;
      else if (age === 'young') baseRate *= 0.9;
      else if (age === 'mid') baseRate *= 1.5;
      else if (age === 'senior') baseRate *= 2.6;
    } else if (type === 'auto') {
      baseRate = 0.45;
    } else if (type === 'travel') {
      baseRate = 0.12;
    } else if (type === 'business') {
      baseRate = 1.2;
    }

    const calculatedMonthPrice = Math.round((coverage * baseRate * 1000) / 1000) * 1000;
    estimatedPrice.textContent = formatVND(calculatedMonthPrice);

    // Format label for coverage
    if (coverage >= 1000) {
      const billions = (coverage / 1000).toFixed(1).replace('.0', '');
      coverageValueLabel.textContent = `${billions} Tỷ VNĐ`;
    } else {
      coverageValueLabel.textContent = `${coverage} Triệu VNĐ`;
    }
  }

  coverageLimit.addEventListener('input', calculateEstimate);
  insType.addEventListener('change', calculateEstimate);
  insAge.addEventListener('change', calculateEstimate);
  insGender.addEventListener('change', calculateEstimate);

  if (btnConsultNow) {
    btnConsultNow.addEventListener('click', () => {
      const targetSelect = document.getElementById('targetProduct');
      if (targetSelect) {
        targetSelect.value = insType.value;
      }
      const consultSection = document.getElementById('consult');
      if (consultSection) {
        consultSection.scrollIntoView({ behavior: 'smooth' });
        const nameInput = document.getElementById('fullName');
        if (nameInput) nameInput.focus();
      }
    });
  }

  calculateEstimate();
}

/* ─── 2. PRODUCT TABS FILTER ─── */
function initProductTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const prodCards = document.querySelectorAll('.prod-card');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      prodCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.style.display = 'flex';
          card.style.animation = 'fadeIn 0.3s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // Handle dropdown clicks from navigation
  const dropdownLinks = document.querySelectorAll('.dropdown-item');
  dropdownLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const cat = link.getAttribute('data-cat');
      if (cat) {
        const matchingBtn = document.querySelector(`.tab-btn[data-filter="${cat}"]`);
        if (matchingBtn) {
          matchingBtn.click();
        }
      }
    });
  });
}

/* ─── 3. PRODUCT DETAIL MODAL ─── */
const productDetailsData = {
  health: {
    category: 'Bảo hiểm Sức Khỏe Cao Cấp',
    title: 'Aegis CarePlus Toàn Diện — Biểu Phí & Quyền Lợi',
    html: `
      <p>Gói bảo hiểm sức khỏe cao cấp bảo lãnh viện phí không giới hạn tại hơn 680+ bệnh viện công lập và tư nhân quốc tế tại Việt Nam và Đông Nam Á.</p>
      <h4>Quyền Lợi Nội Trú (Tối đa 2.000.000.000 VNĐ / năm)</h4>
      <ul>
        <li>Tiền phòng và giường: Chi trả thực tế đến 4.500.000 đ/ngày (Phòng đơn tiêu chuẩn quốc tế).</li>
        <li>Phòng chăm sóc đặc biệt (ICU): Chi trả 100% không giới hạn số ngày.</li>
        <li>Phẫu thuật nội trú & cấy ghép tạng: Chi trả tối đa 100% hạn mức năm.</li>
        <li>Điều trị ung thư (Hóa trị, xạ trị, liệu pháp miễn dịch): Chi trả theo chi phí thực tế.</li>
      </ul>
      <h4>Quyền Lợi Ngoại Trú & Bổ Sung</h4>
      <ul>
        <li>Khám bệnh, xét nghiệm chẩn đoán, thuốc kê đơn: Tối đa 30.000.000 đ/năm (3.000.000 đ/lần khám).</li>
        <li>Chăm sóc thai sản & sinh con: 40.000.000 đ/năm (Thời gian chờ 270 ngày).</li>
        <li>Nha khoa điều trị (Trám, nhổ răng bệnh lý, cạo vôi): 10.000.000 đ/năm.</li>
      </ul>
      <h4>Thời Gian Chờ Áp Dụng</h4>
      <p>Tai nạn: 24h · Bệnh thông thường: 30 ngày · Bệnh đặc biệt & bệnh có sẵn: 365 ngày.</p>
    `
  },
  life: {
    category: 'Bảo hiểm Nhân Thọ & Hưu Trí',
    title: 'An Thịnh Toàn Gia & Hưu Trí — Chi Tiết Quyền Lợi',
    html: `
      <p>Giải pháp bảo vệ tài chính dài hạn tích hợp quỹ đầu tư an toàn có bảo tức định kỳ dành cho người trụ cột gia đình.</p>
      <h4>Quyền Lợi Bảo Vệ Thu Nhập</h4>
      <ul>
        <li>Quyền lợi tử vong hoặc thương tật toàn bộ vĩnh viễn: Chi trả 100% - 300% Số tiền bảo hiểm (lên đến 3 Tỷ đồng).</li>
        <li>Bảo vệ trước 88 bệnh lý nghiêm trọng (Ung thư, đột quỵ, nhồi máu cơ tim...): Chi trả nhiều lần đến 200% STBH.</li>
        <li>Quyền lợi miễn đóng phí nếu người được bảo hiểm mắc bệnh hiểm nghèo giai đoạn cuối.</li>
      </ul>
      <h4>Quyền Lợi Tích Lũy & Đầu Tư</h4>
      <ul>
        <li>Lãi suất cam kết tối thiểu 4.5%/năm trong 5 năm đầu tiên.</li>
        <li>Thưởng duy trì hợp đồng định kỳ mỗi 3 năm.</li>
        <li>Linh hoạt rút một phần giá trị tài khoản từ sau năm hợp đồng thứ 3.</li>
      </ul>
    `
  },
  auto: {
    category: 'Bảo hiểm Xe Cơ Giới',
    title: 'AutoCare Vật Chất Ô Tô — Quy Trình & Phạm Vi Bảo Vệ',
    html: `
      <p>Bảo hiểm vật chất xe toàn diện cho xe con từ 4 đến 9 chỗ, xe gia đình và xe dịch vụ công nghệ.</p>
      <h4>Phạm Vi Bồi Thường Toàn Diện</h4>
      <ul>
        <li>Thiệt hại vật chất do đâm va, lật đổ, chìm, rơi, hỏa hoạn, cháy nổ, thiên tai bão lụt.</li>
        <li><strong>Bảo hiểm thủy kích:</strong> Chi trả sửa chữa động cơ xe bị hư hỏng do ngập nước đô thị (Mức khấu trừ chỉ 10%).</li>
        <li>Bảo hiểm mất cắp bộ phận (Gương chiếu hậu, logo, cần gạt nước...): Tối đa 2 vụ/năm.</li>
        <li>Sửa chữa tại Garage chính hãng với phụ tùng mới 100% không tính khấu hao phụ tùng thay mới.</li>
      </ul>
      <h4>Dịch Vụ Cứu Hộ 24/7</h4>
      <p>Tổng đài điều phối cứu hộ 1900 6868 miễn phí trong bán kính 100km trên toàn lãnh thổ Việt Nam.</p>
    `
  },
  travel: {
    category: 'Bảo hiểm Du Lịch Quốc Tế',
    title: 'GlobeSecure Toàn Cầu — Đáp Ứng Visa Schengen & Quốc Tế',
    html: `
      <p>Chứng nhận bảo hiểm hợp lệ 100% được tất cả các Đại Sứ Quán Châu Âu (Schengen), Mỹ, Canada, Anh, Úc chấp thuận.</p>
      <h4>Quyền Lợi Y Tế Quốc Tế</h4>
      <ul>
        <li>Chi phí y tế cấp cứu và nằm viện ở nước ngoài: Tối đa 2.500.000.000 VNĐ (€100.000 / $100.000).</li>
        <li>Vận chuyển y tế cấp cứu hồi hương: Chi trả 100% thực tế theo chỉ định của bác sĩ SOS International.</li>
        <li>Trợ cấp nằm viện nước ngoài: 1.500.000 đ/ngày.</li>
      </ul>
      <h4>Sự Cố Chuyến Đi</h4>
      <ul>
        <li>Trễ chuyến bay liên tục từ 4 giờ: Bồi thường 2.000.000 đ/mỗi 4 giờ (Tối đa 12.000.000 đ).</li>
        <li>Hành lý đến chậm hoặc thất lạc: Tối đa 30.000.000 đ.</li>
        <li>Mất giấy tờ thông hành, hộ chiếu (Passport): Hỗ trợ chi phí cấp lại đến 20.000.000 đ.</li>
      </ul>
    `
  },
  business: {
    category: 'Bảo hiểm Doanh Nghiệp & Tài Sản',
    title: 'BizShield Bảo Vệ Doanh Nghiệp & Cháy Nổ Bắt Buộc',
    html: `
      <p>Giải pháp bảo vệ tài sản doanh nghiệp, kho bãi, máy móc và trách nhiệm pháp lý theo chuẩn quy định Nhà nước.</p>
      <h4>Phạm Vi Bảo Vệ</h4>
      <ul>
        <li>Bảo hiểm Cháy nổ bắt buộc theo Nghị định 97/2021/NĐ-CP và Nghị định 23/2018/NĐ-CP.</li>
        <li>Thiệt hại tài sản do giông bão, ngập lụt, vỡ đường ống nước, va chạm phương tiện.</li>
        <li>Chi phí dọn dẹp hiện trường và cứu hộ tài sản: Hỗ trợ 10% giá trị bồi thường.</li>
        <li>Bảo hiểm trách nhiệm công cộng đối với người thứ ba lên đến 10 tỷ đồng/vụ.</li>
      </ul>
    `
  },
  silver: {
    category: 'Bảo hiểm Sức Khỏe Cha Mẹ',
    title: 'SilverCare Người Cao Tuổi (50 - 75 Tuổi)',
    html: `
      <p>Thiết kế dành riêng cho đấng sinh thành, thủ tục tham gia đơn giản không qua khám sức khỏe rườm rà.</p>
      <h4>Quyền Lợi Trọng Tâm</h4>
      <ul>
        <li>Chi phí viện phí nội trú và phẫu thuật: Lên đến 500.000.000 đ/năm.</li>
        <li>Bảo vệ các bệnh lý tuổi già phổ biến (Huyết áp, tim mạch, khớp...) sau thời gian chờ luật định.</li>
        <li>Hỗ trợ chi phí điều dưỡng y tế chăm sóc tại nhà sau phẫu thuật: Tối đa 300.000 đ/ngày.</li>
        <li>Đường dây nóng kết nối trực tiếp bác sĩ chuyên khoa lão khoa tư vấn chế độ ăn uống, dùng thuốc hàng ngày.</li>
      </ul>
    `
  }
};

function initProductModal() {
  const modal = document.getElementById('productModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalCancelBtn = document.getElementById('modalCancelBtn');
  const modalCtaBtn = document.getElementById('modalCtaBtn');
  const modalCategoryBadge = document.getElementById('modalCategoryBadge');
  const modalTitle = document.getElementById('modalTitle');
  const modalBody = document.getElementById('modalBody');

  if (!modal) return;

  const detailButtons = document.querySelectorAll('.open-detail-modal');

  detailButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const prodKey = btn.getAttribute('data-product');
      const data = productDetailsData[prodKey];
      if (data) {
        modalCategoryBadge.textContent = data.category;
        modalTitle.textContent = data.title;
        modalBody.innerHTML = data.html;
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  if (modalCancelBtn) modalCancelBtn.addEventListener('click', closeModal);
  if (modalCtaBtn) modalCtaBtn.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeModal();
    }
  });
}

/* ─── 4. HOSPITAL DIRECTORY FINDER ─── */
function initHospitalFinder() {
  const cityButtons = document.querySelectorAll('.city-btn');
  const searchInput = document.getElementById('hospitalSearch');
  const hospitalCards = document.querySelectorAll('.hosp-card');

  if (!searchInput || hospitalCards.length === 0) return;

  let currentCity = 'all';
  let searchQuery = '';

  function filterHospitals() {
    hospitalCards.forEach(card => {
      const cardCity = card.getAttribute('data-city');
      const cardText = card.textContent.toLowerCase();

      const matchesCity = (currentCity === 'all' || cardCity === currentCity);
      const matchesSearch = (!searchQuery || cardText.includes(searchQuery));

      if (matchesCity && matchesSearch) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  cityButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      cityButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCity = btn.getAttribute('data-city');
      filterHospitals();
    });
  });

  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    filterHospitals();
  });
}

/* ─── 5. FAQ ACCORDION ─── */
function initFaqAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    if (!questionBtn) return;

    questionBtn.addEventListener('click', () => {
      const isOpen = item.classList.contains('active');

      // Close other items
      faqItems.forEach(otherItem => {
        if (otherItem !== item) {
          otherItem.classList.remove('active');
        }
      });

      // Toggle current
      if (isOpen) {
        item.classList.remove('active');
      } else {
        item.classList.add('active');
      }
    });
  });
}

/* ─── 6. LEAD CONSULTATION FORM & TOAST ─── */
function initLeadForm() {
  const leadForm = document.getElementById('leadForm');
  const toast = document.getElementById('toastNotification');
  const toastTitle = document.getElementById('toastTitle');
  const toastMsg = document.getElementById('toastMsg');

  if (!leadForm || !toast) return;

  leadForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const fullName = document.getElementById('fullName').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const productSelect = document.getElementById('targetProduct');
    const selectedProductName = productSelect.options[productSelect.selectedIndex].text;

    if (!fullName || !phone) {
      alert('Vui lòng nhập họ tên và số điện thoại liên hệ.');
      return;
    }

    // Phone validation for Vietnam
    const phoneRegex = /(84|0[3|5|7|8|9])+([0-9]{8})\b/;
    if (!phoneRegex.test(phone.replace(/\s+/g, ''))) {
      alert('Vui lòng nhập số điện thoại hợp lệ (10 chữ số).');
      return;
    }

    // Show Toast
    toastTitle.textContent = `Tiếp nhận thành công!`;
    toastMsg.textContent = `Cảm ơn ${fullName}. Chuyên viên tư vấn cho gói "${selectedProductName}" sẽ liên hệ qua SĐT ${phone} trong 15 phút.`;

    toast.classList.add('show');
    leadForm.reset();

    setTimeout(() => {
      toast.classList.remove('show');
    }, 5500);
  });
}

/* ─── 7. MOBILE MENU & SMOOTH NAV ─── */
function initMobileMenu() {
  const menuToggle = document.getElementById('menuToggle');
  const navMenu = document.getElementById('navMenu');

  if (!menuToggle || !navMenu) return;

  menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('open');
  });

  const navLinks = navMenu.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
    });
  });
}
