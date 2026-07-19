# Guru Team Trellis Preset

The preset installs companion assets and Guru Team entry overlays for the
`guru-team` Trellis workflow into an existing Trellis project.

It does not run `trellis init` and does not modify Trellis upstream files.
It is idempotent: identical files are skipped, missing files are installed,
Guru-managed companion assets are upgraded in place with `.bak` backups,
existing `.trellis/guru-team/config.yml` is preserved, known upstream
Trellis-generated entry files are replaced with Guru Team overlays, and unknown
local modifications are preserved by writing `.new` copies.

The current config template includes `middle_platform_knowledge.mode:
optional_warn`. Existing target repo configs are not overwritten just to add
this key; if it is absent, the workflow interprets it as `optional_warn`.
`required` is opt-in only, and `off` is opt-out only.

The preset also materializes the project-level `.trellis/config.yaml`
`codex.dispatch_mode` default. Missing, commented-out, or invalid values are
updated to `sub-agent` so Codex can dispatch `trellis-implement` /
`trellis-check` and satisfy Branch Review Gate by default. In that default mode
implementation, Phase 2 check, and post-commit Branch Review are three separate
sub-agent evidence boundaries: `trellis-implement` / channel `implement`
produces implementation handoff, `trellis-check` / channel `check` produces
evidence for `phase2-check.json`, and an independent review sub-agent reviews
the full committed branch diff before the main session records Branch Review
Gate. An explicit `codex.dispatch_mode: inline` value is preserved as a
user-selected downgrade or debug mode; missing sub-agent evidence must fail
closed unless explicit inline/self-exemption artifact evidence exists.

The preset also installs Guru Team sub-agent definitions. Technical dispatch ids
stay stable (`trellis-implement`, `trellis-check`, `trellis-research`, channel
runtime `implement` / `check`), while UI-facing labels are Chinese where the
platform supports them. Codex uses Chinese `description`, but keeps
`nickname_candidates` ASCII because current Codex rejects non-ASCII nicknames and
ignores malformed agent files. Markdown-based agent files use Chinese
descriptions and headings. Implement/check definitions require an unfinished
handoff instead of a false completion claim when the main session interrupts or
replaces a worker, including current diff, remaining work, validation state, and
gate blockers for same-agent resume or replacement handoff.

Platform overlays are selectable. By default, the installer applies shared
`.agents/skills` entries plus Codex and Cursor overlays. Repeat
`--platform <name>` to select a specific set; supported values are `codex`,
`cursor`, and `claude`. Use `--all-platforms` to preserve the historical
full-overlay behavior. `--platform` and `--all-platforms` are mutually
exclusive, and invalid platform names fail closed.

The preset records the installed Guru Team extension version and source
provenance in `.trellis/guru-team/extension.json`. The canonical extension
version lives in `trellis/guru-team-extension.json`; it is separate from the
official Trellis CLI version and from the marketplace index schema version in
`trellis/index.json`.

The preset also normalizes known Trellis-generated English documentation
language rules in target business repositories. It deterministically replaces
the fixed `All documentation ... English` template lines in `.trellis/spec/**` and
`.trellis/tasks/00-bootstrap-guidelines/**/*.md` with the Guru Team Chinese
documentation rule. It does not scan `.trellis/workspace/**`, ordinary task history, or translate
business `docs/**`; those documents are governed by the workflow's AI-facing
Chinese documentation contract.

Stable workflow marketplace installs should pin the repo release tag that
combines the target official Trellis CLI version and Guru Team revision, for
example `gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`. That release targets
official `@mindfoldhq/trellis` `0.6.5`. Unpinned `gh:castbox/guru-trellis/trellis`
is a latest/canary source and should be reported as mutable provenance.

## Upstream Ownership Freeze

The overlay tree is a frozen transitional migration surface, not an open-ended
way to patch Trellis-owned entries. The strict inventory and schema live at:

- `trellis/presets/guru-team/ownership/upstream-ownership.json`
- `trellis/presets/guru-team/ownership/upstream-ownership.schema.json`

The inventory retains exactly 43 paths from base commit
`291b57b6c02872320a4dce0626a2f718399b8f56`, including a SHA-256 for every
payload, 37 Trellis `0.6.5` clean-init entries, and six historical Codex
prompt/skill entries that clean init no longer generates. Every active entry is
`transitional_legacy`; future issue #132 removal keeps the same record as
`upstream_owned/removed` rather than erasing audit history.

Before any target mutation, `apply_guru_team_trellis_preset.py` validates the
source inventory, overlay bytes, public managed claims, `MANAGED_ASSET_PATHS`,
active Skill ids, and anchored Guru discovery namespaces. Maintainers can run
the same read-only gate directly:

```bash
./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
python3 ./trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
```

The validator and its positive/negative fixtures are source-only assets; they
are not copied into target business repositories. The validator reports path,
schema, category, hash, owner, prerequisite, manifest, and namespace facts. AI
review still owns whether a proposed owner or migration is semantically valid.

## Commit Message Helpers

The preset installs objective helpers for the Guru Team Chinese Conventional
Commits contract:

```bash
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-path>
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json \
  --task <task-path> \
  --pull-request <pr-number> \
  --summary "中文 PR 摘要"
```

The helpers validate subject/body shape and format merge commit payloads only.
They do not decide whether implementation, Phase 2 check, Branch Review Gate, or
PR readiness is sufficient. Work commits use
`{type}({scope}): #{primary_issue} 中文描述` with fixed body sections and
`Refs #<primary_issue>`; commit messages must not use close keywords such as
`Closes`, `Fixes`, `Resolves`, `Close`, `Fix`, or `Resolve`; Trellis metadata commits use an empty body; publish
payloads provide `chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要`
plus the fixed merge body and explicit `gh pr merge ... --subject ... --body-file ...`
command.

## Apply

```bash
git clone --depth 1 --branch v0.6.5-guru.2 \
  https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --platform codex \
  --platform cursor
```

Examples:

```bash
# Shared overlays plus Claude only.
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --platform claude

# Shared overlays plus every known platform overlay.
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --all-platforms
```

## Throwaway Install Verification

Maintainers can verify the current extension's non-interactive install path with:

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

