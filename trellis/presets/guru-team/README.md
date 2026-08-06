# Guru Team Trellis Preset

The preset installs companion assets, Guru Skill packages, and three additive
Guru finish entries for the `guru-team` Trellis workflow into an existing
Trellis project.

It does not run `trellis init` and does not modify Trellis upstream files.
It is idempotent: identical files are skipped, missing files are installed,
Guru-managed companion assets are upgraded in place with `.bak` backups,
and existing `.trellis/guru-team/config.yml` is preserved. Current-only
ownership schema 3.0 defines exactly 11 anchored Guru rules, nine managed
claims, and three additive finish overlays. Official Trellis paths are outside
that contract. A non-current ownership or installed manifest fails closed
before mutation; unknown edits to current Guru-owned assets are preserved with
deterministic `.new` remediation.

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
returns one concise terminal result, `trellis-check` / channel `check` uses
that result with live repository evidence to produce the compact final Phase 2
semantic result, and an independent review sub-agent reviews
the full committed branch diff before the main session records Branch Review
Gate. An explicit `codex.dispatch_mode: inline` value is preserved as a
user-selected downgrade or debug mode; missing sub-agent evidence must fail
closed unless explicit inline/self-exemption artifact evidence exists.

The normal path creates no `implementation-handoff.md`, no
`implementation_handoff` checkpoint field, and no periodic liveness journal.
Implementation terminal output remains ephemeral input to the semantic check
owner; only its compact final schema 4.0 result is recorded in ignored runtime.

The preset also maintains one bounded AI-first principles block in the target
root `AGENTS.md`. Missing files are created, existing user content outside the
stable markers is preserved byte-for-byte, a single older block is refreshed,
and repeated apply is idempotent. Duplicate, unbalanced, embedded, or reversed
markers fail closed before target activation. The JSON result reports
`agents_principles`; root `AGENTS.md` remains user-owned and is not listed in
`install.managed_assets`.

Trellis-owned sub-agent, hook, command, prompt, bundled Skill, and channel-runtime
agent files remain owned by official `trellis init` / `trellis update` / version
upgrade. The preset does not replace those files. Guru-specific semantic behavior
lives in the active marketplace workflow and additive `guru-*` Skill packages;
the preset only configures the supported Codex dispatch mode needed to invoke the
official Trellis agents.

Platform distribution is selectable. Shared `.agents/skills/guru-*` packages are
always installed; selected platforms receive their matching `guru-*` package
copies and additive finish entry. Defaults are Codex and Cursor. Repeat
`--platform <name>` to select a specific set; supported values are `codex`,
`cursor`, and `claude`. `--all-platforms` selects all three. `--platform` and
`--all-platforms` are mutually exclusive, and invalid platform names fail
closed.

The installed manifest records the three additive entries in a separate
top-level `overlays` provenance domain with closed fields
`schema_version/status/selected_platforms/files/removals/conflicts/sidecars`.
Missing entries install, canonical-equal entries remain unchanged, and only a
target matching its exact previous managed hash is upgraded after writing
`.bak`. Unknown or invalid provenance is preserved with deterministic `.new`
and blocks staged activation. Platform shrink deletes only previous-hash-equal
entries; unknown edits remain in place and block.

A fresh target may omit the installed manifest. An existing manifest must use
the complete current schema 2.0 and contain the complete current `overlays`
domain. A non-current schema, missing or extra top-level field, or malformed
overlay provenance fails current-contract validation; the installer
does not recover ownership from `install.managed_assets`, entry markers, or
`Guru Team` text. Current installed validation reconstructs the selected
platform inventory and checks hashes, modes, removals, unselected paths, and
exact `.new/.bak` state independently of the flat managed-assets list.

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
example `gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`. The current stable
mapping is annotated tag `v0.6.5-guru.3`, peeled commit
`dbcbbb2d2776a3952b643b6bcce0a2693d103273`, extension revision
`0.6.5-guru.25`, and official `@mindfoldhq/trellis` `0.6.5`. Workflow
marketplace and preset sources must use that same immutable tag. Unpinned
`gh:castbox/guru-trellis/trellis` is a latest/canary source and should be
reported as mutable provenance.

## Current Ownership Contract

The current-only schema 3.0 inventory and schema live at:

- `trellis/presets/guru-team/ownership/upstream-ownership.json`
- `trellis/presets/guru-team/ownership/upstream-ownership.schema.json`

The inventory describes only assets Guru Team owns now. It contains exactly 11
anchored rules for the installed runtime, canonical workflow and Skill roots,
`guru-*` package discovery roots, and the three finish entries. It exposes nine
current managed claims and does not claim any official Trellis namespace.

The canonical overlay tree contains only these three Guru-owned additive entries:

- `.codex/prompts/guru-finish-work.md`
- `.claude/commands/guru/finish-work.md`
- `.cursor/commands/guru-finish-work.md`

The extension manifest and inventory contain exactly nine anchored Guru namespace
claims. No claim covers an upstream Trellis namespace.

Before any target activation, the installer validates the source inventory,
schema, exact managed claims, overlay tree, `MANAGED_ASSET_PATHS`, active Skill
ids, canonical package set, and anchored Guru discovery namespaces. A fresh
target may omit `.trellis/guru-team/extension.json`; once present, that file
must satisfy the complete current installed-manifest schema 2.0. Non-current
schemas, missing or extra top-level fields, unknown claims, unexpected
overlays, malformed provenance, and unresolved sidecars fail closed before
target mutation. Only current schema 3.0 is valid ownership input.

