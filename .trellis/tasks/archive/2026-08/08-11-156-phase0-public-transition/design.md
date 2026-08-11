# #156 技术设计：Phase 0 public transition 与 source-preserving freshness

## 1. Design Principles

1. Workflow-owned transition只保存下游不能从 live authority重新推导的最小 current identity；
   semantic owner evidence保持 call-local/private。
2. 使用阶段化 closed schemas，避免 nullable/optional mega object；每个字段必须有明确 consumer。
3. `guru-sync-base` public wrapper独占 authoritative sync；低层 components不再由 AI重复编排。
4. Markdown Skill继续拥有 semantic判断，Python/shell只验证 schema、projection、freshness与执行
   已确认副作用。
5. Canonical、installed、dogfood、平台入口与 throwaway graph作为一个 activation unit交付。

## 2. Current To Target

| Boundary | Current | Target |
| --- | --- | --- |
| Sync -> Discovery | DTO只有 branch/repo；Discovery需要完整 private base evidence | `base_current`携带最小 source-preserving provenance，Discovery按 live Git复验 |
| Semantic invocation | 除 Discovery外依赖 repo-local `--owner-*` | call-local stdin invocation envelope；正常路径零 repo locator |
| Clarify/Wording -> Readiness | router DTO不带 checker-bound prerequisite | `clarity_current`与`wording_current`逐阶段累计最小 projection |
| Workspace mutation | public input只有 profile/mode，另读 owner plan/result locator | confirmed mutation内部使用 call-local plan/result，public output只保留 created/refresh/blocked DTO |
| Sync orchestration | Markdown低层 loop + public wrapper内部 loop | workflow只调用一次 public wrapper，runtime内部完成 resolve/execute/check |
| Compatibility prepare | digest + optional base无法恢复原 source | 显式接受 reviewed base provenance；缺失时 query本地 diagnostic |

## 3. Transition Schema Family

新增 workflow-owned `guru-stage0-transition-1.0` schema family，放在 canonical workflow
consumer/transition root，不放入任一 producer private package：

| Stage | Required content | Unique consumer |
| --- | --- | --- |
| `base_current` | transition id、mode、repo、resolution source、selected base、remote、ordered candidates、decision/base HEAD、post-sync digest | Discovery |
| `context_current` | `base_current` identity、target locator、context continuation/content freshness token | Clarification |
| `clarity_current` | `context_current` identity、target disposition、scope/authority content identity、clarity checker token | Wording router/Skill |
| `wording_current` | `clarity_current` identity、fixed wording profile、target content identity、wording checker token | Readiness |
| `readiness_current` | `wording_current` identity、ready scope projection、target/content/linkage identity | Workspace |

每个 stage独立 closed schema且字段全部必填。Refresh/re-entry不把 stale state向前复制：producer只投影
新 sync所需的 caller-owned target/mode/base provenance，`guru-sync-base`重建新的 `base_current`。
Stop输出继续使用 zero payload。

Transition state不包含完整 issue body、scan/history、finding列表、文件 metadata、reviewer/process
信息、用户授权或 producer artifact locator。它随 public stdout进入下一 declared consumer，成功消费后
由调用者丢弃；正常 pre-task不落盘。

## 4. Invocation Transport

### 4.1 Normal transport

为 structured Phase 0 wrappers声明一个 versioned call-local invocation envelope：

```json
{
  "schema_version": "1.0",
  "public_input": {},
  "transition": {},
  "owner_result": {}
}
```

- `public_input`必须通过目标 Skill已声明 profile schema。
- `transition`必须通过该 profile声明的唯一 stage schema；初始 sync没有 transition。
- `owner_result`只属于当前 semantic Skill，必须先完成 AI Gate，再由 public runtime调用该 Skill现有
  checker复验；它从不投影给下游。
- Deterministic sync envelope无 `owner_result`分支；Workspace在确认后使用独立的 call-local
  plan/result mutation envelope，防止把授权写入任何 artifact。
- Wrapper stdout仍只返回一个 actual typed DTO；route由 checker-passed owner result导出。

Shell入口增加明确的 stdin transport（例如 `--invocation -`），避免 `--input -` 与
`--owner-result -`争用同一 stdin。Interface、schema、examples、dispatcher help与 stable errors共同
声明该 transport。AI不需要读取 runtime source。

