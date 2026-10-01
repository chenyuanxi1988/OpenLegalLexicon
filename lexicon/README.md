# Lexicon

这里存放 OpenLegalLexicon 的英文法律主词典、中国法律中文词典、冻结迁移源和基础词目索引。

## 1. `english_legal_dictionary.csv` — 英文法律主词典

**方向：English → 中文参考译法 + English explanation + 中文说明**

主词典不限定为美国法。Black's Law Dictionary 与 Oxford Dictionary of Law 都是重要基础词典，条目通过 `适用法域` 区分 US、UK、EU、INTERNATIONAL、HISTORICAL、LEGAL-LATIN 等语境。

固定工作流：

> Black's / Oxford headword → sense & jurisdiction → independent English explanation → 中文参考翻译 → 中文辅助说明 → current-law verification where needed → A–Z 写入主词典

### 排序

`english_legal_dictionary.csv` 必须始终按英文 headword **A → Z** 排列；同一 headword 的不同义项或不同法域相邻。

### 词典基线

主词典包含 `词典基线` 字段，用于标明该记录来自或对齐于：

- `BLACK'S`
- `OXFORD`
- `BLACK'S; OXFORD`
- `LEGACY`

来源标签不等于法域标签；法域另由 `适用法域` 说明。

## 2. `oxford_dictionary_of_law_10e_reference.md` — Oxford 词目索引

包含 Oxford Dictionary of Law 第 10 版（2022）识别出的 **4,854 条主词条**，按原书 A–Z 排列，并保留词性、cross-reference、abbreviation/expansion 与 source entry 编号。

该文件是正式基础词目层。所有 Oxford headwords 都需要在主词典建设过程中被处理，而不是只做覆盖检查。

## 3. Black's Law Dictionary

Black's 与 Oxford 并列作为英文法律词典的重要基础来源。Black's 对美国法和美国法律英语尤其重要；Oxford 对英国法、欧盟法和英国普通法语境尤其重要。共同 headword 需要区分不同 sense，不能简单互相覆盖。

## 4. `chinese_legal_terms.csv` — 中国法律中文词典

**方向：中文 → English reference translation**

当前 392 条迁移记录。中文是 canonical headword；英文只作参考译法。

## 5. `legal_terms.csv` — 冻结的旧迁移源

现有 392 条，只用于迁移审计和历史核对，不再新增。

## 已删除数据

台湾参考词表已经删除，不再维护或批量参考。
