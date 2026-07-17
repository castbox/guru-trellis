# Round 8 最终放行审查报告

## 审查身份与 freshness

- 逻辑角色：fresh 最终放行审查代理，Round 8
- Technical agent id：`issue114_final_review_r8`
- Reuse decision：`new-agent`；本代理未参与 implementation、Phase 2 或 Round 1-7 review
- Primary issue：`#114`
- Base ref：`origin/main`
- Base SHA：`2528a0762b84159f802e5b258daa7ff55e17b4a5`
- Reviewed HEAD：`32119d2ed400046a44148d7f6b580b59a95a0f94`
- Diff range：`origin/main...HEAD`
- 完整分支范围：5 个 task work commits、94 个 committed paths，`27504 insertions / 963 deletions`
- 审查方式：只读独立语义审查；除本 raw report 外未修改实现、规划、Phase 2、assignment、rollup 或 gate artifact，未 stage、commit、push、创建 PR 或关闭 Issue
- 禁止命令遵守：未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*` recorder

Workspace boundary 检查确认 expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/114-contract-wording-review`，source checkout 干净，suspicious source artifacts 为 0。审查开始和测试结束时 HEAD 均精确等于上述 Reviewed HEAD。

## 审查输入与范围

- 完整读取 live GitHub Issue #114 与兼容基线 Issue #93；对照 Trellis 官方首页、custom workflow 与 custom spec template marketplace 文档。
- 读取 task `prd.md`、`design.md`、`implement.md`、`check.jsonl` 六份 curated spec、schema 1.2 `planning-approval.json`、current `contract-wording-review.json`、Phase 2 R7 `phase2-check.json`、`issue-scope-ledger.json`、`task-start-context.json`、`agent-assignment.json`、task commit plan 005 与 reviews/001-007。
- 审查 `origin/main...HEAD` 完整 committed diff、5 条提交消息、Round 6 finding-fix commit 的 45 个精确路径，以及 canonical Skill/interface/contract/schema/example/wrappers/tests、shared runtime、workflow routes、planning approval adapter、extension/registry、preset installer、throwaway verifier、durable requirements/spec/README 和全部 managed copies。
- 检查 replacement-first 删除、#93 archive、Docs SSOT、fresh install/update-reapply、部署资产、敏感信息与 sidecar 边界。

## 需求清晰度与 replacement-first 结论

Issue #114 的需求已经写清楚，无需补充产品决策。目标 Skill id、三个固定 profile、semantic closed loop、词表与 classification SSOT、AI/script 边界、三个 typed exits、#93 without-weakening compatibility、standalone mode、分发和 update/reapply 验收均有确定合同。

用户要求的“重实现之后，删除原有实现”已按 replacement-first 落地：先建立并验证 `guru-review-contract-wording`，再删除旧 planning ambiguity owner。`record-planning-approval` 与 `check-planning-approval` 继续承担 planning start gate consumer/projection 职责，并改为消费新 evidence；它们不拥有词表、分类、scanner 或 semantic judgment，因此不属于旧实现残留。

当前完整实现满足：

- `change_request` 固定包含 title/body，并绑定 AI 选定 authoritative comments 的稳定 identity、author、真实 `updated_at`、selection reason 与 content hash；
- `planning_artifacts` 固定当前 task 的 `prd.md`、`design.md`、`implement.md`，不能被 selector 缩小；
- `explicit_paths` 仅允许 standalone repo-relative Markdown regular files，拒绝 absolute、traversal、non-Markdown、symlink 和 repo 外路径；
- scanner 只产生 objective facts，AI 负责 rewrite、classification、reason、semantic pass/block 与必要的 human confirmation；
- `planning_artifacts` 除 common Gate 外显式承接 #93 七项 planning semantic dimensions，planning approval 逐项复制已验证值，runtime 不生成默认 `true`；
- `pass`、`content_changed`、`blocked` 各有唯一 consumer/stop，unknown、multiple、unmapped、wrong-profile 或 stale evidence fail closed；
- current `content_changed`/`blocked` 可在完整 same-profile re-entry 后按旧 `facts_sha256` 精确绑定收敛；current `pass`、identical result、wrong digest/profile、stale evidence、missing target、non-planning 与 scan-only 路径均被保护或拒绝，stale replacement 与 supersession 互斥。

## Round 1-7 问题生命周期

