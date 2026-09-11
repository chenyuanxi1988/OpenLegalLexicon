"""Strict UTF-8 JSON I/O and reproducible serialization."""
import hashlib
import json
import unicodedata
from pathlib import Path


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def read_jsonl(path):
    result = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"{path}:{number}: blank JSONL record")
        try:
            result.append(json.loads(line, object_pairs_hook=reject_duplicates))
        except (ValueError, TypeError) as error:
            raise ValueError(f"{path}:{number}: {error}") from error
    return result


def encode_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, values):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(encode_json(v) + "\n" for v in values), encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalized(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def stable_id(source, zh, en, context):
    # Source/reading associations, not globally merged legal concepts.
    key = encode_json([source, normalized(zh), normalized(en), normalized(context)])
    return source + "-" + hashlib.sha256(key.encode()).hexdigest()[:20]
