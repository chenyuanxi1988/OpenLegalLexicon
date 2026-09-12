"""Deterministic extraction of numbered PRC legal articles from pinned HTML."""
import re

from bs4 import BeautifulSoup


CHINESE_DIGITS = {c: i for i, c in enumerate('零一二三四五六七八九')}
CHINESE_DIGITS['〇'] = 0
CHINESE_UNITS = {'十': 10, '百': 100, '千': 1000}


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
    """Return {article_number: normalized full article text} from one HTML page.

    The extractor intentionally requires a complete 1..N article-heading sequence.
    A partial page, duplicate heading, missing article, or reordered text fails closed.
    """
    soup = BeautifulSoup(raw, 'html.parser')
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    text = soup.get_text('\n', strip=True)
    matches = list(re.finditer(r'(?m)^第([一二三四五六七八九十百千零〇]+)条[\s\u3000]', text))
    numbers = [chinese_number(match[1]) for match in matches]
    if not numbers or numbers != list(range(1, len(numbers) + 1)):
        raise ValueError('Missing, duplicate or reordered article headings')
    articles = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.start():end].strip()
        body = re.split(r'\n第[一二三四五六七八九十百千零〇]+[编章节]', body)[0].strip()
        articles[numbers[index]] = ' '.join(body.split())
    return articles
