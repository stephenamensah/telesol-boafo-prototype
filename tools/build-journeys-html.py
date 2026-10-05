"""Builds output/journeys.html from the screenshots in output/shots.
Run tools/capture-journeys.js first, then this script, then tools/render-pdf.js."""
import os, html, glob
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'output')
JPG = os.path.join(OUT, 'jpg')
os.makedirs(JPG, exist_ok=True)
# Compress screenshots so the PDF stays small
for f in glob.glob(os.path.join(OUT, 'shots', '*.png')):
    im = Image.open(f).convert('RGB')
    if im.width > 1500:
        im = im.resize((1500, int(im.height * 1500 / im.width)), Image.LANCZOS)
    im.save(os.path.join(JPG, os.path.basename(f)[:-4] + '.jpg'), quality=82, optimize=True)
FONTCSS = ''  # fonts come from Google Fonts (see <link> in the output HTML)

def img(n): return f"file://{JPG}/{n}.jpg"
E = html.escape

JOURNEYS = [
 dict(code="J1", title="New Home customer orders a package", seg="Telesôl · Home", color="#e3529c",
  persona="Ama, a parent in East Legon whose family streams, studies and works from home.",
  goal="Find the right Home package, confirm her street is covered, pay and book installation.",
  entry="Homepage → Internet menu → Home", outcome="Order TS-###### confirmed, installation slot booked, account created.",
  steps=[
   ("01-home-hero","Land on the homepage","The hero repeats the brand promise: competitive plans, dependable speed and support. The CTA goes straight to Home packages."),
   ("08-internet-menu","Open the Internet menu","The Internet menu lists Home, Business and Boafo. Boafo is marked as a separate site."),
   ("09-home-packages","Compare Home packages","Five packages: Essentials GHS 120, Family GHS 160, Max GHS 275, Family Max GHS 480 and Smart Home GHS 1,255 a month. Family is flagged Most Popular."),
   ("10-home-compare","Check the comparison table","One table sets speed, best use, devices and monthly price side by side."),
   ("11-co-step1-empty","Select Family, then start checkout","Step 1 of 4 asks for the installation area. The order summary stays visible on the right."),
   ("12-co-step1-error","Validation: area missing","Submitting without an area shows a plain-language error under the field."),
   ("13-co-step1-covered","Area confirmed as covered","Typing a covered area (East Legon) shows a green coverage result before she continues."),
   ("14-co-step2-errors","Step 2: details, with validation","Name, a Ghana phone number and email are required. Each missing field gets its own error."),
   ("15-co-step3-payment","Step 3: choose payment","MTN MoMo, Telecel Cash, AT Money or card. The MoMo number is pre-filled from step 2."),
   ("16-co-paying","Approve the payment prompt","The button changes to 'Approve the prompt on your phone…' while payment is pending (simulated)."),
   ("17-co-confirmed","Order confirmed","Confirmation shows the package, installation date and slot, the phone the details went to, and an order reference."),
   ("18-account-new","Land in her new account","The account shows the active plan, unlimited data, renewal date and that this month is paid."),
 ]),
 dict(code="J2", title="New Business customer orders a package", seg="Telesôl · Business", color="#2878c0",
  persona="Kofi, who runs a 15-person office and cannot afford downtime.",
  goal="Choose a business-grade package with the right support level and order it.",
  entry="Homepage hero (blue slide) or Internet → Business", outcome="Same four-step checkout as J1, with the Business package in the summary.",
  steps=[
   ("02-home-hero-blue","Blue hero slide","The second hero slide uses the Business palette and links to Business packages."),
   ("19-business-packages","Compare Business packages","Five packages: Business Essential GHS 365, Connect GHS 680, Signature GHS 1,275, Infinity GHS 2,325, and Dedicated on a custom quote via Talk to sales."),
   ("20-business-compare","Check staff sizing","The table maps each package to staff numbers and typical use."),
   ("21-business-checkout","Checkout with Business Connect","The shared checkout carries the Business package and price. The remaining steps match J1."),
 ]),
 dict(code="J3", title="Undecided visitor uses the plan finder", seg="Telesôl · Home & Business", color="#332750",
  persona="A visitor who doesn't know how many Mbps they need.",
  goal="Get a recommendation from who they are and how many devices they connect.",
  entry="Homepage → 'Still not decided? We can help you choose.'", outcome="A recommended package, one click from checkout.",
  steps=[
   ("04-plan-finder","Pick a profile","Chips for Just Me, Family, I work & Create and My Business, plus a devices slider."),
   ("22-finder-family","Family profile","Choosing Family recommends the Family package with its price and reason."),
   ("23-finder-business","My Business, 18 devices","Switching to My Business and 18 devices recommends Business Connect."),
   ("24-finder-to-checkout","Check This Plan","The button opens checkout with the recommended package already selected."),
 ]),
 dict(code="J4", title="Visitor checks coverage", seg="Telesôl · Coverage", color="#eeab25",
  persona="Someone who wants to know if Telesôl reaches their street before choosing a package.",
  goal="Get a clear yes, coming soon or not yet, and a next step for each answer.",
  entry="Homepage 'Three simple steps' → Check coverage, or the nav", outcome="Covered: go to packages. Coming soon: join the waitlist. Not covered: go to Boafo hotspots.",
  steps=[
   ("06-three-steps","Three simple steps","The homepage explains check location, choose lifestyle, we connect you. Each step links to its page."),
   ("25-coverage-yes","Covered (Adenta)","Green result with direct links to Home and Business packages."),
   ("26-coverage-soon","Coming soon (Kasoa)","Amber result. 'Notify me' adds the visitor to the waitlist and confirms it."),
   ("27-coverage-no","Not covered (Ho)","Red result that points the visitor to Boafo community Wi-Fi instead."),
 ]),
 dict(code="J5", title="Existing customer manages their account", seg="Telesôl · Account", color="#332750",
  persona="Kwame, an existing Essentials customer.",
  goal="Log in, check his plan and pay this month's bill.",
  entry="Login button in the nav", outcome="Bill paid by MoMo, renewal date moved forward, speed test run.",
  steps=[
   ("28-login","Log in","Phone or account number and password. The prototype pre-fills a sample login."),
   ("29-account","Account overview","Active plan, speed, renewal date, days used this cycle, and the next bill with a pay button."),
   ("30-account-paid-speed","Pay bill and run a speed test","The bill shows as paid with an SMS receipt. The speed test reports download speed and ping."),
 ]),
 dict(code="J6", title="Support, contact and about", seg="Telesôl · Help", color="#2c306a",
  persona="A customer with a slow connection, or a prospect with a question.",
  goal="Self-serve from the FAQ, raise a ticket, or request a call back.",
  entry="Support, Contact Us or About Us in the nav", outcome="Ticket number issued, or call-back request confirmed.",
  steps=[
   ("31-support-ticket","FAQ and raise a ticket","FAQs cover installation, unlimited data, billing, plan changes and Boafo. A ticket returns a TK- reference."),
   ("32-contact","Request a call back","Topic list includes Home, Business, Boafo for my community and partnership/franchise."),
   ("33-about","About Telesôl","Positioning: existing infrastructure, unlimited fair pricing, and reach from homes to campuses."),
 ]),
 dict(code="J7", title="Visitor goes to Boafo and buys a Wi-Fi code", seg="Boafo", color="#3d7d55",
  persona="A trader at Makola Market who needs data for a few hours.",
  goal="Move from Telesôl to Boafo, pick a pack, pay with MoMo and get a code.",
  entry="Boafo tile, Internet menu, package switcher or footer", outcome="An 8-character Wi-Fi code on screen (and by SMS, simulated).",
  steps=[
   ("03-home-categories","Click Boafo","Every Boafo link on Telesôl is marked as opening the Boafo site."),
   ("34-boafo-redirect","Redirect screen","A short 'Taking you to Boafo' screen makes the switch to the Boafo site clear."),
   ("35-boafo-home","Boafo homepage","'Welcome to Boafo ~ a community based wifi', with Get Started going to packages."),
   ("36-boafo-photos","Where Boafo lives","Photo mosaic of market, station and campus hotspots."),
   ("37-boafo-how","Online in four steps","Find a hotspot, pick a pack, pay with MoMo, enter your code."),
   ("39-boafo-packages","Choose a pack","30 mins, 1 hour, 24 hours or 7 days. Prices are sample figures."),
   ("40-boafo-get-code","Get a Code","The chosen pack is pre-selected. She enters her MoMo number and network."),
   ("41-boafo-paying","Approve on phone","The pay button shows the pending MoMo approval (simulated)."),
   ("42-boafo-code-issued","Code issued","The code is shown large, with a Copy button and instructions for the Boafo Wi-Fi login page."),
 ]),
 dict(code="J8", title="New Boafo user claims a free 10-minute pack", seg="Boafo", color="#e3529c",
  persona="Someone trying Boafo for the first time.",
  goal="Try the network free before paying.",
  entry="Boafo homepage → 'Get a free 10mins pack'", outcome="Free code issued once per number. A second claim is sent to paid packs.",
  steps=[
   ("38-boafo-free-code","Enter phone, get free code","A valid Ghana number returns a free 10-minute code. Claiming again shows a link to packages instead."),
 ]),
 dict(code="J9", title="Find a hotspot or contact Boafo", seg="Boafo", color="#3d7d55",
  persona="A user looking for the nearest hotspot, or a community leader who wants one.",
  goal="Search hotspots by place, or ask for Boafo in their community.",
  entry="Coverage or Contact Us in the Boafo nav", outcome="A list of live and coming-soon hotspots, or a confirmed request.",
  steps=[
   ("43-boafo-hotspots","Hotspot list","Each hotspot shows its town and whether it is Live or Coming soon."),
   ("44-boafo-hotspot-search","Search 'kumasi'","Results filter as you type. No match offers a 'Request' button."),
   ("45-boafo-contact","Contact Boafo","Options: bring Boafo to my community, help with a code, become a Boafo agent."),
 ]),
]

