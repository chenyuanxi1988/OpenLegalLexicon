# OpenLegalLexicon

**English-first, multi-jurisdiction, Chinese-assisted.**

OpenLegalLexicon 的主产品是一部**英文法律词典**。英文法律词语、词组、程序表达和实务表达是词条主体；中文翻译和中文说明用于辅助中文使用者理解。项目不再把主词典限定为“美国法律词典”。

## 当前结构

| 文件 | 定位 |
| --- | --- |
| `lexicon/english_legal_dictionary.csv` | **英文法律主词典**：English → 中文参考翻译 + English explanation + 中文说明 |
| `lexicon/oxford_dictionary_of_law_10e_reference.md` | Oxford 10e 的 4,854 条 A–Z 词目索引 |
| `lexicon/chinese_legal_terms.csv` | 中国法律中文词典：中文 → English reference translation |
| `lexicon/legal_terms.csv` | 冻结的旧迁移源 |

## 英文法律词典的两大基础词典

### Black's Law Dictionary

Black's 是美国法、美国法律英语和普通法传统的重要基础词典。它用于确认美国法语境中的 headword、sense、词形、交叉参照和概念边界。

### Oxford Dictionary of Law

Oxford 同样是主词典的重要基础来源，而不是次要补充。仓库已经整理出第 10 版（2022）的 **4,854 条** A–Z 词目。Oxford 主要反映英国法，同时包含欧盟法、国际法、历史术语和普通法表达。

### 核心原则

Black's 与 Oxford **并列作为英文法律词典的基础词目与概念来源**，但各自保留法域信息：

- Black's 不等于“所有词都是美国专属”；
- Oxford 不等于“所有词都是英国专属”；
- 同一 headword 可同时存在美国法、英国法、国际法或历史义项；
- 不因为译名相似就把不同法域的法律概念强行合并；
- 对现行法律效果，由相应法域的成文法、规则、判例、法院或监管机构资料校正。

主词典的目标流程是：

> **English headword → Black's / Oxford sense → jurisdiction → independent English explanation → 中文参考翻译 → 中文辅助说明 → current-law verification where needed**

## A–Z 排序

英文主词典始终按英文 headword **A → Z** 排列。Black's 和 Oxford 的词目统一进入同一 A–Z 工作队列；同一 headword 的不同义项相邻，并通过法域和 sense 区分。

## 中国法律中文词典

`lexicon/chinese_legal_terms.csv` 独立维护中国大陆法律概念。中文是 canonical headword，英文只作参考译法。它与英文法律主词典不互相替代。

## 开发规则

1. Black's 与 Oxford 都是主基础词典，不设“Black's 主、Oxford 次”的固定等级；
2. 英文词条按 A–Z 连续推进；
3. 每个正式词条尽量写明法域；
4. 英文解释应是 OpenLegalLexicon 的独立编审表达，而不是机械复制来源原文；
5. 中文翻译和中文说明只用于辅助理解；
6. 历史术语、拉丁语、英国法特有词、美国法特有词都可收录，只要正确标注法域/时代；
7. 不新增无必要的 workflow、branch、PR 或外围工程；内容更新尽量批量整理后直接提交 `main`。

历史台湾双语数据已经删除，不再作为项目来源。
