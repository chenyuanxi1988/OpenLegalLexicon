#!/usr/bin/env python3
"""Build Oxford 10e source inventories from the user-supplied EPUB.

Outputs:
- 4,854 A-Z main-entry records (CSV, complete Markdown, A-Z Markdown)
- abbreviations appendix inventory
- entry-internal marked subterm inventory
- validation report

The script stores no Oxford definition prose. It extracts only headwords,
abbreviation expansions, marked internal terms, source IDs, and source links
needed for provenance, coverage checking, and later independent editorial work.
"""
from pathlib import Path
from collections import Counter, defaultdict, OrderedDict
import argparse
import csv
import re
import zipfile
from bs4 import BeautifulSoup

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWYZ"  # Oxford has no X source part


def parse(epub: Path):
    zf = zipfile.ZipFile(epub)
    alpha = BeautifulSoup(zf.read("OEBPS/0002_FM_AlphaList.xhtml"), "xml")
    links = alpha.find_all("a")
    main_links = links[26:]  # contents link + 25 letter-navigation links

    main = []
    for ordinal, a in enumerate(main_links, 1):
        headword = a.get_text(" ", strip=True)
        href = a.get("href")
        source_file, source_id = href.split("#", 1)
        part_no = int(source_file.split("_part", 1)[1].split(".xhtml", 1)[0])
        letter = LETTERS[part_no - 1]
        main.append(
            dict(
                ordinal=ordinal,
                letter=letter,
                headword=headword,
                source_id=source_id,
                source_file=source_file,
                source_href=href,
            )
        )

    abbrev_doc = BeautifulSoup(zf.read("OEBPS/036_BM_abbrev.xhtml"), "xml")
    abbreviations = []
    for ordinal, p in enumerate(abbrev_doc.find_all("p", class_="abbrevlist"), 1):
        abbreviations.append(
            dict(
                ordinal=ordinal,
                abbreviation=p.find(class_="abb-term").get_text(" ", strip=True),
                expansion=p.find(class_="abb-def").get_text(" ", strip=True),
                source_id=p.get("id"),
            )
        )

    main_by_id = {r["source_id"]: r["headword"] for r in main}
    main_texts = defaultdict(list)
    for r in main:
        main_texts[r["headword"]].append(r["source_id"])

    internal = []
    for part_no in range(1, 26):
        source_file = f"{9 + part_no:03d}_part{part_no}.xhtml"
        doc = BeautifulSoup(zf.read("OEBPS/" + source_file), "xml")
        current_id = current_headword = None
        for span in doc.find_all("span", class_="chaptersubt"):
            text = span.get_text(" ", strip=True)
            a = span.find("a")
            anchor_id = a.get("id") if a else None
            if anchor_id in main_by_id:
                current_id = anchor_id
                current_headword = main_by_id[anchor_id]
                continue
            if not text or re.fullmatch(r"\(?\d+[.)]?\)?", text):
                continue
            internal.append(
                dict(
                    ordinal=len(internal) + 1,
                    term=text,
                    source_file=source_file,
                    parent_source_id=current_id,
                    parent_headword=current_headword,
                    also_main_headword="yes" if text in main_texts else "no",
                )
            )

    zf.close()
    return main, abbreviations, internal


