# Lexicon

这里存放 OpenLegalLexicon 的词典数据和参考索引。

## 1. `us_legal_english.csv` — 主词典

**方向：English → 中文参考翻译**

这是 OpenLegalLexicon 从 2026-09-30 起的核心产品。

英文法律词条是 canonical headword。词条应首先说明其在美国法律中的含义、法域和使用语境，再提供中文参考翻译和中文辅助说明。

推荐法域标签包括：

- `US`
- `US-FEDERAL`
- 具体州法标签
- `INTERNATIONAL_TRANSACTIONAL`（仅限确有美国律师实务价值的国际交易表达）

## 2. `chinese_legal_terms.csv` — 中国法律中文词典

**方向：中文 → English reference translation**

专门维护中国大陆法律概念。中文是 canonical headword，中文释义和中国法律依据是核心；英文只作参考翻译。

该词典与美国法律英语词典独立维护。相同译名不代表两个法域概念等同，也不构成自动去重依据。

## 3. `legal_terms.csv` — 冻结的旧迁移源

**现有 392 条。**

这是项目改向前形成的旧混合词表，包含中国法制度词和国际交易英语。从 2026-09-30 起冻结：

- 不再新增；
- 不再作为主词典；
- 只用于把旧内容逐条迁移到两个新词典；
- 迁移完成并核验之前不删除。

## 4. `oxford_dictionary_of_law_10e_reference.md` — 候选词参考索引

该文件用于发现英文法律词候选、缩写和交叉参照，不是主词典，也不是美国法权威来源。

Oxford 候选词必须先判断是否适用于美国法，并以美国权威来源独立编写释义，才能进入 `us_legal_english.csv`。

## 已删除的数据

`taiwan_reference_terms.csv` 已于 2026-09-30 删除。

项目以后不再维护或批量参考台湾司法院、台湾智慧财产局等台湾双语词表。

## 新词典字段

### US Legal English

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

### Chinese Legal Terms

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