The script creates a temporary Git repo, runs `trellis init -y` with the
`guru-team` marketplace workflow, applies the preset with
`--platform codex --platform cursor`, checks that `.trellis/workflow.md`
exists, verifies that the active workflow requires the three Guru Team planning
artifacts, verifies that `check-env.sh` and `version.sh` are executable,
asserts `.trellis/guru-team/extension.json` exists, asserts `.claude/` was not
created, asserts the active workflow, Codex / Cursor SessionStart hooks, Cursor
sub-agent context hook, brainstorm/check/before-dev skills, and Trellis meta
planning references no longer contain legacy `PRD-only` / lightweight /
optional-design planning hints,
asserts target `.trellis/spec/**` and
`00-bootstrap-guidelines` do not retain known English documentation language
requirements, and runs `check-env --json` plus `version.sh --json`. Trellis CLI accepts
`gh:user/repo/path#ref` workflow marketplace sources; the script defaults to
`TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#main` as an explicit
mutable canary baseline. The unpinned source and `#main` both fail closed on non-`main` branches
or dirty marketplace workflow files unless
`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` is set. This prevents public remote
sampling from being reported as current-branch marketplace verification. When
validating a feature branch or release, set `TRELLIS_WORKFLOW_SOURCE` to the exact
existing branch/tag ref; only that run is evidence for that ref. When
it does run, it also exercises the existing-project `trellis workflow
--create-new` preview, deletes the validated expected preview `.new`, then runs
forced switch, `trellis update --force`, workflow reapply, and preset reapply.
It records ownership-gate JSON at three checkpoints: before the initial preset
apply, after `trellis update` before workflow/preset reapply, and after preset
reapply before final drift/sidecar checks. The installer itself repeats the
pre-mutation gate for both apply operations.
A controlled bare remote and fake GitHub adapter drive the already-installed
`finish-work.sh` through dry-run digest, formal draft binding, official archive,
three-way HEAD equality, ready transition, and clean-tree assertions once after
install and once after update/reapply. The fixture uses installed wrappers,
companion, schemas, config, workflow, and official `task.py`; it does not copy
canonical runtime assets into the target. A final recursive scan must find no
`.new` or `.bak` sidecars. It intentionally lives in this
source repository and is not copied into target business repos as a managed
companion asset.

## Dogfood Overlay Drift Check

After changing any file under `trellis/presets/guru-team/overlays/`, maintainers
must re-apply the preset to this source repository and verify that installed
dogfood copies still match the canonical overlays:

