# Lexicon

这里存放 OpenLegalLexicon 的英文法律主词典、中国法律中文词典、冻结迁移源和基础词目索引。

## 1. `english_legal_dictionary.csv` — 英文法律主词典

**方向：English → 中文参考译法 + English explanation + 中文说明**

主词典不限定为美国法。Black's Law Dictionary 与 Oxford Dictionary of Law 都是重要基础词典，条目通过 `适用法域` 区分 US、UK、EU、INTERNATIONAL、HISTORICAL、LEGAL-LATIN 等语境。

固定工作流：

> Black's / Oxford headword → sense & jurisdiction → independent English explanation → 中文参考翻译 → 中文辅助说明 → current-law verification where needed → A–Z 写入主词典

### 排序

`english_legal_dictionary.csv` 必须始终按英文 headword **A → Z** 排列；同一 headword 的不同义项或不同法域相邻。

### 词典基线

主词典包含 `词典基线` 字段，用于标明该记录来自或对齐于：

- `BLACK'S`
- `OXFORD`
- `BLACK'S; OXFORD`
- `LEGACY`

来源标签不等于法域标签；法域另由 `适用法域` 说明。

## 2. `oxford_dictionary_of_law_10e_reference.md` — Oxford 词目索引

包含 Oxford Dictionary of Law 第 10 版（2022）识别出的 **4,854 条主词条**，按原书 A–Z 排列，并保留词性、cross-reference、abbreviation/expansion 与 source entry 编号。

该文件是正式基础词目层。所有 Oxford headwords 都需要在主词典建设过程中被处理，而不是只做覆盖检查。

## 3. Black's Law Dictionary

Black's 与 Oxford 并列作为英文法律词典的重要基础来源。Black's 对美国法和美国法律英语尤其重要；Oxford 对英国法、欧盟法和英国普通法语境尤其重要。共同 headword 需要区分不同 sense，不能简单互相覆盖。

## 4. `chinese_legal_terms.csv` — 中国法律中文词典

**方向：中文 → English reference translation**

当前 392 条迁移记录。中文是 canonical headword；英文只作参考译法。

## 5. `legal_terms.csv` — 冻结的旧迁移源

现有 392 条，只用于迁移审计和历史核对，不再新增。

## 已删除数据

台湾参考词表已经删除，不再维护或批量参考。


## 编审进度（2026-10-02，A 段批次）

本批基于 main `301017f14b3d29efb0294154fdab094ac08539c0`。主 CSV 现有 **465 条 sense/参照记录、420 个不同 headwords**；净增 399 条记录。Oxford A 段 **367/367 个源词目**已逐项对照用户提供 EPUB，形成 411 条记录；A 段词目队列为 0。Oxford B–Z 仍有 **4,487 个源词目**未按该标准处理。仅有旧迁移记录同名，不算 Oxford 来源处理完成。

### 来源范围与未完成工作

- 词典基线记录分布：Black's 29；Oxford 410；Both 1；Legacy 25。此为记录数，不是整部 Black's 的覆盖率。
- Both 仅用于实际对照过的相同 sense；本批为 abandonment 的财产权利放弃义。absence 的英国诉讼缺席义与 Black's 的历史居所缺席义分别保留。
- 本批新增 Black's 17 条记录使用可访问的 **第 2 版（1910）** OpenJurist 转录，准确标出版本和链接。历史来源不能当作现代美国法核验。
- 原有 Black's 第 8 版 12 条记录保留引用，来源对齐状态为 `inherited_citation_not_rechecked`；本批没有重新取得第 8 版全文，也没有凭空扩展其 citation。
- Black's 完整候选集合尚未枚举、去重及逐项对齐，**未处理总数未知且不是 0**；可访问的 1910 A 段网页显示 1,861 项、19 页，本批并未穷尽。不得将“Oxford A 已处理”表述为“Black's + Oxford A 完成”。
- `black_alignment_pending` 表示未实际核对 Black's 对应词目；不能由此推断 Oxford-only。已新增 Black's-only 以完整 Oxford 10e 索引为比较范围。
- 现有主词典仍需处理其他 Black's senses、US/UK 差异、Oxford B–Z 词目及参照目标。本批不是项目完工。

### 字段和审核状态

新增 `词典基线`、`源词目ID`、`来源对齐状态`、`交叉参照目标`，使来源覆盖可按源条目核算。来源名称或词形相同不表示 sense 相同。

