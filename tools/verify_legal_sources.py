"""Verify selected legal articles against the pinned original HTML cache.

No network calls and no mutation of the approved evidence registry. Download
each document's public URL as <document-id>.html into a separate cache first.
"""
import argparse
from pathlib import Path

from openlegallexicon.evidence import documents
from openlegallexicon.io import digest, write_json
from openlegallexicon.legal_html import extract_articles


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, default=Path.cwd())
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    checked = 0
    results = []
    for doc in documents(args.root):
        path = args.cache / (doc['id'] + '.html')
        if digest(path) != doc['html_sha256']:
            raise ValueError(f"{doc['id']}: source HTML differs from the approved version; inspect before updating")
        articles = extract_articles(path.read_bytes())
        for item in doc['articles']:
            if articles.get(item['number']) != item['text']:
                raise ValueError(f"{doc['id']}: article {item['number']} extraction mismatch")
            checked += 1
        print(f"PASS: {doc['id']}, {len(doc['articles'])} cited articles / {len(articles)} numbered articles")
        results.append({'id':doc['id'],'url':doc['url'],'html_sha256':doc['html_sha256'],
                        'cited_articles':len(doc['articles']),'numbered_articles':len(articles),
                        'all_selected_text_matches':True})
    if args.out:
        write_json(args.out,{'documents':results,'checked_articles':checked,'source_retrieved_dates':sorted({d['retrieved'] for d in documents(args.root)}),
                             'note':'Exact source-text extraction check; not human legal or translation review.'})
    print(f'PASS: {checked} evidence articles match pinned primary-source HTML')


if __name__ == '__main__':
    main()