For current Guru-owned assets, missing paths install, canonical-equal bytes stay
unchanged, an exact previous managed hash creates `.bak` before replacement,
and an unknown local edit is preserved with canonical bytes in `.new` when
safe. Conflicts prevent staged activation.

Maintainers can run the read-only ownership gate directly:

```bash
./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
python3 ./trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
```

The validator reports schema 3.0, 11 rules, nine managed claims, three additive
overlays, and the current registry/package facts. These bindings provide normal
version and drift detection, not semantic ownership judgment; AI review still
owns whether a proposed current owner is valid.

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
git clone --depth 1 --branch v0.6.5-guru.3 \
  https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --platform codex \
  --platform cursor
```

Examples:

```bash
# Shared Guru packages plus Claude packages and finish entry.
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project \
  --platform claude

# Shared Guru packages plus all platform packages and finish entries.
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
`--platform claude --platform codex --platform cursor`, checks that `.trellis/workflow.md`
exists, verifies that the active workflow requires the three Guru Team planning
artifacts, verifies that `check-env.sh` and `version.sh` are executable,
asserts `.trellis/guru-team/extension.json` satisfies the complete current
installed-manifest schema 2.0, derives its managed inventory from canonical
current assets, and verifies the three selected Guru finish entries match their
canonical additive overlays. Source ownership validation must report schema
3.0 with 11 rules, nine managed claims, and three overlays before and after
`trellis update --force` plus workflow/preset reapply.
It also asserts target `.trellis/spec/**` and
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
pre-mutation gate for both apply operations. The expected clean result
is a current ownership pass, complete installed-manifest provenance, zero
conflicts, and zero sidecars.
A controlled bare remote and fake GitHub adapter drive the already-installed
`finish-work.sh` through dry-run digest, formal draft binding, official archive,
three-way HEAD equality, ready transition, and clean-tree assertions once after
install and once after update/reapply. The fixture uses installed wrappers,
companion, schemas, config, workflow, and official `task.py`; it does not copy
canonical runtime assets into the target. It also executes the installed
`test_finish_family_integration.py` before and after update/reapply, covering
the 13 Finish exits, six route groups, Guru entries, terminal evals, and
public/private boundary. A final recursive scan must find no `.new` or `.bak`
sidecars. It intentionally lives in this
source repository and is not copied into target business repos as a managed
companion asset.

## Dogfood Overlay Drift Check

Only the three additive Guru finish entries remain under
`trellis/presets/guru-team/overlays/`. For a current installation, use this
sequence:

1. install the target official Trellis CLI, currently `0.6.5`;
2. run the official `trellis update` or required Trellis version upgrade;
3. preview and switch the `guru-team` marketplace workflow from the selected
   immutable release tag;
4. reapply the Guru preset from that same tag for the selected platforms;
5. preserve unknown local edits and inspect every `.new` / `.bak` sidecar;
6. run ownership, installed-package, dogfood drift, and recursive sidecar checks.

For this source repository, the final preset/drift commands are:

```bash
./trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo . \
  --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

`check-dogfood-overlay-drift.sh` is read-only. It first validates current
ownership schema 3.0, 11 Guru rules, nine managed claims, and the three-entry
canonical overlay tree. It then compares those three additive
overlays with same-path installed dogfood copies and exits non-zero for
ownership failure, missing copies, or changed bytes. It never treats an
upstream-owned path as a dogfood overlay.

A passing drift check is not a replacement for AI review or the Branch Review
Gate.

## Installed Files

Preset 是完整 Guru Team extension configurator。除 companion assets、
Guru Skill packages 和三个 additive finish entries 外，它验证
`trellis/skills/guru-team/registry.json`，将
registry/schema/active packages 安装到 `.trellis/guru-team/skills/`，并把
active package 分发到 shared root 与明确选择的 Codex/Cursor/Claude roots。
Test fixtures 永不安装，未选择的平台 root 不因 skill 分发
而创建。

Preset 安装 current Interface 1.3 schema 与 registry 1.2。每个 active registry row
只允许 `interface_schema_id=guru-team-skill-interface-1.3`。Live Intake 合同为
六包/23 exits；current registry、discovery DTO、invocation 与安装 provenance 不接受
历史 manifest、schema、example 或 eval。`production-current-v1` 是
planning/check/commit 唯一 current manifest，精确绑定
三包、十 profiles、11 exits、current output schemas、四条 authoring-seed edges、private
artifact ids、examples 与 eval cases；不存在 alternate production projector 或 fixture。
当前 active closure 为 14/54，live Intake 合同为 6/23。Preset 在一次 staging
transaction 中安装 current registry、
Interface 1.3、production-current manifest/schema、十三包 public
contracts/wrappers/corpora、registry、extension 和 selected-platform copies；mixed graph
失败关闭。Representative fixture schema ids 和 fixture wrapper 不进入
production registry、extension inventory、installed files 或 selected-platform copies。
其中 `production-current-v1` 严格保持 planning/check/commit 三包与 11 exits；
`guru-review-branch` 作为 additive active package 不扩大该 manifest 的 membership。
同一 transaction 还安装 Interface 1.3 additive
`skill_input_authoring_seed` shape、planning self-reentry、check passed 到 initial commit、
commit self-reentry、commit-to-Branch-Review、Branch-Review-to-publication 与
finalization family 共十二条声明 edge 的 target-owned
authoring examples 与 partition/no-overwrite/full-target-schema probes。该 kind 不增加第五种
projection operation；部分 edge、缺失 authoring example 或 canonical/installed/platform
字节不一致均视为 mixed production graph。
Interface 1.3 scalar `required` 为显式 boolean；preset 安装的 `guru-sync-base` 将
`base_branch` 标为 optional，省略调用继续复用 formal resolver。
Fixture source validation 强制 Skill consumer 使用 active registry exact canonical path 与
相同 target id 的 target-owned input，对非 direct projection 与 direct 到 scalar CLI 做
required 与映射/normalizer 后全域兼容证明，分别检查 public/private
schema id/path 互斥，并要求 wrapper 完整匹配 dispatcher-only template。

Current ownership schema 3.0 只声明 11 条 Guru rules、9 条 managed claims 与 3 个
additive overlays。Preset 不安装或更新任何 `trellis-continue`、`trellis-start`、
`trellis-finish-work`、agent、hook 或 runtime-agent payload。Branch Review `passed`
后的 publication/finalization
路由由 active marketplace workflow 的 mandatory Skill markers 与 additive
`guru-review-task-publication` / `guru-finalize-task` packages 承接。Installer
只验证 current ownership、provenance 与 Guru namespace，不复制 owner Skill 的
semantic 结论。

新增 additive active `guru-verify-extension-installation` package 安装两个
structurally distinct inputs、四个 per-exit contracts、private
`marketplace-verification.json` schema、seven-case production corpus 与 thin wrappers。
它不修改 live Intake 6/23 或 production 3/11 合同。Active
`guru-finalize-task` 另行安装六个 distinct profiles、六个 `exit_id` outputs、
private gate、八条 production eval cases 与四个 finalization runtime wrappers，并
具体绑定 #116/#117 producer edges。Source/installed package closure 为 14 Skills /
54 exits；global workflow marker closure 为 14 invokes / 54 exits / 31 targets。
1.3 closed schema 的 `pattern` 只接受 durable spec 定义的 printable-ASCII portable
grammar，并按 ECMA-262 Unicode-mode search 语义执行；Python-only regex、Unicode source
pattern 和未声明 shorthand 会在 source/installed validation 中 fail closed。

Managed executable
`.trellis/guru-team/scripts/bash/discover-skill-contract.sh` 提供 exact discovery：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root . --mode installed --skill guru-sync-base --json
```

