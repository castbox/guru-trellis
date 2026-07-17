# #114 设计：合同措辞审查 closed-loop Skill 与旧实现迁移

## 1. 设计目标

把 #93 的 planning-only scanner 迁移为 `guru-review-contract-wording` 独占的 step-local semantic Skill，同时保持 planning start gate 的可审计阻塞行为。迁移完成后的所有 durable consumer 只依赖 stable Skill id、profile、evidence schema 和 typed exit，不再展开词表、分类或内部闭环。

## 2. 所有权模型

| 层 | 唯一职责 | 不拥有 |
| --- | --- | --- |
| Global workflow | mandatory invocation、profile route、typed-exit consumer、fail-closed stop | 词表、分类细则、rewrite/review loop、scanner 内部步骤 |
| Canonical Skill package | profile contract、vocabulary/classification semantic SSOT、AI rewrite/review、confirmation policy、evidence 与 exits | Git/worktree/task/publish 流程 |
| Shared runtime | fixed scope construction、UTF-8 scan、hash/digest、schema/whitelist/unchecked/freshness validation | classification 选择、rewrite、reason 充分性、semantic pass/block |
| Planning approval consumer | post-planning user confirmation、三份文档审批 digest、经验证 wording evidence 投影 | controlled-term/scanner/classification owner |
| Platform discovery copies | 发现并加载 canonical package | step-local contract 副本 |

## 3. Canonical package

新增目录 `trellis/skills/guru-team/packages/guru-review-contract-wording/`：

```text
SKILL.md
interface.json
references/contract.md
schemas/contract-wording-review.schema.json
examples/contract-wording-review.json
scripts/record-contract-wording-review.sh
scripts/check-contract-wording-review.sh
tests/test_contract.py
```

`registry.json` 增加 active entry，`interface.json` 使用 schema `1.2`，声明：

- `judgment_mode=semantic`；
- workflow/standalone 相同 entry preconditions；
- ordered stages 为 `forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`；
- runtime commands 为 `record-contract-wording-review` 与 `check-contract-wording-review`；
- result schema id 为 `guru-contract-wording-review-1.0`；
- exits 仅为 `pass`、`content_changed`、`blocked`。

Package scripts 保持 dispatcher-only，通过 `run-skill-command` 调用 installed shared runtime。Public package 不携带 active task、workspace journal、platform prompt、本机路径或业务私有状态。

## 4. Profile 与 scope builder

### 4.1 `change_request`

固定输入为一个 live issue 或 side-effect-free draft：

- title 与 body 始终进入 scope；
- authoritative comments 由 AI 在 review 前选择，evidence 记录 comment stable id、author、updated time、selection reason 和 content hash；
- 未被选中的 comments 不作为 contract authority，选择集合本身进入 scope digest；
- 调用方不能传 field selector 排除 title/body。

Issue/draft mutation 后返回 `content_changed`。Live GitHub mutation 必须继承现有 exact payload confirmation、preimage match、mutation evidence 和 live reread 边界；draft mutation保持 side-effect-free reviewed bytes。

### 4.2 `planning_artifacts`

Scope builder 从 current active task identity 推导且只接受：

```text
{TASK_DIR}/prd.md
{TASK_DIR}/design.md
{TASK_DIR}/implement.md
```

三者均为 required regular files。Caller 不能传路径集合、排除项或 alias。每个文件记录 repo-relative path、size、SHA-256；scope digest 同时绑定 task identity 和排序后的三项 identity。

Passed evidence 持久化为 `{TASK_DIR}/contract-wording-review.json`，供 planning approval consumer 使用。Artifact 必须 tracked、task-local、未被 ignore；旧内容不同则不覆盖，除非本轮是同一 profile 的明确 re-entry 且旧 evidence 已被新内容 hash 判定 stale。

### 4.3 `explicit_paths`

Scope 仅来自用户本轮明确指定的 repo-relative `.md` regular files：

