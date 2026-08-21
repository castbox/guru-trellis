# #290 设计：selected-base authority checkout 路由

## 设计结论

采用两阶段确定性解析：先只依据显式参数、repo config、ordered refs 和 remote default 选择 `selected_base`；再在同一 Git common-dir 的 registered worktrees 中绑定该 base 的 authority checkout。第二阶段只验证已选 base，不得触发重选。

保持 `guru-sync-base` 为 deterministic Skill。没有新增 scope、充分性或用户选择判断；runtime 继续独占 resolve、fetch、ff-only、freshness、checker 和 typed exit 投影。

## 责任与数据流

```text
session checkout (may be detached)
  -> select_base(session repository refs/config/remote)
  -> bind_authority_checkout(common-dir worktree list, selected_base)
  -> resolution digest(authority branch/head/clean identity)
  -> explicit fetch in authority checkout
  -> merge --ff-only in authority checkout when behind
  -> validator(authority checkout + local ref + remote ref)
  -> base_current.repo_locator = authority checkout
  -> guru-discover-change-context
```

### Base selection

- 保留 `explicit -> config scalar -> ordered candidate -> remote default`。
- candidate existence 仍只看 exact local 或 remote-tracking ref。
- selection 完成前不读取 worktree availability；selection 完成后不再求值低优先级来源。

### Authority binding

- 通过 `git worktree list --porcelain` 读取当前 Git common-dir 已注册 checkout。
- 唯一合法候选必须绑定 `refs/heads/<selected_base>`。
- 校验候选目录是 exact repository root、symbolic branch `==` selected base、HEAD `==` local branch ref、worktree clean。
- missing、dirty、identity mismatch 使用稳定 `CommandError`，由 public owner 映射为 `blocked`。
- 不调用 `git checkout`、`git switch`、`git branch` 或 `git worktree add`。

### Digest 与执行

- pre-sync resolution 保留现有 schema/version 和 selected-base provenance；其中 `decision_checkout` 的语义明确为 base authority checkout，而非 session checkout。
- authority path 是 invocation-local routing fact，不加入持久化 artifact；public transition 的既有 `repo_locator` 字段承载实际 authority checkout。
- executor 从同一 resolver 重新得到 selected base 和 authority checkout，比较 exact pre-sync digest 后才 fetch。
- fetch 使用 `refs/heads/<base>:refs/remotes/<remote>/<base>`；仅当 local behind 且为 remote ancestor 时由 `merge --ff-only` 前进。
- checker 在 authority checkout 上验证 clean 与 `HEAD == local == remote`；不在 detached session 上做错误 equality。
- downstream `guru-create-task-workspace.reviewed_base_freshness` 必须按 provenance
  `source` 对四级 live authority 做 package-local revalidation：explicit 绑定既有
  `--base-branch` assertion，config/config-candidate 绑定当前 config 与 exact refs，
  remote-default 绑定当前 remote HEAD。current source、selected base 与完整 candidates
  必须分别 exact 等于 transition provenance；`prepare()` 不得在 freshness 前再执行一次
  config-only resolution。

## 兼容策略

- 保持 `guru-base-sync-result-1.0`、`public-synced-output-2.0`、`synced/skipped/blocked`、consumer 和 transition shape。
- `decision_checkout` 字段改为其既有合同本来要求的 selected-base decision authority；不增加 dual-read 或 schema 兼容分支。
- current checkout 已在 selected base 时，authority resolver 返回当前 checkout，现有成功路径保持不变。
- downstream 继续读取 `transition.base`；唯一行为修正是 `transition.repo_locator` 和 handoff repo locator 在 detached session 场景指向实际 authority checkout。

## Canonical 与投影

Canonical owner 位于 `trellis/skills/guru-team/packages/guru-sync-base/`。修改 contract、runtime、tests/evals 后，通过 preset `apply.sh --repo .` 同步 `.trellis/guru-team/skills/packages/`、`.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 五类声明投影，再运行 dogfood overlay drift 检查并确认无 `.new/.bak`。

## Architecture change contract

- `impact_kind`: `architecture_impact`。
- `change_path`: `target_native`。
- Current boundary：session checkout 同时承担 invocation 与 selected-base decision checkout。
- Target boundary：session 仅负责调用；base authority checkout 唯一负责同步；Trellis task workspace 只承载 task change。
- Current/target semantic owner：`guru-sync-base` deterministic runtime；task writer 为 `290-detached-base-authority-checkout`；shared current single-writer 为 Architecture/RDT promotion owner。
- Compatibility exit：不存在 legacy dual-read；旧的 session-branch coupling 在本 task 完成后删除。
- GAP：task 内关闭 detached normal-path routing gap；不修改或关闭 `ARCH-GAP-001..005` 和 `#267`。
- Parallel scope：task worktree 内只修改 canonical `guru-sync-base` producer、受影响的
  `guru-create-task-workspace` freshness consumer、对应 managed projection、task-owned
  Architecture/RDT contribution 和 #290 测试；禁止直接竞争 shared current，promotion
  串行执行。
- ADR：需要，记录三种 checkout identity 与 selected-base-first 绑定决策；不复制 Issue 或 constitution 正文。

## 风险与缓解

- 选 base 后误回退其他 checkout：用两阶段 API 和显式缺失测试阻止。
- authority path 漂移：resolve/execute 共用 resolver，checker 对实际 authority root 复核。
- selection provenance 漂移：producer/consumer integration test 分别把 explicit override、
  ordered `dev -> main` 与 remote-default transition 交给 workspace freshness consumer。
- schema 意外破坏：保留 closed schema，增加 compatibility assertions 和真实 public wrapper 测试。
- installed/platform 漂移：canonical 后 reapply，执行 drift、inventory、mode 和 equality checks。
- 验证范围膨胀：只运行 `guru-sync-base` package contract/runtime/eval、dispatcher/schema/manifest regression、preset reapply/drift、声明平台 projection equality 与一个代表性 detached worktree；完整 release matrix 留给 `#267`。
