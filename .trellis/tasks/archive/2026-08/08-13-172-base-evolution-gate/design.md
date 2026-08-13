# 技术设计

## 架构

```text
eligible boundary
  -> package-local deterministic pair guard
     -> unchanged/current pair: resume_target (no semantic invocation)
     -> new pair: guru-reconcile-task-base semantic owner
        -> reconciled: thin router -> original resume_target
        -> review_continuity_required: guru-review-branch bounded profile
        -> implementation_required: implementation -> guru-check-task
        -> planning_stale: Planning
        -> scope_confirmation_required: guru-clarify-requirements
        -> blocked: stop
```

Global workflow 只编排 boundary、mandatory invocation 与 exit consumer。新 package 独占 entry、semantic loop、candidate validation、private state、freshness 和 typed outputs。现有 owner 仅保留自己的语义结论，并通过最小 projection 与 Gate 交互。

## Pair Guard

Guard 作为 `guru-reconcile-task-base` package 的 deterministic command，输入由 boundary consumer 提供：task ref、task head、selected base ref、上次已消费的 base anchor、`resume_target`。Runtime 从 live Git 读取 current base head并形成以下客观结果：

- `unchanged`：current base 等于 caller anchor，直接恢复 route。
- `current_pair`：同一 pair 有尚未消费且 identity 精确匹配的 private result，投影其 exit。
- `new_pair`：形成唯一 `(task_head, old_base_head, new_base_head, resume_target)` semantic invocation input。
- `blocked`：non-ancestor/history rewrite、缺失 anchor、task/base identity 不唯一或 private state 不可验证。

Guard 不生成同义词、路径语义影响、impact、validation plan、finding 或 pass。它不 fetch selected base，不 fast-forward decision checkout；active task 的 live ref observation 与 pre-task `guru-sync-base` 分工明确。

## Semantic Owner

`guru-reconcile-task-base` 的 owner result 分层记录：

1. `authority_impact`：live authority/Docs acceptance 是否改变。
2. `task_content_impact`：base delta 是否要求修改 task planning/code/docs/tests。
3. `integration_impact`：临时 candidate 是否可形成、冲突类型、受影响验证与 continuity necessity。

Owner 先读 `semantic-retrieval.md`，再构造最小概念族；runtime 只执行 AI 给定的 Git diff/candidate/validation commands。AI Gate 绑定 pair、reviewed scope、关键 delta、验证充分性、findings、未验证边界与唯一 exit。

临时 candidate 使用受控临时目录或 detached worktree，由 executor 创建并在 owner完成后清理；不修改 task branch，不创建持久 branch/ref/commit。命令必须通过 closed schema 输入，拒绝任意 shell 字符串作为 route authority。

## Public I/O

输入按真实 caller profile 分离，不定义大量 optional 字段的总 DTO。每个触发 Gate 的 profile 必须包含：

- boundary profile 与 exact `resume_target` enum；
- task ref 与 task-content HEAD；
- selected base ref、old/current base HEAD；
- caller 当前语义结果的最小 identity（仅当 Gate 必须判断其 continuity）。

六个 output schema 分离。`reconciled` 只携带 router 无法重建的 pair identity 与 `resume_target`；其余 exit 只携带对应 owner 必需的 task ref、pair/finding refs 或 scope reason。Producer-to-consumer projection 在 `interface.json` 中显式声明并由 registry validator 校验。

## Boundary 集成

一个 workflow-owned router 定义所有 boundary 的 `resume_target` 闭集。每个现有 producer exit 先投影到 guard input；guard no-op 或 `reconciled` 恢复原 target。Mapped exits 自动承接，不向用户显示 exit id，不请求通用确认。

Finalizer 增加独立 `base_reconciliation_required` output/input route。`publication_review_stale` 只保留 PR title/body、issue scope、validation statement 或 deployment/security metadata 自身过期。Publication 不再接收 base-only mismatch。

## Bounded Continuity

`guru-review-branch` 增加独立 input profile 和 authoring seed：

- 输入绑定既有 passed task-review content HEAD、old/new base、candidate identity 和由 semantic-retrieval SSOT 判定命中的 delta。
- Review Gate 仅审查 delta 对 task scope 的影响、candidate、冲突解决与受影响验证。
- finding lifecycle 继续归 Branch Review owner。
- pass 输出 integration pair current identity，不重写 task semantic review checkpoint。

如果 continuity 发现 task bytes 必须改变，则返回现有 `implementation_required`；planning/authority 变化通过新增或既有最小 projection 到其 owner，不能在 Branch Review 私自解决。

## Private State 与迁移

Pair checkpoint 位于 task-local ignored owner namespace，内容仅保留下一个 boundary consumer 无法重建的 pair、exit、resume target 与最小 validation identity。正常 consumer 成功后删除；unfinished/replacement recovery 才保留。

迁移 adapter 只读 current legacy context/review/publication/finalizer state：

- 有旧 base anchor时形成首次 pair；缺失时做一次完整但有界的 initial reconcile。
- 同一 task-content HEAD 的旧 Branch Review pass 可保持 task review validity。
- legacy `publication_review_stale` 按 current stale reason 分流，base-only 转新 route。
- 不写 tracked compatibility artifact，不批量更新 active tasks，不读取其它 package private state。

## Canonical 与 Installed 投影

1. Canonical Skill package：`trellis/skills/guru-team/packages/guru-reconcile-task-base/**`。
2. Canonical registry/workflow/spec/preset installer 持有 public graph 与 managed inventory。
3. `apply.sh --repo .` 同步 `.trellis/guru-team/**`、Shared/Codex/Claude/Cursor skill copies、dogfood workflow/spec 与 platform overlay。
4. Workflow marketplace仍只安装 `.trellis/workflow.md`；完整 runtime 由 preset 安装。
5. 平台 entry 只引用 workflow/Skill，不复制 guard或impact classification。

## 测试设计

- Package unit/contract：schema、projection、guard、candidate、private state、migration 与六 exits。
- Semantic eval：Issue 状态矩阵全部场景，断言 evidence/route，不以关键词或 wall-clock 计数代替判断。
- Stateful integration：真实 producer stdout 投影到 guard/Gate/consumer，覆盖所有 eligible boundaries。
- Performance fixture：精确统计 live ref、GitHub/Docs/history、semantic invoke、artifact 与 interaction 次数。
- Historical replay：在 current runtime 重建 #132/#161 合法事实，不写假 state、不复用旧 digest authority。
- Distribution：source/installed/package/platform discovery、registry graph counts、apply/reapply/update/upgrade、`.new/.bak`、drift、marketplace init/preview/switch。

## 风险与回滚

- 风险：guard 偷渡 semantic route。控制：guard result 只含客观 pair state，semantic scenarios 全部由 owner eval 审查。
- 风险：为每个 boundary 复制逻辑。控制：单 guard/input authoring/projection 和单 router target table。
- 风险：破坏既有 public API。控制：新 schema/profile/exit id 与显式 migration，不静默改旧 schema bytes。
- 风险：跨 package 读取 private runtime。控制：consumer contract tests 与 source scan 阻断 private path import/read。
- 风险：installed/dogfood 漂移。控制：canonical-first、apply、managed inventory 和 clean throwaway验证。
- 回滚：在尚未发布前按 task diff 回退新 package/router/migration；不涉及数据库或外部数据。已发布后按 public API migration 新版本回退，不删除旧 schema compatibility assets。
