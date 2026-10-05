// One full-length PDF page per website screen (for importing into Canva).
const { chromium } = require('playwright');
const path=require('path');
// BASE_URL captures a deployed copy instead, e.g. https://<user>.github.io/<repo>/website/
const URL=process.env.BASE_URL||'file://'+path.resolve(__dirname,'../website/index.html');
const OUT=path.resolve(__dirname,'../output/pages');require('fs').mkdirSync(OUT,{recursive:true});
const routes=[['home','Telesôl — Homepage'],['home-packages','Home packages'],['business-packages','Business packages'],['coverage','Check coverage'],['support','Support'],['about','About us'],['contact','Contact us'],['login','Login'],['boafo','Boafo — Homepage'],['boafo-packages','Boafo — Packages'],['boafo-code','Boafo — Get a Code'],['boafo-coverage','Boafo — Hotspots'],['boafo-contact','Boafo — Contact']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:800}});
await p.emulateMedia({media:'screen',reducedMotion:'reduce'});
let i=0;
for(const [r] of routes){await p.goto(URL+'#'+r);await p.reload();await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.addStyleTag({content:'.nav,.bnav{position:relative!important}.proto{display:none!important}'});
 const h=await p.evaluate(()=>document.documentElement.scrollHeight);
 await p.pdf({path:`${OUT}/sp-${String(++i).padStart(2,'0')}.pdf`,width:'1280px',height:h+'px',printBackground:true,pageRanges:'1'});
 console.log(r,h);}
console.log('Merge with: python3 tools/merge-pages.py');
await b.close()})();