| 来源 | Finding | 当前状态 | 关闭证据 |
| --- | --- | --- | --- |
| Round 1 | P2 extension artifact contract 未登记 `contract-wording-review.json` | `closed` | canonical/installed extension manifest 与 preset regression 均覆盖 public artifact inventory |
| Round 2 | P1 live authoritative comment 未绑定真实 `updated_at` | `closed` | REST comments adapter 以 `node_id` 对齐 comment，并绑定 author、body/hash、真实更新时间；缺失、重复、API failure 与 stale 路径 fail closed |
| Round 4 | P1 planning semantic dimensions 被 projection 默认生成 | `closed` | 七项 dimensions 仅由 AI Gate 显式记录；schema/runtime 拒绝 missing、false、extra、wrong-profile，planning projection exact-copy |
| Round 6 | P1 current `content_changed` / `blocked` mandatory re-entry dead-end | `closed` | digest-bound same-profile supersession、互斥 stale replacement 与完整 failure matrix 已进入 runtime/contract/workflow/tests/throwaway |
| Round 6 | P2 production 71-test suite 残留旧 active Skill/marker 预期 | `closed` | production active ids 为 5，markers 为 5 invokes / 17 exits / 11 targets，并覆盖四平台分发 |

Round 3、Round 5 和 Round 7 分别完成对应 finding closure；Round 7 报告的 `findings_count=0` 只作为 lifecycle 输入。本轮重新审查完整 HEAD，没有把 earlier closure 当作最终结论，也没有发现上述 finding 回归或新的 current-scope defect。

## Docs SSOT 结论

- Strategy：`ssot_first`。
- Implementation handoff chain 记录 durable docs merge、task-history-only 边界和 remote marketplace limitation；Round 6 修复继续同步 canonical contract、workflow、requirements、README 与六份 durable spec，Phase 2 R7 复核这些输入与最终代码/test/distribution 一致。
- Canonical package contract 独占 vocabulary、classification、semantic loop、profile/evidence/replacement 合同；global workflow 只拥有 mandatory invocation、固定 profile route、typed-exit consumer 与 fail-closed stop；planning approval、overlay 与 companion script spec 只保留自身 obligation。
- Task `design.md` 是获批规划与 finding 演进的历史输入，不是最终 replacement state machine 的第二 owner。Round 4/6 raw findings、fresh implementation handoff、Phase 2 R7 与 durable SSOT 共同记录了 post-planning 修订，未要求追溯改写 approved task history。
- Durable docs 与 task delta 已按 `ssot_first` 合并；task-history-only 内容留在 task/review artifacts。当前没有应留到后续 PR 的 Docs SSOT 缺口；唯一发布限制是真实 pushed marketplace ref 尚不存在，必须由 publish gate 验证。
- 六份 curated spec diff 均已逐项复核，没有重复词表/分类/scanner owner，也没有遗漏 current non-pass supersession、planning dimensions、legacy deletion 或 distribution/update 合同。

结论：当前 scope 的 durable docs、task artifacts、code/schema/config/script/test 与安装副本一致，无 blocking Docs SSOT inconsistency。

## 验证与分发结果

本轮独立复跑：

- Shared runtime：`507/507 passed`。
- Production skill package suite：`71/71 passed`。
- Canonical wording package：`16/16 passed`。
- Preset + upstream ownership：`45/45 passed`。
- Planning/Phase 2 gate subset：`54/54 passed`。
- Source validation：5 active skills、5 invokes、17 exits、11 targets，`status=passed`。
- Installed validation：5 active skills、208 managed files、0 sidecar、0 removal、0 conflict，`status=passed`。
- Canonical、installed、Agents、Codex、Cursor、Claude 六树 package byte equality；canonical/installed workflow、runtime、registry byte equality；12/12 wrappers executable。
- Task commit plan 005 的 45 个 exact stage paths 与 HEAD commit 45 个 paths 完全一致。
- 35 个 changed JSON 与 2 个 changed JSONL 均可解析；task context validation 通过。
- Python syntax compile、Bash syntax、dogfood overlay drift、upstream ownership、`git diff --check origin/main...HEAD` 均通过。
- Planning evidence 为 schema 1.2、`explicit-post-planning-review`、zero unchecked；三份 planning document SHA-256 与 approval 记录一致，wording facts identity 与 approval binding 一致，七项 dimensions 全为显式 `true`。

本轮没有再次执行耗时的完整 throwaway shell。已独立审查 verifier 的 initial 与 after-update installed `content_changed -> pass` supersession、bytes-unchanged assertion、package/inventory checks、`trellis update --force`、workflow/preset reapply、closeout 与最终零 `.new`/`.bak` 路径，并复核同一 finding-fix 内容上 fresh implementation terminal evidence `evt-0228-aa0134a716` 与 Phase 2 terminal evidence `evt-0232-f3328ee5ff` 的 exit 0 结果。该证据覆盖 fresh install、update/reapply、五平台安装、initial/after-update supersession 和 closeout；真实 remote marketplace ref 仍明确留给 publish gate。

