# 第 1 轮最终放行审查原始报告

## 审查身份

- 审查轮次：`1`
- 审查角色：`最终放行审查代理`
- 审查来源：`independent-agent`
- 技术代理标识：`/root/branch_review_110_final`
- 复用决策：`new-agent`
- 基线：`origin/main`（`f9f094f0a995e230226c8a94ff34944ba9d87b53`）
- 差异范围：`origin/main...f8e9f09280220ebce6ef22f10382867b5e6d2770`
- 审查 HEAD：`f8e9f09280220ebce6ef22f10382867b5e6d2770`
- 问题数量：`3`（P0=0、P1=1、P2=2、P3=0）
- 审查结论：阻塞，不得记录 passed Branch Review Gate

固定记录字段：`technical_agent_id=/root/branch_review_110_final`，`logical_role=最终放行审查代理`，`reuse_decision=new-agent`，`reviewed_head=f8e9f09280220ebce6ef22f10382867b5e6d2770`，`findings_count=3`。

## 审查范围

本轮由未参与任何前序 Branch Review round 的新 technical agent 独立审查：

- Live GitHub issue #110、parent umbrella #98 与 follow-up #111，确认当前任务只实现并关闭 #110。
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、`agent-assignment.json`、task commit plan 与实现/检查 handoff evidence。
- `origin/main...HEAD` 的完整 103 文件 committed diff，共 11100 insertions、596 deletions。
- Canonical `guru-sync-base` package、shared runtime、workflow、preset installer、overlay、dogfood installed runtime/package、`.agents`、`.codex`、`.cursor`、`.claude` 四个平台分发副本。
- Durable `.trellis/spec/**`、`README.md`、workflow/preset README 与 `docs/requirements/**` Docs SSOT。
- Runtime、skill package、package-local、preset tests，以及安装、update/reapply、drift、sidecar、安全和部署影响。

## Findings

### F-001 [P1] Canonical Skill 把冲突确认排在 digest-bound execution 之后

- 位置：`trellis/skills/guru-team/packages/guru-sync-base/references/contract.md:9`。
- Canonical 顺序图写成 `resolve-only -> AI selected-base review -> digest-bound execute -> AI Review Gate -> conditional conflict confirmation`，即先执行同步，再做冲突确认。
- 同一合同 `:40-50` 规定 AI 在 fetch 前检查 selected base 与用户显式线索是否冲突，并且该冲突触发 human confirmation；task `design.md:141` 也明确确认发生在 executor 前。Canonical 顺序与正文、设计合同相互矛盾。
- 该 package 是 Agent 执行 step-local loop 的直接合同。Agent 若按顺序图执行，可能在用户尚未确认 invocation/selected-base 冲突时先 fetch，甚至 fast-forward 本地 base，造成未经授权的仓库副作用。后置 AI Review Gate 无法撤销已经发生的 Git 操作。
- Canonical、installed、shared、Codex、Cursor、Claude package 副本当前 digest 一致，因此该矛盾会被完整分发，而不是单一副本漂移。
- 修复要求：把唯一 canonical 顺序改为 `resolve-only -> AI selected-base review -> conditional conflict confirmation -> digest-bound execute -> AI Review Gate -> objective result validation -> cleanup -> typed exit`，再通过 preset/apply 同步全部受管副本并复跑 package/drift/throwaway 验证。

### F-002 [P2] Durable 主时序图遗漏 mandatory post-execution AI Review Gate

- 位置：`docs/requirements/guru-team-trellis-flow.md:148`。
- 时序图在 executor 返回 `base-sync result + facts_sha256` 后，于 `:149` 直接调用 `check-base-sync --evidence-file ...`，然后进入 `check-env` / `prepare-task`；图中没有 AI 对 scope、selected-base evidence、实际 fetch/fast-forward 副作用、before/after Git facts 和 unexpected effect 的语义审查。
- 这与 canonical contract `references/contract.md:87-100` 及同一 durable 文档 `:168` 的 mandatory AI Review Gate 要求冲突，并让 validator 看起来可以替代 AI semantic review，违反“AI 判断先发生，脚本随后 validator”的仓库边界。
- 修复要求：在 result 返回与 validator 调用之间显式插入 AI Review Gate，并只在该 gate 通过后调用 `check-base-sync`；同时保持 validator 后才进入后续 typed-exit consumer。

### F-003 [P2] Durable Request triage 表仍把 `check-env + prepare-task` 写成首个步骤

- 位置：`docs/requirements/guru-team-trellis-flow.md:167`。
- Request triage 行仍声明 issue-backed、task-like、file-changing 请求“先跑 `check-env` + `prepare-task`”。但紧邻的 `:168`、`:174-177`，以及 canonical/dogfood workflow 都规定 repo-changing route 的 mandatory first hop 是 `guru-sync-base`，只有 `synced` 后才能进入 context discovery、`check-env` 和 `prepare-task`。
- 该旧入口叙述会误导平台入口或后续维护者在 base freshness 尚未建立时先读取环境、GitHub issue/duplicate 或仓库语义上下文，破坏 #110 要解决的“base sync 先于 repo-changing semantic read”核心边界。
- 修复要求：将该行明确改为 `guru-sync-base -> synced -> check-env / prepare-task`，并说明 `skipped` 仅适用于 tool-free classification 证明无 repo/network action 的 workflow route。

## Docs SSOT 判断

