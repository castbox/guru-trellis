# Guru Team Preset

The [common causal authority](./spec/workflow/causal-completion-semantics.md)
is installed at `.trellis/spec/workflow/causal-completion-semantics.md` through
the existing managed-spec installer. Qualification and stage packages read
that one source; apply/reapply distributes their stage-local contracts.

Normal revision/recovery contracts live in `guru-check-task` and
`guru-review-task-delivery`; apply/reapply projects those canonical packages
to installed and platform copies. Targeted validation proves those projections;
it does not replace the cumulative Upgrade/Release matrix.

This preset installs the companion assets and current Skill packages for the
`guru-team` canonical workflow into an existing Trellis project. The
canonical package source is `trellis/skills/guru-team`; installed packages,
Shared/Codex/Claude/Cursor skills and finish entries are managed projections.
The installer never edits upstream Trellis source or a global npm package.

Architecture review uses the existing
[canonical Skill](../../skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md)
and its [step-local contract](../../skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md).
New conclusions use fresh independent subagents; platform entries load and
schedule that same contract. Install/update must reapply the matching complete
preset so canonical, installed and selected platform copies use the same method.
Projection checks and actual native behavior are separate evidence; current
#404 coverage and limitations live in its [unique Test](../../../docs/requirements-design-test-contributions/404-independent-architecture-review/test.md).

## Apply And Verify

本次 repository 正式发布目标为 `v0.7.0-guru.3`，extension 为 `0.7.0-guru.3`，固定 Fork CLI/core 为 `0.7.0-castbox.3`，package manager 为 `pnpm@10.32.1`；predecessor 是已发布的 `v0.7.0-guru.1`。版本轴独立，保持现有 extension，不发布中间 `.2`。Guru 目标仍为未发布候选，本准备文档不表示 candidate gate 或 Release 已通过。正式 Fork `.3` 已由 PR28 合并并通过 main CI，当前 lock 已固定；Guru 精确远端 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源定向验收已完成，见 [唯一系列 Test](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md) / EVD-051。后继文档 HEAD 不代表重跑；Guru 软件发布、真实业务安装和完整累计矩阵仍未验证。
候选验证的 preset 与 workflow marketplace 使用同一可寻址的完整 Guru candidate SHA；
只有目标发布且远端 tag 核验与最终 candidate 匹配后，才使用同一 immutable
`v0.7.0-guru.3`（marketplace `gh:castbox/guru-trellis/trellis#v0.7.0-guru.3`，preset 来自该 tag
的 checkout）。Fork main CI 成功不替代 Guru
exact-candidate、installed/lifecycle 或发布门禁。

本次最终 candidate 门禁在准备交付与 Finish 合并后，从 fresh `origin/main` 重新冻结
exact commit/tree 执行；早期 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的验收不能替代
本次候选验证。tag、tag-pinned smoke、GitHub Release 与 Release Issue closure 仍为后续独立动作。

历史已发布 `v0.7.0-guru.1` 所锁定 Fork 的 update 会在访问旧 `0.6.17` 项目数据前拒绝，原数据保持不变。
已发布 `v0.7.0-guru.1` 不支持旧安装原地升级；拒绝不代表升级成功。
本次 `.3` 目标（extension `0.7.0-guru.3` / Fork `0.7.0-castbox.3`）提供独立 semantic
`guru-upgrade-installation`，支持全部 `v0.6.x-guru.*` 与 `v0.7.0-guru.*` 正常安装，
按实际 receipt/ownership/core/task 差异分组；从固定目标 source package 加载，不先进入
business Intake，普通 apply 保持严格。
支持来源、固定依赖前置条件和验收状态见 [MIGRATION-495.md](./MIGRATION-495.md)。
正式 Fork source/CI 已固定，Guru 分组验收及上述精确来源的同源远端验收已完成；
普通 update/reapply 不替代迁移，普通 runtime 无兼容双读或自动迁移。
迁移保留业务定制、无关 dirty/untracked 与合法当前任务状态；legacy nonterminal 的 pinned-old/deferred 处置及 rollback 恢复实际升级前来源的边界保持 [迁移说明](./MIGRATION-495.md) 合同。
当前 knowledge authority 为 `current-main-0.6.17-guru.76` / `active`，不是软件发布版本。

