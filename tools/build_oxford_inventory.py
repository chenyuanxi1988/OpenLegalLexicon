#!/usr/bin/env python3
"""Build the Oxford 10e headword inventory from the user-supplied EPUB.

This script stores no Oxford definition prose. It extracts only the alphabetical
main-entry labels and source links needed for provenance and coverage checking.
"""
from pathlib import Path
from collections import Counter, defaultdict
import argparse, csv, zipfile
from bs4 import BeautifulSoup

PREFIX = "acref-9780192897497-e-"

def extract(epub: Path):
    with zipfile.ZipFile(epub) as zf:
        soup = BeautifulSoup(zf.read("OEBPS/0002_FM_AlphaList.xhtml"), "xml")
    links = soup.find_all("a")
    main = links[26:]  # 1 contents link + 25 letter-navigation links
    rows=[]
    for ordinal,a in enumerate(main,1):
        headword=a.get_text(" ",strip=True)
        href=a.get("href")
        source_file,source_id=href.split("#",1)
        part_no=int(source_file.split("_part",1)[1].split(".xhtml",1)[0])
        letters="ABCDEFGHIJKLMNOPQRSTUVWYZ"
        letter=letters[part_no-1]
        rows.append(dict(ordinal=ordinal,letter=letter,headword=headword,source_id=source_id,source_file=source_file,source_href=href))
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("epub",type=Path)
    ap.add_argument("--out",type=Path,default=Path("sources/oxford_10e"))
    args=ap.parse_args(); rows=extract(args.epub); args.out.mkdir(parents=True,exist_ok=True); (args.out/"by_letter").mkdir(exist_ok=True)
    if len(rows)!=4854: raise SystemExit(f"Expected 4854 main entries, got {len(rows)}")
    ids=[r["source_id"] for r in rows]
    if len(set(ids))!=4854: raise SystemExit("Source IDs are not unique")
    with open(args.out/"headwords.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    lines=["# Oxford 10e Main-Entry Inventory","", "**Main-entry baseline:** 4,854 source links.",""]
    current=None
    for r in rows:
        if r["letter"]!=current: current=r["letter"]; lines += [f"## {current}",""]
        lines.append(f'{r["ordinal"]}. **{r["headword"]}** — `{r["source_id"]}` — `{r["source_file"]}`')
    (args.out/"headwords.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        vals=[r for r in rows if r["letter"]==L]
        ll=[f"# Oxford 10e — {L}","",f"**Count:** {len(vals)}",""]+[f'- **{r["headword"]}** — `{r["source_id"]}` — `{r["source_file"]}`' for r in vals]
        (args.out/"by_letter"/f"{L}.md").write_text("\n".join(ll)+"\n",encoding="utf-8")
    print(f"OK: {len(rows)} entries / {len(set(ids))} unique source IDs")

if __name__ == "__main__": main()
