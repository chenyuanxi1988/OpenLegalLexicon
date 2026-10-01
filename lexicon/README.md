# Lexicon

这里存放 OpenLegalLexicon 的正式词典、冻结迁移源和英文词目来源层。

## 1. `us_legal_english.csv` — 美国法律英语主词典

**方向：English → 中文参考翻译**

**当前：37 条记录（12 条 Black's A 段 + 25 条迁移种子）。**

英文法律词条是 canonical headword。美国法正式词条以 **Black's Law Dictionary** 作为首要概念基线，并用美国现行法源核验。

### 固定工作流

> Oxford / Black's headword → 去重与法域判断 → Black's 美国法概念基线 → 美国现行法源核验 → 中文参考翻译 + 独立英文解释 + 中文辅助说明 → A–Z 写入主词典

规则：

1. 先核对 Oxford / Black's 的 headword、义项、词形和交叉参照；
2. 对美国法词条，以 Black's 为首要概念基线；
3. 再用美国宪法、法典、联邦规则、判例、法院/监管机构材料或相应州法核验；
4. 不由模型脱离来源自行发明核心定义；
5. 中文翻译、中文说明和项目英文解释是独立编审内容；
6. 不逐字复制第三方词典整段原文释义。

### A–Z 排序规则

`us_legal_english.csv` 必须始终按 `英文词条` **A → Z** 排列。

- 扩词本身也按 A → Z 推进；
- 新词条插入正确字母位置；
- 相同 headword 的不同义项相邻；
- 同一 headword 再按义项、法域或用途区分；
- 缩写、别名和交叉参照保留来源关系。

## 2. `oxford_dictionary_of_law_10e_reference.md` — Oxford 正式英文词目层

**当前：4,854 条主词条，按原书 A–Z 顺序。**

该文件从现在起正式进入英文词典处理流程，不再只是被动的覆盖检查文件。

用途：

- 提供完整的 Oxford A–Z 词目覆盖；
- 提供词性、交叉参照和缩写/展开线索；
- 与 Black's 做 headword / sense / variant 对齐；
- 发现 Black's 之外值得保留的英国法、欧盟法、国际法或历史词汇。

因为 Oxford 以英国法为主，不能把 4,854 条全部直接标成美国法核心词条：

- 与美国法重合的词条，经 Black's 和美国法源核验后进入/补强 `us_legal_english.csv`；
- 英国法特有词保留 `UK_REFERENCE` 或相应法域身份；
- 参考词不计入美国法核心词条数量；
- 不再额外复制一份相同的 Oxford 词目清单，直接维护现有文件。

## 3. `chinese_legal_terms.csv` — 中文法律词典

**方向：中文 → English reference translation**

**当前：392 条迁移记录。**

中文是 canonical headword。中国法记录继续以中国法律依据和中国法语境为核心；英文只作为参考译法，不构成与美国法概念的自动对应。

## 4. `legal_terms.csv` — 冻结的旧迁移源

现有 392 条。该文件不再新增，仅作为迁移审计和历史核对来源保留。392 条已经完整进入 `chinese_legal_terms.csv`；其中 25 条国际交易英语已经整理为 English-first 迁移种子进入 `us_legal_english.csv`。

## 已删除的数据

`taiwan_reference_terms.csv` 已删除。项目以后不再维护或批量参考台湾司法院、台湾智慧财产局等台湾双语词表。
