# Third-party notices

Data providers and data license evidence are listed in `data/sources.json` and `DATA_LICENSE.md`. Generated distributions include a copy of that registry and a source attribution file.

Build tools are installed as separate dependencies, not vendored into this repository:

| Dependency | Pinned version | License / upstream |
| --- | --- | --- |
| pypinyin | 0.55.0 | MIT; https://pypi.org/project/pypinyin/0.55.0/ |
| opencc-python-reimplemented | 0.1.7 | Apache-2.0; https://pypi.org/project/opencc-python-reimplemented/0.1.7/ |
| jsonschema | 4.26.0 | MIT; https://pypi.org/project/jsonschema/4.26.0/ |
| beautifulsoup4 (source updates) | 4.14.3 | MIT; https://pypi.org/project/beautifulsoup4/4.14.3/ |
| PyYAML (format verification) | 6.0.3 | MIT; https://pypi.org/project/PyYAML/6.0.3/ |
| Anki (optional integration verification only) | 26.8.1 | AGPL-3.0-or-later; https://pypi.org/project/anki/26.8.1/ |

OpenCC supplies character conversion tables; pypinyin supplies pronunciation tables. Automatically produced forms are identified as machine conversions/readings, not verified legal terminology or expert-reviewed pronunciation. This project does not redistribute their source dictionaries; retain their own licenses when redistributing dependencies.

Anki is an optional external application backend used only for importer compatibility tests in an isolated collection. It is not bundled into the lexicon data exports or required for ordinary searches/builds.
