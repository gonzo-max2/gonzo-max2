from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os, sys
root=Path(__file__).resolve().parents[1]
docs=root/'docs'
html=(docs/'index.html').read_text().replace('<link rel="stylesheet" href="./styles.css">','').replace('<script type="module" src="./app.js"></script>','')
css=(docs/'styles.css').read_text(); js=(docs/'app.js').read_text(); profile=json.loads((docs/'data/profile.json').read_text())
receipt={'schema':'gonzo-profile-apex-ui-smoke/v1','passed':False,'checks':{},'errors':[]}
try:
  p=sync_playwright().start()
  browser=p.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_BROWSER_EXECUTABLE') or None,headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
  page=browser.new_page(viewport={'width':1440,'height':1000})
  page.on('pageerror',lambda err: receipt['errors'].append(str(err)))
  page.set_content(html)
  page.add_style_tag(content=css)
  page.evaluate('(profile)=>window.__PROFILE__=profile',profile)
  page.add_script_tag(content=js)
  page.wait_for_function("document.querySelectorAll('.atlas-tab').length===9",timeout=15000)
  page.evaluate("document.documentElement.dataset.motion='off'; state.motion=false; document.querySelectorAll('[data-reveal]').forEach(el=>el.classList.add('revealed'))")
  checks=receipt['checks']
  checks['atlas_tabs']=page.locator('.atlas-tab').count()
  checks['proof_tabs']=page.locator('.proof-tab').count()
  page.locator('.atlas-tab').nth(1).click(); checks['atlas_switch']=page.locator('#stage-title').inner_text()
  page.locator('.phase-button').nth(3).click(); checks['phase_switch']=page.locator('#phase-title').inner_text()
  page.locator('.trip-state').nth(4).click(); checks['trip_switch']=page.locator('#route-state-label').inner_text()
  page.locator('#tamper-ledger').click(); page.wait_for_timeout(150); checks['ledger_tamper']=page.locator('#ledger-state').inner_text().strip()
  page.locator('#repair-ledger').click(); page.wait_for_timeout(250); checks['ledger_repair']=page.locator('#ledger-state').inner_text().strip()
  checks['duplicate_ids']=page.evaluate("()=>{const a=[...document.querySelectorAll('[id]')].map(x=>x.id); return a.filter((x,i)=>a.indexOf(x)!==i)}")
  receipt['passed']=not receipt['errors'] and checks=={
    'atlas_tabs':9,'proof_tabs':4,'atlas_switch':'Vozime','phase_switch':'Act','trip_switch':'COMPLETE','ledger_tamper':'MUTATION DETECTED','ledger_repair':'PROOF FABRIC VALID','duplicate_ids':[]}
  receipt['expected_pass']=True
except Exception as e:
  receipt['errors'].append(repr(e))
(root/'receipts'/'ui-smoke.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt),flush=True)
os._exit(0 if receipt['passed'] else 1)
