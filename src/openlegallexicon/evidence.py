"""Offline, versioned legal evidence; no inferred official English translation."""
from pathlib import Path

from opencc import OpenCC

from .io import read_json


def documents(root):
    path = Path(root) / 'data/evidence/laws.json'
    return read_json(path) if path.exists() else []


def editorial_entry(row, source, docs, pronunciation):
    lookup = {d['id']: d for d in docs}
    used = [lookup[e['document_id']] for e in row['evidence']]
    context = '；'.join(dict.fromkeys(d['title'] for d in used))
    return {
        'schema_version': '1.1.0', 'id': row['id'],
        'forms': {'zh_Hans': row['zh'], 'zh_Hant': OpenCC('s2t').convert(row['zh']), 'en': row['en']},
        'script_conversion': {'method': 'OpenCC-s2t-0.1.7', 'review': 'machine_generated'},
        'source_origin': source['origin'], 'jurisdictions': ['CN'],
        'jurisdiction_basis': 'editorial_with_evidence', 'legal_status': 'not_assessed',
        'domains': row['domains'], 'domain_basis': 'editorial',
        'kind': row['kind'], 'kind_basis': 'editorial', 'alignment': 'contextual_translation',
        'pronunciation': pronunciation, 'scope_note': source['scope'] + ' 依据：' + context,
        'definition_zh': row['definition_zh'], 'learning_note': row['learning_note'],
        'translation_note': row['translation_note'], 'evidence': row['evidence'],
        'references': [{'source_id': source['id'], 'record': row['id'], 'page': 1,
                        'context': context, 'source_updated': source['retrieved']}],
        'relations': row['relations'], 'license': source['license'],
        'review': {'extraction': 'validated', 'translation': 'project_authored',
                   'editor': 'OpenLegalLexicon / Codex (AI-assisted; no human expert review)'},
        'flags': [], 'status': 'evidence_linked',
    }


def reference_text(entry, docs):
    lookup = {d['id']: d for d in docs}
    return ' | '.join(
        f"{lookup[ref['document_id']]['title']} 第{','.join(map(str, ref['articles']))}条 "
        f"{lookup[ref['document_id']]['url']}"
        for ref in entry['evidence']
    )
