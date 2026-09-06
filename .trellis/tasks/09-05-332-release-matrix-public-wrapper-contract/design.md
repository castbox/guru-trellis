# Technical Design

## 1. Problem Statement

当前 Release Gate 暴露的不是单一 verifier 文件错误，而是两类相互放大的合同漂移：

1. #330 的优化事务被发布成新的 facade wrapper/command，原 `invoke.sh` 被降级为 legacy；
2. compatibility matrix `_assert_platform_projection()`、throwaway
   `verify_package_projections()` / `verify_closeout_package_boundaries()` 与
   `runtime/validate.py` 又把 `invoke.sh` 文件名硬编码为全局规则，而每个 Skill 的 wrapper path
   由自身 Interface 独立声明。

只修第一类会继续误拒绝 `guru-restore-archived-task`；只修第二类会掩盖 #330 四阶段的公共 API
退役错误。目标设计必须同时恢复既有入口 identity，并让 generic consumer 只相信 Interface。

## 2. Architectural Invariants

1. `interface.json.public_contracts.invocation` 是每个 Skill 唯一 public invocation authority；它绑定
   wrapper path、input profile、example argv、stdout/error contract。
2. 既有公共入口 identity 是兼容合同。#330 四阶段继续使用原 `scripts/invoke.sh` 和原 command id；
   优化发生在其 package runtime 内部。
3. 一个 Skill 对平台只投影一个 public wrapper。其它 record/check/execute/preview/helper wrapper 全部
   package-private，不进入 Shared/Codex/Claude/Cursor。
4. Wrapper 只定位 managed dispatcher、绑定一个固定 command id 并透传 argv；业务判断、校验或事务
   实现在 package-local Python runtime，不进入 shell 或共享目录。
5. Happy Path 与 compatibility path 可共享 owner/runtime primitives，但正常调用只走其需要的分支，
   不串行执行两套检查。
6. 同一 invocation、同一 authority、mutation 前无状态变化的事实可复用；mutation boundary 和
   post-mutation proof 仍执行必要重读。

## 3. Target Public Entry Model

四阶段最终 public graph：

| Skill | Stable public wrapper | Stable command id | Happy Path input | Compatibility input |
| --- | --- | --- | --- | --- |
| `guru-create-task-commit` | `scripts/invoke.sh` | `invoke-guru-create-task-commit` | prepared candidate locator | existing call-local invocation envelope |
| `guru-review-task-publication` | `scripts/invoke.sh` | `invoke-guru-review-task-publication` | public input + AI semantic result | public input + existing owner result |
| `guru-finalize-task` | `scripts/invoke.sh` | `invoke-guru-finalize-task` | public input + AI review + confirmed preview identity | public input + existing owner result |
| `guru-merge-task-pr` | `scripts/invoke.sh` | `invoke-task-pr-merge` | public input + AI review/current gate | public input + existing checked gate |

`commands.json` 为每个 stable command 声明 Happy Path 与兼容参数的 closed union/conflicts；
`runtime/invoke.py` 根据互斥参数形态选择一次执行模式。正常模式直接调用 PR #341 已实现的
invocation-local transaction 能力；兼容模式只服务实际旧 caller。

不保留以下 public command/wrapper：

- `invoke-guru-create-task-commit-happy-path-v1` / `invoke-happy-path-v1.sh`；
- `review-task-publication` / `review-task-publication.sh`；
- `finalize-task-happy-path` / `finalize-task-happy-path.sh`；
- `complete-task-pr-merge` / `complete-task-pr-merge.sh`。

仍被 stable command 直接消费的 transaction functions 保留在现有 package-local runtime；只服务第二
command 分派的 adapter branch 删除，并由 tests 证明没有剩余 consumer。任何 package-private runtime
均不得迁入共享 `.trellis/guru-team/scripts/bash/**`。

## 4. Stage-Local Execution

### 4.1 Commit

`prepare-task-commit.sh` 仍是唯一 mutation 前 prepare，负责 task/Phase 2/Git binding、AI path
classification 输入校验、message canonicalization 和 candidate creation。确认后：

```text
scripts/invoke.sh --candidate-artifact <locator>
  -> one mutation-boundary candidate validation
  -> isolated index/hooks/commit/ref update/postconditions
  -> exact stdout-loss recovery
  -> typed exit projection and cleanup
```

