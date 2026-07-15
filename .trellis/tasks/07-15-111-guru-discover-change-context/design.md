# #111 `guru-discover-change-context` 技术设计

## 1. 设计目标

本设计把 Phase 0 现有 inline context discovery route 收敛为公共 semantic Skill。Global workflow 只拥有 mandatory invocation、跨 Skill transition 与 typed exit consumer；package 独占 current-state 审查、history preview、AI Review Gate、snapshot record/check 与 refresh 合同。

## 2. SSOT 与责任边界

| 层 | SSOT | 责任 | 禁止事项 |
| --- | --- | --- | --- |
| Global workflow | `trellis/workflows/guru-team/workflow.md` | Phase 0 顺序、mandatory invocation、typed exit consumer、fail-closed stop | 复制 step-local Skill 正文 |
| Canonical package | `trellis/skills/guru-team/packages/guru-discover-change-context/` | modes、preconditions、语义阶段、artifact、validators、exits、re-entry | 携带 task 私有状态或平台 prompt |
| Shared deterministic runtime | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与 Bash wrappers | canonicalization、history preview、digest、schema、record、live check | 判断 relevance、sufficiency、candidate 选择或 reuse/new target |
| Preset installer | `trellis/presets/guru-team/` | canonical bytes 安装、platform discovery、manifest、mode、conflict 与 sidecar | 依据内容启发式覆盖用户文件 |
| Durable docs/spec | `docs/requirements/**`、`.trellis/spec/**`、README | 公共行为、数据、安装、升级与作者合同 | 记录当前 task 执行日志 |
| Task artifact | `{TASK_DIR}/context-discovery.json` | 经 AI Gate 审查并经 validator 绑定的当前快照 | 成为共享索引或跨 task 可变状态 |

## 3. Package 与公共 API

Canonical package 目录：

```text
trellis/skills/guru-team/packages/guru-discover-change-context/
├── SKILL.md
├── interface.json
├── references/contract.md
├── examples/context-discovery.json
├── schemas/context-discovery.schema.json
├── scripts/
│   ├── preview-change-context-history.sh
│   ├── record-context-discovery.sh
│   └── check-context-discovery.sh
└── tests/test_contract.py
```

新增稳定公共命令：

- `preview-change-context-history`
- `record-context-discovery`
- `check-context-discovery`

新增 artifact schema id：`guru-context-discovery-1.0`。Scoring algorithm id 固定为 `guru-context-history-score-1.0`。上述 id、command 与 exit id 属于团队公共 API；破坏性语义调整必须新建版本 id 或提供迁移合同。

## 4. Modes 与一致 preconditions

`workflow` 与 `standalone` 声明同一组 preconditions：

1. `runtime_dependency`：完整 Guru Team preset、installed manifest、shared dispatcher、active package inventory 均通过 installed validation。
2. `fresh_base`：输入包含 validator-passed `guru-base-sync-result-1.0`、selected base、decision checkout、base HEAD、remote HEAD 与 `post_sync_resolution_sha256`；live Git 必须保持 clean 且三方 SHA 一致。
3. `repository_identity`：repo root、remote owner/repo 与 base ref 必须能确定性解析，持久化字段只保存 portable repo identity。
4. `change_input`：输入必须归一为 issue、request、paths、commands、config keys、schema fields、symbols 中一个非空 clue 集合。
5. `evidence_freshness`：live issue/draft digest、reviewed Git blobs、query digest、archive manifest digest 与 snapshot digest 必须匹配 validator 重读事实。

Workflow mode 的输入来自 `guru-sync-base:synced`、用户请求和 live issue/proposed draft。Standalone mode 由直接调用者提供相同结构化输入。任何 precondition 失配都在语义读取前产生 `refresh_base` 或 `blocked`，不得降级为旧 checkout 搜索。

## 5. 闭环状态机

```text
fresh-base-check
  -> live-change-and-duplicate-facts
  -> current-docs-review
  -> current-code-contract-review
  -> current-test-review
  -> canonical-query-clues
  -> one-history-preview
  -> candidate-selection-and-deep-read
  -> ai-review-gate
  -> conditional-human-confirmation(not_required)
  -> stdout-recorder-and-validator
  -> context_ready | refresh_base | blocked
```

### 5.1 Forward behavior

- Base validator 必须先通过。
- Live issue 读取必须记录 `repo`、`number`、`url`、`state`、`updated_at`、body digest 与 facts digest；无 issue 时记录 proposed draft digest，且不写 GitHub。
- Duplicate search 必须只查询 open issues，记录 query、checked_at、candidate facts digest 与 AI reasons。
- AI 必须先审查 durable Docs SSOT，再审查 code/API/config/schema/ownership，最后审查 tests/fixtures/throwaway/update evidence。
- Current review 每个 evidence row 必须包含 repo-relative path、Git blob id 或 content digest、review purpose、observation 与 query clues。
- Current observations 完成后，只执行一次 history preview command。

