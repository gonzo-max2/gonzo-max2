#!/usr/bin/env python3
from __future__ import annotations

from html import escape
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / 'content' / 'profile.json').read_text(encoding='utf-8'))
OUT = ROOT / 'assets' / 'apex'
OUT.mkdir(parents=True, exist_ok=True)


def palette(dark: bool) -> dict[str, str]:
    return {
        'bg': '#05080b' if dark else '#edf1f3',
        'surface': '#0b1116' if dark else '#ffffff',
        'surface2': '#101920' if dark else '#e4ebef',
        'line': '#26333e' if dark else '#c7d1d7',
        'text': '#f5f7f8' if dark else '#11181d',
        'soft': '#b9c4cb' if dark else '#45545f',
        'muted': '#7f8d99' if dark else '#687782',
        'faint': '#52606b' if dark else '#94a0a8',
        'teal': '#2ad7b5' if dark else '#087c6b',
        'blue': '#75baff' if dark else '#1769aa',
        'violet': '#b79cff' if dark else '#6c4fc6',
        'green': '#54d99a' if dark else '#16784d',
        'amber': '#f1b85b' if dark else '#845600',
        'danger': '#ff6d78' if dark else '#b4232d',
    }


def header(w: int, h: int, title: str, desc: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title>'
        f'<desc id="desc">{escape(desc)}</desc>'
    )