def flow(steps, color):
    return f'<div class="flow{" cols" if len(steps)>7 else ""}">' + ''.join(
        f'<span class="fstep"><b style="background:{color}">{i+1}</b>{E(s[1])}</span>' for i,s in enumerate(steps)) + '</div>'

pages = []
# cover
pages.append(f'''<section class="page cover" style="background-image:url({img('01-home-hero')})">
<div class="coverin"><div class="kicker">Website prototype · Screens &amp; user journeys</div>
<h1>Telesôl &amp; Boafo</h1>
<p class="sub">Interactive prototype built from the Telesôl brand concept: Home, Business and Boafo internet packages, end to end.</p>
<div class="meta"><span>Stephen Asante Mensah<br><small>Head of Product and Innovation</small></span><span>30 September 2026<br><small>Version 1 · prototype</small></span></div></div></section>''')

# overview
rows = ''.join(f'<tr><td><span class="code" style="background:{j["color"]}">{j["code"]}</span></td><td><b>{E(j["title"])}</b><br><small>{E(j["seg"])}</small></td><td>{E(j["entry"])}</td><td>{len(j["steps"])}</td><td>{E(j["outcome"])}</td></tr>' for j in JOURNEYS)
pages.append(f'''<section class="page">
<div class="ph"><span class="eyebrow">Overview</span><h2>What the prototype covers</h2></div>
<div class="two">
<div>
<p class="lead">Two linked websites. <b>Telesôl</b> sells Home and Business packages and serves existing customers. <b>Boafo</b> is the separate community Wi-Fi site: every Boafo link on Telesôl goes there through a short redirect screen.</p>
<div class="sitemap">
 <div class="site tel"><h4>Telesôl</h4>
  <div class="node">Homepage<small>Hero · package tiles · plan finder · app · 3 steps · testimonials</small></div>
  <div class="grid"><div class="node pink">Home packages<small>Essentials · Family · Max · Family Max · Smart Home</small></div><div class="node blue">Business packages<small>Essential · Connect · Signature · Infinity · Dedicated</small></div></div>
  <div class="node">Checkout<small>Location → Details → Payment → Done</small></div>
  <div class="grid"><div class="node">Check coverage</div><div class="node">Login → My account</div><div class="node">Support</div><div class="node">About · Contact</div></div>
 </div>
 <div class="arrow">Boafo link<br>→<br><small>redirect screen</small></div>
 <div class="site boa"><h4>Boafo</h4>
  <div class="node">Homepage<small>Welcome · photos · 4 steps · free 10 mins</small></div>
  <div class="node">Packages<small>30 mins · 1 hr · 24 hrs · 7 days</small></div>
  <div class="node">Get a Code<small>MoMo payment → code</small></div>
  <div class="node">Coverage (hotspots)</div><div class="node">Contact Us</div>
 </div>
</div>
</div>
<div>
<div class="callout soft"><b>What production needs</b>
<ul>
<li>Coverage lookup against real homes passed and POPs.</li>
<li>MoMo and card payment gateway, plus SMS for receipts and codes.</li>
<li>Customer accounts, billing and renewals from 24online.</li>
<li>Boafo voucher generation linked to the hotspot captive portal.</li>
</ul></div>
</div></div></section>''')

