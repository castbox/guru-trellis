# #117 BR-117-F10 Implementation Complete

## Files Modified

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - executor 向 throwaway verifier 传递显式 work root，并只读取真实安装目标
    `<work>/project`；
  - 从 checked-out canonical source、installed extension manifest 与平台
    destination 构建 231 项 deterministic expected asset set；
  - 记录 stable command ids、installed asset expectations/digests/category
    completeness，以及每个 capability 的 `command_refs` / `asset_paths`；
  - `verified` 对 missing、duplicate、unexpected、digest mismatch、manifest /
    platform relation error、unknown reference 与不完整 capability evidence
    fail closed。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - 新增 231-asset inventory 正向与 mismatch/missing/duplicate 负例；
  - 新增 executor 真实 installed target、capability evidence 与
    `verified` completeness gate 测试；
  - 抽取共用 source/install fixture helper，使 marketplace compatibility
    成功路径也生成真实 `<work>/project`，不以 command exit 0 冒充安装通过。
- `trellis/skills/guru-team/adapters/eval/native_adapter.py`
  - production eval fixture 使用 package 自身完整 execution example；
  - capability facts 使用 stable command/asset references，不再生成
    `evidence_step`。
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/`
  - 更新 `interface.json`、`references/contract.md`；
  - 更新 execution/private evidence schemas 与 examples；
  - package contract tests 增加 inventory/category/reference/private-schema
    闭合验证。
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - 由 canonical workflow runtime 同步的 dogfood 运行副本。
- `.trellis/guru-team/skills/adapters/eval/native_adapter.py`
  - 由 canonical native adapter 同步的 installed 副本。
- `.trellis/guru-team/skills/packages/guru-verify-extension-installation/`
  与 `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、
  `.cursor/skills/` 下的同名 package
  - 由 preset apply 同步为 byte-identical package copies。
- `.trellis/guru-team/extension.json`
  - 更新 runtime/adapter/package file digests 与 dirty source provenance；
  - 保持全平台、2322 managed files、zero conflict/sidecar/removal 的
    installed manifest。
- `.trellis/tasks/07-25-117-verify-extension-installation/implementation-handoff.md`
  - 本轮 F10 实现、Docs SSOT、验证和 `trellis-check` 交接。

并行生命周期产物 `agent-assignment.json`、`review.md`、
`review-gate.json`、`task-commit-plans/005.json`、
`reviews/007-f9-closure.md` 与 `reviews/008-final.md` 不属于本次实现，
保持其当前并行状态，不在本 handoff 中认领。

## Implementation Summary

1. Executor 仍从 exact remote ref 冻结并验证 checkout commit，但 throwaway
   command 现在接收显式临时 work root。安装证据只从该 command 生成的
   `<work>/project` 读取，不从 source checkout、dogfood worktree 或合成空目录读取。
2. Expected asset set 由四类 durable relation 构成：
   - `canonical_workflow`：1 个 active workflow；
   - `managed_manifest`：6 个 preset/runtime 与 4 个 schema；
   - `skill_manifest`：44 个 installed shared package assets；
   - `platform_manifest`：Agents/Codex/Claude/Cursor 共 176 个 package assets。
3. 每个 expectation 记录 category、optional platform、installed path、
   canonical source path、expected SHA-256 与 relation。Inventory 记录 expected
   set digest、五类 count/completeness、missing/duplicate/unexpected/mismatched
   paths、relation errors 和 final completeness。
4. Installed digest 从 throwaway target 实际 bytes 计算。Manifest path/source/hash、
   selected platform、canonical source existence 与 installed byte digest 任一不一致，
   execution 均不能成为 `passed`。
5. Command facts 使用 stable ids。Capability facts 通过 closed capability-to-command
   与 capability-to-category mapping 生成 `command_refs` 和 `asset_paths`；
   不再把共同的 last-command index 当作所有能力的充分证据。
6. Recorder/semantic shape gate 对 duplicate command/capability facts、unknown
   references、缺失 asset evidence 与 incomplete inventory fail closed。
   `verified` 额外要求每个 selected capability 同时具有 passed command 和
   installed asset evidence。
