# OpenLegalLexicon 开发计划与基准指令

更新：2026-10-02

本文件是词典开发、任务交接和验收的基准指令。2026-10-02 用户最新指令优先：**先完成全部 Oxford 词目；Black's 新来源与新增对齐暂停，等待用户提供来源；具体词目整理交由 ChatGPT 网页版执行，由验收端检查结果。** 不得把未实际启动的网页版任务表述为正在执行。

## 1. 项目定位与来源关系

项目是一部 **English-first, multi-jurisdiction, Chinese-assisted** 的英文法律词典，不是美国法律词典。英文 headword 是主入口，中文译法和说明帮助理解。

Black's Law Dictionary 与 Oxford Dictionary of Law 并列作为核心基础词典，不设 Black's 主、Oxford 次的固定等级。Black's 重点覆盖美国法、美国法律英语和普通法传统；Oxford 重点覆盖英国法，并包括 EU、国际法、历史术语、Legal Latin 等。

Oxford 优先是当前执行顺序，不改变两本词典的长期并列地位。现阶段不继续搜集或扩写 Black's 来源；保留已有 Black's 记录及真实来源状态，不自动删除或宣称重新核实。用户提供 Black's 来源后再恢复相应处理。

## 2. 仓库、分支与文件边界

仅操作仓库 `chenyuanxi1988/OpenLegalLexicon`，唯一工作分支为 `main`。

| 文件 | 用途与约束 |
|---|---|
| `lexicon/english_legal_dictionary.csv` | 唯一英文法律主词典 |
| `lexicon/oxford_dictionary_of_law_10e_reference.md` | Oxford 第 10 版 A–Z 源词目索引，约 4,854 个 headwords |
| `lexicon/chinese_legal_terms.csv` | 独立中国法中文词典，不因英文整理随意重构 |
| `lexicon/legal_terms.csv` | 冻结旧迁移源；仅发现明确迁移错误时修复 |
| `lexicon/README.md` | 当前覆盖、审核队列、批次验证及来源边界 |

台湾来源数据已经删除，禁止重新引入台湾词表、台湾中文或台湾英文参考资料。不得创建 sidecar 重复词典或为了方便新增复杂工程结构。已迁移的国际交易英语继续保留，按多法域规则复核；旧中文迁移历史不改变两个词典的独立边界。

## 3. 总目标与当前阶段

长期目标：Black's 与 Oxford 可用英文法律 headwords 按 A → Z 全部处理，未处理队列为 0。

当前目标：先完成全部 Oxford 源词目，不等待 Black's 来源。每个 Oxford 源词目必须在主 CSV 中具有可追溯处理结果，分别为：

- 正式词条；
- 独立法域 sense；
- cross-reference；
- abbreviation；
- historical / Latin / EU / international reference；
- 已写入独立解释、明确标记 `needs_current_law_review` 的待现行法复核记录。

仅把词目放入索引、保留同名 Legacy 记录、写空占位定义或笼统标记“暂缓”，不计为已处理。源词目数量、独立 headword 数量与 CSV sense/参照记录数量分别统计。

## 4. 高吞吐连续 A–Z 工作方式

每轮处理最大安全连续 A–Z 区间，目标至少 **250–500 个源 headwords/批次**。能完成整个当前字母就完成整个字母；如字母较短可连续衔接下一字母。尾段不足目标时如实报告。不要每轮只处理几十条，也不要按部门法零散跳跃。

每批先重新读取远程 `main` 最新 SHA，读取该 SHA 对应内容，不能假设历史 SHA 仍然有效。读取 Oxford 当前连续区间，回查原书词形、sense、参照和缩写，编写中英文内容，再排序、检查、提交和验收。

稳定概念、历史词、Latin、cross-reference、abbreviation 不过度检索，直接依据已核实的词目与 sense 结构编写独立简洁解释。少数复杂词不能拖住整批。

## 5. 主 CSV 必需内容与追溯

每条正式记录至少维护：

- 英文词条、中文参考译法、词性、领域、适用法域、类型；
- 英文释义、中文辅助说明、使用语境、同义词或变体、常见搭配；
- 权威来源、条目 ID、数据许可、审核状态。

已增加的追溯字段继续维护：`词典基线`、`源词目ID`、`来源对齐状态`、`交叉参照目标`。词典基线使用 `Black's` / `Oxford` / `Both` / `Legacy`；Both 仅用于实际核实后的相应 sense，不能因 headword 相同自动标注。

来源应标明实际使用的词典版本、可核实定位及必要现行法源。数据许可不得暗示拥有基础词典原文的许可；遵循仓库的数据许可说明。

## 6. 独立解释与中文辅助

英文释义必须是 OpenLegalLexicon 独立编写的简洁解释，不长段逐字复制 Black's 或 Oxford。基础词典用于确定 headword、sense、词形、abbreviation、cross-reference、概念边界与法域差异。

中文提供准确参考译法；必要时列多个译法，容易误解时增加中文解释。不制造与中国法概念的虚假等同。英文概念、中文辅助说明、使用语境及法域标签必须相互一致。

## 7. 法域、时代与多义项

尽量明确适用法域，例如：

`US`、`US-FEDERAL`、`ENGLAND-WALES`、`UK`、`COMMON-LAW`、`EU`、`INTERNATIONAL`、`INTERNATIONAL_TRANSACTIONAL`、`LEGAL-LATIN`、`HISTORICAL`、`ROMAN-LAW-HISTORICAL`。

必要时使用准确的其他法域标签。历史制度不得写成现行制度。UK 不能机械替代 England and Wales，也不能把英国不同地区的制度视为相同。

同一 headword 如具有 US / UK / EU / International / Historical 等不同义项，分别保留相邻 sense，不机械合并为模糊定义。只有概念边界实际一致时才可采用共同 sense。

