# #110 技术设计：`guru-sync-base`

## 1. 设计结论

在现有 public Skill infrastructure 上增加一个 active package，并把已有 base resolution、planner refresh 与 executor freshness 逻辑收敛为共享 deterministic core：

```text
tool-free route
  -> guru-sync-base resolve-only stdout facts
  -> pre-sync digest-bound sync executor
  -> post-sync resolution digest
  -> schema/digest/live Git validator
  -> synced | skipped | blocked
```

Global workflow 只拥有 AI tool-free route classification、mandatory invocation、route transition 与 typed-exit consumer。`guru-sync-base` package 声明 `judgment_mode=deterministic`，独占 selected-base resolution、sync procedure、recorder/validator 与 standalone behavior；Skill 内不执行 selected-base AI confirmation、post-execution AI Review Gate 或 conditional human confirmation。实现不引入 repo-external evidence lifecycle、lease、release executor 或 quarantine cleanup 合同。

## 2. SSOT 与资产边界

| 层 | Canonical SSOT | 责任 |
| --- | --- | --- |
| Global workflow | `trellis/workflows/guru-team/workflow.md` | tool-free route、mandatory invoke、exit transition、fail-closed stop |
| Public Skill | `trellis/skills/guru-team/packages/guru-sync-base/` | 完整 step-local 闭环合同 |
| Registry/interface | `trellis/skills/guru-team/registry.json`、`trellis/skills/guru-team/schemas/skill-interface.schema.json` 与 package `interface.json` | public id、`judgment_mode`、stage profile、mode parity、runtime dependency、validator、exit consumer |
| Deterministic runtime | `trellis/workflows/guru-team/scripts/` | base resolution facts、fetch、ff-only、result encode、schema/digest/live Git validation |
| Distribution | `trellis/presets/guru-team/` | canonical audit、installed package、平台副本、managed hashes、extension manifest |
| Dogfood | `.trellis/guru-team/skills/` 与平台 skill roots | 生成运行副本，不拥有语义 |
| Durable contracts | `AGENTS.md`、`docs/requirements/**`、`.trellis/spec/**`、三份 public README | 人类可审查长期合同与 deterministic 例外边界 |

## 3. Base resolution

### 3.1 输入

- `--base <branch>`：用户显式 base。
- `.trellis/guru-team/config.yml` 的 scalar `base_branch`；空字符串代表未配置。
- `base_branch_candidates`：有序候选列表，缺省为 `dev`、`develop`、`main`、`master`。
- Remote 名固定从 `--remote` 读取，省略时为 `origin`。

### 3.2 固定顺序

1. 显式 `--base`。
2. 非空 scalar `base_branch`。
3. 对 `base_branch_candidates` 按配置顺序去重，选择首个拥有 exact local ref 或 `<remote>/<candidate>` remote-tracking ref 的 branch；缺省优先级为 `dev -> develop -> main -> master`。
4. 只有第 3 步没有任何 existing candidate 时，才使用 `git ls-remote --symref <remote> HEAD` 返回的 remote default branch。

每个实际进入的优先级来源都必须通过 `git check-ref-format --branch`；显式 `--base` 或 scalar `base_branch` 已选定时，低优先级候选不得提前阻断。第 3 步保留第一次出现的候选顺序，多个 existing candidate 不是歧义；resolver 必须选择最高优先级的一个。候选不存在且 remote default 查询失败时返回结构化 `blocked`，不产生 current-branch fallback。

该顺序保留 #110 前 `prepare-task` 的已有行为：旧 `resolve_base_branch()` 依次扫描 `dev`、`develop`、`main`、`master` 并返回首个 existing ref。Remote default 是最后的 repo fallback，不得因 GitHub 缺省指向 `main` 而覆盖已存在的 `dev` 或 `develop`。

Resolution `source` 固定为 `explicit`、`config`、`config-candidate`、`remote-default` 之一，分别对应上述四级来源。有序 candidate 选中时只能记录 `config-candidate`。

`sync-base --resolve-only` 只向 stdout 输出 resolution JSON，记录 `source`、selected base、remote、候选集合、完整 pre-sync decision checkout 与 `resolution_sha256`，不写本机路径。Workflow 的 AI route classification 只决定是否调用 Skill；selected base 由上述确定性优先级直接决定，不再要求 AI 确认。

`sync-base --execute --expected-resolution-sha256 <digest>` 在执行边界重新解析同一输入。digest 或重算结果不匹配时返回 `blocked`，不得 fetch 或修改 ref。