- `baseline_concept_review`：独立简洁释义经概念编审，不表示全面现行法核验。
- `historical_reference_review`：历史参考义项；不得当作现行法效果。
- `cross_reference_review`：来源指向和展开已检查；目标词条是否已完成另计。
- `needs_current_law_review`：现行法、法域条件或制度变化尚需核验。
- `blacks_baseline_review` / `migration_review`：既有记录的原状态，不能推断为本批重新审核。

本批修复 A 段 `=` 自动提取误判，例如 abus de droit、accounting practice 和 acknowledgment of service；B–Z 的 `=` 仍须回查 EPUB。年度 annual return 已明确为旧称；Administrative Court 机构名称已对照 Judiciary 官方页面更新到 King's Bench Division，但该记录的程序细节仍保留现行法复核状态。

### 法域分布（按记录的完整标签计）

| 法域标签 | 记录数 |
|---|---:|
| HISTORICAL | 31 |
| LEGAL-LATIN; HISTORICAL | 2 |
| LEGAL-LATIN | 19 |
| US-FEDERAL | 1 |
| US-MARITIME | 1 |
| ROMAN-LAW-HISTORICAL | 5 |
| US | 3 |
| CIVIL-LAW-HISTORICAL | 1 |
| COMMON-LAW | 107 |
| ENGLAND-WALES | 117 |
| GENERAL | 10 |
| UK | 74 |
| EUROPEAN-HUMAN-RIGHTS | 1 |
| INTERNATIONAL | 27 |
| EU; CIVIL-LAW | 1 |
| EU | 13 |
| COMMON-LAW; INTERNATIONAL | 2 |
| INTERNATIONAL_TRANSACTIONAL | 37 |
| HISTORICAL; LEGAL-LATIN | 2 |
| LEGAL-LATIN; COMMON-LAW | 3 |
| ENGLAND-WALES; LEGAL-LATIN | 1 |
| LEGAL-LATIN; INTERNATIONAL | 2 |
| SCOTLAND | 1 |
| COMMON-LAW; LEGAL-LATIN | 1 |
| EU; UK | 2 |
| EU; INTERNATIONAL | 1 |

### 待现行法复核记录（213 条）

下面逐条列出 ID；具体释义及法域以主 CSV 为准。