旧 `--invocation -` 调用保留为同一 command 的 compatibility branch，不在 candidate Happy Path 前
执行。`check-task-commit-plan.sh` 与 `create-task-commit.sh` 继续 package-private。

### 4.2 Publication

AI 先完成 current Publication semantic review。正常调用：

```text
scripts/invoke.sh --input <public> --semantic-result <review>
  -> one invocation-local snapshot
  -> record already-made semantic result
  -> objective check
  -> typed projection and checkpoint retirement
```

旧 `--owner-result` 形态只在 compatibility branch 使用。Runtime 不选择 finding、route、Issue
disposition 或 PR adequacy。

### 4.3 Finalizer

`preview-finalization.sh` 保持 read-only action preview。确认后原 `invoke.sh` 直接执行当前事务循环：

```text
validate confirmed preview identity
  -> execute current checked transition
  -> automatically continue only mapped same-plan recovery/reprepare
  -> stop on scope/authority/payload/side-effect-set change
  -> project one stable exit
```

旧 `--owner-result` 形态保留为 compatibility branch；正常 `--review-input` 形态不先创建并检查一套
legacy gate。现有独立 push、PR、archive/Ready 确认约束继续由 repository-private release contract
叠加，不因入口合并而复用授权。

### 4.4 Merge

Pending checks 仍只使用一个 `watch-task-pr-checks`。通过 semantic gate 和 exact merge 确认后：

```text
scripts/invoke.sh --input <public> --review-input <review>
  -> one pre-merge full snapshot
  -> checked expected-head merge
  -> one post-merge full snapshot
  -> output-loss recovery
  -> terminal/re-entry projection and cleanup
```

旧 gate-only 形态保留为 compatibility branch。`merged|merge_blocked|phase2_reentry_required|
closure_mismatch` 投影后当前 Merge Skill 立即停止。

## 5. Generic Wrapper Consumers

### 5.1 Projection Source Of Truth

Installer 的 `skill_platform_public_files()` 和 installed runtime `public_files()` 已按 Interface 选择
wrapper，继续作为正确基线。后续消费者统一复用相同规则：

```text
public_wrapper = interface.public_contracts.invocation.wrapper
declared_validator = validator whose command == public_wrapper
platform projection = public contract assets + exactly public_wrapper
private wrappers = all other validator commands
```

缺失、多个匹配、unsafe path、非 regular/executable、bytes/mode drift 或 private wrapper 泄漏均
fail closed。

### 5.2 Matrix And Throwaway

- `_assert_platform_projection()` 从 installed package Interface 读取 wrapper，比较 shared/selected
  platform 与 installed package 的 exact bytes/mode，并拒绝其它 scripts。
- `verify_package_projections()` 与 `verify_closeout_package_boundaries()` 使用同一声明式选择，不再
  写死 `scripts/invoke.sh`。
- Publication/closeout 专属 smoke 只在该 package 的稳定入口确实为 `invoke.sh` 时使用该路径；通用
  helper 不继承该假设。

### 5.3 Runtime And Eval

- `runtime/validate.py` 对 `public_contracts.invocation.wrapper` 对应 validator 执行 platform managed
  launcher fallback 校验；其它 package-private wrapper 只要求 canonical/installed launcher。
- Generic eval projection、trace 与 exact comparison 使用 request/interface 中的 wrapper path。
- Qualification Codex sandbox helper 只服务 `guru-qualify-*` 且其 Interface 固定为 `invoke.sh`；保留
  profile-local实现，并增加测试证明它不会处理任意 Skill wrapper。
- `guru-restore-archived-task` 作为不同 wrapper path 的 positive fixture，覆盖 source、installed、
  Shared/Codex/Claude/Cursor projection 与 actual invocation。

## 6. Distribution And Deletion

Canonical 修改完成后，通过 preset apply 生成 installed/dogfood/platform projection与 extension
manifest。删除旧 managed wrapper 时必须进入 installer removal inventory；不得手工只删某一 projection。

`trellis/presets/guru-team/README.md` 删除不存在的共享 facade path，并分别说明：

- shared companion wrappers 的真实 inventory；
- package-local validator/helper wrappers；
- Interface-declared single platform public wrapper。

`.new`、`.bak`、unexpected sidecar、mode 或 ownership drift 任一非零均阻断完成。

## 7. Compatibility And Migration