HOME_P=[("Essentials","GHS 120"),("Family","GHS 160"),("Max","GHS 275"),("Family Max","GHS 480"),("Smart Home","GHS 1,255")]
BIZ_P=[("Business Essential","GHS 365"),("Business Connect","GHS 680"),("Business Signature","GHS 1,275"),("Business Infinity","GHS 2,325"),("Business Dedicated","Custom")]
def ptable(rows,color):
    return '<table class="ptab"><thead><tr><th>Package</th><th>Monthly price</th></tr></thead><tbody>'+''.join(f'<tr><td><span class="pdot" style="background:{color}"></span>{E(n)}</td><td>{E(p)}</td></tr>' for n,p in rows)+'</tbody></table>'
pages.append(f'''<section class="page"><div class="ph"><span class="eyebrow">Packages</span><h2>Package line-up and monthly prices</h2></div>
<div class="two" style="grid-template-columns:1fr 1fr"><div><h4 class="ptitle" style="color:#e3529c">Home</h4>{ptable(HOME_P,'#e3529c')}</div>
<div><h4 class="ptitle" style="color:#2878c0">Business</h4>{ptable(BIZ_P,'#2878c0')}</div></div>
<p class="foot-note">Business Dedicated is priced per customer; the prototype routes it to Talk to sales instead of checkout.</p></section>''')
pages.append(f'''<section class="page">
<div class="ph"><span class="eyebrow">Journey index</span><h2>Nine user journeys, 45 screens</h2></div>
<table class="idx"><thead><tr><th></th><th>Journey</th><th>Entry point</th><th>Screens</th><th>Outcome</th></tr></thead><tbody>{rows}</tbody></table>
<p class="foot-note">Screens were captured from the working prototype at 1280px desktop width. Mobile views are on the last pages.</p>
</section>''')

