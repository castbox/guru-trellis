# #114 按 Skill-first 重实现 #93：`guru-review-contract-wording`

## 目标

新增可独立调用的 semantic closed-loop Skill `guru-review-contract-wording`，统一拥有合同措辞审查的受控词版本、分类集合、固定 profile scope、AI rewrite/review、deterministic scanner/recorder/checker 和 typed exits。在新链路完成回归验证后，删除 #93 留在 planning approval runtime、workflow、平台入口及文档中的旧规则所有权和重复实现。

## 需求清晰度结论

Issue #114 已写清目标、三个固定 profile、闭环顺序、词表与分类 SSOT、三个外部出口、脚本边界、#93 兼容范围及验收口径，已经具备进入设计和实施规划的条件。用户补充的“重实现之后，删除原有实现”解释为 replacement-first migration：先证明新 Skill 覆盖旧行为，再删除旧 owner；不删除仍承担 planning start gate 的 `record-planning-approval` 与 `check-planning-approval` consumer。

## 背景与现状证据

- Source issue: https://github.com/castbox/guru-trellis/issues/114
- Dependency #109 已关闭，根 `AGENTS.md` 已建立 Skill-first closed-loop 规则。
- #93 archived task 位于 `.trellis/tasks/archive/2026-07/07-10-093-planning-ambiguity-scanner/`，其固定三文件范围、全部 hit 记录、unchecked blocking 和九类分类语义是本任务的兼容基线。
- 旧 owner 位于 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：`PLANNING_AMBIGUITY_*` 常量、planning 专用 scan/parse/payload/error helpers 及 planning approval 对这些 helper 的直接调用。
- `trellis/skills/guru-team/registry.json` 尚未注册 `guru-review-contract-wording`。
- Durable workflow/docs/spec 与平台入口仍展开 #93 完整词表、分类和 scanner 行为，没有引用独立 Skill。

## 范围

### In Scope

1. 创建并注册 `guru-review-contract-wording` canonical package，声明 `judgment_mode=semantic`，同时支持 workflow 与 standalone mode。
2. 固定三个 profile：
   - `change_request`：当前 issue/draft 的 title、body，以及 AI 明确选定并记录理由的 authoritative comments；调用方不能排除 title/body。
   - `planning_artifacts`：当前 task 的 `prd.md`、`design.md`、`implement.md`；调用方不能缩小或替换这三个文件。
   - `explicit_paths`：standalone 用户明确指定的 repo-relative Markdown files；workflow 禁止用它替代前两个 profile。
3. 新增 versioned contract-wording evidence schema，绑定 profile、固定 scope、内容 hash、全部 scanner hits、AI revisions、classification/reason、unchecked hits、AI Review Gate 和 typed exit。
4. 新增 generic deterministic scanner、recorder、checker runtime commands 及 package dispatcher wrappers；scripts 只处理 objective facts 和 structural/freshness validation。
5. AI 按固定顺序完成 scope 构造、扫描、优先 rewrite、保留词面分类、重扫、semantic review、命中条件下的人类确认，再调用 recorder/checker。
6. 实现 `pass`、`content_changed`、`blocked` 三个稳定 exit，并由 workflow 中唯一 consumer router 按 evidence 已绑定的 profile 恢复调用方。
7. 保留 #93 planning behavior：三份 planning 文档固定扫描、全部 hits、未分类或 `contract_violation` 阻塞、九类 semantics、Phase 2 check 与 Branch Review 复核。
8. `record-planning-approval` 和 `check-planning-approval` 改为消费并验证新 Skill 的 `planning_artifacts` evidence；planning approval 不再拥有词表、分类、扫描或 AI 判断规则。
9. replacement-first 验证通过后，删除旧 planning 专用常量/helper/CLI 分类输入和 workflow/platform/docs 中完整规则副本；保留必要的 compatibility projection 时必须由新 evidence 生成且不能形成第二规则 owner。
10. 同步 canonical workflow、dogfood workflow、durable docs/spec、preset installer、extension manifest、四个平台 discovery copies 和测试。
11. 验证 source、dogfood、throwaway install 以及 `trellis update` 后 preset reapply 的新包与新路由。