### 4.2 Compatibility

现有 `--input <path>` / `--owner-* <path>`只在兼容确有 consumer时暂留：

- Interface与README明确标记 `compatibility_only`，不作为 normal workflow example；
- normal workflow、production eval与完整 throwaway transcript必须使用 call-local transport；
- locator只能指向规则已声明的短生命周期 owner material，成功后由 owner消费清理；
- 若 repo现有 consumer扫描证明无外部兼容需要，则在本 task内删除，而不是保留无 consumer alias。

## 5. Producer And Consumer Changes

### 5.1 `guru-sync-base`

- Public wrapper内部执行一次 formal resolver/executor/checker，输出 `base_current`。
- `synced` DTO暴露 source、selected base、remote、ordered candidates、decision/base HEAD和
  post-sync digest的最小 projection；不暴露完整 sync result或Git操作历史。
- SKILL/contract/workflow/platform文案删除 AI低层三步编排，只保留 stable Skill invocation。

### 5.2 Discovery And Clarification

- Discovery owner checker以 `base_current` + live Git取代完整 upstream private sync result。
- Discovery `context_ready`生成 `context_current`；Clarification只接收该 public stage与当前 live
  authority，不读 Discovery private evidence。
- Clarification `clear`生成 `clarity_current`；duplicate retain/retarget与 refresh exits各自只投影
  唯一 consumer需要的 current target/base continuation。

### 5.3 Wording And Readiness

- Wording `change_request`消费 `clarity_current`，其 `pass`输出 `wording_current`；
  `content_changed`完整重入时废弃旧 stage并重新读取 authority。
- Readiness recorder/checker不再接收完整 `--owner-prerequisites`文件；它验证
  `wording_current`内的 clarity/wording最小 projections与 live target/content。
- Readiness `ready`生成 `readiness_current`，保持十维 semantic review不变。

### 5.4 Workspace

- Workspace消费 `readiness_current`，独立读取 live naming/branch/worktree/task facts并展示精确
  副作用；confirmation仍只存在于当前对话。
- Recorder/executor/checker通过 call-local plan/result transport串联。成功后只写
  `issue-scope-ledger.json`和现有 ignored workspace/task mappings；不保存 prerequisite bundle。

## 6. Source-Preserving Freshness

将 base resolution provenance定义为 closed value：

```text
source + selected_base + remote + ordered_candidates + decision_head
+ local/remote base head + post_sync_resolution_sha256
```

`resolve_base_selection`增加 reviewed provenance输入路径：按 recorded source重建同一优先级输入，
而不是先尝试 configured fallback resolver再猜测显式 base。验证顺序为：

1. schema与source/candidate/base关系；
2. current config/remote与reviewed provenance是否仍可解析同一 selection；
3. current decision/local/remote HEAD与clean state；
4. post-sync resolution digest；
5. 仅在全部相同时复用。

Compatibility `prepare-task`接受完整 reviewed provenance（一个 JSON scalar或一组
provenance-preserving closed arguments），而不是只接受 digest。缺失时返回
`missing_reviewed_base_provenance`，不得执行
GitHub reads、fetch或semantic route；真实变化返回 `base_provenance_changed`或
`base_state_changed`并保持 query-only。

## 7. Single Sync Boundary

```text
workflow stable Skill call
  -> guru-sync-base public wrapper
    -> resolve
    -> execute one guarded fetch/ff-only path
    -> objective check
    -> base_current stdout
  -> Discovery
```

Low-level `sync-base.sh`/`check-base-sync.sh`保留为 package internal components和 focused tests，
不再出现在 normal workflow、platform prompt或用户执行步骤中。Refresh exit重新调用整个 public
Skill一次，不先运行低层 guard。

## 8. Validation Design

### 8.1 Contract tests

- 五阶段 transition schemas、每条 exit/consumer projection、全部字段 direct-use与 stage mismatch。
- Envelope unknown/missing field、wrong transition stage、owner/input/target mismatch与 stable errors。
- normal wrappers拒绝隐藏 repo locator作为唯一 transport，legacy路径只出现在兼容矩阵明确列出的 case。
- source/candidates/base/digest/HEAD真实变化与 representation-preserving 回归。

### 8.2 End-to-end public transcript

在 clean throwaway安装后的 package root运行同一 production harness：