7. Public output DTO、四个 typed exits、consumer mapping、remote/ref/HEAD
   identity 与 semantic AI ownership 均未改变。Inventory、digests、capability
   evidence 继续是 owner-private state。

## Requirement And Design Carryover

- 完成 `BR-117-F10`：把真实 installed bytes、完整 expected set 与
  per-capability evidence 纳入 deterministic facts，并阻止 partial install /
  command-only success 进入 `verified`。
- 保留已审核 semantic/deterministic 边界：AI 仍独占 applicability、profile、
  adequacy、findings 与 route；runtime 只执行、记录、校验与投影。
- 保留 workflow/standalone 两个输入、四个最小 exits、task-local/session-only
  persistence、retry/stale、remote HEAD binding 和 redaction 合同。
- 保留 production eval 与 clean installation 双验收：eval fixture 使用完整事实，
  但不替代实际 install/update/reapply。
- 未实现或激活 #118 producer edge、#119 finish-family integration 或 #132
  legacy cleanup。
- 未扩展恶意篡改、并发竞态、TOCTOU、锁、原子写入或其它明确排除场景。

## Docs SSOT Handoff

- Strategy: `ssot_first`
- Durable docs/spec/contract sync:
  - canonical package `interface.json` 已把 executor objective 与 `verified`
    evidence 收敛为 command + complete installed inventory；
  - canonical package `references/contract.md` 已拥有 work-root、installed target、
    expected set、relation/category completeness、capability refs 与 fail-closed
    规则；
  - execution/private schemas 与 examples已成为 machine-readable durable
    evidence contract，并同步全部 installed/platform copies；
  - 实现前后核对 `skill-package-contract.md`、`companion-scripts.md`、
    `quality-guidelines.md`、preset `installer.md`、`upstream-ownership.md`
    与 `public-docs.md`。这些 higher-level owners 已要求 installed digests、
    per-capability facts、remote clean install、update/reapply、ownership 与
    production-eval independence，因此 F10 无需重复修改。
- Task delta merged to durable owners:
  - explicit throwaway work root 与 `<work>/project` installed evidence source；
  - 231-asset canonical/manifest/platform relation model；
  - category completeness、path/digest/relation failure matrix；
  - stable command ids 与 capability command/asset references；
  - `verified` 的 complete inventory 与 per-capability evidence preconditions。
- Task-history-only content:
  - F10 finding provenance、首次旧 compatibility fixture failure与修复过程；
  - Claude inherited environment 401 的诊断/clean-env rerun；
  - preset backup recovery、throwaway temporary locators 和本 handoff 的命令证据。
- No-update reason / current PR limitation:
  - workflow route、`.trellis/spec/`、README、overlay 和 ownership inventory
    无更新；F10 没有新增 public API、安装命令、route 或用户文档行为，相关
    higher-level durable docs 已完整覆盖；
  - exact pushed feature-ref clean installation 仍受当前分支未获 push 授权限制。
- Durable-doc implementation inputs:
  - package Interface/private state、companion executor/recorder/checker boundary；
  - installer manifest/ownership/update/reapply 与 zero-sidecar contract；
  - production eval/public-only projection 和 remote clean-install independence。
- Confirmed task-delta implementation inputs:
  - F10 要求的 installed target source、expected inventory、relation checks、
    capability evidence、partial/mismatch/duplicate fail-closed 场景。

## Verification Results

- Focused runtime after compatibility fixture repair:
  - `MarketplaceVerificationContractTest` targeted success path +
    `ExtensionVerificationRuntimeTest`: 28 passed。
- Full runtime:
  - `test_guru_team_trellis.py`: Ran 600，OK，13 skipped。
- Package/preset suites:
  - canonical verifier package: 9 passed；
  - installed verifier package: 9 passed；
  - all 12 canonical package contract files: 114 passed；
  - `test_skill_packages.py`: 175 passed；
  - preset/ownership Python suite: 54 passed。
