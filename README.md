# Telesôl & Boafo prototype

This repository holds the clickable prototypes and the tooling that produces the user-journey screenshots and PDFs:

- **The website prototype:** Telesôl plus the linked Boafo community Wi-Fi site.
- **The Telesôl mobile app prototype.**
- **The tooling:** scripts that generate the screenshots and the user-journey PDF from the website prototype.

None of it has a build step or a framework. Each prototype is one HTML file with its CSS and JavaScript inline.

```
telesol-prototype/
├── website/
│   ├── index.html          Telesôl + Boafo website (all pages, routing, flows)
│   └── assets/             Hero artwork and Boafo photos from the brand concept
├── mobile-app/
│   └── index.html          Telesôl customer app (phone-frame prototype)
├── tools/
│   ├── capture-journeys.js     Clicks through every journey and saves 50 screenshots
│   ├── build-journeys-html.py  Lays the screenshots out as the journey document (HTML)
│   ├── render-pdf.js           Prints that HTML to the landscape A4 journey PDF
│   ├── capture-pages-pdf.js    One full-length PDF page per website screen (for Canva)
│   └── merge-pages.py          Merges those pages into one PDF
├── output/                 Generated files (git-ignored)
└── package.json
```

## Run the prototypes

Open `website/index.html` or `mobile-app/index.html` in a browser. To serve them locally instead, run:

```bash
npm run serve        # then open http://localhost:3000/website/
```

Fonts come from Google Fonts: Unbounded, Barlow Condensed and Work Sans. Without an internet connection the browser falls back to system fonts.

## Regenerate the screenshots and PDFs

You need Node 18 or later and Python 3 with `pillow` and `pypdf`.

```bash
npm install                      # installs Playwright
npx playwright install chromium  # first time only
pip install pillow pypdf

npm run journeys   # → output/Telesol-Boafo-Screens-and-User-Journeys.pdf (39 pages)
npm run pages      # → output/Telesol-Boafo-Prototype-Screens.pdf (13 full-length pages)
```

`npm run journeys` runs three steps: it captures the screenshots, builds the journey HTML, and renders the PDF. Run the journeys again after any change to the website, so the screenshots match it.

## Website: where to change things

All of the following are in `website/index.html`.

| What | Where |
|---|---|
| Packages and prices | `const PLANS = { home: [...], biz: [...] }`. Each package has `id`, `name`, `speed`, `price` and `feat`. Set `price: null` to show "Custom" with a Talk to sales button, as Business Dedicated does. |
| Boafo packs | `const BOAFO = [...]` |
| Covered areas (coverage check) | `const AREAS = {...}`. The values are `'ok'` (connected) or `'soon'` (coming soon). |
| Boafo hotspots | `const SPOTS = [...]` |
| Plan finder rules | `function recommend()` |
| Brand colours | The CSS tokens on `:root`: `--plum`, `--gold`, `--pink`, `--blue`, `--green` and others |
| Indigo palette for inner pages | `#telesol.ink {...}`. It applies to every page except Home and the two package pages. |
| Fonts | The `--f-display`, `--f-cond` and `--f-body` tokens, plus the Google Fonts `<link>` |

### Routes

The site works on one page and switches screens with the address bar (`#route`):

- **Telesôl:** `home`, `home-packages`, `business-packages`, `coverage`, `checkout`, `support`, `about`, `contact`, `login`, `account`
- **Boafo:** `boafo`, `boafo-packages`, `boafo-code`, `boafo-coverage`, `boafo-contact`

Every Boafo link on the Telesôl site goes through the "Taking you to Boafo" redirect screen first.

### What is simulated

None of these connect to a real system yet. In production each one needs a back-end service:

- **Payments:** Mobile Money (MTN, Telecel, AT) and card.
- **SMS:** receipts and Boafo codes.
- **Coverage lookup:** in production, against the real homes passed and POPs.
- **Login and account data:** in production, from 24online.
- **Boafo code generation:** in production, linked to the hotspot captive portal.

## Mobile app: where to change things

All of the following are in `mobile-app/index.html`.

- `PLANS` and `BOAFO` hold the packages and packs.
- `V = { splash, signin, otp, home, plans, upgrade, pay, paid, speed, coverage, support, outage, boafo, profile }` holds one function per screen.
- The chips under the phone let you jump to any screen.

The app uses the same packages and prices as the website, apart from Business Dedicated, which is quoted by sales. If you change prices, update `PLANS` in both files.

## User journeys covered by the PDF

| # | Journey | Screens |
|---|---|---|
| J1 | New Home customer orders a package | 12 |
| J2 | New Business customer orders a package | 4 |
| J3 | Undecided visitor uses the plan finder | 4 |
| J4 | Visitor checks coverage | 4 |
| J5 | Existing customer manages their account | 3 |
| J6 | Support, contact and about | 3 |
| J7 | Visitor goes to Boafo and buys a Wi-Fi code | 9 |
| J8 | New Boafo user claims a free 10-minute pack | 1 |
| J9 | Find a hotspot or contact Boafo | 3 |

The journey steps, captions and personas are in the `JOURNEYS` list in `tools/build-journeys-html.py`. Each step names the screenshot it uses, and `tools/capture-journeys.js` creates each screenshot under the same name.

## Notes

- Package speeds and the device and staff limits are indicative placeholders. The prices are the confirmed line-up.
- Contact numbers and emails on the Contact and Support pages are placeholders.
