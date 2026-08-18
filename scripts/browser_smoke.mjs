import { chromium } from 'playwright';

const base = process.env.SITE_URL || 'http://127.0.0.1:8080';
const widths = [320, 375, 390, 430, 768, 1024, 1280, 1440, 1920];
const routes = ['/', '/katalog/', '/projects/', '/contacts/', '/franchises/', '/reviews/', '/batutnyj-centr-pod-klyuch/'];
const browser = await chromium.launch({headless: true});
const failures = [];

for (const width of widths) {
  for (const route of routes) {
    const page = await browser.newPage({ viewport: { width, height: width <= 430 ? 844 : 900 } });
    const pageErrors = [];
    page.on('pageerror', error => pageErrors.push(String(error)));
    try {
      const response = await page.goto(base + route, { waitUntil: 'domcontentloaded', timeout: 15000 });
      if (!response || response.status() >= 400) throw new Error(`HTTP ${response?.status()}`);
      await page.waitForSelector('h1', { state: 'visible', timeout: 5000 });
      const overflow = await page.evaluate(() => ({
        doc: document.documentElement.scrollWidth,
        body: document.body.scrollWidth,
        viewport: window.innerWidth,
      }));
      if (Math.max(overflow.doc, overflow.body) > overflow.viewport + 2) {
        throw new Error(`horizontal overflow ${Math.max(overflow.doc, overflow.body)}px > ${overflow.viewport}px`);
      }
      if (pageErrors.length) throw new Error(`page errors: ${pageErrors.join(' | ')}`);

      if (width <= 768) {
        const menu = page.locator('.menu-btn');
        if (await menu.count()) {
          await menu.click();
          const mobile = page.locator('.mobile-menu.is-open');
          await mobile.waitFor({ state: 'visible', timeout: 3000 });
          const box = await mobile.boundingBox();
          if (box && (box.x < -1 || box.x + box.width > width + 1)) throw new Error('mobile menu outside viewport');
          await menu.click();
        }
      } else {
        const mega = page.locator('.mega-trigger');
        if (await mega.count()) {
          await mega.click();
          await page.locator('.mega.is-open').waitFor({ state: 'visible', timeout: 3000 });
        }
      }
    } catch (error) {
      failures.push(`${width}px ${route}: ${error.message}`);
    } finally {
      await page.close();
    }
  }
}

await browser.close();
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`Browser smoke passed: ${widths.length} viewports × ${routes.length} routes = ${widths.length * routes.length} page checks`);