`1.3` 返回 input/invocation/per-exit output/consumer/projection/private-artifact
locators。Missing/drift/version mismatch 使用 stable
`code`、repo-relative `field_path` 与 `remediation` fail closed。

Active `guru-approve-task-plan` package 随 registry-driven install 分发到 shared root 与所选
Codex/Cursor/Claude discovery roots，并依赖同一 preset 安装的 schema
`guru-planning-approval-3.0`、shared dispatcher 和
`record-planning-approval` / `check-planning-approval` runtime commands。该分发是
Guru-owned additive content，不扩展当前三文件
`trellis/presets/guru-team/overlays/**` 集合。

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
- `.trellis/guru-team/config-template.yml`
- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/schemas/closeout-plan.schema.json`
- `.trellis/guru-team/schemas/finish-summary.schema.json`
- `.trellis/guru-team/schemas/marketplace-verification.schema.json`
- `.trellis/guru-team/scripts/bash/check-env.sh`
- `.trellis/guru-team/scripts/bash/version.sh`
- `.trellis/guru-team/scripts/bash/prepare-task.sh`
- `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh`
- `.trellis/guru-team/scripts/bash/check-skill-packages.sh`
- `.trellis/guru-team/scripts/bash/discover-skill-contract.sh`
- `.trellis/guru-team/scripts/bash/discover-skill-evals.sh`
- `.trellis/guru-team/scripts/bash/run-skill-evals.sh`
- `.trellis/guru-team/scripts/bash/run-skill-command.sh`
- `.trellis/guru-team/scripts/bash/invoke-stage0-skill.sh`
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
- `.trellis/guru-team/scripts/bash/record-agent-recovery.sh`
- `.trellis/guru-team/scripts/bash/check-agent-recovery.sh`
- `.trellis/guru-team/scripts/bash/prepare-task-commit.sh`
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh`
- `.trellis/guru-team/scripts/bash/create-task-commit.sh`
- `.trellis/guru-team/scripts/bash/format-merge-commit.sh`
- `.trellis/guru-team/scripts/bash/review-branch.sh`
- `.trellis/guru-team/scripts/bash/check-review-gate.sh`
- `.trellis/guru-team/scripts/bash/record-task-publication-review.sh`
- `.trellis/guru-team/scripts/bash/check-task-publication-review.sh`
- `.trellis/guru-team/scripts/bash/execute-extension-verification.sh`
- `.trellis/guru-team/scripts/bash/record-extension-verification.sh`
- `.trellis/guru-team/scripts/bash/check-extension-verification.sh`
- `.trellis/guru-team/scripts/bash/invoke-extension-verification.sh`
- `.trellis/guru-team/scripts/bash/preview-finalization.sh`
- `.trellis/guru-team/scripts/bash/record-finalization-gate.sh`
- `.trellis/guru-team/scripts/bash/check-finalization-gate.sh`
- `.trellis/guru-team/scripts/bash/execute-finalization-transition.sh`
- `.trellis/guru-team/scripts/bash/finish-work.sh`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`

Production skill registry 包含 active `guru-create-task-workspace`、`guru-sync-base`、
`guru-discover-change-context`、`guru-clarify-requirements`、
`guru-review-contract-wording`、`guru-review-change-request`、
`guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`、
`guru-finalize-task`、`guru-review-branch`、`guru-review-task-publication`、
`guru-select-workflow-mode`、`guru-verify-extension-installation`。这十四个 active packages 共声明
54 个 external exits。`guru-finalize-task` 的
`workflow_integration_state=integrated`，package 可直接发现且拥有唯一 global
invoke 与六个 exit marker。当前 canonical extension version
`0.6.5-guru.25` 已由 stable source `v0.6.5-guru.3` 发布；该 annotated tag peeled 到
`dbcbbb2d2776a3952b643b6bcce0a2693d103273`，并以官方 Trellis CLI `0.6.5` 为目标。
Repo release tag 与 extension revision 是独立版本轴；workflow 与 preset 必须 pin 同一
immutable tag。Preset 将 active package
（含 interface、artifact schema、
example、thin wrappers 与 tests）安装到 `.trellis/guru-team/skills/`，并分发到 shared
root 和所选 Codex/Cursor/Claude skill roots；planned id 不安装。升级后必须处理
`.new`/`.bak`，再通过 source/installed package validation 与 dogfood drift。

Interface 1.3 中 `workflow` 表示 global mandatory routing，`standalone` 表示
所选平台 direct discovery。两种 mode 都依赖完整 current Guru Team runtime；单独
复制 Skill 目录不是 self-contained/portable 安装。Preset 因此同时安装
`.trellis/guru-team/scripts/bash/run-skill-command.sh`、extension runtime capability、
audited package inventory 与 discovery copies。Wrapper 只能经过该 dispatcher；non-current runtime、
缺失 manifest/dispatcher、API/command mismatch 或 managed drift 会在 companion command
之前 fail closed，并提示安装/升级完整 preset、处理 `.new` / `.bak`、重跑验证。

`guru-verify-extension-installation` 的 standalone discovery 仍依赖完整 preset：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root . --mode installed --skill guru-verify-extension-installation --json
```

