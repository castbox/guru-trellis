# #130 最终放行审查原始报告

## 审查身份

- 逻辑角色：`最终放行审查代理`
- 技术 agent id：`/root/issue130_final_release_review`
- reviewed HEAD：`a0ce7610c5e470efa9c08fee9fcc18fbd8993716`
- base：`origin/main@edbd762a93d2a06c8624b13681689e57106acda0`
- diff range：`origin/main...HEAD`
- 审查结论：`block`
- findings_count：2

## 审查范围

已审查 live GitHub Issue #130、根 `AGENTS.md`、`.trellis/workflow.md` Phase 2/Phase 3.5、`prd.md`、`design.md`、`implement.md`、approved `Docs SSOT Plan`、implementation handoff、原实现代理到 replacement 的恢复链、`phase2-check.json`、`issue-scope-ledger.json`、task commit plan、commit message，以及 `origin/main...HEAD` 的完整 92 路径 diff。

实现面覆盖 canonical `guru-check-task` package、interface、schema、example、wrapper、runtime、workflow route、registry、extension manifest、preset/throwaway、durable requirements/spec、task artifacts、tests，以及 shared/Agents/Codex/Claude/Cursor 安装副本。影响面覆盖 CI/CD、container、Docker/Compose、K8s/Kustomize、DB migration、Makefile、部署与安全边界。

Issue scope 复核为：#130 是当前 close scope，#127 是 related，#81/#108/#131/#132 是 follow-up；本轮未把 hostile tamper、TOCTOU、锁、压力竞态、fault injection、cross-OS 加固引入 finding。

## 具体证据、命令与结果

- `gh issue view 130 --repo castbox/guru-trellis ...`：live issue 仍为 OPEN，定位、四出口、single semantic owner、scope-before-severity、artifact 与 normal-operation boundary 均与 planning 一致。
- `git rev-parse HEAD` / `git rev-parse origin/main`：分别为 reviewed HEAD 与 intake base；分支仅有一个 task work commit。
- `git diff --stat origin/main...HEAD` / `git diff --name-status origin/main...HEAD`：完整 diff 为 92 路径，18828 insertions、478 deletions。
- 5 模块 unittest：`Ran 670 tests in 200.595s`，`OK (skipped=13)`。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：exit 0；clean init、workflow preview/switch、preset install、`trellis update --force`、workflow/preset reapply、source/installed validation、43-entry ownership 与 dogfood drift 均通过。
- `python3 -m py_compile ...`：通过。
- `bash -n` 检查 package record/check wrapper、preset apply 与 throwaway verifier：通过。
- `git diff --check origin/main...HEAD`：通过。
- canonical/shared/Agents/Codex/Claude/Cursor 的 8 个 package 文件逐文件 SHA-256：全部相等；wrapper mode 在 commit tree 中为 executable。
- `find . -type f \( -name '*.new' -o -name '*.bak' \) -print`：无 sidecar。
- 完整 diff 对 `.github`、Docker/Compose、K8s/Kustomize、migration、Makefile 的路径扫描：无变更。
- task commit plan working metadata 记录 `result.status=committed`、`exit=committed`、commit SHA 精确匹配 reviewed HEAD、`hook_mutation=false`，committed paths 与 exact stage paths 对齐；commit tree 内保留 planned bytes，符合 metadata tail 合同。

## Docs SSOT 判断

`Docs SSOT Plan` 使用 `ssot_first`，durable requirements/spec/README 均已在实现前定义最终合同，task delta 已合并，task-history-only 内容边界明确，无 no-update exception。实际 durable paths 与 package/workflow/distribution 的 owner、四出口、normal-operation scope 和 no-deploy 语义整体一致。

但是 durable PRD R4/R5/R8/R9、package contract 与 interface 明确要求 requirement/planning trigger、完整 entry evidence、reviewed paths、adequacy evidence linkage，以及 checker 对 full-round/hash/linkage 的客观校验；当前 runtime/schema 对这些合同的实现存在下述两个 finding。因此 Docs SSOT 本身已同步，但代码尚未完全承接，当前 scope 的 Docs SSOT reconciliation 不能判定通过。

## 实现、Phase 2 与替换链判断

原实现代理 `/root/issue130_implement` 的 stale cutover 具有 `stale-assessed`、`terminated-unfinished`、replacement assignment/start 证据；replacement `/root/issue130_implement_replacement` 后续 completed，阶段二检查代理 `/root/issue130_check` 也 completed。Phase 2 stable projection 对合法 post-commit Branch Review metadata tail 的设计与测试成立，当前 replacement/recovery chain 客观闭环。

现有 `phase2-check.json` 自身记录了完整 durable paths、reviewed paths、670 tests、throwaway、ownership/drift/equality、findings=0、unverified=0 和 `passed -> guru-create-task-commit`。但本轮在生产 materializer/checker 路径复现出两个未被 Phase 2 捕获的 current-scope correctness 缺口，因此该 Phase 2 semantic conclusion 对 reviewed HEAD 不再充分，必须返回 implementation 并重新执行完整 Phase 2。

## 问题（findings）

### P0

无。

### P1

#### F-BR-001：closed pass 可以在关键 entry 与 adequacy evidence 全空时成立