### 5.2 AI Review Gate

Gate 必须逐项记录：

- reviewed scope 与明确未覆盖面；
- current evidence relevance 与 sufficiency；
- duplicate/history conflict；
- 可复用机制、不可复用机制与理由；
- 每个 load-bearing conclusion 的 evidence refs；
- findings、severity、resolution 状态；
- `passed` 或 `blocked` 结论与原因。

Script 不得生成上述结论。Recorder 只接受 AI 已提供的结构化结论并执行 schema、identity、digest 与 live freshness 校验。

### 5.3 Conditional human confirmation

本 Skill 不拥有 duplicate reuse/new target 决策，因此该阶段固定记录 `status=not_required` 与 `reason=decision_owned_by_guru-clarify-requirements`。若 evidence 无法在不作产品选择的前提下形成安全结论，Skill 返回 `blocked`；不得在本阶段代替下游询问或决定。

## 6. Canonical query 与 scoring

### 6.1 Query shape

Canonical query 使用固定字段：

```json
{
  "issue_refs": [],
  "pr_refs": [],
  "branches": [],
  "paths": [],
  "commands": [],
  "config_keys": [],
  "schema_fields": [],
  "symbols": [],
  "terms": [],
  "queries": [],
  "tokens": []
}
```

Canonicalization 规则：

- 所有数组先拒绝非字符串、空字符串、NUL 与 control characters。
- Issue/PR refs 归一为 `#<positive-integer>` 与 `PR #<positive-integer>`。
- Repo-relative paths 使用 POSIX slash，拒绝 absolute、`..`、symlink component 与受保护前缀；exact identity 保留大小写和标点。
- 其它文本执行 Unicode NFKC、casefold、首尾空白删除、内部空白折叠；按 canonical value 去重后字节序排序。
- `terms` 是结构化短词线索；`queries` 是完整 request/query 文本。两者不得互相替代。
- Tokens 从 `terms`、`queries` 和其它文本 clues 的 NFKC/casefold 值按非 letter/number 边界、snake/kebab/path separators 与 camel-case transition 拆分；长度小于 2 的非数字 token 删除。
- Canonical JSON 使用 UTF-8、sorted keys、紧凑 separators 与终止换行；其 SHA-256 为 `query_sha256`。

### 6.2 Exact/token score

每个 candidate 只使用 `finish-summary.json:index.*`。Unique exact match 权重固定为：

| Clue kind | Points |
| --- | ---: |
| `issue_refs` | 1000 |
| `pr_refs` | 900 |
| `branches` | 800 |
| `paths` | 700 |
| `commands` | 600 |
| `config_keys` | 600 |
| `schema_fields` | 600 |
| `symbols` | 600 |
| `terms` | 400 |
| `queries` | 300 |

`terms` exact match 的 candidate 集合是 `index.search_terms.*` 全部 canonical scalar values 与 `index.retrieval_text` canonical tokens；`queries` exact match 使用 `index.retrieval_text` 的 normalized phrase containment。`token_points = min(99, unique_query_tokens_present_in_index_retrieval_text)`。`total_score = exact_points + token_points`。一条 clue 在一个 candidate 内只计分一次；同值跨 kind 按各 kind 单独计分。其它 exact match 使用同名 `index.search_terms` kind 的 canonical identity；token match 只读取 `index.retrieval_text` 的 canonical tokens。

固定排序键：

1. `total_score` 降序；
2. `exact_match_count` 降序；
3. `token_match_count` 降序；
4. `finish_summary_path` UTF-8 字节序升序。

Projection 固定保留前 20 个 `total_score > 0` candidates。每个 row 只含 candidate id、repo-relative summary path、index digest、score breakdown、matched clues、`problem`、`outcome`、`changed_behavior`、受影响 surface 投影、contract change 投影与 search terms 投影。

## 7. Archive manifest、invalid isolation 与 preview digest

History engine 递归枚举且只打开 `.trellis/tasks/archive/**/finish-summary.json`。对每个路径：

- 先执行 repo-root containment、component `lstat`、regular-file 与 non-symlink 检查；
- 解析 JSON 后只提取 `index`；不消费 `task`、`git`、`github`、`artifacts` 或其它 sibling fields；
- 以 `context-discovery.schema.json` 内嵌的 index projection contract 校验所需 shape；
- Valid entry 记录 `{path,status=valid,index_sha256}`；invalid entry 记录 `{path,status=invalid,error_code}`，不记录原始异常文本或文件内容。

`archive_manifest_sha256` 由按 path 排序的 manifest rows 计算。Invalid rows 不参与 candidate score，但必须进入 preview evidence。一个 invalid row 不阻断其余 valid rows；AI Review Gate 必须判断 invalid coverage 是否使 load-bearing conclusion 不充分。