```bash
./trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo . \
  --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

`check-dogfood-overlay-drift.sh` is read-only. It first runs the ownership gate,
then compares canonical overlay files with same-path installed copies in this
repository and exits non-zero for ownership failure, missing copies, or changed
copies. It is a source-repository maintainer check and is not installed into
target business repositories as a managed companion asset.

If `apply.sh` creates `.new` or `.bak` files, inspect and resolve them before
committing. A passing drift check is not a replacement for AI review or the
Branch Review Gate.

## Installed Files

Preset 是完整 Guru Team extension configurator。除 companion assets 和
platform overlays 外，它验证 `trellis/skills/guru-team/registry.json`，将
registry/schema/active packages 安装到 `.trellis/guru-team/skills/`，并把
active package 分发到 shared root 与明确选择的 Codex/Cursor/Claude roots。
Reserved ids 与 test fixtures 永不安装，未选择的平台 root 不因 skill 分发
而创建。

Active `guru-approve-task-plan` package 随 registry-driven install 分发到 shared root 与所选
Codex/Cursor/Claude discovery roots，并依赖同一 preset 安装的 schema
`guru-planning-approval-2.0`、shared dispatcher 和
`record-planning-approval` / `check-planning-approval` runtime commands。该分发是
Guru-owned additive content，不修改 frozen `trellis/presets/guru-team/overlays/**`。

每个 active package 的 `SKILL.md` 必须有与 stable id/interface 一致的唯一
`name`/`description` frontmatter；`tests[]` 必须定位 package-local
`tests/<file>` regular file。Test evidence 属于 package tree，因此随 installed
copy 和所选平台副本进入 manifest inventory；标签、虚构、越界、重复或
symlink-backed test evidence 会在 mutation 前被 source validator 阻断。

Skill 文件按 installed manifest 中的 previous managed hash 更新：missing
直接安装，canonical-equal 保持 unchanged，known upgrade 先写 `.bak` 再替换，
unknown/invalid provenance 保留原文件并写 `.new` 后阻塞。完成安装或
`trellis update` 后重放时，必须处理所有 sidecar，再运行 source/installed
`check-skill-packages` 和 dogfood drift 检查。

Known upgrade 的 conflict manifest 只在 `conflicts=[]` 且 `sidecars[]` 全部是与
当前 managed `files[]` 相邻的 `.bak` 时可用于恢复。未删除的 backup 会在重放时
继续保留并阻塞；全部删除后再次 apply 才能转为 `status=ok`。`.new`、未知编辑、
异常路径、未绑定 backup 或实际 conflict 不得走此恢复分支。

Manifest 的 `files[]` 是当前完整 inventory；平台选择缩减时，known managed
旧副本安全删除并进入 `removals[]`，unknown/invalid 副本保留并进入
`conflicts[]`，`sidecars[]` 必须与磁盘 `.new/.bak` 精确一致。任何 conflict
都会令 `status=conflict`。所有 skill 路径在读写/删除前逐组件 `lstat`；target
或 ancestor 的 regular/dangling/internal/external/multilevel symlink 一律拒绝，
不会沿链接读写 repo 外内容。

Managed Guru Team assets are installed under `.trellis/guru-team/` regardless of
platform selection:

- `.trellis/guru-team/config.yml`
- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/schemas/task-start-context.schema.json`
- `.trellis/guru-team/schemas/closeout-plan.schema.json`
- `.trellis/guru-team/schemas/finish-summary.schema.json`
- `.trellis/guru-team/schemas/marketplace-verification.schema.json`
- `.trellis/guru-team/scripts/bash/check-env.sh`
- `.trellis/guru-team/scripts/bash/version.sh`
- `.trellis/guru-team/scripts/bash/prepare-task.sh`
- `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh`
- `.trellis/guru-team/scripts/bash/check-skill-packages.sh`
- `.trellis/guru-team/scripts/bash/run-skill-command.sh`
- `.trellis/guru-team/scripts/bash/sync-base.sh`
- `.trellis/guru-team/scripts/bash/check-base-sync.sh`
- `.trellis/guru-team/scripts/bash/preview-change-context-history.sh`
- `.trellis/guru-team/scripts/bash/record-context-discovery.sh`
- `.trellis/guru-team/scripts/bash/check-context-discovery.sh`
- `.trellis/guru-team/scripts/bash/record-requirements-clarification.sh`
- `.trellis/guru-team/scripts/bash/check-requirements-clarification.sh`
- `.trellis/guru-team/scripts/bash/record-contract-wording-review.sh`
- `.trellis/guru-team/scripts/bash/check-contract-wording-review.sh`
- `.trellis/guru-team/scripts/bash/record-change-request-review.sh`
- `.trellis/guru-team/scripts/bash/check-change-request-review.sh`
- `.trellis/guru-team/scripts/bash/record-task-workspace-plan.sh`
- `.trellis/guru-team/scripts/bash/create-task-workspace.sh`
- `.trellis/guru-team/scripts/bash/check-task-workspace-result.sh`
- `.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh`
- `.trellis/guru-team/scripts/bash/record-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/check-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/record-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/check-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/record-agent-assignment.sh`
- `.trellis/guru-team/scripts/bash/check-agent-assignment.sh`
- `.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh`
- `.trellis/guru-team/scripts/bash/check-subagent-liveness.sh`
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh`
- `.trellis/guru-team/scripts/bash/create-task-commit.sh`
- `.trellis/guru-team/scripts/bash/format-merge-commit.sh`
- `.trellis/guru-team/scripts/bash/review-branch.sh`
- `.trellis/guru-team/scripts/bash/check-review-gate.sh`
- `.trellis/guru-team/scripts/bash/publish-pr.sh`
- `.trellis/guru-team/scripts/bash/finish-work.sh`
- `.trellis/guru-team/scripts/bash/backfill-finish-summary.sh`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`

Production skill registry 同时保留 reserved `guru-create-work-commit`，以及 active
`guru-create-task-workspace`、`guru-sync-base`、
`guru-discover-change-context`、`guru-clarify-requirements`、
`guru-review-contract-wording`、`guru-review-change-request`、
`guru-create-task-commit`。Planned id 不安装 package，也不能拥有 invoke/exit marker。当前
canonical extension version 是待发布的
`0.6.5-guru.16`；已发布 stable source 仍是 `v0.6.5-guru.2`。Preset 将 active package
（含 interface、artifact schema、
example、thin wrappers 与 tests）安装到 `.trellis/guru-team/skills/`，并分发到 shared
root 和所选 Codex/Cursor/Claude skill roots；reserved id 不安装。升级后必须处理
`.new`/`.bak`，再通过 source/installed package validation 与 dogfood drift。

Interface schema 1.2 中 `workflow` 表示 global mandatory routing，`standalone` 表示
所选平台 direct discovery。两种 mode 都依赖完整 compatible Guru Team runtime；单独
复制 Skill 目录不是 self-contained/portable 安装。Preset 因此同时安装
`.trellis/guru-team/scripts/bash/run-skill-command.sh`、extension runtime capability、
audited package inventory 与 discovery copies。Wrapper 只能经过该 dispatcher；旧 runtime、
缺失 manifest/dispatcher、API/command mismatch 或 managed drift 会在 companion command
之前 fail closed，并提示安装/升级完整 preset、处理 `.new` / `.bak`、重跑验证。

`guru-discover-change-context` package 同时安装
`guru-context-discovery-1.0` schema、example、contract、tests 与三个 executable thin
wrappers。Direct discovery 与 workflow route 使用相同 fresh-base/change-input/evidence
freshness preconditions。Runtime 只读取 archived `finish-summary.json:index.*`，使用
`guru-context-history-score-1.0`，不读取 workspace/runtime 或 repo-level archive
index/cache。Pre-task recorder stdout-only；task-local recorder 只写 expected digest 匹配的
同一 `context-discovery.json` snapshot；pre-task/standalone 绑定 decision branch，真实 task
feature worktree 绑定 `task.json.branch` 且保持相同 HEAD/base refs/provenance/repo 与 task-local
dirty scope。Zero candidate 固定 empty selection/deep reads 与 `mem_review=not_needed`，不触发
其它历史源。Installed/throwaway gates 覆盖 zero/candidate preview、真实 feature-worktree
record/check、invalid mem shape、`trellis update`、workflow/preset reapply 和最终 zero sidecar。
Source issue 的 live state 可为 normalized `open` / `closed`，但 duplicate candidates 与
draft-created issue binding 仍 open-only。40 位 current evidence Git identity 必须解析为
exact blob；tree、gitlink commit、tag、missing object 或 identity drift 不能满足
Docs、code/contracts、tests evidence。Deep-read locator 分别绑定 selected task artifact、
canonical GitHub issue/PR 或 exact Git object/ref；closed schema 与结构化 locator 不保存
raw source payload，只做 field-specific validation。
Duplicate candidate 的 managed schema/runtime 使用 repo、number、`#number` identity、
canonical issue URL、open state 与 update time 的 canonical digest projection，并在 fresh
base 后从同一次 search 返回字段重算 identity、URL 与 digest，不进行第二次 search 或
candidate re-read。Managed schema/runtime 同时强制 `blocked` exit
与 blocked AI Review Gate 双向一致。
Refresh record/check 记录并核对当前 stable stale codes、superseded query/snapshot
digests、reason 与 detection time，然后要求整步 re-entry；只消费当前 payload 与 expected
snapshot identity，不重建 ancestry。
`context_ready` 指向 active `guru-clarify-requirements`；source/installed validator 要求
active Skill consumer 与唯一 workflow/stop target marker 均可解析。

`guru-clarify-requirements` package additive 安装
`guru-requirements-clarification-2.0` schema、example、contract、tests和两个 executable
dispatcher wrappers。Runtime assets 是
`.trellis/guru-team/scripts/bash/record-requirements-clarification.sh` 与
`check-requirements-clarification.sh`；不存在 mutation executor。Workflow/standalone
preconditions相同；answered evidence、question lifecycle与confirmed payload/live mutation均
fail-closed验证。Pre-task/standalone stdout-only，
active-task Scope Change Gate mandatory invoke本Skill，并由caller-aware clear router恢复planning或
exact interrupted progression；只验证现有 ledger/planning/stale-gate/re-entry linkage，不创建专用 clarification artifact。Throwaway initial install、
`trellis update`、workflow re-selection与preset reapply均执行 standalone record/check probe，
并验证 `clear` / `needs_context` / `refresh_context` / `retarget_context` / `new_task` /
`blocked` consumers。2.0 绑定 target disposition、duplicate decision、authority impact 和新
action/exit；1.0 artifact/caller fail closed，必须从 `guru-sync-base` 重跑，不自动迁移。

Active-task `clear`/`new_task` 必须携带非空七类 terminal proposal set，每个五类 scope
classification 无论 origin 均要求 exact 用户证据，并 exact 绑定当前
`issue-scope-ledger.json.scope_decisions[]` structured trail、所需用户证据、live GitHub
authority、通过 shared `guru-planning-approval-2.0` 完整 validator 且 exact reviewed/approved 三文档绑定的
planning evidence，以及 review/stale/re-entry evidence。`mechanism_removed/replaced` 使用
optional origin/null confirmation，不进入 trail/action mutation。GitHub authority mutation
必须返回 `refresh_context`；context 时间覆盖 authority 后 task update 绑定同一 digest，
不要求第二次 refresh；`new_task` 只向 #112
传递 side-effect-free draft，不在本 package 创建 issue/task。

`guru-review-contract-wording` package 安装
`guru-contract-wording-review-1.0` schema、example、contract、tests 和两个
executable dispatcher wrappers。Workflow/standalone preconditions 相同；固定 profiles
为 `change_request`、`planning_artifacts`、`explicit_paths`，typed exits 为 `pass`、
`content_changed`、`blocked`。Vocabulary、classification semantics、AI rewrite/review
loop 和 confirmation policy 只存在于 canonical package contract；runtime 只负责固定 scope、
scan、hash/digest、unchecked、schema/freshness 与 Gate/exit 结构校验。Installed runtime
同时拒绝 selected comment 缺 author/updated time，并为 live issue revision 校验 exact
confirmed payload digest、preimage 和 current reread mutation-result identity。
Task-local current `content_changed`/`blocked` 在 consumer 进入完整 same-profile re-entry 后，
必须用 `--supersede-reentry-facts-sha256` 精确绑定旧 result，且完整 current 新结果必须与
旧 artifact 不同；stale evidence 只使用互斥的 `--replace-stale`，相同结果和 current `pass`
不得无理由覆盖。Runtime 只校验 transition facts，不决定 semantic route。
`planning_artifacts:pass` 写 task-local `contract-wording-review.json`，供 planning
approval adapter 投影消费；它还必须包含 canonical contract 定义的 exact
`semantic_review.ai_review_gate.planning_checked_dimensions`，全部显式 AI-reviewed 为 true
才能成功。Runtime 只验证该 planning-only 字段的 shape/value，projection 只逐项复制，不默认
生成。其它 profile 禁止该字段且保持 stdout-only。Fresh install、dogfood、四平台
discovery copies 与 update/reapply 必须同时包含 package、commands、schema 和 route markers。

`guru-review-change-request` package additive 安装
`guru-change-request-review-1.0` schema、deidentified `issue-review.json` example、contract、
tests 和两个 executable dispatcher wrappers。Runtime assets 是
`.trellis/guru-team/scripts/bash/record-change-request-review.sh` 与
`check-change-request-review.sh`。Workflow/standalone preconditions 相同；三类 target、current
context/clarity/wording linkage、十项 dimensions、findings、scope conclusion、AI Gate 与五出口
由 canonical semantic package 拥有。Runtime 只重建 portable projection/linkage/facts 并校验
schema/hash/ref/freshness/consumer/ready invariant，不生成 readiness、finding、delivery unit 或
route。Pre-task/standalone stdout-only；#112 后续只能持久化同一 checker-passed bytes。

五出口固定为 `ready` -> active `guru-create-task-workspace`、
`clarify_requirements` -> `guru-clarify-requirements`、`review_wording` ->
`guru-review-contract-wording`、`refresh_context` -> `guru-sync-base`、`blocked` ->
`change-request-review-blocked`。Fresh install、selected platform discovery、installed validation
与 update/reapply 必须证明 active workspace package存在、`ready` 没有 legacy full-intake fallback，
并覆盖三类 target、五出口和 zero cache/sidecar residue。

`guru-create-task-workspace` package 安装
`guru-task-workspace-plan-1.0`、`guru-task-workspace-result-1.0`、contract、examples、tests
和三个 executable dispatcher wrappers。Draft invocation 创建 exact issue 后固定
`refresh_review`；open issue invocation 使用独立 workspace/task confirmation。Assignee 按
explicit、single issue assignee、zero issue assignees/current login、multiple/unresolved user
choice 顺序解析。成功后只写四个 tracked task-local Intake artifacts 与 ignored
`.trellis/.runtime/guru-team/**` mappings。

Draft create 前使用 exact open title/body/labels 与 creation time执行 0/1/>1 recovery；
唯一匹配被恢复，零匹配才创建，多个匹配阻断。完整 Intake重入时，workflow-created issue
携带完整 checker-passed created-issue result，并与 fresh context 的 canonical live
existing-issue identity一致；该 context使用`kind=issue`与 null `issue_binding`。

Shared overlays are always installed:

- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-brainstorm/SKILL.md`
- `.agents/skills/trellis-before-dev/SKILL.md`
- `.agents/skills/trellis-check/SKILL.md`
- `.agents/skills/trellis-continue/SKILL.md`
- `.agents/skills/trellis-finish-work/SKILL.md`

Default Codex overlays are installed when no platform flag is provided, or when
`--platform codex` / `--all-platforms` is used:

- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.codex/agents/trellis-research.toml`
- `.codex/hooks/session-start.py`
- `.codex/prompts/trellis-start.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/prompts/trellis-finish-work.md`
- `.codex/skills/trellis-start/SKILL.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-finish-work/SKILL.md`
- `.agents/skills/trellis-meta/references/customize-local/change-workflow.md`
- `.agents/skills/trellis-meta/references/customize-local/change-context-loading.md`
- `.agents/skills/trellis-meta/references/local-architecture/context-injection.md`
- `.agents/skills/trellis-meta/references/local-architecture/task-system.md`
- `.agents/skills/trellis-meta/references/platform-files/agents.md`

Default Cursor overlays are installed when no platform flag is provided, or when
`--platform cursor` / `--all-platforms` is used:

- `.cursor/agents/trellis-implement.md`
- `.cursor/agents/trellis-check.md`
- `.cursor/agents/trellis-research.md`
- `.cursor/hooks/session-start.py`
- `.cursor/hooks/inject-subagent-context.py`
- `.cursor/commands/trellis-continue.md`
- `.cursor/commands/trellis-finish-work.md`
- `.cursor/skills/trellis-brainstorm/SKILL.md`
- `.cursor/skills/trellis-before-dev/SKILL.md`
- `.cursor/skills/trellis-check/SKILL.md`
- `.cursor/skills/trellis-meta/references/customize-local/change-workflow.md`
- `.cursor/skills/trellis-meta/references/customize-local/change-context-loading.md`
- `.cursor/skills/trellis-meta/references/local-architecture/context-injection.md`
- `.cursor/skills/trellis-meta/references/local-architecture/task-system.md`
- `.cursor/skills/trellis-meta/references/platform-files/agents.md`

Claude overlays are installed only when `--platform claude` or `--all-platforms`
is used:

- `.claude/agents/trellis-implement.md`
- `.claude/agents/trellis-check.md`
- `.claude/agents/trellis-research.md`
- `.claude/commands/trellis/continue.md`
- `.claude/commands/trellis/finish-work.md`

The active `.trellis/workflow.md` is installed or switched through the official
Trellis workflow marketplace:

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.2 \
  --template guru-team
```

## Spec Bootstrap

`trellis init` may create `.trellis/tasks/00-bootstrap-guidelines/`. That task is
a one-time repository-level prompt to replace generic `.trellis/spec/` templates
with the target repository's real conventions.

The Guru Team preset must not silently complete that task as an install or
upgrade side effect. An AI installer may report that the task exists and explain
what spec files it would inspect or modify, but it should ask the user whether
to complete bootstrap now or leave it for a separate follow-up. If the user does
not explicitly confirm, preserve the task and do not rewrite `.trellis/spec/`
template content.

When the user does confirm bootstrap in a target business repository, generated
or refreshed `.trellis/spec/**` prose and any docs SSOT files created or
completed under `docs/**` must use Chinese human-readable prose by default.
Literal commands, paths, config keys, GitHub keywords, external API names, and
code symbols may remain English.

The daily user-facing entry points are natural-language task requests, issue
URLs or issue numbers, `trellis-continue`, and `trellis-finish-work`. The
`trellis-start` overlay remains installed as a fallback / explicit orientation
entry for platforms without automatic startup injection, disabled or unapproved
hooks, suspected bootstrap failures, or manual context reloads.

Planning, check, review, and publish helpers are internal companion script
subcommands used by the workflow; they are not daily user-facing entries.
`guru-approve-task-plan` owns the semantic review and the single
`planning-approval.json` artifact. It consumes current checker-validated
`guru-review-contract-wording:planning_artifacts:pass`, reviews adequacy,
provenance, choices and unusual proposals, runs the AI Gate, separates dedicated
proposal confirmation from post-planning confirmation, and returns one of four
typed exits. The installed `record-planning-approval.sh` and
`check-planning-approval.sh` commands consume/rebuild deterministic facts for
schema `guru-planning-approval-2.0`; they do not create semantic conclusions.
For `approved_scope_expansion`, they recompute the proposal from one controlled
current planning locator or canonical unusual candidate, then require the
source-appropriate dedicated confirmation and runtime-materialized current
authority SHA-256 to bind that same digest. An unusual candidate link reuses its
existing confirmation rather than asking twice; a caller-only digest fails.
Active schema 1.2 requires complete Skill re-entry and v2 recording. Scope
ledger task identity and requirement authority use the same issue-category
projection. The checker revalidates the invocation base/HEAD/dirty snapshot
while the task is still planning; after activation freshness is based on
planning, Docs SSOT, authority and wording content, not later implementation
HEAD drift, metadata tail, or unrelated dirty paths. `task.py start` remains
only a status transition.
`resolve-human-artifacts.sh` is the deterministic fact layer for phase replies:
before a planning stop, Phase 2 completion, Branch Review Gate result,
finish-work dry-run reply, or final archive/publish reply, the AI runs it and
renders a `Markdown 产物 review 表` with only `prd.md`, `design.md`,
`implement.md`, `review.md`, and `pr-body.md`. Missing files are shown without
Markdown links, and JSON evidence such as `phase2-check.json`,
`review-gate.json`, or `agent-assignment.json` is not part of the standard
table.
`record-phase2-check.sh` records the full-scope `trellis-check`
result before commit, including the pre-commit `dirty_paths`; validation
commands are evidence inside that report, not a substitute for the check.
`phase2-check.json` is a Guru Team artifact that freezes the completed
`trellis-check` AI judgment, coverage, validation results, findings, and dirty
paths; it is not the Trellis-native step itself and script recorder/validator
success cannot replace `trellis-check`.
`record-subagent-liveness-event.sh` / `check-subagent-liveness.sh` /
`check-agent-assignment.sh` manage task-local `agent-assignment.json` liveness:
Chinese `logical_role` is the Trellis process identity, `agent_id` is the
technical platform id, and `platform_nickname` is display-only. `agent-assignment.json`
schema 1.1 is the single assignment/status/liveness/review ledger with
`agents[]`, `status_events[]`, `liveness[agent_id].last_scan_snapshot`, review
rounds, and reuse decisions. The liveness recorder writes assignment, progress,
status request, stale, resume/replacement, terminal, and workspace-boundary
audit events already observed by AI/human. The checker is short-lived and
single-sample: it reads task/source checkout snapshots plus recorded progress
event digests, returns one decision, and exits. It never reads platform UI,
sends status requests, terminates agents, or judges implementation quality.
`progress_scan_interval=120s` is scan cadence; `max_progress_silence=180s`
starts at `progress_anchor_at`. Only `status_request_required` authorizes one
status request, and only `stale_allowed` authorizes `stale-assessed`.
`status-requested` does not refresh anchor or extend deadline. Stale cutover
must record `termination_reason=stale_cutover`, `termination_source_event_id`,
and `replacement_reason=max_progress_silence_exceeded`; manual/platform
unfinished termination uses
`termination_reason=manual_or_platform_terminated_unfinished`. Failed, stale,
unfinished, or replacement partial output cannot pass Phase 2 / Branch Review
until a recovery chain reaches `completed`. `record-agent-assignment.sh` remains
for review rounds and reuse decisions; its old `--status-event` path fails
closed.

After the task work commit, `review-branch.sh` audits that committed
non-metadata task paths after the Phase 2 recorded HEAD are covered by those
dirty paths and that no non-metadata dirty paths remain in the working tree.
Do not re-record Phase 2 after commit just to make HEAD match. `review-branch.sh`
records and validates the prior AI/human review result; it is not the reviewer.
Passing gates require every finding owner to have one explicit closure form: a
later same-agent `问题闭环审查代理` review with zero findings and
`reuse-for-closure`; a different fresh closure agent whose technical identity has not appeared in any earlier review round and is linked by
`reuse_decisions[] decision=new-agent` with exact `from_round`, `to_round`,
closure agent, reviewed HEAD, and reason; or a replacement closure chain when
the finding owner failed/interrupted and cannot continue. A closure round that
still has findings becomes a new finding owner and must be closed before a fresh
`最终放行审查代理` independent review can pass. The
final review must cover the full current HEAD
diff with zero findings of any priority, must not continue implementation or
patch missing Phase 2 check work, and be recorded with task-local
`reviews/*.md` raw reports, a final `review.md` rollup that links every raw
report, a Chinese summary, concrete evidence, `--review-source
independent-agent`, `--review-report <task-local review.md>`, and
`--agent-assignment <task-local agent-assignment.json>`. The gate stores the
final review digest, raw `review_reports[]` digests, assignment digest, Chinese roles summary, and status event count, and validates
closure-before-final, unfinished termination recovery-chain completeness, the
last fresh final round, and that the final reviewer did not own an earlier
finding round. Observations and follow-up candidates may be recorded separately,
but they must not hide current-scope findings. Independent review sub-agents
review docs, code, tests, artifacts, and diff evidence as AI reviewers; they do
not run Guru Team recorder/validator extension scripts such as
`review-branch.sh`, `check-review-gate.sh`, or `record-*`. The main session runs
those scripts only after the review result exists. `--reviewer` is identity metadata
only and cannot replace the review report digest; `*-main-session` /
`self-review` cannot pass the gate.
Branch Review also verifies Docs SSOT execution instead of performing it for the
first time. The final reviewer must read the approved `Docs SSOT Plan`,
implementation handoff, `phase2-check.json`, durable docs, task artifacts, and
the full diff, then report any current-scope Docs SSOT inconsistency as a
finding. The reviewer does not merge durable docs or patch missing Phase 2 docs
work.
`finish-work.sh` rejects ordinary direct calls, while `publish-pr.sh` is an
unconditional compatibility blocker, so
`trellis-continue` cannot chain closeout, commit review metadata, push, or
create a PR before the explicit `trellis-finish-work` entrypoint. Normal PR
publish is triggered only by `finish-work.sh --from-trellis-finish-work` after
a reviewed dry-run returns an immutable closeout plan digest. Formal finish
requires the same digest, pushes reviewed content, records marketplace evidence
and readiness, binds a draft PR, validates the final archive projection, then
creates one archive metadata commit and marks the PR ready after three-way HEAD
alignment. Every interruption resumes through the same finish entry.
Shared prepare lexically `lstat`s each existing archive root, month, and final
destination component, rejects every symlink including dangling and
repo-internal targets without following it, and requires the final locator to
be absent. The identical preflight repeats immediately before official move.
Missing `task.json.children` means an empty list; otherwise
it must be `list[str]`. Official active-task exact/suffix lookup blocks only a
child whose active `task.json` would be rewritten, while an archived child does
not block its parent.

After a passed gate, finish-work accepts only Trellis metadata tail. Durable
docs, `.trellis/spec/`, source, tests, schema, config, scripts, preset, overlay,
CI/CD, deployment, migration, or Makefile drift after the gate must return to
Phase 2/3; dry-run and formal finish do not perform a first Docs SSOT merge.

`finish-work.sh --dry-run --from-trellis-finish-work` is a side-effect-free
readiness preview. It validates the gate, dirty state, AI-authored
`finish-summary-index.json`, and PR body/readiness, then prints the immutable
plan, digest, future archive mapping, metadata allowlist, and transitions
without moving or writing task files, creating commits, pushing,
or creating a PR.
After dry-run, the AI should render the active-task `Markdown 产物 review 表`;
after formal archive, it must rerun the resolver and render the archive-path
table because active task links are no longer the final review entry points.

Before finish-work publishes, the AI must generate or review a PR body for
GitHub reviewers who do not know the Trellis task. The body should use concrete
Chinese sections for `变更摘要`, `影响范围`, `验证结果`, `Review Gate`,
`Issue 关闭范围`, `安全说明`, and `Docs SSOT` / `文档同步`. The Docs SSOT section
states the plan strategy, durable docs updates or no-update reason, task deltas
merged back, task-history-only content, and any follow-up or current PR
limitation. Low-information summaries such as
`当前 Trellis task`, `已提交实现与文档更新`, or `详见 artifact` are blocked for
non-draft publish. Non-draft publish requires reviewed Markdown with
task-local `--body-file <path>`; formal finish builds
`pr-readiness.json.publish_inputs` with repo/base/head/reviewed HEAD/title/body
SHA-256/`draft=true`/reviewed source and `closeout_plan_digest`. Generated fallback
bodies are preview-only. Finish-work requires the direct task-local
`pr-body.md` with exact raw UTF-8 bytes and rejects every symlink component
from repo root through the task parent and final file, including alias,
dangling, and loop paths. It rejects `--body-artifact` and external or
whitespace-normalized substitutes. The readiness/body files are committed before the
draft PR create and moved unchanged by archive. The script validates objective structure,
reviewed source presence, Docs SSOT section/key presence, and close/ref
semantics but does not replace AI release judgment.

## One-Time Archived Task Backfill

For repositories with archived tasks created before the normal finish-summary
path, run the managed one-time migration after install or update:

```bash
.trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --dry-run
.trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --write
```

The wrapper is a managed executable and preset reapply restores it. It scans
only `.trellis/tasks/archive/**/<task>/`, skips existing summaries unless
`--write --force` is used, keeps complete changed paths grouped by kind, and
continues after task-local errors. It does not read active tasks,
workspace/runtime state, GitHub, or `trellis mem`, and it creates no global
index. This migration prepares historical records for #98 discovery while the
normal finish-work path remains unchanged.

## Workflow Guardrails

For `no_task` issue-backed, task-like, or file-changing requests in a Guru Team
project, tool-free classification is followed by mandatory `guru-sync-base`, not
bare `task.py create`. The Skill resolves explicit `--base`, scalar
`base_branch`, the first existing branch in configured `base_branch_candidates`
order (default `dev`, `develop`, `main`, `master`), then remote default when no
candidate exists; the current branch is never an implicit base. Multiple existing
candidates are ordered, not ambiguous. The deterministic Skill performs
digest-bound execution without a selected-base or post-execution AI gate. A
`synced` result requires a clean checkout and equal decision/local/remote HEADs;
`skipped` returns to the original request, while `blocked` stops fail closed.
Only `synced` enters the mandatory
`guru-discover-change-context -> guru-clarify-requirements ->
guru-review-contract-wording -> guru-review-change-request ->
guru-create-task-workspace` chain. The following command is query-only
compatibility and is not a workflow hop:

After task planning and a current `planning_artifacts:pass`, Phase 1 mandatory
invokes `guru-approve-task-plan`. Only `approved` enters
`phase-1-task-activation`; `revision_required` re-enters the Skill,
`clarify_scope` routes to `guru-clarify-requirements`, and `blocked` stops at
`task-plan-approval-blocked`. The preset distributes this route's package and
v2 deterministic runtime; it does not move the step-local review loop into a
platform overlay.

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --expected-resolution-sha256 <post-sync-resolution-sha256> \
  "<user request or issue URL>"
```

