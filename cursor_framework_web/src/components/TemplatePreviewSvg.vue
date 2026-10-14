<script setup lang="ts">
import { computed } from 'vue'
import { templates } from '../data/templates'

const props = defineProps<{ slug: string }>()

const template = computed(() => templates.find((t) => t.slug === props.slug))
</script>

<template>
  <div class="template-thumbnail" :data-slug="slug">
    <div class="thumbnail-inner">
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 1. INSURANCE: AEGIS BẢO AN - BẢO HIỂM TOÀN DIỆN 4.0                  -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-if="slug === 'insurance'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="ins-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#041224" />
            <stop offset="60%" stop-color="#082346" />
            <stop offset="100%" stop-color="#020e1c" />
          </linearGradient>
          <linearGradient id="ins-gold" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#fbbf24" />
            <stop offset="100%" stop-color="#d97706" />
          </linearGradient>
          <linearGradient id="ins-shield-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#0284c7" stop-opacity="0.5" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#ins-bg)" />

        <!-- Browser chrome bar -->
        <rect x="0" y="0" width="400" height="22" fill="#030b15" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#081c33" stroke="#0f345c" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#38bdf8" font-size="7.5" font-family="monospace">🔒 https://aegisbaoan.vn/bao-hiem-4.0</text>

        <!-- Navbar -->
        <rect x="0" y="22" width="400" height="24" fill="#041429" opacity="0.9" />
        <circle cx="20" cy="34" r="5" fill="#f59e0b" />
        <path d="M20 30.5 L24 33 L20 37.5 L16 33 Z" fill="#041429" />
        <text x="30" y="37" fill="#ffffff" font-size="9" font-weight="700" letter-spacing="0.5">AEGIS BẢO AN</text>
        <text x="135" y="36.5" fill="#94a3b8" font-size="7">Sản phẩm</text>
        <text x="175" y="36.5" fill="#94a3b8" font-size="7">Bồi thường 24h</text>
        <text x="235" y="36.5" fill="#94a3b8" font-size="7">680+ Bệnh viện</text>
        <rect x="316" y="27" width="70" height="14" rx="7" fill="url(#ins-gold)" />
        <text x="328" y="37" fill="#041224" font-size="7" font-weight="700">TÍNH PHÍ 30S</text>

        <!-- Hero Content -->
        <rect x="18" y="56" width="95" height="12" rx="6" fill="#0369a1" fill-opacity="0.3" stroke="#38bdf8" stroke-width="0.7" />
        <circle cx="26" cy="62" r="2" fill="#22c55e" class="pulse-dot" />
        <text x="33" y="65" fill="#38bdf8" font-size="6.5" font-weight="600">BẢO HIỂM DOANH NGHIỆP 4.0</text>

        <text x="18" y="86" fill="#ffffff" font-size="14" font-weight="800">Bảo Vệ Toàn Diện</text>
        <text x="18" y="103" fill="#38bdf8" font-size="14" font-weight="800">Sức Khỏe & Tài Sản</text>
        <text x="18" y="118" fill="#94a3b8" font-size="7.5">Bồi thường e-Claim trực tuyến 24h · 680+ Bệnh viện</text>

        <!-- CTAs -->
        <rect x="18" y="128" width="80" height="18" rx="4" fill="url(#ins-gold)" />
        <text x="27" y="140" fill="#041224" font-size="7.5" font-weight="700">Đăng Ký Tư Vấn</text>
        <rect x="104" y="128" width="68" height="18" rx="4" fill="#0b294d" stroke="#1d4ed8" stroke-width="0.8" />
        <text x="113" y="140" fill="#ffffff" font-size="7.5">Xem Quyền Lợi</text>

        <!-- Trust badges bottom -->
        <rect x="18" y="160" width="60" height="24" rx="3" fill="#061c36" stroke="#0e3d74" stroke-width="0.6" />
        <text x="24" y="171" fill="#38bdf8" font-size="8" font-weight="700">680+</text>
        <text x="24" y="180" fill="#64748b" font-size="6">Bệnh viện bảo lãnh</text>

        <rect x="84" y="160" width="60" height="24" rx="3" fill="#061c36" stroke="#0e3d74" stroke-width="0.6" />
        <text x="90" y="171" fill="#22c55e" font-size="8" font-weight="700">24H</text>
        <text x="90" y="180" fill="#64748b" font-size="6">e-Claim tức thì</text>

        <rect x="150" y="160" width="60" height="24" rx="3" fill="#061c36" stroke="#0e3d74" stroke-width="0.6" />
        <text x="156" y="171" fill="#fbbf24" font-size="8" font-weight="700">99.2%</text>
        <text x="156" y="180" fill="#64748b" font-size="6">Hài lòng bồi thường</text>

        <!-- Right Side: 3 Package cards + Floating Golden Shield -->
        <g class="float-slow">
          <!-- Shield Card -->
          <rect x="230" y="54" width="154" height="136" rx="8" fill="#051c36" stroke="#0284c7" stroke-width="1.2" opacity="0.95" />
          <rect x="238" y="62" width="138" height="34" rx="5" fill="#0a2a50" />
          <circle cx="254" cy="79" r="10" fill="url(#ins-shield-grad)" />
          <path d="M254 73 L260 76 L254 84 L248 76 Z" fill="#ffffff" />
          <text x="270" y="76" fill="#ffffff" font-size="8" font-weight="700">Aegis Care Plus</text>
          <text x="270" y="86" fill="#38bdf8" font-size="6.5">Bảo vệ sức khỏe 1.2 tỷ / năm</text>

          <!-- Plan items -->
          <rect x="238" y="102" width="138" height="26" rx="4" fill="#062242" />
          <text x="246" y="113" fill="#e2e8f0" font-size="7" font-weight="600">Aegis Enterprise Biz</text>
          <text x="246" y="123" fill="#f59e0b" font-size="6.5">Hạn mức bồi thường 50 tỷ</text>

          <rect x="238" y="132" width="138" height="26" rx="4" fill="#062242" />
          <text x="246" y="143" fill="#e2e8f0" font-size="7" font-weight="600">Aegis Wealth Life</text>
          <text x="246" y="153" fill="#10b981" font-size="6.5">Tích lũy & hoàn phí 110%</text>

          <rect x="238" y="164" width="138" height="18" rx="3" fill="#0284c7" />
          <text x="278" y="176" fill="#ffffff" font-size="7" font-weight="700">BẢNG PHÍ TỰ ĐỘNG</text>
        </g>

        <!-- Floating live badge -->
        <g class="float-fast">
          <rect x="210" y="180" width="105" height="22" rx="11" fill="#0a192f" stroke="#fbbf24" stroke-width="1" />
          <circle cx="222" cy="191" r="3" fill="#fbbf24" class="pulse-dot" />
          <text x="230" y="194" fill="#fbbf24" font-size="6.5" font-weight="700">⚡ e-Claim đã duyệt: 14.8 Tỷ</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 2. CRM: HELIX CRM - PIPELINE & ANALYTICS DASHBOARD                 -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'crm'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="crm-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0b0f19" />
            <stop offset="100%" stop-color="#111827" />
          </linearGradient>
          <linearGradient id="crm-chart" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#6366f1" stop-opacity="0.4" />
            <stop offset="100%" stop-color="#6366f1" stop-opacity="0.0" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#crm-bg)" />

        <!-- Chrome -->
        <rect x="0" y="0" width="400" height="22" fill="#080c14" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="200" height="14" rx="4" fill="#131b2e" stroke="#1f293d" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#818cf8" font-size="7.5" font-family="monospace">🔒 https://helixcrm.io/sales-pipeline</text>

        <!-- Left Mini Sidebar -->
        <rect x="0" y="22" width="42" height="228" fill="#0c111d" />
        <circle cx="21" cy="36" r="7" fill="#6366f1" />
        <rect x="12" y="58" width="18" height="12" rx="2" fill="#1e293b" />
        <rect x="12" y="78" width="18" height="12" rx="2" fill="#6366f1" />
        <rect x="12" y="98" width="18" height="12" rx="2" fill="#1e293b" />
        <rect x="12" y="118" width="18" height="12" rx="2" fill="#1e293b" />

        <!-- Top Nav in Content -->
        <rect x="42" y="22" width="358" height="26" fill="#111827" stroke="#1f293d" stroke-width="0.5" />
        <text x="54" y="38" fill="#ffffff" font-size="9" font-weight="700">PIPELINE DASHBOARD</text>
        <circle cx="355" cy="35" r="7" fill="#38bdf8" />
        <circle cx="376" cy="35" r="7" fill="#6366f1" />
        <circle cx="376" cy="31" r="2" fill="#22c55e" class="pulse-dot" />

        <!-- 3 KPI Cards -->
        <rect x="52" y="56" width="102" height="42" rx="5" fill="#172033" stroke="#25324d" stroke-width="0.8" />
        <text x="60" y="68" fill="#94a3b8" font-size="6.5">TOTAL REVENUE (MRR)</text>
        <text x="60" y="84" fill="#ffffff" font-size="12" font-weight="800">$148,520</text>
        <text x="60" y="94" fill="#22c55e" font-size="6.5">↑ +38.4% MoM</text>

        <rect x="162" y="56" width="102" height="42" rx="5" fill="#172033" stroke="#25324d" stroke-width="0.8" />
        <text x="170" y="68" fill="#94a3b8" font-size="6.5">WON DEALS</text>
        <text x="170" y="84" fill="#ffffff" font-size="12" font-weight="800">1,280 Deals</text>
        <text x="170" y="94" fill="#6366f1" font-size="6.5">★ Conversion: 47%</text>

        <rect x="272" y="56" width="118" height="42" rx="5" fill="#172033" stroke="#25324d" stroke-width="0.8" />
        <text x="280" y="68" fill="#94a3b8" font-size="6.5">AVG DEAL SIZE</text>
        <text x="280" y="84" fill="#fbbf24" font-size="12" font-weight="800">$8,450</text>
        <text x="280" y="94" fill="#38bdf8" font-size="6.5">Enterprise Sales</text>

        <!-- Kanban Columns -->
        <!-- Col 1: Qualified -->
        <rect x="52" y="106" width="102" height="132" rx="5" fill="#0f172a" stroke="#1e293b" stroke-width="0.8" />
        <rect x="58" y="112" width="90" height="14" rx="3" fill="#1e293b" />
        <text x="64" y="122" fill="#94a3b8" font-size="7" font-weight="600">Leads (28)</text>

        <g class="float-slow">
          <rect x="58" y="132" width="90" height="34" rx="4" fill="#1e293b" stroke="#334155" stroke-width="0.6" />
          <text x="64" y="144" fill="#ffffff" font-size="7" font-weight="600">VNG Tech Group</text>
          <text x="64" y="154" fill="#38bdf8" font-size="6.5">$24,000 · SLA 2h</text>
        </g>

        <rect x="58" y="172" width="90" height="30" rx="4" fill="#1e293b" />
        <text x="64" y="184" fill="#e2e8f0" font-size="7">Momo Payment</text>
        <text x="64" y="194" fill="#94a3b8" font-size="6">$12,500</text>

        <!-- Col 2: In Proposal -->
        <rect x="162" y="106" width="102" height="132" rx="5" fill="#0f172a" stroke="#1e293b" stroke-width="0.8" />
        <rect x="168" y="112" width="90" height="14" rx="3" fill="#312e81" />
        <text x="174" y="122" fill="#a5b4fc" font-size="7" font-weight="600">Demo Scheduled (14)</text>

        <g class="float-gentle">
          <rect x="168" y="132" width="90" height="38" rx="4" fill="#1e293b" stroke="#6366f1" stroke-width="0.9" />
          <text x="174" y="144" fill="#ffffff" font-size="7" font-weight="700">Shopee Logistics</text>
          <text x="174" y="154" fill="#6366f1" font-size="6.5">$65,000 · Contract Review</text>
          <circle cx="246" cy="158" r="4" fill="#22c55e" />
        </g>

        <!-- Col 3: Won Chart -->
        <rect x="272" y="106" width="118" height="132" rx="5" fill="#0f172a" stroke="#1e293b" stroke-width="0.8" />
        <text x="280" y="122" fill="#ffffff" font-size="7.5" font-weight="700">REVENUE VELOCITY</text>
        <!-- Sparkline Curve -->
        <path d="M280 190 Q300 170 320 175 T350 145 T380 135 L380 210 L280 210 Z" fill="url(#crm-chart)" />
        <path d="M280 190 Q300 170 320 175 T350 145 T380 135" fill="none" stroke="#6366f1" stroke-width="2" />
        <circle cx="380" cy="135" r="3.5" fill="#22c55e" class="pulse-dot" />
        <text x="280" y="226" fill="#94a3b8" font-size="6.5">Q3 Target: 118% Achieved</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 3. SALE: CYBER DEAL PRO - FLASH SALE E-COMMERCE                    -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'sale'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="sale-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#140700" />
            <stop offset="60%" stop-color="#2a0d02" />
            <stop offset="100%" stop-color="#0d0401" />
          </linearGradient>
          <linearGradient id="sale-btn" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#f97316" />
            <stop offset="100%" stop-color="#ea580c" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#sale-bg)" />

        <!-- Chrome -->
        <rect x="0" y="0" width="400" height="22" fill="#0a0503" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#1c0d06" stroke="#381a0e" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#fb923c" font-size="7.5" font-family="monospace">🔒 https://megasale.vn/flash-cyber-deal</text>

        <!-- Top Urgency Banner -->
        <rect x="0" y="22" width="400" height="18" fill="#ea580c" />
        <text x="200" y="34" fill="#ffffff" font-size="7.5" font-weight="800" text-anchor="middle" letter-spacing="1">⚡ FLASH SALE 50% HÔM NAY · FREESHIP TOÀN QUỐC ⚡</text>

        <!-- Hero text -->
        <rect x="20" y="52" width="90" height="14" rx="4" fill="#431407" stroke="#f97316" stroke-width="0.8" />
        <text x="26" y="62" fill="#fb923c" font-size="7" font-weight="700">GIỚI HẠN 24H CHỈ CÒN</text>

        <!-- Countdown timer boxes -->
        <g class="float-gentle">
          <rect x="20" y="74" width="28" height="26" rx="4" fill="#240c04" stroke="#f97316" stroke-width="1" />
          <text x="34" y="91" fill="#ffffff" font-size="11" font-weight="800" text-anchor="middle">08</text>
          <text x="34" y="98" fill="#ea580c" font-size="5" text-anchor="middle">GIỜ</text>

          <text x="52" y="91" fill="#f97316" font-size="11" font-weight="800">:</text>

          <rect x="58" y="74" width="28" height="26" rx="4" fill="#240c04" stroke="#f97316" stroke-width="1" />
          <text x="72" y="91" fill="#ffffff" font-size="11" font-weight="800" text-anchor="middle">24</text>
          <text x="72" y="98" fill="#ea580c" font-size="5" text-anchor="middle">PHÚT</text>

          <text x="90" y="91" fill="#f97316" font-size="11" font-weight="800">:</text>

          <rect x="96" y="74" width="28" height="26" rx="4" fill="#240c04" stroke="#f97316" stroke-width="1" />
          <text x="110" y="91" fill="#ffffff" font-size="11" font-weight="800" text-anchor="middle">15</text>
          <text x="110" y="98" fill="#ea580c" font-size="5" text-anchor="middle">GIÂY</text>
        </g>

        <text x="20" y="122" fill="#ffffff" font-size="13" font-weight="900">Tai Nghe Không Dây Pro Max</text>
        <text x="20" y="136" fill="#fed7aa" font-size="7.5">Chống ồn chủ động ANC 45dB · Pin 60H</text>

        <!-- Price -->
        <text x="20" y="162" fill="#f97316" font-size="18" font-weight="900">$299</text>
        <text x="74" y="162" fill="#78716c" font-size="10" text-decoration="line-through">$599</text>
        <rect x="112" y="150" width="38" height="15" rx="3" fill="#dc2626" />
        <text x="120" y="161" fill="#ffffff" font-size="7.5" font-weight="800">-50%</text>

        <!-- CTA -->
        <rect x="20" y="174" width="130" height="26" rx="5" fill="url(#sale-btn)" />
        <text x="45" y="190" fill="#ffffff" font-size="8.5" font-weight="800">MUA NGAY (FREESHIP)</text>

        <!-- Social proof -->
        <text x="20" y="214" fill="#facc15" font-size="8">★★★★★</text>
        <text x="56" y="214" fill="#d6d3d1" font-size="7">4.9/5 · 2,840+ Đã Bán</text>

        <!-- Right Product Showcase Card -->
        <g class="float-slow">
          <rect x="195" y="54" width="185" height="175" rx="8" fill="#1f0b04" stroke="#7c2d12" stroke-width="1.2" />
          <!-- Headphone illustration -->
          <circle cx="287" cy="120" r="44" fill="#301105" />
          <path d="M260 120 A 28 28 0 0 1 315 120" fill="none" stroke="#f97316" stroke-width="6" stroke-linecap="round" />
          <rect x="252" y="115" width="12" height="24" rx="4" fill="#fb923c" />
          <rect x="310" y="115" width="12" height="24" rx="4" fill="#fb923c" />

          <!-- Badge -->
          <rect x="206" y="66" width="75" height="16" rx="4" fill="#ea580c" />
          <text x="214" y="77" fill="#ffffff" font-size="7" font-weight="800">🔥 BEST SELLER #1</text>

          <rect x="206" y="190" width="163" height="24" rx="4" fill="#140702" stroke="#431407" stroke-width="0.8" />
          <text x="216" y="202" fill="#ffffff" font-size="7" font-weight="700">Bảo hành 24 Tháng 1-Đổi-1</text>
          <text x="216" y="210" fill="#fb923c" font-size="6">Đổi trả miễn phí 30 ngày tận nhà</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 4. REALESTATE: LUXSTAY REALTY - BẤT ĐỘNG SẢN NGHỈ DƯỠNG           -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'realestate'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="re-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#051525" />
            <stop offset="100%" stop-color="#0b2238" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#re-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#030c14" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#081e33" stroke="#0e375e" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#38bdf8" font-size="7.5" font-family="monospace">🔒 https://luxstay.vn/villas-penthouse</text>

        <!-- Navbar -->
        <rect x="0" y="22" width="400" height="24" fill="#061a2e" opacity="0.9" />
        <text x="20" y="37" fill="#ffffff" font-size="9" font-weight="800">LUXSTAY REALTY</text>
        <text x="120" y="36.5" fill="#94a3b8" font-size="7">Biệt Thự</text>
        <text x="165" y="36.5" fill="#94a3b8" font-size="7">Penthouse</text>
        <text x="215" y="36.5" fill="#94a3b8" font-size="7">Dự Án Mở Bán</text>

        <!-- Search Filter Bar -->
        <rect x="20" y="54" width="360" height="28" rx="6" fill="#0b2c4d" stroke="#155e75" stroke-width="0.8" />
        <text x="32" y="70" fill="#94a3b8" font-size="7">📍 Thảo Điền, Q.2</text>
        <line x1="120" y1="58" x2="120" y2="78" stroke="#164e63" />
        <text x="130" y="70" fill="#94a3b8" font-size="7">🏠 Penthouse Sky Villa</text>
        <line x1="240" y1="58" x2="240" y2="78" stroke="#164e63" />
        <text x="250" y="70" fill="#38bdf8" font-size="7" font-weight="700">💰 10 - 25 TỶ</text>
        <rect x="325" y="58" width="50" height="20" rx="4" fill="#0284c7" />
        <text x="337" y="71" fill="#ffffff" font-size="7" font-weight="700">TÌM KIẾM</text>

        <!-- Left Villa Showcase -->
        <g class="float-slow">
          <rect x="20" y="90" width="220" height="142" rx="6" fill="#071e33" stroke="#0e4370" stroke-width="1" />
          <!-- Villa architecture facade -->
          <rect x="30" y="100" width="200" height="74" rx="4" fill="#0b3052" />
          <!-- Glass windows -->
          <rect x="40" y="110" width="50" height="50" fill="#38bdf8" opacity="0.3" />
          <rect x="100" y="110" width="60" height="50" fill="#38bdf8" opacity="0.3" />
          <rect x="170" y="110" width="50" height="50" fill="#38bdf8" opacity="0.3" />
          <!-- Infinity Pool -->
          <rect x="30" y="166" width="200" height="8" fill="#0ea5e9" opacity="0.8" />

          <!-- Card details -->
          <text x="32" y="190" fill="#ffffff" font-size="8.5" font-weight="800">Sky Villa Diamond Penthouse</text>
          <text x="32" y="202" fill="#94a3b8" font-size="6.5">350m² · 4 Phòng ngủ · Hồ bơi riêng kính viền tràn bờ</text>
          <text x="32" y="218" fill="#38bdf8" font-size="11" font-weight="900">12.5 TỶ VNĐ</text>
          <rect x="172" y="204" width="58" height="18" rx="3" fill="#0284c7" />
          <text x="180" y="216" fill="#ffffff" font-size="6.5" font-weight="700">XEM 360° VR</text>
        </g>

        <!-- Right Side info cards -->
        <rect x="250" y="90" width="130" height="66" rx="6" fill="#072036" stroke="#0e4370" stroke-width="0.8" />
        <text x="260" y="105" fill="#f59e0b" font-size="7.5" font-weight="800">DỰ ÁN ĐANG MỞ BÁN</text>
        <text x="260" y="120" fill="#ffffff" font-size="8" font-weight="700">The River Thủ Thiêm</text>
        <text x="260" y="132" fill="#94a3b8" font-size="6.5">Chiết khấu 8% trong tuần</text>
        <text x="260" y="146" fill="#22c55e" font-size="7">✓ Sổ hồng vĩnh viễn</text>

        <g class="float-gentle">
          <rect x="250" y="164" width="130" height="68" rx="6" fill="#072036" stroke="#0e4370" stroke-width="0.8" />
          <circle cx="270" cy="184" r="10" fill="#0284c7" />
          <text x="288" y="182" fill="#ffffff" font-size="7.5" font-weight="700">Tư Vấn VIP 1-1</text>
          <text x="288" y="192" fill="#94a3b8" font-size="6.5">Chuyên viên 10 năm kinh nghiệm</text>
          <rect x="260" y="206" width="110" height="18" rx="3" fill="#f59e0b" />
          <text x="284" y="218" fill="#051525" font-size="7" font-weight="800">ĐẶT LỊCH XEM NHÀ</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 5. BAZI: BÁT TỰ TIÊN TRI - TỨ TRỤ MỆNH LÝ                          -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'bazi'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="bazi-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#2a0505" />
            <stop offset="100%" stop-color="#450a0a" />
          </linearGradient>
          <linearGradient id="bazi-gold" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#facc15" />
            <stop offset="100%" stop-color="#ca8a04" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#bazi-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#170202" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#300707" stroke="#500e0e" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#fca5a5" font-size="7.5" font-family="monospace">🔒 https://bazi.master/tu-tru-menh-ly</text>

        <!-- Header -->
        <text x="200" y="44" fill="url(#bazi-gold)" font-size="12" font-weight="900" text-anchor="middle" letter-spacing="1">BÁT TỰ TIÊN TRI · TỨ TRỤ MỆNH LÝ</text>
        <text x="200" y="56" fill="#fca5a5" font-size="7" text-anchor="middle">Thiên Can · Địa Chi · Thần Sát · Dụng Thần Luận Đoán</text>

        <!-- 4 Pillars Cards -->
        <g class="float-gentle">
          <!-- Năm -->
          <rect x="25" y="70" width="80" height="74" rx="5" fill="#380909" stroke="#b91c1c" stroke-width="1" />
          <rect x="25" y="70" width="80" height="16" rx="4" fill="#7f1d1d" />
          <text x="65" y="81" fill="#fef08a" font-size="7" font-weight="700" text-anchor="middle">TRỤ NĂM</text>
          <text x="65" y="103" fill="#ffffff" font-size="12" font-weight="900" text-anchor="middle">Giáp Thìn</text>
          <text x="65" y="117" fill="#86efac" font-size="6.5" text-anchor="middle">Mộc - Rồng (Thổ)</text>
          <text x="65" y="132" fill="#cbd5e1" font-size="6" text-anchor="middle">Thiên Can: Tỉ Kiên</text>

          <!-- Tháng -->
          <rect x="115" y="70" width="80" height="74" rx="5" fill="#380909" stroke="#b91c1c" stroke-width="1" />
          <rect x="115" y="70" width="80" height="16" rx="4" fill="#7f1d1d" />
          <text x="155" y="81" fill="#fef08a" font-size="7" font-weight="700" text-anchor="middle">TRỤ THÁNG</text>
          <text x="155" y="103" fill="#ffffff" font-size="12" font-weight="900" text-anchor="middle">Đinh Mão</text>
          <text x="155" y="117" fill="#f87171" font-size="6.5" text-anchor="middle">Hỏa - Mèo (Mộc)</text>
          <text x="155" y="132" fill="#cbd5e1" font-size="6" text-anchor="middle">Lệnh Tháng: Đế Vượng</text>

          <!-- Ngày (Nhật Chủ) -->
          <rect x="205" y="70" width="80" height="74" rx="5" fill="#450a0a" stroke="#facc15" stroke-width="1.3" />
          <rect x="205" y="70" width="80" height="16" rx="4" fill="#b45309" />
          <text x="245" y="81" fill="#ffffff" font-size="7" font-weight="800" text-anchor="middle">NHẬT CHỦ (NGÀY)</text>
          <text x="245" y="103" fill="#facc15" font-size="12" font-weight="900" text-anchor="middle">Canh Tuất</text>
          <text x="245" y="117" fill="#fef08a" font-size="6.5" text-anchor="middle">Dương Kim - Tướng Tinh</text>
          <text x="245" y="132" fill="#fef08a" font-size="6" font-weight="700" text-anchor="middle">Thân Vượng Đắc Địa</text>

          <!-- Giờ -->
          <rect x="295" y="70" width="80" height="74" rx="5" fill="#380909" stroke="#b91c1c" stroke-width="1" />
          <rect x="295" y="70" width="80" height="16" rx="4" fill="#7f1d1d" />
          <text x="335" y="81" fill="#fef08a" font-size="7" font-weight="700" text-anchor="middle">TRỤ GIỜ</text>
          <text x="335" y="103" fill="#ffffff" font-size="12" font-weight="900" text-anchor="middle">Bính Tý</text>
          <text x="335" y="117" fill="#38bdf8" font-size="6.5" text-anchor="middle">Hỏa - Chuột (Thủy)</text>
          <text x="335" y="132" fill="#cbd5e1" font-size="6" text-anchor="middle">Cung Tử Tức: Quý Nhân</text>
        </g>

        <!-- Bagua Rotating Circle Graphic on the right-bottom -->
        <g class="spin-slow" style="transform-origin: 340px 195px;">
          <circle cx="340" cy="195" r="26" fill="#1c0404" stroke="#facc15" stroke-width="1.2" stroke-dasharray="4 2" />
          <circle cx="340" cy="195" r="14" fill="#500707" />
          <path d="M340 181 A 7 7 0 0 1 340 195 A 7 7 0 0 0 340 209 A 14 14 0 0 1 340 181 Z" fill="#facc15" />
          <circle cx="340" cy="188" r="2" fill="#500707" />
          <circle cx="340" cy="202" r="2" fill="#facc15" />
        </g>

        <!-- Ngũ hành balance bars -->
        <rect x="25" y="156" width="280" height="74" rx="6" fill="#2d0606" stroke="#5a0e0e" stroke-width="0.8" />
        <text x="36" y="172" fill="#fef08a" font-size="8" font-weight="700">NGŨ HÀNH BẢN MỆNH</text>
        <text x="36" y="186" fill="#ffffff" font-size="7">Kim: 28%  |  Mộc: 25%  |  Thủy: 18%  |  Hỏa: 20%  |  Thổ: 9%</text>
        <text x="36" y="202" fill="#86efac" font-size="7" font-weight="700">HỶ DỤNG THẦN: THỦY & THỔ (Khai vận tài lộc)</text>
        <rect x="36" y="210" width="130" height="15" rx="3" fill="url(#bazi-gold)" />
        <text x="46" y="221" fill="#2a0505" font-size="7" font-weight="800">XUẤT BẢN ĐỒ BÁT TỰ CHI TIẾT</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 6. NUMEROLOGY: PYTHAGORAS THẦN SỐ HỌC TOÀN DIỆN                   -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'numerology'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="num-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#050814" />
            <stop offset="100%" stop-color="#0c1736" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#num-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#040610" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#0c1a3b" stroke="#17316a" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#38bdf8" font-size="7.5" font-family="monospace">🔒 https://numerology.vn/life-path-pythagoras</text>

        <!-- Hero text -->
        <text x="20" y="48" fill="#38bdf8" font-size="8" font-weight="700">KHOA HỌC SỐ HỌC PYTHAGORAS</text>
        <text x="20" y="68" fill="#ffffff" font-size="14" font-weight="900">Giải Mã Sứ Mệnh Cuộc Đời</text>

        <!-- Big Life Path Number 8 Card -->
        <g class="float-slow">
          <rect x="20" y="80" width="130" height="145" rx="8" fill="#0e214d" stroke="#06b6d4" stroke-width="1.2" />
          <text x="32" y="98" fill="#a5f3fc" font-size="7.5" font-weight="700">SỐ ĐƯỜNG ĐỜI (LIFE PATH)</text>
          <circle cx="85" cy="140" r="32" fill="#16347a" />
          <text x="85" y="156" fill="#38bdf8" font-size="44" font-weight="900" text-anchor="middle">8</text>
          <text x="85" y="188" fill="#ffffff" font-size="8" font-weight="800" text-anchor="middle">NHÀ LÃNH ĐẠO</text>
          <text x="85" y="200" fill="#93c5fd" font-size="6.5" text-anchor="middle">Tài chính · Uy quyền · Thực tế</text>
          <rect x="30" y="208" width="110" height="12" rx="3" fill="#06b6d4" />
          <text x="45" y="217" fill="#050814" font-size="6" font-weight="800">NĂNG LƯỢNG RUNG ĐỘNG: 94%</text>
        </g>

        <!-- 3 Pyramids on the right -->
        <g class="float-gentle">
          <rect x="165" y="80" width="215" height="145" rx="8" fill="#091838" stroke="#1d4ed8" stroke-width="0.8" />
          <text x="178" y="98" fill="#ffffff" font-size="8.5" font-weight="700">4 ĐỈNH CAO KIM TỰ THÁP</text>

          <!-- Pyramid 1 -->
          <polygon points="195,145 220,110 245,145" fill="#1e3a8a" stroke="#60a5fa" stroke-width="1" />
          <circle cx="220" cy="110" r="7" fill="#f59e0b" />
          <text x="220" y="113" fill="#000" font-size="7" font-weight="800" text-anchor="middle">3</text>
          <text x="220" y="156" fill="#93c5fd" font-size="6" text-anchor="middle">27 Tuổi</text>

          <!-- Pyramid 2 -->
          <polygon points="245,145 275,102 305,145" fill="#1e3a8a" stroke="#60a5fa" stroke-width="1" />
          <circle cx="275" cy="102" r="7" fill="#f59e0b" />
          <text x="275" y="105" fill="#000" font-size="7" font-weight="800" text-anchor="middle">7</text>
          <text x="275" y="156" fill="#93c5fd" font-size="6" text-anchor="middle">36 Tuổi</text>

          <!-- Pyramid 3 -->
          <polygon points="305,145 335,95 365,145" fill="#1e3a8a" stroke="#60a5fa" stroke-width="1" />
          <circle cx="335" cy="95" r="7" fill="#06b6d4" />
          <text x="335" y="98" fill="#000" font-size="7" font-weight="800" text-anchor="middle">11</text>
          <text x="335" y="156" fill="#93c5fd" font-size="6" text-anchor="middle">45 Tuổi</text>

          <!-- 4 Core Indicators row -->
          <rect x="178" y="172" width="190" height="42" rx="4" fill="#0d214d" />
          <text x="188" y="186" fill="#e2e8f0" font-size="7">Sứ mệnh: Số 1 (Tiên phong)</text>
          <text x="280" y="186" fill="#e2e8f0" font-size="7">Linh hồn: Số 4 (Vững vàng)</text>
          <text x="188" y="202" fill="#e2e8f0" font-size="7">Nhân cách: Số 6 (Yêu thương)</text>
          <text x="280" y="202" fill="#38bdf8" font-size="7" font-weight="700">Thái độ: Số 8</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 7. FOOD DELIVERY: SPEEDFOOD GIAO NHANH 15 PHÚT                     -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'food-delivery'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="food-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#180c06" />
            <stop offset="100%" stop-color="#2c1106" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#food-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#0f0703" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#240f06" stroke="#481e0b" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#fb923c" font-size="7.5" font-family="monospace">🔒 https://speedfood.vn/giao-nhanh-15p</text>

        <!-- Navbar -->
        <text x="20" y="38" fill="#ef4444" font-size="10" font-weight="900">SPEED<tspan fill="#f59e0b">FOOD</tspan></text>
        <text x="110" y="37" fill="#94a3b8" font-size="7">🍔 Burger</text>
        <text x="155" y="37" fill="#94a3b8" font-size="7">🍕 Pizza</text>
        <text x="200" y="37" fill="#94a3b8" font-size="7">🍣 Sushi</text>
        <text x="245" y="37" fill="#94a3b8" font-size="7">🥤 Đồ Uống</text>

        <!-- Hero text -->
        <rect x="20" y="54" width="100" height="14" rx="4" fill="#ef4444" />
        <text x="28" y="64" fill="#ffffff" font-size="7" font-weight="800">⚡ GIAO SIÊU TỐC 15 PHÚT</text>
        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">Món Ngon Nóng Hổi</text>
        <text x="20" y="102" fill="#f59e0b" font-size="14" font-weight="900">Giao Tận Cửa Nhà</text>
        <text x="20" y="118" fill="#d1d5db" font-size="7.5">Hơn 5,000+ Nhà hàng liên kết · Freeship đơn từ 99K</text>

        <rect x="20" y="130" width="95" height="22" rx="4" fill="#ef4444" />
        <text x="32" y="144" fill="#ffffff" font-size="7.5" font-weight="800">ĐẶT MÓN NGAY →</text>

        <!-- Right Side Burger Showcase -->
        <g class="float-slow">
          <circle cx="295" cy="130" r="58" fill="#3d1608" stroke="#f97316" stroke-width="1.5" />
          <!-- Burger Bun top -->
          <ellipse cx="295" cy="110" rx="38" ry="18" fill="#d97706" />
          <!-- Sesame dots -->
          <circle cx="285" cy="105" r="1.5" fill="#fef3c7" />
          <circle cx="305" cy="106" r="1.5" fill="#fef3c7" />
          <circle cx="295" cy="100" r="1.5" fill="#fef3c7" />
          <!-- Lettuce wave -->
          <path d="M260 122 Q275 116 295 124 T330 120" stroke="#22c55e" stroke-width="4" fill="none" />
          <!-- Tomato -->
          <rect x="262" y="125" width="66" height="5" rx="2" fill="#ef4444" />
          <!-- Cheese -->
          <polygon points="260,131 330,131 315,138 275,138" fill="#fbbf24" />
          <!-- Patty -->
          <rect x="258" y="136" width="74" height="10" rx="3" fill="#78350f" />
          <!-- Bun bottom -->
          <ellipse cx="295" cy="148" rx="36" ry="10" fill="#d97706" />

          <!-- Floating -30% Tag -->
          <rect x="325" y="80" width="45" height="18" rx="4" fill="#ef4444" />
          <text x="333" y="92" fill="#ffffff" font-size="8" font-weight="800">-30%</text>
        </g>

        <!-- Live order notification bar -->
        <g class="float-fast">
          <rect x="20" y="172" width="180" height="38" rx="6" fill="#1e0b04" stroke="#7c2d12" stroke-width="1" />
          <circle cx="36" cy="191" r="8" fill="#22c55e" />
          <text x="50" y="187" fill="#ffffff" font-size="7" font-weight="700">🛵 Tài xế Nguyễn Văn A</text>
          <text x="50" y="198" fill="#fbbf24" font-size="6.5">Đang giao đơn #SF8492 · Còn 4 phút</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 8. FITNESS: TITANFIT GYM & HUẤN LUYỆN VIÊN 1-1                    -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'fitness'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="fit-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#140608" />
            <stop offset="100%" stop-color="#240a10" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#fit-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#0d0305" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#24070c" stroke="#4c0d18" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#f43f5e" font-size="7.5" font-family="monospace">🔒 https://titanfit.vn/pt-personal-trainer</text>

        <!-- Nav -->
        <text x="20" y="38" fill="#f43f5e" font-size="10" font-weight="900">TITAN<tspan fill="#ffffff">FIT</tspan></text>
        <text x="110" y="37" fill="#94a3b8" font-size="7">Gói Tập</text>
        <text x="160" y="37" fill="#94a3b8" font-size="7">HLV 1-1</text>
        <text x="210" y="37" fill="#94a3b8" font-size="7">Lịch Trình</text>

        <!-- Hero text -->
        <text x="20" y="68" fill="#f43f5e" font-size="8" font-weight="800">CHINH PHỤC VÓC DÁNG LÝ TƯỞNG</text>
        <text x="20" y="88" fill="#ffffff" font-size="14" font-weight="900">Bứt Phá Giới Hạn</text>
        <text x="20" y="104" fill="#ffffff" font-size="14" font-weight="900">Huấn Luyện Viên 1-1</text>
        <text x="20" y="120" fill="#94a3b8" font-size="7.5">Giáo án cá nhân hóa theo chỉ số InBody · Cam kết kết quả</text>

        <rect x="20" y="132" width="105" height="22" rx="4" fill="#f43f5e" />
        <text x="32" y="146" fill="#ffffff" font-size="7.5" font-weight="800">ĐĂNG KÝ TẬP THỬ</text>

        <!-- KPI widgets on right -->
        <g class="float-slow">
          <!-- Calorie Ring Widget -->
          <rect x="195" y="56" width="90" height="85" rx="6" fill="#20080e" stroke="#f43f5e" stroke-width="1" />
          <circle cx="240" cy="94" r="24" fill="none" stroke="#4c0519" stroke-width="5" />
          <circle cx="240" cy="94" r="24" fill="none" stroke="#f43f5e" stroke-width="5" stroke-dasharray="110 40" stroke-linecap="round" />
          <text x="240" y="93" fill="#ffffff" font-size="10" font-weight="800" text-anchor="middle">850</text>
          <text x="240" y="103" fill="#f43f5e" font-size="5.5" font-weight="700" text-anchor="middle">KCAL / 1000</text>
          <text x="240" y="130" fill="#cbd5e1" font-size="6" text-anchor="middle">Tiêu Hao Hôm Nay</text>

          <!-- Heart rate pulse -->
          <rect x="295" y="56" width="90" height="85" rx="6" fill="#20080e" stroke="#fb7185" stroke-width="1" />
          <circle cx="340" cy="80" r="10" fill="#f43f5e" />
          <path d="M305 106 L320 106 L325 96 L332 118 L340 98 L348 112 L355 106 L375 106" fill="none" stroke="#22c55e" stroke-width="2" />
          <text x="340" y="125" fill="#ffffff" font-size="11" font-weight="800" text-anchor="middle">138 BPM</text>
          <text x="340" y="134" fill="#22c55e" font-size="5.5" text-anchor="middle">Nhịp Tim Ổn Định</text>
        </g>

        <!-- Weekly streak bar -->
        <rect x="20" y="170" width="365" height="46" rx="6" fill="#1f070c" stroke="#4c0519" stroke-width="0.8" />
        <text x="32" y="186" fill="#ffffff" font-size="7.5" font-weight="700">LỊCH TẬP TUẦN NÀY (5/7 BUỔI HOÀN THÀNH)</text>
        <rect x="32" y="196" width="40" height="12" rx="3" fill="#22c55e" />
        <text x="42" y="205" fill="#000" font-size="6" font-weight="800">T2 ✓</text>
        <rect x="80" y="196" width="40" height="12" rx="3" fill="#22c55e" />
        <text x="90" y="205" fill="#000" font-size="6" font-weight="800">T3 ✓</text>
        <rect x="128" y="196" width="40" height="12" rx="3" fill="#22c55e" />
        <text x="138" y="205" fill="#000" font-size="6" font-weight="800">T4 ✓</text>
        <rect x="176" y="196" width="40" height="12" rx="3" fill="#22c55e" />
        <text x="186" y="205" fill="#000" font-size="6" font-weight="800">T5 ✓</text>
        <rect x="224" y="196" width="40" height="12" rx="3" fill="#22c55e" />
        <text x="234" y="205" fill="#000" font-size="6" font-weight="800">T6 ✓</text>
        <rect x="272" y="196" width="40" height="12" rx="3" fill="#4c0519" />
        <text x="282" y="205" fill="#94a3b8" font-size="6">T7</text>
        <rect x="320" y="196" width="40" height="12" rx="3" fill="#4c0519" />
        <text x="330" y="205" fill="#94a3b8" font-size="6">CN</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 9. BEAUTY SPA: SERENE LOTUS SPA & CLINIC                          -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'beauty-spa'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="spa-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#1e0821" />
            <stop offset="100%" stop-color="#360d3d" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#spa-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#130416" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#290b30" stroke="#521461" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#f472b6" font-size="7.5" font-family="monospace">🔒 https://serenelotus.vn/spa-treatment</text>

        <!-- Title -->
        <text x="200" y="46" fill="#f472b6" font-size="12" font-weight="900" text-anchor="middle" letter-spacing="1">SERENE LOTUS SPA & CLINIC</text>
        <text x="200" y="58" fill="#fbcfe8" font-size="7" text-anchor="middle">Liệu Pháp Trẻ Hóa Da Tế Bào Gốc & Thư Giãn Chuyên Sâu</text>

        <!-- Lotus Vector in center -->
        <g class="float-slow" style="transform-origin: 200px 96px;">
          <circle cx="200" cy="95" r="26" fill="#4a1254" />
          <!-- Lotus petals -->
          <path d="M200 75 Q212 90 200 108 Q188 90 200 75 Z" fill="#ec4899" />
          <path d="M188 84 Q178 98 196 106 Q194 92 188 84 Z" fill="#f472b6" opacity="0.8" />
          <path d="M212 84 Q222 98 204 106 Q206 92 212 84 Z" fill="#f472b6" opacity="0.8" />
        </g>

        <!-- 3 Service Cards -->
        <rect x="25" y="130" width="105" height="90" rx="6" fill="#2d0b33" stroke="#701a75" stroke-width="0.8" />
        <text x="35" y="148" fill="#ffffff" font-size="7.5" font-weight="700">Trẻ Hóa Collagen</text>
        <text x="35" y="159" fill="#f472b6" font-size="6.5">Liệu trình 60 phút</text>
        <text x="35" y="174" fill="#fbcfe8" font-size="6">Tái tạo cấu trúc da</text>
        <text x="35" y="188" fill="#fbbf24" font-size="9" font-weight="800">890,000đ</text>
        <rect x="35" y="196" width="85" height="16" rx="3" fill="#d946ef" />
        <text x="52" y="207" fill="#ffffff" font-size="6" font-weight="700">ĐẶT LỊCH</text>

        <rect x="145" y="130" width="110" height="90" rx="6" fill="#3b0744" stroke="#d946ef" stroke-width="1.2" />
        <rect x="145" y="130" width="110" height="14" rx="4" fill="#a21caf" />
        <text x="200" y="140" fill="#ffffff" font-size="6.5" font-weight="800" text-anchor="middle">ƯU ĐÃI THÁNG -35%</text>
        <text x="155" y="158" fill="#ffffff" font-size="7.5" font-weight="700">Massage Đá Nóng</text>
        <text x="155" y="169" fill="#f472b6" font-size="6.5">Thảo dược Tây Tạng 90p</text>
        <text x="155" y="188" fill="#fbbf24" font-size="9" font-weight="800">1,250,000đ</text>
        <rect x="155" y="196" width="90" height="16" rx="3" fill="#ec4899" />
        <text x="175" y="207" fill="#ffffff" font-size="6" font-weight="700">ĐẶT NGAY</text>

        <rect x="270" y="130" width="105" height="90" rx="6" fill="#2d0b33" stroke="#701a75" stroke-width="0.8" />
        <text x="280" y="148" fill="#ffffff" font-size="7.5" font-weight="700">Detox Thải Độc Da</text>
        <text x="280" y="159" fill="#f472b6" font-size="6.5">Công nghệ O2 Hydro</text>
        <text x="280" y="174" fill="#fbcfe8" font-size="6">Sạch sâu tinh khiết</text>
        <text x="280" y="188" fill="#fbbf24" font-size="9" font-weight="800">750,000đ</text>
        <rect x="280" y="196" width="85" height="16" rx="3" fill="#d946ef" />
        <text x="297" y="207" fill="#ffffff" font-size="6" font-weight="700">ĐẶT LỊCH</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 10. TRAVEL: VIVU TRAVEL KHÁM PHÁ THIÊN ĐƯỜNG                       -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'travel'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="trav-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#041f38" />
            <stop offset="100%" stop-color="#0369a1" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#trav-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#021526" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#072e52" stroke="#0e5699" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#38bdf8" font-size="7.5" font-family="monospace">🔒 https://vivutravel.vn/tour-phu-quoc-3n2d</text>

        <!-- Island & Palm vector -->
        <ellipse cx="320" cy="170" rx="75" ry="22" fill="#ca8a04" opacity="0.6" />
        <!-- Palm tree trunk & leaves -->
        <path d="M340 170 Q344 140 338 120" stroke="#78350f" stroke-width="3" fill="none" />
        <path d="M338 120 Q320 115 310 128" stroke="#16a34a" stroke-width="2.5" fill="none" />
        <path d="M338 120 Q355 112 365 125" stroke="#16a34a" stroke-width="2.5" fill="none" />
        <path d="M338 120 Q340 105 348 98" stroke="#22c55e" stroke-width="2" fill="none" />

        <!-- Airplane and trail -->
        <g class="float-gentle">
          <path d="M80 65 Q180 40 280 60" stroke="#bae6fd" stroke-width="1.2" stroke-dasharray="3 3" fill="none" />
          <path d="M280 60 L292 57 L288 65 L285 62 Z" fill="#ffffff" />
        </g>

        <!-- Hero text -->
        <rect x="20" y="52" width="110" height="14" rx="4" fill="#0284c7" />
        <text x="28" y="62" fill="#ffffff" font-size="6.5" font-weight="800">✈️ TOUR KHUYẾN MÃI HÈ</text>
        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">Thiên Đường Phú Quốc</text>
        <text x="20" y="102" fill="#facc15" font-size="14" font-weight="900">3 Ngày 2 Đêm Resort 5★</text>
        <text x="20" y="118" fill="#e0f2fe" font-size="7.5">Bao vé máy bay khứ hồi · Buffet sáng · Cano lặn san hô</text>

        <!-- Pricing Card -->
        <rect x="20" y="132" width="165" height="74" rx="6" fill="#082847" stroke="#38bdf8" stroke-width="1" />
        <text x="32" y="150" fill="#94a3b8" font-size="7">GIÁ TOUR TRỌN GÓI CHỈ TỪ</text>
        <text x="32" y="168" fill="#facc15" font-size="14" font-weight="900">2,990,000đ</text>
        <text x="110" y="168" fill="#64748b" font-size="8" text-decoration="line-through">4,500,000đ</text>
        <text x="32" y="180" fill="#22c55e" font-size="6.5">✓ Còn 6 suất bay giờ đẹp</text>
        <rect x="32" y="186" width="140" height="14" rx="3" fill="#f97316" />
        <text x="64" y="196" fill="#ffffff" font-size="6.5" font-weight="800">ĐẶT TOUR GIỮ CHỖ</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 11. EDU TUTOR: EDUSMART ACADEMY LUYỆN THI IELTS                   -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'edu-tutor'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="edu-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0a1a3a" />
            <stop offset="100%" stop-color="#1e3a8a" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#edu-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#061024" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#132752" stroke="#234691" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#60a5fa" font-size="7.5" font-family="monospace">🔒 https://edusmart.edu.vn/ielts-cam-ket-dau-ra</text>

        <text x="20" y="38" fill="#ffffff" font-size="10" font-weight="900">EDUSMART <tspan fill="#fbbf24">ACADEMY</tspan></text>
        <text x="150" y="37" fill="#93c5fd" font-size="7">Khóa Học</text>
        <text x="200" y="37" fill="#93c5fd" font-size="7">Giảng Viên 8.5+</text>
        <text x="270" y="37" fill="#93c5fd" font-size="7">Lịch Thi Thử</text>

        <!-- Hero text -->
        <text x="20" y="66" fill="#facc15" font-size="7.5" font-weight="800">CAM KẾT ĐẦU RA BẰNG HỢP ĐỒNG</text>
        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">Luyện Thi IELTS 8.0+</text>
        <text x="20" y="102" fill="#60a5fa" font-size="14" font-weight="900">Học 1-Kèm-1 Cùng Cựu Giám Khảo</text>
        <text x="20" y="118" fill="#e2e8f0" font-size="7.5">Phương pháp tư duy tuyến tính · Sửa bài Writing chi tiết 24/7</text>

        <!-- 4 skills badges -->
        <rect x="20" y="132" width="40" height="24" rx="4" fill="#172e66" stroke="#3b82f6" stroke-width="0.8" />
        <text x="40" y="143" fill="#93c5fd" font-size="6" text-anchor="middle">LISTENING</text>
        <text x="40" y="153" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">8.5</text>

        <rect x="68" y="132" width="40" height="24" rx="4" fill="#172e66" stroke="#3b82f6" stroke-width="0.8" />
        <text x="88" y="143" fill="#93c5fd" font-size="6" text-anchor="middle">READING</text>
        <text x="88" y="153" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">8.5</text>

        <rect x="116" y="132" width="40" height="24" rx="4" fill="#172e66" stroke="#3b82f6" stroke-width="0.8" />
        <text x="136" y="143" fill="#93c5fd" font-size="6" text-anchor="middle">WRITING</text>
        <text x="136" y="153" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">7.5</text>

        <rect x="164" y="132" width="40" height="24" rx="4" fill="#172e66" stroke="#3b82f6" stroke-width="0.8" />
        <text x="184" y="143" fill="#93c5fd" font-size="6" text-anchor="middle">SPEAKING</text>
        <text x="184" y="153" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">8.0</text>

        <!-- Tutor card right -->
        <g class="float-slow">
          <rect x="235" y="60" width="145" height="155" rx="8" fill="#112552" stroke="#3b82f6" stroke-width="1.2" />
          <circle cx="307" cy="98" r="24" fill="#1e3a8a" />
          <!-- Cap -->
          <polygon points="307,84 287,94 307,100 327,94" fill="#facc15" />
          <rect x="304" y="100" width="6" height="8" fill="#facc15" />

          <text x="307" y="134" fill="#ffffff" font-size="9" font-weight="800" text-anchor="middle">Thầy David Miller</text>
          <text x="307" y="146" fill="#60a5fa" font-size="7" text-anchor="middle">IELTS 9.0 · 12 Năm Kinh Nghiệm</text>

          <rect x="247" y="158" width="121" height="22" rx="4" fill="#0d1b3d" />
          <text x="257" y="172" fill="#22c55e" font-size="7" font-weight="700">★ 98.4% Đỗ Đại Học Top Đầu</text>

          <rect x="247" y="186" width="121" height="20" rx="3" fill="#f59e0b" />
          <text x="274" y="199" fill="#000" font-size="7" font-weight="800">ĐĂNG KÝ THI THỬ</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 12. AGRITECH: SMART FARM IOT GIÁM SÁT THỜI GIAN THỰC               -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'agritech'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="agri-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#02211f" />
            <stop offset="100%" stop-color="#074e47" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#agri-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#021413" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#052c28" stroke="#0e544d" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#2dd4bf" font-size="7.5" font-family="monospace">🔒 https://smartfarm.agri.vn/live-telemetry</text>

        <!-- Title -->
        <text x="20" y="38" fill="#2dd4bf" font-size="10" font-weight="900">AGRITECH <tspan fill="#ffffff">IOT PLATFORM</tspan></text>
        <circle cx="360" cy="35" r="4" fill="#22c55e" class="pulse-dot" />
        <text x="368" y="38" fill="#22c55e" font-size="7">LIVE</text>

        <!-- 4 IoT Gauges -->
        <rect x="20" y="52" width="85" height="52" rx="5" fill="#032b27" stroke="#0f766e" stroke-width="0.8" />
        <text x="28" y="66" fill="#99f6e4" font-size="6.5">ĐỘ ẨM ĐẤT</text>
        <text x="28" y="86" fill="#ffffff" font-size="14" font-weight="900">68.5%</text>
        <text x="28" y="96" fill="#2dd4bf" font-size="6">Tối ưu (Mục tiêu 65%)</text>

        <rect x="115" y="52" width="85" height="52" rx="5" fill="#032b27" stroke="#0f766e" stroke-width="0.8" />
        <text x="123" y="66" fill="#99f6e4" font-size="6.5">ĐỘ PH ĐẤT</text>
        <text x="123" y="86" fill="#38bdf8" font-size="14" font-weight="900">6.8 pH</text>
        <text x="123" y="96" fill="#38bdf8" font-size="6">Độ kiềm lý tưởng</text>

        <rect x="210" y="52" width="85" height="52" rx="5" fill="#032b27" stroke="#0f766e" stroke-width="0.8" />
        <text x="218" y="66" fill="#99f6e4" font-size="6.5">NHIỆT ĐỘ KHÍ</text>
        <text x="218" y="86" fill="#facc15" font-size="14" font-weight="900">26.2°C</text>
        <text x="218" y="96" fill="#facc15" font-size="6">Hệ thống làm mát: OFF</text>

        <rect x="305" y="52" width="75" height="52" rx="5" fill="#032b27" stroke="#0f766e" stroke-width="0.8" />
        <text x="313" y="66" fill="#99f6e4" font-size="6.5">ÁNH SÁNG</text>
        <text x="313" y="86" fill="#ffffff" font-size="12" font-weight="900">8,400 Lx</text>
        <text x="313" y="96" fill="#2dd4bf" font-size="6">Quang hợp 100%</text>

        <!-- Drone & Greenhouse map -->
        <g class="float-slow">
          <rect x="20" y="114" width="240" height="116" rx="6" fill="#02211e" stroke="#0f766e" stroke-width="1" />
          <text x="32" y="130" fill="#ffffff" font-size="8" font-weight="800">SƠ ĐỒ NHÀ KÍNH KHU A (24 HECTA)</text>

          <!-- Grid plots -->
          <rect x="32" y="140" width="45" height="36" rx="3" fill="#064e3b" stroke="#10b981" stroke-width="0.8" />
          <text x="40" y="160" fill="#a7f3d0" font-size="6.5">Lô A1 (Dưa)</text>

          <rect x="85" y="140" width="45" height="36" rx="3" fill="#064e3b" stroke="#10b981" stroke-width="0.8" />
          <text x="93" y="160" fill="#a7f3d0" font-size="6.5">Lô A2 (Cà)</text>

          <rect x="138" y="140" width="45" height="36" rx="3" fill="#064e3b" stroke="#10b981" stroke-width="0.8" />
          <text x="146" y="160" fill="#a7f3d0" font-size="6.5">Lô A3 (Ớt)</text>

          <rect x="191" y="140" width="45" height="36" rx="3" fill="#064e3b" stroke="#10b981" stroke-width="0.8" />
          <text x="200" y="160" fill="#a7f3d0" font-size="6.5">Lô A4 (Rau)</text>

          <!-- Drone status -->
          <circle cx="215" cy="196" r="6" fill="#0ea5e9" />
          <text x="32" y="200" fill="#e2e8f0" font-size="7">🚁 Drone T-40 đang phun sương tự động Lô A3</text>
          <text x="32" y="218" fill="#2dd4bf" font-size="6.5">Tốc độ tưới: 1.2 Lít/phút · Pin: 88%</text>
        </g>

        <!-- Right Side Yield Analysis -->
        <rect x="270" y="114" width="110" height="116" rx="6" fill="#032b27" stroke="#0f766e" stroke-width="0.8" />
        <text x="280" y="130" fill="#facc15" font-size="7.5" font-weight="800">DỰ BÁO NĂNG SUẤT</text>
        <text x="280" y="152" fill="#ffffff" font-size="14" font-weight="900">+42.8%</text>
        <text x="280" y="164" fill="#99f6e4" font-size="6.5">So với canh tác thường</text>
        <text x="280" y="184" fill="#a7f3d0" font-size="6.5">Tiết kiệm nước: 65%</text>
        <text x="280" y="196" fill="#a7f3d0" font-size="6.5">Chi phí nhân công: -50%</text>
        <rect x="280" y="206" width="90" height="16" rx="3" fill="#10b981" />
        <text x="294" y="217" fill="#000" font-size="6" font-weight="800">XUẤT BÁO CÁO</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 13. FARM: GREENFARM NÔNG SẢN HỮU CƠ VIETGAP                        -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'farm'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="farm-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#062410" />
            <stop offset="100%" stop-color="#14532d" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#farm-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#031408" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#0b381a" stroke="#166534" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#86efac" font-size="7.5" font-family="monospace">🔒 https://greenfarm.vn/nong-san-huu-co</text>

        <!-- Navbar -->
        <text x="20" y="38" fill="#4ade80" font-size="10" font-weight="900">GREEN<tspan fill="#facc15">FARM</tspan></text>
        <text x="120" y="37" fill="#bbf7d0" font-size="7">Rau Củ Tươi</text>
        <text x="180" y="37" fill="#bbf7d0" font-size="7">Trứng Sữa</text>
        <text x="240" y="37" fill="#bbf7d0" font-size="7">Truy Xuất QR</text>

        <!-- Hero text -->
        <rect x="20" y="52" width="105" height="14" rx="4" fill="#16a34a" />
        <text x="28" y="62" fill="#ffffff" font-size="6.5" font-weight="800">100% CHUẨN VIETGAP & USDA</text>
        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">Nông Sản Sạch Tươi Ngon</text>
        <text x="20" y="102" fill="#facc15" font-size="14" font-weight="900">Thu Hoạch & Giao Trong Ngày</text>
        <text x="20" y="118" fill="#e2e8f0" font-size="7.5">Không thuốc trừ sâu · Không chất bảo quản · Truy xuất nguồn gốc QR</text>

        <!-- 3 Product Cards -->
        <rect x="20" y="132" width="110" height="96" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="0.8" />
        <text x="30" y="148" fill="#ffffff" font-size="7.5" font-weight="700">Rau Thủy Canh</text>
        <text x="30" y="159" fill="#86efac" font-size="6.5">Xà lách mỡ Đà Lạt 500g</text>
        <text x="30" y="174" fill="#facc15" font-size="9" font-weight="800">35,000đ</text>
        <rect x="30" y="182" width="90" height="16" rx="3" fill="#16a34a" />
        <text x="46" y="193" fill="#ffffff" font-size="6" font-weight="700">MUA NGAY</text>

        <rect x="140" y="132" width="110" height="96" rx="5" fill="#052e16" stroke="#22c55e" stroke-width="0.8" />
        <text x="150" y="148" fill="#ffffff" font-size="7.5" font-weight="700">Cà Chua Bi Hữu Cơ</text>
        <text x="150" y="159" fill="#86efac" font-size="6.5">Ngọt mọng nước hộp 1kg</text>
        <text x="150" y="174" fill="#facc15" font-size="9" font-weight="800">55,000đ</text>
        <rect x="150" y="182" width="90" height="16" rx="3" fill="#16a34a" />
        <text x="166" y="193" fill="#ffffff" font-size="6" font-weight="700">MUA NGAY</text>

        <rect x="260" y="132" width="120" height="96" rx="5" fill="#0d3f20" stroke="#facc15" stroke-width="1.2" />
        <rect x="260" y="132" width="120" height="14" rx="4" fill="#ca8a04" />
        <text x="320" y="142" fill="#000" font-size="6.5" font-weight="800" text-anchor="middle">GIỎ COMBO GIA ĐÌNH</text>
        <text x="270" y="160" fill="#ffffff" font-size="7.5" font-weight="700">Combo 7 Món Tươi</text>
        <text x="270" y="172" fill="#bbf7d0" font-size="6">Đủ ăn 3-4 ngày (5kg)</text>
        <text x="270" y="188" fill="#facc15" font-size="10" font-weight="900">199,000đ</text>
        <rect x="270" y="196" width="100" height="18" rx="3" fill="#22c55e" />
        <text x="292" y="208" fill="#000" font-size="6.5" font-weight="800">ĐẶT ĐỊNH KỲ</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 14. ORCHARD: SUNORCHARD VƯỜN TRÁI CÂY GLOBALGAP                   -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'orchard'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="orc-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#192804" />
            <stop offset="100%" stop-color="#365314" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#orc-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#0e1702" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#243806" stroke="#4d7c0f" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#a3e635" font-size="7.5" font-family="monospace">🔒 https://sunorchard.vn/trai-cay-xuat-khau</text>

        <text x="20" y="38" fill="#a3e635" font-size="10" font-weight="900">SUN<tspan fill="#facc15">ORCHARD</tspan></text>
        <text x="130" y="37" fill="#d9f99d" font-size="7">Sầu Riêng Ri6</text>
        <text x="200" y="37" fill="#d9f99d" font-size="7">Xoài Cát Hòa Lộc</text>
        <text x="280" y="37" fill="#d9f99d" font-size="7">Bưởi Da Xanh</text>

        <!-- Hero text -->
        <rect x="20" y="52" width="115" height="14" rx="4" fill="#65a30d" />
        <text x="28" y="62" fill="#ffffff" font-size="6.5" font-weight="800">ĐẶC SẢN MIỀN TÂY GLOBALGAP</text>
        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">Sầu Riêng Ri6 & Xoài Cát</text>
        <text x="20" y="102" fill="#facc15" font-size="14" font-weight="900">Bao Ăn 1-Đổi-1 Tận Nhà</text>
        <text x="20" y="118" fill="#ecfccb" font-size="7.5">Chín cây tự nhiên · Cơm vàng hạt lép · Giao nhanh thùng xốp lạnh</text>

        <!-- Right Side Fruit Tree and Durian illustration -->
        <g class="float-slow">
          <circle cx="320" cy="130" r="50" fill="#263e08" stroke="#a3e635" stroke-width="1.2" />
          <!-- Durian icon -->
          <ellipse cx="320" cy="130" rx="30" ry="36" fill="#84cc16" />
          <!-- Spikes -->
          <circle cx="310" cy="115" r="3" fill="#4d7c0f" />
          <circle cx="330" cy="115" r="3" fill="#4d7c0f" />
          <circle cx="320" cy="130" r="3" fill="#4d7c0f" />
          <circle cx="310" cy="145" r="3" fill="#4d7c0f" />
          <circle cx="330" cy="145" r="3" fill="#4d7c0f" />
          <text x="320" y="186" fill="#fef08a" font-size="7" font-weight="800" text-anchor="middle">RI6 HẠT LÉP 100%</text>
        </g>

        <!-- 2 product cards -->
        <rect x="20" y="134" width="125" height="84" rx="5" fill="#142304" stroke="#65a30d" stroke-width="0.8" />
        <text x="30" y="150" fill="#ffffff" font-size="8" font-weight="700">Sầu Riêng Ri6 (Nguyên Trái)</text>
        <text x="30" y="162" fill="#bef264" font-size="6.5">Trọng lượng: 2.8kg - 3.5kg</text>
        <text x="30" y="178" fill="#facc15" font-size="10" font-weight="900">145,000đ / kg</text>
        <rect x="30" y="188" width="105" height="18" rx="3" fill="#84cc16" />
        <text x="54" y="200" fill="#000" font-size="6.5" font-weight="800">ĐẶT HÀNG</text>

        <rect x="155" y="134" width="125" height="84" rx="5" fill="#142304" stroke="#65a30d" stroke-width="0.8" />
        <text x="165" y="150" fill="#ffffff" font-size="8" font-weight="700">Xoài Cát Hòa Lộc Loại 1</text>
        <text x="165" y="162" fill="#bef264" font-size="6.5">Hộp 5kg biếu tặng sang trọng</text>
        <text x="165" y="178" fill="#facc15" font-size="10" font-weight="900">95,000đ / kg</text>
        <rect x="165" y="188" width="105" height="18" rx="3" fill="#84cc16" />
        <text x="189" y="200" fill="#000" font-size="6.5" font-weight="800">ĐẶT HÀNG</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 15. AITECH: NEUROAI ENTERPRISE AUTONOMOUS AGENTS                  -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'aitech'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="ai-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0b0417" />
            <stop offset="100%" stop-color="#210a42" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#ai-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#07020f" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#180730" stroke="#3c1075" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#c084fc" font-size="7.5" font-family="monospace">🔒 https://neuroai.tech/enterprise-agents</text>

        <!-- Navbar -->
        <text x="20" y="38" fill="#a855f7" font-size="10" font-weight="900">NEURO<tspan fill="#38bdf8">AI</tspan></text>
        <text x="110" y="37" fill="#d8b4fe" font-size="7">Multi-Agents</text>
        <text x="180" y="37" fill="#d8b4fe" font-size="7">RAG Knowledge</text>
        <text x="260" y="37" fill="#d8b4fe" font-size="7">API & SDK</text>

        <!-- Neural Graph nodes on the right -->
        <g class="float-slow">
          <!-- Synaptic lines -->
          <line x1="260" y1="90" x2="310" y2="70" stroke="#a855f7" stroke-width="1.2" opacity="0.8" />
          <line x1="260" y1="90" x2="310" y2="120" stroke="#38bdf8" stroke-width="1.2" opacity="0.8" />
          <line x1="310" y1="70" x2="360" y2="90" stroke="#38bdf8" stroke-width="1.2" opacity="0.8" />
          <line x1="310" y1="120" x2="360" y2="90" stroke="#ec4899" stroke-width="1.2" opacity="0.8" />
          <line x1="310" y1="120" x2="350" y2="150" stroke="#a855f7" stroke-width="1.2" opacity="0.8" />

          <!-- Nodes -->
          <circle cx="260" cy="90" r="7" fill="#8b5cf6" />
          <circle cx="310" cy="70" r="9" fill="#06b6d4" />
          <circle cx="310" cy="120" r="8" fill="#a855f7" />
          <circle cx="360" cy="90" r="11" fill="#ec4899" />
          <circle cx="350" cy="150" r="7" fill="#06b6d4" />
        </g>

        <!-- Hero Prompt Window -->
        <rect x="20" y="52" width="220" height="96" rx="6" fill="#120624" stroke="#8b5cf6" stroke-width="1" />
        <rect x="20" y="52" width="220" height="18" rx="4" fill="#200a40" />
        <circle cx="30" cy="61" r="2.5" fill="#ef4444" />
        <circle cx="37" cy="61" r="2.5" fill="#eab308" />
        <circle cx="44" cy="61" r="2.5" fill="#22c55e" />
        <text x="56" y="64" fill="#c084fc" font-size="6.5" font-family="monospace">terminal — agent_pipeline.py</text>

        <text x="30" y="84" fill="#38bdf8" font-size="7" font-family="monospace">> agent.run("Synthesize enterprise RAG")</text>
        <text x="30" y="96" fill="#22c55e" font-size="7" font-family="monospace">✔ Vector index loaded: 2.4M embeddings</text>
        <text x="30" y="108" fill="#a855f7" font-size="7" font-family="monospace">✔ Reasoning model: DeepSeek R1 / Claude 3.7</text>
        <text x="30" y="120" fill="#facc15" font-size="7" font-family="monospace">✔ Consensus verified · Latency: 12ms</text>
        <text x="30" y="134" fill="#ffffff" font-size="7.5" font-weight="700">Tokens/s: 240.5 · Accuracy: 99.4%</text>

        <!-- Telemetry widgets bottom -->
        <rect x="20" y="160" width="115" height="58" rx="5" fill="#140728" stroke="#3b156b" stroke-width="0.8" />
        <text x="30" y="174" fill="#94a3b8" font-size="6.5">INFERENCE LATENCY</text>
        <text x="30" y="192" fill="#22c55e" font-size="14" font-weight="900">12 ms</text>
        <text x="30" y="206" fill="#a855f7" font-size="6.5">Real-time Streaming</text>

        <rect x="145" y="160" width="115" height="58" rx="5" fill="#140728" stroke="#3b156b" stroke-width="0.8" />
        <text x="155" y="174" fill="#94a3b8" font-size="6.5">COST OPTIMIZATION</text>
        <text x="155" y="192" fill="#38bdf8" font-size="14" font-weight="900">-78%</text>
        <text x="155" y="206" fill="#38bdf8" font-size="6.5">Smart Prompt Caching</text>

        <rect x="270" y="160" width="110" height="58" rx="5" fill="#140728" stroke="#ec4899" stroke-width="0.8" />
        <text x="280" y="174" fill="#f472b6" font-size="6.5">ACTIVE WORKFLOWS</text>
        <text x="280" y="192" fill="#ffffff" font-size="14" font-weight="900">1,480+</text>
        <text x="280" y="206" fill="#22c55e" font-size="6.5">● All nodes operational</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 16. COMPUTECH: GEARPRO GAMING PC & LINH KIỆN WORKSTATION          -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'computech'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="comp-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#120406" />
            <stop offset="100%" stop-color="#24070a" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#comp-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#0a0203" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#24060b" stroke="#521019" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#f87171" font-size="7.5" font-family="monospace">🔒 https://gearpro.vn/rtx-5090-workstation</text>

        <!-- Navbar -->
        <text x="20" y="38" fill="#ef4444" font-size="10" font-weight="900">GEAR<tspan fill="#ffffff">PRO</tspan></text>
        <text x="110" y="37" fill="#fca5a5" font-size="7">PC Gaming</text>
        <text x="175" y="37" fill="#fca5a5" font-size="7">VGA RTX 50-Series</text>
        <text x="260" y="37" fill="#fca5a5" font-size="7">Build Cấu Hình</text>

        <!-- Hero text -->
        <rect x="20" y="52" width="115" height="14" rx="4" fill="#dc2626" />
        <text x="28" y="62" fill="#ffffff" font-size="6.5" font-weight="800">CẤU HÌNH GAMING TỐI THƯỢNG</text>
        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">ASUS ROG Strix RTX 5090</text>
        <text x="20" y="102" fill="#ef4444" font-size="14" font-weight="900">32GB GDDR7 · PCIe 5.0</text>
        <text x="20" y="118" fill="#cbd5e1" font-size="7.5">Bảo hành 36 tháng chính hãng 1-Đổi-1 · Hỗ trợ trả góp 0%</text>

        <!-- PC Case Graphic right -->
        <g class="float-slow">
          <rect x="250" y="56" width="130" height="155" rx="8" fill="#1a0609" stroke="#ef4444" stroke-width="1.5" />
          <!-- Glass panel with RGB fans -->
          <circle cx="315" cy="95" r="22" fill="#290a10" stroke="#dc2626" stroke-width="2" />
          <circle cx="315" cy="95" r="12" fill="#ef4444" opacity="0.6" />
          <circle cx="315" cy="148" r="22" fill="#290a10" stroke="#38bdf8" stroke-width="2" />
          <circle cx="315" cy="148" r="12" fill="#38bdf8" opacity="0.6" />
          <text x="315" y="196" fill="#ffffff" font-size="7.5" font-weight="800" text-anchor="middle">FPS 240+ @ 4K ULTRA</text>
        </g>

        <!-- Product details card left -->
        <rect x="20" y="132" width="215" height="80" rx="6" fill="#170407" stroke="#4c0d16" stroke-width="0.8" />
        <text x="32" y="148" fill="#facc15" font-size="8" font-weight="800">CẤU HÌNH ĐỀ XUẤT WORKSTATION</text>
        <text x="32" y="160" fill="#ffffff" font-size="7">CPU: Intel Core i9-14900KS | RAM: 64GB DDR5 RGB</text>
        <text x="32" y="172" fill="#ffffff" font-size="7">SSD: 2TB Samsung 990 Pro Gen5 | Nguồn: 1200W Platinum</text>
        <text x="32" y="192" fill="#ef4444" font-size="12" font-weight="900">89,900,000đ</text>
        <rect x="135" y="178" width="90" height="22" rx="3" fill="#dc2626" />
        <text x="147" y="192" fill="#ffffff" font-size="7" font-weight="800">THÊM VÀO GIỎ</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 17. PRESCHOOL: MẦM NON CẦU VỒNG HOA MẶT TRỜI                       -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'preschool'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="pre-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#141a05" />
            <stop offset="100%" stop-color="#2d3a08" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#pre-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#0d1203" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#1e2706" stroke="#41540d" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#facc15" font-size="7.5" font-family="monospace">🔒 https://mamnoncauvong.edu.vn/montessori</text>

        <!-- Rainbow Arc Graphic -->
        <g class="float-slow">
          <path d="M250 180 A 65 65 0 0 1 380 180" fill="none" stroke="#ef4444" stroke-width="5" />
          <path d="M255 180 A 60 60 0 0 1 375 180" fill="none" stroke="#f97316" stroke-width="5" />
          <path d="M260 180 A 55 55 0 0 1 370 180" fill="none" stroke="#facc15" stroke-width="5" />
          <path d="M265 180 A 50 50 0 0 1 365 180" fill="none" stroke="#22c55e" stroke-width="5" />
          <path d="M270 180 A 45 45 0 0 1 360 180" fill="none" stroke="#38bdf8" stroke-width="5" />
          <!-- Smiling Sun -->
          <circle cx="370" cy="95" r="16" fill="#facc15" />
          <circle cx="365" cy="92" r="2" fill="#713f12" />
          <circle cx="375" cy="92" r="2" fill="#713f12" />
          <path d="M366 100 Q370 105 374 100" stroke="#713f12" stroke-width="1.5" fill="none" />
        </g>

        <!-- Hero text -->
        <text x="20" y="38" fill="#facc15" font-size="10" font-weight="900">MẦM NON CẦU VỒNG <tspan fill="#4ade80">HOA MẶT TRỜI</tspan></text>
        <rect x="20" y="52" width="125" height="14" rx="4" fill="#f59e0b" />
        <text x="28" y="62" fill="#000" font-size="6.5" font-weight="800">PHƯƠNG PHÁP MONTESSORI QUỐC TẾ</text>

        <text x="20" y="86" fill="#ffffff" font-size="14" font-weight="900">Môi Trường Hạnh Phúc</text>
        <text x="20" y="102" fill="#facc15" font-size="14" font-weight="900">Ươm Mầm Tài Năng Trẻ</text>
        <text x="20" y="118" fill="#fef08a" font-size="7.5">Camera 24/7 trực tuyến · Bữa ăn dinh dưỡng chuẩn Viện Pasteur</text>

        <!-- 3 Class cards -->
        <rect x="20" y="132" width="70" height="78" rx="5" fill="#1f2808" stroke="#facc15" stroke-width="0.8" />
        <text x="55" y="148" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">LỚP MẦM</text>
        <text x="55" y="160" fill="#e2e8f0" font-size="6.5" text-anchor="middle">12 - 24 Tháng</text>
        <text x="55" y="174" fill="#a3e635" font-size="6" text-anchor="middle">Vận động giác quan</text>
        <rect x="28" y="184" width="54" height="16" rx="3" fill="#84cc16" />
        <text x="36" y="195" fill="#000" font-size="6" font-weight="800">TÌM HIỂU</text>

        <rect x="98" y="132" width="70" height="78" rx="5" fill="#1f2808" stroke="#facc15" stroke-width="0.8" />
        <text x="133" y="148" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">LỚP CHỒI</text>
        <text x="133" y="160" fill="#e2e8f0" font-size="6.5" text-anchor="middle">3 - 4 Tuổi</text>
        <text x="133" y="174" fill="#a3e635" font-size="6" text-anchor="middle">Tư duy ngôn ngữ</text>
        <rect x="106" y="184" width="54" height="16" rx="3" fill="#84cc16" />
        <text x="114" y="195" fill="#000" font-size="6" font-weight="800">TÌM HIỂU</text>

        <rect x="176" y="132" width="70" height="78" rx="5" fill="#1f2808" stroke="#facc15" stroke-width="0.8" />
        <text x="211" y="148" fill="#facc15" font-size="8" font-weight="800" text-anchor="middle">LỚP LÁ</text>
        <text x="211" y="160" fill="#e2e8f0" font-size="6.5" text-anchor="middle">5 Tuổi</text>
        <text x="211" y="174" fill="#a3e635" font-size="6" text-anchor="middle">Tiền tiểu học</text>
        <rect x="184" y="184" width="54" height="16" rx="3" fill="#84cc16" />
        <text x="192" y="195" fill="#000" font-size="6" font-weight="800">TÌM HIỂU</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 18. CHURCH: GIÁO XỨ ÂN ĐIỂN - THÁNH ĐƯỜNG CÔNG GIÁO                -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'church'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="chu-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#24070a" />
            <stop offset="100%" stop-color="#450a0f" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#chu-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#140204" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#2d060a" stroke="#5a0e16" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#fca5a5" font-size="7.5" font-family="monospace">🔒 https://giaoxuandien.vn/phung-vu-loi-chua</text>

        <!-- Gothic Arch & Golden Cross in Center -->
        <g class="float-slow">
          <!-- Radiant rays -->
          <circle cx="200" cy="85" r="42" fill="#7f1d1d" opacity="0.4" />
          <circle cx="200" cy="85" r="30" fill="#991b1b" opacity="0.5" />
          <!-- Cross -->
          <rect x="196" y="55" width="8" height="55" rx="2" fill="#fbbf24" stroke="#ca8a04" stroke-width="0.8" />
          <rect x="180" y="70" width="40" height="8" rx="2" fill="#fbbf24" stroke="#ca8a04" stroke-width="0.8" />
        </g>

        <!-- Title -->
        <text x="200" y="128" fill="#fde047" font-size="12" font-weight="900" text-anchor="middle" letter-spacing="1">GIÁO XỨ ÂN ĐIỂN · THÁNH ĐƯỜNG CÔNG GIÁO</text>
        <text x="200" y="142" fill="#fecaca" font-size="7.5" text-anchor="middle">"Chúa là Đấng chăn giữ tôi, tôi chẳng thiếu thốn gì." — Thi Thiên 23:1</text>

        <!-- Schedule & Ministry cards -->
        <rect x="25" y="156" width="165" height="70" rx="6" fill="#31060a" stroke="#b91c1c" stroke-width="0.9" />
        <text x="35" y="172" fill="#fbbf24" font-size="8" font-weight="800">GIỜ LỄ CHÚA NHẬT</text>
        <text x="35" y="186" fill="#ffffff" font-size="7">Lễ 1: 06h00 (Lễ Sáng)</text>
        <text x="35" y="198" fill="#ffffff" font-size="7">Lễ 2: 08h30 (Dành Cho Thiếu Nhi)</text>
        <text x="35" y="210" fill="#ffffff" font-size="7">Lễ 3: 17h30 (Lễ Chiều & Giới Trẻ)</text>

        <rect x="210" y="156" width="165" height="70" rx="6" fill="#31060a" stroke="#b91c1c" stroke-width="0.9" />
        <text x="220" y="172" fill="#fbbf24" font-size="8" font-weight="800">SINH HOẠT CỘNG ĐOÀN</text>
        <text x="220" y="186" fill="#ffffff" font-size="7">Thứ Sáu 19h30: Giờ Chầu Thánh Thể</text>
        <text x="220" y="198" fill="#ffffff" font-size="7">Ca Đoàn Têrêsa · Ban Bác Ái Xã Hội</text>
        <rect x="220" y="204" width="145" height="15" rx="3" fill="#ca8a04" />
        <text x="248" y="215" fill="#000" font-size="6.5" font-weight="800">XIN Ý CẦU NGUYỆN ONLINE</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 19. BLOG: TECHJOURNAL - TẠP CHÍ CÔNG NGHỆ & ĐỔI MỚI SÁNG TẠO       -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'blog'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="blg-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#061f18" />
            <stop offset="100%" stop-color="#0f3d32" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#blg-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#03120e" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#0a2b22" stroke="#165947" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#34d399" font-size="7.5" font-family="monospace">🔒 https://techjournal.io/ai-revolution-2026</text>

        <!-- Top Nav -->
        <text x="20" y="38" fill="#10b981" font-size="10" font-weight="900">TECH<tspan fill="#ffffff">JOURNAL</tspan></text>
        <text x="120" y="37" fill="#a7f3d0" font-size="7">Trí Tuệ Nhân Tạo</text>
        <text x="200" y="37" fill="#a7f3d0" font-size="7">Kỹ Thuật Web</text>
        <text x="270" y="37" fill="#a7f3d0" font-size="7">Bảo Mật Cloud</text>

        <!-- Featured Article Left -->
        <g class="float-slow">
          <rect x="20" y="52" width="230" height="175" rx="6" fill="#092920" stroke="#10b981" stroke-width="1.2" />
          <rect x="28" y="60" width="214" height="74" rx="4" fill="#114234" />
          <rect x="36" y="68" width="55" height="14" rx="3" fill="#059669" />
          <text x="44" y="78" fill="#ffffff" font-size="6.5" font-weight="800">HOT STORY</text>

          <text x="36" y="150" fill="#ffffff" font-size="10" font-weight="900">Kỷ Nguyên AI Agents 2026: Tự Động Hóa</text>
          <text x="36" y="163" fill="#6ee7b7" font-size="7">Làn sóng chuyển đổi số toàn diện các quy trình vận hành</text>
          <text x="36" y="180" fill="#94a3b8" font-size="6.5">Tác giả: Ts. Hoàng Minh · 6 phút đọc · 1.4k lượt xem</text>

          <rect x="36" y="194" width="80" height="20" rx="3" fill="#10b981" />
          <text x="48" y="207" fill="#000" font-size="7" font-weight="800">ĐỌC BÀI VIẾT →</text>
        </g>

        <!-- Sidebar Articles Right -->
        <rect x="260" y="52" width="120" height="82" rx="5" fill="#092920" stroke="#134e40" stroke-width="0.8" />
        <text x="268" y="68" fill="#facc15" font-size="6.5" font-weight="700">#FRONTEND</text>
        <text x="268" y="82" fill="#ffffff" font-size="7.5" font-weight="700">Top 10 Kiến Trúc Vue 3 & TypeScript</text>
        <text x="268" y="96" fill="#94a3b8" font-size="6">Đăng ngày 12/10 · 840 views</text>

        <rect x="260" y="144" width="120" height="83" rx="5" fill="#092920" stroke="#134e40" stroke-width="0.8" />
        <text x="268" y="160" fill="#38bdf8" font-size="6.5" font-weight="700">#SECURITY</text>
        <text x="268" y="174" fill="#ffffff" font-size="7.5" font-weight="700">Phòng Ngự Zero Trust Cho Doanh Nghiệp</text>
        <text x="268" y="188" fill="#94a3b8" font-size="6">Đăng ngày 10/10 · 1.1k views</text>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 20. PORTFOLIO: ALEX TRẦN - SENIOR FULLSTACK & CREATIVE DESIGNER     -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'portfolio'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="port-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#0a0514" />
            <stop offset="100%" stop-color="#1f0933" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#port-bg)" />
        <rect x="0" y="0" width="400" height="22" fill="#07030e" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#1b082e" stroke="#3e1366" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#f472b6" font-size="7.5" font-family="monospace">🔒 https://alextran.design/selected-works</text>

        <!-- Nav -->
        <text x="20" y="38" fill="#ec4899" font-size="10" font-weight="900">ALEX<tspan fill="#ffffff">.DEV</tspan></text>
        <text x="120" y="37" fill="#fbcfe8" font-size="7">Dự Án</text>
        <text x="170" y="37" fill="#fbcfe8" font-size="7">Kỹ Năng</text>
        <text x="220" y="37" fill="#fbcfe8" font-size="7">Giới Thiệu</text>
        <rect x="300" y="27" width="80" height="14" rx="7" fill="#ec4899" />
        <text x="312" y="37" fill="#ffffff" font-size="6.5" font-weight="700">LIÊN HỆ NGAY</text>

        <!-- Hero text -->
        <g class="float-slow">
          <rect x="20" y="52" width="115" height="14" rx="7" fill="#2d0a3d" stroke="#ec4899" stroke-width="0.8" />
          <circle cx="28" cy="59" r="2.5" fill="#22c55e" class="pulse-dot" />
          <text x="35" y="62" fill="#f472b6" font-size="6.5" font-weight="700">AVAILABLE FOR HIRE</text>
        </g>

        <text x="20" y="86" fill="#ffffff" font-size="15" font-weight="900">Alex Trần</text>
        <text x="20" y="103" fill="#f472b6" font-size="13" font-weight="800">Senior Creative Fullstack</text>
        <text x="20" y="118" fill="#e2e8f0" font-size="7.5">Thiết kế UI/UX đỉnh cao & Lập trình ứng dụng Web hiện đại</text>

        <!-- Tech chips -->
        <rect x="20" y="128" width="48" height="14" rx="3" fill="#2d0a3d" />
        <text x="28" y="138" fill="#f472b6" font-size="6.5">Vue 3</text>
        <rect x="74" y="128" width="58" height="14" rx="3" fill="#2d0a3d" />
        <text x="82" y="138" fill="#38bdf8" font-size="6.5">TypeScript</text>
        <rect x="138" y="128" width="56" height="14" rx="3" fill="#2d0a3d" />
        <text x="146" y="138" fill="#a855f7" font-size="6.5">Three.js</text>

        <!-- Showcase card right -->
        <g class="float-gentle">
          <rect x="215" y="52" width="165" height="175" rx="8" fill="#180729" stroke="#ec4899" stroke-width="1.2" />
          <rect x="225" y="62" width="145" height="80" rx="5" fill="#2b0d47" />
          <circle cx="297" cy="102" r="22" fill="#ec4899" opacity="0.3" />
          <text x="297" y="106" fill="#ffffff" font-size="8" font-weight="800" text-anchor="middle">WEB3 FINTECH APP</text>

          <text x="227" y="158" fill="#ffffff" font-size="8" font-weight="800">Helix Pay — Global Wallet</text>
          <text x="227" y="170" fill="#f472b6" font-size="6.5">Dự án đạt giải Awwwards Site of the Day</text>

          <rect x="227" y="184" width="141" height="20" rx="4" fill="#a21caf" />
          <text x="260" y="197" fill="#ffffff" font-size="7" font-weight="700">XEM CASE STUDY</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 21. AUTO SHOWROOM: AUTOPRIME MOTORS                                  -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'auto-showroom'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="auto-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#070a12" />
            <stop offset="50%" stop-color="#0f172a" />
            <stop offset="100%" stop-color="#1e293b" />
          </linearGradient>
          <linearGradient id="auto-gold" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#fbbf24" />
            <stop offset="100%" stop-color="#d97706" />
          </linearGradient>
          <linearGradient id="auto-car-body" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#334155" />
            <stop offset="50%" stop-color="#64748b" />
            <stop offset="100%" stop-color="#1e293b" />
          </linearGradient>
          <radialGradient id="auto-headlight" cx="0.9" cy="0.6" r="0.5">
            <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8" />
            <stop offset="100%" stop-color="#0284c7" stop-opacity="0" />
          </radialGradient>
        </defs>

        <rect width="400" height="250" fill="url(#auto-bg)" />

        <!-- Browser Top Bar -->
        <rect x="0" y="0" width="400" height="22" fill="#03060c" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="230" height="14" rx="4" fill="#0b1322" stroke="#1e293b" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#f59e0b" font-size="7.5" font-family="monospace">🔒 https://autoprime.vn/showroom-oto-da-hang</text>

        <!-- Navbar -->
        <rect x="0" y="22" width="400" height="24" fill="#0a0f1d" opacity="0.95" />
        <rect x="18" y="27" width="14" height="14" rx="3" fill="url(#auto-gold)" />
        <path d="M21 34 L25 29 L29 34 Z" fill="#070a12" />
        <text x="36" y="37" fill="#ffffff" font-size="9" font-weight="800" letter-spacing="0.5">AUTOPRIME MOTORS</text>
        <text x="160" y="36.5" fill="#94a3b8" font-size="7">Kho Xe Sẵn</text>
        <text x="210" y="36.5" fill="#94a3b8" font-size="7">Lái Thử Tận Nhà</text>
        <text x="272" y="36.5" fill="#94a3b8" font-size="7">Dự Toán Lăn Bánh</text>
        <rect x="330" y="27" width="56" height="14" rx="4" fill="url(#auto-gold)" />
        <text x="338" y="37" fill="#070a12" font-size="7" font-weight="700">1800 6969</text>

        <!-- Hero Content Left -->
        <rect x="18" y="56" width="118" height="12" rx="6" fill="#f59e0b" fill-opacity="0.15" stroke="#f59e0b" stroke-width="0.8" />
        <circle cx="26" cy="62" r="2" fill="#22c55e" class="pulse-dot" />
        <text x="33" y="65" fill="#f59e0b" font-size="6.5" font-weight="700">SIÊU THỊ XE ĐA THƯƠNG HIỆU</text>

        <text x="18" y="86" fill="#ffffff" font-size="14.5" font-weight="800">Sở Hữu Xe Mơ Ước</text>
        <text x="18" y="103" fill="#f59e0b" font-size="14" font-weight="800">Trải Nghiệm 5 Sao</text>
        <text x="18" y="118" fill="#94a3b8" font-size="7.5">176 Hạng mục kiểm định · Vay 85% Lãi từ 6.8%/năm</text>

        <!-- CTAs -->
        <rect x="18" y="128" width="76" height="18" rx="4" fill="url(#auto-gold)" />
        <text x="26" y="140" fill="#070a12" font-size="7.5" font-weight="700">Xem Kho 128+ Xe</text>
        <rect x="100" y="128" width="76" height="18" rx="4" fill="#1e293b" stroke="#334155" stroke-width="0.8" />
        <text x="108" y="140" fill="#ffffff" font-size="7.5">Tính Giá Lăn Bánh</text>

        <!-- Trust Badges bottom -->
        <rect x="18" y="160" width="56" height="24" rx="3" fill="#0d1424" stroke="#1e293b" stroke-width="0.6" />
        <text x="24" y="171" fill="#f59e0b" font-size="8" font-weight="700">5.800+</text>
        <text x="24" y="180" fill="#64748b" font-size="6">Xe đã giao</text>

        <rect x="78" y="160" width="56" height="24" rx="3" fill="#0d1424" stroke="#1e293b" stroke-width="0.6" />
        <text x="84" y="171" fill="#38bdf8" font-size="8" font-weight="700">176 Hạng mục</text>
        <text x="84" y="180" fill="#64748b" font-size="6">Kiểm định chuẩn</text>

        <rect x="138" y="160" width="56" height="24" rx="3" fill="#0d1424" stroke="#1e293b" stroke-width="0.6" />
        <text x="144" y="171" fill="#22c55e" font-size="8" font-weight="700">24H</text>
        <text x="144" y="180" fill="#64748b" font-size="6">Giao xe tận nhà</text>

        <!-- Showcase Car Right (Stylized Luxury Sports Sedan) -->
        <g class="float-gentle">
          <rect x="205" y="52" width="180" height="180" rx="10" fill="#0d1424" stroke="#f59e0b" stroke-width="1.2" opacity="0.95" />
          
          <!-- Car Display Platform -->
          <rect x="215" y="60" width="160" height="95" rx="6" fill="#070b14" />
          <!-- Headlight Glow -->
          <ellipse cx="360" cy="115" rx="40" ry="25" fill="url(#auto-headlight)" />
          
          <!-- Stylized Car Silhouette Vector -->
          <path d="M230 115 C240 102, 260 92, 285 88 C310 84, 335 88, 350 96 L362 108 C366 112, 368 116, 368 120 L368 124 C368 126, 366 128, 362 128 L355 128 C355 120, 345 116, 338 120 C333 124, 333 128, 333 128 L265 128 C265 120, 255 116, 248 120 C243 124, 243 128, 243 128 L232 128 C228 128, 226 126, 226 122 Z" fill="url(#auto-car-body)" />
          <!-- Glass Cabin Window -->
          <path d="M260 94 C275 90, 310 88, 330 96 L342 106 L254 106 Z" fill="#38bdf8" fill-opacity="0.35" stroke="#38bdf8" stroke-width="0.8" />
          <!-- Wheels -->
          <circle cx="254" cy="128" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2.5" />
          <circle cx="254" cy="128" r="3" fill="#f59e0b" />
          <circle cx="344" cy="128" r="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="2.5" />
          <circle cx="344" cy="128" r="3" fill="#f59e0b" />
          <!-- LED Matrix Beam -->
          <line x1="362" y1="110" x2="376" y2="114" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" />

          <!-- Car Info & Price -->
          <text x="218" y="170" fill="#ffffff" font-size="8.5" font-weight="800">Mercedes-Benz C300 AMG 2026</text>
          <text x="218" y="181" fill="#38bdf8" font-size="7">2.0L Turbo 258HP · Lướt 8.500km</text>
          
          <rect x="218" y="188" width="154" height="22" rx="4" fill="#1e293b" />
          <text x="224" y="202" fill="#fbbf24" font-size="8" font-weight="800">1.920.000.000 ₫</text>
          <text x="320" y="202" fill="#4ade80" font-size="6.5" font-weight="700">Trả trước: 288Tr</text>

          <rect x="218" y="214" width="154" height="14" rx="3" fill="url(#auto-gold)" />
          <text x="260" y="224" fill="#070a12" font-size="6.5" font-weight="800">LÁI THỬ TẬN NHÀ MIỄN PHÍ</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- 22. VIET RESTAURANT: VỊ XƯA QUÁN                                      -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else-if="slug === 'viet-restaurant'"
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="rest-bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#120b07" />
            <stop offset="50%" stop-color="#24140b" />
            <stop offset="100%" stop-color="#3d2112" />
          </linearGradient>
          <linearGradient id="rest-gold" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#f59e0b" />
            <stop offset="100%" stop-color="#b45309" />
          </linearGradient>
          <linearGradient id="rest-pot-clay" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#9a3412" />
            <stop offset="100%" stop-color="#431407" />
          </linearGradient>
        </defs>

        <rect width="400" height="250" fill="url(#rest-bg)" />

        <!-- Browser Top Bar -->
        <rect x="0" y="0" width="400" height="22" fill="#0a0503" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <rect x="54" y="4" width="220" height="14" rx="4" fill="#1c0f08" stroke="#451a03" stroke-width="0.8" />
        <text x="64" y="14.5" fill="#f59e0b" font-size="7.5" font-family="monospace">🔒 https://vixuaquan.vn/am-thuc-di-san-3-mien</text>

        <!-- Navbar -->
        <rect x="0" y="22" width="400" height="24" fill="#180e07" opacity="0.95" />
        <circle cx="22" cy="34" r="6" fill="#b45309" />
        <ellipse cx="22" cy="34" rx="4" ry="2" fill="#fef08a" />
        <text x="34" y="37" fill="#ffffff" font-size="9" font-weight="800" font-family="serif">VỊ XƯA QUÁN</text>
        <text x="145" y="36.5" fill="#d6cfc7" font-size="7">Thực Đơn 3 Miền</text>
        <text x="215" y="36.5" fill="#d6cfc7" font-size="7">Voucher 15%</text>
        <text x="270" y="36.5" fill="#d6cfc7" font-size="7">4 Chi Nhánh</text>
        <rect x="325" y="27" width="60" height="14" rx="4" fill="url(#rest-gold)" />
        <text x="333" y="37" fill="#120b07" font-size="7" font-weight="800">ĐẶT BÀN</text>

        <!-- Hero Content Left -->
        <rect x="18" y="56" width="124" height="12" rx="6" fill="#b45309" fill-opacity="0.2" stroke="#d97706" stroke-width="0.8" />
        <circle cx="26" cy="62" r="2" fill="#f59e0b" class="pulse-dot" />
        <text x="33" y="65" fill="#fbbf24" font-size="6.5" font-weight="700">MICHELIN SELECTED 2024-2026</text>

        <text x="18" y="86" fill="#ffffff" font-size="14.5" font-weight="800" font-family="serif">Vị Xưa Tinh Hoa</text>
        <text x="18" y="103" fill="#f59e0b" font-size="13.5" font-weight="800" font-family="serif">Mâm Cơm Gia Đình Việt</text>
        <text x="18" y="118" fill="#d6cfc7" font-size="7.5">Cơm Niêu Cháy Giòn · Cá Bống Kho Tộ Mật Mía</text>

        <!-- CTAs -->
        <rect x="18" y="128" width="80" height="18" rx="4" fill="url(#rest-gold)" />
        <text x="26" y="140" fill="#120b07" font-size="7.5" font-weight="800">Đặt Bàn Nhận 15%</text>
        <rect x="104" y="128" width="72" height="18" rx="4" fill="#2d170b" stroke="#78350f" stroke-width="0.8" />
        <text x="112" y="140" fill="#fef3c7" font-size="7.5">Xem 120+ Món</text>

        <!-- Highlights Bottom -->
        <rect x="18" y="160" width="56" height="24" rx="3" fill="#1e1108" stroke="#451a03" stroke-width="0.6" />
        <text x="24" y="171" fill="#f59e0b" font-size="8" font-weight="700">38+ Năm</text>
        <text x="24" y="180" fill="#a89f91" font-size="6">Giữ lửa di sản</text>

        <rect x="78" y="160" width="56" height="24" rx="3" fill="#1e1108" stroke="#451a03" stroke-width="0.6" />
        <text x="84" y="171" fill="#22c55e" font-size="8" font-weight="700">120 Món</text>
        <text x="84" y="180" fill="#a89f91" font-size="6">Đặc sản 3 miền</text>

        <rect x="138" y="160" width="56" height="24" rx="3" fill="#1e1108" stroke="#451a03" stroke-width="0.6" />
        <text x="144" y="171" fill="#fbbf24" font-size="8" font-weight="700">4.9 ★</text>
        <text x="144" y="180" fill="#a89f91" font-size="6">4.8K+ Đánh giá</text>

        <!-- Showcase Dish Right (Stylized Traditional Clay Pot Rice & Fish Stew) -->
        <g class="float-slow">
          <rect x="205" y="52" width="180" height="180" rx="10" fill="#1e1108" stroke="#d97706" stroke-width="1.2" opacity="0.96" />
          
          <!-- Dish Platter / Bamboo Mat Background -->
          <circle cx="295" cy="112" r="48" fill="#2c170c" stroke="#5c2e0b" stroke-width="2" />
          
          <!-- Steaming Clay Pot (Niêu Đất) -->
          <path d="M260 115 C260 134, 275 145, 295 145 C315 145, 330 134, 330 115 L260 115 Z" fill="url(#rest-pot-clay)" />
          <ellipse cx="295" cy="115" rx="35" ry="8" fill="#78350f" />
          <!-- Golden Crispy Rice Layer -->
          <ellipse cx="295" cy="114" rx="30" ry="6" fill="#fde68a" />
          <!-- Caramelized Fish Stew & Chili in Pot -->
          <ellipse cx="295" cy="113" rx="22" ry="4" fill="#451a03" />
          <circle cx="290" cy="113" r="3" fill="#dc2626" />
          <circle cx="298" cy="113" r="2" fill="#16a34a" />
          
          <!-- Steaming Aroma Curls (Khói Nghi Ngút) -->
          <path d="M285 104 C282 96, 288 90, 284 82" stroke="#fef3c7" stroke-width="1.4" stroke-linecap="round" fill="none" opacity="0.75" />
          <path d="M295 102 C298 94, 292 88, 296 78" stroke="#fef3c7" stroke-width="1.6" stroke-linecap="round" fill="none" opacity="0.85" />
          <path d="M305 104 C308 96, 302 90, 306 82" stroke="#fef3c7" stroke-width="1.4" stroke-linecap="round" fill="none" opacity="0.75" />

          <!-- Dish Info & Voucher Banner -->
          <text x="218" y="170" fill="#ffffff" font-size="8.5" font-weight="700" font-family="serif">Cơm Niêu Cháy Cá Bống Kho Tộ</text>
          <text x="218" y="181" fill="#fef08a" font-size="7">Món ăn biểu tượng văn hóa ẩm thực Việt</text>
          
          <rect x="218" y="188" width="154" height="22" rx="4" fill="#351a0b" stroke="#9a3412" stroke-width="0.8" />
          <text x="224" y="202" fill="#fbbf24" font-size="7.5" font-weight="700">Mã E-Voucher: VIXUA15</text>
          <text x="325" y="202" fill="#4ade80" font-size="7" font-weight="800">Giảm 15%</text>

          <rect x="218" y="214" width="154" height="14" rx="3" fill="url(#rest-gold)" />
          <text x="250" y="224" fill="#120b07" font-size="6.5" font-weight="800">GIỮ BÀN VIEW ĐẸP NGAY</text>
        </g>
      </svg>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- FALLBACK: MODERN ENTERPRISE SAAS DASHBOARD                        -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <svg
        v-else
        class="thumbnail-svg"
        viewBox="0 0 400 250"
        preserveAspectRatio="xMidYMid slice"
        aria-hidden="true"
      >
        <defs>
          <linearGradient :id="`fb-${slug}`" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" :stop-color="template?.accent || '#6366f1'" stop-opacity="0.9" />
            <stop offset="100%" stop-color="#09090b" stop-opacity="1" />
          </linearGradient>
        </defs>
        <rect width="400" height="250" :fill="`url(#fb-${slug})`" />
        <rect x="0" y="0" width="400" height="22" fill="#000000" opacity="0.5" />
        <circle cx="12" cy="11" r="3" fill="#ef4444" opacity="0.85" />
        <circle cx="21" cy="11" r="3" fill="#eab308" opacity="0.85" />
        <circle cx="30" cy="11" r="3" fill="#22c55e" opacity="0.85" />
        <text x="20" y="70" fill="#ffffff" font-size="16" font-weight="900">{{ template?.name || slug }}</text>
        <text x="20" y="90" fill="#cbd5e1" font-size="8.5">{{ template?.tagline || 'Enterprise Template' }}</text>
        <rect x="20" y="120" width="120" height="24" rx="4" fill="#ffffff" />
        <text x="40" y="135" fill="#000000" font-size="7.5" font-weight="800">TRẢI NGHIỆM DEMO</text>
      </svg>

      <!-- Glass light shimmer beam moving continuously across the screen -->
      <div class="shimmer-glass" aria-hidden="true"></div>
    </div>
  </div>
