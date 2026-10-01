# OpenLegalLexicon

**English-first, U.S.-law-first, Chinese-assisted.**

OpenLegalLexicon 的主产品是一部以**美国法律英语**为核心的开放法律词典。英文法律词语、词组、程序表达和实务表达是词条主体；中文翻译和中文注释用于帮助中文使用者理解。中国法律中的中文概念另行维护为独立的中文法律词典，并提供英文参考译法。

## 当前词典

| 文件 | 定位 | 方向 | 当前规模 |
| --- | --- | --- | ---: |
| `lexicon/us_legal_english.csv` | **主词典**：美国法律英语 | English → 中文参考翻译 | **25 条迁移种子** |
| `lexicon/chinese_legal_terms.csv` | 中文法律词典 | 中文 → English reference translation | **392 条迁移记录** |
| `lexicon/legal_terms.csv` | 冻结的旧迁移源 | legacy | **392 条** |

## US Legal English Dictionary

`lexicon/us_legal_english.csv` 是项目以后唯一的美国法律英语主词典和核心进度指标。

基本结构：

> **English headword → Black's Law Dictionary baseline → U.S. legal verification/context → 中文参考翻译与说明**

英文是 canonical headword。中文不是概念来源，只是辅助理解。

### Black's Law Dictionary 基线

美国主词典以后统一以 **Black's Law Dictionary** 作为首要词典基线。用户已经提供该词典，并已经整理过词目清单；后续扩词直接以该清单为主工作底稿，不再由 AI 自行发明词目体系或凭印象补写定义。

具体规则：

1. 先依据 Black's 确认 headword、词形、义项和交叉参照；
2. 再用美国宪法、法典、联邦规则、判例、法院或监管机构资料核验当前法律状态、法域和具体限制；
3. 中文翻译、中文说明、使用提示和数据编排由 OpenLegalLexicon 独立整理；
4. 不把 Black's 的整段原文释义直接复制进公开词典；
5. 如 Black's 与现行法、州法或特定监管规则存在更新差异，以现行权威法源校正并注明；
6. 当前 25 条旧数据迁移种子继续保留 `migration_review`，后续按 Black's 基线逐条重审。

### A–Z 排序

`us_legal_english.csv` 必须始终按 `英文词条` **A → Z** 排列，大小写不影响排序。

- 主体扩词顺序也是 A → Z，而不是按部门法批次随意追加；
- 新词条必须插入正确字母位置；
- 相同 headword 的不同义项相邻排列，再按义项或法域区分；
- 缩写、别名和交叉参照优先参考 Black's 的词条结构。

当前 25 条迁移种子本身已经按 A–Z 排列。

## Chinese Legal Terms Dictionary

`lexicon/chinese_legal_terms.csv` 是中文作为 canonical headword 的独立词典：

> **中文法律词条 → 中国法释义/法源 → English reference translation**

现有 392 条旧中文主词条已经完整迁入。中国法概念以中国现行法律、司法解释、法院和监管资料为依据；英文只作参考译法。不同法域概念不得因为译名相似而自动视为等同。

## 参考资料层级

- **Black's Law Dictionary**：美国主词典的首要词目与概念框架基线；
- **美国现行权威法源**：用于核验、更新、限定法域和具体法律效果；
- `lexicon/oxford_dictionary_of_law_10e_reference.md`：英国法词典候选索引，只作补充覆盖检查，不作为美国主词典定义基线。

项目不是对 Black's 原文的逐字转载，而是以其词目和概念结构为基础，制作独立的英中法律学习词典，包括中文翻译、中文说明、美国法语境核验、标签和编排。

历史台湾司法院及台湾智慧财产局双语数据已从当前仓库删除，并停止作为本项目的数据源和候选词来源。

## 开发规则

1. 美国主词典先核对 Black's，再做中文翻译和美国法语境核验；
2. 主词典按 A → Z 连续推进，不按批次把新词堆到文件尾部；
3. 中国词典与美国词典独立维护；
4. 不因字面相似跨法域合并概念；
5. 不把项目释译冒充官方译文；
6. 除非现有 CSV 已无法维护，否则不新增 workflow、复杂 CI、分支体系或其他外围工程。
