# 来源与参考资料

OpenLegalLexicon 现在分为两个独立词典：美国法律英语主词典和中国法律中文词典。来源必须与目标法域对应，不能用一个法域的定义替代另一个法域。

## 1. 美国法律英语主词典

目标文件：`lexicon/us_legal_english.csv`

优先依据美国权威法律来源独立编写：

- U.S. Constitution；
- U.S. Code；
- Code of Federal Regulations；
- Federal Rules of Civil Procedure、Federal Rules of Evidence、Federal Rules of Criminal Procedure 等官方规则；
- U.S. Supreme Court 和其他联邦法院公开判决；
- U.S. Courts；
- SEC、FTC、DOJ、EEOC、NLRB、USPTO、Treasury/OFAC、IRS、CBP、USTR 等官方机构；
- 涉及州法时使用相应州法、州法院和州监管来源。

主词典的英文定义、中文辅助说明和编排由项目独立撰写。中文译法仅用于帮助理解，不用于宣称美国法概念与中国法概念完全等同。

## 2. 中国法律中文词典

目标文件：`lexicon/chinese_legal_terms.csv`

优先依据中国大陆现行法律法规、司法解释、法院和监管机关公开材料。中文概念是词条主体，英文只作为参考译法。

## 3. 旧词表

`lexicon/legal_terms.csv` 为项目改向前形成的 392 条混合词表，已冻结为迁移源。

其中中国法条目将迁入中文词典；国际交易英语只有在重新按 English-first 逻辑审核后才能进入美国法律英语主词典。

## 4. Oxford Dictionary of Law 参考索引

`lexicon/oxford_dictionary_of_law_10e_reference.md`

来源于用户提供的 Oxford University Press《A Dictionary of Law》第 10 版（2022）用于候选词发现的索引整理。

该文件不复制整本词典的完整释义。Oxford 内容只用于：

- 发现候选英文法律词；
- 比较词形、交叉参照和缩写；
- 检查词典覆盖缺口。

Oxford 候选词必须再用美国权威法律来源独立核验，不能因为出现在英国法律词典中就直接进入美国法主词典。

## 5. 用户提供的其他专业词典和教材

用户提供的英汉/汉英法律词典、教材、专业数据库材料及其他受版权保护资料，仅用于：

- 候选词发现；
- 概念辨析；
- 译法比较；
- 覆盖缺口检查；
- 误译风险提示。

不整本复制其受版权保护的释义、例句或独创编排。需要进入主词典的内容应重新依据目标法域权威来源独立撰写。

## 6. 台湾数据

历史台湾司法院及台湾智慧财产局双语参考词表已于 2026-09-30 从仓库删除，并停止作为本项目的数据源和候选词来源。
