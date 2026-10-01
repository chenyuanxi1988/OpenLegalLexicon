# Lexicon

这里存放 OpenLegalLexicon 的两个正式词典、冻结的迁移源和参考索引。

## 1. `us_legal_english.csv` — 美国法律英语主词典

**方向：English → 中文参考翻译**

**当前：25 条迁移种子。**

英文法律词条是 canonical headword。美国主词典以后统一以 **Black's Law Dictionary** 作为首要词典基线。用户已经提供该词典，并已整理出词目清单；后续美国词典直接以该清单为主工作底稿。

### 固定工作流

> Black's headword / sense → 美国现行法源核验 → 中文参考翻译 → 中文辅助说明 → A–Z 写入主词典

规则：

1. 先核对 Black's 的 headword、义项、词形和交叉参照；
2. 再用美国宪法、法典、联邦规则、判例、法院/监管机构材料或相应州法核验；
3. 不由模型脱离 Black's 自行发明核心定义；
4. 中文翻译和中文说明是项目独立编审内容；
5. 不逐字复制 Black's 的整段原文释义；
6. 当前 25 条迁移种子仍标记 `migration_review`，后续按 Black's 基线逐条重审。

### A–Z 排序规则

`us_legal_english.csv` 必须始终按 `英文词条` **A → Z** 排列，大小写不影响排序。

- 扩词本身也按 A → Z 推进；
- 新词条插入正确字母位置，不按批次追加到文件尾部；
- 相同 headword 的不同义项相邻；
- 同一 headword 再按义项、法域或用途区分；
- 缩写、别名和交叉参照优先参考 Black's 的词条组织方式。

当前 25 条迁移种子已经处于 A–Z 顺序。

正式法域标签可包括：`US`、`US-FEDERAL`、具体州法标签，以及确有美国律师实务价值的 `INTERNATIONAL_TRANSACTIONAL`。

## 2. `chinese_legal_terms.csv` — 中文法律词典

**方向：中文 → English reference translation**

**当前：392 条迁移记录。**

中文是 canonical headword。中国法记录继续以中国法律依据和中国法语境为核心；英文只作为参考译法，不构成与美国法概念的自动对应。

为避免信息损失，当前暂时保留旧词表的 17 字段结构。

## 3. `legal_terms.csv` — 冻结的旧迁移源

现有 392 条。该文件不再新增，仅作为迁移审计和历史核对来源保留。392 条已经完整进入 `chinese_legal_terms.csv`；其中 25 条国际交易英语已经整理为 English-first 迁移种子进入 `us_legal_english.csv`。

## 4. Black's 与其他参考资料

Black's 是美国主词典的**首要词目与概念框架基线**。项目不是对原书的逐字重印，而是基于其词目/义项体系进行独立的中文翻译、中文说明、美国法语境核验、标签和数据编排。

`oxford_dictionary_of_law_10e_reference.md` 只作为英国法候选词索引和覆盖检查，不作为美国词典的定义基线。

## 已删除的数据

`taiwan_reference_terms.csv` 已删除。项目以后不再维护或批量参考台湾司法院、台湾智慧财产局等台湾双语词表。