`prepare-task.sh --json` is query-only compatibility. It may read
an explicit issue and search duplicates, but it does not create a GitHub issue,
worktree, branch, Trellis task, or `.trellis/tasks/<task-slug>/task-start-context.json`. Freeform
requests without a source issue return `proposed_issue`, `requires_confirmation`,
`naming_quality`, `preflight.base_freshness`, and `no task context/runtime write` in
stdout JSON. Before `gh auth status`, issue reads, or duplicate search,
`prepare-task` reuses the same strict resolution/sync core used by
`guru-sync-base`; `fetch_performed: false` or unequal decision/local/remote HEADs
cannot be `fresh: true`. A behind local base advances only on the selected-base
checkout via `git merge --ff-only`; wrong checkout, dirty state, missing refs,
fetch failure, divergence, resolution drift, or post-sync mismatch fail closed.
Prepare requires the preceding validator/guard post-sync resolution digest and
the same resolver inputs. It preserves explicit/config/config-candidate/remote-default provenance.
Resolution and result facts are stdout-only. Neither standalone nor workflow
mode creates resolution/result evidence files, leases, release commands, or
cleanup state. The compatibility query consumes the current post-sync digest
and reruns the shared core before its reads. Workspace mutation freshness is
owned and revalidated by `guru-create-task-workspace`; identity/digest drift
requires a fresh Skill invocation.
Legacy `--create-issue-confirmed`, `--create-worktree`, and `--create-task`
fail closed before any write and point to active `guru-create-task-workspace`.

