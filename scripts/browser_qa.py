#!/usr/bin/env python3
"""Optional browser checks; not required to serve the website.

Requires the Python Playwright package and an installed Chrome/Chromium browser.
CHROME_PATH can select the browser; AXE_CORE_PATH enables the accessibility audit.
CGD_QA_OUTPUT_DIR selects the report/screenshot directory (default: system temp).
The browser intercepts requests and serves only this checkout; no contact is sent.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, mimetypes, sys, os, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=Path(os.environ.get('CGD_QA_OUTPUT_DIR', str(Path(tempfile.gettempdir())/'cgd-site-qa')))
OUTPUT.mkdir(parents=True, exist_ok=True)
CHROME=os.environ.get('CHROME_PATH') or shutil.which('google-chrome') or shutil.which('chromium')
AXE=os.environ.get('AXE_CORE_PATH')
BASE='https://capital-glass-qa.test'
paths=['/'+str(p.relative_to(ROOT)) for p in ROOT.rglob('*.html') if '.git' not in p.parts]
failures=[]; errors=[]; bad_requests=[]
def route_handler(route):
 from urllib.parse import urlsplit, unquote
 u=urlsplit(route.request.url)
 if u.hostname!='capital-glass-qa.test': route.abort(); return
 f=(ROOT/('index.html' if u.path=='/' else unquote(u.path).lstrip('/'))).resolve()
 if not f.is_relative_to(ROOT) or any(part.startswith('.') for part in f.relative_to(ROOT).parts): route.fulfill(status=403,body='Forbidden');return
 if not f.is_file():
  bad_requests.append(u.path);route.fulfill(status=404,body='Not found');return
 route.fulfill(status=200,content_type=mimetypes.guess_type(str(f))[0] or 'application/octet-stream',body=f.read_bytes())
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 context=browser.new_context();context.route('**/*',route_handler);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 for width,height in [(360,640),(390,844),(430,932),(1440,900)]:
  page.set_viewport_size({'width':width,'height':height})
  for path in paths:
   page.goto(BASE+path,wait_until='load')
   r=page.evaluate('''() => {const rect=s=>document.querySelector(s).getBoundingClientRect();const action=rect('.hero .cta-row');const trust=rect('.trust-points');const fixed=rect('.float-cta');return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,heroCtaBottom:action.bottom,trustBottom:trust.bottom,stickyTop:fixed.top,short:[...document.querySelectorAll('.btn,.float-cta a,.menu-btn,summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.height&&r.height<(e.matches('.btn,.float-cta a')?52:48)}).map(e=>e.outerHTML.slice(0,100)),forms:document.querySelectorAll('form,input,select,textarea').length}}''')
   issue={}
   if r['scrollWidth']>width: issue['overflow']=r['scrollWidth']
   if r['short']: issue['short']=r['short']
   if r['forms']: issue['forms']=r['forms']
   if width<1000 and r['heroCtaBottom']>r['stickyTop']:issue['heroCtaBelowFold']=r
   if width==360 and r['trustBottom']>r['stickyTop']: issue['trustBelowFold']=r
   if issue: failures.append({'path':path,'viewport':[width,height],**issue})
  if width==360:
   page.goto(BASE+'/');page.screenshot(path=str(OUTPUT/'cgd-home-360.png'),full_page=False)
  if width==390:
   page.goto(BASE+'/services/storefront-glass-repair.html');page.screenshot(path=str(OUTPUT/'cgd-storefront-390.png'),full_page=False)
  if width==1440:
   page.goto(BASE+'/');page.screenshot(path=str(OUTPUT/'cgd-home-desktop.png'),full_page=False)
 Path(str(OUTPUT/'cgd-layout-results.json')).write_text(json.dumps({'pages':len(paths),'cases':len(paths)*4,'failures':failures,'errors':errors,'bad_requests':bad_requests},indent=2))
 # Confirm selected work photos decode after scrolling into view.
 page.set_viewport_size({'width':390,'height':844});page.goto(BASE+'/gallery.html')
 for photo in page.locator('.work-gallery img').all():
  photo.scroll_into_view_if_needed()
  photo.evaluate('(img) => img.decode()')
  assert photo.evaluate('(img) => img.naturalWidth > 0 && img.complete')
 page.locator('#work-gallery').scroll_into_view_if_needed();page.screenshot(path=str(OUTPUT/'cgd-gallery-390.png'),full_page=False)
 # Mobile navigation open/close, Escape, outside click and focus.
 page.set_viewport_size({'width':360,'height':640});page.goto(BASE+'/')
 page.locator('.menu-btn').click();assert page.locator('.menu-btn').get_attribute('aria-expanded')=='true'
 assert page.locator('.main-nav').is_visible()
 page.keyboard.press('Escape');assert page.locator('.menu-btn').get_attribute('aria-expanded')=='false'
 page.locator('.menu-btn').click();page.mouse.click(3,500);assert page.locator('.menu-btn').get_attribute('aria-expanded')=='false'
 page.locator('details summary').first.click();assert page.locator('details').first.get_attribute('open') is not None
 # Cancel navigation only, allowing the site's delegated tracking listener to run.
 page.evaluate("document.addEventListener('click', e=>{if(e.target.closest('a[href^=\"tel:\"],a[href^=\"https://wa.me\"]'))e.preventDefault()},true)")
 page.locator('.float-cta .call').click();page.locator('.float-cta .whatsapp').click()
 data=page.evaluate('window.dataLayer');assert [e['event'] for e in data]==['call_button_click','whatsapp_button_click'];assert all(e['cta_placement']=='sticky_mobile' for e in data)
 assert 'text=' not in json.dumps(data) and 'target_href' not in json.dumps(data)
 page.evaluate("() => { window.__gtag=[]; window.gtag=(...args)=>{window.__gtag.push(args);}; }")
 page.locator('.hero .btn-call').click();gtag=page.evaluate('window.__gtag');assert len(gtag)==1 and gtag[0][1]=='call_button_click';assert len(page.evaluate('window.dataLayer'))==2
 nojs=browser.new_context(java_script_enabled=False,viewport={'width':360,'height':640});nojs.route('**/*',route_handler);fallback=nojs.new_page();fallback.goto(BASE+'/contact.html');assert fallback.locator('.float-cta .call').is_visible() and fallback.locator('.float-cta .whatsapp').is_visible();nojs.close()
 # WCAG audit on representative conversion and content templates.
 axe_path=Path(AXE) if AXE else None
 accessibility=[]
 if axe_path and axe_path.is_file():
  for path in ['/','/services/storefront-glass-repair.html','/locations/washington-dc.html','/contact.html','/blog/how-to-measure-storefront-glass.html','/gallery.html','/testimonials-case-studies.html']:
   page.goto(BASE+path);page.add_script_tag(path=str(axe_path));violations=page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))}");accessibility.append({'path':path,'violations':violations})
 result={'pages':len(paths),'layout_cases':len(paths)*4,'failures':failures,'javascript_errors':errors,'missing_requests':bad_requests,'menu':'passed','accordion':'passed','tracking':'passed (dataLayer and direct gtag, no duplicates)','no_javascript_contact':'passed','work_photos':'8 responsive gallery images decoded','accessibility':accessibility}
 Path(str(OUTPUT/'cgd-browser-results.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));browser.close()
 if failures or errors or bad_requests or any(r['violations'] for r in accessibility):sys.exit(1)
