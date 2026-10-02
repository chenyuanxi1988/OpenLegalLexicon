#!/usr/bin/env python3
"""Generate A-Z canonical editorial scaffolds from sources/oxford_10e/headwords.csv.

This deliberately does not fabricate definitions or translations. It creates a
stable place for every source record and preserves the source ID until the
entry has been independently drafted and reviewed.
"""
from pathlib import Path
import argparse
import csv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=Path("sources/oxford_10e/headwords.csv"))
    ap.add_argument("--out", type=Path, default=Path("lexicon"))
    args = ap.parse_args()

    with args.source.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 4854:
        raise SystemExit(f"Expected 4854 records, got {len(rows)}")

    args.out.mkdir(parents=True, exist_ok=True)
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        vals = [r for r in rows if r["letter"] == letter]
        lines = [
            f"# OpenLegalLexicon — {letter}",
            "",
            "> Editorial scaffold. Pending fields must be independently drafted and reviewed; do not substitute Oxford definition prose.",
            "",
        ]
        for r in vals:
            lines += [
                f'## {r["headword"]}',
                "",
                "- **English definition:** _Pending independent editorial draft._",
                "- **中文译名:** _待独立编审。_",
                "- **Jurisdiction / scope:** _Pending review._",
                "- **Cross-references:** _Pending review._",
                f'- **Source:** Oxford 10e — `{r["source_id"]}`',
                "- **Review status:** `inventory`",
                "",
            ]
        (args.out / f"{letter}.md").write_text("\n".join(lines), encoding="utf-8")

    print("OK: canonical scaffolds generated for 4,854 source records")


if __name__ == "__main__":
    main()
