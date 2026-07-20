# #144 最小 typed handoff I/O 实现交接

## 0. Round 1 Branch Review finding 修复交接

状态：`Round 1 Finding Fix Complete`

本轮以全新的实现代理身份修复 `reviews/round-01-final-finding.md` 中四项 current-scope
P2；未修改或删除 `review.md`、`reviews/round-01-final-finding.md`、`review-gate.json`、
`agent-assignment.json` 和 `task-commit-plans/001.json`。未执行 Phase 2 recorder、commit、
push、PR、Branch Review recorder 或 finish-work。修复后必须重新执行完整 Phase 2 语义检查，
再创建 finding-fix commit 和新一轮独立 Branch Review。

### 四项 finding 修复

1. Skill consumer ownership：`consumer.kind=skill` 现在只接受
   `contract.kind=skill_input`，并要求被引用 `interface.json` 的 `id` 与
   `consumer.id` 完全一致。Producer-owned `json_schema` 或错误 target interface 均阻断。
2. Projection totality：所有非 `direct` projection 现在要求 consumer required field
   来自 producer required field，并对每个 mapping 做保守静态全域兼容证明。支持 exact
   property schema、有限 `const`/`enum` normalize、非空 scalar string、positive integer，
   以及带显式 ASCII non-blank pattern 的 trim；无法证明时即使 example 通过也拒绝激活。
   Representative repeat output 因此显式声明 trim 后仍非空的 pattern。
3. Public/private disjointness：public output 与 private artifact 的 schema id 集合和 path
   集合分别求交；复用相同 id/不同 path 或相同 path/不同 id 都会得到
   `[public_private_overlap]`。
4. Dispatcher-only wrapper：interface 1.3 invocation wrapper 必须绑定恰好一个 declared
   validator，并以完整 bytes 匹配支持的 dispatcher-only template。仅在注释/死代码中出现
   `run-skill-command.sh`，或 wrapper 自行 `printf` typed DTO，均不能通过。

### 正常 authoring 负例

- Skill consumer 改绑 producer output schema，或指向错误 Skill interface id。
- 从 producer `required` 移除 scalar consumer 必填来源字段。
- 去掉 trim non-blank proof 后让合法 producer example 为单个空格，normalize 后变为空串。
- public/private 分别复用 schema id 或 schema path。
- wrapper 只在注释写 dispatcher 名并本地输出合法 DTO。

### 验证结果

- Targeted 四 finding + representative happy path：5/5 passed。
- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'`：
  99/99 passed。
- Preset installer tests：39/39 passed；ownership tests：6/6 passed。
- Source/installed `check-skill-packages`、legacy discovery、dogfood drift、upstream
  ownership、canonical/installed byte equality、Python compile、Bash syntax、JSON parse、
  task validation、workspace boundary、`git diff --check`：全部通过。
- Dogfood apply 首轮只产生 runtime 的一个 known-managed `.bak`；核验新 installed bytes
  与 canonical SHA-256 相同后删除，幂等 reapply 为零 `.new`/`.bak`、零 conflict/removal。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh`：通过 clean init、
  workflow preview/switch、preset install、`trellis update`、reapply、mixed fixture smoke、
  source/installed/ownership 与最终零 sidecar；最终为 384 managed files、9 legacy、
  0 production minimal。

### Docs SSOT 与范围

- Durable Docs SSOT 已同步：`.trellis/spec/workflow/skill-package-contract.md`、
  `companion-scripts.md`、`quality-guidelines.md`、`docs/requirements/requirement-main.md`、
  `docs/requirements/guru-team-trellis-flow.md` 及三份 public README。
- Durable contract 现在明确 target-owned Skill input、非 direct projection 全域证明、
  schema id/path 分别互斥和 complete-byte dispatcher-only wrapper 规则。
- Task-history-only：Round 1 raw finding、review rollup/gate、agent liveness/assignment、旧
  commit plan、逐次命令原始输出、临时 throwaway 路径和本轮交接；这些不进入 durable
  runtime contract。
- 九个 production Skills 继续为 interface 1.2 + `legacy`，没有 payload/interface/route
  迁移；mixed 1.3 fixture 仍为 test-only。#145/#146 继续是 follow-up，不由 #144 关闭。
- 未修改 frozen overlay、CI/CD、container、K8s、DB migration 或 Makefile；无部署/数据库
  迁移影响，未引入 hostile-input/并发/TOCTOU/锁/原子写入等排除范围。
- Public marketplace sample 只证明公开 marketplace 通路和本地 unpublished canonical
  bytes；它不是当前 feature ref 的 immutable remote evidence。Exact feature-ref marketplace
  verification 仍须在 reviewed branch push 后由 finish/publish gate 补齐。

### 本轮 implementation dirty paths

- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/tasks/07-20-144-minimal-typed-handoff-io/implementation-handoff.md`
- `README.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `docs/requirements/requirement-main.md`
- `trellis/presets/guru-team/README.md`
- `trellis/skills/guru-team/tests/fixtures/representative-active/packages/guru-example-action/schemas/action-repeat-output.schema.json`
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/workflows/guru-team/README.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`

Branch Review metadata 的既有 dirty paths 由主会话继续管理，不属于本轮 implementation
dirty list，也未被本代理改写。

## 1. 实现状态

`Implementation Complete`

Issue #144 的批准实现范围已经完成，等待独立 `trellis-check` 执行 Phase 2 语义复核。
本代理未执行 `trellis-check`，未写 `phase2-check.json`，也未执行 commit、push、PR、
Branch Review 或 finish-work。

Expected task workspace 与 actual repository root 仍一致；source checkout 保持 clean。
Planning approval 在实现收敛前复核为 `approved`，
`facts_sha256=184bfeebbc7634420fc741975a3b29d538a7e535674376ecb81ffa97081daf3f`。

