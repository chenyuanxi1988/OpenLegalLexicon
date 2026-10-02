# Oxford 10e Source Inventory

Source work: Oxford University Press, *A Dictionary of Law*, 10th edition (2022).

## Verified main-entry baseline

The EPUB's own `Alphabetical List of Entries` contains **4,880 links** in total. After excluding:
- 1 link to the alphabetical-list heading; and
- 25 in-page letter-navigation links,

there are exactly **4,854 main-entry links**.

These 4,854 links are the completeness baseline for the Oxford main-entry pass.

## Per-letter counts

| Letter | Count |
|---|---:|
| A | 367 |
| B | 158 |
| C | 597 |
| D | 302 |
| E | 285 |
| F | 175 |
| G | 107 |
| H | 110 |
| I | 257 |
| J | 79 |
| K | 12 |
| L | 201 |
| M | 216 |
| N | 121 |
| O | 107 |
| P | 477 |
| Q | 43 |
| R | 319 |
| S | 433 |
| T | 193 |
| U | 95 |
| V | 93 |
| W | 93 |
| X | 0 |
| Y | 10 |
| Z | 4 |

**Total: 4,854.**

Oxford's alphabetical index contains no `X` main-entry section in this EPUB.

Letter membership is taken from the Oxford A–Z source-part structure (`part1` through `part25`, corresponding to A–W, Y, Z), not simply from the first visible character of a headword. This matters for entries such as `“but for” test`, `“dog-leg” claim`, `“Dutch courage”`, and `18–25 trust`.

## Supplementary inventories

The following have now also been independently counted, while remaining outside the 4,854 main-entry baseline:

- **Abbreviations appendix:** 127 abbreviation records.
- **Entry-internal marked subterms:** 708 occurrences after removing purely numeric sense labels.
- **Unique visible internal terms:** 694.
- **Unique internal terms also appearing as main headwords:** 249.
- **Unique internal terms not appearing as main headwords:** 445.

The internal-term inventory is a candidate/review inventory only. An internal label must not automatically be promoted to a canonical dictionary headword.

## Reproducibility

`tools/build_oxford_inventory.py` rebuilds the 4,854-record source inventory from the user-supplied EPUB without storing Oxford definition prose.

`VALIDATION_REPORT.md` records the count and duplicate checks.

Planned/generated inventory outputs are:

- `headwords.csv` — full source inventory with ordinal, letter, headword, source ID, and source XHTML file;
- `headwords.md` — human-readable complete list;
- `by_letter/A.md` ... `by_letter/Z.md` — letter-split human-readable inventories;
- `abbreviations.csv` / `abbreviations.md` — separate abbreviations appendix inventory;
- `internal_terms.csv` / `internal_terms.md` — separate entry-internal candidate-term inventory.

## Known review flags

Two visible alphabetical-index labels occur twice with different source IDs:
- `confession`
- `district judge`

They are intentionally retained as separate source records. Body-entry review is required before any canonical deduplication or naming normalization.
