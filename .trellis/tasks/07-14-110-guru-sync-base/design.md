# #110 技术设计：`guru-sync-base`

## 1. 设计结论

在 #120/#125 已合并的 public Skill infrastructure 上增加一个 active package，并把现有 `resolve_base_branch`、planner refresh、executor freshness 逻辑收敛为共享 deterministic core：

```text
tool-free route
  -> guru-sync-base resolve-only evidence
  -> AI invocation/selected-base confirmation
  -> digest-bound sync executor
  -> AI Review Gate
  -> conditional confirmation stage
  -> result schema/digest/live Git validator
  -> synced | skipped | blocked
```

Global workflow 只拥有 mandatory invocation、route transition 与 typed-exit consumer。Skill package 独占 selected-base resolution、sync procedure、AI review dimensions、evidence lifecycle 与 standalone behavior。

## 2. SSOT 与资产边界

| 层 | Canonical SSOT | 责任 |
| --- | --- | --- |
| Global workflow | `trellis/workflows/guru-team/workflow.md` | tool-free route、mandatory invoke、exit transition、fail-closed stop |
| Public Skill | `trellis/skills/guru-team/packages/guru-sync-base/` | 完整 step-local 闭环合同 |
| Registry/interface | `trellis/skills/guru-team/registry.json` 与 package `interface.json` | public id、mode parity、runtime dependency、schema、validator、exit consumer |
| Deterministic runtime | `trellis/workflows/guru-team/scripts/` | base resolution facts、fetch、ff-only、result encode、schema/digest/live Git validation |
| Distribution | `trellis/presets/guru-team/` | canonical audit、installed package、平台副本、managed hashes、extension manifest |
| Dogfood | `.trellis/guru-team/skills/` 与平台 skill roots | 生成运行副本，不拥有语义 |
| Durable contracts | `docs/requirements/**`、`.trellis/spec/**`、三份 public README | 人类可审查长期合同 |

## 3. Base resolution

### 3.1 输入

- `--base <branch>`：用户显式 base。
- `.trellis/guru-team/config.yml` 的新 scalar `base_branch`；空字符串代表未配置。
- 兼容入口：`base_branch_candidates` 去重后只有一个值时，该值按 config single-value 处理。
- Remote 名固定从 `--remote` 读取，省略时为 `origin`。

### 3.2 固定顺序

1. 显式 `--base`。
2. 非空 scalar `base_branch` 或单元素 `base_branch_candidates`。
3. `git ls-remote --symref <remote> HEAD` 返回的 remote default branch。
4. 在 `base_branch_candidates` 中筛选本地或 remote-tracking exact refs，去重后必须恰好一个。

每个 branch name 先通过 `git check-ref-format --branch`。Remote default 查询失败只进入第 4 步，不产生 current-branch fallback。第 4 步得到零个或两个以上候选时返回结构化 `blocked`。

`sync-base --resolve-only` 输出 resolution evidence，记录 `source`、selected base、remote、候选集合、decision checkout branch 与 `resolution_sha256`；不记录 repository absolute path。AI 必须在 fetch 前确认 invocation intent、resolution source 与 selected base。

`sync-base --execute --resolution-file <path> --expected-resolution-sha256 <digest>` 在执行边界重算 resolution。原始 bytes、digest 或重算结果任一不匹配均返回 `blocked`，不得 fetch 或修改 ref。

## 4. Sync state machine

### 4.1 前置 facts

Resolve-only 与 execute 从当前 invocation repository 读取：

- decision checkout branch；
- decision HEAD before；
- NUL-safe dirty status；
- selected local ref HEAD；
- selected remote-tracking ref locator。

Dirty 或 local ref 缺失在 fetch 前返回 `blocked`。Execute 还必须证明 AI 已确认的 resolution digest 与当前重算结果一致。

### 4.2 Fetch 与 fast-forward

1. 执行显式 refspec fetch：`git fetch --no-tags <remote> refs/heads/<base>:refs/remotes/<remote>/<base>`。
2. Fetch 非零或 remote ref 缺失返回 `blocked`。
3. Local 与 remote SHA 一致时不修改 local branch。
4. Local 是 remote ancestor 时，decision checkout branch 必须与 selected base 同名，然后执行 `git merge --ff-only <remote>/<base>`。
5. Local 不是 remote ancestor 时返回 `blocked`。
6. 非 selected-base checkout 不通过 `git branch -f` 修改 base；该路径返回 `blocked`。

### 4.3 Fresh equality

同步后重读：

- decision HEAD after；
- local base HEAD after；
- remote base HEAD；
- dirty status after。

