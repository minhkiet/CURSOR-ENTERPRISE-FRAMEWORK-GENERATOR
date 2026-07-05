// One-shot screenshot capture for the 6 template previews.
// Each template is served from the local static server at:
//   http://localhost:8732/templates/{slug}/
// We render at 1440x900 desktop, wait for fonts+animations, then
// capture the top 540px region (which is the hero) and resize to
// 360x225 (the card preview aspect ratio).

import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const BASE = 'http://localhost:8732/templates';
const OUT  = path.resolve('public/templates/_previews');

const SLUGS = [
  'bazi',
  'numerology',
  'crm',
  'sale',
  'blog',
  'portfolio',
];

async function shoot(page, slug) {
  await page.goto(`${BASE}/${slug}/`, { waitUntil: 'networkidle', timeout: 20000 });
  // Allow web fonts and hero animations to settle
  await page.waitForTimeout(1200);
  // Capture the hero region — top 540px tall, full desktop width
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(200);

  const filename = `${slug}.png`;
  await page.screenshot({
    path: path.join(OUT, filename),
    clip: { x: 0, y: 0, width: 1440, height: 900 },
    type: 'png',
  });
  console.log(`  ok  ${slug}.png`);
}

async function main() {
  await mkdir(OUT, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2, // crisp on hi-dpi
  });
  const page = await ctx.newPage();
  for (const slug of SLUGS) {
    console.log(`-> ${slug}`);
    try {
      await shoot(page, slug);
    } catch (err) {
      console.log(`  FAIL ${slug}: ${err.message}`);
    }
  }
  await browser.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});