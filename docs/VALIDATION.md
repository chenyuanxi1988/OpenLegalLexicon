# 验证记录与复现

## 已执行

- macOS arm64 / Python 3.12：全量来源、摘要、结构及关系校验通过。
- 18 项测试通过：缺页、变更列、CSV 引号、重复键、数据被修改、重复 ID、悬空关系、许可不匹配、无依据法域、读音边界、隔离条目、导出追溯、TSV 往返、命令退出码与重复构建。
- 两次相同配置构建的所有文件 SHA-256 一致。
- librime 1.11.2：简体、繁体词典真实编译；7 组无空格/单引号分音节的输入返回预期候选，见 `reports/rime-2026-09-11.json`。

原始输入法方案用 table_translator 时虽然能编译，却无法查到多音节词。改用 script_translator 后通过。空格是候选选择键，不作为音节间键；单引号用于分音节。

输入法测试创建独立临时用户目录，不读取或更改用户的实际词典与配置。C API 检查代码见 `tests/rime_smoke.c`。

## 复现

```sh
python -m pip install -e '.[dev]'
oll validate
python -m unittest discover -s tests -v
oll build --out build/verify-1
# Linux 上先安装 librime-dev、librime-bin 和 C 编译器：
python tools/verify_rime.py --bundle build/verify-1 --out build/rime-test.json
```

macOS 可用已安装输入法自带的 rime_deployer 和 librime 动态库，通过 `--deployer`、`--library` 指定路径；`--include` 指定对应的 rime_api.h 所在目录。头文件取自 Rime 官方仓库，未将第三方头文件复制进本项目。

CI 已配置 Python 3.10 / 3.12 校验，Python 3.12 作真实 Rime 检查；远端是否实际执行成功以 GitHub Actions 记录为准。

## 仍未证明

这些结果证明工程管线与已测输入法行为，不证明 2,730 条词对的法律含义都准确、全部分类都正确，也不证明任意输入法兼容。多数领域分类和所有普通话读音仍属于自动生成。原词表的历史机构、旧法与外国制度需要逐条复核。

Anki 导入、跨法域释义补全、私有词库叠加、Qwen3-ASR 真实模型调用与语音识别效果的评测仍在继续。未运行的项目不会标成通过。
