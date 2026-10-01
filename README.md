# OpenLegalLexicon

**English-first, U.S.-law-first, Chinese-assisted.**

OpenLegalLexicon 的主产品是一部以**美国法律英语**为核心的开放法律词典。英文法律词语、词组、程序表达和实务表达是词条主体；中文翻译和中文注释用于帮助中文使用者理解。中国法律中的中文概念另行维护为独立的中文法律词典，并提供英文参考译法。

## 当前词典

| 文件 | 定位 | 方向 | 当前规模 |
| --- | --- | --- | ---: |
| `lexicon/us_legal_english.csv` | **主词典**：美国法律英语 | English → 中文参考翻译 | **37 条当前记录**（12 条 Black's A 段 + 25 条迁移种子） |
| `lexicon/oxford_dictionary_of_law_10e_reference.md` | **Oxford 英文词目层** | A–Z 英文词目/交叉参照 | **4,854 条** |
| `lexicon/chinese_legal_terms.csv` | 中文法律词典 | 中文 → English reference translation | **392 条迁移记录** |
| `lexicon/legal_terms.csv` | 冻结的旧迁移源 | legacy | **392 条** |

## US Legal English Dictionary

`lexicon/us_legal_english.csv` 是项目的美国法律英语主词典和核心进度指标。

基本结构：

> **English headword → Black's Law Dictionary baseline → U.S. legal verification/context → 中文参考翻译与说明**

英文是 canonical headword。中文不是概念来源，只是辅助理解。

### 两层英文词目来源

项目现在同时使用两层英文词目来源：

1. **Black's Law Dictionary**：美国主词典的首要词目、义项和概念边界基线；
2. **Oxford Dictionary of Law (10th ed., 2022)**：已经整理好的 **4,854 条 A–Z 英文词目层**，从现在起正式进入处理队列，不再只是被动覆盖检查。

Oxford 词目全部保留并参与去重、词形、交叉参照和覆盖检查；但 Oxford 以英国法为主，因此：

- 与美国法重合或在美国实务中成立的词条，回到 Black's 和美国现行法源核验后进入/补强 `us_legal_english.csv`；
- 英国法、欧盟法或其他非美国法特有词可以保留为 `UK_REFERENCE` / 相应参考法域，不计入美国法核心词条；
- 不因 Oxford 收录某个词就自动把它标成美国法；
- 不重复再建一份人工复制的 Oxford 词目文件，直接使用现有 `lexicon/oxford_dictionary_of_law_10e_reference.md` 作为正式 Oxford 词目层。

### Black's Law Dictionary 基线

美国主词典统一以 **Black's Law Dictionary** 作为首要定义与概念边界基线。用户已经提供该词典；后续不由 AI 脱离 Black's 自行发明核心词目体系或凭印象补写定义。

具体规则：

1. 先确认 Oxford/Black's 是否存在对应 headword、词形、义项和交叉参照；
2. 对美国法词条，以 Black's 为首要概念基线；
3. 再用美国宪法、法典、联邦规则、判例、法院或监管机构资料核验当前法律状态、法域和具体限制；
4. 中文翻译、中文说明、使用提示和数据编排由 OpenLegalLexicon 独立整理；
5. 不把第三方词典的整段原文释义直接复制进公开词典；
6. 如词典表述与现行法、州法或特定监管规则存在时间差，以现行权威法源校正并注明。

### A–Z 排序

所有英文词目按 **A → Z** 处理。

- Oxford 4,854 条保留其原书 A–Z 顺序；
- Black's 新增/补充词条也按 A–Z 插入；
- 同一 headword 的不同义项相邻排列，再按义项或法域区分；
- 缩写、别名和交叉参照保留来源关系；
- `us_legal_english.csv` 的正式记录保持 A–Z 有序。

## Chinese Legal Terms Dictionary

`lexicon/chinese_legal_terms.csv` 是中文作为 canonical headword 的独立词典：

> **中文法律词条 → 中国法释义/法源 → English reference translation**

现有 392 条旧中文主词条已经完整迁入。中国法概念以中国现行法律、司法解释、法院和监管资料为依据；英文只作参考译法。不同法域概念不得因为译名相似而自动视为等同。

## 开发规则

1. 英文词目先按 Oxford + Black's A–Z 覆盖整理；
2. 美国法正式释义以 Black's 为首要基线，并由美国现行法源核验；
3. Oxford 特有英国法词条不冒充美国法核心词；
4. 中国词典与美国词典独立维护；
5. 不因字面相似跨法域合并概念；
6. 不把项目释译冒充官方译文；
7. 除非现有数据结构已无法维护，否则不新增 workflow、复杂 CI、分支体系或其他外围工程。

历史台湾司法院及台湾智慧财产局双语数据已从当前仓库删除，并停止作为本项目的数据源和候选词来源。
