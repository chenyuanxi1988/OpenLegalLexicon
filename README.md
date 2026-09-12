# OpenLegalLexicon

可追溯的中英文法律词汇，面向学习、检索、中文输入法和后续语音输入集成。

Traceable Chinese–English legal terminology for study, search and input methods.

**开发中：0.1.0.dev3。** 当前已有可运行、可验证、可直接下载的数据管线和词库；中国大陆核心学习层已完成四批：民商/数据/竞争/知识产权、行政/劳动、税务/贸易、刑事。下一阶段重点是来源参考层逐条编审，之后再进入私有词库叠加和 Qwen3-ASR/真实音频评测。完成状态和续作入口见 [PROGRESS.md](PROGRESS.md)，每步记录见 [WORK_LOG.md](WORK_LOG.md)。

## 现在包含什么

| 内容 | 当前结果 |
| --- | --- |
| 官方来源快照 | 司法院双语词汇 2,121 行；智慧财产局商标词表 613 行 |
| 结构化记录 | 共 2,948 条：2,730 条来源对应 + 218 条有法条证据的项目释义；其中 5 条模板/占位来源记录默认不展示，因此默认构建为 2,943 条 |
| 核心学习层 | 218 条中文释义、学习提示、英文项目释译及译法说明；覆盖民法典、公司法、个人信息保护法、反垄断法、著作权法、行政处罚法、行政复议法、劳动合同法、增值税法、关税法、对外贸易法及包含刑法修正案（十二）的现行刑法 |
| 字段 | 原文、简繁体、英文、拼音、来源、许可、语境、释义、译法说明、法条证据、关系、法域及审核状态 |
| 检索 | 中文、英文、拼音、ID，以及领域、来源地区、已核验法域筛选 |
| 导出 | JSONL、TSV、双向 Anki TSV、核心学习 CSV/Anki、英文候选词表、简体和繁体 Rime 词典及独立方案 |
| 追溯 | 每份构建附来源与许可、导出行到词条的映射、构建配置、SHA-256 摘要 |
| 最新远端验证 | GitHub Actions 34668084340：Python 3.10/3.12、单测、构建、真实 Rime、真实 Anki 与下载发布全部成功；自动下载提交 `21d9bce79724d6637c37a1816ff916a95cb640f7` 已进入 `main` |

两家第三方提供机构都位于台湾，词表中同时含本地、外国、国际制度与历史名称。`source_origin=TW` 仅表示来源地区，**不表示术语都适用于台湾，更不表示简体转换后就适用于中国大陆**。未经查证的 `jurisdictions` 留空。原词对是来源中的译文对应，不冒充跨法域的严格等义概念。

中国大陆核心学习层是 OpenLegalLexicon 原创编写层：中文释义、学习提示和英文均逐条关联具体法律条文，英文状态为 `project_authored`，不是官方正式译文；AI 辅助编辑、机器简繁转换和机器读音均明确标示，也不冒充人工法律专家审核。

第三批税务/贸易层特别区分增值税零税率与免税、税率与征收率、关税纳税人与扣缴义务人、四类进口税率以及反倾销/反补贴/保障措施。第四批刑事层使用包含刑法修正案（十二）的现行合并文本，覆盖罪刑法定、故意/过失、正当防卫、共同犯罪、单位犯罪、自首、立功、缓刑、追诉时效，并单独收录修正案（十二）涉及的公司治理和行贿重点。刑法抓取器同时修复了“第十七条之一”等插入条款可能污染前一基础条文的问题。

模板、占位符和隔离条目不进入默认学习/输入法输出。输入法还排除多项中文、附注及过长标签。拼音、简体及部分来源参考层分类由程序生成，状态明确记录。

## 使用

学生和教师可先下载 [核心学习词典 CSV](dictionary/legal_dictionary_core.csv) 或 [核心 Anki 闪卡](dictionary/anki_core.tsv)。完整来源参考版与输入法文件见 [dictionary/](dictionary/README.md)。

按主题或法域查询时，可以增加 `--profile learning`，仅选择有释义和法条证据的词条。例如：