Package wrapper 在 AI 完成 applicability/profile/adequacy/findings review 后才调用
executor、recorder、checker 与 public invocation。Task-bearing 调用只写一个 task-local
owner result；taskless standalone 不写 repo cache/index。Production eval 证明两个
inputs、四 exits、retry/unavailable/stale route；真实 pushed-remote clean install 另行
证明 init/preview/switch/update/reapply/ownership/sidecar/README/redaction。两者互不替代。

Verifier public repo/ref 指向 target repository；task-bearing source provenance
来自 target checkout 的 installed manifest，并要求 `tree_state=clean` 后才解析 source
ref 或 clone。Runtime 使用隔离的 target/source
checkouts：reviewed-content 只属于 target，installer/canonical package/ownership/source
sidecars 只属于 source。Annotated source tag 记录 direct object 但选择 peeled commit，
并要求 selected commit 等于 manifest commit。Taskless fallback 仅适用于显式 source
verification 且 manifest absent；malformed manifest 不降级。Source clone locator 必须为
credential-free canonical GitHub HTTPS，unsafe locator 在 clone/artifact 前阻断。
Private/execution schema 3.0 current-only，public inputs 与四个 exit DTO 未改变。

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
Task-local package/runtime 还以 validated task/snapshot locators 精确绑定 owner checker，
用 private `task_worktree_state` 记录除 fixed snapshot/runtime 外的完整 dirty worktree。
Different-byte fixed snapshot 仅在 prior regular/trackable、exact expected prior digest 与
完整 new/live/worktree validation 通过后 formal replace，并记录
`superseded_snapshot_sha256`；失败保持 prior bytes，same-byte retry 幂等。Preset、selected
platform copies、fresh install 和 current update/reapply 必须保持这些 schema/runtime/
wrapper/test bytes 与 executable modes 一致。
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
preconditions相同；answered evidence、question lifecycle与objective payload/live mutation均
fail-closed验证。Pre-task/standalone stdout-only，
active-task Scope Change Gate mandatory invoke本Skill，并由caller-aware clear router恢复planning或
exact interrupted progression；只验证 compact ledger 与当前 live owner linkage，不创建专用 clarification artifact。Throwaway initial install、
`trellis update`、workflow re-selection与preset reapply均执行 standalone record/check probe，
并验证 `clear` / `needs_context` / `refresh_context` / `retarget_context` / `new_task` /
`blocked` consumers。只接受 closed 2.0 artifact；其他 schema version 在 normalization 前
fail closed，recorder/checker 不执行迁移或投影。

Active-task `clear`/`new_task` 必须携带非空七类 terminal proposal set，每个五类 scope
classification 保存已选择的 disposition，并 exact 绑定 compact owner-result
`decision_trail`。该 trail 只含 `trail_id`、proposal id/digest/decision 与 live GitHub authority
kind/URL/content checksum；`issue-scope-ledger.json` 是 closed scope-only 2.0，只含 schema
version 与 primary/close/related/followup issue。planning/context/review/stale/interrupted/re-entry
evidence 由 checker 从 owner 与 live facts 重读。Result、trail、runtime、checkpoint、
archive、schema 和 public DTO 均不得保存用户授权状态、原话、ref、时间或 digest。
`mechanism_removed/replaced` 使用 optional origin，不进入 trail/action mutation。GitHub authority mutation
必须返回 `refresh_context`；context 时间覆盖 live authority 后 task update preimage 绑定当前 context digest，
不要求第二次 refresh；`new_task` 只向 #112
传递 side-effect-free draft，不在本 package 创建 issue/task。

