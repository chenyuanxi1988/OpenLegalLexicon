# 可直接使用的法律词典

这是 **0.1.0.dev5 来源参考版与核心学习版**，由本次构建生成。本构建包含 3,055 条结构化记录、332 条核心学习词条及 6,110 条双向学习记录。项目仍在开发，尚未逐条完成法律译义、法域与读音复核。

| 用途 | 文件 |
| --- | --- |
| 核心学习 | [332 条核心词典 CSV](legal_dictionary_core.csv)、[664 条双向 Anki 记录](anki_core.tsv) |
| 完整来源参考 | [CSV](legal_dictionary.csv)、[TSV](legal_dictionary.tsv)、[Anki](anki.tsv)、[JSONL](lexicon.jsonl) |
| 通用词表 | [中文简体](legal_terms_zh.txt)、[繁体](legal_terms_zh_hant.txt)、[英文](english.txt) |
| Rime 简体 | [词典](openlegal_hans.dict.yaml) + [方案](openlegal_hans.schema.yaml) |
| Rime 繁体 | [词典](openlegal_hant.dict.yaml) + [方案](openlegal_hant.schema.yaml) |
| 追溯 | [法条证据](legal_evidence.json)、[构建清单](build.json)、[摘要](SHA256SUMS.json) |

GitHub 文件页面的 Raw / Download raw file 可直接保存文件。使用说明见[项目主页](https://github.com/chenyuanxi1988/OpenLegalLexicon#使用)和[Anki 导入说明](https://github.com/chenyuanxi1988/OpenLegalLexicon/blob/main/docs/STUDY.md)。

模板、隔离记录和疑似错误译义默认不进入学习与输入法产物。原始来源记录仍保存在项目快照中，待核查结果见[编审队列](https://github.com/chenyuanxi1988/OpenLegalLexicon/blob/main/reports/source-review-queue.json)。下载新版不会自动删除个人 Anki 集合中此前导入的隔离卡片，更新方式见 Anki 导入说明。

来源地区不等于法律适用法域；简繁转换也不改变法域。核心英文 project_authored 是项目释译，source_attributed 是来源原译文，两者均不表示法律专家审核。仅复核分类时不会提升译文审核状态。

转发时保留 [ATTRIBUTION.md](ATTRIBUTION.md)、[DATA_LICENSE.md](DATA_LICENSE.md) 和 [sources.json](sources.json)。英文及 Rime 文件附逐行索引。本页与其他下载文件由构建生成，维护者运行 publish_dictionary.py 和 --check 验证同步，不手工修改生成结果。