1. existing open issue happy path直至 workspace/task creation；
2. reviewed draft创建 issue后 refresh/re-entry；
3. duplicate retain与 retarget；
4. wording pass/content_changed；
5. readiness reroute/ready；
6. refresh与每个 stop family。

每个 semantic owner payload通过 production recorder/checker；producer actual stdout直接进入下一
consumer envelope。Harness不得 import shared runtime，不写隐藏 prerequisite locator，expected exit只在
actual output之后断言。

### 8.3 Distribution

- source/installed package graph、migration manifest、registry、extension inventory集合完全匹配；
- preset staging原子安装完整 transition family和六包；失败保留旧完整 graph；
- fresh install、existing workflow preview/switch、update/reapply、平台副本、managed hashes、
  ownership、overlay drift及零 sidecar。

## 9. Ownership And Affected Surfaces

| Owner | Primary surfaces |
| --- | --- |
| Durable workflow contracts | `.trellis/spec/workflow/{skill-package-contract,workflow-contract,data-contracts,companion-scripts,quality-guidelines,index}.md` |
| Product requirements | `docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md` |
| Canonical workflow | `trellis/workflows/guru-team/workflow.md`、workflow consumer/transition schemas、README |
| Six packages | `trellis/skills/guru-team/packages/guru-{sync-base,discover-change-context,clarify-requirements,review-contract-wording,review-change-request,create-task-workspace}/**` |
| Shared deterministic runtime | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`及 tests/bash wrappers |
| Activation/distribution | registry、stage0 migration manifest、extension manifest、preset scripts/tests/README/overlays |
| Installed copies | `.trellis/**`、`.agents/**`、`.codex/**`、`.claude/**`、`.cursor/**`及 manifest声明平台，仅由 preset同步 |

## 10. Compatibility, Rollout And Rollback

- Stable Skill ids与 typed exit ids不变；transition/envelope schemas使用新 versioned ids。
- 六包、workflow consumer schemas、runtime和manifest一次激活，禁止 mixed graph。
- Canonical/source validation失败时不运行 preset apply；installed validation失败时保留旧完整 graph
  并处理 sidecar后重试。
- 如果实现证明现有外部 locator consumer不可安全移除，保留明确 compatibility-only adapter与
  removal condition；不得让 adapter成为 normal route。
- 任一 semantic ownership或用户选择边界需要变化时停止实现，回到 clarification/planning review。

## 11. Risks

| Risk | Mitigation |
| --- | --- |
| Transition逐步膨胀成 audit artifact | 独立 stage schemas、字段 direct-use proof、禁止 private/process fields |
| Readiness丢失必要 prerequisite | 以 consumer checker实际读取字段反推最小 projection，并加真实 transcript |
| stdin transport与旧 wrappers冲突 | versioned envelope flag、closed parser、compatibility matrix和 stable errors |
| Base representation-preserving 路径掩盖真实 drift | source-preserving reconstruction后仍核对 selected base、HEAD、clean和digest |
| Installer形成 mixed graph | staging validation + versioned activation unit + source/installed集合完全匹配 |

## 12. Provenance Matrix

| ID | Load-bearing conclusion | Authority |
| --- | --- | --- |
| P1 | 六包必须作为完整 producer/consumer graph修复 | Issue #156 Scope A/C/D；#145 atomic activation |
| P2 | 正常路径使用阶段 transition，不使用 private artifact locator | Issue #156 Scope A；#144 Interface 1.3；#178 ephemeral path |
| P3 | Base provenance必须保留 source/candidates/HEAD/digest | Issue #156 Scope B |
| P4 | Public sync是唯一 authoritative入口 | Issue #156 Scope C；官方 workflow Markdown扩展合同 |
| P5 | Prepare仅为 compatibility query且缺 provenance本地阻断 | Issue #156 Scope B |
| P6 | Semantic ownership和human confirmation不变 | Issue #156 non-goals；AGENTS Markdown/script boundary |
| P7 | 真实 throwaway transcript不得合成 hidden prerequisites | Issue #156 Scope D |
| P8 | Canonical/install/platform/update形成同一交付 | Issue #156 Scope E；仓库开箱即用与抗漂移门禁 |

P1-P8覆盖 PRD R1-R7 与 A1-A12，无 scope expansion 或 unresolved product choice。
