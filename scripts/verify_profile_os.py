#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['README.md','content/profile.json','docs/index.html','docs/styles.css','docs/app.js','docs/data/profile.json','docs/site.webmanifest','docs/sw.js','PROFILE_OS_ARCHITECTURE.md','DEPLOYMENT.md','assets/generated/hero-dark.svg','assets/generated/hero-light.svg','assets/generated/systems-dark.svg','assets/generated/systems-light.svg','assets/generated/blockchain-dark.svg','assets/generated/blockchain-light.svg','assets/generated/capabilities-dark.svg','assets/generated/capabilities-light.svg']
PATS=[re.compile(r'ghp_[A-Za-z0-9]{20,}'),re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),re.compile(r'sk-[A-Za-z0-9]{20,}')]
def main():
 e=[]
 for rel in REQUIRED:
  if not (ROOT/rel).is_file():e.append(f'missing required file: {rel}')
 profile=json.loads((ROOT/'content/profile.json').read_text())
 if len(profile.get('systems',[]))<9:e.append('profile must contain at least nine systems')
 if not any(x.get('id')=='blockchain' for x in profile['systems']):e.append('blockchain system missing')
 for p in ROOT.rglob('*'):
  if not p.is_file() or '.git' in p.parts or p.suffix=='.zip':continue
  try:t=p.read_text(encoding='utf-8')
  except UnicodeDecodeError:continue
  for pat in PATS:
   if pat.search(t):e.append(f'credential-shaped secret in {p.relative_to(ROOT)}')
 for p in (ROOT/'assets').rglob('*.svg'):
  try:r=ET.parse(p).getroot()
  except ET.ParseError as ex:e.append(f'invalid SVG {p.relative_to(ROOT)}: {ex}');continue
  kids=list(r)
  if not any(x.tag.endswith('title') for x in kids) or not any(x.tag.endswith('desc') for x in kids):e.append(f'SVG lacks title/desc: {p.relative_to(ROOT)}')
 html=(ROOT/'docs/index.html').read_text();css=(ROOT/'docs/styles.css').read_text();js=(ROOT/'docs/app.js').read_text();readme=(ROOT/'README.md').read_text()
 if 'https://cdn.' in html or '<script src="http' in html:e.append('external runtime dependency')
 if 'prefers-reduced-motion' not in css:e.append('reduced motion missing')
 if 'forced-colors' not in css:e.append('forced colors missing')
 for needle in ['crypto.subtle.digest','requestAnimationFrame','visibilitychange','IntersectionObserver']:
  if needle not in js:e.append(f'advanced feature missing: {needle}')
 refs=re.findall(r'(?:src|srcset)="(\./[^"]+)"',readme)
 for ref in refs:
  if not (ROOT/ref.removeprefix('./')).is_file():e.append(f'missing README asset: {ref}')
 receipt={'schema':'gonzo-profile-verification/v1','passed':not e,'systems':len(profile['systems']),'readme_asset_references':len(refs),'errors':e,'sha256':{}}
 for rel in REQUIRED:
  p=ROOT/rel
  if p.is_file():receipt['sha256'][rel]=hashlib.sha256(p.read_bytes()).hexdigest()
 (ROOT/'receipts'/'security-and-structure.json').write_text(json.dumps(receipt,indent=2)+'\n')
 if e:
  [print('ERROR:',x,file=sys.stderr) for x in e];return 1
 print(json.dumps({'passed':True,'systems':len(profile['systems']),'assets':len(refs)}));return 0
if __name__=='__main__':raise SystemExit(main())
