#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from html import escape
import hashlib, json, shutil
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "profile.json"
ASSETS = ROOT / "assets" / "generated"
DOCS = ROOT / "docs"


def load() -> dict[str, Any]:
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    ids = [item["id"] for item in data["systems"]]
    if len(ids) != len(set(ids)):
        raise ValueError("system IDs must be unique")
    return data


def colors(dark: bool) -> dict[str, str]:
    return {
        "bg": "#070A0E" if dark else "#F5F7FA",
        "surface": "#0E151C" if dark else "#FFFFFF",
        "surface2": "#121C24" if dark else "#EDF2F5",
        "border": "#26333E" if dark else "#C9D3DC",
        "text": "#F5F7FA" if dark else "#141A22",
        "muted": "#9AA8B6" if dark else "#5D6B78",
        "accent": "#2AD7B5" if dark else "#087C6B",
        "accent2": "#75BAFF" if dark else "#1769AA",
    }


def header(w: int, h: int, title: str, desc: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'


def hero(data: dict[str, Any], dark: bool) -> str:
    c = colors(dark); ident=data["identity"]; current=data["current"]
    domains = " · ".join(data["domains"])
    return f"""{header(1200,430,ident['brand'],ident['headline'])}
<style>.pulse{{animation:pulse 2.8s ease-in-out infinite;transform-origin:center}}.drift{{animation:drift 9s ease-in-out infinite alternate}}.flow{{stroke-dasharray:12 16;animation:flow 4.8s linear infinite}}@keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}@keyframes drift{{from{{transform:translate3d(-8px,0,0)}}to{{transform:translate3d(10px,-5px,0)}}}}@keyframes flow{{to{{stroke-dashoffset:-56}}}}@media(prefers-reduced-motion:reduce){{.pulse,.drift,.flow{{animation:none}}}}</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg']}"/><stop offset=".52" stop-color="{c['surface']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient><radialGradient id="field" cx="74%" cy="44%" r="56%"><stop offset="0" stop-color="{c['accent']}" stop-opacity=".18"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></radialGradient><linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['accent']}" stop-opacity="0"/><stop offset=".2" stop-color="{c['accent']}" stop-opacity=".38"/><stop offset=".5" stop-color="{c['accent']}"/><stop offset=".8" stop-color="{c['accent2']}" stop-opacity=".38"/><stop offset="1" stop-color="{c['accent2']}" stop-opacity="0"/></linearGradient></defs>
<rect width="1200" height="430" rx="20" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="428" rx="19" fill="none" stroke="{c['border']}"/><ellipse class="drift" cx="880" cy="188" rx="270" ry="170" fill="url(#field)"/>
<g opacity=".34" stroke="{c['border']}"><path d="M0 74H1200"/><path d="M0 350H1200"/><path d="M88 0V430"/><path d="M1112 0V430"/></g>
<g transform="translate(88 59)"><rect width="44" height="44" rx="10" fill="{c['accent']}" fill-opacity=".10" stroke="{c['accent']}"/><path d="M13 26V18l9-6 9 6v8l-9 6-9-6Z" fill="none" stroke="{c['accent']}" stroke-width="2"/><path d="M22 12v20M13 18l18 8M31 18l-18 8" stroke="{c['accent']}" stroke-width="1.35" opacity=".68"/></g>
<text x="151" y="87" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" letter-spacing="3">{escape(ident['brand'])}</text><text x="1110" y="87" text-anchor="end" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="1.6">{escape(ident['location'].upper())}</text>
<text x="88" y="174" fill="{c['text']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="49" font-weight="740" letter-spacing="-1.7">Engineering systems that prove</text><text x="88" y="228" fill="{c['text']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="49" font-weight="740" letter-spacing="-1.7">what they actually did.</text>
<text x="90" y="276" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="16">{escape(domains)}</text>
<g transform="translate(88 315)" font-family="ui-monospace,SFMono-Regular,Consolas,monospace"><circle class="pulse" cx="6" cy="8" r="5" fill="{c['accent']}"/><text x="22" y="12" fill="{c['text']}" font-size="11" letter-spacing="1.1">{escape(current['status'])}</text><text x="208" y="12" fill="{c['muted']}" font-size="11">MAYA {escape(current['release'])}</text><text x="338" y="12" fill="{c['muted']}" font-size="11">{len(data['systems'])} SYSTEMS</text><text x="456" y="12" fill="{c['muted']}" font-size="11">VERIFIED PIPELINE</text></g>
<path class="flow" d="M88 370H1112" stroke="url(#line)" stroke-width="2"/><text x="88" y="403" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="12">{escape(current['mission'])}</text></svg>"""


def systems(data: dict[str, Any], dark: bool) -> str:
    c=colors(dark); cards=[]
    for i,item in enumerate(data["systems"]):
        row,col=divmod(i,3); x=56+col*370; y=122+row*154; accent=item["accent"]; stack=" · ".join(item["stack"][:4])
        cards.append(f"""<g transform="translate({x} {y})"><rect width="346" height="132" rx="12" fill="{c['surface']}" stroke="{c['border']}"/><rect width="4" height="132" rx="2" fill="{accent}"/><text x="22" y="27" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9.5" letter-spacing="1.3">{i+1:02d} · {escape(item['domain'].upper())}</text><text x="22" y="58" fill="{c['text']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="17" font-weight="700">{escape(item['short'])}</text><text x="22" y="84" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="11.2">{escape(stack)}</text><circle cx="316" cy="26" r="5" fill="{accent}"><animate attributeName="opacity" values=".35;1;.35" dur="{3.2+(i%4)*.7:.1f}s" repeatCount="indefinite"/></circle><path d="M22 105H322" stroke="{accent}" stroke-opacity=".28"/><text x="22" y="121" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8.8">{escape(item['status'].upper())}</text></g>""")
    return f"""{header(1200,610,'GONZO systems portfolio','Nine systems across autonomous engineering, mobility, blockchain, realtime interaction, audio, RF sensing, forensics, and quality automation.')}<style>@media(prefers-reduced-motion:reduce){{animate{{display:none}}}}</style><rect width="1200" height="610" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="608" rx="17" fill="none" stroke="{c['border']}"/><text x="56" y="52" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="2">SYSTEMS PORTFOLIO</text><text x="56" y="88" fill="{c['text']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="27" font-weight="720">One engineering standard across nine product domains.</text>{''.join(cards)}<text x="56" y="585" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="11">Private active development, internal tooling, and explicitly labelled research tracks.</text></svg>"""


def blockchain(data: dict[str, Any], dark: bool) -> str:
    c=colors(dark); labels=[('01','INTENT','8F2A…91D0'),('02','POLICY','14C9…AA73'),('03','ACTION','6E01…B47F'),('04','PROOF','C8D4…109E'),('05','RECEIPT','A1F7…DD22')]; nodes=[]; connectors=[]
    for i,(num,label,digest) in enumerate(labels):
        x=58+i*220
        nodes.append(f"""<g transform="translate({x} 156)"><rect width="182" height="112" rx="12" fill="{c['surface']}" stroke="{c['border']}"/><text x="18" y="27" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9.5" letter-spacing="1.4">BLOCK {num}</text><text x="18" y="58" fill="{c['text']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="16" font-weight="700">{label}</text><text x="18" y="84" fill="{c['accent']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">{digest}</text><circle cx="158" cy="26" r="5" fill="{c['accent']}"><animate attributeName="r" values="4;6;4" dur="{2.4+i*.35:.2f}s" repeatCount="indefinite"/></circle></g>""")
        if i<4:
            connectors.append(f'<path d="M{240+i*220} 212H{278+i*220}" stroke="{c["accent"]}" stroke-width="2" stroke-dasharray="6 7"><animate attributeName="stroke-dashoffset" from="0" to="-26" dur="1.5s" repeatCount="indefinite"/></path>')
    return f"""{header(1200,360,'Blockchain proof chain','A conceptual chain linking intent, policy, action, proof, and receipt through cryptographic digests.')}<style>@media(prefers-reduced-motion:reduce){{animate{{display:none}}}}</style><rect width="1200" height="360" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="358" rx="17" fill="none" stroke="{c['border']}"/><text x="56" y="54" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="2">BLOCKCHAIN SYSTEMS LAB</text><text x="56" y="92" fill="{c['text']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="27" font-weight="720">Cryptographic receipts for inspectable automation.</text><text x="56" y="119" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="13">Research direction · smart-contract safety · event-sourced ledgers · zero-knowledge architecture</text>{''.join(connectors)}{''.join(nodes)}<circle cx="58" cy="324" r="5" fill="{c['accent']}"/><text x="74" y="329" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="11">Interactive SHA-256 chain verification is available in the GitHub Pages experience.</text></svg>"""


def capabilities(data: dict[str, Any], dark: bool) -> str:
    c=colors(dark); xs=[650,790,930,1070]; headers=['RESEARCH','PROTOTYPE','INTEGRATED','VERIFIED']; rows=[]
    for i,item in enumerate(data['capabilities']):
        y=128+i*47; cells=[]
        for key,x in zip(['research','prototype','integrated','verified'],xs):
            on=item[key]; cells.append(f'<circle cx="{x}" cy="{y-5}" r="7" fill="{c["accent"] if on else c["surface2"]}" stroke="{c["accent"] if on else c["border"]}"/>')
        rows.append(f'<text x="56" y="{y}" fill="{c["text"]}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="13">{escape(item["name"])}</text>'+''.join(cells))
    h=''.join(f'<text x="{x}" y="82" text-anchor="middle" fill="{c["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9.5" letter-spacing="1">{label}</text>' for x,label in zip(xs,headers))
    return f"""{header(1200,540,'Engineering capability maturity','Capability matrix showing research, prototype, integrated, and verified maturity.')}<rect width="1200" height="540" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="538" rx="17" fill="none" stroke="{c['border']}"/><text x="56" y="50" fill="{c['muted']}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" letter-spacing="2">CAPABILITY MATURITY</text>{h}<path d="M56 96H1144" stroke="{c['border']}"/>{''.join(rows)}<text x="56" y="511" fill="{c['muted']}" font-family="Inter,ui-sans-serif,system-ui,sans-serif" font-size="11">Maturity is disclosed explicitly; research tracks are not represented as production systems.</text></svg>"""


def readme(data: dict[str, Any]) -> str:
    rows=[]
    for i in range(0,len(data['systems']),2):
        cells=[]
        for item in data['systems'][i:i+2]:
            stacks=' '.join(f'`{x}`' for x in item['stack'])
            cells.append(f'<td width="50%" valign="top">\n\n### {item["name"]}\n\n{item["summary"]}\n\n{stacks}\n\n**Status:** {item["status"]}\n\n</td>')
        if len(cells)==1: cells.append('<td width="50%"></td>')
        rows.append('<tr>\n'+'\n'.join(cells)+'\n</tr>')
    principles='\n'.join(f'- {x}' for x in data['identity']['principles'])
    return f"""<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/generated/hero-light.svg">
  <img alt="{data['identity']['brand']} — {data['identity']['headline']}" src="./assets/generated/hero-dark.svg" width="100%">
</picture>

<p align="center"><strong>Autonomous AI · Mobility · Blockchain · Native DSP · RF research · Realtime product architecture</strong></p>
<p align="center"><a href="#maya-codex-nexus">MAYA</a> · <a href="#systems-portfolio">Systems</a> · <a href="#blockchain-systems-lab">Blockchain</a> · <a href="#engineering-activity">Activity</a> · <a href="https://gonzo-max2.github.io/gonzo-max2/">Interactive Profile OS</a></p>
<img src="./assets/continuum-divider.svg" alt="" width="100%">

## Operating profile

I design systems where **reasoning, execution, verification, and evidence remain one continuous object**.

{data['identity']['bio']}

<table><tr><td width="50%" valign="top">

### Current mission

**{data['current']['flagship']} {data['current']['release']}**

{data['current']['mission']}.

</td><td width="50%" valign="top">

### Delivery standard

{principles}

</td></tr></table>

## MAYA Codex Nexus

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/maya-system-dark.svg"><source media="(prefers-color-scheme: light)" srcset="./assets/maya-system-light.svg"><img alt="MAYA Codex Nexus proof-native execution architecture" src="./assets/maya-system-dark.svg" width="100%"></picture>

**MAYA Codex Nexus** is a local-first autonomous engineering workstation built around:

> Instruction → Observe → Frame → Decide → Act → Verify → Learn → Receipt

Its core invariant is simple: **a completion claim is not complete until its evidence is inspectable**.

## Systems portfolio

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/generated/systems-dark.svg"><source media="(prefers-color-scheme: light)" srcset="./assets/generated/systems-light.svg"><img alt="Nine-system engineering portfolio" src="./assets/generated/systems-dark.svg" width="100%"></picture>

<table>{''.join(rows)}</table>

## Blockchain Systems Lab

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/generated/blockchain-dark.svg"><source media="(prefers-color-scheme: light)" srcset="./assets/generated/blockchain-light.svg"><img alt="Blockchain proof-chain architecture" src="./assets/generated/blockchain-dark.svg" width="100%"></picture>

The blockchain track is explicitly a **research direction**, focused on cryptographic execution receipts, event-sourced ledger integrity, smart-contract safety, verifiable autonomous actions, zero-knowledge proof architecture, and honest on-chain/off-chain boundaries.

The interactive Pages experience includes a local SHA-256 proof-chain demonstrator that detects tampering without a wallet, extension, or external blockchain service.

## Capability maturity

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/generated/capabilities-dark.svg"><source media="(prefers-color-scheme: light)" srcset="./assets/generated/capabilities-light.svg"><img alt="Engineering capability maturity matrix" src="./assets/generated/capabilities-dark.svg" width="100%"></picture>

## Engineering activity

The panel below is generated from GitHub's API by this repository's own workflow.

<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/activity-dark.svg"><source media="(prefers-color-scheme: light)" srcset="./assets/activity-light.svg"><img alt="Verified GitHub engineering activity" src="./assets/activity-dark.svg" width="100%"></picture>

## Collaboration model

- Autonomous developer tooling
- Secure local AI infrastructure
- Mobility and dispatch platforms
- Blockchain verification and cryptographic receipt systems
- Native desktop and audio software
- RF telemetry and scientific interfaces
- Recovery, evidence, and verification tooling
- High-performance, accessibility-complete interaction systems

<p align="center"><strong>Build locally. Verify everything. Ship with evidence.</strong></p>
"""


def main() -> int:
    data=load(); ASSETS.mkdir(parents=True,exist_ok=True)
    for name,fn in [('hero',hero),('systems',systems),('blockchain',blockchain),('capabilities',capabilities)]:
        (ASSETS/f'{name}-dark.svg').write_text(fn(data,True),encoding='utf-8')
        (ASSETS/f'{name}-light.svg').write_text(fn(data,False),encoding='utf-8')
    (ROOT/'README.md').write_text(readme(data),encoding='utf-8')
    (DOCS/'assets').mkdir(parents=True,exist_ok=True); (DOCS/'data').mkdir(parents=True,exist_ok=True)
    for p in (ROOT/'assets').glob('*.svg'): shutil.copy2(p,DOCS/'assets'/p.name)
    for p in ASSETS.glob('*.svg'): shutil.copy2(p,DOCS/'assets'/p.name)
    (DOCS/'data'/'profile.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf-8')
    files={}
    for p in sorted(x for x in ROOT.rglob('*') if x.is_file() and 'receipts' not in x.parts and '.git' not in x.parts):
        files[p.relative_to(ROOT).as_posix()]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
    (ROOT/'receipts'/'profile-build.json').write_text(json.dumps({'schema':'gonzo-profile-build/v1','systems':len(data['systems']),'case_studies':len(data['caseStudies']),'generated_assets':len(list(ASSETS.glob('*.svg'))),'files':files},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'systems':len(data['systems']),'generated_assets':len(list(ASSETS.glob('*.svg')))}))
    return 0

if __name__=='__main__': raise SystemExit(main())
