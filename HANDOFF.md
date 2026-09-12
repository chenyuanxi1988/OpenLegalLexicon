# Codex / ChatGPT 交接入口

这是仓库的续作说明，面向接手本项目的任何助手。聊天用于讨论，GitHub `main`、当前数据、CI 和本文件用于交接；不要依赖某个分享链接能够实时更新，也不要使用旧聊天里的未提交 tree 覆盖新主线。

## 接手先做什么

1. 使用 GitHub 插件读取最新 `main` 提交及 `COORDINATION.json`，然后读 `PROGRESS.md`、`WORK_LOG.md`、README 与 `AGENTS.md`。
2. 确认最新源码提交的 CI，以及对应自动生成文件是否真的发布；仅有“工作流成功”不代表在并发更新时已生成当前下载版。
3. 依下节认领主线写入权，并把本地工作副本同步至刚读取的版本。旧的未提交修改先另存，逐项重放仍有必要的差异，不用旧文件整体覆盖最新文件。
4. 从实际待办继续。已存在的快照、证据、编审注释和测试不重复创建；旧日志中的“下一步”可能已经完成，需查实际提交。

## 主线协作规则

`COORDINATION.json` 是双方约定的工作登记，不是 GitHub 提供的服务器锁。只有记录中的当前持有人提交人工源码/数据改动到 main；其他助手可以研究、审阅或准备独立分支。自动构建任务只写其已授权的生成路径。

认领时同时更新 owner、claim_id、task、base_commit、updated_at 和 lease_expires_at。每次使用新的唯一 claim_id，租期为 45 分钟；持续工作者每 20 分钟或阶段提交时刷新租期。所有时间使用 UTC。读到他人未过期认领时，继续独立的只读研究，不同时写同一主线。用户明确要求接手，或租期已经过期，均可重新认领；不需要等待因额度中断而无法回复的上一个助手。

认领和提交必须使用最新父提交及 `force=false` 更新 main。两个助手同时认领时，只有成功写入并再次读回自己 claim_id 的一方算认领成功。提交前重新读主线和认领记录：如果 owner/claim_id 变了，停止主线写入；如果只是 CI 或其他提交推进了 main，先读差异、保留新内容，再基于新父提交重建本批改动。不要只换父 SHA 就推送旧 tree。

额度将尽或本轮结束时，优先保存小型源码检查点、进度和下一步，释放 owner。若额度突然耗尽来不及释放，45 分钟租期让下一位能恢复；已完成内容以远端 commit 为准。未推送的本地文件不列为对方已拿到的成果。

## 当前续作路线

已存在四批共 218 条核心学习词条及两套共 2,730 条来源参考记录。来源参考层的编审队列工具、自动刷新流程和前两批注释也已存在；不要重复从 99 条或“队列尚未提交”开始。

先核验来源参考编审提交 `ab9a10b62de304688da9889985caa9097c8280ee` 及其后续 CI/下载版。接着读取实时生成的 `reports/source-review-queue.json` 和 `data/annotations.json`，处理尚未复核的候选。已复核分类不等于已核验译义、法域或释义，按字段记录证据。

后续完成范围仍以 PROGRESS 的必须交付清单为准，包括来源参考复核、机构/法规/程序/缩写覆盖、私有词库叠加、Qwen3-ASR 实际接口与音频评测，以及最终发布审计。

## 环境与验证

普通查询和构建使用仓库快照，安装依赖后可以离线工作。不要依赖上一位助手的电脑路径。

```sh
python -m pip install -e '.[dev]'
oll validate
python -m unittest discover -s tests -v
oll build --out build/handoff-check
python tools/publish_dictionary.py
python tools/publish_dictionary.py --check
```

真实 Rime 和 Anki 的依赖、命令以 `.github/workflows/ci.yml` 与验证工具为准。接手环境若无法本地执行，提交源码后通过 GitHub Actions 验证并读取真实日志；没有执行的测试明确标为未运行。大体积 dictionary 文件由 CI 生成，不手工通过插件逐个上传。

每批更新 README、PROGRESS、WORK_LOG 和必要的验证文档。保存：基准提交、改动文件、实际执行的检查及结果、未完成项、失败原因、下一项可执行动作。断点不能只记录“继续努力”或一个未落地的 tree SHA。

## 可发给接手对话的消息

> 请继续开发 chenyuanxi1988/OpenLegalLexicon。先用 GitHub 插件读取最新 main 的 HANDOFF.md、COORDINATION.json、AGENTS.md、PROGRESS.md 和 WORK_LOG.md，核验实际提交与 CI；按交接规则认领并接手。不要覆盖新主线、重复已完成批次，或把未执行的测试说成通过。完成一个可验证批次后更新文档并提交，再继续整体目标。

这个消息由用户在希望切换时发出即可。本仓库不保存私人聊天链接、账号授权材料或本地私有项目内容。
