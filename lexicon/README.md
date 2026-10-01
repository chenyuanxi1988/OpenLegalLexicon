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


## 编审进度（2026-10-02，A–B 及 C 开头）

主 CSV：**749 条记录，678 个不同 headwords**。本批基于 main `ec58218b2a0b560543ebe0960b14e57d1c5ee5e0`，连续处理 **258 个 Oxford 源词目**（B 全部 158 个 + C 开头 100 个），净增 284 条 sense/参照记录。

| 范围 | 源词目数 | 已处理 | 未处理 |
|---|---:|---:|---:|
| Oxford A | 367 | 367 | 0 |
| Oxford B | 158 | 158 | 0 |
| Oxford C | 597 | 100 | 497 |
| Oxford A–Z | 4854 | 625 | 4229 |

C 本批末项是 `challenge to jury`；继续从原书下一源条目推进，不跳部门法。A–C 索引使用原书 source-entry ID；C 未处理词目也标记 `unprocessed`。C 中原始提取遗漏的 `CFSP` 已恢复（来源为空锚点后第二链接）；两条驾驶致死词目补全 `or drugs` / `or inconsiderate driving`，没有把截断词目创建为另一个概念。B 的 `bar` 与 `Bar`、`bill` 与 `Bill` 按源词形分别保留。

### 来源对齐和完成边界

Black's 与 Oxford 并列为核心基础；本批不把未核实者归为 Oxford-only。

- 记录基线分布：Black's 29；Oxford 693；Both 2；Legacy 25。
- 实际相同概念对照：abandonment 的财产权利放弃义、bailment 的占有交付义，标记 Both；后者的 1910 年契约式表述只作历史比较。实际不同义项对照：absence 的英国诉讼缺席与 Black's 历史居所缺席，分别保留。
- 17 条新 Black's 记录来自第 2 版（1910）OpenJurist 转录。原有 12 条第 8 版记录保留 citation，但标 `inherited_citation_not_rechecked`，本轮没有重新取得该版全文。不得把 1910 来源称作已更新的现代美国法。
- 可访问的 Black's 1910 A 网页显示 1,861 项 / 19 页，B 显示 827 项；完整集合尚未枚举和逐项对齐。**Black's 未处理总数未知且不为 0**，不能据上述 CSV 记录数宣称整部覆盖。
- `black_alignment_pending` 不是 Oxford-only；`blacks_only_against_oxford10_index` 的比较范围为 Oxford 第 10 版完整词目索引。
- 已有同名 Legacy 记录不计作 Oxford 来源已处理。Oxford 未处理词目 **4,229**；项目尚未达到最终完成标准。

### 字段与审核状态

`词典基线`、`源词目ID`、`来源对齐状态`、`交叉参照目标`使来源及 sense 可追溯。`baseline_concept_review` 仅表示独立概念编审，不表示全面现行法核验；`historical_reference_review` 是历史义项；`cross_reference_review` 是参照/展开核对；`needs_current_law_review` 明确保留现行法复核缺口；既有 `blacks_baseline_review` 与 `migration_review` 不被解释为本轮重新审核。

A 段 `=` 误判已修复。D–Z 的 `=` 仍需回查原书，不可直接当成缩写。Administrative Court 已用官方页面更新到 King's Bench Division；annual return 保留为确认其旧称后的历史义项。Biodiversity Treaty 不沿用 2022 的“拟议”状态描述现状，保留明确复核标记；涉及刑法、税法、国籍、金融监管、英国机构及法律改革的记录不假装完成现行法核验。

### 法域分布（完整标签、按记录计）