### Out of Scope

- 不改写 archived task artifacts，包括 #93 归档目录。
- 不实现 #101、#112、#129、#132 的后续职责；本任务只提供它们引用的稳定 Skill/evidence/exit 合同。
- 不构建通用自然语言 requirement reviewer；零 controlled-term hit 不能替代 semantic requirement review。
- 不让 scanner 自动选择 classification、rewrite、reason、semantic pass/block 或 route intent。
- 禁止 `explicit_paths` 缩小 `change_request` 或 `planning_artifacts` 的 required scope。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不引入 issue 正文排除的恶意 actor、对抗性输入、故意伪造、并发竞态、TOCTOU、锁、额外 fault injection、crash consistency 或跨 OS 原子性加固。

## 功能需求

### FR-1 Canonical Skill package

- Stable id 必须是 `guru-review-contract-wording`，registry state 必须是 `active`。
- `SKILL.md`、`interface.json`、`references/contract.md`、schema、example、dispatcher wrappers 和 package tests 必须满足 `guru-team-skill-interface-1.2`。
- Workflow 和 standalone 的 entry preconditions 必须一致，且均依赖完整兼容的 Guru Team preset runtime。

### FR-2 Profile scope 与 freshness

- 每个 profile 必须有独立的 deterministic scope builder，result 必须记录 profile、scope item identity、内容 hash 和 scope digest。
- `change_request` 必须绑定 live issue/draft title/body；selected authoritative comments 必须记录稳定 comment identity、选择理由和内容 hash。
- `planning_artifacts` 必须绑定当前 active task 和三份固定文件的 repo-relative path/content hash。
- `explicit_paths` 必须绑定用户本次明确指定的 repo-relative Markdown file set。
- 内容改变后，旧 hits、classification、review 和 result identity 必须 stale；Skill 必须重建 scope 并重新扫描。

### FR-3 Semantic closed loop

- 正向行为顺序固定为 scope build -> deterministic scan -> AI rewrite -> AI classification -> content-changed rescan -> AI Review Gate。
- AI 必须优先把弱约束改为确定合同；需要保留的词面必须写入白名单 classification 和非空、可审计 reason。
- AI Review Gate 必须确认 `unchecked_normative_hits=[]`、rewrite 未改变未经确认的真实产品语义、保留分类理由充分，并明确零 hit 不能替代 requirement review passed 结论。
- 文件、draft 或 issue mutation 只有在 invocation authority 覆盖该 mutation 时执行；GitHub live mutation 仍须 exact payload confirmation 与 live reread。

### FR-4 Deterministic evidence

- Scanner 只输出 version、scope item、location/field、line、term、text 和 content identity。
- Recorder 只记录 AI/human 已完成的 revisions、classifications、reasons、Gate result 和 exit，并派生 canonical digests。
- Checker 必须重新构造 profile scope、重新扫描、校验 vocabulary/classification version、hit completeness、hash、unchecked rules、Gate/exit biconditional 和 artifact freshness。
- 未分类、未知分类、空 reason、`contract_violation`、scope 不完整、hash stale 或 scan mismatch 必须 fail closed。

### FR-5 Typed exits 与 route

- `pass`：scope/hash current，全部 hits 已分类，unchecked 为空，AI Review Gate passed，且本轮没有尚未被 consumer 处理的内容变更。
- `content_changed`：Skill 已在授权范围内修改 reviewed content，并对新内容完成重扫和 evidence 绑定。
- `blocked`：无法在不改变未确认产品语义的前提下 rewrite、缺少 mutation authority、用户拒绝必须的 mutation，或仍存在 unchecked violation。
- 每个 exit 在 interface 中只能指向一个 workflow/stop consumer；workflow router 只按 evidence 中已验证的 profile 做固定映射，不能重新作语义判断。

### FR-6 Planning approval compatibility