- Production eval:
  - Shared source与 installed：各 7/7 passed；
  - Codex source与 installed：各 7/7 passed；
  - Claude source与 installed：外层移除 inherited
    `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_BASE_URL` 后各 7/7 passed；
  - Cursor source与 installed：各 7/7 `unsupported`，符合当前 capability contract；
  - Claude 初次 inherited-env run 的 7 个 case 均因 401 `execution_error`；
    fresh `claude auth status` 证明 first-party login current，clean-env rerun
    消除了该外部环境问题。
- Full local-source throwaway:
  - `verify-throwaway-install.sh` exit 0；
  - 覆盖 public marketplace discovery、current-worktree local workflow sample、
    initial apply、existing preview/switch、`trellis update --force`、workflow
    reselect、preset reapply、no-developer preservation、pre-146 recovery、
    ownership、installed eval 和 final zero-sidecar；
  - retained `/project` 的 F10 collector：expected=231、observed=231、
    matched=231、`complete=true`；
  - category counts：workflow 1、preset 6、schema 4、skill 44、platform 176；
  - missing/duplicate/unexpected/mismatched paths 与 relation errors 全为空。
- Distribution/install checks:
  - source/installed Skill validation passed，closure 12 active Skills /
    46 exits / 27 targets；
  - installed manifest 2322 managed files，0 conflict、0 sidecar、0 removal；
  - upstream ownership 43-entry frozen inventory passed；
  - dogfood overlay drift passed；
  - canonical/installed/shared/Codex/Claude/Cursor package `diff -qr` passed；
  - canonical/installed runtime、native adapter equality passed。
- Static checks:
  - changed JSON parse、Bash syntax、Python compile passed；
  - recursive non-fixture `.new`/`.bak` scan为零；
  - task validation与 `git diff --check` passed。
- TypeCheck:
  - skipped；仓库没有该 Python runtime 的独立静态 typecheck owner，由 full
    unittest、schema/package validators 与 Python compile 承接。

## Handoff For `trellis-check`

- Focus areas:
  - 复核 expected-set 来源只包含 checked-out canonical source 与 installed
    extension manifest，installed digest只从 throwaway `<work>/project` 读取；
  - 复核 1/6/4/44/176 五类资产、四种 relation、duplicate/path/digest/platform
    负例与 final completeness 双向一致；
  - 复核每个 capability 的 command refs 与 asset category mapping，确认不存在
    command-only 或 asset-only `verified`；
  - 复核 recorder/checker、private schema、examples 与 package contract 的
    machine/semantic/public边界，确认 public DTO和 consumer无扩张；
  - 复核 marketplace compatibility wrapper 继续调用唯一 executor，且测试 fixture
    不再用 exit 0 绕过 installed evidence；
  - 复核 canonical/runtime/shared/Codex/Claude/Cursor byte identity、extension
    manifest digests、full throwaway final target与 zero-sidecar终态；
  - 执行完整 Docs SSOT reconciliation，确认 F10 task delta 已全部进入 package
    durable contract/schema，higher-level no-update reason成立。
- Validations intentionally deferred to check:
  - Phase 2 semantic review、finding classification与 `phase2-check.json`
    recorder/validator；
  - 独立复核完整 diff 与当前并行 task metadata，不复用本实现 agent判断。
- Intentionally deferred beyond implementation/check:
  - exact post-push remote-ref verification。当前未获 commit/push授权，local-source
    throwaway不能冒充 exact pushed feature-ref；
  - Branch Review Gate、task commit、push、PR readiness、Issue closure。
- Remaining risks:
  - exact remote-ref gate仍需在后续已授权 push 后绑定实际 remote HEAD；
  - 当前 extension manifest记录 dirty source provenance，这是未提交实现阶段的
    真实状态；后续 commit/apply/review应重新绑定最终 commit；
  - Claude native eval依赖调用进程环境。当前 clean first-party环境已全量通过，
    后续 check若继承冲突的 provider变量，应先区分环境配置与实现回归。
