"""Verify selected legal articles against the pinned original HTML cache.

No network calls and no mutation of the approved evidence registry. Download
each document's public URL as <document-id>.html into a separate cache first.
"""
import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup

from openlegallexicon.evidence import documents
from openlegallexicon.io import digest, write_json


def chinese_number(text):
    digits = {c: i for i, c in enumerate('零一二三四五六七八九')}
    digits['〇'] = 0
    units = {'十': 10, '百': 100, '千': 1000}
    total = number = 0
    for char in text:
        if char in digits:
            number = digits[char]
        else:
            total += (number or 1) * units[char]
            number = 0
    return total + number


def extract_articles(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    text = soup.get_text('\n', strip=True)
    matches = list(re.finditer(r'(?m)^第([一二三四五六七八九十百千零〇]+)条[\s\u3000]', text))
    numbers = [chinese_number(m[1]) for m in matches]
    if not numbers or numbers != list(range(1, len(numbers) + 1)):
        raise ValueError('Missing, duplicate or reordered article headings')
    articles = {}
    for i, match in enumerate(matches):
        body = text[match.start():matches[i + 1].start() if i + 1 < len(matches) else len(text)].strip()
        body = re.split(r'\n第[一二三四五六七八九十百千零〇]+[编章节]', body)[0].strip()
        articles[numbers[i]] = ' '.join(body.split())
    return articles


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