- Docs SSOT 策略：`ssot_first`。
- Canonical workflow 与 dogfood `.trellis/workflow.md` byte-identical；canonical/installed/public platform package 副本也保持一致，未发现一次性 patch 或副本漏同步。
- 但 F-001 是 canonical step-local Skill SSOT 自相矛盾，F-002/F-003 是 durable requirements 与 canonical workflow/Skill 合同不一致；三项均属于 #110 当前范围的 Docs SSOT defect。
- 当前结论：Docs SSOT 未通过。不得用 task planning、Phase 2 passed 声明或相同副本 digest 覆盖语义矛盾。

## 验证证据

本轮独立验证结果：

- Runtime suite：`288 tests passed`。
- Skill suite：`66 tests passed`。
- `guru-sync-base` package-local suite：`5 tests passed`。
- Preset suite：`36 tests passed`。
- 合计：`395 tests passed`。
- `git diff --check`：通过，无 whitespace error。
- Changed JSON：27 个文件经结构解析通过。
- Changed Bash：17 个文件经 `bash -n` 通过。
- Changed Python：16 个文件经不落盘 `compile()` 通过。
- Source/installed package validators：2 个 invokes、6 个 exits 通过；83 个 managed files，0 conflict、0 removal、0 sidecar。
- Canonical/installed/shared/Codex/Cursor/Claude package 文件 digest 一致；canonical 与 dogfood workflow byte-identical。
- 本地 throwaway：fresh init、preset install、standalone sync/validator、workflow preview/switch、`trellis update`、workflow/preset reapply、closeout、zero-sidecar 全部通过。

这些验证证明实现和分发的大部分机械合同可执行，但不能替代对 F-001 至 F-003 的语义审查；测试通过不构成 Branch Review 放行。

## Phase 2 提交后审计

- `phase2-check.json` 记录的检查 HEAD 是基线 `f9f094f0a995e230226c8a94ff34944ba9d87b53`，并冻结了提交前 103 个 `dirty_paths`；当前工作提交 HEAD 是 `f8e9f09280220ebce6ef22f10382867b5e6d2770`。
- 完整 committed diff 的 103 个路径均在 Phase 2 dirty-path evidence 范围内；未发现提交后新增的非 metadata source/spec/docs/test/preset drift。
- 当前未提交改动仅为 task-local Branch Review/commit bookkeeping metadata；本审查没有修改实现、durable docs、spec、测试、schema、config、preset 或 overlay。
- Phase 2 报告本身记录零开放 finding，但 Branch Review 必须独立审查完整最终 diff；F-001 至 F-003 是本轮新发现，不能沿用 Phase 2 passed 结论。

## 开箱即用与 Upgrade/Update

- 已覆盖本地 canonical source 的 throwaway fresh init、workflow preview/switch、preset 安装、standalone/workflow 入口、`trellis update` 后 workflow/preset reapply、closeout 和 zero-sidecar。
- Preset apply 后 canonical/dogfood/平台副本无 drift，未留下 `.new` / `.bak` / conflict / removal sidecar。
- 未执行当前未 push 分支的真实远端 marketplace 安装验证。该项按设计必须在 reviewed content push 后、PR 创建前运行，当前保持 pending 是正确状态；不能把公开 main sample 或本地 canonical 安装声明为当前分支的远端验证。
- F-001 至 F-003 修复会改 canonical package/durable docs，必须返回完整 Phase 2 后重新创建工作提交，再重新执行 Branch Review；之后的远端 marketplace gate 必须绑定新 reviewed HEAD。

## Issue、部署与安全影响

- Issue scope：`close_issues=[#110]`、`related_issues=[#98]`、`followup_issues=[#111]`，分类正确。F-001 至 F-003 均属于 #110 当前合同一致性，不能转移到 #111；修复前证据不足以关闭 #110。
- #111 只负责把稳定的 `guru-discover-change-context` consumer route 内部实现替换为独立 closed-loop Skill，不承担本轮三个缺陷。
- CI/CD：完整 diff 未修改 `.github/workflows` 或其它 CI/CD 配置，无需同步。
- Docker/Compose：未修改容器资产，无需同步。
- Kubernetes/Kustomize/Helm：未修改部署清单，无需同步。
- 数据库 migration/schema：未涉及数据库资产，无需同步。
- Makefile：未修改，无需同步。
- Runtime 影响：有。`guru-sync-base` 会 fetch 并在严格条件下 fast-forward selected base，因此 F-001 的确认顺序直接影响副作用授权。
- 安全：未发现 token、secret、private key、数据库 URL、签名 URL、客户数据或本机绝对路径泄漏；external evidence、symlink/component boundary、digest/facts identity 与 clean checkout 相关测试通过。

## 观察项

1. 当前分支真实远端 marketplace verification 尚未执行，必须在 push 后 publish gate 完成；这是预期 pending 发布门禁，不是本轮 finding。

## 后续候选

1. #111 保持既有 follow-up：实现 `guru-discover-change-context` closed-loop Skill。本轮不实现、不关闭，也不把 F-001 至 F-003 转移到该 issue。

## 最终结论

本轮 `findings_count=3`。HEAD `f8e9f09280220ebce6ef22f10382867b5e6d2770` 的运行时、分发、测试、throwaway 安装与 upgrade/update 机械验证均通过，但 canonical confirmation 顺序存在 1 个 P1，durable sequence/triage 文档存在 2 个 P2，导致 step-local Skill SSOT 与 durable requirements 不一致。按照任何 P0/P1/P2/P3 均阻断的 Branch Review Gate 合同，本轮结论为不通过，不得进入 finish-work。

必须返回实现阶段修复 F-001 至 F-003，重新执行完整 Phase 2、创建新的 finding-fix work commit，再由本 finding owner 按 `reuse-for-closure` 复核至 `findings_count=0`；闭环后仍需派发此前未参与 review rounds 的全新 `最终放行审查代理` 对最新 HEAD 完整 diff 做最终放行审查。