Execute 成功后重新解析同一 provenance/base/remote/candidates 与同步后的 decision checkout，输出 `post_sync_resolution` 和 `post_sync_resolution_sha256`。Already-equal 时两个 digest相同；fast-forward 时 post-sync digest 必须反映新 HEAD 并区别于 pre-sync digest。Pre-sync digest 只保护 resolve-to-execute，post-sync digest 才能由 validator 和下一 freshness guard 消费。

## 4. Sync state machine

### 4.1 前置 facts

Resolve-only 与 execute 从当前 invocation repository 读取：

- decision checkout branch；
- decision HEAD before；
- NUL-safe dirty status；
- selected local ref HEAD；
- selected remote-tracking ref locator。

Dirty 或 local ref 缺失在 fetch 前返回 `blocked`。Execute 还必须证明 resolver stdout 的 resolution digest 与当前重算结果一致。

### 4.2 Fetch 与 fast-forward

1. 执行显式 refspec fetch：`git fetch --no-tags <remote> refs/heads/<base>:refs/remotes/<remote>/<base>`。
2. Fetch 非零或 remote ref 缺失返回 `blocked`。
3. Local 与 remote SHA 一致时不修改 local branch。
4. Local 是 remote ancestor时，decision checkout branch 必须与 selected base 同名，然后执行 `git merge --ff-only <remote>/<base>`。
5. Local 不是 remote ancestor时返回 `blocked`。
6. 非 selected-base checkout 不通过 `git branch -f` 修改 base；该路径返回 `blocked`。

### 4.3 Fresh equality

同步后重读 decision HEAD、local base HEAD、remote base HEAD 与 dirty status。Checkout 必须保持 clean，三个完整 commit SHA 必须逐字符完全一致；否则 `fresh=false` 并返回 `blocked`。

## 5. Result 与 validator

### 5.1 Schema

新增 `schemas/base-sync-result.schema.json`，schema id 为 `guru-base-sync-result-1.0`。Success result 使用 closed object：

- `schema_version`、`skill_id`、`status`；
- `resolution`：source、selected base、remote、candidates；
- `decision_checkout`：branch、HEAD before/after、clean before/after；
- `git`：local/remote refs、HEAD before/after、fetch、fast-forward facts；
- `fresh`；
- `post_sync_resolution` 与 `post_sync_resolution_sha256`；
- `facts_sha256`。

`facts_sha256` 对去掉自身字段后的 canonical JSON bytes 计算 SHA-256。Example 只使用去身份化 branch/SHA，不写本机路径。

### 5.2 Deterministic recorder/validator

- Resolve-only 与 execute 都向 stdout 输出 JSON facts，不创建跨步骤 result/resolution 文件。
- `guru-sync-base` 的 stage 顺序固定为 `forward_behavior -> recorder_validator -> typed_exit`；输入、状态转换、副作用与 pass/block 条件完全由 resolver、executor 与 validator 机器验证。
- `check-base-sync` 接收 executor result 中的 selected base、pre-sync resolution digest、post-sync resolution digest、facts digest 与 HEAD facts，重新读取 live Git，重建 canonical result，校验 Draft 2020-12 schema、两个 identity generation、selected refs 与当前 clean equality。
- Validator 不 fetch、不 fast-forward、不判断 route、scope、finding 或 semantic pass。
- `skipped` 路径不运行 Git executor；workflow 在 Skill 调用前已经完成 tool-free route classification，`check-base-sync --record-skipped <route-id>` 只生成并校验 stdout-only recorder facts，standalone mode 拒绝该入口。
- 如果未来引入任何 scope、充分性、finding、revision action、用户选择或 route intent 判断，package 必须切回 `judgment_mode=semantic`，不得继续使用 deterministic profile。

## 6. Skill package 与 typed exits

Package 包含 `SKILL.md`、`interface.json`、contract reference、两个 thin wrappers、result schema、example 与 package tests。Caller 在 package 外完成 tool-free route classification 或 standalone 用户意图识别；interface 只接收可机器校验的 normalized `invocation_mode` 与 route id，不把 `invocation_intent` 伪装成 deterministic Skill 内部判断。两个 mode 使用相同的 `runtime_dependency`、`decision_checkout`、`selected_base_resolution`、`clean_checkout` 与 `result_facts` preconditions。

Skill interface schema 从 `1.1` 升级为 `1.2`，新增必填 `judgment_mode` 并条件约束 `ordered_stages`：

- `judgment_mode=semantic`：`forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`。
- `judgment_mode=deterministic`：`forward_behavior -> recorder_validator -> typed_exit`。

