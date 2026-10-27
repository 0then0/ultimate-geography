/* Browser-only QA. Uses an existing Playwright/Chromium installation. */
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

async function main() {
  const root = path.resolve(__dirname, '..');
  const qa = path.join(root, 'build', 'qa');
  const entries = JSON.parse(fs.readFileSync(path.join(qa, 'cards.json')));
  const browser = await chromium.launch({
    headless: true,
    executablePath: process.env.UG_CHROMIUM_PATH,
  });
  const results = { browser: await browser.version(), widths: [360, 393, 412, 1920], checks: [] };
  try {
    const page = await browser.newPage({
      viewport: { width: 393, height: 900 },
      deviceScaleFactor: 1,
    });
    for (const language of [...new Set(entries.map((entry) => entry.language))]) {
      const cards = entries.filter((x) => x.language === language);
      // One shared stylesheet, all Anki-rendered questions/answers. This checks
      // real content including the longest names, not synthetic placeholders.
      const docs = cards.map((x) => fs.readFileSync(x.path, 'utf8'));
      const hintsByPath = new Map(
        cards.map((entry, i) => [entry.path, docs[i].includes('<div class="ug-pronunciation">')]),
      );
      const styles = docs[0].match(/<style[^>]*>[\s\S]*?<\/style>/g).join('\n');
      const contents = docs
        .map(
          (doc, i) =>
            `<section data-index="${i}">${doc.match(/<body[^>]*>([\s\S]*)<\/body>/)[1].replace(/<style[^>]*>[\s\S]*?<\/style>/g, '')}</section>`,
        )
        .join('\n');
      const harness = path.join(qa, `all-${language}.html`);
      fs.writeFileSync(
        harness,
        `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="${pathToFileURL(path.join(qa, 'media')).href}/">${styles}</head><body class="card">${contents}</body></html>`,
      );
      for (const width of results.widths) {
        for (const dark of [false, true]) {
          await page.setViewportSize({ width, height: 1000 });
          await page.goto(pathToFileURL(harness).href);
          await page
            .locator('body')
            .evaluate((body, dark) => body.classList.toggle('nightMode', dark), dark);
          await page.evaluate(() => Promise.all([...document.images].map((img) => img.decode())));
          const measured = await page.evaluate(() => {
            const viewport = document.documentElement.clientWidth;
            const bad = [...document.querySelectorAll('.ug-card, .ug-card *')]
              .filter((el) => {
                if (getComputedStyle(el).display === 'none') return false;
                const r = el.getBoundingClientRect();
                return r.right > viewport + 1 || r.left < -1 || el.scrollWidth > el.clientWidth + 1;
              })
              .map((el) => ({
                tag: el.tagName,
                class: el.className,
                index: el.closest('section')?.dataset.index,
              }));
            const brokenImages = [...document.images].filter(
              (i) => !i.complete || !i.naturalWidth,
            ).length;
            const distortedImages = [...document.images].filter((i) => {
              const s = getComputedStyle(i);
              if (s.display === 'none') return false;
              const r = i.getBoundingClientRect();
              const w = r.width - parseFloat(s.borderLeftWidth) - parseFloat(s.borderRightWidth);
              const h = r.height - parseFloat(s.borderTopWidth) - parseFloat(s.borderBottomWidth);
              // Some upstream maps are 500x421, not 16:9. With a height
              // limit, object-fit: contain preserves their painted ratio
              // inside a differently proportioned element box.
              return (
                Math.abs(w / h - i.naturalWidth / i.naturalHeight) > 0.02 &&
                s.objectFit !== 'contain'
              );
            }).length;
            const invisibleNotes = [...document.querySelectorAll('.ug-note')].filter(
              (e) => getComputedStyle(e).display === 'none',
            ).length;
            const grids = [...document.querySelectorAll('.ug-media-grid')];
            // A bounded image inside a 1fr column used to leave a large empty
            // panel to its right on desktop, despite passing overflow checks.
            const oversizedMapPanels = [...document.querySelectorAll('.ug-map-block')].filter(
              (el) => el.getBoundingClientRect().width > 797,
            ).length;
            const emptyMapPanels = [...document.querySelectorAll('.ug-map-block')].filter((el) => {
              if (viewport !== 1920) return false;
              const img = el.querySelector('.ug-map img');
              const style = getComputedStyle(el);
              const contentWidth =
                el.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
              return img && contentWidth - img.getBoundingClientRect().width > 2;
            }).length;
            const stacked = grids.every(
              (e) => getComputedStyle(e).gridTemplateColumns.split(' ').length === 1,
            );
            return {
              viewport,
              scrollWidth: document.documentElement.scrollWidth,
              bad: bad.slice(0, 12),
              brokenImages,
              distortedImages,
              invisibleNotes,
              oversizedMapPanels,
              emptyMapPanels,
              stacked,
            };
          });
          if (
            measured.bad.length ||
            measured.brokenImages ||
            measured.distortedImages ||
            measured.invisibleNotes ||
            measured.oversizedMapPanels ||
            measured.emptyMapPanels ||
            (width < 900 && !measured.stacked)
          )
            throw new Error(JSON.stringify({ language, width, dark, measured }));
          results.checks.push({
            language,
            width,
            theme: dark ? 'dark' : 'light',
            rendered_sides: cards.length,
            ...measured,
          });
          const dir = path.join(
            qa,
            'screenshots',
            `${language}-${width}-${dark ? 'dark' : 'light'}`,
          );
          fs.mkdirSync(dir, { recursive: true });
          for (let type = 0; type < 4; type++) {
            for (const side of ['question', 'answer']) {
              const entry = cards
                .filter((x) => x.type === type && x.side === side)
                .sort((a, b) => {
                  return (
                    Number(hintsByPath.get(b.path)) - Number(hintsByPath.get(a.path)) ||
                    b.country.length - a.country.length
                  );
                })[0];
              await page.goto(pathToFileURL(entry.path).href);
              await page
                .locator('body')
                .evaluate((body, dark) => body.classList.toggle('nightMode', dark), dark);
              await page.evaluate(() =>
                Promise.all([...document.images].map((img) => img.decode())),
              );
              await page.screenshot({
                path: path.join(dir, `${type}-${side}.png`),
                fullPage: true,
              });
            }
          }
          // All-content checks use Anki's nightMode spelling. Verify AnkiDroid's
          // class spelling and a narrow container in a wide WebView separately.
          await page.locator('body').evaluate((body) => {
            body.className = 'card night_mode mobile';
            body.style.width = '360px';
          });
          const overflow = await page.evaluate(
            () => document.body.scrollWidth > document.body.clientWidth,
          );
          if (overflow) throw new Error(`Embedded mobile container overflow: ${language}/${width}`);
        }
      }
    }
    fs.writeFileSync(
      path.join(qa, 'layout-verification.json'),
      `${JSON.stringify(results, null, 2)}\n`,
    );
    console.log(
      JSON.stringify({
        browser: results.browser,
        scenarios: results.checks.length,
        card_sides_per_scenario: entries.length / new Set(entries.map((e) => e.language)).size,
        screenshots: results.checks.length * 8,
      }),
    );
  } finally {
    await browser.close();
  }
}
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