for j in JOURNEYS:
    pages.append(f'''<section class="page jintro">
<div class="band" style="background:{j['color']}"><span class="jcode">{j['code']}</span><span class="jseg">{E(j['seg'])}</span></div>
<div class="ph"><h2>{E(j['title'])}</h2></div>
<div class="facts">
 <div><span class="lab">Who</span>{E(j['persona'])}</div>
 <div><span class="lab">Goal</span>{E(j['goal'])}</div>
 <div><span class="lab">Entry point</span>{E(j['entry'])}</div>
 <div><span class="lab">Outcome</span>{E(j['outcome'])}</div>
</div>
<div class="jbody"><div><span class="lab" style="margin-top:7mm;display:block">Journey steps</span>
{flow(j['steps'], j['color'])}</div>
<figure class="endst"><span class="lab" style="margin-top:7mm;display:block">End state</span><div class="shot"><img src="{img(j['steps'][-1][0])}"></div></figure></div>
</section>''')
    st = j['steps']
    for k in range(0, len(st), 2):
        cells = ''
        for i, s in enumerate(st[k:k+2]):
            n = k+i+1
            cells += f'''<figure><div class="shot"><img src="{img(s[0])}"></div>
<figcaption><span class="num" style="background:{j['color']}">{j['code']}.{n}</span><div><b>{E(s[1])}</b><p>{E(s[2])}</p></div></figcaption></figure>'''
        pages.append(f'<section class="page shots"><div class="runner"><span style="color:{j["color"]}">{j["code"]}</span> {E(j["title"])}</div><div class="pair">{cells}</div></section>')