- #330 四阶段原 wrapper path/command id 从未改变；current main 中新增但尚未进入正式
  `v0.6.15-guru.5` 的 facade ids 在本 release preparation 内删除，不形成第二长期 public API。
- 旧 stable argument shape 由原 command 的 compatibility branch 承接；其 schema/example/tests 保留到
  现有 consumer 明确退役，不在正常路径读取。
- 新 Happy Path argument shape 写入原 Interface invocation example 和 `SKILL.md`；旧 caller 不需要改变
  executable path。
- `guru-restore-archived-task` 保持自身原 wrapper/command，不被 #330 兼容迁移波及。

## 8. RDT And Architecture Plan

- Strategy: `ssot_first`。
- Durable workflow contracts：修订 `.trellis/spec/workflow/{skill-package-contract,companion-scripts,
  workflow-contract,data-contracts,quality-guidelines}.md` 及 preset copies，删除“新 facade 替代旧入口”
  表述，保留事务与 operation budget 语义。
- Source authority：`current-main-0.6.5-guru.44` 保持 active 且内容不被本 implementation slice 原地
  改写；existing #332 release contribution 保留其 `.43 -> .44` promotion history。
- Task-owned RDT contribution：新增
  `docs/requirements-design-test-contributions/332-release-wrapper-entry-correction/`，承接 original-entry
  continuity、Interface-driven generic wrapper、non-`invoke.sh` regression、23 / 97 / 77 graph 与
  Release Gate freshness。
- Task-owned Architecture contribution：新增
  `docs/architecture/contributions/332-release-wrapper-entry-correction.md`，Planning path 为
  `dedicated_refactor_slice`，命中 `concept-semantic-completeness`、`cohesion-change-isolation`、
  `minimum-necessary-complexity`、`debt-one-way-convergence`，并绑定 expected `.44`。
- 初始 implementation/Phase 2/task commit/independent Branch Review 只写 task-owned contributions；通过后
  serialized RDT/Architecture owner 生成 successor `.45`，在 `.45` 中修订 `DES-019`、distribution
  evidence、#330 RDT 语义和 live-derived 23 Skills / 97 exits / 77 commands。promotion-created diff 再次
  进入 fresh Phase 2、task commit 与独立完整 Branch Review。
- ADR：当前不创建。仅当 implementation discovery 证明现有 constitution/change contract 无法承接新的
  长期 architecture decision 时返回 Planning 重审。
- Public docs：README 只陈述真实安装/调用面；task planning docs 不成为长期 SSOT。

## 9. Validation Strategy

1. Contract tests：四阶段 stable wrapper/command id、互斥 Happy/compat args、无第二 public wrapper。
2. Behavior equivalence：相同 fixture 比较旧 stable invocation shape 与新 Happy shape 的 typed exit、DTO、
   blocker、mutation、recovery、lifecycle；不比较或保留错误的新 wrapper identity。
3. Operation budget：Happy mode command/read ceilings继续满足 #330，且测试断言 compatibility branch 未被
   Happy mode触发。
4. Generic wrapper variation：`restore-archived-task.sh` 通过 installer、runtime validator、matrix、throwaway、
   eval trace 和 platform leak checks。
5. Distribution：source/installed package validators、all-platform reapply、ownership、dogfood drift、
   managed removals、recursive sidecar zero。
6. Authority promotion：task-owned contributions 通过初始 committed review 后，以 expected `.44` 串行
   生成 `.45`，并对 promotion-created diff 重跑 Phase 2、commit 与 full-diff Branch Review。
7. Release proof：preparation PR merge 后在新的 detached clean exact candidate 上从零执行 #332 完整
   Release Gate；当前 Phase 2 不运行旧 candidate gate。

## 10. Risk And Rollback

- 主要风险是把兼容参数 overload 变成常态双路径。通过 mutually-exclusive argument schema、mode-specific
  operation counters 和“Happy mode 不触发 compatibility primitive”断言控制。
- 第二风险是删除 wrapper 时遗漏 managed projection。只修改 canonical，通过 installer removals 和
  manifest parity 验证，不手工修补平台副本。
- 第三风险是把 qualification-only `invoke.sh` 假设错误泛化。通过 generic/non-generic 分层测试控制。
- 任一 package transaction behavior、public DTO、mutation count、installed compatibility 或 Architecture
  project check 失败时，不进入 Publication/Release；保留当前 branch 供修订，不修改历史 tag/Release。
