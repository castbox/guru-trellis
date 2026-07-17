# Round 7 问题闭环审查报告

## 审查身份与 freshness

- 逻辑角色：问题闭环审查代理，Round 7；本轮只负责关闭 Round 6 finding，不得作为最终放行 reviewer
- Technical agent id：`issue114_closure_review_r7`
- Reuse decision：`new-agent`；该 technical agent 未参与此前 implementation、Phase 2 或 Round 1-6 review
- Primary issue：`#114`
- Base ref：`origin/main`
- Base SHA：`2528a0762b84159f802e5b258daa7ff55e17b4a5`
- Reviewed HEAD：`32119d2ed400046a44148d7f6b580b59a95a0f94`
- Diff range：`origin/main...HEAD`
- 完整分支范围：5 个 task work commits、94 个 committed paths；Round 6 finding-fix commit `088300a...32119d2` 包含 45 个精确路径
- 审查方式：只读独立语义审查；除本 raw report 外未修改实现、规划、Phase 2、assignment、rollup 或 gate artifact，未 stage、commit、push、创建 PR 或关闭 Issue
- 禁止命令遵守：未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*` recorder

Workspace boundary 检查确认 expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/114-contract-wording-review`，source checkout 干净，suspicious source artifacts 为 0。审查开始时 HEAD 精确等于上述 Reviewed HEAD。

## 审查输入与范围

