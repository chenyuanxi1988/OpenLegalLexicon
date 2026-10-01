# OpenLegalLexicon 开发计划

更新：2026-10-01

## 1. 项目定位

OpenLegalLexicon 的主项目是：

> **English-first, multi-jurisdiction, Chinese-assisted.**

主产品是一部**英文法律词典**，不是“美国法律词典”。英文法律概念、法律短语、程序表达和实务表达是 canonical headword；中文翻译与中文说明只作为理解辅助。

中国大陆法律概念由 `lexicon/chinese_legal_terms.csv` 独立维护，不与英文主词典混成一个法域。

## 2. 两个并列基础词典

### Black's Law Dictionary

用于美国法、美国法律英语和普通法传统中的词目、义项、词形、交叉参照与概念边界。

### Oxford Dictionary of Law (10th ed., 2022)

仓库已经整理 `lexicon/oxford_dictionary_of_law_10e_reference.md`，包含 **4,854 条** A–Z 词目。Oxford 对英国法、欧盟法、国际法、历史术语和普通法表达具有独立价值。

### 关系

Black's 与 Oxford **并列作为英文法律词典的基础词典**。不再采用“Black's 是主基线、Oxford 只是覆盖检查”的旧方向。

每个 headword 允许出现以下情况：

- 仅见于 Black's；
- 仅见于 Oxford；
- 两者均有但义项基本一致；
- 两者均有但美国法/英国法义项不同；
- 同词具有国际法、欧盟法、历史法、拉丁语或实务语境。

不得把这些差异机械合并。

## 3. 主词典

目标文件：`lexicon/english_legal_dictionary.csv`

固定字段围绕以下内容维护：

- 英文词条
- 中文参考译法
- 词性
- 领域
- 适用法域
- 类型
- 英文释义
- 中文辅助说明
- 使用语境
- 同义词或变体
- 常见搭配
- 词典基线（Black's / Oxford / both / legacy）
- 权威来源
- 条目 ID
- 数据许可
- 审核状态

## 4. A–Z 开发顺序

英文词典严格按照 **A → Z** 推进。

统一流程：

1. 读取当前字母段的 Black's 与 Oxford headwords；
2. 统一词形并识别重复 headword；
3. 区分 sense、cross-reference、abbreviation；
4. 判断法域与时代：US / UK / EU / INTERNATIONAL / HISTORICAL / LEGAL-LATIN / 其他；
5. 对两本词典的概念边界进行对照；
6. 编写独立、简洁的英文解释；
7. 编写中文参考译法与中文辅助说明；
8. 对会随法律变化的词条，用相应法域的现行法源校正；
9. 按 A–Z 写入 `english_legal_dictionary.csv`；
10. 同一 headword 的不同法域或不同义项保持相邻。

## 5. 解释原则

英文解释不是简单“美式定义”或“英式定义”，而是根据词条来源和法域分别写清楚：

- US 义项：结合 Black's 与美国现行法源；
- UK 义项：结合 Oxford 与英国现行法源；
- BOTH / COMMON-LAW：说明共同概念和必要差异；
- EU / INTERNATIONAL：按对应制度解释；
- HISTORICAL / LATIN：说明历史来源及现代使用价值。

中文解释只帮助理解，不制造与中国法的虚假等同。

## 6. Oxford 4,854 条的地位

Oxford 4,854 条全部进入正式处理队列，而不是只作为参考索引。

现有 `oxford_dictionary_of_law_10e_reference.md` 继续保留原始 A–Z 顺序、词性、交叉参照和缩写信息。正式词典处理时逐条将其分类为：

- 已进入主词典；
- 与 Black's 合并为同一 headword 的不同 sense；
- UK/EU/International/Historical 独立词条；
- cross-reference / abbreviation；
- 暂缓（需进一步核验）。

## 7. 旧数据

- `lexicon/legal_terms.csv` 冻结，不再新增；
- 392 条旧中文词条已迁入 `chinese_legal_terms.csv`；
- 旧的 `us_legal_english.csv` 改名为 `english_legal_dictionary.csv`，以反映新定位；
- 已迁移的国际交易英语继续保留，但按新的多法域规则复核。

## 8. 质量门槛

每个正式词条至少满足：

- headword 与来源可追溯；
- 英文解释不是来源原文的机械复制；
- 中文译法清楚；
- 法域或历史状态明确；
- 不把 US/UK/EU/国际法不同制度误作同一概念；
- 对现行法律变化敏感的词条完成必要的当前法源核验；
- A–Z 顺序正确；
- 条目 ID 不重复。

## 9. 工程规则

继续执行内容优先原则：

- 不新增 workflow；
- 不新建无必要 branch；
- 不为每几条词建立 PR；
- 不增加复杂测试/报告系统；
- 批量整理、批量校验、少量清晰 commit 直接更新 `main`。

## 10. 当前执行顺序

从 A 段继续，将 Black's 与 Oxford 合并处理，直到 Z：

> **A → B → C → ... → Z**

最终完成标准是：两本基础词典的全部 headword 均已被处理为正式词条、交叉参照、缩写或明确的法域/历史参考记录；未处理队列为 0。
