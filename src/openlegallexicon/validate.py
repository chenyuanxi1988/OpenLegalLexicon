"""Schema checks plus cross-record/source invariants, all offline."""
from pathlib import Path
from functools import lru_cache

from jsonschema import Draft202012Validator, FormatChecker

from .io import normalized, read_json, read_jsonl
from .model import PURE_HAN


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
            expected = {'source_id','record','zh','en','context','page','source_updated'}
            if not isinstance(row, dict) or set(row) != expected:
                errors.append(f"{path}:{i}: unexpected snapshot fields")
                continue
            if any(not isinstance(row[k], str) or not row[k].strip() for k in ['source_id','record','zh','en','context']):
                errors.append(f"{path}:{i}: empty/non-string source cell")
            if not isinstance(row['page'], int) or isinstance(row['page'], bool) or not 1 <= row['page'] <= source['pages']:
                errors.append(f"{path}:{i}: invalid source page")
    return errors


def validate_entries(entries, sources, root):
    root = Path(root)
    errors = []
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
        for relation in entry['relations']:
            if relation['target'] not in ids or relation['target'] == label:
                errors.append(f"{label}: dangling or self relation {relation['target']}")
        pronunciation = entry['pronunciation']
        if pronunciation:
            zh = entry['forms']['zh_Hans']
            if not PURE_HAN.fullmatch(zh) or len(pronunciation['rime'].split()) != len(zh) or len(pronunciation['tone_numbers'].split()) != len(zh):
                errors.append(f"{label}: pinyin syllables do not align with Chinese characters")
        if entry['status'] == 'editorial_checked' and entry['review']['editor'] is None:
            errors.append(f"{label}: editorial status requires a named review record")
    return errors
