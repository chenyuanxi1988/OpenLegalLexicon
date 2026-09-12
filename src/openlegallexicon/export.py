"""Deterministic distributions, including traceability for lossy formats."""
from collections import defaultdict
import csv
import io
from pathlib import Path
import re
import shutil
import tempfile

from . import __version__
from .io import digest, write_json, write_jsonl
from .model import PURE_HAN, eligible, quality_report
from .evidence import documents, evidence_registry_hashes, reference_text


def separated_values(rows, delimiter):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, delimiter=delimiter, lineterminator='\n')
    writer.writerows(rows)
    return stream.getvalue()


def tsv(rows):
    return separated_values(rows, '\t')


def rime_rows(entries, script):
    grouped = defaultdict(set)
    exclusions = []
    for entry in entries:
        text = entry['forms'][script]
        if not eligible(entry) or not PURE_HAN.fullmatch(text) or not 2 <= len(text) <= 20 or not entry['pronunciation']:
            exclusions.append(entry['id'])
            continue
        code = entry['pronunciation']['rime']
        if len(code.split()) != len(text) or not re.fullmatch(r'[a-zv]+(?: [a-zv]+)*', code):
            exclusions.append(entry['id'])
            continue
        grouped[(text, code)].add(entry['id'])
    return [(text, code, sorted(ids)) for (text, code), ids in sorted(grouped.items(), key=lambda p:(p[0][1],p[0][0]))], exclusions