# homepage tour appendix? mobile
mob = [("m1-home","Homepage"),("m2-menu","Menu with Internet options"),("m3-packages","Home packages"),("m4-boafo","Boafo homepage"),("m5-boafo-packages","Boafo packages")]
pages.append('<section class="page"><div class="ph"><span class="eyebrow">Responsive</span><h2>Mobile views (390px)</h2></div><div class="phones">' +
  ''.join(f'<figure><img src="{img(m)}"><figcaption>{E(c)}</figcaption></figure>' for m,c in mob) + '</div></section>')
pages.append(f'''<section class="page"><div class="ph"><span class="eyebrow">Homepage sections</span><h2>Brand concept carried into the build</h2></div>
<div class="pair"><figure><div class="shot"><img src="{img('05-convenience')}"></div><figcaption><div><b>Convenience</b><p>App section with App Store and Google Play buttons (placeholders until the app ships).</p></div></figcaption></figure>
<figure><div class="shot"><img src="{img('07-testimonials')}"></div><figcaption><div><b>Testimonials</b><p>'Great plans. Reliable speed. Support that listens.' Sample quotes from the concept.</p></div></figcaption></figure></div></section>''')

CSS = FONTCSS + '''
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Work Sans",sans-serif;color:#1d1330;font-size:10.5pt;line-height:1.45;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:14mm 16mm;page-break-after:always;position:relative;overflow:hidden;background:#fff}
h1,h2,h4{font-family:Unbounded,sans-serif;margin:0}
.eyebrow{font-family:"Barlow Condensed";font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#e3529c;font-size:10pt}
.ph{margin-bottom:7mm}.ph h2{font-size:20pt;color:#332750;margin-top:2mm;font-weight:700}
.cover{background-size:cover;background-position:center;padding:0;display:flex;align-items:flex-end}
.coverin{background:#fff;width:100%;padding:12mm 16mm 12mm}
.kicker{font-family:"Barlow Condensed";font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#e3529c}
.cover h1{font-size:40pt;color:#332750;margin-top:2mm}
.cover .sub{font-size:13pt;color:#2a1f44;max-width:190mm;margin:3mm 0 6mm}
.meta{display:flex;gap:24mm;font-weight:600;color:#332750}.meta small{font-weight:400;color:#6b5d78}
.two{display:grid;grid-template-columns:1.35fr 1fr;gap:10mm}
.lead{font-size:11.5pt;margin:0 0 5mm}
.sitemap{display:grid;grid-template-columns:1.25fr 22mm 1fr;gap:3mm;align-items:center}
.site{border-radius:4mm;padding:4mm;display:grid;gap:2.2mm}
.site.tel{background:#f6eef3}.site.boa{background:#e4f1e8}
.site h4{font-size:11pt;color:#332750}.site.boa h4{color:#2c5e3f}
.node{background:#fff;border-radius:2.5mm;padding:2.2mm 3mm;font-weight:600;font-size:9pt}
.node small{display:block;font-weight:400;color:#6b5d78;font-size:7.8pt}
.node.pink{border-left:2mm solid #e3529c}.node.blue{border-left:2mm solid #2878c0}
.site .grid{display:grid;grid-template-columns:1fr 1fr;gap:2.2mm}
.arrow{text-align:center;font-family:Unbounded;font-size:8pt;color:#3d7d55;line-height:1.3}.arrow small{font-family:"Work Sans";color:#6b5d78}
.callout{background:#fff4e0;border-radius:4mm;padding:5mm 6mm;margin-bottom:5mm}
.callout.soft{background:#f5f3f8}
.callout ul{margin:2mm 0 0;padding-left:5mm}.callout li{margin-bottom:1.5mm}
.idx{width:100%;border-collapse:collapse;font-size:9.5pt}
.idx th{text-align:left;font-family:Unbounded;font-size:8pt;color:#6b5d78;font-weight:600;padding:2mm;border-bottom:1.5px solid #332750}
.idx td{padding:2.6mm 2mm;border-bottom:1px solid #e6dfee;vertical-align:top}
.idx small{color:#6b5d78}
.code{display:inline-block;color:#fff;font-family:Unbounded;font-weight:700;font-size:8.5pt;padding:1mm 2.4mm;border-radius:99px}
.ptab{width:100%;border-collapse:collapse;font-size:12pt;margin-top:4mm}.ptab th{text-align:left;font-family:Unbounded;font-size:8.5pt;color:#6b5d78;padding:3mm;border-bottom:1.5px solid #332750}.ptab td{padding:4mm 3mm;border-bottom:1px solid #e6dfee;font-variant-numeric:tabular-nums}.ptab td:last-child{font-family:Unbounded;font-weight:600;text-align:right}.ptab th:last-child{text-align:right}.pdot{display:inline-block;width:3mm;height:3mm;border-radius:50%;margin-right:3mm}.ptitle{font-size:14pt}
.foot-note{color:#6b5d78;font-size:9pt;margin-top:4mm}
.jintro .band{position:absolute;left:0;top:0;right:0;height:22mm;display:flex;align-items:center;gap:6mm;padding:0 16mm;color:#fff}
.jcode{font-family:Unbounded;font-weight:800;font-size:22pt}.jseg{font-family:"Barlow Condensed";font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:12pt}
.jintro .ph{margin-top:22mm}.jintro .ph h2{font-size:24pt}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:5mm 10mm;font-size:11.5pt}
.lab{display:block;font-family:"Barlow Condensed";font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#6b5d78;font-size:9.5pt;margin-bottom:1mm}
.flow{display:flex;flex-direction:column;gap:2mm;align-items:flex-start}
.flow.cols{display:grid;grid-template-columns:1fr 1fr;gap:2mm 3mm;align-items:start}.flow.cols .fstep{font-size:8.6pt}
.shots{display:flex;flex-direction:column}.shots .pair{margin-block:auto}
.jbody{display:grid;grid-template-columns:1fr 1.15fr;gap:10mm}
.endst .shot img{max-height:92mm}
.fstep{display:flex;align-items:center;gap:2mm;background:#f5f3f8;border-radius:99px;padding:1.2mm 4mm 1.2mm 1.2mm;font-size:9.5pt;font-weight:500}
.fstep b{color:#fff;width:6.5mm;height:6.5mm;border-radius:50%;display:grid;place-items:center;font-size:8pt;font-family:Unbounded}
.runner{font-family:Unbounded;font-size:9pt;font-weight:600;color:#6b5d78;margin-bottom:5mm}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
figure{margin:0}
.shot{background:#f5f3f8;border-radius:3mm;overflow:hidden;border:1px solid #e6dfee}
.shot img{width:100%;max-height:128mm;object-fit:contain;object-position:top;display:block}
.pair{align-items:start}
.shots .pair{margin-block:auto}
figcaption{display:flex;gap:3mm;margin-top:4mm;align-items:flex-start}
figcaption b{font-family:Unbounded;font-size:10pt;color:#1d1330;font-weight:600}
figcaption p{margin:1mm 0 0;color:#4d4060;font-size:9.5pt}
.num{color:#fff;font-family:Unbounded;font-weight:700;font-size:8pt;padding:1.2mm 2.4mm;border-radius:99px;white-space:nowrap}
.phones{display:grid;grid-template-columns:repeat(5,1fr);gap:6mm}
.phones img{width:100%;border-radius:4mm;border:1px solid #e6dfee;display:block}
.phones figcaption{font-size:9pt;font-weight:600;justify-content:center}
'''
open(os.path.join(OUT,'journeys.html'),'w').write(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;600;700;800&family=Barlow+Condensed:ital,wght@0,600;0,700;1,600;1,700&family=Work+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap"><title>Telesôl & Boafo – Screens and User Journeys</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
print(len(pages),'pages')
