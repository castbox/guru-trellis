# Round 4 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理，本轮发现问题后成为 finding owner
- Technical agent id：`issue114_final_review_r4`
- Reuse decision：`new-agent`
- Primary issue：`#114`
- Reviewed HEAD：`78ea618f470eaa33fb09f6b5dacc112a60a14e04`
- Diff range：`origin/main...HEAD`
- 审查方式：只读独立语义审查；未修改文件、未提交、未 push，未调用 recorder 或 review gate 脚本

## 审查范围

- 审查 `origin/main...HEAD` 全部 90 个 committed paths 和 3 个 task work commits。
- 读取 live Issue #114、`prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、implementation handoff、`phase2-check.json`、`issue-scope-ledger.json`、`review.md` 及 Round 1-3 原始报告。
- 对照 #93 archived task、旧 runtime/workflow，复核 replacement-first 兼容范围。
- 审查 canonical Skill、interface/schema、shared runtime、workflow、planning adapter、manifest、installer、throwaway verifier、durable docs/spec 和四平台副本。
- 实时复核 Trellis 官方 workflow/spec marketplace 文档及公开 GitHub comment adapter。

## 需求清晰度

Issue #114 已明确以下合同，具备可执行性：

- 三个固定 profile：`change_request`、`planning_artifacts`、`explicit_paths`；
- fixed scope、hash binding、content-change rescan；
- scanner 与 AI rewrite/classification/review 的职责边界；
- versioned artifact、三个 typed exits 及唯一 consumer；
- #93 planning gate 不得弱化、archive 不追溯修改；
- replacement-first 成功后删除旧 owner；
- canonical、dogfood、platform、throwaway、update/reapply 验收边界。

因此下面 finding 不属于需求歧义。`Reimplements and generalizes closed #93 without weakening its delivered planning gate` 以及 task PRD FR-6 已足以要求保留 #93 的完整 AI planning ambiguity review。

## Findings

### P1：新 Skill 未承接 #93 的七项 AI planning ambiguity review，却由 deterministic projection 无条件写成已通过

#93 的交付合同要求 scanner 不替代 AI ambiguity review，且 `ambiguity_review` 的七个 checked dimensions 必须保留，见：

- `.trellis/tasks/archive/2026-07/07-10-093-planning-ambiguity-scanner/prd.md:102`
- 当前 task `prd.md:86-92` 也明确要求 reviewer、summary、checked dimensions 只能从已验证的新 evidence 投影。

但当前实现存在断层：

- Canonical Skill AI Gate 只要求六项 wording dimensions，见 `references/contract.md:106-110` 和 runtime `CONTRACT_WORDING_REVIEW_DIMENSIONS`。
- 这六项不包含 `no_requirement_weakening`、`source_issue_semantics_preserved`、`conditional_paths_have_conditions`、`no_parallel_implementation_paths`、`gates_have_machine_verifiable_conditions`、`acceptance_criteria_are_deterministic`、`external_quotes_are_labeled_non_contract`。
- Repo-wide active-source 搜索表明，这七项只剩 runtime 常量和测试，不再由 workflow、Skill contract 或 durable Markdown 要求 AI 实际审查。
- `contract_wording_planning_projection()` 在 `guru_team_trellis.py:8646-8648` 没有读取对应 AI evidence，而是对七项逐项无条件生成 `true`。
- 当前 task artifact 直接展示了该不对应关系：`contract-wording-review.json:49-55` 只有六项新 wording dimensions，`planning-approval.json:144-152` 却出现七项 legacy dimensions 全部为 `true`。

正常 workflow 中，诚实 AI 只按当前 package contract 完成六项检查即可得到 `planning_artifacts:pass`；随后脚本会把未被要求审查的七项语义结论记录为通过。这会允许含条件路径不完整、并行实现路径、不可机器验证 gate 或不确定验收标准的 planning artifacts 越过 start gate。

影响：

- #93 完整 planning ambiguity gate 被弱化；
- deterministic recorder 实际生成了未经对应 AI Gate 审查的语义结论；
- replacement-first 尚未完成，旧 semantic owner 已提前从 active workflow 删除；
- package/runtime/preset 测试通过不能替代缺失的 Markdown semantic obligation。

Required fix：

- 让 `planning_artifacts` 的新 Skill AI Gate 显式承接 #93 七项语义维度，或保留等价的独立 semantic gate；
- evidence schema 必须记录这些 AI-reviewed dimensions；
- planning projection 只能投影已记录且已验证的结论，不得无条件生成 `true`；
- 同步 canonical package、workflow、durable docs/spec、platform copies 和回归测试；
- 返回 implementation，重新执行完整 Phase 2、task commit、finding closure 和 fresh final review。

