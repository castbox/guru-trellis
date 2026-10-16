# #575 S1：来源与公开映射设计

本文件拥有 S1 的长期机制；需求读 requirements.md，实际结果只读 test.md。整体 Task 的原生切换与后续交付机制由原 workflow 和 maintenance contracts 拥有，此处不复制算法。

## D575-S1-01 / CON575-S1-01：唯一来源与实际消费

唯一 source record 为 `trellis/presets/guru-team/source/trellis-source.json`。本切片采用 Fork `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0` / tree `41ff285d857036324e480e1eb64d08fffd5956e1` / ordered parents `138961cbcac8367d15abe3d9d2f06101fa921cf6`、`e28e44b7d45533584732aad74fd869a8bec7b466` / main CI `38851816688`，CLI/Core `0.7.0-castbox.3`，package manager `pnpm@10.32.1`。

根 README 的构建入口从该 record 读取 commit 和 repository，依次核对干净源码、取得精确 ref、固定 HEAD、安装/build，成功后才写 `.guru-source-commit` 并执行实际 CLI。生产 `validate_fork_source` 核验 Git/source/模板/build/CI，maintenance `inspect_source` 核验匹配 CLI/Core bytes 与 API1.0。两者只提供事实，不选择任务、审批或发布。

正式 tools 操作还要求 Guru canonical source clean committed；S1 的未提交源码不能通过该前置。公开文档不把预览拒绝当作安装成功，也不通过 local_candidate 或伪写来源来解除它。

## D575-S1-02 / CON575-S1-02：四轴和历史边界

稳定发布 `v0.7.0-guru.3` 的 Guru tree 与其 Fork lock `5c760463680ffc10a3f26957b330c57a4b0c3ff8` / CI `37735554354` 属于原 immutable tag。当前未发布源码采用新的 Fork lock，manifest 暂保留 `.3` 以符合原 maintenance target consumer；它不能被描述为已发布 `.3` tag 的新内容。

下一发布目标为 `.4`。切换工具/所选 Task 后，最终 `.4` extension 和原 maintenance revision assertion 由后续切片同步推进。源码试用的 workflow marketplace 与 preset 必须来自同一真实远端完整 Guru SHA；稳定安装使用同一真实已发布 tag 和该 tag 的 Fork lock。不存在的 `.4` tag 不是 provider。

三份 README 与 public-docs spec 只修订当前来源/发布映射；旧 development pair、旧版本与 #495/#503 的 exact-source 验收保留为历史，不改写成新源证明。知识版本来自四层 READMEs，与软件版本分离；孤立贡献不晋升 shared authority。

## D575-S1-03 / CON575-S1-03：独立切片与原 owner

首切片的独立效果是可提交、可构建、可读取的正式 source/doc 映射。旧 installed graph、源/安装投影差异与 M/S2 明确保留，不被称为已经迁移或最终 parity。

实际后续采用沿 [task-delivery migration](../../../trellis/presets/guru-team/spec/workflow/task-delivery-migration.md) 和 [独立维护边界](../../../trellis/presets/guru-team/MIGRATION-566.md)。原 tools owner 管工具/受管资产，公共维护管 Task/session/binding，原 Publish/Merge 与 private owners 管历史事实和 controls；下一 native consumer 和 Creation 决定实际新 Delivery。这里不新建恢复状态、适配器或 gate。

RDT 本贡献和 task Architecture 候选经过首轮完整 committed 独立 Review 后，才由原 owners 按 expected-current 串行晋升。晋升差额重新 Phase2/commit/完整独立 Review。后续切片使用独立贡献定位，不改写本切片晋升历史。S1 Publication 必须列出剩余义务；整 Task Completion、Closure/Finish 与 release Stage2 各由原 owner 判断。
