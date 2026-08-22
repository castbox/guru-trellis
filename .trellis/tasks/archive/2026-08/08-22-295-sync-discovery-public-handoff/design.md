# #295 技术设计：Sync public base_current 到 Discovery live observation

## 1. Design Principles

1. Sync private result只由Sync owner消费；`base_current`是跨owner的唯一事实投影。
2. Discovery使用自己的live observation证明entry freshness，不反向重建producer private state。
3. Schema语义变化使用新versioned id和新active path；旧schema保持历史兼容，不发生silent break。
4. AI继续拥有Discovery semantic review；Python仅执行schema、Git identity、freshness与typed route
   的确定性校验。
5. 产品wrapper与test统一通过managed interpreter；PATH Python只用于构造受控缺依赖fixture。
6. Canonical source、dogfood installed与四个平台投影作为一个managed package unit交付。

## 2. Current To Target

```text
Current
Sync public base_current
  -> transcript/private caller reconstructs guru-base-sync-result-1.0
  -> Discovery owner-result 2.0 embeds Sync private result + private digests
  -> checker validates reconstructed producer internals

Target
Sync public base_current
  -> declared thin projection creates Discovery public input 2.0
  -> Discovery checker live-reads authority and creates base_observation
  -> Discovery owner-result 3.0 binds only Discovery-owned evidence
  -> context_ready public output projects to Clarify
```

## 3. Public Contract Migration

### 3.1 Preserved Sync API

- Stable Skill id：`guru-sync-base`。
- Stable exit：`synced`。
- Active output：`guru-stage0-sync-base-output-synced-2.0`。
- Active transition：`guru-stage0-transition-base-current-1.0`。
- `guru-base-sync-result-1.0`继续是`stdout_only_pre_task` private artifact。

Sync interface的`project_synced` projection继续投影caller-owned scalar fields，并把真实
`transition`作为独立`base_current`传给Discovery semantic invocation。该projection不映射
`facts_sha256`或private result。

### 3.2 Discovery input 2.0

新增：

- `schemas/public-pre-task-input-2.0.schema.json`
- `examples/public-pre-task-input-2.0.json`
- aggregate input的新active discriminator引用
- interface consumer/projection/eval与installed inventory引用

2.0 input字段固定为：

```text
profile=pre_task
source_exit=synced|declared standalone start
mode=workflow|standalone
change_input=<closed clue set>
continuation_id=<caller-owned identity>
```

`repo_locator`、`base_branch`和完整base provenance由独立`base_current`提供，不在public input
重复表达。旧`public-pre-task-input.schema.json`保留1.0 immutable identity并退出active graph。

### 3.3 Discovery owner-result 3.0

新增active schema/example 3.0；旧2.0 schema/example保留legacy identity。3.0删除：

- `base_evidence.sync_result`
- `$defs.baseSyncResult`
- `base_sync_facts_sha256`
- 将Sync private digest视为Discovery freshness authority的字段

3.0增加owner-private `base_observation`：

```json
{
  "repo": "castbox/guru-trellis",
  "repo_locator": "<authority checkout locator>",
  "selected_base": "main",
  "remote": "origin",
  "authority_branch": "main",
  "decision_head": "<sha40>",
  "local_head": "<sha40>",
  "remote_head": "<sha40>",
  "clean": true,
  "current": true
}
```

Machine-local locator只存在call-local owner evidence；public output继续只携带transition需要的
portable identity。

## 4. Live Freshness Algorithm

Discovery在任何Issue/Docs/code/test/history读取前执行：

1. 校验public input 2.0与`base_current` closed schemas、mode、continuation和stage一致。
2. 以`base_current.repo_locator`解析authority checkout并核对Git common-dir与GitHub repo identity。
3. 核对authority symbolic branch必须与selected base相同，checkout HEAD必须与decision HEAD相同。
4. 核对local `refs/heads/<base>`和remote-tracking ref仍存在，且必须与public HEAD identity相同。
5. 核对authority clean且没有worktree/ref ambiguity。
6. public identity仍current时生成`base_observation`并继续semantic discovery。

Typed route矩阵：

| Observation | Exit | Side effect |
| --- | --- | --- |
| public/live HEAD current且authority clean | continue owner，最终可`context_ready` | none |
| remote/local base正常前进或public identity stale | `refresh_base` | none |
| dirty、wrong branch/ref、missing、repo mismatch、ambiguous、invalid structure | `blocked` | none |

Discovery不fetch或修改任何ref。`refresh_base`仅投影Sync public input需要的mode/repo/base/route，
不保留旧private result或supersession chain。

