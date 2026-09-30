# OpenLegalLexicon

**English-first, U.S.-law-first, Chinese-assisted.**

OpenLegalLexicon 的主产品是一部以**美国法律英语**为核心的开放法律词典。英文法律词语、词组、程序表达和实务表达是词条主体；中文翻译和中文注释只用于帮助中文使用者理解，不再把主词典做成“中文法律概念 → 寻找英文译法”的中翻英词库。

中国法律中的中文概念另行维护为独立的中文法律词典，并提供英文参考译法。不同法域的概念不得因为译名相似而自动视为等同。

## 当前词典

| 文件 | 定位 | 方向 | 当前规模 |
| --- | --- | --- | ---: |
| `lexicon/us_legal_english.csv` | **主词典**：美国法律英语 | English → 中文参考翻译 | **25 条迁移种子** |
| `lexicon/chinese_legal_terms.csv` | 中文法律词典 | 中文 → English reference translation | **392 条迁移记录** |
| `lexicon/legal_terms.csv` | 冻结的旧迁移源 | legacy | **392 条** |

### US Legal English Dictionary

`lexicon/us_legal_english.csv` 是项目以后唯一的主成果和核心进度指标。

基本结构：

> **English legal term → U.S. legal meaning/context → Chinese reference translation**

英文是 canonical headword。中文不是概念来源，只是辅助理解。词条首先回答“这个词在美国法律、法院、法学院、监管和律师实务中是什么意思、怎样使用”，然后再给中文参考译法。

本轮先从旧词表中迁移了 **25 条国际交易英语**，例如 `closing`、`due diligence`、`term sheet`、`representations and warranties`、`material adverse change (MAC)` 等。它们全部标记为 `INTERNATIONAL_TRANSACTIONAL` 和 `migration_review`，只是 English-first 的迁移种子，**尚不能视为已经完成美国法权威来源复核**。

后续只有在依据美国法或美国律师实务权威来源完成独立核验后，才升级为正式已审核的美国法律英语词条。

### Chinese Legal Terms Dictionary

`lexicon/chinese_legal_terms.csv` 是中文作为 canonical headword 的独立词典。

基本结构：

> **中文法律词条 → 中文法域/制度语境 → English reference translation**

本轮为避免旧数据在改向时丢失，已把旧 `legal_terms.csv` 的 **392 条中文主词条全部迁入**。其中绝大多数是中国大陆法律制度词，也包含少量跨境交易中的中文实务表达，保留它们是为了中文检索和双向查找，不代表这些概念属于中国法法定术语。

中国法概念仍应以中国现行法律、司法解释和监管资料为依据；英文只作参考译法。

## 跨法域原则

两个词典独立维护。

例如旧词表中的 `合同 → contract`、`代理 → agency`、`胁迫 → duress`、`反诉 → counterclaim`、`要约 → offer` 都是按中国法语境编写的记录。它们已经保留在中文词典中，但**不会因为英文词形相同就直接搬进美国法律英语主词典**。

美国词典中的 `contract`、`agency`、`duress`、`counterclaim`、`offer` 等以后必须重新依据美国法权威来源独立编写。

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

`lexicon/oxford_dictionary_of_law_10e_reference.md` 仅作为英文候选词索引。Oxford 是英国法律词典，出现于该索引的词条必须重新判断是否适用于美国法，并以美国权威来源独立核验后才进入主词典。

历史台湾司法院及台湾智慧财产局双语数据已从当前仓库删除，并停止作为本项目的数据源和候选词来源。

## 开发规则

今后优先投入词条内容本身：

1. 先确认目标法域；
2. 美国主词典先核对美国法含义，再写中文辅助翻译；
3. 中文词典先核对中文概念和法源，再给英文参考译法；
4. 不因字面相似跨法域合并概念；
5. 不把项目释译冒充官方译文；
6. 不整本复制受版权保护的词典内容；
7. 除非现有 CSV 已经无法维护，否则不新增 workflow、复杂 CI、分支体系或其他外围工程。
