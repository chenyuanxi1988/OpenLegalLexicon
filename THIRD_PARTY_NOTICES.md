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

OpenCC supplies character conversion tables; pypinyin supplies pronunciation tables. Automatically produced forms are identified as machine conversions/readings, not verified legal terminology or expert-reviewed pronunciation. This project does not redistribute their source dictionaries; retain their own licenses when redistributing dependencies.