- 拒绝 absolute path、parent traversal、非 Markdown、缺失、symlink 和 repo 外路径；
- evidence 记录用户指定的规范化 path set 与 hash；
- workflow 的 `change_request`/`planning_artifacts` consumer 禁止调用本 profile；
- standalone result 通过 stdout 返回，不写固定 repo cache。

## 5. Shared vocabulary 与 scanner

Shared runtime 新增 generic `CONTRACT_WORDING_VOCABULARY_V2` 和 `CONTRACT_WORDING_CLASSIFICATIONS_V1` 常量。Canonical Skill contract 给出这两个 version 的完整人类可读定义；workflow、README、spec consumer 和平台入口只引用 version，不复制内容。

旧 `PLANNING_AMBIGUITY_*` 常量、`scan_planning_normative_language()`、`parse_planning_normative_hit_*()`、`planning_normative_language_*()` 在 replacement verification 后删除。Generic scanner 接收 scope builder 的 normalized items，不知道 planning approval：

1. 对 Markdown/file field 按 UTF-8 行扫描；issue/draft title/body/comment 按稳定 field + 1-based line 扫描。
2. 同一 location 中每个 vocabulary term 产出一个 hit fact。
3. Hit identity 绑定 `scope_item_id + field/path + line + term + content_sha256`。
4. Scanner 输出 objective `term/location/text/hash`，不写 classification/reason。
5. 输出顺序由 scope item order、line、vocabulary order 固定。

## 6. Semantic loop

Skill 按以下顺序执行：

```text
validate entry/profile
  -> build fixed scope + hashes
  -> deterministic scan
  -> AI rewrite weak contract clauses
  -> AI classify retained lexical hits with reason
  -> if content changed: rebuild scope + rescan
  -> AI Review Gate
  -> conditional mutation confirmation when required
  -> recorder + checker
  -> one typed exit
```

AI Review Gate 固定覆盖以下六项：

- required profile scope 未被缩小；
- 每个 current hit 有 classification 与非空 reason；
- `unchecked_normative_hits=[]`；
- rewrite 没有改变未经用户确认的产品语义；
- retained classification 与 current text、触发条件、确定值或引用对象一致；
- 零 hit 没有被当作完整 requirement review 的替代证据。

Classification 固定为 issue #114 声明的九项：`contract_violation`、`quoted_source_non_contract`、`term_definition`、`literal_identifier`、`historical_record_non_contract`、`deterministic_threshold`、`deterministic_default`、`deterministic_option`、`deterministic_reference`。任何未分类或 `contract_violation` 均进入 unchecked 并阻塞 `pass`。

## 7. Evidence schema

`guru-contract-wording-review-1.0` 是 closed Draft 2020-12 object，核心结构如下：

```json
{
  "schema_version": "1.0",
  "skill_id": "guru-review-contract-wording",
  "profile": "planning_artifacts",
  "mode": "workflow",
  "vocabulary_version": "contract-wording-v2",
  "classification_version": "contract-wording-classifications-v1",
  "scope": {
    "items": [],
    "scope_sha256": "<sha256>"
  },
  "scan": {
    "hits": [],
    "scan_sha256": "<sha256>"
  },
  "semantic_review": {
    "revisions": [],
    "classifications": [],
    "unchecked_normative_hits": [],
    "ai_review_gate": {}
  },
  "human_confirmation": {},
  "typed_exit": "pass",
  "facts_sha256": "<sha256>"
}
```

详细合同：

