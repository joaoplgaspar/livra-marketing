// Renderiza cada <section class="slide"> de um carrossel.html em PNG 1080x1350.
// Uso (rodar a partir de E:\Projetos\lura para resolver @playwright/test):
//   node E:/Projetos/livra-marketing/teste-skills-2026-10/caminho-3/_trabalho/render.cjs a-releitura [b-... c-...]
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require(require.resolve('@playwright/test', { paths: [process.cwd()] }));

const ROOT = path.resolve(__dirname, '..');

(async () => {
  const pautas = process.argv.slice(2);
  const exe = process.env.PW_CHROME || 'C:/Users/synzp/AppData/Local/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-win64/chrome-headless-shell.exe';
  const browser = await chromium.launch({ executablePath: exe });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  for (const pauta of pautas) {
    const dir = path.join(ROOT, pauta);
    await page.goto(pathToFileURL(path.join(dir, 'carrossel.html')).href, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))));
    const fonts = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style));
    const slides = page.locator('section.slide');
    const n = await slides.count();
    // checa texto que vaza da caixa do slide ou da margem lateral de 80px
    const issues = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('section.slide').forEach((s, i) => {
        const r = s.getBoundingClientRect();
        s.querySelectorAll('[data-t], p, h1, h2, h3, span, li, div').forEach(el => {
          if (!el.childNodes.length || ![...el.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) return;
          const range = document.createRange(); range.selectNodeContents(el);
          for (const b of range.getClientRects()) {
            if (b.width < 1) continue;
            if (b.left - r.left < 80 || r.right - b.right < 80 || b.top < r.top || b.bottom > r.bottom)
              out.push(`slide ${i + 1}: "${el.textContent.trim().slice(0, 40)}" L${Math.round(b.left - r.left)} R${Math.round(r.right - b.right)} T${Math.round(b.top - r.top)} B${Math.round(r.bottom - b.bottom)}`);
          }
          const fs = parseFloat(getComputedStyle(el).fontSize);
          if (fs < 32) out.push(`slide ${i + 1}: fonte ${fs}px em "${el.textContent.trim().slice(0, 30)}"`);
        });
      });
      return [...new Set(out)];
    });
    for (let i = 0; i < n; i++) {
      const file = path.join(dir, String(i + 1).padStart(2, '0') + '.png');
      await slides.nth(i).screenshot({ path: file });
    }
    console.log(`${pauta}: ${n} slides | fontes: ${[...new Set(fonts)].join(', ')}`);
    if (issues.length) console.log('  avisos:\n   ' + issues.join('\n   '));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
