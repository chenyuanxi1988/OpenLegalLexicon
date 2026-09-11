"""Explicit source associations with conservative, attributed enrichment."""
from collections import Counter, defaultdict
from pathlib import Path
import re

from opencc import OpenCC
from pypinyin import Style, lazy_pinyin

from .io import digest, normalized, read_json, read_jsonl, stable_id

PURE_HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+\Z")
DOMAIN_RULES = {
    "contracts": ["契約", "違約", "履約", "要約", "租賃", "買賣"],
    "company": ["公司", "股東", "董事", "股份", "合夥"],
    "m_and_a": ["併購", "合併", "收購"],
    "finance": ["銀行", "貸款", "利息", "債券", "信託", "證券", "基金", "金融"],
    "intellectual_property": ["商標", "專利", "著作權", "智慧財產", "營業秘密"],
    "privacy": ["個人資料", "隱私", "資訊隱私"],
    "competition": ["公平交易", "競爭", "壟斷", "聯合行為"],
    "employment": ["勞工", "勞動", "僱傭", "雇主", "工會", "罷工"],
    "tax": ["稅", "課徵"],
    "trade": ["進口", "出口", "關稅", "貿易"],
    "dispute_resolution": ["訴訟", "仲裁", "調解", "判決", "上訴", "法院", "裁定", "訴願", "審判", "證據"],
    "criminal": ["刑", "犯罪", "罪", "羈押", "逮捕", "拘提", "檢察", "偵查", "假釋"],
    "constitutional": ["憲法", "違憲", "基本權", "平等權", "人權", "法律保留", "比例原則"],
    "administrative": ["行政", "公務員", "公法", "公權力", "國家賠償"],
    "civil": ["民法", "民事", "物權", "債權", "侵權", "人格", "所有權"],
    "family": ["婚", "家事", "親權", "繼承", "收養", "扶養", "遺產", "少年"],
    "property": ["土地", "不動產", "地上權", "抵押", "地役權"],
}
DOMAINS = sorted([*DOMAIN_RULES, "core", "ai", "unclassified"])
KINDS = ["term", "statute", "institution", "role", "document", "action", "abbreviation", "unclassified"]
PINYIN_PHRASES = {
    "行政": "xing2 zheng4", "行为": "xing2 wei2", "执行": "zhi2 xing2",
    "行使": "xing2 shi3", "行刑": "xing2 xing2", "发行": "fa1 xing2",
    "银行": "yin2 hang2", "重复": "chong2 fu4", "重新": "chong2 xin1",
    "重行": "chong2 xing2", "会计": "kuai4 ji4", "会同": "hui4 tong2",
    "调解": "tiao2 jie3", "调查": "diao4 cha2", "调处": "tiao2 chu3",
    "调动": "diao4 dong4", "调任": "diao4 ren4", "处分": "chu3 fen4",
    "处罚": "chu3 fa2", "处所": "chu4 suo3", "正当": "zheng4 dang4",
    "不当": "bu4 dang4", "当事人": "dang1 shi4 ren2", "当庭": "dang1 ting2",
    "假释": "jia3 shi4", "给予": "ji3 yu3", "供给": "gong1 ji3",
}
PINYIN_PATTERN = re.compile('(' + '|'.join(sorted(PINYIN_PHRASES, key=lambda p:(-len(p),p))) + ')')


def infer_domains(row):
    if row["source_id"] == "tw-tipo-trademark":
        return ["intellectual_property"], "source_collection"
    domains = sorted(domain for domain, keys in DOMAIN_RULES.items() if any(key in row["zh"] for key in keys))
    return domains or ["unclassified"], "automatic_keyword_rules"


def infer_kind(zh, en):
    if re.fullmatch(r"[A-Z][A-Z0-9-]{1,15}", en):
        return "abbreviation"
    if re.search(r"(?:法|條例|規則|辦法|要點|準則|細則)$", zh) and len(zh) > 3:
        return "statute"
    if re.search(r"(?:法院|檢察署|委員會|事務所|政府|法務部)$", zh):
        return "institution"
    if re.search(r"(?:法官|檢察官|律師|當事人|證人|被告|原告)$", zh):
        return "role"
    if re.search(r"(?:判決書|聲請書|申請書|通知書|起訴書|契約書)$", zh):
        return "document"
    return "unclassified"


def reading(zh):
    if not PURE_HAN.fullmatch(zh):
        return None
    syllables = []
    for part in PINYIN_PATTERN.split(zh):
        if part in PINYIN_PHRASES:
            syllables.extend(PINYIN_PHRASES[part].split())
        elif part:
            syllables.extend(lazy_pinyin(part, style=Style.TONE3, neutral_tone_with_five=True))
    return {"system": "hanyu_pinyin", "tone_numbers": " ".join(syllables), "rime": " ".join(re.sub(r'[1-5]', '', syllable) for syllable in syllables), "method": "pypinyin-0.55.0+legal-phrase-boundaries-v1", "review": "machine_generated"}


