# OpenLegalLexicon

可追溯的中英文法律词汇，面向学习、检索、中文输入法和后续语音输入集成。

Traceable Chinese–English legal terminology for study, search and input methods.

**开发中：0.1.0.dev1。** 当前有可运行的数据管线和词库，尚未完成全领域、全法域覆盖与逐条法律译义复核。完成状态和续作入口见 [PROGRESS.md](PROGRESS.md)，每步记录见 [WORK_LOG.md](WORK_LOG.md)。

## 现在包含什么

| 内容 | 当前结果 |
| --- | --- |
| 官方来源快照 | 司法院双语词汇 2,121 行；智慧财产局商标词表 613 行 |
| 结构化词条 | 2,730 条来源对应；同一来源 4 行经空白规范化后相同的词对合并并保留所有原始行号 |
| 字段 | 原文、简繁体、英文、拼音、来源、许可、语境、分类依据、法域审核状态 |
| 检索 | 中文、英文、拼音、ID，以及领域、来源地区、已核验法域筛选 |
| 导出 | JSONL、TSV、双向 Anki TSV、英文候选词表、简体和繁体 Rime 词典及独立方案 |
| 追溯 | 每份构建附来源与许可、导出行到词条的映射、构建配置、SHA-256 摘要 |

两家提供机构都位于台湾，词表中同时含本地、外国、国际制度与历史名称。`source_origin=TW` 仅表示来源地区，**不表示术语都适用于台湾，更不表示简体转换后就适用于中国大陆**。未经查证的 `jurisdictions` 留空。原词对是来源中的译文对应，不冒充跨法域的严格等义概念。

模板、占位符和隔离条目不进入默认学习/输入法输出。输入法还排除多项中文、附注及过长标签。拼音、简体及部分分类由程序生成，状态明确记录；尚不能声称已经由法律专家逐条审核。

## 使用

无需安装开发环境：[直接下载词典、中文/英文词表和 Rime 文件](dictionary/README.md)。当前为来源参考版，适用范围与未完成核验项目见该目录说明。

以下步骤供开发者或希望自行筛选和构建的使用者：

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

当前默认构建产生 2,725 条可展示词条、5,450 张双向学习记录、2,504 项英文候选，以及简繁各 2,410 行 Rime 词典。筛选后数量会变化；完整审计数据仍保留全部原始记录。词条数、译法数、输入法行数和卡片数分别统计，不能互相当作词库规模。

### 输入法

`openlegal_hans.dict.yaml` 配合 `openlegal_hans.schema.yaml`，或繁体 `hant` 对应文件。把选择的两份文件及署名、数据许可文件放入 Rime 用户资料目录，在方案列表加入 `openlegal_hans` 或 `openlegal_hant`，重新部署后选择“法律词汇”。输入完整拼音查词，音节可用单引号分隔；空格用于选择候选。

如需并入既有全拼方案，使用 `import_tables` 引入相应词典，并在修改自己的方案前保留原配置。本项目权重统一为 1，仅表示初始权重，不是语料词频，也不承诺可直接导入搜狗等私有二进制格式。

### 学习

`anki.tsv` 含稳定 ID、问题、答案、语境、学习注释、来源、标签。按 [学习导入说明](docs/STUDY.md) 建立一次笔记类型后导入；两种方向各一条记录，重复导入依据 ID 更新。原译文中的并列项保持在一张卡内，不擅自拆成等义术语。

## 数据与许可

代码和原创文档采用 [MIT](LICENSE)；第三方数据保留 **OGDL-Taiwan-1.0**，原创数据注释与编排采用 **CC BY 4.0**。详见 [DATA_LICENSE.md](DATA_LICENSE.md)。使用或转发构建结果时，保留其中的 `ATTRIBUTION.md`、`sources.json` 和数据许可文件。

原始数据许可证据、来源摘要均已保存。香港律政司词表当前未导入，理由见 [来源审查](docs/SOURCE_REVIEW.md)。

## 开发与贡献

```sh
python -m unittest discover -s tests -v
oll report --out build/quality.json
```

运行真实输入法检查需要 librime 开发库与 `rime_deployer`，见 [验证说明](docs/VALIDATION.md)。字段规则见 [数据结构](docs/DATA_MODEL.md)，贡献与更新流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。

下一阶段继续补充中国大陆等法域的来源证据、领域分类和学习注释，并核验 Qwen3-ASR 适配及语音评测；这些工作尚未完成，详见 [开发计划](DEVELOPMENT_PLAN.md)。
