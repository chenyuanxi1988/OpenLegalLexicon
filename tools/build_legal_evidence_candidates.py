#!/usr/bin/env python3
"""Build reviewable evidence candidates from a fresh official-law HTML cache.

This tool is deliberately one-way: it reads a registered source-target batch and
a retrieval manifest, extracts only the requested articles, and writes a
candidate `laws-*.json`. It never edits approved evidence or editorial entries.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from openlegallexicon.io import digest, read_json, write_json
from openlegallexicon.legal_html import extract_articles


def resolved(root: Path, value: Path) -> Path:
    return value if value.is_absolute() else root / value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--targets', type=Path, default=Path('data/evidence/source_targets.json'),
                        help='target registry, relative to --root unless absolute')
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()

    if args.out.exists():
        raise ValueError(f'{args.out}: refusing to overwrite an existing candidate file')

    target_path = resolved(args.root, args.targets)
    targets = read_json(target_path)
    manifest = read_json(args.cache / 'legal-downloads.json')
    targets_by_id = {row['id']: row for row in targets}
    manifest_by_id = {row['id']: row for row in manifest}
    if len(targets_by_id) != len(targets) or len(manifest_by_id) != len(manifest):
        raise ValueError('duplicate target or manifest ID')
    if set(targets_by_id) != set(manifest_by_id):
        raise ValueError('retrieval manifest must cover exactly the registered source targets')

    documents = []
    for document_id in sorted(targets_by_id):
        target = targets_by_id[document_id]
        retrieval = manifest_by_id[document_id]
        expected = {
            'id': target['id'], 'title': target['title'], 'url': target['url'],
            'version': target['version'], 'priority_articles': target['priority_articles'],
        }
        for key, value in expected.items():
            if retrieval.get(key) != value:
                raise ValueError(f'{document_id}: retrieval manifest disagrees on {key}')
        path = args.cache / retrieval['path']
        if path.name != f'{document_id}.html' or path.parent.resolve() != args.cache.resolve():
            raise ValueError(f'{document_id}: unexpected cache path')
        if digest(path) != retrieval['sha256']:
            raise ValueError(f'{document_id}: downloaded HTML hash mismatch')

        extracted = extract_articles(path.read_bytes())
        missing = [number for number in target['priority_articles'] if number not in extracted]
        if missing:
            raise ValueError(f'{document_id}: requested articles missing from complete sequence: {missing}')
        selected = []
        for number in target['priority_articles']:
            text = extracted[number]
            selected.append({
                'number': number,
                'text': text,
                'sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            })
        documents.append({
            'id': document_id,
            'title': target['title'],
            'url': target['url'],
            'jurisdictions': [target['jurisdiction']],
            'retrieved': retrieval['retrieved'],
            'version': target['version'],
            'html_sha256': retrieval['sha256'],
            'text_basis': 'PRC-Copyright-Law-Article-5(1)',
            'articles': selected,
        })
        print(f'CANDIDATE: {document_id}, {len(selected)} selected / {len(extracted)} numbered articles')

    args.out.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.out, documents)
    print(f'WROTE: {args.out}; review source versions and extracted text before moving into data/evidence/laws-*.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