The AI should read the issue and provide a semantic English short-name through
`--short-name`, `--workspace-slug`, and `--task-slug` when the title is Chinese,
non-ASCII, or too generic; use `--branch` only when a special explicit branch
name is needed. Recommended worktree/task slug format is
`NNN-business-capability`; when `--branch` is omitted, recommended branch format
is `<branch-type>/NNN-business-capability`, for example
`feat/052-resume-detail-inline-attachment-preview`. `prepare-task` does not
perform Chinese transliteration or pinyin conversion; it deterministically
infers a supported branch type, assembles the name, checks conflicts, and blocks
low-information names before executor side effects.
When `workspace_mode: worktree`, create the execution workspace and task through
active `guru-create-task-workspace`. Task creation consent is not approval to run bare
`python3 ./.trellis/scripts/task.py create ...` in the source checkout.
Executor paths also enforce `naming_quality` and fail closed before creating a
worktree, branch, or Trellis task if the generated or overridden name is low
information, such as `issue-52`, `52-issue-52`, a bare number, or only generic
tokens like `bug`, `fix`, `task`, `work`, `update`, or `change`.

Only passed Gate plus confirmed active scope may mutate. Passed plus refused,
`reroute`, and `blocked` produce checker-validated zero-write `cancelled`,
`refresh_review`, and `blocked` results. Public result stdout omits the absolute
workspace path; the checker derives it from current config, reviewed slug, and
live Git facts, while local absolute mappings remain ignored runtime only.

