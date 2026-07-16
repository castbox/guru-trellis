# #111 `guru-discover-change-context` 闭环 Skill

## 1. 目标

在 Guru Team 扩展中交付公共语义 Skill `guru-discover-change-context`。该 Skill 必须在 fresh base 上先审查当前 Docs SSOT、代码/API/config/schema、测试与现有行为，再检索 archived task 的 `finish-summary.json:index.*`，形成可供 `guru-clarify-requirements` 消费的变更上下文快照。

本任务只关闭 [castbox/guru-trellis#111](https://github.com/castbox/guru-trellis/issues/111)。父 issue、前置合同、被阻塞任务和已完成历史合同只作为上下文，不进入关闭范围。

## 2. 已确认依据

- Live issue #111 定义了 Skill id、两种调用模式、固定执行顺序、history engine、三个 typed exits、task-local artifact 与脚本边界。
- 官方 Trellis 文档确认 `.trellis/workflow.md` 是 workflow 运行合同，公共外部 Skill 由 Guru Team preset 分发，spec template 不承载 active task 或运行态。
- `.trellis/spec/workflow/skill-package-contract.md` 已定义 public Skill registry、interface schema 1.2、semantic 五阶段、mandatory invocation marker、typed exit 唯一 consumer、shared dispatcher 与 managed-hash 分发。
- `.trellis/spec/workflow/workflow-contract.md` 明确当前 `guru-discover-change-context` 仍是 inline route，#111 负责激活 canonical package 与 mandatory route。
- #97 与 #100 已建立 task-local `finish-summary.json` 及历史回填；#105 保证已归档 summary 保留 canonical PR URL 与 `pr_refs`；#53 与 #96 禁止 shared handoff、workspace journal 以及本机运行态进入 committed evidence。
- #120 与 #110 的归档证据证明 canonical package/runtime/distribution 模式已落地，#111 必须复用该基础设施。
- Live issue #111 在 2026-07-16 增加“场景范围控制”：freshness、digest、schema、invalid isolation 与 path boundary 只能作为普通 correctness/reproducibility 校验；未声明的安全、威胁、攻击、恶意/误用、并发及其它非常规加固不属于当前交付范围。

## 3. 交付范围

### R1：公共 semantic Skill package

- 必须在 `trellis/skills/guru-team/packages/guru-discover-change-context/` 提供 `SKILL.md`、interface、contract reference、result schema、去身份化 example、thin wrappers 与 package tests。
- `trellis/skills/guru-team/registry.json` 必须把 `guru-discover-change-context` 登记为 `active`。
- Interface 必须声明 `judgment_mode=semantic`，阶段顺序固定为 `forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`。
- Workflow 与 standalone mode 必须使用一致的 entry preconditions、artifact identity 与 freshness 判定。

### R2：fresh base 与输入合同

- 两种 mode 必须消费 validator-passed `guru-sync-base:synced` evidence，绑定 repository、selected base、decision checkout、base HEAD 与 `post_sync_resolution_sha256`。
- 任一 base identity、clean state 或 live Git binding 失配时，Skill 必须在读取 issue、Docs、代码、测试和历史前返回 `refresh_base`。
- Workflow mode 必须接收用户请求及 live issue 或 proposed draft clues。
- Standalone mode 必须接受 issue URL/number、自然语言 request、paths、commands、config keys、schema fields 或 symbols，并执行同一 freshness 检查。

### R3：固定的 current-state 顺序

正向行为必须按下列顺序执行，不得把 current-state 与 history 合并：

1. 校验 fresh base evidence。
2. 读取 live issue，或构造不写仓库与 GitHub 的 proposed change draft。
3. 搜索 open GitHub issue duplicate candidates；只记录 candidates 与 reasons。
4. AI 审查 updated-base durable Docs SSOT。
5. AI 审查代码、API、config、schema 与 ownership。
6. AI 审查 tests、fixtures、throwaway 与 update coverage。
7. 形成 current-state observations 与 canonical query clues。
8. 执行一次 archived finish-summary preview。
9. AI 选择或排除 candidates，并窄读所选证据。
10. AI Review Gate 审查 relevance、sufficiency、conflict、reuse 与 load-bearing conclusions。
11. Recorder/validator 形成结构化结果并返回一个 typed exit。

### R4：duplicate 决策边界

- Skill 必须通过一次 open GitHub issue search 读取 candidates，并记录搜索时点的候选身份、字段派生 facts digest、匹配理由与 AI 观察。
- Recorder/validator 必须从该次搜索返回的候选字段重算 identity 与 facts digest；不得增加 post-review live re-read、closed-after-review、cross-repo hostile-input 或 unreadable candidate 场景。
- Skill 不得决定最终复用已有 issue 或创建新 issue。
- `context_ready` 必须把 duplicate evidence 交给 `guru-clarify-requirements` route，由后续步骤处理用户选择与 issue intake。

### R5：确定性 history preview

- History engine 只能扫描 `.trellis/tasks/archive/**/finish-summary.json` 的 `index.*`。
- Engine 必须实现 versioned canonical query、issue/PR/branch/path/term/query exact/token scoring、`query_sha256`、`archive_manifest_sha256`、invalid isolation、固定排序、固定 limit 与受限 projection。
- Engine 不得读取 `.trellis/workspace/**`、`.trellis/.runtime/**`、repo-level index/cache、`finish-summary-index.json` 或整个 archive 目录内容。
- 无候选必须是成功结果，且不得触发其它历史源。
- Malformed JSON、缺失 index、index shape 错误以及越过 archive/path boundary 的 summary 必须进入按 repo-relative path 排序的 invalid evidence，不得泄露原始内容或本机绝对路径。只保留代表性的普通 invalid-isolation 覆盖，不建立 symlink/FIFO hostile-input、TOCTOU 或跨 OS 文件系统矩阵。

### R6：AI candidate 与深读合同

- Preview 有候选时，AI 必须选择 1 至 3 个候选深读；未选择的 preview candidates 必须逐项记录排除理由。
- Preview 无候选时，AI 必须记录 `selected_candidates=[]` 并继续 Review Gate。
- 深读只能打开所选 task 中能支撑当前判断的明确 artifact，并逐项记录 repo-relative path 与用途。
- `trellis mem` 只能在 task artifact、Docs/code/tests、GitHub 与 Git history 均无法解释一个 load-bearing decision 时调用；调用原因和已穷尽来源必须写入快照。
- 未触发 `trellis mem` 时必须记录 `status=not_needed` 与证据充分性理由。

### R7：artifact、持久化与 refresh

- Pre-task 调用必须仅通过 stdout 形成 canonical snapshot，不得写 repo、task、workspace、runtime、archive index 或 cache。
- Task 创建后，持久化调用必须把同一 canonical snapshot 写入 `{TASK_DIR}/context-discovery.json`，并校验 expected snapshot digest、query digest、archive manifest digest、base HEAD 与本次 live issue/draft identity；此阶段只接纳新 task 目录内的 tracked dirty paths 和 gitignored runtime mapping。
- Artifact 必须受 Git 跟踪并随 task archive；零候选快照同样持久化。
- Freshness 失配后的结果必须记录 reason、superseded query digest、superseded snapshot digest 与时间，再返回 `refresh_base`。
- Artifact、example、manifest 与公共文档不得携带 secret、private data、workspace journal、本机绝对路径或业务私有运行态。该约束通过 closed schema、portable locator 和不持久化 raw payload 承接；不得增加 whole-payload signed URL/credential/path 扫描器。

### R8：typed exits 与唯一 consumer

- `context_ready`：current/history evidence 与 AI Review Gate 完整；唯一 consumer 为 workflow route `guru-clarify-requirements`。
- `refresh_base`：base 或 snapshot binding stale；唯一 consumer 为 `guru-sync-base`。
- `blocked`：输入不可读、合同无效或无法安全形成 evidence；唯一 consumer 为 fail-closed stop `change-context-blocked`。
- Unknown、multiple、unmapped exit 或 consumer drift 必须由 source validator 阻塞。

### R9：workflow、distribution 与 Docs SSOT

- Canonical workflow 与 dogfood workflow 必须 mandatory invoke `guru-discover-change-context`，并只消费上述三个 exits。
- 现有 `guru-sync-base:synced` 必须进入该 Skill；`context_ready` 之后才进入 clarification/intake route。
- Preset 必须安装 canonical package、installed copy、shared/Codex/Cursor/Claude discovery copies、schema、runtime commands 与 executable mode。
- 本任务不得新增或扩写 transitional legacy overlay；现有 `trellis-start` 入口只接受一致性检查。
- Durable requirements、workflow/preset specs、根 README、workflow README 与 preset README 必须同步新公共 API、安装、升级、refresh、side-effect 与 history 边界。

### R10：验证与开箱即用

- Tests 必须覆盖 mode parity、fresh/stale base、current-before-history 顺序、query canonicalization、scoring、digest、invalid isolation、sort、limit、projection、zero candidate、1 至 3 个 deep-read、mem gate、artifact same-snapshot persistence、refresh 与 typed exits。
- Source/installed Skill validator、preset selected-platform、managed hash、dogfood drift、upstream ownership 与 sidecar gates 必须通过。
- Clean throwaway 必须覆盖 marketplace init/preview/switch、preset apply、Skill direct discovery、workflow invocation、zero-candidate 与 candidate preview、task-local record/check、`trellis update --force`、workflow/preset reapply 和最终零 sidecar。
- Remote current-ref marketplace verification 只能在 branch push 后由 finish-work 阶段执行；Phase 2 不得把本地验证表述为远端通过。

### R11：场景范围控制与既有扩张收敛

- 本任务只覆盖 live issue 正文列出的正常调查路径、常见 invalid isolation、确定性摘要与已继承的 task-local/no-shared-write 边界。
- 已提交或未提交实现中的 forged provenance、tamper/post-write tamper、refresh ancestor/receipt trust chain、symlink/FIFO target matrix、signed URL/credential scanner、concurrency race、atomic locking、fault injection、跨 OS atomicity 以及同类非常规加固必须从当前合同、代码、schema、测试、throwaway 和 durable docs 中删除。
- Base freshness 必须消费 `guru-sync-base` 的 validator-passed evidence，不得在本 Skill 内重建第二套 full provenance/security validator。
- `facts_sha256` 字段重算、typed exit 与 AI Gate 状态一致性、query/manifest/preview/snapshot digest、lexical repo-relative path boundary 与 mixed valid/invalid isolation属于普通 correctness，必须保留。
- Planning、Phase 2 check 与 Branch Review 必须先执行 scope qualification。排除项只能记录为 scope proposal 或 future consideration，不能成为当前 P0-P3 finding；若 AI 认为绝对必要，必须经 #113 展示 exact proposal 并取得用户专用显式确认。

## 4. Docs 状态与需求影响

- `docs_state`：`partial_docs`。
- 证据：`docs/requirements/requirement-main.md` 与 `guru-team-trellis-flow.md` 只保留 inline route；workflow/preset specs 已定义公共 Skill 基础设施与 finish-summary 边界，但尚未定义 change-context result schema、history scoring、refresh 或 same-snapshot persistence。
- 本任务会改变 durable workflow、公共 Skill API、artifact contract、companion command、preset inventory、安装验证和公开使用说明。
- 权威 `Docs SSOT Plan` 位于 `design.md` 第 11 节，执行 checkpoint 位于 `implement.md` 第 3 节。

## 5. 验收标准

- [ ] AC1：`guru-discover-change-context` 在 registry/interface/workflow 中使用同一 stable id，且 package 通过 source validation。
- [ ] AC2：两种 mode 的 entry preconditions 与 freshness contract 字节语义一致；stale base 在语义读取前返回 `refresh_base`。
- [ ] AC3：Current-state 审查严格先于 archived history preview；自动化测试证明顺序不可交换。
- [ ] AC4：Duplicate evidence 只记录一次 open search 的 candidates/reasons，并从返回字段重算 identity/digest；不作 reuse/new target 终局决定，也不增加 post-review live re-read。
- [ ] AC5：History engine 只消费 archived `finish-summary.json:index.*`，并输出稳定 query/manifest/preview digests。
- [ ] AC6：Scoring、invalid isolation、sort、limit 和 projection 在输入顺序改变后仍产生相同 canonical result。
- [ ] AC7：有候选时 deep-read 数量为 1 至 3；零候选时返回成功 evidence，且不访问 mem 或其它历史源。
- [ ] AC8：`trellis mem` 只在四类主证据无法解释 load-bearing decision 时执行，并留下结构化理由。
- [ ] AC9：AI Review Gate 明确记录 scope、relevance、sufficiency、conflict、reuse、load-bearing conclusions、findings 与 pass/block。
- [ ] AC10：Pre-task 调用对 repo 零写入；task 创建后的 recorder 以 expected digest 持久化同一 snapshot。
- [ ] AC11：`context_ready`、`refresh_base`、`blocked` 各有唯一 consumer，unknown/multiple/unmapped route 均失败。
- [ ] AC12：Canonical、installed、shared、Codex、Cursor、Claude copies 与 manifest inventory 一致，所有 wrapper executable mode 正确。
- [ ] AC13：Canonical preset apply 后 dogfood drift、upstream ownership 与 `.new`/`.bak` gates 通过。
- [ ] AC14：Clean throwaway 的安装、direct discovery、workflow route、artifact persistence、update/reapply 全链通过。
- [ ] AC15：公共产物不含 secret、private data、workspace journal、本机绝对路径、active task state 或 repo-level archive cache。
- [ ] AC16：PR 关闭语义只有 `Closes #111`；#53、#96、#97、#98、#100、#101、#105、#109、#110、#112、#113 均不关闭。
- [ ] AC17：完整 `origin/main...HEAD` diff 与 working tree 均不存在 R11 排除的 threat/attack/tamper/hostile-input/并发加固合同、实现、测试或公开文档；Phase 2 与 Branch Review 对候选 finding 先记录 scope basis 再分配 severity。

## 6. 范围外

- 不实现 `guru-clarify-requirements`、`guru-review-change-request` 或 task workspace 创建 Skill。
- 不决定 duplicate issue 的最终 reuse/new target。
- 不修改 `finish-summary.json:index` 的既有生产 schema；本任务只消费其当前合同。
- 不建立 repo-level archive index、cache、daemon、search service 或 shared handoff。
- 不读取或写入 `.trellis/workspace/**`。
- 不修改 Trellis upstream、全局 npm package、`node_modules` 或被 #128 冻结的 transitional legacy overlay payload。
- 不实现 forged/tamper/恶意或误用 threat model、refresh ancestor/receipt trust chain、symlink/FIFO hostile-input matrix、signed URL/credential 全 payload 扫描、并发竞态、原子锁定、fault injection 或跨 OS 原子性。
- 不关闭 #111 之外的 issue。

## 7. 中台知识门禁

`not_applicable`。本任务修改 Guru Team Trellis extension 自身，不涉及 `go-guru`、`proto-guru`、Unity3D Guru SDK、Flutter Guru SDK 或其它中台 SDK/API 合同，因此不查询 `guru-knowledge-center`。

## 8. 阻塞项

无外部阻塞。旧 planning approval、Phase 2、task work commit 与 Branch Review 基于 2026-07-16 之前的 issue scope，均不得作为修订后实现与放行证据；必须完成本轮规划确认、收敛实现、fresh Phase 2、fresh commit 与 fresh Branch Review。
