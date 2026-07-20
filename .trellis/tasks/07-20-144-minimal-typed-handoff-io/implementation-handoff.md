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