def hero(dark: bool) -> str:
    c = palette(dark)
    return f'''{header(1200, 520, 'GONZO systems profile', 'Engineering systems that remain truthful under pressure.')}
<style>
  .spin{{animation:spin 28s linear infinite;transform-origin:892px 260px}}
  .spin2{{animation:spin 18s linear infinite reverse;transform-origin:892px 260px}}
  .pulse{{animation:pulse 2.8s ease-in-out infinite}}
  .flow{{stroke-dasharray:12 16;animation:flow 4s linear infinite}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  @keyframes flow{{to{{stroke-dashoffset:-56}}}}
  @media(prefers-reduced-motion:reduce){{.spin,.spin2,.pulse,.flow{{animation:none}}}}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c['bg']}"/><stop offset=".55" stop-color="{c['surface']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
  <radialGradient id="field" cx="75%" cy="48%" r="54%"><stop stop-color="{c['teal']}" stop-opacity=".16"/><stop offset="1" stop-color="{c['teal']}" stop-opacity="0"/></radialGradient>
  <linearGradient id="titleGradient" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{c['text']}"/><stop offset=".6" stop-color="{c['teal']}"/><stop offset="1" stop-color="{c['blue']}"/></linearGradient>
</defs>
<rect width="1200" height="520" rx="20" fill="url(#bg)"/>
<rect x="1" y="1" width="1198" height="518" rx="19" fill="none" stroke="{c['line']}"/>
<rect width="1200" height="520" rx="20" fill="url(#field)"/>
<g stroke="{c['line']}" opacity=".42"><path d="M0 74H1200M0 446H1200"/><path d="M80 0V520M1120 0V520"/></g>
<g transform="translate(80 48)"><rect width="44" height="44" rx="11" fill="{c['teal']}" fill-opacity=".09" stroke="{c['teal']}"/><path d="M13 26V18l9-6 9 6v8l-9 6-9-6Z" fill="none" stroke="{c['teal']}" stroke-width="2"/><path d="M22 12v20M13 18l18 8M31 18l-18 8" stroke="{c['teal']}" stroke-width="1.4" opacity=".7"/></g>
<text x="145" y="76" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="13" letter-spacing="3">GONZO // SYSTEMS</text>
<text x="80" y="180" fill="{c['soft']}" font-family="Inter,system-ui,sans-serif" font-size="48" font-weight="700" letter-spacing="-1.5">I build systems</text>
<text x="80" y="240" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="58" font-weight="760" letter-spacing="-2">that remain truthful</text>
<text x="80" y="308" fill="url(#titleGradient)" font-family="Inter,system-ui,sans-serif" font-size="58" font-weight="760" letter-spacing="-2">under pressure.</text>
<text x="82" y="357" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="16">Autonomous AI · Mobility · Blockchain · Native DSP · RF sensing · Proof architecture</text>
<g transform="translate(82 397)" font-family="ui-monospace,Consolas,monospace" font-size="10"><circle class="pulse" cx="6" cy="7" r="5" fill="{c['teal']}"/><text x="22" y="11" fill="{c['text']}">ACTIVE DEVELOPMENT</text><text x="190" y="11" fill="{c['muted']}">MAYA 6.6.1</text><text x="300" y="11" fill="{c['muted']}">09 SYSTEMS</text><text x="404" y="11" fill="{c['muted']}">PROFILE OS / APEX</text></g>
<g>
  <circle cx="892" cy="260" r="184" fill="none" stroke="{c['teal']}" stroke-opacity=".28"/>
  <circle class="spin" cx="892" cy="260" r="138" fill="none" stroke="{c['teal']}" stroke-opacity=".28" stroke-dasharray="4 9"/>
  <circle class="spin2" cx="892" cy="260" r="92" fill="none" stroke="{c['blue']}" stroke-opacity=".32" stroke-dasharray="2 8"/>
  <rect x="837" y="205" width="110" height="110" rx="27" fill="{c['surface']}" stroke="{c['teal']}"/>
  <text x="892" y="278" text-anchor="middle" fill="{c['teal']}" font-family="Inter,system-ui,sans-serif" font-size="50" font-weight="780">G</text>
  <g fill="{c['surface']}" stroke="{c['line']}"><rect x="695" y="130" width="84" height="34" rx="17"/><rect x="996" y="153" width="94" height="34" rx="17"/><rect x="1024" y="342" width="86" height="34" rx="17"/><rect x="724" y="370" width="80" height="34" rx="17"/><rect x="664" y="258" width="68" height="34" rx="17"/></g>
  <g fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9" text-anchor="middle"><text x="737" y="151">MAYA</text><text x="1043" y="174">VOZIME</text><text x="1067" y="363">CHAIN</text><text x="764" y="391">DSP</text><text x="698" y="279">RF</text></g>
  <g fill="{c['teal']}"><circle cx="892" cy="76" r="5"/><circle cx="1032" cy="154" r="5"/><circle cx="1038" cy="348" r="5"/><circle cx="800" cy="416" r="5"/><circle cx="708" cy="250" r="5"/></g>
</g>
<path class="flow" d="M80 466H1120" stroke="{c['teal']}" stroke-opacity=".55" stroke-width="2"/>
<text x="80" y="495" fill="{c['faint']}" font-family="ui-monospace,Consolas,monospace" font-size="9" letter-spacing="1.4">INSTRUCTION → COGNITION → ACTION → ARTIFACT → VERIFICATION → RECEIPT</text>
</svg>'''


def maya(dark: bool) -> str:
    c = palette(dark)
    phases = [('01','OBSERVE','Acquire truth'),('02','FRAME','Model mission'),('03','DECIDE','Commit path'),('04','ACT','Execute safely'),('05','VERIFY','Challenge claim'),('06','RECEIPT','Persist proof')]
    nodes=[]
    for i,(n,title,copy) in enumerate(phases):
        x=76+i*174
        nodes.append(f'''<g transform="translate({x} 206)"><rect width="148" height="154" rx="14" fill="{c['surface']}" stroke="{c['line']}"/><circle cx="24" cy="28" r="9" fill="{c['surface']}" stroke="{c['teal']}" stroke-width="2"/><text x="24" y="32" text-anchor="middle" fill="{c['teal']}" font-family="ui-monospace,Consolas,monospace" font-size="8">{n}</text><text x="18" y="80" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="15" font-weight="700">{title}</text><text x="18" y="105" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="11">{copy}</text><path d="M18 128H130" stroke="{c['teal']}" stroke-opacity=".28"/></g>''')
    return f'''{header(1200, 430, 'MAYA Codex Nexus', 'Instruction becomes inspectable evidence through six authoritative phases.')}
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{c['teal']}"/><stop offset="1" stop-color="{c['blue']}"/></linearGradient></defs>
<rect width="1200" height="430" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="428" rx="17" fill="none" stroke="{c['line']}"/>
<text x="56" y="54" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">MAYA CODEX NEXUS / PROOF CONTINUUM</text>
<text x="56" y="98" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="30" font-weight="720">A mission becomes inspectable evidence.</text>
<text x="56" y="130" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="14">One runtime object connects intent, safe cognition, action, artifacts, verification, and receipts.</text>
<path d="M100 234H1100" stroke="url(#g)" stroke-width="2" stroke-dasharray="12 10"/>
{''.join(nodes)}
<circle cx="56" cy="398" r="5" fill="{c['teal']}"/><text x="72" y="402" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9">RAW PRIVATE REASONING SUPPRESSED · DISPLAY-SAFE COGNITION · EXACT EVIDENCE ORIGIN</text>
</svg>'''


