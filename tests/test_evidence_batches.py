import json
from pathlib import Path
import tempfile
import unittest

from openlegallexicon.evidence import documents


class EvidenceBatchTests(unittest.TestCase):
    def test_split_registries_load_in_filename_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / 'data' / 'evidence'
            evidence.mkdir(parents=True)
            (evidence / 'laws.json').write_text(json.dumps([{'id': 'baseline'}]), encoding='utf-8')
            (evidence / 'laws-tax.json').write_text(json.dumps([{'id': 'tax'}]), encoding='utf-8')
            (evidence / 'laws-admin.json').write_text(json.dumps([{'id': 'admin'}]), encoding='utf-8')
            (evidence / 'source_targets.json').write_text(json.dumps([{'id': 'ignored'}]), encoding='utf-8')
            self.assertEqual([row['id'] for row in documents(root)], ['baseline', 'admin', 'tax'])

    def test_registry_must_be_json_array(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / 'data' / 'evidence'
            evidence.mkdir(parents=True)
            (evidence / 'laws-invalid.json').write_text(json.dumps({'id': 'not-an-array'}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'JSON array'):
                documents(root)


if __name__ == '__main__':
    unittest.main()