## 旧实现、Archive 与边界

- Active source 中不存在 `PLANNING_AMBIGUITY_*`、`scan_planning_normative_language()`、`parse_planning_normative_hit*()` 或 planning 专用 language helper。
- `--normative-hit` 唯一 active 命中是 preset test 的 `assertNotIn` 负向拒绝断言，不是 executable owner 或 workflow usage。
- Vocabulary v2、classification catalog 与 semantic loop 的完整定义只存在于 canonical package/shared runtime；installed/platform copies 是受 manifest 管理的 byte-identical 分发副本。
- `origin/main...HEAD` 对 `.trellis/tasks/archive/**` 的 path diff 为 0；#93 archived artifacts 未追溯改写。
- 未扩张 #101、#112、#129、#132，也未重新引入 Issue 明确排除的恶意 actor、故意伪造、非常规并发、TOCTOU、锁、额外 fault injection 或跨 OS 原子性范围。

## 部署与安全

- 完整 94-path diff 对 CI/CD、Docker、Docker Compose、容器启动脚本、Kubernetes/Kustomize、Helm、数据库 schema/migration/seed 和 Makefile 的 path count 为 0；不涉及服务部署、数据库迁移或生产配置变更。
- Changed filenames 中没有 `.env`、credential、secret、private key 或证书文件；高置信 added-line credential scan 为 0，未发现 GitHub token、AWS key、private key、签名 URL、客户数据或敏感原始记录。
- 验证生成的 ignored `__pycache__` 已移出 worktree；最终 sidecar audit 无 `.new`、`.bak`、`.pyc` 或 `__pycache__`。

## Findings 汇总

- P0：0
- P1：0
- P2：0
- P3：0
- Findings count：`0`

## 观察项

- 分支尚未 push，真实 remote branch/tag marketplace ref 不存在；本地 unpublished workflow、fresh install 与 update/reapply 已验证，真实远端 ref 安装必须由 publish gate 完成，当前不得声称远端安装通过。
- `issue-scope-ledger.json` 中 Issue #114 的 `acceptance_evidence` 仍为空，必须在 publish 前补齐，当前不得 close Issue。
- `review.md` 与 `review-gate.json` 仍是 earlier failed rollup/gate metadata；main session 必须汇总 reviews/001-008 的完整 lifecycle 后重新生成并运行 Branch Review Gate。它们是刻意保留的未提交 review metadata，不是 source drift。
- Phase 2 R7 使用提交前 HEAD `088300a7...` 加 exact dirty snapshot；HEAD commit `32119d2...` 的 45 个路径与 task commit plan 005 完全一致并包含 fresh Phase 2 artifact，因此不存在提交后遗漏。

## 后续候选

无。Issue #114 当前范围内的所有 finding 已闭环，remote ref 与 acceptance evidence 属于既有 publish gate obligation，不需要新增 follow-up issue。

## 证据交接

- 完整审查范围：`origin/main...32119d2ed400046a44148d7f6b580b59a95a0f94`，5 commits，94 paths。
- 部署影响：无 CI/CD、容器、Kubernetes/Helm、数据库 migration 或 Makefile 变更。
- 安全影响：未发现敏感文件或高置信 credential added lines；无 sidecar 残留。
- Docs SSOT：`ssot_first` 已完成，durable SSOT、task history、runtime、tests 与 managed copies 一致。
- Findings/观察项/后续候选：findings 0；观察项仅为 publish/gate metadata obligations；后续候选 0。
- 本报告可供 main session 汇总 task-local `review.md` 并作为 Branch Review Gate 的 fresh final raw report；main session 仍须执行 recorder/validator，不能用本报告替代 gate artifact。

## 结论

- Round 8 最终放行审查：`通过`
- Reviewed HEAD：`32119d2ed400046a44148d7f6b580b59a95a0f94`
- Diff range：`origin/main...HEAD`
- Findings count：`0`
- Issue #114 的需求清晰，replacement-first 重实现已完成，原有 active implementation 已删除，保留的 planning approval helpers 仅为新 evidence consumer。
- 当前结果可进入 main session 的 `review.md` rollup 与 Branch Review Gate；在 gate 通过、publish evidence 完整前，不得进入 Issue closeout。
