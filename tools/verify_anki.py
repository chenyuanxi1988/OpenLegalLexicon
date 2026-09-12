"""Verify TSV with Anki's actual importer in a disposable collection."""
import argparse
import csv
import html
import importlib.metadata
import io
from pathlib import Path
import tempfile

from anki.collection import Collection, ImportCsvRequest, CsvMetadata

from openlegallexicon.io import write_json


def main():
    p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,required=True);p.add_argument('--out',type=Path);args=p.parse_args()
    path=(args.bundle/'anki.tsv').resolve()
    body='\n'.join(line for line in path.read_text().splitlines() if not line.startswith('#'))
    rows=list(csv.reader(io.StringIO(body),delimiter='\t'))
    expected={row[0]:row for row in rows}
    if len(expected)!=len(rows):raise ValueError('duplicate note keys')
    with tempfile.TemporaryDirectory(prefix='oll-anki-') as tmp:
        col=Collection(str(Path(tmp)/'collection.anki2'))
        try:
            model=col.models.new('OpenLegalLexicon')
            for field in ['ID','Front','Back','Scope','Note','Source']:
                col.models.add_field(model,col.models.new_field(field))
            template=col.models.new_template('Card')
            template['qfmt']='{{Front}}<hr>{{Scope}}'
            template['afmt']='{{FrontSide}}<hr id="answer">{{Back}}<p>{{Note}}</p><small>{{Source}}</small>'
            col.models.add_template(model,template)
            model_id=col.models.add_dict(model).id
            metadata=col.get_csv_metadata(str(path),None)
            if metadata.is_html or metadata.tags_column!=7:
                raise ValueError('Anki did not recognize the TSV headers')
            metadata.global_notetype.id=model_id
            metadata.global_notetype.field_columns[:]=[1,2,3,4,5,6]
            metadata.dupe_resolution=CsvMetadata.UPDATE
            request=ImportCsvRequest(path=str(path),metadata=metadata)
            col.import_csv(request)
            first_notes=col.note_count();first_cards=col.card_count()
            if first_notes!=len(rows) or first_cards!=len(rows):
                raise ValueError(f'first import count mismatch: {first_notes} notes / {first_cards} cards / expected {len(rows)}')
            col.import_csv(request)
            if col.note_count()!=first_notes or col.card_count()!=first_cards:
                raise ValueError('reimport duplicated records')
            for fields,tags in col.db.all('select flds, tags from notes'):
                values=[html.unescape(v) for v in fields.split('\x1f')]
                row=expected[values[0]]
                if values!=row[:6]:raise ValueError(f'field loss or incorrect mapping: {values[0]}')
                if set(tags.split())!=set(row[6].split()):raise ValueError('lost source/domain tags')
            report={'engine':'Anki','version':importlib.metadata.version('anki'),'isolated_collection':True,'first_import_notes':first_notes,'first_import_cards':first_cards,'second_import_notes':col.note_count(),'second_import_cards':col.card_count(),'all_fields_and_tags_match':True}
            if args.out:write_json(args.out,report)
            print(f'PASS: {first_notes} notes/cards; identical reimport count; every field and tag preserved')
        finally:col.close()


if __name__=='__main__':main()
