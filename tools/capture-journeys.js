const { chromium } = require('playwright');
const path=require('path');
// BASE_URL captures a deployed copy instead, e.g. https://<user>.github.io/<repo>/website/
const URL=process.env.BASE_URL||'file://'+path.resolve(__dirname,'../website/index.html');
const OUT=path.resolve(__dirname,'../output/shots');require('fs').mkdirSync(OUT,{recursive:true});
(async()=>{
const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:1280,height:800},deviceScaleFactor:1.5,reducedMotion:'reduce'});
await ctx.addInitScript(()=>document.addEventListener('DOMContentLoaded',()=>{const e=document.querySelector('.proto');if(e)e.hidden=true}));
const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
const W=ms=>p.waitForTimeout(ms);
async function go(h){await p.evaluate(h=>{location.hash=h},h);await nav('#'+h);await W(400)}
async function to(sel,off=90){await p.evaluate(([s,o])=>{const e=document.querySelector(s);window.scrollTo(0,e.getBoundingClientRect().top+scrollY-o)},[sel,off]);await W(250)}
async function nav(h){await p.goto(URL+h);await p.reload();await p.evaluate(()=>document.fonts.ready);await W(300)}
async function clk(s){await p.evaluate(s=>document.querySelector(s).click(),s)}
async function shot(n,keepToast){if(!keepToast)await p.evaluate(()=>document.getElementById('toast').classList.remove('on'));const full=/^(09|19|2[5-9]|3[0-3]|39|4[0-5])-/.test(n); if(full){await p.evaluate(()=>scrollTo(0,0));await W(100)} await p.screenshot({path:`${OUT}/${n}.png`,fullPage:full});console.log('shot',n)}
async function sub(sel){await p.evaluate(s=>document.querySelector(s).dispatchEvent(new Event('submit',{cancelable:true})),sel);}