- 完整读取 live GitHub Issue #114；需求已经明确 stable Skill id、三个固定 profile、semantic closed loop、词表与九类 classification SSOT、三个 typed exits、script 边界、#93 without-weakening compatibility、standalone use 和 canonical/platform/dogfood/throwaway/update 验收范围。
- 对照 Trellis 官方首页、custom workflow 与 custom spec template marketplace 文档；确认 workflow 行为应由 Markdown 扩展面定义，deterministic script 不得替代 AI semantic judgment，spec marketplace 不应承载 active task 或平台运行状态。
- 完整读取 task `prd.md`、`design.md`、`implement.md`、`check.jsonl` 的六份 curated spec、schema 1.2 `planning-approval.json`、current `contract-wording-review.json`、Phase 2 R7 `phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、task commit plan 005 与 reviews/001-006。
- 审查 canonical Skill/interface/contract/schema/runtime、workflow route、planning approval adapter、extension manifest、registry、preset installer、throwaway verifier、production package suite、durable requirements/spec/README，以及 installed/Agents/Codex/Cursor/Claude managed copies。
- 检查 replacement-first 删除、#93 archive、Docs SSOT、fresh install/update-reapply、部署资产、敏感信息和 sidecar 边界。

## 需求清晰度与 replacement-first 结论

Issue #114 的需求已经写清楚，无需补充产品选择。用户要求的“重实现之后，删除原有实现”已按 replacement-first 落地：先建立并验证 `guru-review-contract-wording`，再删除旧 planning ambiguity 规则 owner；仍承担 planning start gate consumer 职责的 `record-planning-approval` 与 `check-planning-approval` 被保留并改为消费新 evidence，这不属于旧实现残留。

当前完整实现继续满足：

- `change_request` 固定 title/body，并绑定 AI 选定 authoritative comments 的稳定 identity、author、真实 `updated_at` 和 content hash；
- `planning_artifacts` 固定当前 task 的 `prd.md`、`design.md`、`implement.md`，不能被 selector 缩小；
- `explicit_paths` 仅 standalone，拒绝 absolute、traversal、non-Markdown、symlink 和 repo 外路径；
- scanner 只输出 objective term/location/text/hash facts，AI 负责 rewrite、classification、reason、semantic pass/block；
- `planning_artifacts` evidence 除六项 common Gate 外强制承接 #93 七项 planning semantic dimensions，planning projection 只逐项复制已验证值；
- `pass`、`content_changed`、`blocked` 均有唯一 consumer/stop，unknown、multiple、unmapped 或 stale route fail closed。

## Round 6 Finding 生命周期

### P1：current `content_changed` / `blocked` mandatory re-entry dead-end

状态：`closed`。

Round 6 的正常路径复现条件已被消除：

- Runtime 在 `cmd_record_contract_wording_review()` 中把 stale replacement 与 current re-entry supersession 明确拆成两个互斥入口；同时传入两种 assertion 会返回 `contract_wording_replacement_modes_conflict`。
- `--supersede-reentry-facts-sha256` 只允许 `planning_artifacts` 的非 scan-only task-local recorder 使用；`change_request`、`explicit_paths`、scan-only 或无 existing target 均 fail closed。
- Supersession 先用 current scope/scan 完整校验 existing artifact；stale artifact 不能走 re-entry supersession，只能使用独立的 `--replace-stale`。
- Existing 与 new result 必须是同一 profile/mode，旧 `facts_sha256` 必须与参数精确一致，新 result 必须完整 current 且与旧 artifact 不同。
- 只有 current `content_changed` 或 `blocked` 可被 supersede；current `pass`、未知 exit、identical result、wrong digest/profile 均 fail closed。
- Runtime 只校验 transition facts，不判断 consumer 是否应进入 re-entry；完整 re-entry 与 semantic route 继续由 Skill/workflow Markdown 拥有，没有把 AI 判断下放给 script。

回归证据覆盖：

- `content_changed -> pass`，且第二轮 bytes 不再改变；
- `blocked -> pass`，并保护 current `pass` 不被同结果或新 prose 覆盖；
- no target、identical result、wrong digest、wrong profile、stale evidence、non-task profile、replacement mode conflict 和 scan-only/profile restriction；
- fresh throwaway 初装及 `trellis update --force` + workflow/preset reapply 后，均执行 installed planning `content_changed -> pass`、checker 与 closeout。

因此 Round 6 P1 已完成 code、contract、workflow、spec、README、managed copy、unit regression 与 installed throwaway 的完整闭环。

### P2：production package suite 仍使用旧 active Skill/marker 预期

状态：`closed`。

- `test_skill_packages.py` 已把 production active ids 更新为 5 个，包含 `guru-review-contract-wording`。
- Production marker 断言已更新为 5 个 invoke markers、17 个 exit markers、11 个 target markers。
- Distribution regression 在 `.agents`、`.codex`、`.cursor`、`.claude` 四个目标根中显式检查新 Skill 的 `SKILL.md`、schema 和两个 executable wrappers。
- 本轮独立复跑 production suite：`71/71 passed`；source 与 installed validator 也分别返回 5 active、17 exits、11 targets。

因此 Round 6 P2 已关闭，repo-level production regression 不再失败，新 public Skill 的四平台分发也被既有全量 suite 明确覆盖。

## 历史 Finding 保持状态

- Round 1 `P2-extension-artifact-contract`：保持 `closed`。Canonical/installed extension manifest 均登记 `contract-wording-review.json`，preset regression 覆盖 public artifact inventory。
- Round 2 `P1-live-comment-updated-at`：保持 `closed`。REST comments adapter 使用 `node_id` 对齐 selected comment，并绑定真实 `updated_at`、author、body/hash；API/shape/duplicate/missing/stale 路径 fail closed。
- Round 4 `P1-planning-semantic-dimensions-projection`：保持 `closed`。七项 planning dimensions 仅由 AI Gate 显式记录，schema/runtime 对 missing、false、extra、wrong-profile fail closed，planning approval 只 exact-copy current evidence。

## 验证结果

本轮独立复跑：

- Shared runtime：`507/507 passed`
- Production skill package suite：`71/71 passed`
- Canonical wording package：`16/16 passed`
- Preset + upstream ownership：`45/45 passed`
- Planning/Phase 2 gate subset：`54/54 passed`
- Source package validation：5 active skills、5 invokes、17 exits、11 targets，`status=passed`
- Installed validation：5 active skills、208 managed、0 sidecar、0 removal、0 conflict，`status=passed`
- Canonical、installed、Agents、Codex、Cursor、Claude package，以及 canonical/installed workflow、runtime、registry：byte equality passed
- Dogfood overlay drift 与 upstream ownership：passed
- Python compile、Bash syntax、JSON/JSONL parse、task validate、`git diff --check origin/main...HEAD`：passed
- Planning evidence：schema 1.2、`explicit-post-planning-review`、三份 planning document SHA-256、wording facts/scope/scan digests、七项 dimensions 与 zero unchecked 均 current

Fresh install/update-reapply 证据不是用单元测试摘要替代：Round 6 implementation terminal event `evt-0228-aa0134a716` 和 fresh Phase 2 terminal event `evt-0232-f3328ee5ff` 均记录完整 throwaway exit 0；本轮进一步审查了 verifier 的 initial 与 after-update installed supersession 路径、bytes-unchanged assertion、package/inventory checks 和最终零 `.new`/`.bak` 条件。本轮没有再次执行整套远程/throwaway shell；使用的是同一 finding-fix diff 上由 fresh Phase 2 R7 刚完成的可追溯 terminal evidence。

## Legacy、Archive 与旧实现删除

- Active source 中不存在 `PLANNING_AMBIGUITY_*`、`scan_planning_normative_language()`、`parse_planning_normative_hit_*()` 或 planning 专用 language helper。
- `--normative-hit` 唯一 active 命中是 preset test 的 `assertNotIn` 负向拒绝断言，不是可执行旧 owner 或 workflow usage。
- Vocabulary v2、九类 classification 和 semantic loop 的完整定义由 canonical package contract/shared runtime 拥有；其 installed/platform managed copies属于分发副本，workflow、requirements、README 与 consumer specs 只引用 stable Skill/profile/schema/exit/obligation，没有第二 active semantic owner。
- `origin/main...HEAD` 对 `.trellis/tasks/archive/**` 的 path diff 为 0；#93 archived artifacts 未被追溯改写。

## Docs SSOT

- Strategy：`ssot_first`。
- Canonical package contract、workflow、requirements、workflow/preset README 与六份 durable spec 已承接 same-profile supersession、planning dimensions、legacy deletion、distribution 和 update/reapply 合同。
- Global workflow 只拥有 mandatory invocation、profile route、typed-exit consumer 和 fail-closed stop；step-local semantic contract 仍由 Skill 独占；runtime 只处理 deterministic facts。
- Task `design.md` 是 finding 产生前获批的历史规划输入，其 stale-only replacement 和六项 common Gate 表述不是当前 durable behavior owner；Round 4/6 raw findings、Phase 2 R7 与本轮审查明确记录了实现演进，最终稳定合同已经收敛到 canonical/durable SSOT。该历史表述不造成 active 双 owner，也不要求改写已获批 planning artifact。
- 结论：当前 scope 的 Docs SSOT 已收敛，无 blocking inconsistency。

## 部署与安全

- 完整 diff 对 CI/CD、Docker、Docker Compose、容器启动脚本、Kubernetes/Kustomize、Helm、数据库 schema/migration/seed 和 Makefile 的 path count 为 0；不涉及服务部署、数据库迁移或生产配置变更。
- Added-line credential scan 未发现 GitHub token、AWS key、private key、明文 password/token、签名 URL、`.env`、客户数据或敏感原始记录。
- 验证生成的 gitignored `__pycache__` 已清理；最终 package/worktree sidecar audit 无 `.new`、`.bak`、`.pyc`。
- 未扩张 #101、#112、#129、#132，也未重新引入 Issue 明确排除的恶意 actor、故意伪造、非常规并发、TOCTOU、锁、额外 fault injection 或跨 OS 原子性范围。

## Findings 汇总

- P0：0
- P1：0
- P2：0
- P3：0
- Findings count：`0`

## 观察项

- 分支尚未 push，真实 remote branch/tag marketplace ref 不存在；本地 unpublished workflow、throwaway fresh install 和 update/reapply 已验证，真实远端 ref 安装必须由 publish gate 完成，当前不得声称远端安装通过。
- `issue-scope-ledger.json` 中 Issue #114 的 `acceptance_evidence` 仍为空，必须在 publish 前补齐，当前不得 close issue。
- `review.md` 与 `review-gate.json` 仍是 Round 4 的失败 rollup/gate；main session 必须在录入 Round 5-7 lifecycle 后重新生成。它们属于刻意保留、尚未提交的 Branch Review metadata tail，不是未审查 source drift。
- Phase 2 R7 使用提交前模型绑定 `088300a` 和当时 dirty snapshot；commit 32119d2 的 45 个 exact paths 与 task commit plan 005 完全一致并包含 fresh Phase 2 artifact，因此不存在提交后遗漏。

## 后续候选

无。Round 6 两项 finding 均已在 Issue #114 当前 scope 内闭环，不需要新增 follow-up issue。

## 结论

- Round 6 P1：`closed`
- Round 6 P2：`closed`
- Round 7 问题闭环审查：`通过`
- Reviewed HEAD：`32119d2ed400046a44148d7f6b580b59a95a0f94`
- Diff range：`origin/main...HEAD`
- Findings count：`0`
- 本报告可供 main session 汇总 Round 7 finding lifecycle，但不是最终放行结论。下一步必须由从未参与 implementation、Phase 2 或任何 earlier review round 的 fresh 最终放行审查代理，对当前完整 diff 执行独立 final review；在 final review、rollup 和 Branch Review Gate 通过前，不得进入 `trellis-finish-work`、push、PR 或 Issue #114 closeout。