Source 与 installed interface validator 必须按 profile 精确校验字段和阶段，并拒绝缺失、未知或 profile/stage mismatch。当前 active interfaces 同步迁移：`guru-sync-base` 使用 deterministic，`guru-create-task-commit` 显式使用 semantic；后者行为不变。Stable skill id、external exit id、runtime command 不变。

| Exit | Consumer | 证据 |
| --- | --- | --- |
| `synced` | workflow route `guru-discover-change-context` | validator-passed fresh result facts 与 post-sync resolution digest |
| `skipped` | workflow route `original-request-route` | tool-free route classification 与 stdout-only recorder facts |
| `blocked` | stop `base-sync-blocked` | resolution、Git 或 validator failure facts |

`guru-discover-change-context` 在 #110 中仍指向现有 inline context discovery route；#111 才把该 route 内部实现替换成 mandatory public Skill，consumer id 不变。

## 7. Workflow integration

Phase 0 顺序调整为：

```text
tool-free request classification
  -> mandatory invoke guru-sync-base
  -> synced: guru-discover-change-context route
  -> skipped: original request route
  -> blocked: stop
```

`check-env`、`prepare-task`、issue read、duplicate search、Docs/code/tests/history discovery 均位于 `synced` 之后。Global workflow 只消费 typed exit，不拥有 Skill 内部验证步骤，也不承载 implement/check sub-agent 行为。

## 8. `prepare-task` reuse

共享 core 替换 current-branch fallback 与 planner stale-only behavior，并使用 rolling post-sync identity：

1. `guru-sync-base` 的 validator-passed `post_sync_resolution_sha256` 是 `cmd_prepare` 第一条 guard 的 expected digest；同步前 `resolution_sha256` 不得跨过 fast-forward 继续复用。
2. `cmd_prepare` 在 `gh auth status`、issue read、duplicate search 前调用 shared sync core，消费 expected digest并获得 initial fresh result与新的 post-sync digest。
3. Planner payload 继续在 `preflight.base_freshness` 暴露兼容字段，并新增 pre/post resolution、decision checkout 与三方 equality facts。
4. `--create-issue-confirmed` 在 GitHub mutation 前消费 planner guard 输出的 post-sync digest并重跑 core。
5. `--create-worktree` / `--create-task` 在 mutation 前依次消费上一 guard 输出的 post-sync digest并重跑 core。
6. Task-start context 只保存 portable base/local/remote SHA，不保存完整 pre-task result 或本机 path。

`refresh_base_freshness_for_planner` 与 `ensure_base_freshness` 保留为内部兼容 adapter，二者调用新 core；旧 planner 不再把 `stale` 当成可继续 plan。

## 9. Distribution 与 public API

- Extension version 从 `0.6.5-guru.6` 升到 `0.6.5-guru.7`。
- `active_skill_ids` 加入 `guru-sync-base`。
- `artifact_schema_ids` 加入 `guru-base-sync-result-1.0`。
- `companion_scripts` 加入 `sync-base` 与 `check-base-sync`。
- Preset 安装 canonical package 到 `.trellis/guru-team/skills/`，并按 selected platforms 分发 shared、Codex、Cursor、Claude copies。
- Dogfood 使用 canonical preset apply 生成；不得手改 generated copies。
- Managed hash、`.new`、`.bak`、installed manifest 与 sidecar 规则沿用现有合同，不新增旁路。

## 10. 测试矩阵

### 10.1 Runtime unit tests

- 四级 resolution、lazy precedence、stdout pre-sync digest、execute re-resolution binding 与 post-sync digest generation。
- Ordered candidates 覆盖 `dev + main -> dev`、`develop + main -> develop`、`main + master -> main`、单一候选、同名 local/remote ref 去重与自定义候选顺序。
- 候选均不存在时 remote default query success/failure；全部来源失败时 `blocked`。
- Invalid branch、dirty、missing local、missing remote、fetch failure。
- Already fresh、behind + ff-only、diverged、wrong checkout、post-sync mismatch。
- 真实 Git `behind -> resolve -> execute ff-only -> validate -> prepare`，并断言 prepare 使用 post-sync digest；config/branch/dirty/digest drift 在 fetch 或 mutation 前阻塞。
- Result schema/digest tamper、stale Git facts与 validator live re-read。
- `prepare-task` initial sync 发生在 issue read 前；executor rerun 发生在 mutation 前；每个 guard 的 post-sync digest 成为下一 guard 的 expected digest。

### 10.2 Package/distribution tests