四个条件必须同时成立：checkout 仍 clean、decision HEAD after 与 local HEAD after 一致、local HEAD after 与 remote HEAD 一致、三个 SHA 均为完整 commit id。否则 `fresh=false` 并返回 `blocked`。

## 5. Result 与 validator

### 5.1 Schema

新增 `schemas/base-sync-result.schema.json`，schema id 为 `guru-base-sync-result-1.0`。Success result 使用 closed object：

- `schema_version`、`skill_id`、`status`；
- `resolution`：source、selected base、remote、candidates；
- `decision_checkout`：branch、HEAD before/after、clean before/after；
- `git`：local/remote refs、HEAD before/after、fetch、fast-forward facts；
- `fresh`；
- `facts_sha256`。

`facts_sha256` 对去掉自身字段后的 canonical JSON bytes 计算 SHA-256。Example 只使用去身份化 branch/SHA，不写本机路径。

### 5.2 Evidence lifecycle

- `sync-base --resolve-only` 把 resolution JSON 输出到 stdout，并在 repo root 外写临时 resolution file。
- AI 在该 tool output 上确认 invocation intent 与 selected base。
- `sync-base --execute` 绑定 resolution bytes/digest，执行同步，把 result JSON 输出到 stdout，并在 repo root 外写临时 result file。
- Skill 在 result tool output 上执行最终 AI Review Gate。
- `check-base-sync` 读取 evidence，校验 component/symlink boundary、Draft 2020-12 schema、digest、selected refs 与当前 clean Git facts。
- Validator 不 fetch、不 fast-forward、不判断 route、scope、finding 或 semantic pass。
- Skill 删除临时 evidence 后返回 typed exit。

`skipped` 路径不运行 Git executor。AI Review Gate 确认 tool-free route 后，`check-base-sync --record-skipped <route-id>` 只生成并校验 stdout-only recorder facts；standalone mode 拒绝该入口。

## 6. Skill package 与 typed exits

Package 包含：

```text
guru-sync-base/
├── SKILL.md
├── interface.json
├── references/contract.md
├── scripts/sync-base.sh
├── scripts/check-base-sync.sh
├── schemas/base-sync-result.schema.json
├── examples/base-sync-result.json
└── tests/test_contract.py
```

两个 mode 的 `entry_precondition_ids` 完全一致：`invocation_intent`、`runtime_dependency`、`decision_checkout`、`selected_base_resolution`、`clean_checkout`、`result_evidence`。

| Exit | Consumer | 证据 |
| --- | --- | --- |
| `synced` | workflow route `guru-discover-change-context` | AI-reviewed、validator-passed fresh result |
| `skipped` | workflow route `original-request-route` | AI-reviewed route 与 stdout-only recorder facts |
| `blocked` | stop `base-sync-blocked` | resolution、Git、AI review 或 validator failure evidence |

`guru-discover-change-context` 在 #110 中仍指向现有 inline context discovery route；#111 把该 route 的内部实现替换成 mandatory public Skill，consumer id 不变。

Conditional human confirmation stage 的触发条件是 invocation intent 或 selected base 与用户请求冲突。该路径在 executor 前向用户确认；零候选、多候选或 stale resolution 仍返回 `blocked`，用户只能用显式 base 开始新 invocation。Workflow repo-changing route 与 standalone 显式请求已经提供无冲突 intent 时不再次询问。

## 7. Workflow integration

Phase 0 顺序调整为：

```text
tool-free request classification
  -> mandatory invoke guru-sync-base
  -> synced: guru-discover-change-context route
  -> skipped: original request route
  -> blocked: stop
```

`check-env`、`prepare-task`、issue read、duplicate search、Docs/code/tests/history discovery 均位于 `synced` 之后。Workflow 与 dogfood copy 使用完全相同的 unfenced markers。

## 8. `prepare-task` reuse

共享 core 替换 current-branch fallback 与 planner stale-only behavior：

1. `cmd_prepare` 在 `gh auth status`、issue read、duplicate search 前消费已由 Skill 确认的 resolution identity并运行 shared sync core，获得 initial fresh result。
2. Planner payload 继续在 `preflight.base_freshness` 暴露兼容字段，并新增 resolution、decision checkout 与三方 equality facts。
3. `--create-issue-confirmed` 在 GitHub mutation 前重跑 core。
4. `--create-worktree` / `--create-task` 在 worktree/task mutation 前重跑 core。
5. Task-start context 只保存 portable base/local/remote SHA，不保存完整 pre-task result或本机 path。

