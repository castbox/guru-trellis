# ADR-006: selected-base authority checkout routing

状态：`accepted`。Owner：Issue #290。Predecessor：无。经 exact committed range
`ec4df880…d4165f26` 的 independent Branch Review 与 expected `.38` serialized
promotion 进入 `.39` shared-current authority。

## Context

Codex session 可以从 detached worktree 启动。现有 `guru-sync-base` 把 session
checkout 同时当作 base selection shell 与 decision checkout，因而要求 session 自身
绑定 selected base。该耦合使正常 detached session 在同一 repository 已有 clean
selected-base checkout 时仍失败。

Base selection 已有固定 authority precedence：explicit、config scalar、ordered
existing refs、remote default。现有 worktree 不能改变这个 precedence，也不能在已选
base 缺 checkout 时触发其他 candidate fallback。

## Decision

`guru-sync-base` 使用两个顺序固定的确定性阶段：

1. selection 只根据 explicit/config/ref/remote-default authority 确定
   `selected_base`；
2. binding 只在同一 Git common-dir 的 registered worktrees 中查找绑定
   `refs/heads/<selected_base>` 的 exact clean checkout。

Session checkout 只负责调用并允许 detached。绑定后的 base authority checkout 独占
fetch、`merge --ff-only`、clean 与 `HEAD == local ref == remote-tracking ref` 验证。
Trellis task workspace 继续由独立 workspace gate 创建。

Binding missing、dirty 或 identity mismatch 返回稳定 `blocked`；系统不 checkout、
switch、创建 branch/worktree，也不重选低优先级 base。resolve、execute、validator
共享同一 resolver 和 freshness chain，public `repo_locator` 指向实际 authority
checkout。

## Consequences

- detached session 成为受支持的 invocation shell，不再承担 base synchronization。
- current checkout 已绑定 selected base 时仍解析为同一 authority root，保持成功路径。
- public schemas、`synced/skipped/blocked` exits 与 downstream consumers 保持不变。
- runtime 必须读取 registered worktree inventory，但该 inventory 只服务 selection 后的
  exact binding，不成为 selection authority。
- selected base 没有合法 authority checkout 时流程 fail closed；自动创建 checkout 或
  fallback 属于明确非目标。

## Rejected alternatives

- 让 detached session 临时 checkout selected base：产生未授权 Git mutation，并混淆
  session 与 authority identity。
- 按现有 clean worktree 选择 base：改变既有 precedence，可能把 explicit/config base
  静默降级为 `main`。
- 为旧 session-branch coupling 增加 dual-read：形成第二 authority 与无退出兼容路径，
  不符合 `target_native`。

## Verification and promotion

Acceptance 由 #290 package/runtime/eval、schema compatibility、managed projection、
preset reapply/drift 与一个代表性 detached wrapper 正常路径共同验证。完整 release
matrix、tag 与 GitHub Release 仍由 #267 独占。

本 ADR 已绑定 #290 independent committed full-diff Branch Review 与 expected Architecture
identity `current-main-0.6.5-guru.38`，由 serialized promotion 接受为 `.39` current。
promotion-created diff 仍必须重新通过 Phase 2、task commit 与独立 Branch Review。