The tracked `task-start-context.json` provides only portable `workspace_slug`,
`task_workspace_id`, and repo-relative `task_artifact_dir`; it never provides an
absolute `workspace_path`. In worktree mode, derive and validate the machine-local
task worktree from the current checkout, `.trellis/.runtime/guru-team/**`,
`git worktree list`, and `check-workspace-boundary.sh --task`. Before writing or validating
`planning-approval.json`, `phase2-check.json`, `agent-assignment.json`,
`reviews/*.md`, `review.md`, or `review-gate.json`, run:

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

The helper reports expected workspace, actual repo root, source checkout
status, task worktree status, and suspicious current-task artifacts or review
metadata in the source checkout. It is a deterministic validator/fact snapshot,
not stale judgment, cleanup, or patch migration. Editing tools without an
explicit `workdir` must use absolute paths under the task worktree confirmed by the
boundary helper. The #76 liveness checker uses this source/task fact
layer: source checkout `HEAD`, dirty status, diff stat, or mtime changes are
`workspace_boundary_violation_progress`, not stale evidence.

`create-task-workspace` reruns the shared core before GitHub or worktree/task mutation.
Each run keeps `preflight.base_freshness` in the current result only and requires
clean decision/local/remote equality. Planner evidence never replaces either
mutation-time guard, preventing new task branches from starting from a stale
local base.