def load_entries(root):
    root = Path(root)
    sources = read_json(root / "data/sources.json")
    overrides = read_json(root / "data/annotations.json")
    converter = OpenCC("t2s")  # Character/script conversion only; not tw2sp vocabulary localization.
    collected = {}
    for source in sources:
        if source["redistribution"] != "permitted":
            raise ValueError(f"source {source['id']}: redistribution is not permitted")
        path = root / source["snapshot"]
        if not path.resolve().is_relative_to(root.resolve() / "data/snapshots"):
            raise ValueError("snapshot path must remain inside data/snapshots")
        if digest(path) != source["snapshot_sha256"]:
            raise ValueError(f"{path}: snapshot hash mismatch; review and re-register the source update")
        rows = read_jsonl(path)
        if len(rows) != source["expected_records"]:
            raise ValueError(f"{path}: unexpected record count")
        seen_records = set()
        for row in rows:
            if row["source_id"] != source["id"] or row["record"] in seen_records:
                raise ValueError(f"{path}: wrong source ID or repeated record locator")
            seen_records.add(row["record"])
            zh, en = normalized(row["zh"]), normalized(row["en"])
            entry_id = stable_id(source["id"], zh, en, row["context"])
            reference = {"source_id": source["id"], "record": row["record"], "page": row["page"], "context": row["context"], "source_updated": row["source_updated"]}
            if entry_id in collected:
                collected[entry_id]["references"].append(reference)
                continue
            domains, basis = infer_domains(row)
            flags = []
            if not PURE_HAN.fullmatch(zh):
                flags.append("compound_or_annotated_chinese")
            if any(mark in zh + en for mark in ("○", "＿", "__", "〈", "〉")):
                flags.append("template_or_placeholder")
            if len(zh) > 20:
                flags.append("long_chinese_label")
            if re.search(r"[;；\n]", en):
                flags.append("multiple_or_annotated_translations")
            if "�" in zh + en or not re.search(r"[A-Za-z]", en):
                flags.append("invalid_bilingual_text")
            entry = {
                "schema_version": "1.0.0", "id": entry_id,
                "forms": {"zh_Hant": zh, "zh_Hans": converter.convert(zh), "en": en},
                "script_conversion": {"method": "OpenCC-t2s-0.1.7", "review": "machine_generated"},
                "source_origin": source["origin"], "jurisdictions": [],
                "jurisdiction_basis": "not_assessed", "legal_status": "not_assessed",
                "domains": domains, "domain_basis": basis,
                "kind": infer_kind(zh, en), "kind_basis": "automatic_surface_rules",
                "alignment": "source_association", "pronunciation": reading(converter.convert(zh)),
                "scope_note": source["scope"], "learning_note": "",
                "references": [reference], "relations": [],
                "license": source["license"], "review": {"extraction": "validated", "translation": "source_attributed", "editor": None},
                "flags": flags, "status": "source_attributed",
            }
            collected[entry_id] = entry
    for entry_id, annotation in overrides.items():
        if entry_id not in collected:
            raise ValueError(f"annotation references unknown entry {entry_id}")
        allowed = {"jurisdictions", "jurisdiction_basis", "domains", "domain_basis", "kind", "kind_basis", "learning_note", "relations", "status", "flags", "pronunciation"}
        if not isinstance(annotation, dict) or set(annotation) - allowed:
            raise ValueError(f"{entry_id}: unsupported annotation field")
        collected[entry_id].update(annotation)
    return sorted(collected.values(), key=lambda e: e["id"]), sources


def eligible(entry):
    return entry["status"] != "quarantined" and "invalid_bilingual_text" not in entry["flags"] and "template_or_placeholder" not in entry["flags"]


def select(entries, *, query="", domain=None, jurisdiction=None, origin=None, include_quarantined=False):
    query = normalized(query).casefold()
    result = []
    for e in entries:
        if not include_quarantined and not eligible(e):
            continue
        if domain and domain not in e["domains"]:
            continue
        if jurisdiction and jurisdiction not in e["jurisdictions"]:
            continue
        if origin and e["source_origin"] != origin:
            continue
        fields = [*e["forms"].values(), e["id"], e["learning_note"]]
        if e["pronunciation"]:
            fields.extend([e["pronunciation"]["rime"], e["pronunciation"]["tone_numbers"]])
        if query and not any(query in value.casefold() for value in fields):
            continue
        result.append(e)
    return result


def quality_report(entries, sources):
    homographs = defaultdict(list)
    for entry in entries:
        homographs[entry["forms"]["zh_Hans"]].append(entry["id"])
    return {
        "source_records": sum(s["expected_records"] for s in sources),
        "entries": len(entries), "eligible_entries": sum(eligible(e) for e in entries),
        "status": dict(Counter(e["status"] for e in entries)),
        "by_source": dict(Counter(e["references"][0]["source_id"] for e in entries)),
        "by_domain": dict(Counter(d for e in entries for d in e["domains"])),
        "jurisdiction_assessed": sum(bool(e["jurisdictions"]) for e in entries),
        "translation_review": dict(Counter(e["review"]["translation"] for e in entries)),
        "flags": dict(Counter(f for e in entries for f in e["flags"])),
        "homograph_groups": {text: ids for text, ids in sorted(homographs.items()) if len(ids) > 1},
        "limits": ["Source associations are not assertions of universal legal equivalence.", "Automated labels/readings are not independent legal review.", "Origin TW identifies the provider region, not the applicable legal jurisdiction."]
    }
