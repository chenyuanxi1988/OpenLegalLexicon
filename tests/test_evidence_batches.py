import json
from pathlib import Path
import tempfile
import unittest

from openlegallexicon.evidence import documents, evidence_registry_hashes
from openlegallexicon.io import digest


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

    def test_provenance_tracks_batch_changes_and_only_loaded_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(evidence_registry_hashes(root), {})
            evidence = root / 'data' / 'evidence'
            evidence.mkdir(parents=True)
            baseline = evidence / 'laws.json'
            batch = evidence / 'laws-extra.json'
            baseline.write_text('[{"id":"baseline"}]', encoding='utf-8')
            batch.write_text('[{"id":"first"}]', encoding='utf-8')
            (evidence / 'source_targets.json').write_text('[]', encoding='utf-8')
            (evidence / 'laws-directory.json').mkdir()
            before = evidence_registry_hashes(root)
            self.assertEqual(before, {
                'data/evidence/laws.json': digest(baseline),
                'data/evidence/laws-extra.json': digest(batch),
            })
            batch.write_text('[{"id":"second"}]', encoding='utf-8')
            after = evidence_registry_hashes(root)
            self.assertEqual(before['data/evidence/laws.json'], after['data/evidence/laws.json'])
            self.assertNotEqual(before['data/evidence/laws-extra.json'], after['data/evidence/laws-extra.json'])
            baseline.unlink()
            self.assertEqual(evidence_registry_hashes(root), {'data/evidence/laws-extra.json': digest(batch)})
            self.assertEqual(documents(root), [{'id': 'second'}])


if __name__ == '__main__':
    unittest.main()