`guru-review-contract-wording` package 安装
`guru-contract-wording-review-1.0` schema、example、contract、tests 和两个
executable dispatcher wrappers。Workflow/standalone preconditions 相同；固定 profiles
为 `change_request`、`planning_artifacts`、`explicit_paths`，typed exits 为 `pass`、
`content_changed`、`blocked`。Vocabulary、classification semantics、AI rewrite/review
loop 和 interaction policy 只存在于 canonical package contract；runtime 只负责固定 scope、
scan、hash/digest、unchecked、schema/freshness 与 Gate/exit 结构校验。Installed runtime
同时拒绝 selected comment 缺 author/updated time，并为 live issue revision 校验 exact
proposed payload bytes、preimage 和 current reread mutation-result identity；它不接收或校验授权 digest。
All profiles emit stdout-only owner-private results. A mapped same-profile
re-entry discards the prior result, rebuilds current scope/scan, and creates no
task-local replacement or supersession digest chain. `planning_artifacts:pass`
is consumed immediately by its typed-exit router; it is not written as
`contract-wording-review.json`. It must still contain the canonical contract's exact
`semantic_review.ai_review_gate.planning_checked_dimensions`，全部显式 AI-reviewed 为 true
才能成功。Runtime 只验证该 planning-only 字段的 shape/value；the planning owner rereads
the current three planning files and never imports wording history. 其它 profile 禁止该字段。
Fresh install、dogfood、四平台
discovery copies 与 update/reapply 必须同时包含 package、commands、schema 和 route markers。

`guru-review-change-request` package additive 安装
`guru-change-request-review-1.0` schema、deidentified `issue-review.json` example、contract、
tests 和两个 executable dispatcher wrappers。Runtime assets 是
`.trellis/guru-team/scripts/bash/record-change-request-review.sh` 与
`check-change-request-review.sh`。Workflow/standalone preconditions 相同；三类 target、current
context/clarity/wording linkage、十项 dimensions、findings、scope conclusion、AI Gate 与五出口
由 canonical semantic package 拥有。Runtime 只重建 portable projection/linkage/facts 并校验
schema/hash/ref/freshness/consumer/ready invariant，不生成 readiness、finding、delivery unit 或
route。Pre-task/standalone stdout-only；#112 直接消费 checked exit，只持久化
`issue-scope-ledger.json`，不复制 `issue-review.json`。

五出口固定为 `ready` -> active `guru-create-task-workspace`、
`clarify_requirements` -> `guru-clarify-requirements`、`review_wording` ->
`guru-review-contract-wording`、`refresh_context` -> `guru-sync-base`、`blocked` ->
`change-request-review-blocked`。Fresh install、selected platform discovery、installed validation
与 update/reapply 必须证明 active workspace package 存在、`ready` 只路由到该 package，
并覆盖三类 target、五出口和 zero cache/sidecar residue。

`guru-create-task-workspace` package 安装
ignored-runtime `guru-task-workspace-plan-2.0`、`guru-task-workspace-result-2.0`、contract、examples、tests
和三个 executable dispatcher wrappers。Draft invocation 创建 exact issue 后固定
`refresh_review`；open issue invocation 使用独立 workspace/task confirmation。Assignee 按
explicit、single issue assignee、zero issue assignees/current login、multiple/unresolved user
choice 顺序解析。成功后除 official `task.json` 外只写 tracked task-local
`issue-scope-ledger.json` 与 ignored `.trellis/.runtime/guru-team/**` mappings。

Draft create 前使用 exact open title/body/labels 与 creation time执行 0/1/>1 recovery；
唯一匹配被恢复，零匹配才创建，多个匹配阻断。完整 Intake重入时，workflow-created issue
携带完整 checker-passed created-issue result，并与 fresh context 的 canonical live
existing-issue identity一致；该 context使用`kind=issue`与 null `issue_binding`。

Guru Skill packages are distributed independently of overlays:

- canonical registry/schema/packages/tests are installed under
  `.trellis/guru-team/skills/`;
- active packages are always copied to `.agents/skills/guru-*/`;
- selected Codex, Cursor, and Claude platforms receive matching
  `.codex/skills/guru-*/`, `.cursor/skills/guru-*/`, and
  `.claude/skills/guru-*/` copies.

The canonical overlay tree has exactly three files. Each is installed only when
its platform is selected:

- Codex: `.codex/prompts/guru-finish-work.md`;
- Cursor: `.cursor/commands/guru-finish-work.md`;
- Claude: `.claude/commands/guru/finish-work.md`.

Official Trellis owns every `trellis-*` Skill, command, prompt, hook, platform
agent, bundled reference, and `.trellis/agents/*` runtime file. The preset never
installs, replaces, or managed-upgrades those paths. Official update/upgrade
manages them independently; preset reapply validates only current Guru-owned
paths.

`install.managed_assets` is derived from the current deterministic
companion/additive inventory, including the selected Guru finish entries.
Distributed Skill-package files are recorded separately in
`skill_packages.files`; README text does not duplicate a numeric inventory.

The active `.trellis/workflow.md` is installed or switched through the official
Trellis workflow marketplace:

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 \
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
URLs or issue numbers, official Trellis platform entries that load the active
workflow, and additive `guru-finish-work` (Codex prompt, Claude
`/guru:finish-work`, Cursor `/guru-finish-work`). The preset does not patch
`trellis-start`, `trellis-continue`, or `trellis-finish-work`; stable mandatory
Guru routing is defined by `.trellis/workflow.md`.