def export_bundle(entries, sources, root, destination, filters):
    root, destination = Path(root), Path(destination)
    if destination.exists():
        raise ValueError(f'{destination}: output already exists; choose a new directory')
    if destination.resolve().is_relative_to(root.resolve() / 'data'):
        raise ValueError('output must not be inside source data')
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.oll-build-', dir=destination.parent))
    try:
        active = [e for e in entries if eligible(e)]
        docs = documents(root)
        used_docs = {r['document_id'] for e in entries for r in e['evidence']}
        write_json(stage / 'legal_evidence.json', [d for d in docs if d['id'] in used_docs])
        source_ids = {ref['source_id'] for e in entries for ref in e['references']}
        selected_sources = [s for s in sources if s['id'] in source_ids]
        write_jsonl(stage / 'lexicon.jsonl', entries)
        write_json(stage / 'sources.json', selected_sources)
        write_json(stage / 'quality.json', quality_report(entries, selected_sources))
        attribution = '# 数据来源与许可\n\n'
        for source in selected_sources:
            attribution += f"- {source['attribution']} [资料]({source['url']})；[许可]({source['license_url']})。\n"
        attribution += '\nOpenLegalLexicon contributors：原创注释、编排及转换，CC BY 4.0。软件 MIT。法条原文摘录依据《中华人民共和国著作权法》第五条第一项，不对法条本身主张著作权。\n\n简繁转换、拼音与部分分类由程序生成；原机构未审核或认可本衍生物。资料地区不等于适用法域。词对不能直接当作跨法域等义定义。project_authored 表示项目释译，不是官方译文或法律专家审核；evidence_linked 表示已关联具体法条。\n'
        (stage / 'ATTRIBUTION.md').write_text(attribution, encoding='utf-8')
        for filename in ['DATA_LICENSE.md', 'THIRD_PARTY_NOTICES.md', 'LICENSE']:
            shutil.copyfile(root / filename, stage / filename)
        table = [['id','zh_Hans','zh_Hant','en','source_origin','jurisdictions','domains','pinyin','translation_review','source_ids']]
        for e in active:
            table.append([e['id'],e['forms']['zh_Hans'],e['forms']['zh_Hant'],e['forms']['en'],e['source_origin'],','.join(e['jurisdictions']),','.join(e['domains']),e['pronunciation']['tone_numbers'] if e['pronunciation'] else '',e['review']['translation'],','.join(sorted({r['source_id'] for r in e['references']}))])
        (stage / 'lexicon.tsv').write_text(tsv(table), encoding='utf-8')
        study=[['中文','繁體','英文','拼音','领域','适用法域','来源地区','类型','来源语境','学习注释','来源记录','条目ID','数据许可','译文审核','中文释义','译法说明','法律依据']]
        core_study=[study[0]]
        for e in sorted(active,key=lambda e:(e['forms']['zh_Hans'],e['id'])):
            row=[e['forms']['zh_Hans'],e['forms']['zh_Hant'],e['forms']['en'],e['pronunciation']['tone_numbers'] if e['pronunciation'] else '',','.join(e['domains']),','.join(e['jurisdictions']) or '待核查',e['source_origin'],e['kind'],e['references'][0]['context'],e['learning_note'],' | '.join(f"{r['source_id']}:{r['record']}" for r in e['references']),e['id'],e['license'],e['review']['translation'],e['definition_zh'],e['translation_note'],reference_text(e,docs)]
            study.append(row)
            if e['definition_zh'] and e['evidence']:
                core_study.append(row)
        (stage / 'legal_dictionary.tsv').write_text(tsv(study),encoding='utf-8')
        # BOM lets desktop spreadsheet applications recognize Chinese UTF-8 reliably.
        (stage / 'legal_dictionary.csv').write_text(separated_values(study,','),encoding='utf-8-sig')
        (stage / 'legal_dictionary_core.csv').write_text(separated_values(core_study,','),encoding='utf-8-sig')
        for script,suffix in [('zh_Hans','zh'),('zh_Hant','zh_hant')]:
            words=sorted({e['forms'][script] for e in active if PURE_HAN.fullmatch(e['forms'][script]) and 2<=len(e['forms'][script])<=40})
            (stage / f'legal_terms_{suffix}.txt').write_text(''.join(w+'\n' for w in words),encoding='utf-8')
        # Custom first-field IDs are visible, stable note keys, not fabricated Anki GUIDs.
        cards = []
        core_cards = []
        for e in active:
            scope = f"来源地区 {e['source_origin']} / 法域 {','.join(e['jurisdictions']) or '待核查'} / {e['references'][0]['context']}"
            provenance = ' | '.join(f"{r['source_id']}:{r['record']}" for r in e['references'])
            if e['evidence']:
                provenance += ' | ' + reference_text(e,docs)
            note = ' '.join(s for s in [e['definition_zh'],e['learning_note'],e['translation_note']] if s)
            tags = ' '.join(['OpenLegalLexicon', f"origin::{e['source_origin']}", f"review::{e['review']['translation']}", *[f'domain::{d}' for d in e['domains']], *[f'jurisdiction::{j}' for j in e['jurisdictions']]])
            for direction, front, back in [('zh-en',e['forms']['zh_Hans'],e['forms']['en']),('en-zh',e['forms']['en'],e['forms']['zh_Hans'])]:
                card=[f"{e['id']}:{direction}",front,back,scope,note,provenance,tags]
                cards.append(card)
                if e['definition_zh'] and e['evidence']:
                    core_cards.append(card)
        header = '#separator:Tab\n#html:false\n#tags column:7\n#columns:ID\tFront\tBack\tScope\tNote\tSource\tTags\n'
        (stage / 'anki.tsv').write_text(header + tsv(cards), encoding='utf-8')
        (stage / 'anki_core.tsv').write_text(header + tsv(core_cards), encoding='utf-8')
        english = defaultdict(set)
        for e in active:
            term = e['forms']['en']
            if len(term) <= 100 and re.fullmatch(r"[A-Za-z][A-Za-z0-9 ’'.,()/-]*",term):
                english[term].add(e['id'])
        (stage / 'english.txt').write_text(''.join(term+'\n' for term in sorted(english,key=lambda t:(t.casefold(),t))), encoding='utf-8')
        write_json(stage / 'english.index.json', {term:sorted(ids) for term,ids in english.items()})
        statistics = {'entries':len(entries),'study_notes':len(cards),'core_study_entries':len(core_study)-1,'english_completions':len(english)}
        for script, suffix in [('zh_Hans','hans'),('zh_Hant','hant')]:
            name = 'openlegal_' + suffix
            rows, excluded = rime_rows(entries, script)
            header = f'# Rime dictionary\n# Data: see ATTRIBUTION.md and DATA_LICENSE.md\n# Pronunciations include machine-generated readings; fixed weight is not corpus frequency.\n---\nname: {name}\nversion: "{__version__}"\nsort: by_weight\nuse_preset_vocabulary: false\ncolumns: [text, code, weight]\n...\n'
            (stage / f'{name}.dict.yaml').write_text(header + tsv((text,code,1) for text,code,_ in rows), encoding='utf-8')
            schema = f'''# Isolated legal vocabulary scheme, UTF-8
schema:
  schema_id: {name}
  name: 法律词汇（{suffix}）
  version: "{__version__}"
engine:
  processors: [speller, selector, navigator, express_editor]
  segmentors: [abc_segmentor]
  translators: [script_translator]
speller:
  alphabet: abcdefghijklmnopqrstuvwxyz
  delimiter: "'"
translator:
  dictionary: {name}
  enable_sentence: false
  enable_user_dict: false
  enable_completion: true
  enable_encoder: false
'''
            (stage / f'{name}.schema.yaml').write_text(schema, encoding='utf-8')
            write_json(stage / f'{name}.index.json', {'rows':[{'text':text,'code':code,'entry_ids':ids} for text,code,ids in rows], 'excluded_entry_ids':excluded})
            statistics[f'rime_{suffix}_rows'] = len(rows)
        builder_hashes={p.relative_to(root).as_posix():digest(p) for p in sorted((root/'src/openlegallexicon').glob('*.py'))}
        evidence_hashes = evidence_registry_hashes(root)
        write_json(stage / 'build.json', {'tool_version':__version__,'schema_version':'1.1.0','builder_sha256':builder_hashes,'source_registry_sha256':digest(root/'data/sources.json'),'evidence_sha256':evidence_hashes.get('data/evidence/laws.json'),'evidence_registries_sha256':evidence_hashes,'filters':filters,'statistics':statistics,'input_snapshots':{s['snapshot']:s['snapshot_sha256'] for s in selected_sources},'annotations_sha256':digest(root/'data/annotations.json')})
        checksums = {p.name:digest(p) for p in sorted(stage.iterdir()) if p.is_file()}
        write_json(stage / 'SHA256SUMS.json', checksums)
        stage.rename(destination)
        return statistics
    except BaseException:
        shutil.rmtree(stage)
        raise