## 5. Runtime And Dependency Boundary

- Package shell wrappers继续只source package `runtime/launch.sh`。
- Shared launcher继续通过`runtime/resolve-python.sh`验证active pointer、runtime inventory、
  interpreter executable与dependency lock，再运行dispatcher。
- Target tests通过public wrapper或显式managed test launcher进入同一interpreter。
- PATH Python无`jsonschema` fixture不直接运行package Python module；fixture用PATH隔离后调用
  public wrapper并断言managed interpreter成功。
- `active.json`缺失、runtime id过期、interpreter缺失或inventory drift分别保持精确
  `runtime_not_bootstrapped`、`managed_runtime_missing`或`runtime_dependency_missing` error。

## 6. Transcript And Test Design

### 6.1 Real wrapper chain

代表性fixture按以下顺序执行：

```text
sync invoke.sh --invocation -
  -> actual synced stdout
  -> interface project_synced projection
  -> discovery invoke.sh --invocation - with public input 2.0 + actual base_current
  -> actual context_ready stdout
  -> interface project_context_ready projection
  -> Clarify input schema validation
```

Discovery owner result仍由AI语义fixture authoring加production recorder/checker产生，但其base
evidence只能来自Discovery live observer。Fixture不读取Sync private stdout，不调用
`sync-base.sh`/`check-base-sync.sh`，不import Sync package runtime。

### 6.2 Behavior matrix

- detached invocation + clean main authority + existing open Issue -> `context_ready`。
- proposed draft与zero-history -> `context_ready`。
- no-impact semantic result保持pass。
- remote/local base advance -> `refresh_base`。
- dirty、wrong branch/ref、missing ref、repo mismatch、ambiguous worktree -> `blocked`。
- normal pre-task全链前后Git status与protected path inventory一致。
- PATH Python无jsonschema仍经public wrappers通过；missing/stale managed pointer精确失败。

## 7. Distribution And Managed Projections

Canonical修改位于：

- `trellis/skills/guru-team/packages/guru-{sync-base,discover-change-context}/**`
- `trellis/skills/guru-team/consumers/workflow/stage0/**`
- registry、migration/activation、shared runtime/tests
- `trellis/workflows/guru-team/**`
- `trellis/presets/guru-team/**`

Preset apply生成并验证：

- `.trellis/guru-team/skills/packages/**` installed runtime copy
- `.agents/skills/guru-*/**` Shared discovery
- `.codex/skills/guru-*/**`
- `.claude/skills/guru-*/**`
- `.cursor/skills/guru-*/**`
- current extension manifest、hashes、modes与selected platform inventory

Canonical先通过source validation；随后执行all-platforms reapply。任何unknown local edit、`.new`
或`.bak`使activation失败，不能用覆盖解决。

## 8. Docs And Architecture Impact

- Docs strategy：`delta_first`。
- RDT contribution建立#295 requirement/design/test/traceability delta。
- Architecture contribution选择`target_native`：不增加新owner、不保留dual read、不扩大public
  DTO，只使现有`ARCH-DOM-004` deterministic runtime和`ARCH-INT-001` public projection满足
  `ARCH-DOM-001` workflow lifecycle contract。
- ADR `required=false`：现有public/private boundary和single-writer原则不变。
- shared `.39` current不在task implementation阶段直接修改；promotion owner在full-diff review后
  生成successor current并触发fresh gates。

## 9. Compatibility And Rollback

- Skill ids、typed exits、Sync output 2.0、base-current 1.0与Clarify consumer保持兼容。
- Discovery input 1.0与owner-result 2.0退出active graph但保留versioned legacy assets；active
  installation禁止mixed 1.0/2.0 input或2.0/3.0 owner runtime。
- Schema/runtime/interface/transcript/preset作为一个activation unit更新。
- Source validation失败时不reapply；installed sidecar或drift出现时停止并修复canonical/provenance。
- 实现若需要暴露Sync private result、改变semantic ownership或扩大Issue scope，立即回到planning。

## 10. Risks

| Risk | Control |
| --- | --- |
| public input与transition重复base authority | 2.0 input删除repo/base字段，base只由transition拥有 |
| live observer误把正常advance视为structural block | route matrix区分stale current与invalid authority |
| tests继续通过private helper构造输入 | static scan删除helper并要求actual wrapper stdout |
| PATH Python掩盖managed runtime缺陷 | PATH隔离fixture只调用public wrapper并验证pointer errors |
| installer形成mixed graph | version inventory、source/installed validation与single reapply gate |
| shared current并行冲突 | task-owned contributions + expected `.39` serialized promotion |