Planning, check, review, and publish helpers are internal companion script
subcommands used by the workflow; they are not daily user-facing entries.
`guru-approve-task-plan` owns the semantic review and the single ignored-runtime
`planning-approval.json` checkpoint. It consumes current live authority,
wording, planning, Docs SSOT, and issue scope, reviews eight semantic
dimensions, and returns one of four typed exits. The installed
`record-planning-approval.sh` and `check-planning-approval.sh` commands preserve
and validate the compact `guru-planning-approval-3.0` result; they do not create
semantic conclusions or persist authorization. Every non-3.0 input fails closed;
the owner accepts only a newly checked current invocation. Scope
ledger task identity and requirement authority use the same issue-category
projection. The checker revalidates the invocation base/HEAD/dirty snapshot
while the task is still planning; after activation freshness is based on
planning, Docs SSOT, authority and wording content, not later implementation
HEAD drift, metadata tail, or unrelated dirty paths. `task.py start` remains
only a status transition. The Planning public wrapper deletes its checkpoint
after the checked typed output passes schema validation; activation and Phase 2
consume only the DTO and current live facts.
`resolve-human-artifacts.sh` is the deterministic fact layer for phase replies:
before a planning stop, Phase 2 completion, Branch Review Gate result,
finish-work dry-run reply, or final archive/publish reply, the AI runs it and
renders a `Markdown 产物 review 表` with only `prd.md`, `design.md`,
`implement.md`, and `pr-body.md`. Missing files are shown without Markdown
links, and JSON gate/evidence is not part of the standard table.
`record-phase2-check.sh` records the AI-authored closed `guru-check-task`
result before commit, including `phase2_capture_commit`,
`reviewed_content_sha256`, and the pre-commit `dirty_paths`; validation
commands are evidence inside that report, not a substitute for the semantic
check. `phase2-check.json` is the single ignored-runtime `guru-phase2-check-4.0` artifact owned
by active `guru-check-task`. Official unchanged `trellis-check` is evidence-only;
the Skill owns scope-before-severity, adequacy, findings, full rerun, Docs SSOT
review, its AI Gate, and four typed exits. Coverage flags, worker output, or
script recorder/validator success cannot replace that loop. The preset
distributes the additive Guru package to shared/Codex/Cursor/Claude roots
without modifying any upstream-owned `trellis-check` file; current ownership
remains limited to schema 3.0's anchored Guru namespaces.
The Phase 2 public wrapper emits only `task_ref + phase2_commit_anchor` for
`passed`, retains that one checkpoint for Task Commit, and deletes the other
three exit checkpoints after output-schema validation. Task Commit rereads the
retained checkpoint, current reviewed-content identity, and commit parent, then
deletes the checkpoint after successful publication or recovery. Branch Review
consumes only the committed DTO and live Git.
Schema 4.0 keeps only the current commit anchor, reviewed-content identity, nine
adequacy dimensions, finding lifecycle, Docs SSOT
judgment, and actual validation evidence with direct Gate consumers. Routine
assignment, handoff, liveness, raw worker payload, and review rounds are not
persisted. Only a real unfinished-to-replacement event uses
`record-agent-recovery.sh` / `check-agent-recovery.sh` and the ignored
`.trellis/.runtime/guru-team/agent-recovery/<task-key>.json` checkpoint. That
checkpoint stores one minimal `unfinished`/`replacement` chain and never enters
the task tree, public DTO, commit, or archive.

Active `guru-review-branch` is the sole Phase 3.5 semantic owner. The global
workflow mandatory-invokes its
six-field public input (`profile`, `mode`, `task_ref`, `base_ref`,
`branch_review_commit`, `review_intent`) and consumes its four typed exits (`passed`,
`implementation_required`, `scope_confirmation_required`, `blocked`).
Reviewer lifecycle, finding qualification, Docs SSOT Gate, recovery checkpoint,
private artifacts and re-entry remain package-owned step-local contracts.

Its `passed` exit proceeds through the same entries to active
`guru-review-task-publication`: the caller first authors the two current
task-local publication content candidates, then invokes the active owner with
only its declared target-owned fields. The caller does not decide publication
sufficiency or readiness. The later `guru-finalize-task` consumer is active,
installed, and globally integrated; machine recovery routes are auto-consumed.
Branch Review and Publication each delete their own checkpoint after validating
their selected DTO. Neither downstream Skill reads or deletes upstream private
state.

`review-branch.sh` and `check-review-gate.sh` are package-owned deterministic
recorder/validator implementation details. They run only after the AI Review
Gate exists and cannot decide scope, finding qualification, sufficiency, pass,
or route. Platform entries and this installer do not duplicate those semantic
rules or expose private artifacts as public handoff data.
`finish-work.sh` rejects ordinary direct calls, so an ordinary continuation
cannot chain closeout, commit review metadata, push, or create a PR before the
explicit `guru-finish-work` entrypoint. That entry is
a thin live-workflow router: it runs Phase 3.6 through
`guru-review-task-publication`, then invokes `guru-finalize-task` only from
`ready`. The finalizer alone may call the private deterministic closeout engine
after its semantic review and exact plan confirmation. It automatically routes
verification, stale publication evidence, same-plan recovery, and reprepare;
every interruption resumes through the same semantic owner loop.
When the current plan requires extension verification, the finalizer consumes
only the checker-passed current owner result and task-local
`marketplace-verification.json` through retry, final projection, normal archive,
and active-completed recovery. It neither rewrites the owner artifact, changes
the scope-only Ledger, nor adds any public DTO field.
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

