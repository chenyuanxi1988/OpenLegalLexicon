# 来源与参考资料

OpenLegalLexicon 分为两个独立词典：美国法律英语主词典和中文法律词典。来源必须与目标法域对应，不能用一个法域的定义替代另一个法域。

## 1. 美国法律英语主词典

目标文件：`lexicon/us_legal_english.csv`

### 首要词典基线：Black's Law Dictionary

美国主词典以后统一以 **Black's Law Dictionary** 作为首要词典基线。用户已经提供该词典并已整理过词目清单；该清单是美国主词典 A → Z 扩展的主工作底稿。

Black's 在项目中的作用：

- 确认英文 headword；
- 区分不同义项；
- 确认词形、缩写、别名和交叉参照；
- 提供美国法律概念的核心边界和传统用法。

项目不会把 Black's 的整段英文释义逐字复制为公开数据。OpenLegalLexicon 基于其词目和概念框架，独立完成中文翻译、中文说明、使用提示、标签、数据编排，并结合现行美国法源作必要核验和更新。

### 美国现行权威法源

Black's 之后，按需要使用以下资料核验当前法律状态、法域和具体规则：

- U.S. Constitution；
- U.S. Code；
- Code of Federal Regulations；
- Federal Rules of Civil Procedure、Federal Rules of Evidence、Federal Rules of Criminal Procedure 等官方规则；
- U.S. Supreme Court 和其他联邦法院公开判决；
- U.S. Courts；
- SEC、FTC、DOJ、EEOC、NLRB、USPTO、Treasury/OFAC、IRS、CBP、USTR 等官方机构；
- 涉及州法时使用相应州法、州法院和州监管来源。

### 当前迁移种子

2026-09-30，从旧词表中筛出 25 条跨境交易实务英文进入主词典，当前仍标记：

- `INTERNATIONAL_TRANSACTIONAL`
- `migration_review`

这些记录属于旧数据迁移种子，后续要重新放回 Black's A–Z 体系中逐条核验。

## 2. 中文法律词典

目标文件：`lexicon/chinese_legal_terms.csv`

旧 `lexicon/legal_terms.csv` 的 392 条中文主词条已完整迁入。中国法概念以中国大陆现行法律法规、司法解释、法院和监管机关公开材料为核心来源；英文只作参考译法。

## 3. Oxford Dictionary of Law 参考索引

`lexicon/oxford_dictionary_of_law_10e_reference.md` 来源于用户提供的 Oxford University Press《A Dictionary of Law》第 10 版（2022），用于候选词发现、比较词形和覆盖缺口检查。

Oxford 是英国法律词典，不作为美国主词典的首要词目或定义基线。需要进入美国主词典的候选，应回到 Black's 和美国现行法源核验。

## 4. 其他专业词典和教材

其他专业法律词典、教材、数据库和用户提供资料可以用于：

- 词形和译法比较；
- 概念辨析；
- 覆盖缺口检查；
- 学习提示和交叉参照研究。

项目公开的数据是独立编审后的词条、翻译、说明、标签和结构，不把第三方词典整段原文当作项目原创内容重新发布。

## 5. 台湾数据

历史台湾司法院及台湾智慧财产局双语参考词表已从仓库删除，并停止作为本项目的数据源和候选词来源。