def systems(dark: bool) -> str:
    c=palette(dark)
    systems=PROFILE['systems']
    positions=[(600,290),(335,120),(865,118),(1000,285),(858,458),(600,500),(340,458),(205,286),(600,92)]
    cards=[]
    links=[]
    for i,(system,(x,y)) in enumerate(zip(systems,positions,strict=True)):
        accent=system['accent']
        if i:
            links.append(f'<path d="M600 290L{x} {y}" stroke="{accent}" stroke-opacity=".24"/>')
        w=190 if i else 224
        h=72 if i else 94
        cards.append(f'''<g transform="translate({x-w/2} {y-h/2})"><rect width="{w}" height="{h}" rx="14" fill="{c['surface']}" stroke="{accent}" stroke-opacity=".65"/><text x="18" y="29" fill="{c['faint']}" font-family="ui-monospace,Consolas,monospace" font-size="8">{i+1:02d} · {escape(system['domain'].upper())}</text><text x="18" y="53" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="14" font-weight="700">{escape(system['short'])}</text>{'<text x="18" y="76" fill="'+c['muted']+'" font-family="ui-monospace,Consolas,monospace" font-size="8">FLAGSHIP / 6.6.1</text>' if i==0 else ''}<circle cx="{w-18}" cy="20" r="4" fill="{accent}"/></g>''')
    return f'''{header(1200, 610, 'Systems Atlas', 'Nine operational worlds connected by one engineering standard.')}
<rect width="1200" height="610" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="608" rx="17" fill="none" stroke="{c['line']}"/>
<text x="56" y="50" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">SYSTEMS ATLAS / NINE OPERATIONAL WORLDS</text>
<text x="56" y="88" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="27" font-weight="720">One engineering standard across nine product domains.</text>
<g stroke-width="1.5">{''.join(links)}</g>{''.join(cards)}
<text x="56" y="580" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="11">Autonomous AI · Mobility · Realtime interaction · Native DSP · RF sensing · Forensics · Quality automation · Blockchain research</text>
</svg>'''


