# Guru Team Trellis AI-first Workflow 验收要求

本文定义稳定的产品验收要求，不展开 recorder 参数、schema 字段清单或逐平台复制内容。
执行细节由 canonical workflow 和各 Skill package 独占。

## 1. 架构与 SSOT

1. `.trellis/workflow.md` 只拥有 phase 顺序、mandatory Skill 调用、typed exit consumer
   和 fail-closed stop。
2. 每个 active `guru-*` Skill 独占 entry、AI judgment、必要的人类授权、recorder / validator
   和 re-entry 合同。
3. Platform command、prompt、breadcrumb 和 `trellis-start` 只加载 workflow 与路由，不复制
   Step-local 流程。
4. Python / shell 只执行、记录或校验确定性事实，不决定 scope、finding、pass 或 publication
   readiness。

## 2. 交互预算

一个已完整展示、current、unique、unambiguous 的 proposal 或 side effect，只提示
`确认继续`；任意明确肯定回复均授权该已展示动作。内部 evidence 仍绑定 exact target、HEAD、
scope、authority 和 digest，但不得要求用户复述 SHA、digest、proposal 原文或固定句式。

Scope expansion、post-planning approval、commit、push、PR、merge、Issue mutation 和 cleanup
仍是不同的 authority boundary。共享 prompt 不代表共享授权。只有 target、HEAD、scope、
authority、可选项或 side-effect plan 改变时才重新展示并确认。存在多项选择或歧义时必须提出
真实问题，不能用通用确认替代。

Mapped exits、stale、re-entry、reprepare、recorder/checker 和 same-plan recovery 由 AI workflow
自动承接，不向用户暴露为 routine handoff 或“确认继续”。

## 3. Planning 与 Intake

Repo-changing intake 先 mandatory invoke `guru-sync-base`，再按 global workflow 进入 current
Skill chain。Intake clarity 可使用 `trellis-brainstorm` 的单问题方法，但最终 scope、GitHub
action 和 route 仍由 owning Skill 判断。

创建 Issue、worktree、branch 或 task 前必须展示真实目标和副作用。Planning 保留
`prd.md`、`design.md`、`implement.md`、Docs SSOT decision 与独立 post-planning approval，
因为这些内容有直接实现消费者。最终 close/ref/follow-up 只由 `issue-scope-ledger.json`
持久化。

## 4. 实现、Phase 2 与恢复

Implementation 与 official `trellis-check` 的 terminal result 是 AI 的直接输入，不生成
`implementation-handoff.md`、routine assignment、routine liveness 或重复 completion prose。
`guru-check-task` 保留完整 task scope、adequacy、Docs SSOT 和 finding judgment，并只持久化
最终 `phase2-check.json`。

只有 agent 真实 unfinished 且必须 replacement 时，才在 gitignored runtime 保存最小 recovery
checkpoint。正常 completion、wait timeout、mapped re-entry 和 fresh dispatch 不写 recovery
artifact。

## 5. Task Commit

`guru-create-task-commit` 的 candidate 位于 gitignored owner-private runtime。Git 可推导的
commit SHA、tree、parent、message 和 path facts 不回写 tracked handoff。成功后删除 candidate，
不得在 commit 后向同一 tracked plan 写 `committed/result/tree_evidence`，因此正常 commit 不会
主动制造 post-commit dirty。

既有 active task 中的 tracked schema 1.0 commit plan 只读兼容，不原地升级；下一次合法
re-entry 使用 ignored candidate。历史 archive 字节保持不变。

## 6. Branch Review

Branch Review 保留 qualification-first、完整 `origin/<base>...HEAD` 审查、current-scope P0-P3
finding、scope proposal、closure 和 fresh final review 的语义价值，但新流程只持久化 compact
`review-gate.json`。

初次 open finding 返回 `implementation_required`。Fix 通过 Phase 2 并产生新 commit 后，finding
owner 或真实 unfinished-agent replacement 在 AI 内部完成瞬态 closure：保留原始
`introduced_head`，把 `resolved_at_head` 绑定 fix commit，并给出 concrete closure evidence。
Closure 不产生 public exit 或 artifact；workflow 立即调度不同的 fresh final reviewer 完整审查
当前 range。只有 `fresh_final_review` 可以写最终 compact passed gate。

新 public input schema 1.1 只允许 `initial_review|fresh_final_review`。旧 schema 2.0 gate 中的
`finding_fix_review`、assignment 和 raw reports 仅只读；active task re-entry 在内存完成 closure，
再生成 1.1 fresh-final input，不改写旧 evidence。正常
finding -> fix -> closure -> fresh final 路径不得出现 validator 自相矛盾、逐轮文书或通用确认。

## 7. Publication 与 Finalization

`guru-review-task-publication` 保留 Issue closure、PR body、验证、安全、部署和 release readiness
判断。`guru-finalize-task` 以一个已确认 plan 驱动 push、条件 marketplace verification、Draft PR、
archive transaction 和 Ready；内部 recovery exit 自动承接。

Schema 1.1 archive 长期保留 11 个有直接 history/recovery consumer 的 core files：task identity、
三份 planning、scope ledger、planning approval、Phase 2、compact review gate、closeout plan、
finalization gate 和 finish summary。适用 verifier 时 `marketplace-verification.json` 是第 12 个。
Raw rounds、legacy rollup、commit candidate、PR preparation 和其他可从 exact evidence commit 或
GitHub authority 推导的 checkpoint 不复制进 archive。

## 8. Distribution 与升级

每次 workflow、Skill、runtime、preset 或 overlay 修改都必须同步 canonical、dogfood、Guru
namespace 和声明支持的平台副本，并验证：

- source / installed package、schema、mode 与 executable bit；
- clean marketplace install、workflow preview/switch 和 preset install；
- `trellis update` / upgrade 后 preset reapply；
- user-modified 文件产生受控 `.new/.bak`，不静默覆盖；
- dogfood drift、all-platform equality 和 owner manifest；
- README 命令可执行且不依赖本机隐藏状态。

## 9. 非目标

本轮不扩展 malicious actor、伪造、并发竞态、锁、TOCTOU、额外 fault injection、跨 OS crash
consistency；不重新实现或重新审核 #116/#117/#118 Skill 内部行为；不修改、关闭或提前实现
#119/#132。冻结的 #119 worktree 只作为正常路径回归输入，必须保持字节和 Git 状态不变。