- 位置：`trellis/skills/guru-team/packages/guru-check-task/schemas/phase2-check.schema.json:68-82`；`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:9749-9818`、`:10017-10133`
- 违反合同：PRD R4、R5、R8、R9；interface 的 11 项 entry precondition；package contract 的 evidence-bound adequacy/reviewed-path/full-scope Gate。
- 正常路径复现：从当前合法 AI-authored Phase 2 input 出发，将 `requirement_provenance.artifacts`、`implementation_handoff.artifacts`、`docs_ssot_plan.durable_paths`、`repository_snapshot.reviewed_paths` 设为空，并将 10 个 adequacy dimension 的 `evidence_refs` 设为空；调用生产 `materialize_phase2_check_payload` 后得到 `typed_exit=passed`，schema errors 与 `phase2_semantic_errors` 均为空。
- 根因：schema 对上述数组未设置必要的 `minItems`；runtime projection 只要求数组类型；semantic checker 只闭合 finding/unverified id，没有要求 adequacy evidence 非空或解析到本轮 reviewed artifact/command/path。`candidate.trigger_refs` 同样允许 current-scope/scope-change candidate 为空，削弱 scope-first 的 trigger evidence。
- 影响：honest-but-fallible AI 正常遗漏 evidence 时，recorder/checker 仍可发布一个 evidence-free `passed`，使本 Skill 的 11 项 entry 与完整 adequacy Gate 退化为无法审计的 assertion。这是 #130 当前 acceptance 的核心缺陷，必须阻断放行。
- 修复方向：对需要证据的 entry collection 和 passed adequacy dimension 建立非空合同；限定 current-scope/scope-change trigger refs；在 runtime 中校验 evidence refs 解析并覆盖当前 round 的 planning/handoff/docs/reviewed paths/commands，而不让脚本判断语义充分性。

### P2

#### F-BR-002：checker 未重算 semantic 子 digest 与 full-round Gate binding

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:9986-10014`、`:10017-10133`、`:10304-10401`
- 违反合同：interface validator 声明的 `schema, reference, digest, full-round and exit/consumer validation`；PRD R8/R9；package contract 的 current full-round identity。
- 正常路径复现：读取当前合法 `phase2-check.json`，把 `execution_sha256`、`scope_sha256`、`adequacy_sha256`、Gate 的 planning/snapshot/scope/adequacy digest、`findings_count` 和 `full_round_sha256` 改为形状合法但错误的值，再按 checker 当前算法重算 top-level `facts_sha256`；schema errors 与 `phase2_semantic_errors` 均为空，outer facts 也匹配。
- 根因：recorder 的 `phase2_semantic_projection` 会生成这些派生值，但 checker 的 `validate_phase2_check` 不重新执行或等价重算该 projection；`phase2_semantic_errors` 只比较 Gate status/exit 与 finding/route 关系，top-level facts 只是摘要当前已记录的错误子 digest。
- 影响：正常 recorder 缺陷、错误 payload 生成或后续常规 artifact 更新可留下自洽但错误的 full-round identity，checker 仍接受，无法兑现 stale/linkage/full-round 客观校验。该缺口独立于 hostile tamper。
- 修复方向：checker 从当前 payload 的源字段重算 execution/scope/adequacy/Gate/full-round 派生值并逐项精确比较，补充每个派生字段和 `findings_count` 的负例 regression。

### P3

无。

## 观察项（observations）

无。没有把 current-scope defect 降级为观察项。

## 后续候选（follow-up candidates）

无新增候选。#81/#108/#131/#132 保持既有 ledger follow-up，不由本报告扩张或实现。

## 部署影响

无应用 runtime、生产配置、CI/CD、container、Docker/Compose、K8s/Kustomize、DB migration 或 Makefile 变更。存在 Trellis extension/preset distribution 与 upgrade/reapply 行为变化，clean throwaway 已验证通过。由于两个 Gate correctness finding，当前 extension version `0.6.5-guru.17` 不应进入 finish/publish。

## 安全影响

diff 与 task evidence 未发现 token、secret、private key、`.env`、数据库 URL、签名 URL或敏感原始数据。本报告 findings 属于正常流程 correctness/evidence consistency，不主张 hostile-input、anti-tamper、TOCTOU、锁或其它已排除安全加固。

## Agent reuse 与 liveness 说明

本 agent id 在此前 implement/check/review agent 列表中未出现，分派记录 `evt-0076-104aa59c34` 的 logical role 为 `最终放行审查代理`，reviewed HEAD 精确匹配。本轮无 reviewer reuse/replacement。主会话按 liveness checker 的 `status_request_required` 记录一次 `status-requested`（`evt-0077-cce413128f`），本 agent 随后给出实际进度与 findings，并被记录为 `status-response-observed`（`evt-0078-8c2ecbfba7`）；审查未因此中断。

## 最终结论

`BLOCK`。完整 Branch Review 发现 1 个 P1 与 1 个 P2 current-scope finding；按 Phase 3.5 规则，任何 P0-P3 都阻断。应返回实现代理修复 schema/runtime/tests/distribution copies，重新执行完整 Phase 2、task work commit，并在 findings 闭环后派发符合 ledger 规则的 closure review 与全新最终放行审查。