- `scope.items[]` 使用 profile-discriminated closed item；file item 记录 path/hash/size，change-request field 记录 issue/draft/comment identity 与 field hash。
- `scan.hits[]` 保存全部客观命中；`semantic_review.classifications[]` 用 hit identity 关联，禁止靠 path/line 的模糊匹配。
- `revisions[]` 记录 locator、before/after hash、AI reason、mutation authority 与重扫 identity，不把旧 scan 当成 current result。
- `unchecked_normative_hits[]` 由 recorder 从 current hits/classifications 确定性派生。
- `ai_review_gate` 保存 reviewer、summary、checked dimensions、status 与 reviewed scan identity；scripts 校验 shape/binding，不判断 summary 充分性。
- `facts_sha256` 覆盖除自身外的 canonical JSON。
- `typed_exit=blocked` 当且仅当 Gate blocked；`pass` 要求 current scope、零 unchecked、Gate passed、无未消费 revision；`content_changed` 要求一条或多条授权 revision、after hash/current scan 一致且 Gate passed。

## 8. Recorder/checker 与命令

Runtime 新增 generic helpers，并通过 extension manifest 发布：

```text
record-contract-wording-review
check-contract-wording-review
```

Recorder：

- 接收 profile scope facts、AI-authored classification/revision/Gate、human confirmation evidence；
- 重建 scope 与 scanner facts，拒绝 unused/duplicate/stale hit identity；
- 派生 unchecked、scope/scan/facts digests；
- `planning_artifacts` 只写 current task-local artifact，其他 profile stdout-only。

Checker：

- 执行 published schema validation；
- 重新构造固定 scope、重新扫描、重算 digests；
- 校验 classification whitelist、reason 非空、hit completeness、unchecked、Gate/exit invariant；
- 不接受 caller-provided selector 取代 profile builder；
- 返回 artifact 中已经声明的 exit，不自行选择 route intent。

## 9. Typed exit routing

Interface 为每个 exit 声明唯一 consumer：

| Exit | 唯一 consumer | Profile-aware 固定映射 |
| --- | --- | --- |
| `pass` | `guru-contract-wording-pass-router` | `change_request` -> full task intake continuation；`planning_artifacts` -> planning artifact presentation/approval；`explicit_paths` -> standalone caller |
| `content_changed` | `guru-contract-wording-change-router` | `change_request` -> base/context refresh；`planning_artifacts` -> complete planning review re-entry；`explicit_paths` -> standalone wording re-entry |
| `blocked` | `contract-wording-blocked` stop | 所有 profile 均停止并报告 evidence/reason |

Router 只读取 checker 已验证的 profile/exit，不重新选择 classification、scope 或产品 route。Unknown profile、multiple exit、missing consumer 或 stale result fail closed。

## 10. Planning approval adapter

`record-planning-approval` 保持 post-planning user confirmation owner，但接口迁移为消费 `{TASK_DIR}/contract-wording-review.json`：

- 新 evidence 必须是 `profile=planning_artifacts`、`typed_exit=pass`、current scope/hash、zero unchecked、passed Gate；
- planning approval 继续记录 reviewer、summary、checked dimensions、三份 reviewed/approved digests 和 `user_confirmation.source=explicit-post-planning-review`；
- `ambiguity_review.normative_language` 如需保持现有审计 shape，只能从 verified wording evidence deterministic projection，不再从 `--normative-hit` 重建规则；
- 同时绑定 wording artifact path、schema id、content digest、scope digest 和 scan digest。

`check-planning-approval` 先调用 generic wording checker，再核对 planning approval projection 与 evidence identity，最后校验用户确认和三份 planning doc digests。Phase 2、active-task scope change、task commit 和 Branch Review 使用同一个 planning approval validator，因此仍得到 #93 blocking semantics。

迁移规则：

- 不修改 archived `planning-approval.json`；
- 新 recorder 不再暴露 active `--normative-hit` usage；
- 当前 active task 若只有 pre-#114 approval，下一次进入实现前重新执行 `planning_artifacts` Skill、展示三份文档并取得 fresh post-planning confirmation；
- package/durable docs 明确旧 flag 到新 evidence locator 的迁移命令。

## 11. Replacement-first 删除顺序