The plan binds the initial checker-passed `post_sync_resolution_sha256`. The
executor runs the shared resolver/sync core once before the first confirmed
business mutation. A newly advanced remote may safely fast-forward the selected
base, but then returns `refresh_review` before issue/workspace/task/artifact or
runtime writes. An unchanged post-sync identity continues normally.

The active package uses schemas `guru-task-workspace-plan-1.0` and
`guru-task-workspace-result-1.0` plus runtime commands
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`. It keeps workflow/standalone preconditions
identical, uses mutually exclusive issue/workspace confirmations, and exposes
only `created`, `refresh_review`, `cancelled`, and `blocked` exits. A draft
issue creation invocation always stops at `refresh_review`; branch/worktree/task
creation happens only after full Intake re-entry.

Guru preset apply/update/reapply and the workspace executor do not read,
create, copy, initialize, restore, or delete `.trellis/.developer` or
`.trellis/workspace/**`; they do not require `init_developer.py`. Existing
official identity/journal bytes are preserved, and official Trellis remains free
to use those paths separately. In an isolated subprocess, the exact executor calls
official `common.task_store.cmd_create` with the resolved assignee and disables the
developer accessor only for that handler invocation. `task.json.assignee` and
`task.json.creator` therefore both equal the reviewed login, while existing identity
bytes remain unchanged. The executor writes only four tracked
task-local Intake artifacts plus ignored runtime mappings. The real local A/B
fixture verifies both merge orders without a remote PR or concurrent process.

The installer manages `schemas/closeout-plan.schema.json` and
`schemas/finish-summary.schema.json`, writes top-level
`session_auto_commit: false` into `.trellis/config.yaml`, adds
`.trellis/workspace/` to `.gitignore`, and never creates or rewrites workspace
journal/index files. Shared start and installed Codex/Cursor SessionStart hooks
do not open, enumerate, read, count, or output workspace journals. Before
archive, closeout recovery validates committed plan/readiness, the active
locator, repo/base/head, review gate, current/remote HEAD, and exact PR
identity. Prepare parses `.trellis/config.yaml` with the installed official
parser and supports only missing/empty `hooks.after_archive`; invalid or
non-empty hook configuration is rejected without execution. Immediately before
official move it also checks the live archive month, empty index, exact
untracked set, regular-file/mode contract, and evidence blob bytes. A stale
committed month remains active and is recoverable only by a new dry-run digest
plus an additive plan/readiness supersession commit; no history rewrite or
directory migration is used. After the official move but before the exact archive commit exists,
it still requires the complete archived working-tree layout, exact
dirty/staged paths, blob continuity, and official `task.json` delta; an absent
or mismatched commit remains fail closed. Once current `HEAD` is the exact
planned archive commit, both normal and plan-only archived reentry load the plan
from that commit blob; the immutable plan and Git parent/path/tree/blob facts
are authoritative, so missing or tampered archived working-tree files do not
block the exact push, remote title/body check, HEAD alignment, or
draft-to-ready. A plan-only archived directory is resolvable only by the
`trellis-finish-work` recovery entry; ordinary task commands still require
`task.json`. The real-PR final summary's deterministic bytes/digest participate
in pre-move, incomplete-recovery, and exact-commit continuity. The first two
paths rebuild expected bytes against the already-bound remote PR. Exact
recovery reads only the immutable archive commit's `finish-summary.json` blob
to recover the original PR number/URL and verify those bytes without invoking
the general summary artifact validator; it never reads the working-tree
summary. Missing, closed, or replacement PRs fail closed. Other archived
artifacts remain unopened for semantic validation.
Installed final projection, incomplete recovery, and exact recovery share one
strict PR URL parser. GitHub owner/repository identity is case-insensitive,
while the canonical summary URL preserves the exact valid casing returned by
the remote PR (for example `microsoft/PowerToys`). A different repository,
transport, invalid number, extra path, query, or fragment remains fail closed.
The plan-only path reads the immutable plan from the current commit blob and
runs a dedicated fail-closed boundary before GitHub or fast-path actions. Git
toplevel, configured/effective repository, current head branch, available base
ref, current HEAD transaction, expected digest, task identity, and
active/archive locators must all match. Missing context is never an
unconditional boundary bypass; ordinary task discovery and commands retain
their `task.json` and worktree-mode `task-start-context.json` requirements.
The finish entry validates the raw locator before ordinary resolution or
canonicalization. Only a basename, exact former active locator, or exact
archive locator may select plan-only recovery. Path-like input receives
component-wise `lstat` from the repo root through the final task directory
before any fallback. Basename input preflights `<repo>/<basename>`, the active
candidate, the archive root, and archive candidates in ordinary resolver order.
Every direct or archive candidate first retains only `symlink_component`
evidence, then uses the ordinary resolver's exact follow-symlink
`directory + task.json` predicate. A matching alias fails closed, while an
unmatched alias continues to the next candidate. These checks reject internal/external,
relative/absolute, ancestor/final, multilevel, dangling, and loop symlinks
before raw evidence is discarded. The ordinary resolver then preserves
explicit `task.json`, active task, and normal archived `task.json` precedence.
Plan-only fallback runs only after ordinary not-found:
an exact archive locator selects that candidate, while basename/former-active
fallback requires a unique archive-month match and fails closed on ambiguity.
The plan-only target must still equal the plan's canonical archive locator.
Only the verified Darwin `/var` -> `/private/var` system mapping may re-anchor
an outer path; arbitrary `samefile` and user aliases are never trusted.

Current-checkout direct edits while `no_task` is active are allowed only as an
explicit user override. The user approval must say this turn should skip
creating or reusing a GitHub issue, Trellis task, worktree, and branch. Before
editing, the AI must summarize skipped artifacts, current checkout, current
branch, dirty state, side effects, changed-file scope, and the separate
commit/push/PR approval boundary.

The installed workflow tells AI sessions to run a Middle-platform Knowledge Gate
when a task may touch Guru Team SDKs or frameworks. If `guru-knowledge-center`
MCP is available, the AI queries `project_domain=middle-platform` and persists
citations in task artifacts. If the MCP is unavailable, the default
`optional_warn` mode warns and continues.

The workflow also requires a Phase 1 `Docs SSOT Plan`. Task artifacts should
record task-scoped deltas and links, while durable requirements, designs, test
plans, deploy / operations guides, versioned docs, or equivalent repo docs
remain the long-term source when they exist. The plan is preferably authored in
`design.md`; `prd.md` records docs state and requirements impact, and
`implement.md` records the checklist / checkpoint.

The plan records docs state (`complete_docs`, `partial_docs`, `stale_docs`, or
`no_docs`) and strategy (`ssot_first`, `delta_first`,
`bootstrap_or_repair_docs`, or `no_docs_update_needed`). It also records
evidence paths, affected durable docs or checked no-update paths, task artifact
deltas to merge back, and any required merge checkpoint, minimum repair scope,
follow-up limit, or no-update reason. Finish and Branch Review Gate evidence
must later record the reconciliation outcome, but the strategy choice belongs
in Phase 1 planning.

Installed implement/check agents consume that plan during Phase 2. The
implementation handoff names the strategy, durable docs sync result, task
delta merged back, task-history-only content, no-update or follow-up / PR
limits, and whether implementation inputs came from durable docs or an
approved temporary task delta. The Phase 2 check agent then verifies durable
docs, task artifacts, code/schema/config/deploy/test, and validation/test
coverage against the same strategy. `delta_first` must merge durable docs
before final Phase 2 check; `ssot_first` uses revised durable docs as primary
input; `bootstrap_or_repair_docs` must complete the minimum repair or name a
bounded follow-up and PR limitation; `no_docs_update_needed` must still have a
concrete reason after the final diff is reviewed.


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 时，recorder 在 reviewed content push 后从 immutable closeout plan 生成 pending machine evidence；verifier 成功后只替换为 passed。plan、readiness、artifact 与 ledger 形成 exact pre-draft metadata commit，push 并校验 remote HEAD 后才允许绑定 draft PR。缺失、重复、pending、失败、篡改、HEAD 不匹配或 stale 均阻止创建 PR；human reason 不参与 machine identity，该门禁不创建 tag，AI 仍负责 close scope 与 PR readiness 判断。
