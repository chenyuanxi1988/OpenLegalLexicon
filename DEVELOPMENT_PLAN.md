# Development Plan

## 1. Project objective

Build a reusable **English-first, multi-jurisdiction, Chinese-assisted legal dictionary**.

The primary user-facing unit is a legal word or phrase. Each finished entry must provide an English legal definition and a Chinese term translation, with jurisdiction and source information where required.

## 2. Mandatory editorial standards

### 2.1 Headwords
- Preserve original spelling and wording.
- Preserve multi-word phrases, Latin expressions, abbreviations, capitalization, and legally material punctuation.
- Do not silently normalize two distinct source entries into one.
- Where the source index contains duplicate-looking labels, retain both source IDs until the body entry has been checked and disambiguated.

### 2.2 English definitions
- Public canonical definitions must be **independently written**.
- Preserve distinct senses and materially different applications.
- Do not collapse jurisdiction-specific rules into a generic global rule.
- Oxford wording may be consulted for research and sense identification but should not be copied wholesale into the public dictionary.

### 2.3 Chinese translations
- The Chinese field is the translation of the word/phrase or of each distinct sense.
- It is **not** a sentence-by-sentence Chinese translation of the English definition.
- If no precise Chinese equivalent exists, state that explicitly and provide a careful descriptive translation where useful.
- Avoid importing a PRC-law meaning into a UK/EU/common-law term merely because the Chinese wording looks similar.

### 2.4 Jurisdiction
Use jurisdiction/scope labels whenever a proposition is not genuinely jurisdiction-neutral. Typical labels include:
- England and Wales
- UK
- Scotland / Northern Ireland, where relevant
- EU
- international law
- US
- common law
- historical / obsolete

### 2.5 Cross-references
- Convert source-style “See …” references into internal links once the target canonical entry exists.
- Do not create a link to a non-existent target without flagging it for review.
- Preserve meaningful distinctions between “see”, “compare”, and related-term references where editorially useful.

### 2.6 Source metadata
Each Oxford-derived entry must retain at least:
- source work: *A Dictionary of Law*, 10th ed. (2022);
- original EPUB source entry ID;
- original source file/letter where useful for audit.

Source metadata is for provenance and checking. It does not make Oxford definition prose part of OpenLegalLexicon's public licensed text.

## 3. Oxford 10e baseline

### 3.1 Main entries
The EPUB's own `Alphabetical List of Entries` yields exactly **4,854 main-entry links**.

This count is the completeness baseline for the Oxford main-entry pass.

### 3.2 Excluded from the 4,854 baseline
The following require separate inventories:
- the abbreviations appendix;
- terms, alternative names, and cross-referenced concepts occurring only inside entry text;
- other appendix/front/back-matter items.

They must not be counted as Oxford “main entries” unless they independently appear in the source alphabetical main-entry list.

### 3.3 Duplicate-looking source labels
The alphabetical index contains at least two repeated labels with different source IDs:
- `confession`
- `district judge`

These must remain separate in the source inventory pending/through body-entry disambiguation. Never deduplicate only by headword string.

## 4. Canonical entry schema

Recommended canonical Markdown structure:

```markdown
## headword

- **English definition**
  1. ...
  2. ...
- **中文译名**
  1. ...
  2. ...
- **Jurisdiction:** ...
- **Cross-references:** ...
- **Source:** Oxford 10e — `source-entry-id`
- **Review status:** ...
```

Equivalent CSV/data exports should preserve sense boundaries rather than flattening materially different meanings into one undifferentiated sentence.

## 5. File structure

```text
README.md
DEVELOPMENT_PLAN.md
THIRD_PARTY_NOTICES.md

sources/
  oxford_10e/
    README.md
    headwords.md
    headwords.csv
    by_letter/
      A.md ... Z.md

lexicon/
  A.md ... Z.md

exports/
  OpenLegalLexicon.md
  OpenLegalLexicon.csv
```

`lexicon/` and `exports/` are canonical-output locations. Source inventory files must not be mistaken for finished definitions.

## 6. Implementation order

Proceed in this order:

1. **Inventory all Oxford main entries**
   - establish the 4,854-entry source baseline;
   - retain original IDs;
   - record per-letter counts;
   - flag duplicate-looking labels.

2. **Establish the source list**
   - full Markdown inventory;
   - per-letter Markdown inventory;
   - CSV export.

3. **Draft canonical entries**
   - independently write English definitions;
   - add Chinese translations by sense;
   - preserve multi-sense structure.

4. **Jurisdiction and legal verification**
   - tag England and Wales / UK / EU / international / other scope;
   - check rules that may have changed since 2022 against authoritative current sources;
   - distinguish historical descriptions from current law.

5. **Cross-reference pass**
   - create internal links;
   - identify unresolved targets and spelling variants.

6. **Quality-control pass**
   - missing entries;
   - accidental duplicates;
   - source-ID coverage;
   - broken links;
   - sense loss;
   - jurisdiction leakage;
   - translation inconsistencies.

7. **Final exports and acceptance report**
   - alphabet-split Markdown;
   - complete Markdown;
   - CSV;
   - coverage statistics;
   - unresolved-review list.

## 7. Acceptance criteria

The Oxford main-entry phase is not complete unless:

- all 4,854 source IDs are represented exactly once in the source inventory;
- no source entry is dropped merely because its visible headword duplicates another;
- every finished canonical entry has an English definition and Chinese translation;
- different senses are preserved where legally meaningful;
- jurisdiction-specific propositions are labeled;
- source IDs are traceable;
- cross-reference targets have been checked;
- a final missing/duplicate/broken-link report is generated.

## 8. Repository safety rules

- **Do not create GitHub Actions workflows or other automation workflow files unless explicitly requested.**
- Do not create branches casually for bulk dictionary work.
- Do not perform destructive rewrites of source inventories without a reviewed replacement.
- Prefer coherent, auditable commits with source coverage reported in the commit message or acceptance note.