- `oxford10-1-s2` — abandonment (ENGLAND-WALES)
- `oxford10-1-s3` — abandonment (ENGLAND-WALES)
- `oxford10-1-s4` — abandonment (ENGLAND-WALES)
- `oxford-abatement` — abatement (ENGLAND-WALES)
- `oxford10-2-s2` — abatement (ENGLAND-WALES)
- `oxford10-2-s5` — abatement (ENGLAND-WALES)
- `oxford-abh` — ABH (ENGLAND-WALES)
- `oxford-abortion` — abortion (UK)
- `oxford-absconding` — absconding (ENGLAND-WALES)
- `oxford-absence` — absence (ENGLAND-WALES)
- `oxford-absent-parent` — absent parent (UK)
- `oxford10-10-s1` — absent-mindedness (ENGLAND-WALES)
- `oxford-absolute-assignment` — absolute assignment (ENGLAND-WALES)
- `oxford-absolute-discharge` — absolute discharge (ENGLAND-WALES)
- `oxford-absolute-right` — absolute right (EUROPEAN-HUMAN-RIGHTS)
- `oxford-absolute-title` — absolute title (ENGLAND-WALES)
- `oxford-abstracting-electricity` — abstracting electricity (ENGLAND-WALES)
- `oxford-water-abstraction` — abstraction of water (UK)
- `oxford-abus-de-droit` — abus de droit (EU; CIVIL-LAW)
- `oxford-abuse-dominant-position` — abuse of a dominant position (EU)
- `oxford10-23-s2` — abuse of a dominant position (UK)
- `oxford-abuse-position-trust` — abuse of a position of trust (ENGLAND-WALES)
- `oxford-abuse-process` — abuse of process (ENGLAND-WALES)
- `oxford-abusive-behaviour` — abusive behaviour (ENGLAND-WALES)
- `oxford-abwor` — ABWOR (UK)
- `oxford10-28-s1` — ACAS (UK)
- `oxford10-31-s1` — acceptance of a bill (UK)
- `oxford10-32-s1` — acceptance supra protest (UK)
- `oxford10-35-s1` — access land (ENGLAND-WALES)
- `oxford10-4617-s1` — access to neighbouring land (ENGLAND-WALES)
- `oxford10-34-s2` — accession (UK)
- `oxford10-36-s1` — accessory (ENGLAND-WALES)
- `oxford10-36-s2` — accessory (ENGLAND-WALES)
- `oxford10-41-s1` — accommodation bill (UK)
- `oxford10-43-s2` — accord and satisfaction (ENGLAND-WALES)
- `oxford10-48-s1` — account monitoring order (UK)
- `oxford10-45-s1` — accounting period (UK)
- `oxford10-46-s1` — accounting practice (UK)
- `oxford10-47-s1` — accounting records (UK)
- `oxford10-50-s1` — accounts (UK)
- `oxford10-54-s1` — accumulation (ENGLAND-WALES)
- `oxford10-4935-s1` — acid attacks (ENGLAND-WALES)
- `oxford10-58-s1` — acknowledgment (ENGLAND-WALES)
- `oxford10-59-s1` — acknowledgment and undertaking (ENGLAND-WALES)
- `oxford10-60-s1` — acknowledgment of service (ENGLAND-WALES)
- `oxford10-64-s1` — acquired rights (UK)
- `oxford10-65-s1` — acquis communautaire (EU)
- `oxford10-73-s1` — Act of Parliament (UK)
- `oxford10-74-s1` — act of state (ENGLAND-WALES)
- `oxford10-74-s2` — act of state (US)
- `oxford10-4362-s1` — acte clair (EU)
- `oxford10-4821-s1` — activity directions and conditions (ENGLAND-WALES)
- `oxford10-71-s1` — activity requirement (ENGLAND-WALES)
- `oxford10-75-s1` — actual bodily harm (ENGLAND-WALES)
- `oxford10-76-s1` — actual military service (ENGLAND-WALES)
- `oxford10-78-s1` — actual total loss (UK)
- `oxford10-81-s1` — ad colligenda bona (ENGLAND-WALES; LEGAL-LATIN)
- `oxford10-82-s1` — additional voluntary contribution (UK)
- `oxford10-83-s1` — address for service (ENGLAND-WALES)
- `oxford10-94-s2` — administration (ENGLAND-WALES)
- `oxford10-94-s3` — administration (ENGLAND-WALES)
- `oxford10-94-s4` — administration (ENGLAND-WALES)
- `oxford10-94-s1` — administration (UK)
- `oxford10-95-s1` — administration action (ENGLAND-WALES)
- `oxford10-96-s1` — administration bond (ENGLAND-WALES)
- `oxford10-97-s1` — administration of poison (ENGLAND-WALES)
- `oxford10-98-s1` — administration order (ENGLAND-WALES)
- `oxford10-98-s2` — administration order (UK)
- `oxford10-99-s1` — administration pending suit (ENGLAND-WALES)
- `oxford10-100-s1` — administration period (ENGLAND-WALES)
- `oxford10-4366-s1` — Administrative Court (ENGLAND-WALES)
- `oxford10-103-s1` — administrative powers (UK)
- `oxford10-104-s1` — administrative receiver (UK)
- `oxford10-105-s1` — administrative tribunal (UK)
- `oxford10-106-s1` — administrator (ENGLAND-WALES)
- `oxford10-106-s2` — administrator (UK)
- `oxford10-107-s1` — Admiralty Court (ENGLAND-WALES)
- `oxford10-109-s1` — admissibility of records (ENGLAND-WALES)
- `oxford10-110-s1` — admission (ENGLAND-WALES)
- `oxford10-110-s2` — admission (ENGLAND-WALES)
- `oxford10-111-s1` — admonition (UK)
- `oxford10-112-s2` — adoption (ENGLAND-WALES)
- `oxford10-112-s1` — adoption (UK)
- `oxford10-112-s3` — adoption (UK)
- `oxford10-113-s1` — adoption agency (UK)
- `oxford10-114-s1` — adoption leave (UK)
- `oxford10-115-s1` — adoption service (UK)
- `oxford10-116-s1` — adoption society (UK)
- `oxford10-117-s1` — adoptive relationship (UK)
- `oxford10-120-s1` — adulteration (UK)
- `oxford10-121-s1` — adultery (ENGLAND-WALES)
- `oxford10-4368-s1` — advance decision (ENGLAND-WALES)
- `oxford10-4938-s1` — advance indication of sentence (ENGLAND-WALES)
- `oxford10-122-s1` — advance information (ENGLAND-WALES)
- `oxford10-123-s1` — advancement (ENGLAND-WALES)
- `oxford10-123-s2` — advancement (ENGLAND-WALES)
- `oxford10-4369-s1` — adverse inference (ENGLAND-WALES)
- `oxford10-125-s1` — adverse occupation (ENGLAND-WALES)
- `oxford10-126-s1` — adverse possession (ENGLAND-WALES)
- `oxford10-128-s1` — advice on evidence (ENGLAND-WALES)
- `oxford10-4939-s1` — Advisory Conciliation and Arbitration Service (UK)
- `oxford10-130-s1` — advocacy qualification (ENGLAND-WALES)
- `oxford10-131-s2` — advocate (SCOTLAND)
- `oxford10-132-s1` — Advocates-General (EU)
- `oxford10-133-s1` — advowson (ENGLAND-WALES)
- `oxford10-139-s1` — affirmative resolution (UK)
- `oxford10-140-s1` — affray (ENGLAND-WALES)
- `oxford10-4623-s1` — African, Caribbean, Pacific Group (INTERNATIONAL)
- `oxford10-4370-s1` — AGA (ENGLAND-WALES)
- `oxford10-4371-s1` — age discrimination (UK)
- `oxford10-146-s1` — age of consent (UK)
- `oxford10-143-s1` — agency workers (UK)
- `oxford10-148-s1` — aggravated burglary (ENGLAND-WALES)
- `oxford10-150-s1` — aggravated trespass (ENGLAND-WALES)
- `oxford10-151-s1` — aggravated vehicle-taking (ENGLAND-WALES)
- `oxford10-152-s1` — aggregates levy (UK)
- `oxford10-155-s1` — agreement for a lease (ENGLAND-WALES)
- `oxford10-158-s1` — agricultural holding (ENGLAND-WALES)
- `oxford10-159-s1` — Agricultural Land and Drainage (ENGLAND-WALES)
- `oxford10-160-s1` — agricultural property relief (UK)
- `oxford10-163-s1` — air force law (UK)
- `oxford10-164-s1` — air pollution (UK)
- `oxford10-4940-s1` — air rage (UK)
- `oxford10-165-s1` — airspace (ENGLAND-WALES)
- `oxford10-166-s1` — alcohol treatment requirement (ENGLAND-WALES)
- `oxford10-167-s1` — alderman (ENGLAND-WALES)
- `oxford10-174-s1` — alimony (ENGLAND-WALES)
- `oxford10-4376-s1` — all-ports warning system (UK)
- `oxford10-176-s1` — allegiance (UK)
- `oxford10-177-s1` — allocation (ENGLAND-WALES)
- `oxford10-179-s1` — allotment (UK)
- `oxford10-182-s1` — alteration of share capital (UK)
- `oxford10-184-s1` — alternative finance arrangements (UK)
- `oxford10-185-s1` — Alternative Investment Market (UK)
- `oxford10-186-s1` — alternative verdict (ENGLAND-WALES)
- `oxford10-190-s2` — amendment (ENGLAND-WALES)
- `oxford10-190-s1` — amendment (UK)
- `oxford10-4377-s1` — AMHP (ENGLAND-WALES)
- `oxford10-194-s1` — Amsterdam Treaty (EU)
- `oxford10-196-s1` — ancient lights (ENGLAND-WALES)
- `oxford10-197-s1` — ancillary credit business (UK)
- `oxford10-198-s1` — ancillary probate (ENGLAND-WALES)
- `oxford10-199-s1` — ancillary relief (ENGLAND-WALES)
- `oxford10-200-s1` — ancillary restraint (EU; UK)
- `oxford10-202-s1` — animals (ENGLAND-WALES)
- `oxford10-205-s1` — annual general meeting (UK)
- `oxford10-207-s1` — annual value of land (UK)
- `oxford10-209-s1` — annulment (ENGLAND-WALES)
- `oxford10-209-s2` — annulment (ENGLAND-WALES)
- `oxford10-209-s4` — annulment (EU)
- `oxford10-209-s3` — annulment (UK)
- `oxford10-211-s1` — answer (ENGLAND-WALES)
- `oxford10-212-s1` — antecedents (ENGLAND-WALES)
- `oxford10-214-s1` — anti-avoidance provisions (UK)
- `oxford10-217-s1` — anticompetitive practice (EU; UK)
- `oxford10-219-s1` — antisocial behaviour order (UK)
- `oxford10-220-s1` — antitrust law (US)
- `oxford10-221-s1` — Anton Piller order (ENGLAND-WALES)
- `oxford10-222-s1` — apology (ENGLAND-WALES)
- `oxford10-225-s1` — appeal in Revenue matters (UK)
- `oxford10-232-s1` — applying the proviso (ENGLAND-WALES)
- `oxford10-233-s1` — appointed day (UK)
- `oxford10-238-s2` — appropriation (ENGLAND-WALES)
- `oxford10-238-s3` — appropriation (ENGLAND-WALES)
- `oxford10-238-s1` — appropriation (UK)
- `oxford10-4380-s1` — approved clinician (ENGLAND-WALES)
- `oxford10-4381-s1` — approved mental health professional (ENGLAND-WALES)
- `oxford10-4941-s1` — Approved Premises (ENGLAND-WALES)
- `oxford10-241-s1` — approximation of laws (EU)
- `oxford10-253-s1` — arrangement (UK)
- `oxford10-259-s1` — arson (ENGLAND-WALES)
- `oxford10-261-s1` — Article 101 (EU)
- `oxford10-262-s1` — Article 102 (EU)
- `oxford10-263-s1` — Article 267 (EU)
- `oxford10-4824-s1` — Article 50 (EU)
- `oxford10-264-s1` — articles of association (UK)
- `oxford10-265-s1` — artificial insemination (UK)
- `oxford10-4383-s1` — artificial nutrition and hydration (ENGLAND-WALES)
- `oxford10-269-s1` — assault (ENGLAND-WALES)
- `oxford10-270-s1` — assault by penetration (ENGLAND-WALES)
- `oxford10-271-s1` — assault of a child under 13 by penetration (ENGLAND-WALES)
- `oxford10-4629-s1` — assault on a police constable in the execution of his duty (ENGLAND-WALES)
- `oxford10-272-s1` — Assembly of the European Communities (EU)
- `oxford10-273-s1` — assent (ENGLAND-WALES)
- `oxford10-274-s1` — assent procedure (EU)
- `oxford10-275-s1` — assessment of costs (ENGLAND-WALES)
- `oxford10-278-s1` — assignment (ENGLAND-WALES)
- `oxford10-278-s2` — assignment (ENGLAND-WALES)
- `oxford10-4825-s1` — assisted reproduction (UK)
- `oxford10-4385-s1` — assisted suicide (UK)
- `oxford10-280-s1` — associated operations (UK)
- `oxford10-281-s1` — association agreement (EU; INTERNATIONAL)
- `oxford10-282-s1` — assurance (UK)
- `oxford10-283-s1` — assured agricultural occupancy (ENGLAND-WALES)
- `oxford10-284-s1` — assured shorthold tenancy (ENGLAND-WALES)
- `oxford10-285-s1` — assured tenancy (ENGLAND-WALES)
- `oxford10-288-s1` — at sea (ENGLAND-WALES)
- `oxford10-289-s1` — attachment (ENGLAND-WALES)
- `oxford10-290-s1` — attachment of earnings (ENGLAND-WALES)
- `oxford10-291-s1` — attempt (ENGLAND-WALES)
- `oxford10-292-s1` — attendance centre (ENGLAND-WALES)
- `oxford10-294-s1` — attorney (ENGLAND-WALES)
- `oxford10-295-s1` — Attorney General (ENGLAND-WALES)
- `oxford10-298-s1` — auction ring (UK)
- `oxford10-301-s1` — audit exemption (UK)
- `oxford10-302-s1` — auditor (UK)
- `oxford10-304-s2` — authority (UK)
- `oxford10-305-s1` — authorized capital (UK)
- `oxford10-4386-s1` — authorized guarantee agreement (ENGLAND-WALES)
- `oxford10-306-s1` — authorized investments (ENGLAND-WALES)
- `oxford10-307-s1` — authorized securities (ENGLAND-WALES)
- `oxford10-316-s1` — AVC (UK)
- `oxford10-321-s1` — avoidance of disposition order (ENGLAND-WALES)

### 尚未具备独立主词条的参照目标

European Parliament；House of Lords；Initial Details of the Prosecution Case；Stock Exchange；abigeatus；abigeus；able-bodied seaman；books of account；breach of contract；burglary；challenge to jury；comfort letter；competition law；cuius est solum, eius est usque ad coelum et ad inferos；deed of arrangement；deep seabed area；delegated legislation；discharge；dumping；environmental taxes；equality is equity；estate pur (or per) autre vie；fatal accidents；insanity；insurance；juristic person；larceny；lay days；maritime law；marriage settlement；mistake；natural justice；non-insane automatism；pendente lite；poison；pollution；power of appointment；prenuptial agreement；privileged will；protective trust；proviso；punishment；relevant transfer；road traffic accidents；scheme of arrangement；search order；service law；standard-form contract；testamentary intention；threatening behaviour；treaty；trespass；unascertained goods；voluntary arrangement。

### 本批校验

CSV 解析、逐列完整性、A–Z 排序、ID 唯一性、同 headword 相邻、精确 sense 重复检查、A 段源条目覆盖和参照/缩写分类检查均通过。全部既有 ID 保留。未修改中国法中文词典和冻结迁移源，未恢复台湾来源，未新增工程结构或 CI。
