# Oxford 10e Source Inventory

Source work: Oxford University Press, *A Dictionary of Law*, 10th edition (2022).

## Verified main-entry baseline

The EPUB's own `Alphabetical List of Entries` contains **4,880 links** in total. After excluding:
- 1 link to the alphabetical-list heading; and
- 25 in-page letter-navigation links,

there are exactly **4,854 main-entry links**.

These 4,854 links are the completeness baseline for the first Oxford pass.

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

## Planned inventory files

- `headwords.csv` — full source inventory with ordinal, letter, headword, source ID, and source XHTML file.
- `headwords.md` — human-readable complete list.
- `by_letter/A.md` ... `by_letter/Z.md` — letter-split human-readable inventories.

## Known review flags

Two visible alphabetical-index labels occur twice with different source IDs:
- `confession`
- `district judge`

They are intentionally retained as separate source records. Body-entry review is required before any canonical deduplication or naming normalization.

## Not yet included

The following are separate workstreams and are not part of the 4,854 count:
- abbreviations appendix;
- terminology occurring only inside entry text;
- alternate labels or embedded subterms that are not independent alphabetical main entries.
