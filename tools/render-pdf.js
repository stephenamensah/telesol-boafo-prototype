// Renders output/journeys.html to the landscape A4 user-journey PDF.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = path.resolve(__dirname, '../output');
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + out + '/journeys.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out + '/Telesol-Boafo-Screens-and-User-Journeys.pdf', width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log('Wrote output/Telesol-Boafo-Screens-and-User-Journeys.pdf');
})();