`refresh_base_freshness_for_planner` 与 `ensure_base_freshness` 保留为内部兼容 adapter，二者都调用新 core；旧 planner 不再把 `stale` 当成可继续 plan。

## 9. Distribution 与 public API

- Extension version 从 `0.6.5-guru.6` 升到 `0.6.5-guru.7`。
- `active_skill_ids` 加入 `guru-sync-base`。
- `artifact_schema_ids` 加入 `guru-base-sync-result-1.0`。
- `companion_scripts` 加入 `sync-base` 与 `check-base-sync`。
- Preset 安装 canonical package 到 `.trellis/guru-team/skills/`，并按 selected platforms 分发 shared、Codex、Cursor、Claude copies。
- Dogfood 使用 `apply.sh --repo . --all-platforms` 生成；不得手改 generated copies。
- Managed hash、`.new`、`.bak`、installed manifest 与 sidecar 规则沿用 #120/#125，不新增旁路。

## 10. 测试矩阵

### 10.1 Runtime unit tests

- 四级 resolution、每级 precedence、resolve-only digest 与 execute re-resolution binding。
- Remote default query success/failure。
- Fallback zero/one/multiple。
- Invalid branch、dirty、missing local、missing remote、fetch failure。
- Already fresh、behind + ff-only、diverged、wrong checkout、post-sync mismatch。
- Evidence path inside repo、symlink evidence、schema tamper、digest tamper、stale Git facts。
- `prepare-task` initial sync 发生在 issue read 前；executor rerun 发生在 mutation 前。

### 10.2 Package/distribution tests

- Interface mode parity、stage order、runtime commands、exit map。
- Missing/unknown/duplicate/unmapped marker fail closed。
- Source/installed package validation。
- Selected platform inventory、managed upgrade backup、unknown edit sidecar。
- Standalone wrapper 缺 runtime、drift runtime、完整 preset runtime 三类结果。

### 10.3 Integration gates

- Canonical unit suites 与 package tests。
- Preset installer tests。
- Dogfood apply、source/installed validation、overlay drift。
- Clean throwaway marketplace init/preview/switch、preset apply、standalone sync、workflow route、`trellis update`、workflow/preset reapply、零 sidecar。
- Branch push 后执行 remote marketplace verifier，再进入 finish-work。

## 11. Docs SSOT Plan

- `docs_state`: `partial_docs`
- `strategy`: `ssot_first`
- 原因：本任务改变 Phase 0 顺序、public Skill API、config、schema、runtime commands、installer inventory 与 upgrade contract。
- 实现前更新：`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、`.trellis/spec/workflow/index.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/docs/public-docs.md`。
- 实现后同步：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- Task delta merge：四级 resolution、三方 equality、evidence lifecycle、typed exits、prepare reuse、distribution 与验证矩阵必须进入 durable contracts。
- Merge checkpoint：任何 runtime/schema/package 代码落地前先完成 durable docs/spec；Phase 2 check 复核 docs、workflow、package、runtime、preset、dogfood 与 tests 一致。
- Task-history-only：issue 检索过程、Phase 0 命令输出、临时 evidence、sub-agent liveness、逐轮 finding 保留在 task artifacts，不进入 public package。

## 12. 兼容性、回滚与安全

- Stable workflow id、preset path、既有 Skill id 与既有 companion command 不改名。
- `base_branch_candidates` 继续受支持；多值配置进入 remote-default/fallback 解析，不再按第一个 existing ref静默选择。
- 回滚采用 Git revert 与上一 extension ref 重新应用 workflow/preset；installer 不自动选择 `.new`/`.bak` 内容。
- 本任务不新增服务、数据库、migration、容器、Kubernetes、queue、schedule、CI/CD pipeline 或 Makefile target。
- 日志与 artifacts 不得包含 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或本机绝对路径。

## 13. 需求追踪

| PRD | 设计 | 实现计划 | 验收 |
| --- | --- | --- | --- |
| Public Skill 与 mode parity | 第 2、6、9 节 | 第 2、3、6 步 | AC1、AC2、AC3 |
| 四级 base resolution | 第 3 节 | 第 2、4 步 | AC5 |
| Safe sync 与三方 equality | 第 4、5 节 | 第 4 步 | AC4、AC6、AC7 |
| Workflow first action 与 exits | 第 6、7 节 | 第 3 步 | AC2、AC3、AC4 |
| `prepare-task` reuse | 第 8 节 | 第 4 步 | AC8 |
| 分发、dogfood、update | 第 9、10 节 | 第 5、7、8 步 | AC9、AC10 |
| Docs、安全、部署 | 第 11、12 节 | 第 1、7、8 步 | AC10、AC11 |
