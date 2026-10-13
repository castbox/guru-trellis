# #530：已提交候选接续

状态：Planning；Direct Source：https://github.com/castbox/guru-trellis/issues/530。
TaskId：issue-530-clean-committed-reentry；generation：0。

## 当前事实与目标

在源码 a653c90b064e2435bc147f1bda0e1b7ab632f797，正式 TaskCommit 后 selected base 演进，post_commit Reconcile 生成正式整合提交并返回 fresh Phase 2。检查通过且 worktree clean 时，post_check unchanged 仍进入只接受非空 exact_stage_paths 的 TaskCommit prepare，阻断首次完整 Branch Review。
真实 consumer 是 backend #444；945faa4 安装提交经 Reconcile 到 e73376c，fresh Phase2 passed 后 prepare 报 exact_stage_paths schema_mismatch。该观察是缺陷复现，不是源仓修复证据。

补齐现有 TaskCommit owner 对真实当前已提交候选的正式核验和接续，保留 fresh Phase2 和首次完整独立 Branch Review。

## 范围与验收

| ID | 可观察合同 |
| --- | --- |
| R530-01 | 正式 TaskCommit→base 演进→post_commit Reconcile→fresh Phase2 passed→post_check unchanged→clean 已提交候选经 TaskCommit 正式返回既有 committed DTO，再完成首次 full Branch Review。 |
| R530-02 | 接续绑定 TaskId/generation、正式 branch/checkout、HEAD、selected base、当前 passed Phase2 anchor 与 reviewed content；不得重放旧 committed DTO。 |
| R530-03 | 接续不创建 commit、candidate、空消息、tracked 推进文件、receipt 或新持久化状态；Git HEAD/tree/index/工作区保持原事实。 |
| R530-04 | 真实 dirty 增量继续 prepare→确认精确提交→invoke 原路径。stale、再次 base 演进、finding-fix 与 fresh-final review 的 owner 保持。 |
| R530-05 | Branch Review 仍独立审查完整 selected-base...HEAD，不读取 Phase2 checkpoint、不以 bounded continuity 替代首次 full review。 |
| R530-06 | canonical Workflow/Skill contract/runtime/schema/consumer 与受管投影一致；正常链路、dirty 与 stale 回归及一个代表性安装投影有实际证据。 |

## 非目标

不修改、关闭或重新安装 backend #444，不改变其固定来源 SHA。不做 push、PR、merge、tag、Release、部署、其他资源清理或完整多平台 release matrix。#407 active MERGE_HEAD resolved-tree 恢复独立；本接续不能代替冲突恢复。
不增加 Skill、typed exit、任务阶段、业务权限锁、通用恢复框架、授权记录或长期兼容层。

## Delivery

本 Task 一次交付 R530-01..06；无隐藏剩余实现。软件发布和 backend 新候选安装是外部边界，不能据此声称本 Task 已完成。修复完成须有当前源仓证据和独立 committed full review，Planning 不预填通过。