| 法域 | 数量 |
|---|---:|
| HISTORICAL | 50 |
| LEGAL-LATIN; HISTORICAL | 2 |
| LEGAL-LATIN | 28 |
| US-FEDERAL | 1 |
| US-MARITIME | 1 |
| ROMAN-LAW-HISTORICAL | 5 |
| US | 3 |
| CIVIL-LAW-HISTORICAL | 1 |
| COMMON-LAW | 168 |
| ENGLAND-WALES | 195 |
| GENERAL | 19 |
| UK | 143 |
| EUROPEAN-HUMAN-RIGHTS | 1 |
| INTERNATIONAL | 41 |
| EU; CIVIL-LAW | 1 |
| EU | 19 |
| COMMON-LAW; INTERNATIONAL | 2 |
| INTERNATIONAL_TRANSACTIONAL | 46 |
| HISTORICAL; LEGAL-LATIN | 3 |
| LEGAL-LATIN; COMMON-LAW | 3 |
| ENGLAND-WALES; LEGAL-LATIN | 1 |
| LEGAL-LATIN; INTERNATIONAL | 4 |
| SCOTLAND | 1 |
| COMMON-LAW; LEGAL-LATIN | 2 |
| EU; UK | 3 |
| EU; INTERNATIONAL | 2 |
| GUERNSEY | 1 |
| UK; EU | 1 |
| RELIGIOUS-LAW | 2 |