def write_csv(path: Path, rows):
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def write_outputs(out: Path, main, abbreviations, internal):
    out.mkdir(parents=True, exist_ok=True)
    (out / "by_letter").mkdir(exist_ok=True)

    write_csv(out / "headwords.csv", main)
    write_csv(out / "abbreviations.csv", abbreviations)
    write_csv(out / "internal_terms.csv", internal)

    lines = [
        "# Oxford 10e Main-Entry Inventory",
        "",
        "**Main-entry baseline:** 4,854 source links.",
        "",
    ]
    current = None
    for r in main:
        if r["letter"] != current:
            current = r["letter"]
            lines += [f"## {current}", ""]
        lines.append(
            f'{r["ordinal"]}. **{r["headword"]}** — `{r["source_id"]}` — `{r["source_file"]}`'
        )
    (out / "headwords.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        vals = [r for r in main if r["letter"] == letter]
        ll = [f"# Oxford 10e — {letter}", "", f"**Count:** {len(vals)}", ""]
        ll += [
            f'- **{r["headword"]}** — `{r["source_id"]}` — `{r["source_file"]}`'
            for r in vals
        ]
        (out / "by_letter" / f"{letter}.md").write_text(
            "\n".join(ll) + "\n", encoding="utf-8"
        )

    ab = [
        "# Oxford 10e Abbreviations Appendix Inventory",
        "",
        f"**Count:** {len(abbreviations)}",
        "",
        "> Separate from the 4,854 main-entry baseline.",
        "",
    ]
    for r in abbreviations:
        ab.append(
            f'{r["ordinal"]}. **{r["abbreviation"]}** — {r["expansion"]} — `{r["source_id"]}`'
        )
    (out / "abbreviations.md").write_text("\n".join(ab) + "\n", encoding="utf-8")

    unique_internal = OrderedDict()
    for r in internal:
        unique_internal.setdefault(r["term"], r)
    internal_main = {r["term"] for r in internal if r["also_main_headword"] == "yes"}
    internal_nonmain = {r["term"] for r in internal if r["also_main_headword"] == "no"}
    il = [
        "# Oxford 10e Entry-Internal Term Inventory",
        "",
        f"**Occurrences:** {len(internal)}",
        f"**Unique visible terms:** {len(unique_internal)}",
        f"**Unique terms also present as main headwords:** {len(internal_main)}",
        f"**Unique terms not present as main headwords:** {len(internal_nonmain)}",
        "",
        "> Candidate/review inventory only. Do not automatically promote every internal label to a canonical main entry.",
        "",
    ]
    for r in internal:
        il.append(
            f'{r["ordinal"]}. **{r["term"]}** — parent: **{r["parent_headword"]}** '
            f'(`{r["parent_source_id"]}`) — main-headword match: `{r["also_main_headword"]}`'
        )
    (out / "internal_terms.md").write_text("\n".join(il) + "\n", encoding="utf-8")

    counts = Counter(r["letter"] for r in main)
    labels = defaultdict(list)
    for r in main:
        labels[r["headword"]].append(r["source_id"])
    duplicates = {k: v for k, v in labels.items() if len(v) > 1}

    vr = [
        "# Oxford 10e Inventory Validation Report",
        "",
        f'- Total main-entry records: **{len(main)}**',
        f'- Unique source IDs: **{len({r["source_id"] for r in main})}**',
        f'- Duplicate source IDs: **{len(main) - len({r["source_id"] for r in main})}**',
        f'- Duplicate-looking headword labels: **{len(duplicates)}**',
        f'- Abbreviations appendix records: **{len(abbreviations)}**',
        f'- Entry-internal marked-term occurrences: **{len(internal)}**',
        f'- Unique entry-internal visible terms: **{len(unique_internal)}**',
        f'- Unique entry-internal non-main terms: **{len(internal_nonmain)}**',
        "",
    ]
    for k, v in duplicates.items():
        vr.append(f'- `{k}`: ' + ", ".join(f'`{x}`' for x in v))
    vr += ["", "## Per-letter counts", "", "| Letter | Count |", "|---|---:|"]
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        vr.append(f"| {letter} | {counts.get(letter, 0)} |")
    (out / "VALIDATION_REPORT.md").write_text("\n".join(vr) + "\n", encoding="utf-8")


def validate(main, abbreviations, internal):
    if len(main) != 4854:
        raise SystemExit(f"Expected 4854 main entries, got {len(main)}")
    ids = [r["source_id"] for r in main]
    if len(set(ids)) != 4854:
        raise SystemExit("Main-entry source IDs are not unique")
    if len(abbreviations) != 127:
        raise SystemExit(f"Expected 127 abbreviation records, got {len(abbreviations)}")
    if len(internal) != 708:
        raise SystemExit(f"Expected 708 marked internal-term occurrences, got {len(internal)}")


def main_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", type=Path)
    ap.add_argument("--out", type=Path, default=Path("sources/oxford_10e"))
    args = ap.parse_args()
    main, abbreviations, internal = parse(args.epub)
    validate(main, abbreviations, internal)
    write_outputs(args.out, main, abbreviations, internal)
    print(
        f"OK: {len(main)} main entries / {len(abbreviations)} abbreviations / "
        f"{len(internal)} internal-term occurrences"
    )


if __name__ == "__main__":
    main_cli()
