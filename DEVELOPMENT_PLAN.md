# OpenLegalLexicon 开发计划

更新：2026-09-30

## 1. 项目方向

OpenLegalLexicon 的主项目是：

> **English-first, U.S.-law-first, Chinese-assisted.**

主词典用于学习和使用美国法律英语。英文法律概念是词条主体，中文翻译和中文注释仅作辅助理解。

中国法律概念另由中文词典维护：

> 中文法律词条 → 中国法释义/依据 → English reference translation

两个词典相互独立，不因译名相似而合并概念。

## 2. 正式词典

### A. `lexicon/us_legal_english.csv`

这是核心产品，也是以后唯一用于衡量主项目进度的词典。

核心原则：

1. 英文词条是 canonical headword；
2. 先确定美国法含义和使用语境，再提供中文参考翻译；
3. 优先使用美国宪法、法典、联邦规则、法院和监管机构等权威来源；
4. 涉及州法时明确州法标签；
5. 国际交易表达可标记 `INTERNATIONAL_TRANSACTIONAL`，但不得因此冒充已经完成美国法审核；
6. 中国法语境下已有的同形英文词不得机械迁入。

当前已有 **25 条迁移种子**，全部来自旧词表中的国际交易实务表达，统一标记为 `migration_review`。下一步应逐条补充美国法或美国交易实务权威来源。

### B. `lexicon/chinese_legal_terms.csv`

这是中文 canonical headword 的独立词典。

当前已将旧词表 **392/392 条中文主词条完整迁入**。绝大多数是中国大陆法律制度词，另有少量跨境交易中文实务表达作为中文检索词保留。

当前为避免信息损失，暂时沿用旧词表的 17 字段结构。后续只有在确认不会丢失来源、注释、审核和法源信息时才考虑 schema 简化。

## 3. 旧词表状态

`lexicon/legal_terms.csv` 已冻结为迁移审计源：

- 不再新增；
- 392 条已全部进入中文词典；
- 其中 25 条国际交易英语已重新整理为 English-first 记录进入美国主词典；
- 暂时保留旧文件用于迁移完整性核验。

## 4. 美国法律英语覆盖方向

主词典优先形成以下体系：

1. Contracts
2. Torts
3. Civil Procedure
4. Constitutional Law
5. Criminal Law
6. Criminal Procedure
7. Evidence
8. Property
9. Business Associations / Corporations / Agency
10. Securities Regulation
11. Bankruptcy
12. Intellectual Property
13. Antitrust
14. Employment & Labor
15. Tax
16. Administrative / Regulatory Law
17. Litigation practice and court documents
18. Transactional drafting
19. Legal research and writing
20. Common abbreviations, procedural verbs and fixed legal phrases

## 5. 内容开发顺序

下一阶段不再围绕中国法领域扩充美国主词典，而按美国法学习体系推进。

建议顺序：

### 第一批：基础高频体系

- Contracts
- Torts
- Civil Procedure
- Evidence
- Criminal Law / Criminal Procedure
- Constitutional Law
- Property

重点优先覆盖法学院、Bar Exam、法院文件和律师写作中反复出现的术语与固定搭配。

### 第二批：商事与律师实务

- Agency / Partnerships / Corporations / LLCs
- Securities
- Bankruptcy
- M&A / financing / commercial agreements
- Legal due diligence and transactional drafting

### 第三批：专业领域

- IP
- Antitrust
- Employment & Labor
- Tax
- Administrative / Regulatory Law
- Privacy / cybersecurity / AI
- Sanctions / export controls / international trade

## 6. 质量门槛

美国主词典每个正式审核词条应尽量满足：

- 英文 headword 自然、常用；
- 法域明确；
- 英文定义以美国法语境为基础；
- 中文翻译只是辅助，不制造虚假对应；
- 对容易与中国法混淆的词写明差异；
- 有必要时记录同义词、变体和常见搭配；
- 权威来源可追溯；
- 不把英国法专有制度未经核验直接纳入美国主词典。

中国词典则以中文概念、中文法源和中文释义准确性为首要标准。

## 7. Oxford 参考索引

`lexicon/oxford_dictionary_of_law_10e_reference.md` 只用于候选词发现和覆盖检查。

Oxford 是英国法律词典，其 headwords 不等于美国法核心词。导入流程必须是：

> Oxford candidate → 判断美国法相关性 → 查美国权威来源 → 独立撰写英文释义 → 中文辅助翻译 → 加入主词典

不得把 4,854 个 Oxford 词条机械批量加入美国主词典。

## 8. 工程冻结规则

除非 CSV 已经无法继续维护，否则不再开发：

- 新 workflow；
- 复杂 GitHub Actions；
- 新分支体系；
- 新测试框架；
- 新报告系统；
- 与词条内容无关的外围工程。

每轮内容工作应尽量批量准备、统一审核，并以少量清晰 commit 提交。

## 9. 当前下一步

1. 对 25 条 `migration_review` 国际交易词补充美国交易实务/美国法来源；
2. 从 Contracts、Civil Procedure、Evidence 等美国法基础领域开始建立第一批真正的 `US` / `US-FEDERAL` 词条；
3. 使用 Oxford 和其他词典只做候选发现，不直接复制释义；
4. 保持中文词典与美国主词典独立扩展。
