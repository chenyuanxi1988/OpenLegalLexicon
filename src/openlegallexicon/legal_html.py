"""Deterministic extraction of numbered PRC legal articles from pinned HTML."""
import re

from bs4 import BeautifulSoup


CHINESE_DIGITS = {c: i for i, c in enumerate('零一二三四五六七八九')}
CHINESE_DIGITS['〇'] = 0
CHINESE_UNITS = {'十': 10, '百': 100, '千': 1000}
ARTICLE_HEADING_RE = re.compile(
    r'(?m)^第([一二三四五六七八九十百千零〇]+)条(?:之([一二三四五六七八九十百千零〇]+))?[\s\u3000]'
)


def chinese_number(text):
    total = number = 0
    for char in text:
        if char in CHINESE_DIGITS:
            number = CHINESE_DIGITS[char]
        elif char in CHINESE_UNITS:
            total += (number or 1) * CHINESE_UNITS[char]
            number = 0
        else:
            raise ValueError(f'unsupported Chinese numeral character: {char}')
    return total + number


def extract_articles(raw):
    """Return {base_article_number: normalized full article text} from one HTML page.

    The extractor requires a complete 1..N sequence of base article headings. Inserted
    headings such as ``第十七条之一`` are recognized as boundaries so their text is not
    accidentally appended to the preceding base article. They are currently not
    returned because the evidence schema cites base article numbers only.

    A partial page, duplicate/reordered heading, missing base article, or malformed
    ordering fails closed.
    """
    soup = BeautifulSoup(raw, 'html.parser')
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    text = soup.get_text('\n', strip=True)
    matches = list(ARTICLE_HEADING_RE.finditer(text))
    if not matches:
        raise ValueError('Missing, duplicate or reordered article headings')

    labels = [
        (chinese_number(match[1]), chinese_number(match[2]) if match[2] else 0)
        for match in matches
    ]
    if len(labels) != len(set(labels)) or labels != sorted(labels):
        raise ValueError('Missing, duplicate or reordered article headings')

    base = [(index, match, label[0]) for index, (match, label) in enumerate(zip(matches, labels)) if label[1] == 0]
    numbers = [number for _, _, number in base]
    if not numbers or numbers != list(range(1, len(numbers) + 1)):
        raise ValueError('Missing, duplicate or reordered article headings')

    articles = {}
    for match_index, match, number in base:
        end = matches[match_index + 1].start() if match_index + 1 < len(matches) else len(text)
        body = text[match.start():end].strip()
        body = re.split(r'\n第[一二三四五六七八九十百千零〇]+[编章节]', body)[0].strip()
        articles[number] = ' '.join(body.split())
    return articles
