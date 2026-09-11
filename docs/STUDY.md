# Anki 学习导入

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

来源地区和语境出现在正面；未核验法域显示“待核查”。原译文并列项保持在一张卡内，不宣称各译法在所有语境均适用。目前尚未逐条补全法律定义、例句和易混淆说明。

格式依据：[Anki 官方文本导入说明](https://docs.ankiweb.net/importing/text-files.html)。真实导入结果见 [验证说明](VALIDATION.md)与 `reports/`。