- Interface schema `1.2`、`judgment_mode` 必填、semantic/deterministic exact stage profiles、profile/stage mismatch rejection、两个 active interface migration、mode parity、runtime commands 与 exit map。
- Missing/unknown/duplicate/unmapped marker fail closed。
- Source/installed package validation。
- Selected platform inventory、managed upgrade backup、unknown edit sidecar。
- Standalone wrapper 缺 runtime、drift runtime、完整 preset runtime 三类结果。

### 10.3 Integration gates

- Canonical unit suites、package tests 与 preset installer tests。
- Dogfood apply、source/installed validation、overlay drift。
- Clean throwaway marketplace init/preview/switch、preset apply、behind-base `resolve -> execute ff-only -> validate -> prepare`、already-equal workflow、`trellis update`、workflow/preset reapply 与零 sidecar。
- Branch push 后执行 remote marketplace verifier，再进入 finish-work。

## 11. Docs SSOT Plan

- `docs_state`: `partial_docs`
- `strategy`: `ssot_first`
- 原因：本任务改变 Phase 0 顺序、public Skill API、closed-loop Skill 基础合同、interface schema、config、runtime commands、installer inventory 与 upgrade contract。
- 实现前更新：`AGENTS.md`、`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、`.trellis/spec/workflow/index.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/docs/public-docs.md`。
- Interface migration assets：`trellis/skills/guru-team/schemas/skill-interface.schema.json`、`trellis/skills/guru-team/packages/guru-sync-base/interface.json`、`trellis/skills/guru-team/packages/guru-create-task-commit/interface.json`、source/installed interface validator、representative fixtures 与 package/registry/preset tests。
- Workflow/distribution assets：`trellis/workflows/guru-team/workflow.md`、dogfood `.trellis/workflow.md`、canonical package、preset installer/overlays、installed/platform/dogfood copies与 extension manifest。
- 实现后同步：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- Task delta merge：deterministic 例外、semantic 保留边界、schema `1.2` 迁移、四级 resolution、三方 equality、pre/post-sync digest generation、typed exits、rolling prepare guard、distribution 与验证矩阵必须进入 durable contracts。
- Merge checkpoint：任何 runtime/schema/package 代码落地前先完成 durable docs/spec；Phase 2 check 复核 docs、workflow、package、runtime、preset、dogfood 与 tests 一致。
- Task-history-only：issue 检索过程、Phase 0 命令输出、sub-agent liveness 与逐轮 finding 保留在 task artifacts，不进入 public package。

## 12. 兼容性、回滚与安全

- Stable workflow id、preset path、既有 Skill id 与既有 companion command 不改名。
- Skill interface schema `1.2` 是显式迁移：所有 active interface 同批更新，旧 `1.1` 或缺失 `judgment_mode` fail closed；迁移不改变既有 semantic Skill 的行为和 exits。
- `guru-create-task-commit`、Phase 2 `trellis-check`、Branch Review Gate 与 PR readiness 继续由 AI 作 scope、充分性、finding、revision 和 pass/block 判断，不受 deterministic 例外放宽。
- `base_branch_candidates` 继续受支持；多值配置必须按声明顺序选择第一个 existing ref，保留 #110 前 `prepare-task` 的既有语义。
- 不增加 release-resolution mode、evidence lease、quarantine 或 cleanup public API。
- 回滚采用 Git revert 与上一 extension ref 重新应用 workflow/preset；installer 不自动选择 `.new`/`.bak` 内容。
- 本任务不新增服务、数据库、migration、容器、Kubernetes、queue、schedule、CI/CD pipeline 或 Makefile target。
- 日志与 artifacts 不得包含 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或本机绝对路径。

## 13. 需求追踪

| PRD | 设计 | 实现计划 | 验收 |
| --- | --- | --- | --- |
| Public Skill 与 mode parity | 第 2、6、9 节 | 第 3、4、6 步 | AC1、AC2、AC3 |
| Deterministic 例外与 interface schema `1.2` 迁移 | 第 2、5、6、11、12 节 | 第 1、2、3、6、7、8 步 | AC1、AC2、AC3 |
| 四级 base resolution | 第 3 节 | 第 3、5 步 | AC5 |
| Safe sync 与三方 equality | 第 4、5 节 | 第 5 步 | AC4、AC6、AC7 |
| Workflow first action 与 exits | 第 6、7 节 | 第 4 步 | AC2、AC3、AC4 |
| `prepare-task` shared core reuse | 第 8 节 | 第 5 步 | AC8 |
| 分发、dogfood、update | 第 9、10 节 | 第 6、7、8、9 步 | AC9、AC10 |
| Docs、安全、部署 | 第 11、12 节 | 第 1、8、9 步 | AC10、AC11 |