def vozime(dark: bool) -> str:
    c=palette(dark)
    points=[(92,330),(280,292),(482,230),(690,160),(920,118)]
    labels=['REQUEST','MATCH','ARRIVAL','TRIP','COMPLETE']
    stops=[]
    for i,((x,y),label) in enumerate(zip(points,labels,strict=True)):
        stops.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{c["surface"]}" stroke="{c["blue"]}" stroke-width="3"/><text x="{x}" y="{y+34}" text-anchor="middle" fill="{c["muted"]}" font-family="ui-monospace,Consolas,monospace" font-size="8">{label}</text>')
    return f'''{header(1200, 430, 'Vozime mobility system', 'A deterministic trip lifecycle connecting request, match, arrival, trip, and completion.')}
<defs><linearGradient id="route" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{c['blue']}"/><stop offset="1" stop-color="{c['teal']}"/></linearGradient></defs>
<rect width="1200" height="430" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="428" rx="17" fill="none" stroke="{c['line']}"/>
<text x="56" y="52" fill="{c['blue']}" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">VOZIME / MOBILITY STATE AUTHORITY</text>
<text x="56" y="90" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="27" font-weight="720">Trust moves with the trip state.</text>
<g opacity=".25" stroke="{c['line']}"><path d="M0 150H1200M0 230H1200M0 310H1200"/><path d="M100 110V390M200 110V390M300 110V390M400 110V390M500 110V390M600 110V390M700 110V390M800 110V390M900 110V390M1000 110V390M1100 110V390"/></g>
<path d="M92 330C180 286 214 330 280 292S392 274 482 230 592 214 690 160 822 128 920 118" fill="none" stroke="{c['line']}" stroke-width="10" stroke-linecap="round"/>
<path d="M92 330C180 286 214 330 280 292S392 274 482 230 592 214 690 160 822 128 920 118" fill="none" stroke="url(#route)" stroke-width="6" stroke-linecap="round"/>
{''.join(stops)}
<g transform="translate(982 120)"><rect width="160" height="230" rx="26" fill="{c['surface']}" stroke="{c['line']}"/><text x="20" y="31" fill="{c['blue']}" font-family="ui-monospace,Consolas,monospace" font-size="8">TRIP IN PROGRESS</text><rect x="18" y="50" width="124" height="104" rx="14" fill="{c['surface2']}"/><path d="M36 132C60 112 79 126 99 100S118 76 132 80" fill="none" stroke="url(#route)" stroke-width="3"/><circle cx="36" cy="132" r="5" fill="{c['blue']}"/><circle cx="132" cy="80" r="5" fill="{c['teal']}"/><text x="20" y="183" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="14" font-weight="700">Moving safely</text><text x="20" y="204" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="9">ETA · 08 MIN</text></g>
<text x="56" y="400" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="11">Role-aware state · Maps · Realtime feedback · Notifications · Payment · Safety context</text>
</svg>'''


def ledger(dark: bool) -> str:
    c=palette(dark)
    leaves=[130,340,550,760,970]
    links=[]
    for x in leaves:
        parent=235 if x<445 else 655 if x<865 else 970
        links.append(f'<path d="M{x} 320C{x} 270 {parent} 248 {parent} 215" fill="none" stroke="{c["green"]}" stroke-opacity=".42"/>')
    links += [f'<path d="M235 185C235 145 445 130 445 100" fill="none" stroke="{c["green"]}" stroke-opacity=".42"/>',f'<path d="M655 185C655 145 445 130 445 100" fill="none" stroke="{c["green"]}" stroke-opacity=".42"/>',f'<path d="M970 185C970 145 775 130 775 100" fill="none" stroke="{c["green"]}" stroke-opacity=".42"/>',f'<path d="M445 70C445 42 610 42 610 28" fill="none" stroke="{c["green"]}" stroke-opacity=".65"/>',f'<path d="M775 70C775 42 610 42 610 28" fill="none" stroke="{c["green"]}" stroke-opacity=".65"/>']
    nodes=[]
    for i,x in enumerate(leaves): nodes.append(f'<g transform="translate({x-70} 320)"><rect width="140" height="64" rx="11" fill="{c["surface"]}" stroke="{c["line"]}"/><text x="70" y="27" text-anchor="middle" fill="{c["text"]}" font-family="ui-monospace,Consolas,monospace" font-size="10">RECEIPT {i+1:02d}</text><text x="70" y="45" text-anchor="middle" fill="{c["green"]}" font-family="ui-monospace,Consolas,monospace" font-size="8">{hashlib.sha256(str(i).encode()).hexdigest()[:10]}…</text></g>')
    return f'''{header(1200, 450, 'Blockchain proof fabric', 'Five chained receipts aggregate into one Merkle proof root.')}
<rect width="1200" height="450" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="448" rx="17" fill="none" stroke="{c['line']}"/>
<text x="56" y="52" fill="{c['green']}" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">BLOCKCHAIN PROOF FABRIC / RESEARCH</text>
<text x="56" y="90" fill="{c['text']}" font-family="Inter,system-ui,sans-serif" font-size="27" font-weight="720">Cryptographic receipts, not decorative Web3.</text>
<g>{''.join(links)}</g>
<g transform="translate(540 18)"><rect width="140" height="56" rx="12" fill="{c['surface']}" stroke="{c['green']}"/><text x="70" y="25" text-anchor="middle" fill="{c['text']}" font-family="ui-monospace,Consolas,monospace" font-size="10">MERKLE ROOT</text><text x="70" y="42" text-anchor="middle" fill="{c['green']}" font-family="ui-monospace,Consolas,monospace" font-size="8">A17F90D4…</text></g>
<g transform="translate(375 82)"><rect width="140" height="56" rx="12" fill="{c['surface']}" stroke="{c['line']}"/><text x="70" y="32" text-anchor="middle" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9">AGGREGATE 01</text></g><g transform="translate(705 82)"><rect width="140" height="56" rx="12" fill="{c['surface']}" stroke="{c['line']}"/><text x="70" y="32" text-anchor="middle" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9">AGGREGATE 02</text></g>
<g transform="translate(165 187)"><rect width="140" height="56" rx="12" fill="{c['surface']}" stroke="{c['line']}"/><text x="70" y="32" text-anchor="middle" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9">PAIR 01</text></g><g transform="translate(585 187)"><rect width="140" height="56" rx="12" fill="{c['surface']}" stroke="{c['line']}"/><text x="70" y="32" text-anchor="middle" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9">PAIR 02</text></g><g transform="translate(900 187)"><rect width="140" height="56" rx="12" fill="{c['surface']}" stroke="{c['line']}"/><text x="70" y="32" text-anchor="middle" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="9">PAIR 03</text></g>
{''.join(nodes)}
<text x="56" y="422" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="11">SHA-256 · Chained receipts · Merkle aggregation · Tamper propagation · No wallet or financial interaction</text>
</svg>'''