await nav('#home'); await p.evaluate(()=>document.fonts.ready); await W(600);
await shot('01-home-hero');
await clk('[data-slide="1"]'); await W(200); await shot('02-home-hero-blue'); await clk('.slide.blue [data-slide="0"]');
await to('.cats',160); await shot('03-home-categories');
await to('.finder',70); await shot('04-plan-finder');
await to('.conv',70); await shot('05-convenience');
await to('.steps-band',70); await shot('06-three-steps');
await to('.voices',70); await shot('07-testimonials');
await p.evaluate(()=>scrollTo(0,0)); await clk('#ddbtn'); await W(200); await shot('08-internet-menu');
await clk('.dd-menu a[data-go="home-packages"]'); await W(400); await shot('09-home-packages');
await to('#homeTable',120); await shot('10-home-compare');
// J1 checkout
await clk('#homePlans [data-plan="h-fam"]'); await W(400); await to('.checkout-grid',80); await shot('11-co-step1-empty');
await sub('.co-step[data-step="1"]'); await W(200); await to('.checkout-grid',80); await shot('12-co-step1-error');
await p.fill('#coArea','East Legon'); await p.dispatchEvent('#coArea','input'); await p.fill('#coAddr','GA-183-8164'); await W(200); await to('.checkout-grid',80); await shot('13-co-step1-covered');
await sub('.co-step[data-step="1"]'); await W(300);
await sub('.co-step[data-step="2"]'); await W(200); await to('.checkout-grid',80); await shot('14-co-step2-errors');
await p.fill('#coName','Ama Owusu'); await p.fill('#coPhone','024 123 4567'); await p.fill('#coEmail','ama.owusu@example.com'); await sub('.co-step[data-step="2"]'); await W(300);
await to('.checkout-grid',80); await shot('15-co-step3-payment');
await clk('#payBtn'); await W(300); await to('.checkout-grid',80); await shot('16-co-paying');
await W(1700); await to('.checkout-grid',80); await shot('17-co-confirmed',true);
await clk('.co-step[data-step="4"] [data-go="account"]'); await W(400); await shot('18-account-new');
// J2 business
await clk('#logout'); await W(300);
await nav('#business-packages'); await W(500); await shot('19-business-packages');
await to('#bizTable',120); await shot('20-business-compare');
await clk('#bizPlans [data-plan="b-con"]'); await W(400); await to('.checkout-grid',80); await shot('21-business-checkout');
// J3 finder
await nav('#home'); await W(400); await to('.finder',70);
await clk('[data-who="family"]'); await W(200); await shot('22-finder-family');
await clk('[data-who="biz"]'); await p.fill('#devices','18'); await p.dispatchEvent('#devices','input'); await W(200); await shot('23-finder-business');
await clk('#recGo'); await W(400); await to('.checkout-grid',80); await shot('24-finder-to-checkout');
// J4 coverage
await nav('#coverage'); await W(400);
await p.fill('#covArea','Adenta'); await sub('#covForm'); await W(200); await shot('25-coverage-yes');
await p.fill('#covArea','Kasoa'); await sub('#covForm'); await W(200); await clk('#notifyBtn'); await W(200); await shot('26-coverage-soon');
await p.fill('#covArea','Ho'); await sub('#covForm'); await W(200); await shot('27-coverage-no');
// J5 existing customer
await nav('#login'); await W(400); await shot('28-login');
await sub('#loginForm'); await W(500); await shot('29-account');
await clk('#payBill'); await W(1600); await clk('#speedBtn'); await W(1800); await shot('30-account-paid-speed');
// J6 support
await nav('#support'); await W(400);
await p.fill('#tkAcc','TS-104233'); await p.selectOption('#tkType','Slow speed'); await p.fill('#tkMsg','Speed drops every evening from about 7pm.'); await sub('#ticketForm'); await W(200); await shot('31-support-ticket');
await nav('#contact'); await W(400); await p.fill('#ctName','Kofi Adjei'); await p.fill('#ctPhone','0501234567'); await p.selectOption('#ctTopic','New Business connection'); await sub('#contactForm'); await W(200); await shot('32-contact');
await nav('#about'); await W(400); await shot('33-about');
// J7 Boafo
await nav('#home'); await W(400); await to('.cats',160);
await clk('.cat.boafo'); await W(350); await shot('34-boafo-redirect');
await W(1200); await p.evaluate(()=>scrollTo(0,0)); await W(200); await shot('35-boafo-home');
await to('.mosaic',62); await shot('36-boafo-photos');
await to('.how',62); await shot('37-boafo-how');
await to('.free',62); await p.fill('#frPhone','0551234567'); await sub('#freeForm'); await W(200); await shot('38-boafo-free-code');
await clk('.bnav-links [data-bgo="boafo-packages"]'); await W(400); await shot('39-boafo-packages');
await clk('[data-bpack="day"]'); await W(400); await shot('40-boafo-get-code');
await p.fill('#cdPhone','0241234567'); await sub('#codeForm'); await W(300); await shot('41-boafo-paying');
await W(1500); await shot('42-boafo-code-issued');
await clk('.bnav-links [data-bgo="boafo-coverage"]'); await W(400); await shot('43-boafo-hotspots');
await p.fill('#spotQ','kumasi'); await W(200); await shot('44-boafo-hotspot-search');
await clk('.bnav-links [data-bgo="boafo-contact"]'); await W(400); await p.fill('#bcName','Yaw Boateng'); await p.fill('#bcPhone','0201234567'); await sub('#bContact'); await W(200); await shot('45-boafo-contact');
// mobile
const mctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,reducedMotion:'reduce'});
await mctx.addInitScript(()=>document.addEventListener('DOMContentLoaded',()=>{const e=document.querySelector('.proto');if(e)e.hidden=true}));
const m=await mctx.newPage();
const ms=async n=>{await m.screenshot({path:`${OUT}/${n}.png`});console.log('shot',n)};
await m.goto(URL+'#home'); await m.evaluate(()=>document.fonts.ready); await m.waitForTimeout(500); await ms('m1-home');
await m.click('#burger'); await m.click('#ddbtn'); await m.waitForTimeout(200); await ms('m2-menu');
await m.goto(URL+'#home-packages'); await m.waitForTimeout(400); await ms('m3-packages');
await m.goto(URL+'#boafo'); await m.waitForTimeout(400); await ms('m4-boafo');
await m.goto(URL+'#boafo-packages'); await m.waitForTimeout(400); await ms('m5-boafo-packages');
console.log('errors',errs); await b.close();
})();
