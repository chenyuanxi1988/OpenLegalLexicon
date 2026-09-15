# Anki 学习导入

先选学习范围：[核心学习版](../dictionary/anki_core.tsv) 有 266 条释义、532 条双向学习记录；[完整来源参考版](../dictionary/anki.tsv) 有 2,989 条可展示词条、5,978 条双向学习记录，包含尚未补全释义的来源词对。CSV 查阅版见 [核心词典](../dictionary/legal_dictionary_core.csv)。

在 Anki 里创建名为 OpenLegalLexicon 的笔记类型，字段按顺序为：`ID`、`Front`、`Back`、`Scope`、`Note`、`Source`。第七列是标签，文件头已标明。

建立一个卡片模板，正面：

```html
{{Front}}
<hr>
{{Scope}}
```

背面：

```html
{{FrontSide}}
<hr id="answer">
{{Back}}
<p>{{Note}}</p>
<small>{{Source}}</small>
```

导入 `anki.tsv` 时选择此笔记类型，使用 Tab 分隔，关闭“允许字段包含 HTML”，按列映射六个字段及 Tags。ID 保持在第一个字段，但不放进卡片模板。同一词条两个方向 ID 不同；再次导入时选择更新已有笔记。

来源地区和语境出现在正面；未核验法域显示“待核查”。原译文并列项保持在一张卡内，不宣称各译法在所有语境均适用。核心版的 Note 字段含中文释义、学习提示和译法说明，Source 字段附具体法条及网址。法律文本按版本固定，译文为项目释译；来源参考层仍未逐条补齐法律定义、例句和易混说明。两个导出使用相同的稳定 ID，可通过更新已有笔记避免核心版和完整版相互重复。

格式依据：[Anki 官方文本导入说明](https://docs.ankiweb.net/importing/text-files.html)。真实导入结果见 [验证说明](VALIDATION.md)与 `reports/`。


## 更新已有集合时处理隔离条目

导入新版只新增或更新匹配 ID 的笔记，不自动删除旧版多出的记录。0.1.0.dev4 隔离了以下两个来源词对；若曾导入旧的完整参考版，请先备份个人集合，在 ID 字段核对下列四条旧记录，再决定暂停或移除。不要按“政府公报”“申请期间”的词面批量删除，其他来源的同形记录仍保留。

| 原始词条 | 需检查的旧 ID |
| --- | --- |
| 政府公报 / Government Official | tw-judicial-d93174a9bac5c5bda259:zh-en；tw-judicial-d93174a9bac5c5bda259:en-zh |
| 申请期间 / prosecution of the application | tw-tipo-trademark-6f66fb2f4f3eef2e0b87:zh-en；tw-tipo-trademark-6f66fb2f4f3eef2e0b87:en-zh |

这些是完整参考版的来源记录，核心学习版的词条不受该次来源隔离影响。今后更新先查看[待解决质量清单](../reports/source-review-queue.json)及公开变更日志。