```sh
oll search 行政复议 --profile learning --jurisdiction CN
oll search 竞业限制 --profile learning --domain employment
oll search 反倾销 --profile learning --domain trade
oll search 自首 --profile learning --domain criminal
oll build --profile learning --out build/core-study
```

核心层来源地区 `INTERNATIONAL` 表示项目编写层，适用法域 `CN` 表示中国大陆法律语境。具体法条版本与出处见 [编审与证据](docs/EDITORIAL.md)；领域来源基线见 [中国大陆领域来源基线](docs/CN_DOMAIN_SOURCE_BASELINE_2026-09-12.md)。

无需安装开发环境：[直接下载词典、中文/英文词表和 Rime 文件](dictionary/README.md)。以下步骤供开发者或希望自行筛选和构建的使用者。

需要 Python 3.10 或更新版本。在本仓库目录内：

```sh
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
oll validate
oll search 律师
oll search "trademark" --domain intellectual_property
oll search "xing zheng" --origin TW
oll build --out build/local-1
```

查询和构建使用仓库内的已存快照，安装依赖后可离线运行。从其他目录运行时传入 `oll --root /path/to/OpenLegalLexicon ...`。每次构建使用新的输出目录，避免覆盖已有产物。

最新自动发布构建（`dictionary/build.json`，0.1.0.dev3）包含 **2,943 条默认展示记录、218 条核心学习词条、5,886 条双向学习记录、2,715 项英文候选、简繁各 2,610 行 Rime 词典**。筛选后数量会变化；总结构化记录为 2,948 条，其中 5 条模板/占位来源记录默认排除。词条数、译法数、输入法行数和卡片数分别统计，不能互相当作词库规模。

### 输入法

`openlegal_hans.dict.yaml` 配合 `openlegal_hans.schema.yaml`，或繁体 `hant` 对应文件。把选择的两份文件及署名、数据许可文件放入 Rime 用户资料目录，在方案列表加入 `openlegal_hans` 或 `openlegal_hant`，重新部署后选择“法律词汇”。输入完整拼音查词，音节可用单引号分隔；空格用于选择候选。

如需并入既有全拼方案，使用 `import_tables` 引入相应词典，并在修改自己的方案前保留原配置。本项目权重统一为 1，仅表示初始权重，不是语料词频，也不承诺可直接导入搜狗等私有二进制格式。

### 学习

`anki.tsv` 含稳定 ID、问题、答案、语境、学习注释、来源、标签。按 [学习导入说明](docs/STUDY.md) 建立一次笔记类型后导入；两种方向各一条记录，重复导入依据 ID 更新。`anki_core.tsv` 仅含证据型核心学习层。远端 CI 使用 Anki 26.8.1 官方核心在隔离集合中实际执行导入与重复导入检查。

## 数据与许可

代码和原创文档采用 [MIT](LICENSE)；第三方数据保留 **OGDL-Taiwan-1.0**，原创数据注释、释义、项目英文释译与编排采用 **CC BY 4.0**。详见 [DATA_LICENSE.md](DATA_LICENSE.md)。使用或转发构建结果时，保留其中的 `ATTRIBUTION.md`、`sources.json` 和数据许可文件。

原始数据许可证据、来源摘要均已保存。香港律政司词表当前未导入，理由见 [来源审查](docs/SOURCE_REVIEW.md)。中国大陆法律证据层只保留用于逐条核验的法律文本、版本和摘要；不复制第三方英文译文，也不把整个政府网页视为可自由再分发内容。

## 开发与贡献

```sh
python -m unittest discover -s tests -v
oll report --out build/quality.json
```

运行真实输入法检查需要 librime 开发库与 `rime_deployer`，见 [验证说明](docs/VALIDATION.md)。字段规则见 [数据结构](docs/DATA_MODEL.md)，贡献与更新流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

当前开发顺序是：**先对 2,730 条来源参考层按高频、核心领域和同形异义风险逐批编审**；随后实现私有词库叠加与 Qwen3-ASR/真实音频评测；最后执行完整发布审计。每个阶段均要求远端 CI、真实 Anki/Rime 验证和下载版发布闭环，详见 [PROGRESS.md](PROGRESS.md) 与 [开发计划](DEVELOPMENT_PLAN.md)。
