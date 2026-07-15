#!/usr/bin/env python3
"""Build deterministic APEX profile assets and verification receipt."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import runpy
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    profile_path = ROOT / 'content' / 'profile.json'
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    ids = [item['id'] for item in profile['systems']]
    if len(ids) != len(set(ids)):
        raise ValueError('system IDs must be unique')

    runpy.run_path(str(ROOT / 'scripts' / 'build_apex_assets.py'), run_name='__main__')
    (ROOT / 'docs' / 'data').mkdir(parents=True, exist_ok=True)
    shutil.copy2(profile_path, ROOT / 'docs' / 'data' / 'profile.json')

    files = {}
    for path in sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and 'receipts' not in p.parts):
        rel = path.relative_to(ROOT).as_posix()
        files[rel] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}

    receipt = {
        'schema': 'gonzo-profile-apex-build/v1',
        'systems': len(profile['systems']),
        'generated_apex_assets': len(list((ROOT / 'assets' / 'apex').glob('*.svg'))),
        'pages_runtime': 'dependency-free',
        'contains_credentials': False,
        'files': files,
    }
    (ROOT / 'receipts').mkdir(exist_ok=True)
    (ROOT / 'receipts' / 'profile-build.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'systems': len(profile['systems']), 'apex_assets': receipt['generated_apex_assets']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
