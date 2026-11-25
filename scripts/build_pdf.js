// Génère documents/CV-Aness-Khenichil.pdf à partir de documents/cv.html
// Usage : node scripts/build_pdf.js   (nécessite Playwright)
const path = require('path');
const { chromium } = require('playwright');
(async () => {
    const root = path.join(__dirname, '..', 'documents');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('file://' + path.join(root, 'cv.html'), { waitUntil: 'networkidle' });
    // Vérifie que tout tient sur une page A4
    const overflow = await page.evaluate(() => {
        const bottom = document.querySelector('.page').getBoundingClientRect().bottom;
        return Math.max(...[...document.querySelectorAll('.page > * *')].map(e => e.getBoundingClientRect().bottom)) - bottom;
    });
    if (overflow > 0) { console.error(`Le CV dépasse la page de ${Math.ceil(overflow)} px : raccourcir le contenu.`); process.exitCode = 1; }
    await page.pdf({ path: path.join(root, 'CV-Aness-Khenichil.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await browser.close();
    console.log('CV généré');
})();
