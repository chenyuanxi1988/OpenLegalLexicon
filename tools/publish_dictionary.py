"""Materialize downloadable text dictionaries; --check detects stale outputs."""
import argparse
from pathlib import Path
import tempfile

from openlegallexicon.export import export_bundle
from openlegallexicon.io import write_json, read_json, digest
from openlegallexicon.model import load_entries, select
from openlegallexicon.validate import validate_entries, validate_sources

FILES=['legal_dictionary.tsv','legal_dictionary.csv','legal_terms_zh.txt','legal_terms_zh_hant.txt','english.txt','english.index.json','openlegal_hans.dict.yaml','openlegal_hans.schema.yaml','openlegal_hans.index.json','openlegal_hant.dict.yaml','openlegal_hant.schema.yaml','openlegal_hant.index.json','ATTRIBUTION.md','DATA_LICENSE.md','sources.json','build.json']
FILES += ['legal_dictionary_core.csv','anki.tsv','anki_core.tsv','legal_evidence.json','lexicon.jsonl','README.md']


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path.cwd());p.add_argument('--check',action='store_true');args=p.parse_args()
    errors=validate_sources(args.root)
    if errors:raise ValueError('\n'.join(errors))
    entries,sources=load_entries(args.root)
    errors=validate_entries(entries,sources,args.root)
    if errors:raise ValueError('\n'.join(errors))
    with tempfile.TemporaryDirectory(prefix='oll-publish-') as tmp:
        stage=Path(tmp)/'bundle'
        export_bundle(select(entries),sources,args.root,stage,{'domain':None,'jurisdiction':None,'origin':None})
        destination=args.root/'dictionary'
        if not args.check:destination.mkdir(exist_ok=True)
        stale=[]
        for name in FILES:
            if args.check:
                if not (destination/name).exists() or (destination/name).read_bytes()!=(stage/name).read_bytes():stale.append(name)
            else:(destination/name).write_bytes((stage/name).read_bytes())
        checksums={name:digest(stage/name) for name in FILES}
        if args.check:
            if not (destination/'SHA256SUMS.json').exists() or read_json(destination/'SHA256SUMS.json')!=checksums:stale.append('SHA256SUMS.json')
        else:write_json(destination/'SHA256SUMS.json',checksums)
        if stale:raise ValueError('Regenerate dictionary outputs: '+', '.join(stale))
    print(('CHECKED' if args.check else 'WROTE')+f': {len(FILES)} downloadable files')


if __name__=='__main__':main()