### 待现行法复核记录（395 条）

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
- `oxford10-4619-s1` — actio popularis (INTERNATIONAL)
- `oxford10-4936-s1` — Activities of Transnational Corporations Treaty (INTERNATIONAL)
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
- `oxford10-129-s1` — advisory jurisdiction (INTERNATIONAL)
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
- `oxford10-153-s1` — aggression (INTERNATIONAL)
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
- `oxford10-193-s1` — amnesty (INTERNATIONAL)
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
- `oxford10-216-s1` — anticipatory self-defence (INTERNATIONAL)
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
- `oxford10-286-s1` — asylum (INTERNATIONAL)
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
- `oxford10-311-s1` — aut punire aut dedere (LEGAL-LATIN; INTERNATIONAL)
- `oxford10-304-s2` — authority (UK)
- `oxford10-305-s1` — authorized capital (UK)
- `oxford10-4386-s1` — authorized guarantee agreement (ENGLAND-WALES)
- `oxford10-306-s1` — authorized investments (ENGLAND-WALES)
- `oxford10-307-s1` — authorized securities (ENGLAND-WALES)
- `oxford10-308-s1` — automatic reservation (INTERNATIONAL)
- `oxford10-312-s1` — autrefois acquit (COMMON-LAW)
- `oxford10-313-s1` — autrefois convict (COMMON-LAW)
- `oxford10-316-s1` — AVC (UK)
- `oxford10-321-s1` — avoidance of disposition order (ENGLAND-WALES)
- `oxford10-324-s1` — backed for bail (ENGLAND-WALES)
- `oxford10-325-s1` — bail (ENGLAND-WALES)
- `oxford10-327-s1` — bail hostel (UK)
- `oxford10-328-s1` — bailiff (ENGLAND-WALES)
- `oxford10-328-s2` — bailiff (GUERNSEY)
- `oxford10-333-s1` — bank holidays (UK)
- `oxford10-334-s1` — bankruptcy (ENGLAND-WALES)
- `oxford10-4943-s1` — Banks v Goodfellow test (ENGLAND-WALES)
- `oxford10-335-s1` — banning order (UK)
- `oxford10-336-s1` — banns (ENGLAND-WALES)
- `oxford10-338-s1` — Bar (ENGLAND-WALES)
- `oxford10-337-s2` — bar (ENGLAND-WALES)
- `oxford10-337-s3` — bar (UK)
- `oxford10-339-s1` — Bar Council (ENGLAND-WALES)
- `oxford10-4944-s1` — Barnett formula (UK)
- `oxford10-344-s1` — barrister (ENGLAND-WALES)
- `oxford10-345-s1` — baseline (INTERNATIONAL)
- `oxford10-346-s1` — basic award (UK)
- `oxford10-347-s1` — basic intent (ENGLAND-WALES)
- `oxford10-348-s1` — battered child (UK)
- `oxford10-349-s1` — battered spouse (UK)
- `oxford10-350-s1` — Battered Woman Syndrome (COMMON-LAW)
- `oxford10-351-s1` — battery (ENGLAND-WALES)
- `oxford10-352-s1` — bay (INTERNATIONAL)
- `oxford10-354-s1` — beauty contest (UK)
- `oxford10-4387-s1` — bed and breakfasting (UK)
- `oxford10-355-s1` — Beddoe order (ENGLAND-WALES)
- `oxford10-358-s1` — Benchers (ENGLAND-WALES)
- `oxford10-363-s1` — beneficiary principle (COMMON-LAW)
- `oxford10-364-s1` — benefits in kind (UK)
- `oxford10-366-s1` — Benjamin order (ENGLAND-WALES)
- `oxford10-4632-s1` — bereaved minor’s trust (UK)
- `oxford10-369-s1` — bereavement benefit (UK)
- `oxford10-370-s1` — bereavement, damages for (ENGLAND-WALES)
- `oxford10-371-s1` — Berne Convention (INTERNATIONAL)
- `oxford10-4388-s1` — best interests (ENGLAND-WALES)
- `oxford10-4388-s2` — best interests (UK)
- `oxford10-373-s1` — best value (UK)
- `oxford10-372-s1` — best-evidence rule (COMMON-LAW)
- `oxford10-374-s1` — Beth Din (UK)
- `oxford10-4946-s1` — betting duty (UK)
- `oxford10-377-s1` — bigamy (ENGLAND-WALES)
- `oxford10-381-s1` — Bill (UK)
- `oxford10-382-s1` — bill of costs (ENGLAND-WALES)
- `oxford10-383-s1` — bill of exchange (UK)
- `oxford10-384-s1` — bill of indictment (ENGLAND-WALES)
- `oxford10-386-s1` — bill of sale (ENGLAND-WALES)
- `oxford10-387-s1` — bind over (ENGLAND-WALES)
- `oxford10-4947-s1` — Biodiversity Treaty (INTERNATIONAL)
- `oxford10-388-s1` — birth certificate (UK)
- `oxford10-391-s1` — Black Rod, Gentleman Usher of the (UK)
- `oxford10-389-s1` — blacklist (UK)
- `oxford10-390-s1` — blackmail (ENGLAND-WALES)
- `oxford10-393-s1` — blight notice (ENGLAND-WALES)
- `oxford10-396-s1` — block exemption (EU)
- `oxford10-396-s2` — block exemption (UK)
- `oxford10-395-s1` — blockade (INTERNATIONAL)
- `oxford10-398-s1` — blood specimen (UK)
- `oxford10-399-s1` — blood test (UK)
- `oxford10-399-s2` — blood test (UK)
- `oxford10-4389-s1` — blue bag (ENGLAND-WALES)
- `oxford10-402-s1` — bodily harm (ENGLAND-WALES)
- `oxford10-4391-s1` — Bolam test (ENGLAND-WALES)
- `oxford10-404-s1` — bomb hoax (UK)
- `oxford10-406-s1` — bona vacantia (ENGLAND-WALES)
- `oxford10-408-s1` — bonus issue (UK)
- `oxford10-409-s1` — books of account (UK)
- `oxford10-410-s1` — borough (ENGLAND-WALES)
- `oxford10-415-s1` — boundary commissions (UK)
- `oxford10-4392-s1` — Bournewood gap (ENGLAND-WALES)
- `oxford10-4393-s1` — brain death (UK)
- `oxford10-417-s1` — breach of confidence (ENGLAND-WALES)
- `oxford10-417-s2` — breach of confidence (ENGLAND-WALES)
- `oxford10-419-s1` — breach of privilege (UK)
- `oxford10-420-s1` — breach of statutory duty (ENGLAND-WALES)
- `oxford10-421-s1` — breach of the peace (ENGLAND-WALES)
- `oxford10-424-s1` — breakdown of marriage (UK)
- `oxford10-426-s1` — breath specimen (UK)
- `oxford10-427-s1` — breath test (UK)
- `oxford10-425-s1` — breathalyser (UK)
- `oxford10-4828-s1` — Brexit (UK; EU)
- `oxford10-429-s1` — bribery (UK)
- `oxford10-430-s1` — bridleway (ENGLAND-WALES)
- `oxford10-431-s1` — brief (ENGLAND-WALES)
- `oxford10-431-s2` — brief (ENGLAND-WALES)
- `oxford10-4635-s1` — brief fee (ENGLAND-WALES)
- `oxford10-432-s1` — British citizenship (UK)
- `oxford10-434-s1` — British National (Overseas) (UK)
- `oxford10-435-s1` — British Overseas citizenship (UK)
- `oxford10-436-s1` — British Overseas Territories citizenship (UK)
- `oxford10-437-s1` — British protected person (UK)
- `oxford10-438-s1` — British subject (UK)
- `oxford10-439-s1` — Broadmoor (ENGLAND-WALES)
- `oxford10-440-s1` — brothel (ENGLAND-WALES)
- `oxford10-441-s1` — Brussels Convention (EU; INTERNATIONAL)
- `oxford10-443-s1` — Budget (UK)
- `oxford10-445-s1` — bugging (UK)
- `oxford10-447-s1` — building preservation notice (ENGLAND-WALES)
- `oxford10-448-s1` — building scheme (ENGLAND-WALES)
- `oxford10-449-s1` — building society (UK)
- `oxford10-450-s1` — Bullock order (ENGLAND-WALES)
- `oxford10-451-s1` — burden of proof (COMMON-LAW)
- `oxford10-452-s1` — burglary (ENGLAND-WALES)
- `oxford10-453-s1` — business (UK)
- `oxford10-454-s1` — business asset (UK)
- `oxford10-455-s1` — business liability (UK)
- `oxford10-456-s1` — business name (UK)
- `oxford10-457-s1` — business property relief (UK)
- `oxford10-458-s1` — business tenancy (ENGLAND-WALES)
- `oxford10-460-s1` — byelaw (UK)
- `oxford10-461-s1` — Cabinet (UK)
- `oxford10-4829-s1` — Cabinet Office (UK)
- `oxford10-462-s1` — cabotage (EU)
- `oxford10-463-s1` — CAC (UK)
- `oxford10-464-s1` — Cafcass (ENGLAND-WALES)
- `oxford10-465-s1` — Calderbank letter (ENGLAND-WALES)
- `oxford10-466-s1` — call (ENGLAND-WALES)
- `oxford10-466-s2` — call (UK)
- `oxford10-468-s1` — Calvo clause (INTERNATIONAL)
- `oxford10-469-s2` — cancellation (UK)
- `oxford10-470-s1` — cannabis (UK)
- `oxford10-474-s1` — CAP (EU)
- `oxford10-478-s1` — capital (UK)
- `oxford10-479-s1` — capital allowance (UK)
- `oxford10-480-s1` — capital gains tax (UK)
- `oxford10-482-s1` — capital money (ENGLAND-WALES)
- `oxford10-483-s1` — capital punishment (GENERAL)
- `oxford10-484-s1` — capital redemption reserve (UK)
- `oxford10-481-s1` — capitalization issue (UK)
- `oxford10-485-s1` — capitulation (INTERNATIONAL)
- `oxford10-488-s1` — care contact order (ENGLAND-WALES)
- `oxford10-492-s1` — care order (ENGLAND-WALES)
- `oxford10-493-s1` — care plan (ENGLAND-WALES)
- `oxford10-494-s1` — care proceedings (ENGLAND-WALES)
- `oxford10-4397-s1` — Care Quality Commission for England (ENGLAND-WALES)
- `oxford10-489-s1` — careless and inconsiderate driving (ENGLAND-WALES)
- `oxford10-495-s1` — carer’s allowance (UK)
- `oxford10-4950-s1` — Carltona principle (ENGLAND-WALES)
- `oxford10-499-s1` — carriageway (ENGLAND-WALES)
- `oxford10-502-s1` — cartel (EU; UK)
- `oxford10-505-s1` — case management (ENGLAND-WALES)
- `oxford10-506-s1` — case management conference (ENGLAND-WALES)
- `oxford10-507-s1` — case stated (ENGLAND-WALES)
- `oxford10-515-s1` — Cause Book (ENGLAND-WALES)
- `oxford10-518-s1` — causing a child to watch a sexual act (ENGLAND-WALES)
- `oxford10-519-s1` — causing death by careless driving when under the influence of drink or drugs (ENGLAND-WALES)
- `oxford10-4400-s1` — causing death by careless or inconsiderate driving (ENGLAND-WALES)
- `oxford10-520-s1` — causing death by dangerous driving (ENGLAND-WALES)
- `oxford10-4401-s1` — causing loss by unlawful means (ENGLAND-WALES)
- `oxford10-521-s1` — caution (ENGLAND-WALES)
- `oxford10-521-s2` — caution (ENGLAND-WALES)
- `oxford10-522-s1` — caution against first registration (ENGLAND-WALES)
- `oxford10-523-s1` — caveat (ENGLAND-WALES)
- `oxford10-4951-s1` — CBO (ENGLAND-WALES)
- `oxford10-4639-s1` — CCGs (ENGLAND-WALES)
- `oxford10-4402-s1` — CCRC (UK)
- `oxford10-528-s1` — CE (EU)
- `oxford10-530-s1` — Central Arbitration Committee (UK)
- `oxford10-531-s1` — Central Criminal Court (ENGLAND-WALES)
- `oxford10-532-s1` — Central Office (ENGLAND-WALES)
- `oxford10-533-s1` — certificate of incorporation (UK)
- `oxford10-4831-s1` — certificates of readiness (ENGLAND-WALES)
- `oxford10-534-s1` — Certification Officer (UK)
- `oxford10-535-s1` — certiorari (ENGLAND-WALES)
- `oxford10-538-s2` — cessate grant (ENGLAND-WALES)
- `oxford10-541-s1` — cession (INTERNATIONAL)
- `oxford10-546-s1` — CFP (EU)
- `oxford10-547-s1` — CFSP (EU)
- `oxford10-548-s1` — CGT (UK)
- `oxford10-549-s1` — chain of executorship (ENGLAND-WALES)
- `oxford10-551-s1` — challenge to jury (COMMON-LAW)

