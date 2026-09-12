import copy
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

from openlegallexicon.export import export_bundle, rime_rows, tsv
from openlegallexicon.ingest import judicial_rows, trademark_rows
from openlegallexicon.io import digest, read_json, read_jsonl, stable_id
from openlegallexicon.model import load_entries, reading, select
from openlegallexicon.validate import validate_entries, validate_sources

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries, cls.sources = load_entries(ROOT)

    def editorial_count(self):
        return sum(s['expected_records'] for s in self.sources if s.get('format') == 'editorial_seed')

    def test_entire_snapshot_is_accounted_for(self):
        original_sources=[s for s in self.sources if s.get('format')!='editorial_seed']
        original_source_ids={s['id'] for s in original_sources}
        original_entries=[e for e in self.entries if e['references'][0]['source_id'] in original_source_ids]
        self.assertEqual(sum(s['expected_records'] for s in original_sources),2734)
        self.assertEqual(len(original_entries),2730)
        self.assertEqual(sum(len(e['references']) for e in original_entries),2734)
        self.assertTrue(all(e['status'] in {'source_attributed','editorial_checked','quarantined'} for e in original_entries))
        authored=[e for e in self.entries if e['status']=='evidence_linked']
        self.assertEqual(len(authored),self.editorial_count())
        self.assertEqual(validate_sources(ROOT),[])
        self.assertEqual(validate_entries(self.entries,self.sources,ROOT),[])

    def test_stable_identity_not_dependent_on_page_number(self):
        self.assertEqual(stable_id('s','法院','court','unit'), stable_id('s',' 法院 ','court','unit'))
        self.assertNotEqual(stable_id('s','法院','court','unit'), stable_id('different','法院','court','unit'))
        self.assertNotEqual(stable_id('s','當事人','party','unit'),stable_id('s','當事人','data subject','unit'))

    def test_search_retains_polysemy(self):
        result=select(self.entries,query='當事人')
        self.assertTrue(result)
        self.assertEqual(len({e['id'] for e in result}),len(result))
        self.assertTrue(all(e['source_origin']=='TW' for e in result))
        self.assertEqual(select(self.entries,query='當事人',jurisdiction='CN'),[])

    def test_bilingual_pinyin_and_domain_search(self):
        self.assertTrue(select(self.entries,query='trademark',domain='intellectual_property'))
        self.assertTrue(select(self.entries,query='lv shi'))
        self.assertTrue(select(self.entries,query='律师'))
        self.assertTrue(select(self.entries,query='律師'))

    def test_learning_profile_is_evidence_linked_and_keeps_jurisdiction(self):
        core=select(self.entries,profile='learning',jurisdiction='CN')
        self.assertEqual(len(core),self.editorial_count())
        self.assertTrue(all(e['definition_zh'] and e['evidence'] and e['learning_note'] for e in core))
        self.assertTrue(all(e['review']['translation']=='project_authored' for e in core))
        self.assertEqual(select(core,jurisdiction='TW'),[])
        personal=next(e for e in core if e['id']=='cn-information-handler')
        self.assertIn('processor',personal['translation_note'])
        self.assertEqual(personal['evidence'][0]['articles'],[73])
        admin=next(e for e in core if e['id']=='cn-admin-penalty')
        self.assertEqual(admin['evidence'][0]['articles'],[2])
        labor=next(e for e in core if e['id']=='cn-labor-open-ended-contract')
        self.assertEqual(labor['evidence'][0]['articles'],[14])

    def test_evidence_rejects_missing_article_and_wrong_jurisdiction(self):
        entries=copy.deepcopy(self.entries)
        e=next(e for e in entries if e['id']=='cn-anonymization')
        e['evidence'][0]['articles']=[99999]
        e['jurisdictions']=['HK']
        errors=validate_entries(entries,self.sources,ROOT)
        self.assertTrue(any('evidence article not found' in x for x in errors))
        self.assertTrue(any('jurisdiction lacks' in x for x in errors))

    def test_evidence_rejects_claimed_definition_without_provenance(self):
        e=copy.deepcopy(next(e for e in self.entries if e['status']=='source_attributed'))
        e['definition_zh']='A definition with no cited evidence'
        self.assertTrue(any('definition_zh lacks' in x for x in validate_entries([e],self.sources,ROOT)))

    def test_evidence_text_tampering_fails_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'data/evidence').mkdir(parents=True);(root/'schema').mkdir()
            for name in ['entry.schema.json','evidence.schema.json']:
                (root/'schema'/name).write_bytes((ROOT/'schema'/name).read_bytes())
            docs=read_json(ROOT/'data/evidence/laws.json')
            docs[0]['articles'][0]['text']+=' tampered'
            (root/'data/evidence/laws.json').write_text(json.dumps(docs))
            self.assertTrue(any('hash mismatch' in x for x in validate_entries(self.entries,self.sources,root)))

    def test_legal_phrase_boundaries(self):
        self.assertEqual(reading('视同行政处分')['rime'],'shi tong xing zheng chu fen')
        self.assertIn('xing2 wei2',reading('一行为重复处罚')['tone_numbers'])
        self.assertEqual(reading('会计师')['rime'],'kuai ji shi')
        self.assertEqual(reading('银行法')['rime'],'yin hang fa')
        self.assertEqual(reading('律师')['rime'],'lv shi')
        self.assertIsNone(reading('甲（乙）'))

    def test_schema_blocks_invalid_values_and_unknown_fields(self):
        e=copy.deepcopy(self.entries[0]);e['domains']=['made_up_domain'];e['secret_extra']='x'
        errors=validate_entries([e],self.sources,ROOT)
        self.assertTrue(any('domains' in x for x in errors))
        self.assertTrue(any('secret_extra' in x for x in errors))

    def test_schema_blocks_unknown_version(self):
        e=copy.deepcopy(self.entries[0]);e['schema_version']='2.0.0'
        self.assertTrue(validate_entries([e],self.sources,ROOT))

    def test_duplicates_licenses_and_dangling_relations(self):
        e=copy.deepcopy(next(e for e in self.entries if e['status']=='source_attributed'));e['license']='CC-BY-4.0'
        e['relations']=[{'type':'related','target':'missing-record','evidence':'test fixture'}]
        errors=validate_entries([e,e],self.sources,ROOT)
        for message in ['duplicate ID','license mismatch','dangling']:
            self.assertTrue(any(message in x for x in errors),message)

    def test_jurisdiction_requires_evidence(self):
        e=copy.deepcopy(next(e for e in self.entries if e['status']=='source_attributed'));e['jurisdictions']=['CN']
        self.assertTrue(any('jurisdiction' in x for x in validate_entries([e],self.sources,ROOT)))

    def test_invalid_pinyin_alignment(self):
        e=copy.deepcopy(next(e for e in self.entries if e['pronunciation']))
        e['pronunciation']['rime']='wrong'
        self.assertTrue(any('syllables' in x for x in validate_entries([e],self.sources,ROOT)))
        e=copy.deepcopy(next(e for e in self.entries if e['id']=='cn-anonymization'))
        e['pronunciation']['rime']='ni ming shu'
        self.assertTrue(any('disagrees' in x for x in validate_entries([e],self.sources,ROOT)))

    def test_quarantine_exclusion(self):
        e=copy.deepcopy(self.entries[0]);e['status']='quarantined'
        self.assertEqual(select([e]),[])
        self.assertEqual(len(select([e],include_quarantined=True)),1)
        rows,excluded=rime_rows([e],'zh_Hans')
        self.assertEqual(rows,[]);self.assertEqual(excluded,[e['id']])

    def test_snapshot_tamper_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'data/snapshots').mkdir(parents=True)
            sources=copy.deepcopy(self.sources[:1]);sources[0]['snapshot']='data/snapshots/fixture.jsonl'
            (root/'data/sources.json').write_text(json.dumps(sources))
            (root/'data/annotations.json').write_text('{}')
            (root/'data/snapshots/fixture.jsonl').write_text('{}\n')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):load_entries(root)

    def test_duplicate_json_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.jsonl';path.write_text('{"id":1,"id":2}\n')
            with self.assertRaisesRegex(ValueError,'duplicate JSON key'):read_jsonl(path)

    def test_html_parser_detects_changed_page_or_missing_rows(self):
        def page(n):
            return f'<table class="table_sprite"><thead><tr><th>項次</th><th>中文</th><th>英文</th><th>提供單位</th></tr></thead><tbody><tr><td>{n}</td><td>詞</td><td>term</td><td>unit</td></tr></tbody></table>'
        self.assertEqual(judicial_rows([(1,page(1))])[0]['en'],'term')
        with self.assertRaisesRegex(ValueError,'indices'):judicial_rows([(1,page(2))])
        with self.assertRaisesRegex(ValueError,'missing glossary'):judicial_rows([(1,'<h1>error</h1>')])

    def test_csv_parser_handles_quotes_bom_and_rejects_ragged_rows(self):
        header='\ufeff序號,商標英文專有名詞,商標中文專有名詞,更新日期,發布機關代碼\r\n'
        rows=trademark_rows((header+'1,"a,b",甲,20250711,unit\r\n').encode())
        self.assertEqual(rows[0]['en'],'a,b')
        with self.assertRaisesRegex(ValueError,'ragged'):trademark_rows((header+'1,a,甲,20250711,unit,extra\n').encode())

    def test_tsv_roundtrip_tabs_quotes_newlines(self):
        rows=[['a\tb','"quoted"','line\nbreak','中文']]
        self.assertEqual(list(csv.reader(io.StringIO(tsv(rows)),delimiter='\t')),rows)

    def test_build_reproducibility_traceability_and_rime_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths=[Path(tmp)/'a',Path(tmp)/'b']
            for path in paths:
                export_bundle(self.entries,self.sources,ROOT,path,{})
            first=read_json(paths[0]/'SHA256SUMS.json')
            self.assertEqual(first,read_json(paths[1]/'SHA256SUMS.json'))
            for filename,expected in first.items():self.assertEqual(digest(paths[0]/filename),expected)
            manifest = read_json(paths[0]/'build.json')
            evidence_files = sorted((ROOT/'data/evidence').glob('laws*.json'))
            expected_evidence = {p.relative_to(ROOT).as_posix(): digest(p) for p in evidence_files if p.is_file()}
            self.assertGreater(len(expected_evidence), 1)
            self.assertEqual(manifest['evidence_registries_sha256'], expected_evidence)
            self.assertEqual(manifest['evidence_sha256'], expected_evidence['data/evidence/laws.json'])
            with (paths[0]/'legal_dictionary_core.csv').open(encoding='utf-8-sig') as stream:
                core=list(csv.DictReader(stream))
            self.assertEqual(len(core),self.editorial_count())
            self.assertTrue(all(row['中文释义'] and 'https://' in row['法律依据'] for row in core))
            cards=list(csv.reader(io.StringIO('\n'.join(line for line in (paths[0]/'anki_core.tsv').read_text().splitlines() if not line.startswith('#'))),delimiter='\t'))
            self.assertEqual(len(cards),self.editorial_count()*2)
            self.assertTrue(all('review::project_authored' in row[6] and 'https://' in row[5] and row[4] for row in cards))
            ids={e['id'] for e in self.entries}
            for suffix in ['hans','hant']:
                text=(paths[0]/f'openlegal_{suffix}.dict.yaml').read_text()
                header,body=text.split('...\n',1)
                parsed=yaml.safe_load(header)
                self.assertEqual(parsed['columns'],['text','code','weight'])
                self.assertFalse(parsed['use_preset_vocabulary'])
                rows=list(csv.reader(io.StringIO(body),delimiter='\t'))
                index=read_json(paths[0]/f'openlegal_{suffix}.index.json')['rows']
                self.assertEqual(len(rows),len(index))
                self.assertEqual(len(rows),len({tuple(r[:2]) for r in rows}))
                for row,mapping in zip(rows,index):
                    self.assertEqual(len(row),3)
                    self.assertEqual(row[:2],[mapping['text'],mapping['code']])
                    self.assertTrue(set(mapping['entry_ids'])<=ids)
                    self.assertEqual(len(row[0]),len(row[1].split()))
            with self.assertRaisesRegex(ValueError,'already exists'):
                export_bundle([],[],ROOT,paths[0],{})

    def test_cli_error_exit_and_readable_results(self):
        env={**os.environ,'PYTHONPATH':str(ROOT/'src')}
        command=[sys.executable,'-m','openlegallexicon','--root',str(ROOT),'search','律师']
        result=subprocess.run(command,env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('律師',result.stdout)
        self.assertIn('法域 待核查',result.stdout)
        result=subprocess.run(command+['--limit','0'],env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,2)


if __name__=='__main__':unittest.main()
