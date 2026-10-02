# OpenLegalLexicon

OpenLegalLexicon is an **English-first, multi-jurisdiction, Chinese-assisted legal lexicon**.

The project is intended to build a practical legal-English dictionary in list form. Each canonical word or phrase will ultimately contain at least:

- the English headword or phrase;
- an independently written English legal definition, preserving distinct senses and scope;
- a Chinese translation for each sense (not a line-by-line Chinese translation of the full English definition);
- jurisdiction/scope labels where needed;
- cross-references to related entries;
- source metadata sufficient for verification.

## Current Oxford baseline

The present source baseline is Oxford University Press, *A Dictionary of Law*, 10th edition (2022), supplied to the project for research and indexing.

The EPUB's own alphabetical entry list contains **4,854 A–Z main-entry links**. This figure excludes:

- the separate abbreviations appendix;
- legal terms appearing only inside an entry;
- other non-main-entry material.

Those excluded categories will be inventoried separately and must not be silently merged into the 4,854-entry baseline.

## Editorial rule for definitions

OpenLegalLexicon does **not** use Oxford's definition prose as the public canonical definition text.

Oxford is used to identify headwords, senses, scope, cross-references, and issues requiring verification. Public English definitions are independently drafted by OpenLegalLexicon, then checked against authoritative legal sources where appropriate.

This separation preserves source fidelity while avoiding a public repository that simply republishes copyrighted dictionary prose.

## Canonical entry model

A finished entry should contain:

1. **Headword** — original spelling, including phrases, Latin expressions, and abbreviations.
2. **English definition** — original OpenLegalLexicon wording; separate senses where necessary.
3. **中文译名** — translation by sense; where there is no exact Chinese equivalent, say so rather than forcing one.
4. **Jurisdiction / scope** — e.g. England and Wales, UK, EU, international law, US, common law, historical.
5. **Cross-references** — internal links to canonical entries.
6. **Source metadata** — source edition and source entry ID.
7. **Review status** — inventory / drafted / legally verified / translation reviewed / final.

## File plan

- `sources/oxford_10e/` — Oxford 10e source inventory and provenance data.
- `lexicon/` — canonical OpenLegalLexicon entries, split by letter.
- Complete Markdown and CSV exports will be produced from the canonical data.

## Development rules

The detailed editorial and implementation baseline is in [`DEVELOPMENT_PLAN.md`](DEVELOPMENT_PLAN.md).

**Do not create GitHub Actions or other automated workflow files unless the repository owner explicitly requests them.**
