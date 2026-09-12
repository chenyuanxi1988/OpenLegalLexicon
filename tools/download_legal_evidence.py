#!/usr/bin/env python3
"""Download pinned public legal-text targets into an isolated evidence cache.

The cache is intentionally outside the repository data tree. Each successful
HTTPS download is recorded with its SHA-256 before editorial evidence is added
to data/evidence/laws-*.json. This tool does not approve or mutate evidence.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import shutil
import subprocess

from openlegallexicon.io import digest, read_json, write_json


def validate_target(row: object) -> dict:
    if not isinstance(row, dict):
        raise ValueError('source target must be an object')
    required = {'id', 'title', 'url', 'version', 'jurisdiction', 'intended_domains', 'priority_articles'}
    if set(row) != required:
        raise ValueError(f"source target fields must be exactly {sorted(required)}")
    if not isinstance(row['id'], str) or not row['id']:
        raise ValueError('source target id must be non-empty')
    if not isinstance(row['url'], str) or not row['url'].startswith('https://'):
        raise ValueError(f"{row['id']}: HTTPS URL required")
    if row['jurisdiction'] != 'CN':
        raise ValueError(f"{row['id']}: current evidence bootstrap only accepts CN")
    if not isinstance(row['priority_articles'], list) or not row['priority_articles'] or any(
        isinstance(n, bool) or not isinstance(n, int) or n < 1 for n in row['priority_articles']
    ):
        raise ValueError(f"{row['id']}: priority_articles must be positive integers")
    if len(row['priority_articles']) != len(set(row['priority_articles'])):
        raise ValueError(f"{row['id']}: duplicate priority article")
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--check', action='store_true', help='validate target registry without network access')
    args = parser.parse_args()

    target_path = args.root / 'data/evidence/source_targets.json'
    targets = read_json(target_path)
    if not isinstance(targets, list) or not targets:
        raise ValueError(f'{target_path}: expected a non-empty JSON array')
    targets = [validate_target(row) for row in targets]
    ids = [row['id'] for row in targets]
    if len(ids) != len(set(ids)):
        raise ValueError(f'{target_path}: duplicate source target id')
    if args.check:
        print(f'OK: {len(targets)} legal evidence source targets')
        return 0

    curl = shutil.which('curl')
    if not curl:
        raise SystemExit('curl is required; TLS verification must remain enabled')
    args.cache.mkdir(parents=True, exist_ok=True)
    manifest_path = args.cache / 'legal-downloads.json'
    if manifest_path.exists():
        raise ValueError('use a fresh evidence cache directory; refusing to mix retrieval sessions')

    results = []
    for target in targets:
        path = args.cache / f"{target['id']}.html"
        temporary = path.with_suffix('.html.part')
        subprocess.run(
            [curl, '--fail', '--location', '--proto', '=https', '--proto-redir', '=https',
             '--max-time', '60', '--retry', '2', '--silent', '--show-error', '--output', str(temporary), target['url']],
            check=True,
        )
        temporary.replace(path)
        result = {
            'id': target['id'], 'title': target['title'], 'url': target['url'],
            'version': target['version'], 'path': path.name, 'sha256': digest(path),
            'bytes': path.stat().st_size, 'retrieved': date.today().isoformat(),
            'priority_articles': target['priority_articles'],
        }
        results.append(result)
        write_json(manifest_path, results)
        print(json.dumps(result, ensure_ascii=False), flush=True)

    print('Next: inspect every downloaded page, then build laws-*.json and run tools/verify_legal_sources.py.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
