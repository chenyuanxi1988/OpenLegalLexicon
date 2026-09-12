# 数据结构

`data/snapshots/*.jsonl` 保存原词对和原行号；`data/sources.json` 登记许可、快照版本和摘要；`data/annotations.json` 保存编审字段。原始词对不因转换或纠错被覆盖。`schema/*.schema.json` 采用 JSON Schema 2020-12，未知字段、版本、分类和缺失来源会报错。

源数据从原计划 YAML 改为 JSONL：一行一条便于差异审查，禁止重复 JSON 键，避免 YAML 锚点/隐式类型的输入歧义。YAML 仅用于 Rime 必需的导出。标准化词条由固定版本程序与快照生成。

| 字段 | 含义 |
| --- | --- |
| id | 来源 ID + 对原文、译文和提供单位的内容摘要；不是跨法域概念 ID |
| forms | zh_Hant 原始繁体、zh_Hans 机器转换、en 来源英文原栏；仅统一 NFC 和空白 |
| script_conversion | 转换方法、审核状态；t2s 只做文字转换，不做地区词语替换 |
| source_origin | 资料提供机构地区 |
| jurisdictions / jurisdiction_basis | 概念适用法域及依据；未核验时空数组和 not_assessed |
| legal_status | 法律时效状态；当前未逐项核验，下载日不是法律生效日 |
| domains / domain_basis | 领域及来源分类、自动规则或编审的依据 |
| kind / kind_basis | 术语、法规、机构、角色、文件、动作或缩写；不明确时 unclassified |
| alignment | source_association 表示原表中的对应，不默认 exact_equivalent |
| pronunciation | 普通话声调数字、无调拼音和生成方法；非纯汉字栏不猜注音 |
| references | 来源 ID、原记录编号、页面、提供单位/语境、来源公布的更新日期 |
| scope_note / learning_note | 来源范围说明与学习注释；无注释保持为空 |
| relations | related、contrast、abbreviation_of、replaced_by；必须指向存在条目并附依据 |
| review / status / flags | 提取验证、译文审核、隔离状态及附注/模板等质量提示 |
| license | 本条的原数据许可，与来源登记一致 |

同一来源、原文、译文、提供单位完全相同的行可以合并，原行号全部保留。不同来源、译法或语境不会因同名自动合并。简体转换出现同形词时报告冲突组。Rime 聚合相同“文字+拼音”时，在索引文件中保留所有条目 ID。

上游修正原词对时内容 ID 改变，需核对旧 ID、更新 annotation 和关系并记录替换原因；程序拒绝悬空 annotation。仅排序或分页变化不影响 ID。新增结构版本须提供迁移，当前只接受 1.0.0。

关键词分类只是初始标注，存在歧义。拼音对“行政、行为、会计、银行、重复、处分”等保持词组边界，避免把“视同行政”切成“同行”；未覆盖多音字仍需复核。当前普通话拼音不包含台湾国语差异、粤语或 ASR 实测发音。

私有词库叠加与语音误识别纠正尚未实现；客户和未公开案件资料不进入公开数据。


## 1.1.0：法条证据与原创释义

规范条目新增 `definition_zh`、`translation_note` 和 `evidence`；原来源词对为这三项提供空值，不虚构缺失内容。`evidence` 每项包含 document_id、articles 和 supports。支持字段仅用于中文释义、法域、学习提示和关系，不伪装为英文官方译文证据。

数据源支持 `format=editorial_seed`：以精简的原创记录生成规范条目，使用稳定的 cn- 概念 ID。源文件仍执行 SHA-256 和条目数核验。英文字段审核状态 `project_authored` 与原表 `source_attributed` 分开；`evidence_linked` 需具备释义、法条及具名编辑记录。

非空法域必须有匹配法域的证据，释义和学习提示必须声明证据支持；不存在的条文、被修改的法条文本摘要及未登记的文档都会使校验失败。所有法条证据随构建导出。build.json 的 evidence_registries_sha256 按路径记录实际加载的 laws.json 与全部 laws-*.json 的 SHA-256；保留 evidence_sha256 作为首批 laws.json 的兼容字段。下载目标配置不属于已加载法条，不混入此摘要映射。简体原创记录使用 OpenCC s2t 转换繁体，原繁体记录仍使用 t2s；两者都不进行法域词汇本地化。