Use the source-locked, built `castbox/Trellis@5c760463680ffc10a3f26957b330c57a4b0c3ff8`
CLI (successful main CI `37735554354`) and a matching reviewed Guru
source. For the local workflow sample, compare the canonical `workflow.md`
with the target `.trellis/workflow.md` and preserve target edits before
applying it. Then run:

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo <target>
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root <target> --mode installed --json
```

The installer uses managed-file provenance. Known managed updates may create
backups during the transaction; successful reapply must leave no unresolved
`.new` or `.bak`. User-modified files are preserved for review, not silently
overwritten. Current package wrappers load the installed shared runtime,
including `runtime/task_lifecycle`; platform projections do not contain
private runtime, tests or recovery state.

The workflow's current path is Task Commit -> Branch Review -> Delivery
Review/Publish/Merge (repeatable while active) -> Completion -> Closure ->
Finish -> Cleanup. `guru-activate-task` owns Planning activation. The
current task identity is TaskId and lifecycle generation from current task
metadata. Path-free session focus selects the task; without a session context
key, select an explicit TaskId. The
`check-task-checkout-boundary.sh` command checks TaskId/generation, current
TaskBranchBinding and live Git checkout. It does not read `task.json.branch`,
`worktree_path`, old task/workspace mappings or a persisted checkout path.
The current checkout is resolved from TaskBranchBinding and live registered
Git worktree facts; ignored runtime mapping and checkout paths are neither
task identity nor checkout-path authority.

Old `prepare-task.sh`, `start-task.sh`, task-workspace, Publication,
Finalizer, PR-Merge and `finish-work.sh` companion entrypoints are not
installed as current public commands. They are not compatibility aliases.
The exact public-ID dispositions are in `MIGRATION-434.md`; a replacement ID
identifies a new contract, not an adapter for an old payload.
Historical tasks with retired personnel fields remain read-only. Their TaskIds
prevent reuse, while exact source clues may locate one solely to explain why
Reactivate and Finish recovery reject it. A normally finished archive that
conforms to the current upstream task schema remains eligible for the current
Reactivate contract.

## Source-Repository Official Projection Check

This source repository also dogfoods official Trellis scripts and bundled
Shared/Codex/Claude/Cursor entries. After refreshing those generated assets
from the built, source-locked Fork, verify the actual files separately from
Guru-managed overlay drift:

```bash
python3 trellis/presets/guru-team/scripts/python/verify_dogfood_upstream_projection.py \
  --repo-root . --fork-source <exact-built-fork-checkout> --json
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python \
  -p test_verify_dogfood_upstream_projection.py
```

The read-only check uses official template collectors and hash functions. It
checks generated bytes, official hash entries, the generated `.version`, and
removal of the retired history reader; editable platform configuration and
Guru-owned files have separate owners. The behavior tests run the actual
dogfood task scripts without a supplied Fork replacement, covering Issue and
no-Issue creation, list/context, and rejection of retired personnel arguments.

Refreshing this source repository's generated projection is not an upgrade
path for old installations. The selected Fork rejects a mismatched installed
version before reading old project data; changing only `.version` cannot
establish a current projection. Historical task/workspace bytes remain outside
this check. Clean installation, old-install refusal, remote marketplace and
Release evidence must be reported separately.

Canonical source validation, installed graph/manifest verification, a
representative clean local workflow sample + preset install, current platform actual-load
and reapply/drift checks are part of #434 activation. The complete multi-platform
Release matrix is deferred to its dedicated gate. The pre-#434 long-form
contract is preserved in `README.pre-434.md` for historical diagnosis only.

## 根因候选资格

新增 semantic `guru-qualify-root-cause` 在现有十个 candidate profiles 中承接
normal-scenario、solution-mechanism 的实际合格结果。根因未知的有界诊断可以
继续；有独立效果、风险、owner 和退出依据的缓解保留 `mitigation_only`。
修复证据不足返回诊断，症状抑制只返回机制移除/替换。四出口为
`classified`、`mechanism_revision_required`、`diagnosis_required`、`blocked`。
同机制结论仍适用时由后续阶段消费；新/实质变化机制重新资格。阶段仍审当前
实现和证据，qualification 不等于完成，#383 拥有共同完成语义。

完整 preset 安装后使用 public discovery 和 stdin wrapper：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh --root . --mode installed --skill guru-qualify-root-cause --json
# 先由 AI 读取 public contract/live facts 并完成 gate，再将 call-local envelope 送入：
.trellis/guru-team/skills/packages/guru-qualify-root-cause/scripts/invoke.sh --invocation -
```

三个 record/check/invoke 命令仅 stdin/stdout，无 qualification 文件、cache 或
授权持久化。安装与升级通过 canonical marketplace/preset，并重新应用 preset；
定向验证和代表性 clean/update/reapply 不代表完整多平台 Release 矩阵。