</template>

<style scoped>
.template-thumbnail {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: #09090b;
  pointer-events: none;
  user-select: none;
}

.thumbnail-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: transform;
}

.thumbnail-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}

/* ─── Gentle Motion & Animation Effects ─── */
.float-slow {
  animation: floatSlow 4.5s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}

.float-fast {
  animation: floatFast 3s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}

.float-gentle {
  animation: floatGentle 3.8s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}

.pulse-dot {
  animation: pulseDot 2s ease-in-out infinite;
  transform-box: fill-box;
  transform-origin: center;
}

.spin-slow {
  animation: spinSlow 65s linear infinite;
  transform-box: fill-box;
}

@keyframes floatSlow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3.5px);
  }
}

@keyframes floatFast {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2.5px);
  }
}

@keyframes floatGentle {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-2px) rotate(0.6deg);
  }
}

@keyframes pulseDot {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.35;
    transform: scale(0.8);
  }
}

@keyframes spinSlow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* ─── Shimmer Glass Light Reflection ─── */
.shimmer-glass {
  position: absolute;
  inset: -100% -50%;
  width: 200%;
  height: 300%;
  background: linear-gradient(
    115deg,
    transparent 0%,
    transparent 42%,
    rgba(255, 255, 255, 0.03) 45%,
    rgba(255, 255, 255, 0.12) 48%,
    rgba(255, 255, 255, 0.03) 51%,
    transparent 54%,
    transparent 100%
  );
  animation: glassSweep 6s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  pointer-events: none;
}

@keyframes glassSweep {
  0% {
    transform: translateY(-70%) translateX(-40%);
  }
  28%, 100% {
    transform: translateY(70%) translateX(40%);
  }
}
</style>