1. 新增 package/schema/runtime/commands/tests，不改旧 consumer 行为。
2. 运行三个 profile、evidence、routing、installed package tests。
3. 将 planning approval 切换到新 evidence，并运行 #93 全量 compatibility regression。
4. 将 workflow/durable docs/spec/platform discovery 改为引用 Skill。
5. 证明新链路通过后删除旧 planning constants/helpers/flag usage/full rule copies。
6. 执行 repo-wide search，确认 active source 无第二 owner；随后运行 dogfood、throwaway、update/reapply 验证。

第 2 或第 3 步失败时停止删除并返回修订。最终分支不能同时保留两条 active scanner/classification owner path。

## 12. Docs SSOT Plan

- Docs state: `stale_docs`
- Strategy: `ssot_first`
- Strategy reason: 长期 workflow/Skill/data/installer contract 发生所有权迁移，durable SSOT 必须先改为新 Skill 引用，再据此完成 consumer 和 runtime 删除。
- Affected durable sources:
  - `trellis/skills/guru-team/packages/guru-review-contract-wording/references/contract.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
- Task delta merge: profile、schema、routing、planning migration、legacy deletion 与 verification matrix 写回上述 durable sources。
- Task history only: issue intake、旧代码定位、临时测试输出、每轮 deletion search 结果。
- Merge checkpoint: Phase 2 final check 前完成 canonical/dogfood/docs/spec 同步；Branch Review 再复核 active source 无旧 owner。

## 13. 分发与 upgrade/update

- Preset installer 从 registry 安装 canonical package 到 `.trellis/guru-team/skills/packages/` 以及 shared/Codex/Cursor/Claude discovery roots。
- Extension manifest/public API 增加两个 runtime commands 与 result schema id。
- Canonical package 变化后运行 preset apply 同步 dogfood，再运行 overlay/package drift check。
- Throwaway repo 先通过官方 workflow marketplace 命令安装 `guru-team` workflow，再应用 preset；只使用 installed assets 执行三个 profile 的 package/command smoke test。
- 在 throwaway repo 运行目标 Trellis 版本的 `trellis update`，随后 reapply preset；校验 workflow route、package inventory、manifest command、platform copies 与 evidence checker 仍一致。
- `.new`/`.bak` 必须逐项解释和处理；未处理项使开箱即用或 update gate 失败。

## 14. 测试设计

### Package/runtime

- interface/frontmatter/registry/route/schema inventory；
- 三 profile positive scope 与 selector-shrink rejection；
- v2 vocabulary 全词命中和九类 classification；
- unclassified、unknown、empty reason、`contract_violation` blocking；
- content change -> new hash/rescan；stale/partial/duplicate/unused hit rejection；
- Gate/exit biconditional 与 three-exit router mapping；
- workflow/standalone precondition equality。

### #93 compatibility

- planning scope 恒为三文件；
- 全部 hits 投影与 zero unchecked；
- planning docs 变化使 wording + approval stale；
- missing/non-pass evidence 阻塞 record/check；
- post-planning confirmation 保持 required；
- Phase 2 与 Branch Review consumer 仍调用 shared planning validator；
- archive 不迁移，active legacy approval 返回明确 re-review 错误。

### Distribution

- source/installed `check-skill-packages`；
- preset installer inventory/managed hash/platform copies；
- dogfood apply + drift；
- clean throwaway workflow/preset install；
- `trellis update` + preset reapply；
- repo-wide negative grep 证明旧 owner 与完整规则副本已消失。

## 15. 安全、部署与回滚

- 不涉及服务部署、容器、Kubernetes、DB migration 或 Makefile。
- Evidence 不写 token、secret、`.env`、private key、签名 URL 或客户数据。
- Change request 只记录审查需要的 issue/draft field/hit/revision facts；不持久化无关 comment 或 raw runtime output。
- 回滚以单个任务 commit/PR revert 恢复 pre-#114 状态；删除旧实现前的新链路验证是同一变更的强制 gate，不采用长期双写或双 scanner 回滚方案。