The finalizer's private preview is a side-effect-free readiness step. It
validates the gate, dirty state, AI-authored
`finish-summary-index.json`, and PR body/readiness, then prints the immutable
plan, digest, future archive mapping, exact transaction paths, and transitions
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
current publish inputs with repo/base/head/`branch_review_commit`/title/body
SHA-256/`draft=true`/reviewed source and `closeout_plan_digest`. Generated fallback
bodies are preview-only. Finish-work requires the direct task-local
`pr-body.md` with exact raw UTF-8 bytes and rejects every symlink component
from repo root through the task parent and final file, including alias,
dangling, and loop paths. Only those canonical task-local bytes are accepted.
`pr-readiness.json` is an ignored-runtime
owner checkpoint deleted by its public wrapper; `pr-body.md` remains an active
task input. Neither creates a pre-draft metadata commit, and schema 2.0 omits
both from the long-term archive tree. The script validates objective structure,
reviewed source presence, Docs SSOT section/key presence, and close/ref
semantics but does not replace AI release judgment.
`finish-summary.json` is created only by the normal current
`guru-team.finish-work` path; the preset installs no alternate summary command.

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
guru-create-task-workspace` chain. The following command is a current query-only
diagnostic and is not a workflow hop:

After task planning and a current `planning_artifacts:pass`, Phase 1 mandatory
invokes `guru-approve-task-plan`. Only `approved` enters
`phase-1-task-activation`; `revision_required` re-enters the Skill,
`clarify_scope` routes to the three-field workflow target
`guru-task-plan-clarify-scope-router`, and `blocked` stops at
`task-plan-approval-blocked`. The router establishes scope context and mandatory
invokes `guru-clarify-requirements:active_task_scope_change`; the caller AI
authors the complete semantic input from fresh live context. The preset
distributes this route's package and v2 deterministic runtime; it does not move
the step-local review loop into a platform overlay.

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --expected-resolution-sha256 <post-sync-resolution-sha256> \
  "<user request or issue URL>"
```

`prepare-task.sh --json` is a current query-only diagnostic. It may read
an explicit issue and search duplicates, but it does not create a GitHub issue,
worktree, branch, Trellis task, or task-local artifact. Freeform
requests without a source issue return `proposed_issue`, duplicate candidates,
selected-base facts, naming suggestions, and `naming_quality` in stdout JSON.
They return no authorization/handoff state, absolute workspace path, task-create
command, or task/runtime write. Before `gh auth status`, issue reads, or duplicate search,
`prepare-task` reuses the same strict resolution/sync core used by
`guru-sync-base`; `fetch_performed: false` or unequal decision/local/remote HEADs
cannot be `fresh: true`. A behind local base advances only on the selected-base
checkout via `git merge --ff-only`; wrong checkout, dirty state, missing refs,
fetch failure, divergence, resolution drift, or post-sync mismatch fail closed.
Prepare requires the preceding validator/guard post-sync resolution digest and
the same resolver inputs. It preserves explicit/config/config-candidate/remote-default provenance.
Resolution and result facts are stdout-only. Neither standalone nor workflow
mode creates resolution/result evidence files, leases, release commands, or
cleanup state. The current query consumes the current post-sync digest
and reruns the shared core before its reads. Workspace mutation freshness is
owned and revalidated by `guru-create-task-workspace`; identity/digest drift
requires a fresh Skill invocation.
Issue, branch, worktree, task, artifact, and runtime mutations belong
exclusively to active `guru-create-task-workspace`.

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

Only passed Gate plus confirmed active scope may mutate. Refusal stops before
the recorder/executor and produces no plan, result, or DTO. `reroute` and
`blocked` produce checker-validated zero-write `refresh_review` and `blocked`
results. Public result stdout omits the absolute
workspace path; the checker derives it from current config, reviewed slug, and
live Git facts, while local absolute mappings remain ignored runtime only.

In worktree mode, derive and validate task identity and the machine-local
worktree only from current `task.json`, the current checkout,
`.trellis/.runtime/guru-team/**`, `git worktree list`, and
`check-workspace-boundary.sh --task`. Before writing or validating
`planning-approval.json`, `phase2-check.json`, or `review-gate.json`, run:

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

The helper reports expected workspace, actual repo root, source checkout
status, task worktree status, and suspicious current-task artifacts or review
metadata in the source checkout. It is a deterministic validator/fact snapshot,
not stale judgment, cleanup, or patch migration. Editing tools without an
explicit `workdir` must use absolute paths under the task worktree confirmed by the
boundary helper. The boundary is a deterministic source/task fact layer; it
does not decide sub-agent progress, liveness, or stale state.

`create-task-workspace` reruns the shared core before GitHub or worktree/task mutation.
Each run keeps `preflight.base_freshness` in the current result only and requires
clean decision/local/remote equality. Planner evidence never replaces either
mutation-time guard, preventing new task branches from starting from a stale
local base.

The plan binds the initial checker-passed `post_sync_resolution_sha256`. The
executor runs the shared resolver/sync core once before the first confirmed
business mutation; confirmation remains only in the current dialogue and is
never passed to or persisted by runtime. A newly advanced remote may safely fast-forward the selected
base, but then returns `refresh_review` before issue/workspace/task/artifact or
runtime writes. An unchanged post-sync identity continues normally.

The active package uses ignored-runtime schemas `guru-task-workspace-plan-2.0`
and `guru-task-workspace-result-2.0` plus runtime commands
`record-task-workspace-plan`, `create-task-workspace`, and
`check-task-workspace-result`. It keeps workflow/standalone preconditions
identical, uses mutually exclusive issue/workspace confirmations, and exposes
only `created`, `refresh_review`, and `blocked` exits. A draft
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
bytes remain unchanged. The executor writes only the tracked task-local
`issue-scope-ledger.json` plus ignored runtime mappings. The real local A/B
fixture verifies both merge orders without a remote PR or concurrent process.