def capabilities(dark: bool) -> str:
    c=palette(dark)
    headers=['RESEARCH','PROTOTYPE','INTEGRATED','VERIFIED']
    xs=[720,840,960,1080]
    rows=[]
    for i,item in enumerate(PROFILE['capabilities']):
        y=130+i*48
        dots=''.join(f'<circle cx="{x}" cy="{y-5}" r="7" fill="{c["teal"] if item[key] else c["surface2"]}" stroke="{c["teal"] if item[key] else c["line"]}"/>' for x,key in zip(xs,['research','prototype','integrated','verified'],strict=True))
        rows.append(f'<text x="56" y="{y}" fill="{c["text"]}" font-family="Inter,system-ui,sans-serif" font-size="13">{escape(item["name"])}</text>{dots}')
    heads=''.join(f'<text x="{x}" y="82" text-anchor="middle" fill="{c["muted"]}" font-family="ui-monospace,Consolas,monospace" font-size="9" letter-spacing="1">{h}</text>' for x,h in zip(xs,headers,strict=True))
    return f'''{header(1200, 540, 'Capability maturity', 'Transparent maturity matrix separating research, prototype, integrated, and verified states.')}
<rect width="1200" height="540" rx="18" fill="{c['bg']}"/><rect x="1" y="1" width="1198" height="538" rx="17" fill="none" stroke="{c['line']}"/>
<text x="56" y="50" fill="{c['muted']}" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="2">CAPABILITY MATURITY / TRUTHFUL DISCLOSURE</text>{heads}<path d="M56 96H1144" stroke="{c['line']}"/>{''.join(rows)}
<text x="56" y="514" fill="{c['muted']}" font-family="Inter,system-ui,sans-serif" font-size="11">Research is not presented as production. Verification requires inspectable evidence.</text>
</svg>'''


import hashlib
for name,builder in [('hero',hero),('maya',maya),('systems',systems),('vozime',vozime),('ledger',ledger),('capabilities',capabilities)]:
    (OUT/f'{name}-dark.svg').write_text(builder(True),encoding='utf-8')
    (OUT/f'{name}-light.svg').write_text(builder(False),encoding='utf-8')
print(json.dumps({'generated':12,'output':str(OUT)}))
