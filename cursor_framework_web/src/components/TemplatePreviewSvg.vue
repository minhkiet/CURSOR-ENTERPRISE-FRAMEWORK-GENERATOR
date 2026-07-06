<script setup lang="ts">
import { computed } from 'vue'
import { templates } from '../data/templates'

const props = defineProps<{ slug: string }>()

const template = computed(() => templates.find((t) => t.slug === props.slug))

// Returns the complete SVG as an HTML string so v-html can inject it cleanly
const svgString = computed(() => {
  const t = template.value
  if (!t) return ''

  const accent = t.accent
  const accent2 = t.accentSecondary

  // Base SVG wrapper with gradient + browser chrome
  let content = ''

  if (t.slug === 'crm') {
    content = `
      <rect x="0" y="28" width="60" height="172" fill="rgba(255,255,255,0.03)" />
      <rect x="10" y="42" width="40" height="5" rx="2" fill="rgba(255,255,255,0.12)" />
      <rect x="10" y="56" width="32" height="5" rx="2" fill="rgba(255,255,255,0.12)" />
      <rect x="10" y="70" width="36" height="5" rx="2" fill="rgba(255,255,255,0.12)" />
      <rect x="10" y="84" width="28" height="5" rx="2" fill="rgba(255,255,255,0.12)" />
      <rect x="10" y="98" width="38" height="5" rx="2" fill="rgba(255,255,255,0.12)" />
      <rect x="68" y="36" width="100" height="60" rx="4" fill="rgba(255,255,255,0.06)" />
      <rect x="76" y="44" width="60" height="5" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="76" y="58" width="12" height="30" rx="2" fill="${accent}99" />
      <rect x="94" y="66" width="12" height="22" rx="2" fill="${accent}80" />
      <rect x="112" y="54" width="12" height="34" rx="2" fill="${accent}cc" />
      <rect x="130" y="60" width="12" height="28" rx="2" fill="${accent}99" />
      <rect x="176" y="36" width="66" height="40" rx="4" fill="${accent}1f" />
      <rect x="184" y="46" width="40" height="5" rx="2" fill="${accent}99" />
      <rect x="184" y="58" width="50" height="10" rx="2" fill="rgba(255,255,255,0.3)" />
      <rect x="176" y="84" width="66" height="40" rx="4" fill="${accent}14" />
      <rect x="184" y="94" width="40" height="5" rx="2" fill="${accent}66" />
      <rect x="184" y="106" width="50" height="10" rx="2" fill="rgba(255,255,255,0.25)" />
      <rect x="68" y="104" width="174" height="68" rx="4" fill="rgba(255,255,255,0.04)" />
      <rect x="76" y="114" width="50" height="5" rx="2" fill="rgba(255,255,255,0.25)" />
      <path d="M76 162 L96 152 L116 158 L136 145 L156 150 L176 138 L196 142 L216 130 L236 136" stroke="${accent}cc" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round" />
      <circle cx="96" cy="152" r="2.5" fill="${accent}" />
      <circle cx="156" cy="150" r="2.5" fill="${accent}" />
      <circle cx="216" cy="130" r="2.5" fill="${accent}" />
    `
  } else if (t.slug === 'sale') {
    content = `
      <rect x="20" y="38" width="140" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="52" width="100" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="62" width="110" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="78" width="70" height="22" rx="6" fill="${accent}" />
      <rect x="38" y="85" width="34" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="108" width="50" height="18" rx="5" fill="${accent}40" stroke="${accent}99" stroke-width="1" />
      <rect x="28" y="115" width="34" height="4" rx="2" fill="${accent}cc" />
      <rect x="190" y="38" width="110" height="90" rx="6" fill="rgba(255,255,255,0.07)" />
      <rect x="200" y="48" width="90" height="50" rx="4" fill="rgba(255,255,255,0.1)" />
      <rect x="200" y="104" width="50" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="200" y="114" width="30" height="5" rx="2" fill="${accent}" />
      <rect x="200" y="40" width="36" height="14" rx="4" fill="${accent}" />
      <rect x="206" y="45" width="24" height="4" rx="2" fill="rgba(255,255,255,0.9)" />
      <rect x="190" y="136" width="110" height="64" rx="6" fill="rgba(255,255,255,0.04)" />
      <rect x="200" y="146" width="90" height="34" rx="4" fill="rgba(255,255,255,0.07)" />
      <rect x="200" y="186" width="40" height="5" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="20" y="136" width="156" height="48" rx="6" fill="${accent}1a" />
      <rect x="28" y="144" width="80" height="5" rx="2" fill="${accent}99" />
      <rect x="28" y="158" width="40" height="14" rx="4" fill="${accent}cc" />
      <rect x="100" y="156" width="60" height="16" rx="4" fill="${accent}26" />
    `
  } else if (t.slug === 'bazi') {
    content = `
      <circle cx="160" cy="110" r="60" fill="none" stroke="${accent2}4d" stroke-width="1" />
      <circle cx="160" cy="110" r="48" fill="${accent}1a" />
      <circle cx="160" cy="110" r="28" fill="${accent2}4d" />
      <circle cx="160" cy="110" r="18" fill="${accent}66" />
      <rect x="20" y="38" width="60" height="6" rx="2" fill="${accent2}99" />
      <rect x="20" y="52" width="100" height="8" rx="3" fill="rgba(255,255,255,0.85)" />
      <rect x="20" y="66" width="80" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="82" width="260" height="2" fill="${accent2}66" />
      <rect x="20" y="96" width="260" height="2" fill="${accent2}66" />
      <rect x="20" y="84" width="2" height="14" fill="${accent2}66" />
      <rect x="85" y="84" width="2" height="14" fill="${accent2}66" />
      <rect x="150" y="84" width="2" height="14" fill="${accent2}66" />
      <rect x="215" y="84" width="2" height="14" fill="${accent2}66" />
      <rect x="280" y="84" width="2" height="14" fill="${accent2}66" />
      <rect x="36" y="87" width="30" height="8" rx="2" fill="${accent}80" />
      <rect x="101" y="87" width="30" height="8" rx="2" fill="${accent2}80" />
      <rect x="166" y="87" width="30" height="8" rx="2" fill="${accent}80" />
      <rect x="231" y="87" width="30" height="8" rx="2" fill="${accent2}80" />
      <rect x="20" y="166" width="120" height="24" rx="6" fill="${accent}cc" />
      <rect x="38" y="174" width="84" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="180" width="60" height="4" rx="2" fill="${accent2}66" />
      <rect x="220" y="38" width="80" height="4" rx="2" fill="rgba(255,255,255,0.25)" />
      <rect x="220" y="48" width="70" height="4" rx="2" fill="rgba(255,255,255,0.2)" />
      <rect x="220" y="58" width="75" height="4" rx="2" fill="rgba(255,255,255,0.2)" />
    `
  } else if (t.slug === 'numerology') {
    content = `
      <circle cx="60" cy="50" r="1.5" fill="${accent2}99" />
      <circle cx="280" cy="60" r="1" fill="${accent2}80" />
      <circle cx="260" cy="40" r="1.5" fill="${accent}80" />
      <circle cx="80" cy="70" r="1" fill="${accent}66" />
      <circle cx="300" cy="90" r="1.5" fill="${accent2}99" />
      <circle cx="240" cy="110" r="55" fill="none" stroke="${accent2}40" stroke-width="1" />
      <circle cx="240" cy="110" r="42" fill="none" stroke="${accent}4d" stroke-width="1" />
      <circle cx="240" cy="110" r="30" fill="${accent}26" />
      <circle cx="240" cy="110" r="18" fill="${accent2}4d" />
      <rect x="230" y="106" width="20" height="8" rx="4" fill="rgba(255,255,255,0.85)" />
      <rect x="20" y="40" width="100" height="7" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="54" width="130" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="64" width="90" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="82" width="60" height="40" rx="6" fill="${accent}26" stroke="${accent}4d" stroke-width="1" />
      <rect x="30" y="90" width="40" height="6" rx="3" fill="${accent}b3" />
      <rect x="30" y="102" width="30" height="12" rx="4" fill="rgba(255,255,255,0.85)" />
      <rect x="88" y="82" width="60" height="40" rx="6" fill="${accent2}1f" stroke="${accent2}40" stroke-width="1" />
      <rect x="98" y="90" width="40" height="6" rx="3" fill="${accent2}b3" />
      <rect x="98" y="102" width="30" height="12" rx="4" fill="rgba(255,255,255,0.85)" />
      <rect x="20" y="130" width="280" height="4" rx="2" fill="${accent}4d" />
      <rect x="20" y="138" width="200" height="4" rx="2" fill="${accent2}40" />
      <rect x="20" y="146" width="240" height="4" rx="2" fill="${accent}33" />
      <rect x="20" y="160" width="100" height="24" rx="6" fill="${accent}cc" />
      <rect x="34" y="168" width="72" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
    `
  } else if (t.slug === 'blog') {
    content = `
      <rect x="0" y="26" width="100" height="2" fill="#ffffff" opacity="0.5" />
      <rect x="20" y="38" width="280" height="80" rx="6" fill="rgba(255,255,255,0.08)" />
      <rect x="20" y="50" width="60" height="5" rx="2" fill="rgba(255,255,255,0.55)" />
      <rect x="20" y="60" width="220" height="10" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="76" width="180" height="6" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="88" width="200" height="6" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="20" y="100" width="150" height="6" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="20" y="126" width="135" height="74" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="20" y="136" width="80" height="4" rx="2" fill="rgba(255,255,255,0.45)" />
      <rect x="20" y="146" width="115" height="7" rx="2" fill="rgba(255,255,255,0.7)" />
      <rect x="20" y="158" width="100" height="5" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="20" y="168" width="90" height="5" rx="2" fill="rgba(255,255,255,0.3)" />
      <rect x="20" y="178" width="30" height="4" rx="2" fill="rgba(255,255,255,0.2)" />
      <rect x="163" y="126" width="135" height="74" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="163" y="136" width="80" height="4" rx="2" fill="rgba(255,255,255,0.45)" />
      <rect x="163" y="146" width="115" height="7" rx="2" fill="rgba(255,255,255,0.7)" />
      <rect x="163" y="158" width="100" height="5" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="163" y="168" width="90" height="5" rx="2" fill="rgba(255,255,255,0.3)" />
      <rect x="163" y="178" width="30" height="4" rx="2" fill="rgba(255,255,255,0.2)" />
    `
  } else if (t.slug === 'portfolio') {
    content = `
      <rect x="20" y="38" width="85" height="55" rx="4" fill="rgba(255,255,255,0.15)" />
      <rect x="113" y="38" width="85" height="35" rx="4" fill="rgba(255,255,255,0.1)" />
      <rect x="206" y="38" width="95" height="75" rx="4" fill="rgba(255,255,255,0.2)" />
      <rect x="20" y="100" width="85" height="40" rx="4" fill="rgba(255,255,255,0.08)" />
      <rect x="113" y="80" width="85" height="60" rx="4" fill="rgba(255,255,255,0.12)" />
      <rect x="206" y="120" width="95" height="30" rx="4" fill="rgba(255,255,255,0.07)" />
      <circle cx="54" cy="158" r="14" fill="rgba(255,255,255,0.25)" />
      <rect x="76" y="150" width="80" height="6" rx="3" fill="rgba(255,255,255,0.8)" />
      <rect x="76" y="162" width="60" height="4" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="76" y="170" width="70" height="4" rx="2" fill="rgba(255,255,255,0.3)" />
      <rect x="24" y="44" width="50" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="24" y="54" width="35" height="5" rx="2" fill="rgba(255,255,255,0.25)" />
      <rect x="117" y="44" width="50" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="117" y="54" width="35" height="5" rx="2" fill="rgba(255,255,255,0.25)" />
      <rect x="210" y="44" width="60" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="210" y="54" width="45" height="5" rx="2" fill="rgba(255,255,255,0.25)" />
    `
  } else if (t.slug === 'food-delivery') {
    content = `
      <rect x="20" y="38" width="100" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="52" width="140" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="66" width="200" height="22" rx="6" fill="rgba(255,255,255,0.1)" />
      <rect x="30" y="74" width="100" height="6" rx="3" fill="rgba(255,255,255,0.4)" />
      <rect x="20" y="96" width="50" height="18" rx="9" fill="${accent}" />
      <rect x="26" y="102" width="38" height="6" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="78" y="96" width="50" height="18" rx="9" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" stroke-width="1" />
      <rect x="136" y="96" width="50" height="18" rx="9" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.2)" stroke-width="1" />
      <rect x="20" y="122" width="130" height="78" rx="6" fill="rgba(255,255,255,0.08)" />
      <rect x="28" y="130" width="114" height="45" rx="4" fill="rgba(255,255,255,0.12)" />
      <rect x="28" y="181" width="60" height="5" rx="2" fill="rgba(255,255,255,0.6)" />
      <rect x="28" y="191" width="40" height="5" rx="2" fill="${accent}" />
      <rect x="158" y="122" width="142" height="78" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="166" y="130" width="126" height="45" rx="4" fill="rgba(255,255,255,0.09)" />
      <rect x="166" y="181" width="60" height="5" rx="2" fill="rgba(255,255,255,0.6)" />
      <rect x="166" y="191" width="40" height="5" rx="2" fill="${accent}" />
    `
  } else if (t.slug === 'edu-tutor') {
    content = `
      <rect x="20" y="40" width="120" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="54" width="160" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="70" width="90" height="56" rx="6" fill="rgba(255,255,255,0.1)" />
      <rect x="28" y="80" width="60" height="5" rx="2" fill="rgba(255,255,255,0.55)" />
      <rect x="28" y="90" width="74" height="8" rx="4" fill="rgba(255,255,255,0.25)" />
      <rect x="28" y="103" width="74" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="28" y="112" width="40" height="5" rx="2" fill="${accent}" />
      <rect x="118" y="70" width="90" height="56" rx="6" fill="rgba(255,255,255,0.08)" />
      <rect x="126" y="80" width="60" height="5" rx="2" fill="rgba(255,255,255,0.55)" />
      <rect x="126" y="90" width="74" height="8" rx="4" fill="rgba(255,255,255,0.2)" />
      <rect x="126" y="103" width="74" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="126" y="112" width="40" height="5" rx="2" fill="${accent2}" />
      <rect x="20" y="134" width="280" height="4" rx="2" fill="rgba(255,255,255,0.15)" />
      <rect x="20" y="144" width="280" height="24" rx="4" fill="rgba(255,255,255,0.06)" />
      <rect x="28" y="150" width="30" height="12" rx="6" fill="${accent}66" />
      <rect x="66" y="151" width="120" height="5" rx="2" fill="rgba(255,255,255,0.55)" />
      <rect x="66" y="159" width="80" height="4" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="260" y="151" width="32" height="10" rx="5" fill="${accent}" />
      <rect x="20" y="176" width="130" height="22" rx="6" fill="${accent}" />
      <rect x="34" y="183" width="102" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
    `
  } else if (t.slug === 'beauty-spa') {
    content = `
      <ellipse cx="270" cy="90" rx="18" ry="10" fill="rgba(255,255,255,0.15)" />
      <ellipse cx="262" cy="82" rx="12" ry="6" fill="rgba(255,255,255,0.2)" transform="rotate(-30 262 82)" />
      <ellipse cx="278" cy="82" rx="12" ry="6" fill="rgba(255,255,255,0.2)" transform="rotate(30 278 82)" />
      <ellipse cx="256" cy="76" rx="8" ry="4" fill="rgba(255,255,255,0.25)" transform="rotate(-50 256 76)" />
      <ellipse cx="284" cy="76" rx="8" ry="4" fill="rgba(255,255,255,0.25)" transform="rotate(50 284 76)" />
      <ellipse cx="270" cy="72" rx="6" ry="8" fill="rgba(255,255,255,0.3)" />
      <rect x="20" y="40" width="140" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="54" width="100" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="70" width="200" height="80" rx="8" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.15)" stroke-width="1" />
      <rect x="28" y="80" width="80" height="5" rx="2" fill="rgba(255,255,255,0.55)" />
      <rect x="28" y="90" width="160" height="7" rx="3" fill="rgba(255,255,255,0.7)" />
      <rect x="28" y="104" width="28" height="28" rx="4" fill="rgba(255,255,255,0.15)" />
      <rect x="62" y="104" width="28" height="28" rx="4" fill="rgba(255,255,255,0.25)" />
      <rect x="96" y="104" width="28" height="28" rx="4" fill="rgba(255,255,255,0.15)" />
      <rect x="130" y="104" width="28" height="28" rx="4" fill="rgba(255,255,255,0.15)" />
      <rect x="28" y="138" width="80" height="20" rx="6" fill="${accent}" />
      <rect x="38" y="145" width="60" height="6" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="158" width="88" height="42" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="116" y="158" width="88" height="42" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="212" y="158" width="88" height="42" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="28" y="168" width="60" height="5" rx="2" fill="rgba(255,255,255,0.45)" />
      <rect x="28" y="178" width="40" height="4" rx="2" fill="rgba(255,255,255,0.3)" />
      <rect x="124" y="168" width="60" height="5" rx="2" fill="rgba(255,255,255,0.45)" />
      <rect x="124" y="178" width="40" height="4" rx="2" fill="rgba(255,255,255,0.3)" />
      <rect x="220" y="168" width="60" height="5" rx="2" fill="rgba(255,255,255,0.45)" />
      <rect x="220" y="178" width="40" height="4" rx="2" fill="rgba(255,255,255,0.3)" />
    `
  } else if (t.slug === 'fitness') {
    content = `
      <rect x="20" y="38" width="100" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="52" width="140" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="20" y="68" width="130" height="72" rx="8" fill="${accent}1a" />
      <rect x="20" y="68" width="130" height="40" rx="8" fill="${accent}33" />
      <rect x="20" y="100" width="130" height="8" fill="${accent}1a" />
      <rect x="28" y="116" width="80" height="6" rx="3" fill="rgba(255,255,255,0.6)" />
      <rect x="28" y="128" width="60" height="5" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="158" y="68" width="142" height="72" rx="8" fill="${accent2}14" />
      <rect x="158" y="68" width="142" height="40" rx="8" fill="${accent2}26" />
      <rect x="158" y="100" width="142" height="8" fill="${accent2}14" />
      <rect x="166" y="116" width="80" height="6" rx="3" fill="rgba(255,255,255,0.6)" />
      <rect x="166" y="128" width="60" height="5" rx="2" fill="rgba(255,255,255,0.35)" />
      <rect x="20" y="148" width="280" height="6" rx="3" fill="rgba(255,255,255,0.08)" />
      <rect x="20" y="148" width="180" height="6" rx="3" fill="${accent}99" />
      <rect x="20" y="162" width="88" height="38" rx="6" fill="rgba(255,255,255,0.04)" />
      <rect x="28" y="170" width="50" height="8" rx="3" fill="${accent}b3" />
      <rect x="28" y="183" width="60" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="116" y="162" width="88" height="38" rx="6" fill="rgba(255,255,255,0.04)" />
      <rect x="124" y="170" width="50" height="8" rx="3" fill="${accent2}b3" />
      <rect x="124" y="183" width="60" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
      <rect x="212" y="162" width="88" height="38" rx="6" fill="rgba(255,255,255,0.04)" />
      <rect x="220" y="170" width="50" height="8" rx="3" fill="${accent}b3" />
      <rect x="220" y="183" width="60" height="5" rx="2" fill="rgba(255,255,255,0.4)" />
    `
  } else if (t.slug === 'realestate') {
    content = `
      <rect x="20" y="38" width="180" height="22" rx="6" fill="rgba(255,255,255,0.08)" />
      <rect x="30" y="46" width="100" height="6" rx="3" fill="rgba(255,255,255,0.35)" />
      <rect x="20" y="68" width="160" height="100" rx="6" fill="${accent2}14" />
      <line x1="20" y1="96" x2="180" y2="96" stroke="${accent2}26" stroke-width="0.5" />
      <line x1="20" y1="124" x2="180" y2="124" stroke="${accent2}26" stroke-width="0.5" />
      <line x1="60" y1="68" x2="60" y2="168" stroke="${accent2}26" stroke-width="0.5" />
      <line x1="100" y1="68" x2="100" y2="168" stroke="${accent2}26" stroke-width="0.5" />
      <line x1="140" y1="68" x2="140" y2="168" stroke="${accent2}26" stroke-width="0.5" />
      <circle cx="90" cy="100" r="8" fill="${accent}cc" />
      <circle cx="90" cy="100" r="4" fill="rgba(255,255,255,0.9)" />
      <path d="M90 108 L85 120 L95 120 Z" fill="${accent}cc" />
      <rect x="188" y="68" width="112" height="100" rx="6" fill="rgba(255,255,255,0.06)" />
      <rect x="196" y="76" width="96" height="50" rx="4" fill="rgba(255,255,255,0.08)" />
      <rect x="196" y="132" width="80" height="6" rx="3" fill="rgba(255,255,255,0.6)" />
      <rect x="196" y="144" width="60" height="5" rx="2" fill="${accent}" />
      <rect x="20" y="176" width="60" height="22" rx="6" fill="${accent}26" stroke="${accent}4d" />
      <rect x="88" y="176" width="70" height="22" rx="6" fill="rgba(255,255,255,0.08)" stroke="${accent}33" />
      <rect x="166" y="176" width="50" height="22" rx="6" fill="rgba(255,255,255,0.08)" stroke="${accent}33" />
    `
  } else if (t.slug === 'travel') {
    content = `
      <rect x="20" y="40" width="120" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
      <rect x="20" y="54" width="160" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="36" y="68" width="260" height="2" rx="1" fill="${accent}66" />
      <circle cx="36" cy="69" r="5" fill="${accent}cc" />
      <circle cx="36" cy="69" r="3" fill="rgba(255,255,255,0.9)" />
      <rect x="48" y="60" width="80" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="48" y="70" width="60" height="4" rx="2" fill="${accent}80" />
      <circle cx="120" cy="69" r="5" fill="${accent}99" />
      <circle cx="120" cy="69" r="3" fill="rgba(255,255,255,0.7)" />
      <rect x="132" y="60" width="80" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="132" y="70" width="60" height="4" rx="2" fill="${accent}80" />
      <circle cx="204" cy="69" r="5" fill="${accent}66" />
      <circle cx="204" cy="69" r="3" fill="rgba(255,255,255,0.5)" />
      <rect x="216" y="60" width="80" height="5" rx="2" fill="rgba(255,255,255,0.5)" />
      <rect x="216" y="70" width="60" height="4" rx="2" fill="${accent}80" />
      <rect x="20" y="86" width="130" height="80" rx="8" fill="${accent}1a" />
      <rect x="20" y="86" width="130" height="50" rx="8" fill="${accent}2e" />
      <rect x="20" y="126" width="130" height="8" fill="${accent}1a" />
      <rect x="28" y="140" width="80" height="6" rx="3" fill="rgba(255,255,255,0.6)" />
      <rect x="28" y="152" width="50" height="5" rx="2" fill="${accent}99" />
      <rect x="158" y="86" width="142" height="80" rx="8" fill="${accent2}14" />
      <rect x="158" y="86" width="142" height="50" rx="8" fill="${accent2}26" />
      <rect x="158" y="126" width="142" height="8" fill="${accent2}14" />
      <rect x="166" y="140" width="80" height="6" rx="3" fill="rgba(255,255,255,0.6)" />
      <rect x="166" y="152" width="50" height="5" rx="2" fill="${accent2}99" />
      <rect x="20" y="174" width="130" height="24" rx="6" fill="${accent}cc" />
      <rect x="38" y="182" width="94" height="8" rx="3" fill="rgba(255,255,255,0.9)" />
    `
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="bg-${t.slug}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="${accent}" stop-opacity="0.55" />
        <stop offset="30%" stop-color="${accent}" stop-opacity="0.2" />
        <stop offset="65%" stop-color="#1a1a2e" stop-opacity="1" />
        <stop offset="100%" stop-color="#0a0a0f" stop-opacity="1" />
      </linearGradient>
      <radialGradient id="glow-${t.slug}" cx="50%" cy="30%" r="70%">
        <stop offset="0%" stop-color="${accent}" stop-opacity="0.25" />
        <stop offset="100%" stop-color="transparent" />
      </radialGradient>
    </defs>
    <rect width="320" height="200" fill="url(#bg-${t.slug})" />
    <rect width="320" height="200" fill="url(#glow-${t.slug})" />
    <rect width="320" height="28" fill="rgba(0,0,0,0.2)" />
    <circle cx="12" cy="11" r="3.5" fill="#ef4444" opacity="0.7" />
    <circle cx="24" cy="11" r="3.5" fill="#eab308" opacity="0.7" />
    <circle cx="36" cy="11" r="3.5" fill="#22c55e" opacity="0.7" />
    <rect x="50" y="7" width="220" height="8" rx="4" fill="rgba(255,255,255,0.05)" />
    <rect x="54" y="9" width="140" height="4" rx="2" fill="rgba(255,255,255,0.12)" />
    ${content}
  </svg>`
})
</script>

<template>
  <div class="preview-wrap">
    <!-- SVG injected as complete HTML string so browser parses it correctly -->
    <div class="preview-inner" v-html="svgString" />

    <!-- industry badge overlay -->
    <div v-if="template" class="preview-badge" :style="`--t-accent: ${template.accent}`">
      {{ template.industry }}
    </div>
  </div>
</template>

<style scoped>
.preview-wrap {
  position: absolute;
  inset: 0;
  overflow: hidden;
  background: #09090b;
}

.preview-inner {
  width: 100%;
  height: 100%;
}

.preview-inner :deep(svg) {
  width: 100%;
  height: 100%;
  display: block;
}

.preview-badge {
  position: absolute;
  bottom: 8px;
  left: 10px;
  padding: 2px 8px;
  font-family: monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--t-accent, #10b981);
  background: rgba(0, 0, 0, 0.55);
  border: 1px solid var(--t-accent, #10b981);
  border-radius: 4px;
  backdrop-filter: blur(4px);
  opacity: 0.9;
  pointer-events: none;
}
</style>
