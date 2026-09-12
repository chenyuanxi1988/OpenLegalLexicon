import unittest

from openlegallexicon.legal_html import chinese_number, extract_articles


class LegalHtmlTests(unittest.TestCase):
    def test_chinese_article_numbers(self):
        self.assertEqual(chinese_number('一'), 1)
        self.assertEqual(chinese_number('十一'), 11)
        self.assertEqual(chinese_number('一百零一'), 101)
        self.assertEqual(chinese_number('一千二百六十'), 1260)

    def test_extract_complete_sequence_and_strip_later_chapter_heading(self):
        raw = '''<html><body>
        <p>第一条 第一条正文。</p>
        <p>第二条 第二条正文。</p>
        <h2>第二章 其他规定</h2>
        <p>第三条 第三条正文。</p>
        </body></html>'''.encode('utf-8')
        self.assertEqual(extract_articles(raw), {
            1: '第一条 第一条正文。',
            2: '第二条 第二条正文。',
            3: '第三条 第三条正文。',
        })

    def test_reject_missing_or_partial_sequence(self):
        raw = '<p>第二条 只有第二条。</p><p>第三条 只有第三条。</p>'.encode('utf-8')
        with self.assertRaisesRegex(ValueError, 'Missing, duplicate or reordered'):
            extract_articles(raw)


if __name__ == '__main__':
    unittest.main()