## Finding 统计

- P0：0
- P1：1
- P2：0
- P3：0
- Findings count：`1`

## 历史 Finding 生命周期

- Round 1 `P2-extension-artifact-contract`：保持 closed。Canonical/installed manifest 均登记 `contract-wording-review.json`，preset regression 覆盖两侧 inventory。
- Round 2 `P1-live-comment-updated-at`：保持 closed。REST adapter 使用 `node_id` 对齐评论，并绑定 `user.login`、真实 `updated_at`、body/hash；错误和 stale 路径 fail closed。
- Round 4 新增上述 `P1-planning-semantic-dimensions-projection`，当前 open。

## Replacement-first 与旧实现删除

机械迁移部分已完成：

- Active source 中 `PLANNING_AMBIGUITY_*`、planning 专用 scanner/parser/helper 为 0；
- 旧 `--normative-hit` usage 为 0，仅剩拒绝旧 flag 的负向测试；
- `.trellis/tasks/archive/**` branch diff 为 0；
- vocabulary/classification/scanner 没有第二 active owner。

但完整 replacement-first 仍不通过：旧 scanner owner 已被新 generic Skill 替代，旧 planning AI semantic obligation 却未被新 Skill 承接。不能据此确认“重实现后删除原有实现”已经完整闭环。

## 验证证据

- Package tests：`15/15 passed`
- Runtime tests：`501/501 passed`
- Preset tests：`39/39 passed`
- Source validation：5 active skills、17 exits，通过
- Installed validation：208 managed、0 sidecar、0 removal、0 conflict
- Task/context、planning wording evidence、planning approval 和 commit message checks 通过
- Canonical、installed、Agents、Codex、Cursor、Claude 六份 package 字节一致
- Canonical/dogfood runtime、workflow、registry 一致
- Dogfood overlay drift 和 `git diff --check` 通过
- Live Issue #120 selected-comment scan 成功绑定 node id、author、REST `updated_at` 和 body hash
- 完整 diff 未修改 archive、CI/CD、容器、K8s、Helm、DB migration 或 Makefile
- 审查开始和结束 HEAD 均为 `78ea618f470eaa33fb09f6b5dacc112a60a14e04`

## Docs SSOT 判断

Docs strategy 为 `ssot_first`，新 Skill wording 合同、三个 profile、schema/exits 和 adapter 文档已同步。

但 active package/workflow/docs 删除了 #93 七项 planning semantic review obligation，runtime 又将其作为 compatibility projection 自动写成通过。Docs SSOT 与 declared #93 compatibility 尚未收敛，该不一致由 P1 阻塞。

## 开箱即用与 Upgrade/Update

Phase 2 已覆盖本地 unpublished workflow、fresh preset install、三个 profile、planning compatibility、Trellis update、preset reapply 和全平台安装；本轮独立复核 installer、manifest、package copies 和 drift 均通过。

这些机械门禁不会发现缺失的 AI semantic obligation，因此不关闭 P1。真实 remote branch/tag marketplace 安装仍因分支未 push，按计划留待 publish gate。

## 部署与安全

- 不涉及服务部署、数据库迁移、CI/CD、容器或生产配置。
- 未发现 token、secret、`.env`、private key、签名 URL、客户数据或敏感原始记录。
- 未扩张 #101、#112、#129、#132。
- 未引入恶意 actor、对抗输入、非常规并发、锁、TOCTOU 或 fault-injection 范围。
- 部署与安全边界无独立 finding。

## 观察项

- `phase2-check.json` 是提交前绑定旧 HEAD 和 source dirty paths 的证据；P1 修复提交的 non-metadata paths 已被其 dirty snapshot 覆盖。提交后直接运行 current-head Phase 2 validator 会报告 HEAD/dirty mismatch，这是现有提交后审计模型的预期表现，不是独立 finding。
- `issue-scope-ledger.json` 中 #114 的 `acceptance_evidence` 仍为空，必须在 publish 前补齐。
- `review.md` 尚未纳入 Round 3/4，需在后续 gate 录制前更新。

## 后续候选

无。P1 属于 Issue #114 明确要求的 #93 compatibility 与 replacement-first 范围，不应转为 follow-up。

## 结论

- Round 4 最终放行：不通过
- `reviewed_head=78ea618f470eaa33fb09f6b5dacc112a60a14e04`
- `findings_count=1`
- `reuse_decision=new-agent`
- 阻塞 finding：`1 x P1`
- 本代理已成为 finding owner，不得继续担任后续 fresh final reviewer。
