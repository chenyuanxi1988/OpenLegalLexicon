"""Snapshot extraction. HTML parsing is only needed when updating sources."""
import csv
import io
import re
from pathlib import Path

from .io import digest, read_json, write_json, write_jsonl


def judicial_rows(documents):
    from bs4 import BeautifulSoup
    rows = []
    for page, html in documents:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.select_one("table.table_sprite")
        if table is None:
            raise ValueError(f"judicial page {page}: missing glossary table")
        headers = [th.get_text(" ", strip=True) for th in table.select("thead th")]
        if headers != ["項次", "中文", "英文", "提供單位"]:
            raise ValueError(f"judicial page {page}: changed columns {headers}")
        for tr in table.select("tbody tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
            if len(cells) != 4 or not cells[0].isdigit() or not cells[1] or not cells[2]:
                raise ValueError(f"judicial page {page}: malformed row {cells}")
            rows.append({"source_id": "tw-judicial", "record": cells[0], "zh": cells[1], "en": cells[2], "context": cells[3], "page": page, "source_updated": None})
    indices = [int(r["record"]) for r in rows]
    if indices != list(range(1, len(rows) + 1)):
        raise ValueError("judicial: missing, repeated or out-of-order indices")
    return rows


def trademark_rows(raw):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    expected = ["序號", "商標英文專有名詞", "商標中文專有名詞", "更新日期", "發布機關代碼"]
    if reader.fieldnames != expected:
        raise ValueError(f"trademark: changed columns {reader.fieldnames}")
    rows = []
    for item in reader:
        if None in item or any(value is None for value in item.values()):
            raise ValueError("trademark: ragged CSV row")
        if not item["序號"].isdigit() or not item["商標中文專有名詞"].strip() or not item["商標英文專有名詞"].strip():
            raise ValueError("trademark: invalid row")
        date = item["更新日期"]
        if not re.fullmatch(r"\d{8}", date):
            raise ValueError("trademark: unexpected date")
        rows.append({"source_id": "tw-tipo-trademark", "record": item["序號"], "zh": item["商標中文專有名詞"], "en": item["商標英文專有名詞"], "context": item["發布機關代碼"], "page": 1, "source_updated": f"{date[:4]}-{date[4:6]}-{date[6:]}"})
    if [int(r["record"]) for r in rows] != list(range(1, len(rows) + 1)):
        raise ValueError("trademark: missing or repeated sequence")
    return rows


def import_snapshot(root, cache):
    root, cache = Path(root), Path(cache)
    sources = read_json(root / "data/sources.json")
    sources_by_id = {s["id"]: s for s in sources}
    judicial = sources_by_id["tw-judicial"]
    documents = [(i, (cache / f"judicial-{i}.html").read_text(encoding="utf-8")) for i in range(1, judicial["pages"] + 1)]
    extracted = {"tw-judicial": judicial_rows(documents), "tw-tipo-trademark": trademark_rows((cache / "tipo-trademark.csv").read_bytes())}
    # Validate the whole batch before publishing any snapshot.
    for source_id, rows in extracted.items():
        if len(rows) != sources_by_id[source_id]["expected_records"]:
            raise ValueError(f"{source_id}: count changed ({len(rows)}); inspect source and update its registry deliberately")
    for source_id, rows in extracted.items():
        path = root / sources_by_id[source_id]["snapshot"]
        write_jsonl(path, rows)
        sources_by_id[source_id]["snapshot_sha256"] = digest(path)
    write_json(root / "data/sources.json", sources)
    return {source_id: len(rows) for source_id, rows in extracted.items()}