- `planning_artifacts:pass` 是展示规划链接和进入 post-planning confirmation 的前置证据。
- `record-planning-approval` 必须消费 current `planning_artifacts` evidence，不再接收调用方逐条注入 classification 的旧 `--normative-hit` owner path。
- `check-planning-approval` 必须调用新 checker 验证 current evidence，并继续校验 explicit post-planning confirmation 与三份 planning doc digest。
- `planning-approval.json` 需要保留 #93 的 reviewer/summary/checked dimensions、全部 hits 与空 unchecked 的审计可见性；这些字段只能从已验证的新 evidence 投影，不能复制规则实现。
- 旧 artifact 的迁移规则必须写入 durable contract：不改写 archive；缺少新 evidence binding 的 active planning approval 在下一次进入实现前重新执行 wording review 与 post-planning approval。

### FR-7 删除旧实现

- 删除 `PLANNING_AMBIGUITY_*` 作为 planning approval owner 的常量和 planning 专用 scope/scanner/parser/payload/error helpers。
- 删除 `record-planning-approval --normative-hit` 的 active workflow usage，并用必填 `--contract-wording-evidence <task-local-artifact>` 取代。
- 删除 workflow、README、durable requirements/spec 和 platform entry 中完整 v2 terms、九类列表和内部闭环步骤副本；这些位置只引用 Skill id、profile、schema/version、exit 与 consumer obligation。
- 删除动作必须发生在新 package/runtime/planning compatibility tests 全部通过之后；验证失败时保留旧链路并返回修订，不留下双 active owner。

## Docs SSOT 状态

- Docs state: `stale_docs`
- Evidence paths:
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
- Requirement impact: 旧文档正确描述 #93 行为，但把行为所有权内嵌在 planning approval/workflow 中，未承接 #114 的独立 Skill SSOT。
- Strategy: `ssot_first`
- Task artifact delta: 本 task 只记录 #114 的迁移计划和验证证据；稳定行为写回 canonical package contract、workflow、durable docs/spec。

## 验收标准

- [ ] `guru-review-contract-wording` 通过 source package validation，并被 preset 安装到 shared/Codex/Cursor/Claude 目标。
- [ ] `judgment_mode=semantic` 且 ordered stages 与 semantic profile 完全一致。
- [ ] 三个 profile 的 required scope、hash binding 和 consumer 均有正向与 fail-closed 测试。
- [ ] Scanner 与 AI rewrite/classification/review 严格分层；scripts 不产生 semantic classification 或 pass 决策。
- [ ] 新 evidence schema 记录全部 hits、revisions、classifications/reasons、unchecked、Gate、profile、scope/content digests 和 typed exit。
- [ ] 任一 content mutation 后使用新 hash 重扫；stale evidence 不能通过 checker。
- [ ] `pass`、`content_changed`、`blocked` 具有唯一外部 consumer，profile route matrix 无 unknown/multiple/unmapped path。
- [ ] `planning_artifacts` 完整保留 #93 fixed scope、全部 hit、unchecked blocking 和九类 semantics。
- [ ] `record/check-planning-approval` 只消费新 `planning_artifacts` evidence，仍阻塞缺失/过期 evidence、未分类 hit 和 `contract_violation`。
- [ ] Phase 2 check 与 Branch Review 继续检查 current planning wording evidence。
- [ ] 新链路回归通过后，旧 planning 专用常量/helper/CLI classification owner 和文档/入口完整规则副本已删除。
- [ ] Active source 不存在两个 controlled-term/classification/scanner owner；完整 vocabulary/classification 只存在于 canonical Skill contract 与 shared scanner constants。
- [ ] Archived task artifacts 未被改写；旧 active approval 的迁移/重新审批规则有测试和文档。
- [ ] Targeted unit/package/preset tests、Python compile、Bash syntax、JSON validation、task validate、dogfood apply/drift、`git diff --check` 通过。
- [ ] 干净 throwaway repo 完成 workflow marketplace + preset install，三个 profile 的已安装入口可运行。
- [ ] throwaway repo 执行受支持的 `trellis update` 后 reapply preset，新 package/commands/routes 未丢失且无未处理 `.new`/`.bak`。

## Open Questions

无。实施中若发现必须改变上述 profile、exit、#93 blocking 或 planning approval migration 语义，必须返回 Phase 1 更新三份规划并重新取得 post-planning approval。