`preview_sha256` 绑定 algorithm id、query digest、archive manifest digest、limit、排序后的 candidate projections 与 invalid rows。相同 archive/query 输入必须产生字节一致的 preview。

## 8. Candidate deep-read 与 mem gate

- `candidate_count > 0` 时，AI 必须选择 1 至 `min(3, candidate_count)` 个 candidates。
- `candidate_count = 0` 时，selection 固定为空，流程直接进入 AI Review Gate。
- 每个未选择 candidate 必须记录 `excluded_reason`；每个所选 candidate 必须记录 `selected_reason`。
- Deep-read 只能读取所选 archived task 内明确列出的 artifact、具体 GitHub issue/PR 或具体 Git commit/diff；每次读取都记录 source、portable locator、purpose 与 conclusion。
- 不得枚举或全文读取所选 task 的整个目录。
- Mem gate 的触发条件是：task artifacts、current Docs/code/tests、GitHub 与 Git history 四类来源均已记录 insufficiency，且仍存在一个命名的 load-bearing question。未满足该布尔条件时不得调用 `trellis mem`。
- Artifact 只持久化 mem 的 portable summary、触发原因与 load-bearing conclusion，不持久化本机会话路径、完整对话或 private raw text。

## 9. Result schema 与 same-snapshot persistence

`guru-context-discovery-1.0` 是 closed union，公共字段包括：

- `schema_version`、`generated_at`、`mode`、`typed_exit`；
- `repository`、`base_evidence`、`change_input`、`live_change`、`duplicate_search`；
- `current_state`、`canonical_query`、`history_preview`、`history_review`、`mem_review`；
- `ai_review_gate`、`human_confirmation`、`refresh_history`；
- `snapshot_identity`，含 query、manifest、facts、payload 与 snapshot SHA-256。

`context_ready` 分支必须含完整 current/history/Gate evidence。`refresh_base` 分支必须含 stale reason、superseded query/snapshot digests 与时间。`blocked` 分支必须含 stable error codes 与 non-secret summary。

Pre-task recorder 从 stdin 接收 AI 已审查 payload，canonicalize 后把 result 和 `snapshot_sha256` 输出到 stdout，零 repo 写入。Validator 从 stdin 或明确 input file 读取同一 bytes，复核 schema、digest、fresh Git、live issue/draft 与 archive manifest。

Task 创建后的 recorder 必须接收同一 canonical bytes 及 `--expected-snapshot-sha256`，只写 `{TASK_DIR}/context-discovery.json`。写入前后均验证 task-local path、target absence 或 exact same bytes、HEAD 仍是 snapshot base HEAD、全部 tracked dirty paths 均位于该新 task 目录、query/manifest/live identity 未变。Proposed draft 后续已创建 issue 时，只验证 reviewed draft digest 与新 issue body digest 一致，不改写原 snapshot 的 draft identity。任何差异失败并保留现状，不生成 `.new`、`.bak`、repo cache 或 workspace state。

## 10. Typed exits 与 re-entry

| Exit | 条件 | 唯一 consumer |
| --- | --- | --- |
| `context_ready` | AI Gate passed，stdout snapshot 与 live validator 通过 | workflow route `guru-clarify-requirements` |
| `refresh_base` | base、issue、reviewed blob、query 或 archive manifest binding stale | Skill `guru-sync-base` |
| `blocked` | invalid input、unsafe path、schema/contract failure 或 AI Gate 无法安全通过 | stop `change-context-blocked` |

Re-entry identity 绑定 mode、repository、base post-sync digest、change input digest、live issue/draft digest、query digest、archive manifest digest 与 superseded snapshot digest。`refresh_base` 返回 `guru-sync-base` 后，workflow 必须以新的 `synced` evidence 重新调用整个 Skill；不得从 history preview 或 AI Gate 中段继续。

## 11. Docs SSOT Plan

- `docs_state`：`partial_docs`。
- Evidence paths：`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、`.trellis/spec/workflow/index.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/preset/upstream-ownership.md`、`.trellis/spec/docs/public-docs.md`、`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- `strategy`：`ssot_first`。
- Strategy reason：本任务改变 Phase 0 长期流程、公共 Skill/exits/schema/commands、artifact persistence、history data contract 与安装升级行为；代码必须以先完成 durable contract 为前提。
- Affected durable docs：上述 requirements、workflow/preset/docs specs 与三个公开 README；`.trellis/spec/preset/upstream-ownership.md` 只补充新 `guru-*` package 属于 anchored `guru_owned` namespace 的既有规则应用，不新增 legacy path。
- Task delta to merge：fixed order、mode parity、freshness、scoring、manifest/preview digest、invalid isolation、deep-read/mem gate、same-snapshot persistence、typed exits 与 no-workspace/no-cache 边界。
- Merge checkpoint：实现代理必须先更新 durable docs/spec，再修改 schema/runtime/package/workflow/preset；Phase 2 check 必须核对 docs、interface、schema、code、tests 与 installed behavior 一致。
- Task-history-only：本次候选 #120/#110/#97 的选择理由、当前 task 执行记录与 gate evidence 只留在 task 目录。