### 未具备独立记录的参照目标

Chancellor of the Exchequer；Children and Family Court Advisory and Support Service；Clinical Commissioning Groups；Common Agricultural Policy；Common Fisheries Policy；Commonwealth；Criminal Behaviour Order；Criminal Cases Review Commission；European Parliament；European Union；House of Lords；Initial Details of the Prosecution Case；Maastricht Treaty；Stock Exchange；abigeatus；abigeus；able-bodied seaman；child subjected to physical abuse；comfort letter；compensation；competent patient；competition law；consanguinity；corporation；cuius est solum, eius est usque ad coelum et ad inferos；deed of arrangement；deep seabed area；delegated legislation；discharge；doli capax；domestic violence；dumping；electronic surveillance；entailed interest；environmental taxes；equality is equity；estate pur (or per) autre vie；fatal accidents；fixed asset；football hooliganism；grievous bodily harm；hypothecation；impotence；incompetent patient；insanity；insurance；juristic person；larceny；lay days；loan capital；marital breakdown；maritime law；marriage settlement；mistake；natural justice；negligent misstatement；non-insane automatism；parliamentary privilege；pendente lite；poison；pollution；power of appointment；prenuptial agreement；privileged will；protective trust；proviso；punishment；quashing order；relevant transfer；road traffic accidents；scheme of arrangement；search order；service law；specimen of blood；specimen of breath；standard-form contract；testamentary capacity；testamentary intention；threatening behaviour；treaty；trespass；unascertained goods；voluntary arrangement；welfare principle。

### 校验结果

CSV 解析、A–Z 排序、ID 唯一、不同 sense 相邻、精确 sense 去重、625 个源条目的结果覆盖、参照和缩写类型均通过。保留全部既有 ID，未修改中文词典和冻结迁移源。只更新主词典、同一来源索引和本 README；未新建分支、PR、workflow、CI、tag 或 release，未恢复台湾来源。
