# OpenLegalLexicon

**English-first, U.S.-law-first, Chinese-assisted.**

OpenLegalLexicon 的主产品是一部以**美国法律英语**为核心的开放法律词典。英文法律词语、词组、程序表达和实务表达是词条主体；中文翻译和中文注释只用于帮助中文使用者理解，不再把主词典做成“中文法律概念 → 寻找英文译法”的中翻英词库。

中国法律中的中文概念另行维护为独立的中文法律词典，并提供英文参考译法。不同法域的概念不得因为译名相似而自动视为等同。

## 两个独立词典

| 文件 | 定位 | 方向 |
| --- | --- | --- |
| `lexicon/us_legal_english.csv` | **主词典**：美国法律英语 | English → 中文参考翻译 |
| `lexicon/chinese_legal_terms.csv` | 中国法律中文词典 | 中文 → English reference translation |

### 1. US Legal English Dictionary

`lexicon/us_legal_english.csv` 是项目以后唯一的主成果和核心进度指标。

基本结构：

> **English legal term → U.S. legal meaning/context → Chinese reference translation**

英文是 canonical headword。中文不是概念来源，只是辅助理解。词条首先回答“这个词在美国法律、法院、法学院、监管和律师实务中是什么意思、怎样使用”，然后再给中文参考译法。

法域可细分为 `US`、`US-FEDERAL`、具体州法，以及确有必要的 `INTERNATIONAL_TRANSACTIONAL`。跨境交易英语只有在对美国律师实务具有明确价值时才进入主词典。

### 2. Chinese Legal Terms Dictionary

`lexicon/chinese_legal_terms.csv` 单独维护中国法律概念。

基本结构：

> **中文法律词条 → 中国法释义/依据 → 英文参考译法**

例如《民法典》《公司法》《民事诉讼法》《仲裁法》《个人信息保护法》等中国法制度词应进入该词典，而不是作为美国法律英语主词典的基础。

即使两个词典出现相同英文，例如 `contract`、`agency`、`duress`，也不代表两个法域的 record 可以合并。

## 迁移状态

旧文件 `lexicon/legal_terms.csv` 现有 **392 条**，形成于项目改向之前，混合了中国法制度词和国际交易英语。该文件从 2026-09-30 起**冻结为迁移源（legacy migration source）**：

- 不再向其中新增词条；
- 不再把它作为主词典；
- 中国法来源条目迁入 `chinese_legal_terms.csv`；
- 国际交易英语需改写为 English-first 后再进入 `us_legal_english.csv`；
- 像 `contract`、`agency`、`duress` 这类现有释义基于中国法的英文词，不能直接搬入美国词典，必须另以美国法权威来源重新编写。

在迁移完成并复核前，不删除 `legal_terms.csv`，避免历史数据丢失。

## 美国法律英语建设重点

主词典优先覆盖：

- Contracts
- Torts
- Civil Procedure
- Constitutional Law
- Criminal Law
- Criminal Procedure
- Evidence
- Property
- Business Associations / Corporations / Agency
- Securities Regulation
- Bankruptcy
- Intellectual Property
- Antitrust
- Employment & Labor
- Tax
- Administrative / Regulatory Law
- Litigation and transactional drafting
- Legal research, writing, court documents and common abbreviations

目标不是机械堆词，而是建立一套真正适用于**学习和使用美国法律**的法律英语体系。

## 参考资料

专业法律词典、教材和用户提供的资料可以用于发现候选词、比较用法和检查遗漏，但不整本复制受版权保护的释义、例句或独创编排。

`lexicon/oxford_dictionary_of_law_10e_reference.md` 仅作为英文法律词候选索引。Oxford 词条不能因为出现在该索引中就自动进入美国法主词典；必须先判断其是否适用于美国法律，并用美国法权威来源独立编写释义。

台湾双语参考词表已于 2026-09-30 从仓库移除，不再作为本项目的数据源或候选词来源。

## 开发规则

1. **English-first, U.S.-law-first, Chinese-assisted.**
2. 美国词典和中国词典是两个独立产品，不跨法域机械去重。
3. 美国主词典的定义和语境应优先依据美国权威法律来源。
4. 中文翻译以帮助理解为目的，不追求把美国法概念强行套入中国法术语。
5. 中国法概念只在中文词典中依据中国法解释，英文仅作参考翻译。
6. 不再导入台湾词语数据。
7. 除非词表已无法维护，不增加新的 workflow、复杂 CI、分支体系或外围工程；把时间用于内容本身。

历史工程版本仍保存在归档分支：`archive/pre-content-first-simplification-20260928`。