## 12. Workflow、preset 与 ownership 集成

- Canonical workflow 在 `guru-sync-base:synced` 后 mandatory invoke新 Skill，并声明三个 exit markers。
- Dogfood `.trellis/workflow.md` 由 canonical workflow 同步。
- Registry 与 extension manifest 增加 active id、artifact schema、runtime commands、managed paths 与 patch version。
- Preset installer 复用现有 exact managed hash 状态机，安装 `.trellis/guru-team/skills/`、`.agents/skills/guru-*` 以及 selected platform `guru-*` copies。
- `.agents/skills/trellis-start/**`、`.codex/prompts/**` 与 `.codex/skills/trellis-start/**` 属于 frozen transitional legacy；本任务不改 payload、不扩 path、不调整 ownership inventory。
- Preset apply 后必须运行 dogfood overlay drift 与 upstream ownership validator；任何 legacy baseline drift、unclassified path 或 sidecar 均阻塞。

## 13. 测试设计

### 13.1 Unit 与 contract

- Query normalization：Unicode、case、duplicate、path punctuation、unsafe path、control character。
- Score：每个 exact kind、token-only、duplicate clue、zero score、tie sort、limit 20、input order permutation。
- Manifest：valid、malformed JSON、missing index、bad shape、symlink、path escape、mixed valid/invalid、manifest digest stability。
- Result schema：三 exit union、semantic Gate、human confirmation not-required、refresh history、portable locator、secret/path rejection。
- Package：mode parity、semantic stage profile、runtime dependencies、wrappers、schema/tests/exit markers。

### 13.2 Integration

- Fresh and stale base，且 stale 在 issue/Docs/history read 前阻塞。
- Live issue 与 proposed draft 两条输入支路。
- Current-state 三层审查完成后 history command 仅执行一次。
- 有候选选择 1、2、3 个与排除理由；零候选成功且 mem 未调用。
- Mem gate 的四类 insufficiency 全满足与任一不满足两组事实。
- Pre-task stdout repo zero-write 与 post-task exact same snapshot record/check。
- Query/archive/live issue drift 产生 `refresh_base` 并记录 superseded digests。

### 13.3 Distribution 与 upgrade

- Source/installed skill validation、selected platform copies、executable mode、managed upgrade、unknown local edit、platform shrink。
- Canonical preset apply、dogfood drift、upstream ownership、zero sidecar。
- Clean throwaway marketplace init/preview/switch、preset apply、direct discovery、workflow route、record/check、`trellis update --force`、workflow/preset reapply。

## 14. 兼容、升级与回滚

- 既有 `guru-sync-base` id、exits、commands 与 result schema 不变；只把其 `synced` consumer 从 inline route 激活为 active Skill invocation。
- `finish-summary.json:index` schema 不变，history engine 对既有 backfill summary 使用同一 reader。
- Extension patch version递增；旧安装缺 package/runtime/schema 时 direct invocation 必须 fail closed 并提示重装完整 preset。
- Unknown local edit 保留原文件并产生 `.new`；known managed upgrade 产生 `.bak` 后安装 canonical bytes；所有 sidecar 必须在发布前处理。
- 若 workflow 已接入而 package/distribution/validator 未通过，回滚 workflow markers 与 registry activation，不发布半安装状态。
- 若 history engine 读取 index sibling、workspace、runtime 或 repo cache，立即停止并删除越界实现，重新执行全套安全测试。
- 若 legacy overlay payload 发生 drift，回滚该 drift，保留只通过 `guru-*` canonical/package namespace交付的方案。

## 15. 需求追踪

| PRD | 设计 | 实现计划 | 验收 |
| --- | --- | --- | --- |
| R1 | 2、3、5 | 3 | AC1、AC9、AC11 |
| R2 | 4、10 | 4 | AC2 |
| R3 | 5 | 4、5 | AC3、AC9 |
| R4 | 5.1、5.3 | 4 | AC4 |
| R5 | 6、7 | 5 | AC5、AC6 |
| R6 | 8 | 4、5 | AC7、AC8 |
| R7 | 9、10 | 5、6 | AC10、AC15 |
| R8 | 10 | 3、6 | AC11 |
| R9 | 11、12 | 2、3、6、7 | AC12、AC13 |
| R10 | 13、14 | 8、9 | AC14、AC15、AC16 |
