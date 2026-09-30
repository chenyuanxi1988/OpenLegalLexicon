# OpenLegalLexicon 开发计划

更新：2026-09-30

## 1. 项目方向

OpenLegalLexicon 从 2026-09-30 起正式调整为：

> **English-first, U.S.-law-first, Chinese-assisted.**

项目主目标是建立一部用于**学习和使用美国法律**的法律英语词典，而不是把中国法律概念翻译成英文。

主词典的逻辑：

> English legal term → U.S. legal meaning/context → 中文参考翻译

中国法律概念另建中文词典：

> 中文法律词条 → 中国法释义/依据 → English reference translation

两个词典是独立产品，不因英文或中文译名相似而合并 record。

## 2. 两个正式词典

### A. `lexicon/us_legal_english.csv` — 主词典

这是 OpenLegalLexicon 的核心产品，也是以后唯一用于衡量主项目进度的词典。

基本字段：

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
- 权威来源
- 条目 ID
- 数据许可
- 审核状态

核心原则：

1. 英文词条是 canonical headword。
2. 先确定美国法含义，再考虑中文怎么帮助理解。
3. 中文译名不是用来证明其与某个中国法概念完全等同。
4. 释义应尽量依据美国宪法、法典、规则、法院、监管机关和其他权威美国法律来源独立撰写。
5. 需要时标记 `US-FEDERAL`、具体州法或其他明确法域。
6. 国际交易英语只有在美国律师实务中具有稳定价值时才纳入，并标为 `INTERNATIONAL_TRANSACTIONAL` 或相应语境。

### B. `lexicon/chinese_legal_terms.csv` — 中国法律中文词典

这个词典专门维护中国法概念。

基本字段：

- 中文词条
- 繁體
- 拼音
- 领域
- 适用法域
- 类型
- 中文释义
- 英文参考译法
- 译法说明
- 法律依据
- 使用语境
- 条目 ID
- 数据许可
- 审核状态

中国词典应以中国法律制度本身为中心，英文只作为参考翻译，不承担把中国制度“转化”为美国法概念的功能。

## 3. 旧 392 条的迁移规则

`lexicon/legal_terms.csv` 当前 392 条是旧架构下的混合数据。从本次改向开始冻结，不再新增。

迁移按以下规则进行：

### 第一类：中国法来源条目

凡释义、法域或法律依据明确来自中国大陆法律法规、司法规则或监管规则的条目，迁入 `chinese_legal_terms.csv`。

例如中国《民法典》中的合同、要约、情势变更，中国《公司法》中的实际控制人、股东失权，中国程序法中的再审、执行、保全等，都属于中文词典。

### 第二类：国际交易/律师实务英语

如 `due diligence`、`term sheet`、`closing`、`representations and warranties`、`material adverse change`、`virtual data room` 等，可以成为美国法律英语主词典候选。

但迁移时必须重排为 English-first，并检查其在美国交易实务中的自然度、含义和使用范围；不能仅把旧 CSV 的中英文列对调。

### 第三类：英文词本身常见，但旧释义依据中国法

例如 `contract`、`agency`、`duress`、`counterclaim`、`copyright` 等。

这类旧记录留在中国词典；美国词典需另外创建同名英文 headword，并依据美国法重新撰写定义、语境和 authority。两个 record 不合并。

在 392 条全部完成分类、改写和复核前，不删除旧 `legal_terms.csv`。

## 4. 美国主词典的内容体系

优先按美国法律学习与执业体系扩展：

1. Contracts
2. Torts
3. Civil Procedure
4. Constitutional Law
5. Criminal Law
6. Criminal Procedure
7. Evidence
8. Property
9. Business Associations
10. Agency
11. Corporations and Corporate Governance
12. Securities Regulation and Capital Markets
13. Bankruptcy and Restructuring
14. Intellectual Property
15. Antitrust
16. Employment and Labor
17. Tax
18. Administrative and Regulatory Law
19. Privacy, Cybersecurity and AI
20. Banking, Finance and Secured Transactions
21. Litigation, arbitration and enforcement
22. M&A / PE / VC / transactional drafting
23. Legal research and writing
24. Court documents, deal documents, abbreviations and professional phrases

## 5. 建设阶段

### Phase 0 — 架构切换

- 建立 `us_legal_english.csv`；
- 建立 `chinese_legal_terms.csv`；
- 冻结旧 `legal_terms.csv`；
- 删除台湾参考词表；
- 重写 README、来源和许可说明。

### Phase 1 — 迁移旧 392 条

逐条分流，不做机械复制。

验收标准：

- 旧 392 条全部有明确去向；
- 没有把中国法释义伪装成美国法释义；
- 国际交易英语完成 English-first 改写；
- 中国法条目保留可核查的中国法律依据。

### Phase 2 — 美国法基础词群

优先建设法学院与 NY Bar 高频体系：Contracts、Torts、Civil Procedure、Constitutional Law、Criminal Law/Procedure、Evidence、Property、Business Associations。

先形成约 1,500 条高质量美国法核心词和词组。

### Phase 3 — 执业与商事扩展

扩展 Securities、M&A/PE/VC、Banking/Finance、Bankruptcy、IP、Antitrust、Employment、Tax、Privacy/Cyber/AI、Regulatory。

目标约 3,500–5,000 条。

### Phase 4 — Professional-Ready

继续扩展至 8,000+ 高质量英文主词条，并使用美国法律教材、司法材料、法院文书、交易文件和监管材料做覆盖审计。

数量只是门槛，最终要求是：

- 高频美国法律英语覆盖充分；
- 美国法定义和语境可靠；
- 中文辅助翻译自然但不制造跨法域等同；
- 法学院学习、NY Bar、法律研究和律师实务中的常用表达可查。

## 6. 来源优先级

美国主词典优先使用：

- U.S. Constitution；
- U.S. Code、CFR 及官方 federal rules；
- U.S. Supreme Court 和联邦法院公开判决；
- U.S. Courts；
- SEC、FTC、DOJ、EEOC、NLRB、USPTO、Treasury/OFAC、IRS、CBP、USTR 等官方机构；
- 州法、州法院和州监管来源（涉及州法时）；
- 其他可靠的美国法律权威材料。

专业法律词典、教材、Restatements、专业数据库和用户提供资料可以用于候选词发现和概念核对，但受版权保护内容不整段复制，定义由项目独立撰写。

中国词典继续优先使用中国大陆现行法律法规、司法解释、法院和监管机关公开材料。

## 7. Oxford 词典索引的角色

`lexicon/oxford_dictionary_of_law_10e_reference.md` 仅用于：

- 发现英文法律词候选；
- 发现同义词、缩写和交叉参照；
- 检查主词典覆盖缺口。

它不是美国法词典本身。每个 Oxford 候选词进入美国主词典前都必须经过美国法适用性判断和美国权威来源复核。

## 8. 台湾数据

台湾司法院、台湾智慧财产局等历史双语参考词表从本项目移除。

以后：

- 不保留台湾双语词库文件；
- 不以台湾译法作为批量候选来源；
- 不把台湾词条纳入美国词典或中国大陆中文词典；
- 如个别术语恰好由其他美国或中国大陆权威来源独立收录，不因历史台湾来源而排除，但必须重新依据当前目标法域独立编审。

## 9. 工程冻结规则

除非 CSV 已无法继续维护，否则不再开发新的 workflow、复杂 GitHub Actions、新分支体系、overlay、CLI、测试框架或报告系统。

每轮工作的优先顺序始终是：**选词 → 权威核对 → 独立释义 → 中文辅助翻译 → 去重 → 审核 → 入库。**
