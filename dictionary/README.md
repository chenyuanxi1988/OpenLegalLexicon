# 可直接下载的词典

这里是 **0.1.0.dev2 来源参考版与核心学习版**，由主数据自动生成。尚未逐条完成法律译义、法域与读音复核，不能当作完整成品。

| 用途 | 文件 |
| --- | --- |
| 有释义和法条出处的核心学习 | [99 条核心词典 CSV](legal_dictionary_core.csv)、[198 张 Anki 卡片](anki_core.tsv) |
| 完整参考词对与双向闪卡 | [Anki TSV](anki.tsv)、[结构化 JSONL](lexicon.jsonl)、[法条证据](legal_evidence.json) |
| 学生、教师查阅与筛选 | [Excel 等软件使用的 CSV](legal_dictionary.csv)、[通用 TSV](legal_dictionary.tsv) |
| 软件词表、搜索和文本处理 | [中文简体](legal_terms_zh.txt)、[繁体](legal_terms_zh_hant.txt)、[英文](english.txt) |
| Rime 简体拼音 | [词典](openlegal_hans.dict.yaml) + [方案](openlegal_hans.schema.yaml) |
| Rime 繁体拼音 | [词典](openlegal_hant.dict.yaml) + [方案](openlegal_hant.schema.yaml) |

在文件页面选择 Raw / Download raw file 即可保存，不需要安装 Python。Rime 用法见[主页](../README.md)。搜狗的私有细胞词库格式尚未验证；不要把文本改扩展名为 .scel 后尝试安装。

表格保留来源对应的原文，含语境、审核状态及稳定 ID。所有“待核查”值都是实际缺口。来源机构在台湾不等于概念适用法域为台湾；简体转换不等于中国大陆术语。许可及署名必须随转发保留：[ATTRIBUTION.md](ATTRIBUTION.md)、[DATA_LICENSE.md](DATA_LICENSE.md)、[sources.json](sources.json)。

同目录还保存输入法和英文词表的逐行索引，以及 SHA256SUMS.json 校验摘要。核心版英文为项目释译（project_authored），与官方来源原译文（source_attributed）分别标记。Anki 用法见[学习导入](../docs/STUDY.md)。维护者用 `python tools/publish_dictionary.py` 更新本目录；main 的自动测试通过后，CI 会提交生成文件，保持下载版与源数据同步。拉取请求只做验证，不写入仓库。不要手动编辑生成文件。