## 2. Changed files

### Durable SSOT 与公开文档

- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/workflow/index.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `docs/requirements/README.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

### Canonical schema、runtime、fixture、installer 与 tests

- `trellis/guru-team-extension.json`
- `trellis/skills/guru-team/registry.json`
- `trellis/skills/guru-team/schemas/skill-registry.schema.json`
- `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh`
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/skills/guru-team/tests/fixtures/representative-active/**`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`

Representative fixture 中旧的单一 `fixture-result` example/schema/validator 被 1.2 legacy、
1.3 semantic structured-input 和 1.3 deterministic scalar-CLI 三包混合 fixture 取代。

### Preset 生成的 dogfood copies

- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/skills/registry.json`
- `.trellis/guru-team/skills/schemas/skill-registry.schema.json`
- `.trellis/guru-team/skills/schemas/skill-interface-1.3.schema.json`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/scripts/bash/discover-skill-contract.sh`

九个 production Skill package 及 `.agents`、`.codex`、`.claude`、`.cursor` 平台副本的
payload bytes 未修改；preset apply 只同步本任务新增或升级的受管基础设施。

### Task-local evidence

- `.trellis/tasks/07-20-144-minimal-typed-handoff-io/implementation-handoff.md`

## 3. 需求与设计承接

- R1-R2：保留 interface 1.2 文件、id、body digest 与现有 package payload；新增独立
  interface 1.3，registry schema 升级为 1.1。九个 production active entry 全部显式为
  `guru-team-skill-interface-1.2 + legacy`，runtime 按 registry exact version/state 分派。
- R3-R7：1.3 使用 closed `public_contracts`，分别声明 structured/scalar input、exact
  invocation、per-exit output、consumer input、projection 与 private artifact。Structured
  aggregate 要求 exact ordered `$ref`、共享且 required 的 discriminator 及匹配 `const`；
  scalar CLI 要求 exact argument order/flag/type、ordered binding 与相同 argv。
- Zero-payload stop 保留 routing identity `exit_id`，response payload 为零；只允许空
  `select` projection。非 zero-payload consumer 禁止空 `select`，zero-payload output 禁止
  额外字段或非空 mapping。
- R4-R6：representative invocation 真实执行 wrapper，stdout 必须是单一 declared exit，
  再按 per-exit schema 和实际 consumer projection 复验。Projection 闭集为 `direct`、
  `select`、`rename`、`normalize`，并验证非零 output 的 exact `exit_id const`、direct
  producer/consumer schema equality、mapping target 唯一性、target value type、private-field
  与 runtime-source 隔离。
- R7：private artifact 只含 `runtime_checkpoint` / `gate_evidence`，fixture 覆盖
  `stdout_only_pre_task`、`task_local_tracked` 与 `ignored_runtime` 三种 persistence。
- R8-R9：extension public API 新增 `discover-skill-contract`，发布 1.2/1.3 supported ids、
  current 1.3、兼容 scalar 1.2、registry 1.1、legacy allowlist 与 exact production
  inventories。当前九个 production package 全部 legacy，因此三个 public/private schema
  inventory 为空；fixture extension 使用自己的非空 test-only inventories。
- R10-R11：mixed fixture 同时包含一个 1.2 legacy package、一个 1.3 semantic package 与
  一个 1.3 deterministic scalar package；覆盖 Skill/workflow/stop consumer、self-reentry、
  四种 projection、不同 exit、stable error 和 fail-closed negative matrix。Fixture ids 未
  进入 production registry、extension inventory、安装平台或 mandatory workflow route。
- R12：canonical、installer、dogfood、selected-platform、clean throwaway、update/reapply
  均已承接；frozen upstream-owned overlays 和 43 条 ownership baseline 未修改。
- P15 范围边界保持：没有迁移九个 production Skill；#145/#146 仍为 follow-up；没有把
  semantic judgment 写入 Python/shell，也没有加入 hostile-input、锁、TOCTOU、压力、
  fault injection、crash consistency 或跨 OS 原子性加固。

## 4. AC1-AC15 实现证据

| AC | 实现边界内证据 |
| --- | --- |
| AC1 | 1.2 schema SHA-256 固定为 `33e5daf1362d6580027254fc15d63824cb4688c9e97e896489e9e817b034841e`；1.2 schema 与九个 canonical production package 对 HEAD 无 diff。 |
| AC2 | 独立 1.3 closed schema 覆盖 input、invocation、outputs、consumer inputs、projections、self-reentry、private artifacts；SHA-256 为 `fc808c8600f0e187b404fc27e7f07a0bfd252526af07545acbe55ceebfb3892e`。 |
| AC3 | Registry 1.1 要求 active exact schema/state；live query 确认九项均为 1.2 + `legacy`。 |
| AC4 | 95-test suite 与 mixed fixture 同时报告一个 legacy、两个 `minimal_handoff` package。 |
| AC5 | Fixture 覆盖 structured discriminator/`oneOf`、scalar CLI、Skill/workflow/stop、self-reentry 及 `direct/select/rename/normalize`。 |
| AC6 | 每个 exit 有独立 closed schema、example 和 consumer-use projection；missing/non-constant identity、unconsumed、zero-payload extra-field 与 narrower direct consumer negatives 均被拒绝。 |
| AC7 | Validator 实际执行 action 与 sync wrappers，复验单一 stdout DTO、对应 exit schema 及实际 consumer projection。 |
| AC8 | Invocation/discovery errors 固定为 `code`、`field_path`、`remediation`；unknown skill、version/state mismatch、missing asset 与 installed drift 使用可区分 stable codes。 |
| AC9 | Duplicate target、private-field projection、unknown operation、runtime-source import/read 与 actual projection mismatch 均 fail closed。 |
| AC10 | Interface、fixture extension、production extension、installed manifest、README 与 durable spec 对 public/private inventories 和 persistence 一致。 |
| AC11 | Discovery command 已进入 extension API、canonical/installed executable wrapper、managed inventory、source/installed validator 与 throwaway smoke。 |
| AC12 | Legacy allowlist、reserved/planned package prohibition、production/fixture inventory isolation 均有 validator 与 negative tests。 |
| AC13 | Canonical/installed runtime、registry、registry schema、1.3 schema、discovery wrapper byte-equal；九包与四个平台副本 byte-equal；wrapper/runtime 为 executable、schema 为 non-executable。 |
| AC14 | Throwaway clean init、workflow preview/switch、update、preset reapply、source/installed/ownership checks通过，repository 与 throwaway 最终均无 `.new/.bak`。 |
| AC15 | 三份 README 的 discovery、source/installed 与 throwaway 命令已由 tests/throwaway 执行；current-branch remote marketplace 的未推送限制单独记录，不伪报为 exact-ref pass。 |

上述是 implementation handoff evidence，不代替 `trellis-check` 的独立 semantic pass。

## 5. Docs SSOT Reconciliation

- Docs state：`complete_docs`。
- Strategy：`ssot_first`。
- Durable implementation inputs：三份 `docs/requirements/**`、五份
  `.trellis/spec/workflow/**`、root/workflow/preset 三份 public README。
- Task delta 已合并到 durable docs：1.2/1.3 共存、registry state、caller-owned input、
  exact invocation、per-exit output、consumer/projection、zero-payload、public/private
  inventories、discovery、#145/#146 migration boundary 与完整安装/update 门禁。
- Durable docs sync：完成。实现先以修订后的 durable contract 为主输入，再同步
  schema/runtime/fixture/registry/extension/installer/generated copies/tests；最终命令证据与
  durable docs 一致。
- Task-delta implementation inputs：批准的 `prd.md`、`design.md`、`implement.md` 继续提供
  #144 scope、P1-P15 provenance、R1-R12/AC1-AC15 映射和执行边界；其中可复用合同已回写
  durable docs，未把 task journal 当成运行时 SSOT。
- Task-history-only：Phase 0 临时 evidence、planning confirmation digest、agent assignment/
  liveness、逐轮 finding、首次 preset apply 的两个 known-managed `.bak` 核对、默认
  exact-ref fail-closed 输出、命令原始日志、临时 throwaway 路径及本交接。它们不合并进
  durable docs。
- Middle-platform Knowledge Gate：不适用；本任务不涉及 go-guru、proto-guru、Unity、
  Flutter 或中台 SDK/framework contract。

## 6. 验证结果

- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'`：
  95 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：
  39 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`：
  6 tests passed。
- `apply.sh --repo . --all-platforms`：最终幂等 apply `status=ok`；source/installed
  validation passed，384 managed files，0 conflict、0 removal、0 sidecar。
- 首轮 managed upgrade 只生成 runtime 与 1.3 schema 两个预期 `.bak`；逐项确认新目标
  等于 canonical 后删除，第二次 apply 无 sidecar。当前 recursive `.new/.bak` 为 0。
- `check-skill-packages --mode source`：passed，9 legacy、0 production minimal。
- `check-skill-packages --mode installed`：passed，Claude/Codex/Cursor selected platforms，
  sidecar/conflict/removal 均为 0。
- Installed `guru-sync-base` discovery：`variant=legacy`，1.2 + `legacy`，migration 指向
  1.3 与 #145/#146。
- `check-dogfood-overlay-drift.sh`：passed。
- `check-upstream-ownership.sh --json`：passed，43 frozen/active overlays identity 未变，
  13 managed claims 全部已分类。
- Canonical/installed bytes、四个平台 package copies 与 executable modes：passed。
- Changed Bash `bash -n`、Python `py_compile`、JSON parse：passed。
- Workspace boundary、planning approval 与 `task.py validate`：final passed；task context 为
  10 条 implement entries、11 条 check entries。
- `git diff --check`：handoff 写入后 final passed；source checkout clean，当前 task 未生成
  `phase2-check.json`。
- `verify-throwaway-install.sh` 默认 exact-ref：按设计 exit 2，因为 feature branch 尚未
  commit/push，远端 marketplace 无法解析当前 dirty unpublished ref。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh`：exit 0；覆盖 clean
  init、public marketplace discovery、local unpublished workflow/preset sample、workflow
  preview/switch、初装、`trellis update`、preset reapply、mixed fixture invocation、
  source/installed/ownership/platform checks 与最终零 sidecar。

## 7. 开箱即用、升级与当前限制

- Canonical source 位于 `trellis/`，dogfood `.trellis/guru-team/` 只是 installer 生成副本；
  没有修改 Trellis upstream、全局 npm、`node_modules` 或 frozen overlay payload。
- Extension version 为 `0.6.5-guru.18`，target/tested Trellis CLI baseline 为 0.6.5。
  Throwaway 输出提示 npm latest 为 0.6.7；CLI baseline upgrade 不在 #144 范围。
- Clean init 与 `trellis update` 后 reapply 均通过，证明新 wrapper/schema/runtime/manifest
  可恢复，最终无 unresolved `.new/.bak`。
- Exact current-branch marketplace install 尚未验证：当前 implementer 无 commit/push
  authority，远端不存在可采样的 reviewed branch ref。Public `main` 只验证 marketplace
  通路，本 worktree canonical bytes 验证本次实现；分支 push 后必须由后续 immutable
  marketplace verification 补齐，不能把本轮 canary 记为 exact feature-ref pass。

## 8. 安全与部署判断

- Stable errors 只包含 code、field path 与 remediation；未写入 token、secret、private
  key、`.env`、数据库 URL、签名 URL或用户数据。
- 本任务不新增服务、API、worker、queue、schedule、数据库 migration、容器、Kubernetes、
  Dockerfile、Compose、Kustomize、Makefile 或 CI/CD 发布行为；部署形态不变。
- Public wrapper 不读取/import runtime source；projection 不执行 semantic judgment，也不
  读取 private artifact。

## 9. Trellis-check handoff

Phase 2 checker 应独立完成以下重点，不复用本交接的 pass 断言代替审查：

- 逐项绑定 R1-R12、AC1-AC15 与 P1-P15，确认 scope 只包含 #144 infrastructure/fixture，
  #145/#146 migration 未混入。
- 复核 1.2 digest、九包 typed exits/runtime commands/workflow routes 与 frozen overlay bytes，
  确认 registry metadata 没有 reinterpret legacy behavior。
- 重点审查 runtime 1.3 exact contract validation：aggregate refs/discriminator、scalar argv、
  zero-payload、per-field consumer use、projection type/private boundary、实际 stdout projection
  以及 stable errors。
- 检查 mixed fixture 能证明三包共存、四种 projection、三类 consumer/self-reentry 与三种
  private persistence，同时没有进入 production registry/manifest/platform route。
- 复核 extension inventories、installer managed assets、selected-platform bytes/modes、
  update/reapply 与 recursive sidecar 结果。
- 对照五份 workflow spec、三份 requirements 和三份 public README，完成 Docs SSOT
  reconciliation；task-local finding/log 不得反向覆盖 durable contract。
- 明确把 unpublished exact-ref marketplace verification 记为后续 publish/finish gate 风险，
  不把 public `main` sample 提升为 current-branch remote pass。

## 10. Remaining risks / follow-ups

- 实现边界内未发现未解决 blocker；Phase 2 semantic check、Branch Review 与 PR readiness
  尚未执行。
- Exact feature-ref marketplace install 待分支 reviewed commit/push 后补证。
- #145、#146 继续负责九个 production Skill 的业务 payload migration 与 legacy scalar
  最终切换；本任务不得提前关闭或吸收它们。
- Trellis CLI 0.6.7 兼容性未验证，因为批准 baseline 固定为 0.6.5；若要升级 baseline，
  应单独评审范围与官方变更。

## 11. Round 2 finding-fix implementation handoff

### 11.1 Finding closure

- `F-BR-P2-001`：已在实现层关闭。1.3 `skill_input` consumer 现在从同一份 parsed active
  registry 取得 target row，要求 producer 声明的 `interface_path` 与该 row 的 canonical
  `interface` 字段逐字相等，随后才读取 target interface 并复核 interface id。新增正常
  package copy/refactor 留下 stale same-id interface 的完整 source-validator 负例；该 locator
  现在以 `[consumer_skill_input]` fail closed。
- `F-BR-P2-005`：已在实现层关闭。`direct -> scalar_cli` 现在建立同名 identity mapping，
  与非 direct projection 共用 required-source 和 conservative all-valid-output compatibility
  proof；每个 target scalar argument 都必须由 required producer property 提供，并通过现有
  finite `const`/`enum`、non-empty string、`positive_integer` 等 helper 证明。新增 producer
  schema 允许空字符串但 example 为 `alpha` 的负例，以及 finite enum、positive integer
  正常边界正例。

上述是 implementer closure evidence，不替代 fresh Phase 2 semantic check 或新的 Branch
Review 结论。

### 11.2 Changed files

- Runtime canonical / dogfood：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- Regression tests：`trellis/skills/guru-team/tests/test_skill_packages.py`。
- Durable workflow SSOT：`.trellis/spec/workflow/companion-scripts.md`、
  `.trellis/spec/workflow/skill-package-contract.md`、
  `.trellis/spec/workflow/quality-guidelines.md`。
- Requirements / public docs：`docs/requirements/guru-team-trellis-flow.md`、
  `docs/requirements/requirement-main.md`、`README.md`、
  `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- Generated dogfood provenance：`.trellis/guru-team/extension.json`，由幂等 preset reapply
  按当前 dirty source snapshot 刷新。
- Task-local handoff：本文件。

没有修改 1.2 interface schema、production Skill package、production registry、fixture
registry/inventory、mandatory workflow route、review/gate recorder artifact 或 #145/#146
follow-up ownership。

### 11.3 Docs SSOT reconciliation

- Docs state 继续为 `complete_docs`，strategy 继续为 `ssot_first`。
- Durable contract 已明确：Skill consumer locator 必须等于 active registry target row 的
  exact canonical interface path；非 direct projection 和 direct-to-scalar projection 都
  必须证明 required-source totality 与全域兼容，单一 example 不能形成通过结果。
- Requirements 与 root/workflow/preset README 已同步相同语义；task-local Round 2 raw report
  保持审查历史，不反向成为 runtime SSOT。
- 九个 production Skill 继续为 interface 1.2 + `legacy`，#145/#146 继续负责迁移。

### 11.4 Validation

- Focused mutation tests：7/7 passed；覆盖原 target-owned/id、stale same-id locator、
  structured direct exact equality、non-direct totality，以及 scalar direct empty-string、
  finite、positive-integer 边界。
- Full Skill suite：104/104 passed。
- Preset installer suite：39/39 passed。
- Upstream ownership suite：6/6 passed。
- Source validator：passed，9 legacy、0 production minimal。
- Installed validator：passed，384 managed files，0 sidecar、0 conflict、0 removal。
- `apply.sh --repo . --all-platforms`：`status=ok`，本轮 managed assets 全部 unchanged，
  0 installed/update、0 backup、0 sidecar；source/installed/ownership 内嵌检查通过。
- Dogfood overlay drift：passed；43 frozen/active overlays identity 与 13 managed claims
  全部通过。
- Canonical/dogfood runtime bytes：equal；两份 Python `py_compile`：passed；
  `git diff --check`：passed。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh`：exit 0；覆盖
  clean init、public marketplace discovery、local unpublished workflow/preset sample、
  workflow preview/switch、初装、`trellis update`、preset reapply、source/installed/
  ownership/platform checks 与最终零 sidecar。

### 11.5 Security, deployment, and unverified boundaries

- 本轮只收紧 deterministic package authoring validation；没有把 semantic judgment、review
  或 route intent 写入脚本，也没有新增 hostile-input、竞态、锁、TOCTOU 或 fault-injection
  范围。
- 未读取或写入 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或
  敏感原始记录。
- CI/CD、service、API、worker、container、Kubernetes/Kustomize、DB migration、Makefile
  与部署配置均未修改；无部署和数据迁移影响。
- Exact current feature-ref marketplace verification 仍未完成：branch 尚未 push，public
  sample 不能冒充 immutable feature-ref pass。Trellis CLI 0.6.7 兼容性仍不在批准范围。
- 本轮未运行 Phase 2 recorder/checker、Branch Review recorder/gate、commit、push、PR 或
  finish-work；这些步骤必须由后续独立角色按 workflow 执行。

## 12. Round 4 finding-fix implementation handoff

### 12.1 Finding closure

- Round 4 `workflow/structured-stop consumer contract 未强制 consumer-owned locator` 已在
  实现层关闭。Interface 1.3 将 workflow、skill、structured stop 与 zero-payload stop
  consumer input 拆为不重叠 union；runtime 同时要求原始 locator 已是 canonical spelling，
  并分别位于 `consumers/workflow/**` 或 `consumers/stop/**`。Producer package/output locator、
  cross-kind root、`./`、重复分隔符、父目录与 symlink component 均 fail closed；zero-payload
  stop 继续不携带 schema contract。
- Round 4 `Draft 2020-12 schema 只按未闭合的自定义关键字子集执行` 已在实现层关闭。
  Standard-library runtime 新增递归 closed-subset grammar validation，明确支持当前合同所需
  的 core/applicator/validation 关键字，并拒绝所有未实现关键字、keyword 类型错误、boolean
  schema、unsupported format、非法 regex、remote/unresolved ref 与 recursive ref。实例校验
  同步处理 `$ref` 与 `oneOf` sibling constraints；只有 aggregate structured-input 的 exact
  ordered profile index 允许 package-boundary-contained relative refs。

上述是 implementer closure evidence，不替代 fresh full Phase 2 或新的 Branch Review 结论。

### 12.2 Changed files and Docs SSOT

- Canonical / installed runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- Canonical / fixture / installed interface schema：
  `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json`、
  `trellis/skills/guru-team/tests/fixtures/representative-active/schemas/skill-interface-1.3.schema.json`、
  `.trellis/guru-team/skills/schemas/skill-interface-1.3.schema.json`。
- Regression tests：`trellis/skills/guru-team/tests/test_skill_packages.py`。
- Durable workflow SSOT：`.trellis/spec/workflow/skill-package-contract.md`、
  `.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/quality-guidelines.md`、
  `.trellis/spec/workflow/companion-scripts.md`。
- Generated dogfood provenance：`.trellis/guru-team/extension.json`；preset reapply 已刷新当前
  dirty source snapshot，最终幂等 apply 未再产生 managed update/backup/sidecar。

Docs state 继续为 `complete_docs`，strategy 继续为 `ssot_first`。本轮只补强既有 #144
consumer ownership 与 schema validation 合同；九个 production Skill 仍为 1.2 + `legacy`，
#145/#146 migration scope、workflow route 与 frozen overlays 均未改变。

### 12.3 Validation

- Round 4 focused tests、完整 Skill package suite：112/112 passed。
- Preset installer：39/39 passed；upstream ownership：6/6 passed。
- Shared runtime：548 passed、13 skipped。
- External `Draft202012Validator.check_schema()` 与两个 representative fixture interface：
  passed。
- Source validation：passed，9 production legacy、0 production minimal；installed validation：
  passed，384 managed files，0 sidecar/removal/conflict。
- `apply.sh --repo . --all-platforms` 最终幂等：0 installed、0 updated managed、0 backup、
  0 new copy、0 sidecar/removal；dogfood overlay drift 与 upstream ownership 均 passed。
- Canonical/installed runtime 及 canonical/installed/fixture 1.3 schema bytes：一致；当前 1.3
  schema SHA-256 为
  `d04b0d8476cea2c33e9a1da1ab715b4576fedc514f3c8d4601847cbd78074b10`。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh`：exit 0；覆盖 clean
  init、public marketplace discovery、local unpublished workflow/preset sample、workflow
  preview/switch、初装、`trellis update`、preset reapply、source/installed/ownership/platform
  checks 与最终零 sidecar。

### 12.4 Security, deployment, and unverified boundaries

- 本轮只收紧确定性 authoring/instance validation，没有引入 semantic route/review judgment、
  hostile-input、竞态、锁、TOCTOU、fault injection 或 crash-consistency 范围。
- 未读取或写入 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或
  敏感原始记录。
- CI/CD、service、API、worker、container、Kubernetes/Kustomize、DB migration、Makefile
  与部署配置均未修改；无部署或数据迁移影响。
- 默认 exact feature-ref throwaway 仍预期 exit 2：当前 branch 尚未 push，远端无法解析
  unpublished ref。Public sample 只证明安装/update 通路，不能冒充 immutable feature-ref
  pass；该证据应在 reviewed branch push 后由 Remote Marketplace Verification Gate 补齐。
- 本轮实现后尚未运行 fresh full Phase 2、finding-fix commit、closure Branch Review、push、
  PR 或 finish-work。

## 13. Replacement Phase 2 final-byte handoff

### 13.1 Superseded evidence and finding closure

- 本节是 replacement Phase 2 checker 在 Round 4 修复后的最终字节复核。§12.3 的
  `112/112` Skill suite 与 1.3 schema SHA-256
  `d04b0d8476cea2c33e9a1da1ab715b4576fedc514f3c8d4601847cbd78074b10`
  已被后续机械修复和本节证据取代；最终结果为 `113/113`，最终 SHA-256 为
  `aa174eda5098b832a9208702e9a40ad91baddf2c6154a505ae7977c7406d003f`。
- 已关闭 P2：递归 grammar scan 现在遍历未被 example 触达的 `$defs` / local-ref graph，
  未实现 keyword、非法或 unresolved/recursive ref 均 fail closed。
- 已关闭 P2：consumer-owned locator 同时在 schema 与 runtime 拒绝 owner root 的 `./`、
  `//`、`..`、producer root 与 cross-kind root。
- 已关闭 P2：仅 root schema 允许 `$id`；nested `$id` 在 deterministic validation 中被拒绝。
- 已关闭 P3：Draft integer semantics 接受数学整数 `1.0`，拒绝 `1.5` 与 boolean。
- 已关闭 P3：非字符串 `format` 不再产生 `TypeError` traceback，而是稳定结构化 fail closed。
- 已关闭 P2：`additionalProperties: false` 且未声明 `properties` 时，实例对象的任意字段
  现在均被拒绝。
- 六项 finding 均有正常路径回归测试并在最终全量轮次通过；当前 open P0/P1/P2/P3 均为 0。

### 13.2 Final validation

- Focused finding tests：7/7 passed；完整 Skill package suite：113/113 passed。
- Shared runtime：548 passed、13 skipped；preset installer：39/39 passed；upstream
  ownership：6/6 passed。
- 外部 `Draft202012Validator.check_schema()` 加 canonical schema 与两个 1.3 fixture
  interface：3 passed；另 7 个 instance-semantics comparison 全部一致。
- 1.2 schema SHA-256 保持
  `33e5daf1362d6580027254fc15d63824cb4688c9e97e896489e9e817b034841e`；
  canonical / dogfood / representative fixture 三份 1.3 schema 字节一致，runtime canonical /
  dogfood 字节一致。
- Source validation：9 个 active production Skill 全部为 `1.2 + legacy`，0 production
  minimal；installed validation：384 managed files，0 sidecar/removal/conflict。
- `apply.sh --repo . --all-platforms` 连续两次通过；第二次 0 install/update/backup/new copy。
  九个 Skill 的 canonical package 与 `.agents` / `.codex` / `.claude` / `.cursor` 五个生成
  root 共 45 组字节比较通过，dogfood drift 与 43 frozen/active、13 managed claim ownership
  检查通过。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh` 最终 exit 0；覆盖
  public marketplace discovery、local unpublished workflow sample、clean init、初装、preview /
  switch、`trellis update`、preset reapply、initial/after-update/no-developer package smoke、
  source/installed/ownership/platform checks 与最终零 sidecar。
- 默认 exact-ref throwaway 仍按设计 exit 2：feature branch 尚未 push，远端无法解析当前
  unpublished ref；未把 public sample 冒充 exact feature-ref pass。
- 最终 `py_compile`、changed Bash `bash -n`、changed JSON `jq empty`、`task.py validate`、
  workspace boundary、planning approval、`git diff --check origin/main`、recursive
  `.new/.bak`、敏感路径/secret pattern 与 deployment-path scans 均通过。Source checkout
  clean，`suspicious_source_artifacts=[]`。

### 13.3 Docs SSOT, impact, and gate boundary

- Docs state 仍为 `complete_docs`，strategy 仍为 `ssot_first`。最终 runtime/schema/tests 与
  `.trellis/spec/workflow/{skill-package-contract,data-contracts,quality-guidelines,companion-scripts}.md`
  的 consumer ownership、closed Draft subset 与 fail-closed 合同一致；task finding 历史只留在
  task-local handoff，不成为 durable runtime SSOT。
- #145/#146 继续拥有九个 production Skill 的业务 payload migration；本轮没有把它们吸收进
  #144，也没有改变 frozen workflow route 或 public production package。
- 未发现 secret/credential/signed URL/customer data；CI/CD、service、API、worker、container、
  Kubernetes/Kustomize、DB migration、Makefile 与部署配置均无变更和部署影响。
- Replacement checker 未调用 Phase 2 recorder/checker、Branch Review recorder/gate、commit、
  push、PR 或 finish-work。仓库中现有已提交 `phase2-check.json` 绑定旧 snapshot HEAD
  `535536dbd55427241d7ce88cc14629d47fb6d26c`，不代表本节 final-byte full round；Phase 2 owner
  必须基于本节与 checker report 刷新正式 gate artifact。
- 本轮语义结论建议 `typed_exit=passed`；唯一未完成项是分支 push 后由 Remote Marketplace
  Verification Gate 执行 immutable exact feature-ref 验证，不构成当前实现 finding。

## 14. Round 6 finding-fix implementation handoff

### 14.1 Superseding finding closure

- 本节取代 §13 对当前 runtime/test 最终字节的描述，但不覆盖 §13 已关闭问题的历史。
  Round 6 新增 `F-BR-P2-008` 与 `F-BR-P3-009` 的实现修复已完成；后续 Phase 2 和
  Branch Review 必须以本节对应 dirty snapshot 重新审查，不能复用旧 `phase2-check.json`。
- `F-BR-P2-008` 根因是 minimal handoff contract 的文件 loader、package-local `$ref`、
  workflow marker 与 representative invocation stdout 使用 Python 默认 JSON 解码，且
  in-memory number validator/public serializer 没有 finite guard。现在 contract 专用 loader
  通过 `parse_constant` 拒绝 `NaN` / `Infinity` / `-Infinity`，并拒绝 `1e400` 等会超出
  finite runtime range 的数字；registry、interface、schema、example、marker、local ref 与
  invocation stdout 均复用该入口。Schema/instance 递归验证再次拒绝内存非有限数，public
  DTO 使用 `allow_nan=false` 并在失败时返回既有 structured error，不泄露 traceback。
- `F-BR-P3-009` 根因是 `date-time` 只接受 uppercase `T/Z` 且依赖不支持 leap second 的
  `datetime.fromisoformat()`，`uri` 则把宽松 `urlsplit()` 的 scheme/path 存在性误当作
  RFC 3986 validation。现在 `date-time` 用 stdlib grammar 加 calendar/clock/offset 校验，
  接受 lowercase `t/z` 和仅位于对应 UTC 六月/十二月月末边界的 leap-second notation；
  `uri` 校验 RFC 3986 ASCII scheme、hierarchy/path/query/fragment、authority、IPv6/IPvFuture、
  port、control/whitespace 与 percent encoding。已声明的两个 format 均保留，没有缩减
  public contract。

### 14.2 Changed files and generated synchronization

- Canonical runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Dogfood runtime 与 managed provenance：
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/extension.json`。两份 runtime SHA-256 均为
  `614b576f99ede68d611d21af4610ccdf8b678cf45f335292be52e93f95463301`；extension 只由
  canonical preset apply 机械刷新安装时间、source HEAD/tree state 与 sidecar inventory。
- Targeted/full regression：`trellis/skills/guru-team/tests/test_skill_packages.py`，SHA-256
  `4893840bb1304d5671a03b52e3f28d4ac8a35c8559d9dbb5eedfdd09ee7db955`。
- Durable SSOT：
  `.trellis/spec/workflow/{skill-package-contract,companion-scripts,data-contracts,quality-guidelines}.md`。
  `skill-package-contract.md` 拥有完整语义；其余文件只声明 companion 执行、data boundary
  与 test matrix 责任，没有复制 task finding history。
- Task-local history：仅追加本节 `implementation-handoff.md`；未修改 planning artifacts、
  `phase2-check.json`、`agent-assignment.json`、`review.md`、`reviews/*.md`、
  `review-gate.json`、`task-commit-plans/*.json` 或 `issue-scope-ledger.json`。

### 14.3 Exact validation results

- Targeted Round 6 regression：9/9 passed。覆盖 registry/interface、static schema/example、
  package-local `$ref`、workflow marker、invocation stdout 的 `NaN` / `Infinity` /
  `-Infinity` / overflow，内存 schema/instance finite guard、public serialization，以及
  RFC 3339/RFC 3986 正反例。
- 完整 Skill package suite：122/122 passed（原 113 项加本轮 9 项）。Shared runtime：
  548 passed、13 skipped。Preset installer：39/39 passed。Upstream ownership：6/6 passed。
- Source/installed validators 均 `status=passed`；九个 production Skills 仍全部为
  `1.2 + legacy`，installed inventory 为 384 managed files、0 sidecar/removal/conflict。
  Installed discovery 继续返回 `guru-sync-base` legacy variant 与 #145/#146 migration。
- 首次 `apply.sh --repo . --all-platforms` 只更新 dogfood runtime，并按正常 managed-file
  流程生成旧 runtime `.bak`。该 sidecar 的 SHA-256/size 已与 HEAD 旧文件逐字节证明一致
  (`7fa505...`、1271256 bytes) 后移除；第二次 apply 为
  `updated_managed=[]`、`managed_backups=[]`、`new_copies=[]`。Dogfood drift、43
  frozen/active ownership、13 managed claims 与五个 generated package roots 全部通过。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh` exit 0，覆盖 public
  marketplace discovery、local unpublished workflow sample、clean init、初装、preview/switch、
  `trellis update`、preset reapply、initial/after-update/no-developer smoke、source/installed /
  ownership/platform checks 与最终零 sidecar。默认 exact-ref verifier exit 2，因为当前
  feature branch 尚未 push；未把 public sample 冒充 immutable feature-ref pass。
- `py_compile`、`task.py validate`、workspace boundary、planning approval、canonical/dogfood
  `cmp`、installed discovery、`git diff --check origin/main`、JSON、recursive `.new/.bak`、
  secret/sensitive-path/deployment scans 均通过；source checkout clean，
  `suspicious_source_artifacts=[]`。本轮没有 Bash 代码变更。

### 14.4 Docs, scope, and next gate

- Docs state 保持 `complete_docs`，strategy 保持 `ssot_first`。严格 JSON/finite 和保留
  `date-time|uri` 的 format semantics 已进入 durable SSOT；本节仅保留复现、finding lifecycle
  与具体执行证据。
- #145/#146 继续拥有九个 production Skill payload migration；本轮没有改变 1.2 schema、
  production typed exits、mandatory workflow route 或 migration boundary。未发现 secret、
  deployment、配置、容器、K8s、DB migration 或数据迁移影响。
- 实现代理自检未发现新的 current-scope open finding，但这不替代 fresh Phase 2 或 Branch
  Review。建议 Phase 2 输入把 `F-BR-P2-008`、`F-BR-P3-009` 各记录为 `resolved`，引用本节
  9/122/548/39/6、source/installed、apply/drift/throwaway 证据，并重新计算当前 dirty
  snapshot；若独立 checker 发现新问题，应按实际 finding 返回而非沿用本建议。
- 本实现代理没有调用 Phase 2 recorder/checker、Branch Review recorder/gate、commit、push、
  PR、issue close 或 finish-work。Reviewed branch push 后仍需 Remote Marketplace Verification
  Gate 补 exact immutable feature-ref evidence。

## 15. Round 7 fresh Phase 2 checker handoff

### 15.1 New findings and mechanical closure

- `F-P2-R7-P3-001`：`date-time` validator 依赖 Python `datetime` 的 `1..9999` year
  domain，错误拒绝 RFC 3339 四位 year domain 中的 `0000`。Checker 将 calendar validation
  改为纯 proleptic Gregorian 规则，并用 minute ordinal 判断 numeric offset 下的 UTC
  June/December month-end leap-second boundary；`0000-02-29` 正常接受，非法 year-zero
  calendar date 仍 fail closed。
- `F-P2-R7-P3-002`：IPvFuture grammar 把 leading `v` 实现为大小写敏感，错误拒绝
  RFC 3986 ABNF 下等价的 uppercase `V`。Checker 将该 token 收敛为 `[Vv]`，其余
  version/address grammar、authority 与 port 校验保持不变。
- 两项修复均属于现有 supported-format contract 的机械 correctness closure，没有新增
  format、production Skill payload、workflow route 或异常加固范围。回归位于
  `trellis/skills/guru-team/tests/test_skill_packages.py`；durable contract 同步到
  `.trellis/spec/workflow/skill-package-contract.md` 与
  `.trellis/spec/workflow/quality-guidelines.md`。
- Canonical/runtime 同步文件为
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`；两份最终 SHA-256 均为
  `de1f5a6d9fe96be3a4c1fabfd1868333e8b77e7159b6e1846e85079fffc0cd1d`。
  测试文件最终 SHA-256 为
  `a11a47a461d8f4e3e314a1531c8299e52c09c382da618ede2d4d8e61a5812b5d`；
  dogfood `.trellis/guru-team/extension.json` 仅由 canonical preset apply 刷新 provenance。

### 15.2 Final-byte validation

- Targeted Round 6/7 format 与 strict-JSON regression：9/9 passed；fresh complete Skill
  package suite：122/122 passed。
- Fresh shared runtime：548 passed、13 skipped；preset installer：39/39 passed；upstream
  ownership：6/6 passed。
- 外部 `Draft202012Validator.check_schema()` 对 canonical 1.3 schema 与两个 representative
  1.3 interface：3 passed；canonical/dogfood/fixture 1.3 schema bytes 一致。
- Source/installed validators 均 `status=passed`；九个 active production Skills 全部仍为
  `1.2 + legacy`，0 production minimal；installed inventory 为 384 managed files、0
  sidecar/removal/conflict。Installed `guru-sync-base` discovery 继续返回 `legacy` variant，
  migration follow-up 为 #145/#146。
- `apply.sh --repo . --all-platforms` 第二次执行为完全幂等；dogfood drift、43 frozen/active
  ownership、37 clean-init generated overlays、13 managed claims 与 45 组 generated package
  roots 均通过。Checker 本轮首次 apply 产生的旧 runtime `.bak` 已证明是 apply 前 snapshot
  后移除；最终 recursive `.new/.bak` scan 为空。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh` 最终 exit 0，覆盖
  public marketplace discovery、local unpublished workflow/preset、clean init、preview/switch、
  initial/after-update/no-developer smoke、`trellis update`、reapply 与最终零 sidecar。默认
  exact-ref verifier 按设计 exit 2，因为当前 feature branch 尚未 push；public sample 未被
  冒充 immutable feature-ref pass。
- Final `py_compile`、changed Bash `bash -n`、changed JSON `jq empty`、`task.py validate`、
  `git diff --check origin/main`、canonical/dogfood runtime `cmp`、workspace boundary 与
  planning approval 均通过。Expected workspace 与 actual root 均为本 task worktree；source
  checkout clean，`suspicious_source_artifacts=[]`。
- Added-line secret/credential/private-key/signed-URL/database-URL pattern、敏感路径与
  deployment-path scans 均无命中；CI/CD、service、API、worker、container、Kubernetes /
  Kustomize、DB migration、Makefile 和部署配置无修改，无部署或数据迁移影响。

### 15.3 Docs SSOT and gate conclusion

- Docs state 继续为 `complete_docs`，strategy 继续为 `ssot_first`。本轮 format correctness
  delta 已先进入 durable `skill-package-contract.md` 与 `quality-guidelines.md`，runtime/tests /
  dogfood 再与其同步；finding 生命周期、命令结果和 snapshot digest 只留在本 task-local
  handoff。
- `.trellis/spec/workflow/{skill-package-contract,data-contracts,quality-guidelines,companion-scripts}.md`
  与最终 schema/runtime/fixture/installer 行为一致；#145/#146 继续拥有九个 production Skill
  payload migration，未被 #144 吸收。
- Reviewed committed HEAD 为 `61a78a90909db38bf18d59d32cf03dd712a21e1c`，上述证据绑定
  该 HEAD 上的当前 dirty implementation snapshot。Round 6 两项 finding 与本轮两项 P3
  finding 均已关闭，current-scope open P0/P1/P2/P3 为 0；本报告可支撑重新生成
  `phase2-check.json`，建议 `typed_exit=passed`。
- Checker 未调用 Phase 2 recorder/checker、Branch Review recorder/gate、commit、push、PR、
  issue close 或 finish-work。Phase 2 owner 应使用本节 final-byte evidence 刷新正式 gate
  artifact；分支 push 后仍由 Remote Marketplace Verification Gate 补 exact immutable
  feature-ref evidence。