The installer manages `schemas/closeout-plan.schema.json` and
`schemas/finish-summary.schema.json`, writes top-level
`session_auto_commit: false` into `.trellis/config.yaml`, adds
`.trellis/workspace/` to `.gitignore`, and never creates or rewrites workspace
journal/index files. Shared start and installed Codex/Cursor SessionStart hooks
do not open, enumerate, read, count, or output workspace journals. Before
archive, closeout schema 2.0 recovery validates the untracked closeout plan, the active
locator, repo/base/head, current/remote HEAD, marketplace owner evidence when
applicable, and exact PR
identity. Prepare parses `.trellis/config.yaml` with the installed official
parser and supports only missing/empty `hooks.after_archive`; invalid or
non-empty hook configuration is rejected without execution. Immediately before
official move it also checks the live archive month, empty index, exact
untracked set, regular-file/mode contract, and transaction-parent blob bytes. A stale
schema 2.0 month remains active and is recoverable by rebuilding only the
still-untracked plan with a new dry-run digest; no plan/readiness/evidence commit,
history rewrite, or directory migration is used. After the official move but before the exact archive commit exists,
schema 2.0 first completes idempotent compact-archive pruning, then requires the exact retained
working-tree layout, dirty/staged paths, blob continuity, and official `task.json`
delta. The current retained set contains exactly 7 durable files and conditionally
retains marketplace verification as the eighth. Publication readiness and the Finalizer
gate remain ignored runtime and do not enter the archive;
intake snapshots, assignments, commit plans, raw review rounds and rollups,
PR preparation, and other reconstructible
checkpoints are omitted. Non-2.0 plans and absent or mismatched commits fail
closed. Once current `HEAD` is the exact
planned archive commit, both normal and plan-only archived reentry load the plan
from that commit blob; the committed plan blob and Git parent/path/tree/blob
facts are deterministic recovery inputs, not semantic or workflow authority, so missing or tampered archived working-tree files do not
block the exact push, remote title/body check, HEAD alignment, or
draft-to-ready. A plan-only archived directory is resolvable only by the canonical
`guru-finish-work` route, and ordinary task commands still require `task.json`.
The real-PR final summary's
deterministic bytes/digest participate
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
The plan-only path reads the committed plan from the current commit blob and
runs a dedicated fail-closed boundary before GitHub or fast-path actions. Git
toplevel, configured/effective repository, current head branch, available base
ref, current HEAD transaction, expected digest, task identity, and
active/archive locators must all match. Missing context is never an
unconditional boundary bypass; ordinary task discovery and commands retain
their `task.json` requirement, while worktree boundaries derive from current
task, ignored runtime mapping, current checkout, and live Git facts.
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

Official upstream-owned implement/check agents consume that plan during Phase 2
under the active Guru workflow. The preset does not replace their files. The
implementation agent reports the outcome and changed paths once. The Phase 2
semantic owner uses that ephemeral result plus live repository facts directly
and records only its compact final Docs SSOT, validation, semantic, and route
result in ignored runtime; no independent or embedded handoff is created. The
Phase 2 check agent then verifies durable
docs, task artifacts, code/schema/config/deploy/test, and validation/test
coverage against the same strategy. `delta_first` must merge durable docs
before final Phase 2 check; `ssot_first` uses revised durable docs as primary
input; `bootstrap_or_repair_docs` must complete the minimum repair or name a
bounded follow-up and PR limitation; `no_docs_update_needed` must still have a
concrete reason after the final diff is reviewed.


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 时，Finalizer 在 reviewed content push 后调用 `guru-verify-extension-installation` 生成并校验 task-local `marketplace-verification.json`；`issue-scope-ledger.json` bytes 全程保持不变。Closeout schema 2.0 不创建独立的 plan/readiness/evidence commit；passed artifact 与 remote HEAD 校验完成后才允许绑定 draft PR，并最终随单次 archive metadata transaction 提交。缺失、重复、pending、失败、内容不一致、HEAD 不匹配或 stale 均阻止创建 PR；human reason 不参与 machine identity，该门禁不创建 tag，AI 仍负责 close scope 与 PR readiness 判断。

## Eval 安装与升级清单

Preset 管理 eval schemas、`discover-skill-evals.sh`、`run-skill-evals.sh`、
shared/Codex/Claude/Cursor descriptor、可执行 wrapper、preset-managed shared native runtime，
以及 package-local `evals/**` 的
installed/selected-platform byte 与 executable mode。升级后重新 apply preset，
运行 source/installed eval smoke、platform byte/mode、dogfood drift 和递归零
`.new`/`.bak` 检查。Adapter wrapper 必须从 descriptor 路径执行；shared 从 adapter root
解析 managed executor，Codex/Claude/Cursor 从 `PATH` 解析 documented native command，
installer 不写本机 executable override。普通 Skill invocation
不加载这些 eval assets。Preset 同时管理 `guru-team-skill-eval-native-trace-1.0`
schema、adapter response 与 shared runtime；native CLI 只有通过 repo 外 trace helper
读取 public-only projection 的 exact Skill、调用 exact wrapper，且 receipt 绑定最小 request、
projection、Skill/wrapper digest 与 output 时，trace assertion 才有效。Canonical corpus/private
runtime 留在 native execution 外；四平台 projection 内对应 raw read 必须真实失败。
