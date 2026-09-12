"""Schema checks plus cross-record/source invariants, all offline."""
from pathlib import Path
from functools import lru_cache
import hashlib
import re

from jsonschema import Draft202012Validator, FormatChecker

from .io import normalized, read_json, read_jsonl
from .model import PURE_HAN
from .evidence import documents


@lru_cache(maxsize=8)
def schema_validator(schema_path, modified_ns):
    schema = read_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_errors(value, schema_path, label):
    validator = schema_validator(str(schema_path), Path(schema_path).stat().st_mtime_ns)
    return [f"{label}:{'.'.join(str(p) for p in error.absolute_path) or '$'}: {error.message}" for error in sorted(validator.iter_errors(value), key=lambda e: str(list(e.absolute_path)))]


def validate_sources(root):
    root = Path(root)
    sources = read_json(root / "data/sources.json")
    errors = schema_errors(sources, root / "schema/sources.schema.json", "data/sources.json")
    if errors:
        return errors
    if len({s['id'] for s in sources}) != len(sources):
        errors.append("data/sources.json: duplicate source ID")
    for source in sources:
        if source['redistribution'] != 'permitted':
            errors.append(f"{source['id']}: source not cleared for redistribution")
        path = root / source['snapshot']
        if not path.resolve().is_relative_to(root.resolve() / 'data/snapshots'):
            errors.append(f"{source['id']}: snapshot escapes data/snapshots")
            continue
        for i, row in enumerate(read_jsonl(path), 1):
            if source.get('format') == 'editorial_seed':
                errors.extend(schema_errors(row, root / 'schema/editorial.schema.json', f'{path}:{i}'))
                continue
            expected = {'source_id','record','zh','en','context','page','source_updated'}
            if not isinstance(row, dict) or set(row) != expected:
                errors.append(f"{path}:{i}: unexpected snapshot fields")
                continue
            if any(not isinstance(row[k], str) or not row[k].strip() for k in ['source_id','record','zh','en','context']):
                errors.append(f"{path}:{i}: empty/non-string source cell")
            if not isinstance(row['page'], int) or isinstance(row['page'], bool) or not 1 <= row['page'] <= source['pages']:
                errors.append(f"{path}:{i}: invalid source page")
    return errors


def validate_evidence(root):
    root = Path(root)
    docs = documents(root)
    if not docs:
        return [], {}
    errors = schema_errors(docs, root / 'schema/evidence.schema.json', 'legal evidence')
    if errors:
        return errors, {}
    lookup = {}
    for doc in docs:
        if doc['id'] in lookup:
            errors.append(f"legal evidence: duplicate document {doc['id']}")
        lookup[doc['id']] = doc
        seen = set()
        for article in doc['articles']:
            if article['number'] in seen:
                errors.append(f"{doc['id']}: duplicate article number")
            seen.add(article['number'])
            if hashlib.sha256(article['text'].encode('utf-8')).hexdigest() != article['sha256']:
                errors.append(f"{doc['id']}: article {article['number']} hash mismatch")
    return errors, lookup


def validate_entries(entries, sources, root):
    root = Path(root)
    errors, docs = validate_evidence(root)
    seen = set()
    sources_by_id = {s['id']:s for s in sources}
    ids = {e.get('id') for e in entries}
    for entry in entries:
        label = entry.get('id', '<missing-id>')
        entry_errors = schema_errors(entry, root / 'schema/entry.schema.json', label)
        errors.extend(entry_errors)
        if entry_errors:
            continue
        if label in seen:
            errors.append(f"{label}: duplicate ID")
        seen.add(label)
        for key, text in entry['forms'].items():
            if text != normalized(text):
                errors.append(f"{label}:forms.{key}: not normalized NFC/whitespace")
        for ref in entry['references']:
            source = sources_by_id.get(ref['source_id'])
            if source is None:
                errors.append(f"{label}: unknown source {ref['source_id']}")
            elif entry['license'] != source['license']:
                errors.append(f"{label}: source/data license mismatch")
        if bool(entry['jurisdictions']) != (entry['jurisdiction_basis'] != 'not_assessed'):
            errors.append(f"{label}: jurisdiction requires an explicit basis")
        supported = set()
        supported_jurisdictions = set()
        for evidence in entry['evidence']:
            doc = docs.get(evidence['document_id'])
            if doc is None:
                errors.append(f"{label}: unknown evidence document {evidence['document_id']}")
                continue
            numbers = {a['number'] for a in doc['articles']}
            if not set(evidence['articles']) <= numbers:
                errors.append(f"{label}: evidence article not found")
                continue
            supported.update(evidence['supports'])
            if 'jurisdictions' in evidence['supports']:
                supported_jurisdictions.update(doc['jurisdictions'])
        if not set(entry['jurisdictions']) <= supported_jurisdictions:
            errors.append(f"{label}: jurisdiction lacks matching legal evidence")
        for field in ['definition_zh', 'learning_note']:
            if entry[field] and field not in supported:
                errors.append(f"{label}: {field} lacks legal evidence")
        if entry['status'] == 'evidence_linked':
            if not entry['definition_zh'] or not entry['evidence'] or not entry['review']['editor']:
                errors.append(f"{label}: evidence_linked requires definition, evidence and named editor")
        if entry['review']['translation'] == 'project_authored':
            if not entry['translation_note'] or entry['alignment'] != 'contextual_translation':
                errors.append(f"{label}: project translation requires a note and contextual alignment")
        for relation in entry['relations']:
            if relation['target'] not in ids or relation['target'] == label:
                errors.append(f"{label}: dangling or self relation {relation['target']}")
        pronunciation = entry['pronunciation']
        if pronunciation:
            zh = entry['forms']['zh_Hans']
            if not PURE_HAN.fullmatch(zh) or len(pronunciation['rime'].split()) != len(zh) or len(pronunciation['tone_numbers'].split()) != len(zh):
                errors.append(f"{label}: pinyin syllables do not align with Chinese characters")
            tones = pronunciation['tone_numbers']
            if not re.fullmatch(r'[a-zvü]+[1-5](?: [a-zvü]+[1-5])*', tones):
                errors.append(f"{label}: invalid tone-number pinyin")
            elif re.sub(r'[1-5]', '', tones) != pronunciation['rime']:
                errors.append(f"{label}: toneless pinyin disagrees with tone-number pinyin")
        if entry['status'] == 'editorial_checked' and entry['review']['editor'] is None:
            errors.append(f"{label}: editorial status requires a named review record")
    return errors
