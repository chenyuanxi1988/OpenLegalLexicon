#!/usr/bin/env python3
"""Build a deterministic queue for human review of source-attributed entries.

This tool does not alter annotations or claim legal review. It only ranks source
records so a maintainer can review the highest-risk/highest-value items first.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from openlegallexicon.io import write_json
from openlegallexicon.model import load_entries

HIGH_VALUE_KINDS = {"statute", "institution", "role", "document", "abbreviation"}


def source_id(entry):
    return entry["references"][0]["source_id"] if entry.get("references") else None


def member_view(entry):
    ref = entry["references"][0] if entry.get("references") else {}
    return {
        "id": entry["id"],
        "zh_Hant": entry["forms"].get("zh_Hant"),
        "zh_Hans": entry["forms"].get("zh_Hans"),
        "en": entry["forms"].get("en"),
        "source_id": source_id(entry),
        "record": ref.get("record"),
        "context": ref.get("context"),
        "domains": entry["domains"],
        "domain_basis": entry["domain_basis"],
        "kind": entry["kind"],
        "kind_basis": entry["kind_basis"],
        "jurisdictions": entry["jurisdictions"],
        "jurisdiction_basis": entry["jurisdiction_basis"],
        "status": entry["status"],
        "flags": entry["flags"],
        "translation_review": entry["review"]["translation"],
    }


def build_queue(entries, limit=100):
    by_text = defaultdict(list)
    for entry in entries:
        by_text[entry["forms"]["zh_Hans"]].append(entry)

    groups = []
    queued_ids = set()
    for text, members in by_text.items():
        if len(members) < 2:
            continue
        source_members = [e for e in members if e["status"] == "source_attributed"]
        reviewed_members = [e for e in members if e["status"] != "source_attributed"]
        if not source_members:
            continue
        source_sets = {source_id(e) for e in source_members}
        reasons = []
        score = 0
        if reviewed_members:
            reasons.append("homograph_with_reviewed_or_editorial_entry")
            score += 100
        if len(source_sets) > 1:
            reasons.append("homograph_across_source_collections")
            score += 70
        if any("unclassified" in e["domains"] for e in source_members):
            reasons.append("contains_unclassified_source_entry")
            score += 25
        if any(e["flags"] for e in source_members):
            reasons.append("contains_flagged_source_entry")
            score += 15
        if any(e["kind"] in HIGH_VALUE_KINDS for e in source_members):
            reasons.append("contains_high_value_surface_kind")
            score += 10
        groups.append({
            "priority": score,
            "zh_Hans": text,
            "reasons": reasons,
            "members": [member_view(e) for e in sorted(members, key=lambda x: x["id"])],
        })
        queued_ids.update(e["id"] for e in source_members)

    groups.sort(key=lambda row: (-row["priority"], row["zh_Hans"], [m["id"] for m in row["members"]]))

    singles = []
    for entry in entries:
        if entry["status"] != "source_attributed" or entry["id"] in queued_ids:
            continue
        reasons = []
        score = 0
        if "unclassified" in entry["domains"]:
            reasons.append("unclassified_domain")
            score += 30
        if entry["kind"] in HIGH_VALUE_KINDS:
            reasons.append("high_value_surface_kind")
            score += 25
        if entry["flags"]:
            reasons.append("quality_flag")
            score += 10
        if not reasons or score < 35:
            continue
        singles.append({
            "priority": score,
            "reasons": reasons,
            "entry": member_view(entry),
        })
    singles.sort(key=lambda row: (-row["priority"], row["entry"]["zh_Hans"], row["entry"]["id"]))

    source_entries = [e for e in entries if e["status"] == "source_attributed"]
    unclassified = [e for e in source_entries if "unclassified" in e["domains"]]
    return {
        "purpose": "Deterministic prioritization only; no item is legally reviewed by appearing in this queue.",
        "source_attributed_entries": len(source_entries),
        "unclassified_source_entries": len(unclassified),
        "homograph_review_groups_total": len(groups),
        "single_high_value_candidates_total": len(singles),
        "homograph_review_groups": groups[:limit],
        "single_high_value_candidates": singles[:limit],
        "limits": [
            "Source origin does not establish legal jurisdiction.",
            "Surface-kind and domain rules are machine-generated candidates, not legal review.",
            "Original source translations remain source-attributed until independently reviewed.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", default="reports/source-review-queue.json")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    entries, _ = load_entries(root)
    report = build_queue(entries, limit=args.limit)
    out = root / args.out
    write_json(out, report)
    print(
        f"WROTE: {out}; {report['homograph_review_groups_total']} homograph groups, "
        f"{report['single_high_value_candidates_total']} single high-value candidates, "
        f"{report['unclassified_source_entries']} unclassified source entries"
    )


if __name__ == "__main__":
    main()