## 8. 现行法复核与审核状态

以下类型需要额外核实现行法：

- 法律效果明显随时间变化；
- 高度法域化；
- 受新法、判例或监管变化影响；
- 旧版 Black's / Oxford 表述可能已经过时。

使用相应法域的权威现行法源核验。若核验耗时，可以先写清概念、法域和已知时间边界，并标记 `needs_current_law_review`，不中断整个批次。不得把此标记当作已经完成现行法核验。

既有审核状态含义：

| 状态 | 含义 |
|---|---|
| `baseline_concept_review` | 独立概念编审，不等于全面现行法核验 |
| `historical_reference_review` | 历史参考义项 |
| `cross_reference_review` | 来源参照或展开已检查；目标完成程度另计 |
| `needs_current_law_review` | 明确待现行法复核 |
| `blacks_baseline_review` / `migration_review` | 既有状态，不据此推断本轮重新审核 |

## 9. Oxford 与 Black's 对齐规则

当前 Oxford 阶段按源词目处理，未核实 Black's 的项目保留 `black_alignment_pending`。该标记不是 Oxford-only；暂停 Black's 不影响 Oxford 阶段写入。

用户提供 Black's 来源后，每个连续区间：

1. 读取 Oxford 该字母段及实际可访问的 Black's 对应 headwords；
2. 识别 Oxford-only、Black's-only、Both-same-sense、Both-different-sense；
3. 按法域、时代和 sense 分开处理；
4. 编写独立中英文解释，保留可追溯来源。

禁止伪造 Black's citation。未实际核实的条目不得写成“Black's 收录”。继承但未重查的 citation 保持明确状态；历史版来源不等于现代美国法核验。

Oxford 索引提取标记不得机械执行：`=` 可能是正文缩写或引用误判，`→` 须核对参照关系。保留来源中的大小写区别、完整词形和稳定源条目 ID；原提取遗漏、截断或空锚点须回查原书修复，不能制造另一个概念。

## 10. 写入前与验收检查

主 CSV 始终按英文 headword **A → Z** 排列；同一 headword 的不同 sense 相邻。每批写入前及远程提交后检查：

- CSV 可正常解析，列数与必需字段完整；
- headword 排序正确，同 headword senses 相邻；
- 条目 ID 唯一，既有 ID 不被意外丢失；
- 无意外重复记录，多 sense 有真实概念或法域差异；
- cross-reference 未被误当正式实体定义，目标可追溯；
- abbreviation 未错误展开或重复，类型与词性一致；
- 已处理源词目均有主 CSV 结果，覆盖计数按源条目核算；
- 待现行法复核记录明确列出；
- 文件修改范围符合约束，冻结及独立中文词典无无关变化，台湾来源未恢复。

## 11. 严格工程安全规则

只操作上述仓库，只更新 `main`。严格禁止：

- 创建 branch、创建 PR；
- GitHub Actions / workflow、CI；
- tag / release；
- force push、rebase / cherry-pick；
- 修改仓库权限、Secrets、ruleset、branch protection；
- sidecar 重复词典、无必要复杂工程结构。

每批以重新读取的最新远程内容为基础，尽量只产生 **1 个清晰 commit**，不制造大量碎片 commit。提交前再确认 main；如远程前进，重新读取并保留其内容，重新校验后提交，不覆盖他人更新。不得启动任何 CI 或 workflow 作为校验手段。

## 12. ChatGPT 网页版执行与验收分工

具体词目整理交由实际登录的 ChatGPT 网页版执行；验收端负责读取远程结果、检查来源覆盖与编审质量、执行上述安全和完整性验收。开发基准文档维护属于任务准备。

交接时提供本文件、实际最新 main SHA、Oxford 原书或可核实源内容、当前未处理区间及既有字段结构。不得假设网页版可读取本会话附件、拥有 GitHub 写权限或仍在后台运行。缺少登录、原书或仓库访问时明确报告依赖，不能伪造委派或执行进度。若执行端不能直接写仓库，先交付可检查的批量修改，由验收端核验后仅提交 main。

每批执行结果至少包含：连续源区间、已处理源条目数、新增及总 CSV 记录数、尚未处理队列、待现行法复核清单、验证结果与真实 commit SHA。验收失败应修正该批，不把失败结果计为完成。

## 13. 进度起点与完成标准

2026-10-02 本次文档更新前已重新读取 main，内容提交为 `00ae0081d12b8bc10dcd0f106d75d7293843210c`。这是已核实起点，不是后续批次可以跳过重新读取的固定 SHA。

已报告主 CSV 为 749 条记录、678 个不同 headwords；Oxford A 367/367、B 158/158、C 100/597，合计 **625/4,854** 已处理，**4,229** 未处理。C 上批末项为 `challenge to jury`，下一批从原书下一源条目连续推进，优先完成 C 剩余 497 项。现行法待复核 395 条，具体清单见 lexicon README。后续执行必须按实际远程文件重新核算。

Oxford 阶段只有满足全部 4,854 源词目具有合格结果、未处理 Oxford 队列为 0、法域差异保留且全部结构校验通过，才能报告 Oxford 完成。`needs_current_law_review` 可以存在，但必须明确列出，不得宣称现行法复核全部完成。

全项目最终完成还要求用户提供后可访问的 Black's headwords 已纳入、Black's-only / Oxford-only / shared 已实际对齐、全部来源未处理队列为 0。Black's 暂停期间不得把 Oxford 阶段完成称为全项目完成。

最终报告给出：总词条记录数与不同 headwords 数、各来源覆盖、jurisdiction 分布、明确待现行法复核清单、未处理队列以及最终 commit SHA。
