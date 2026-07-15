# 第 6 轮 F-007 问题闭环审查

## 审查身份与范围

- 角色：`问题闭环审查代理`
- 技术代理：`/root/branch_review_110_f007_closure_finaldesign`
- `reuse_decision=new-agent`
- 审查 HEAD：`ed5fa7baed955f8ba5f84119f4bc177ad170c2d7`
- 基线：`origin/main`（`f9f094f0a995e230226c8a94ff34944ba9d87b53`）
- 完整差异：`origin/main...ed5fa7baed955f8ba5f84119f4bc177ad170c2d7`
- 完整差异规模：124 个文件，新增 22118 行，删除 710 行；4 个 task work commits。
- 闭环对象：Round 5 `reviews/005-final-review.md` 的 F-007（P2）。
- 审查边界：本轮只判断 F-007 在用户批准的最终设计和当前完整分支中是否仍有触发面，不承担新的最终放行，不修实现，不补 Phase 2，不调用 Branch Review recorder/validator，不 commit、push 或创建 PR。

## Workspace Boundary

- `expected_workspace` 与 `actual_repo_root` 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/110-guru-sync-base`。
- Source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，状态干净。
- Task worktree 仅有当前 Branch Review/task-commit liveness metadata；无非 metadata working-tree drift。
- `suspicious_source_artifacts=[]`，boundary 结论为 `status=ok`。

## Findings

- `findings_count=0`
- P0：0
- P1：0
- P2：0
- P3：0

## F-007 生命周期与闭环判断

Round 5 在旧 HEAD `2def8b748dae986e6f9e4d2912c2f8e6d617917a` 上，按照当时的 repo-external result evidence、resolution lease、terminal cleanup 和 zero-residue 设计提出 F-007：malformed/non-canonical result evidence 在内容解析失败后未被删除。

用户随后明确否定该需求扩张，并确认 F-004 修订后的最终 planning。当前闭环标准不是为旧临时文件机制补异常清理，而是确认最终批准合同不再创建该对象。独立复核结论如下：

1. `prd.md`、`design.md`、`implement.md` 明确把 repo-external result/resolution evidence、lease、release executor、quarantine、replacement cleanup、terminal zero-residue 与相关异常文件威胁模型排除出 #110；三份文件当前 SHA-256 与 `planning-approval.json` 中用户确认的 schema `1.2` approval 完全一致。
2. Durable requirements/spec、canonical 与 dogfood workflow、Skill contract、interface、result schema、runtime、tests、preset installer、throwaway script 和 Agents/Codex/Cursor/Claude package copies 均收敛为 stdout-only facts。旧 lifecycle 词汇只存在于历史 Round 1-5 review/gate/task-commit-plan 记录，或当前合同的显式禁止条款，不构成 active API、runtime path 或待实现要求。
3. Runtime CLI 的 `sync-base` 只提供 `--resolve-only`、`--execute`、`--expected-resolution-sha256` 等 Git 同步参数；`check-base-sync` 只通过 `--result-json` 接收调用方从 stdout 捕获的 JSON 字符串。当前 parser、executor、validator 中不存在 `--resolution-file`、`--evidence-file`、`--release-resolution-evidence`、lease id、quarantine 或 cleanup command。
4. `parse_base_sync_result_json()` 直接解析内存字符串/object；`validate_live_base_sync_result()` 校验 schema、facts digest、pre-sync identity、post-sync identity、decision/local/remote live Git equality。Malformed JSON 只产生 deterministic blocked error，不创建可残留的 repo-external 文件。
5. Commit `ed5fa7b` 明确删除旧 `base_sync_evidence_path()`、`read/write/remove_base_sync_evidence()`、`release_base_resolution_evidence()`、result/resolution file CLI 与 prepare lease 传递；替换为 pre-sync resolve-to-execute digest、post-sync result digest以及 prepare guards 的 rolling post-sync digest。

因此，F-007 所依赖的“repo-external malformed result evidence cleanup”对象和 terminal lifecycle 已从当前 normal-scope 产品合同、实现与测试面消失。F-007 不是通过增加旧 cleanup 防御来关闭，而是通过经用户确认的范围纠偏消除触发面；当前不存在仍需修复的 #110 缺陷。

## 当前 Normal-Scope 行为证据

- Base resolver 顺序为 explicit `--base`、非空 scalar `base_branch`、按配置顺序首个 existing candidate（默认 `dev -> develop -> main -> master`）、无 candidate 时 remote default、否则 blocked。
- Resolve stdout 的 `resolution_sha256` 绑定同步前 decision checkout，只保护 resolve 到 execute。
- Execute 只执行 explicit refspec fetch 与 selected-base checkout 上的 `git merge --ff-only`，成功后生成 `post_sync_resolution` 和 `post_sync_resolution_sha256`。
- Validator 重读 live Git，验证 pre/post digest、facts digest、clean checkout 与 decision/local/remote 三方 HEAD equality，并只把 post-sync digest 传给下一 consumer。
- `prepare-task` planner 与每个 GitHub/worktree/task mutation guard 消费前一 guard 的 post-sync digest，复用同一 resolver/sync core，再把新的 post-sync digest 传给下一边界；pre-sync digest 不跨 fast-forward 复用。
- Runtime 回归包含真实 behind-base `resolve -> execute ff-only -> validate -> prepare`，并断言旧 pre-sync digest 在 fast-forward 后 stale、且 config/branch/dirty/digest drift 在相应 fetch/mutation 前 fail closed。

## 验证结果

- Runtime tests：292 项，通过。
- Skill registry/package tests：67 项，通过。
- Canonical `guru-sync-base` contract tests：5 项，通过。
- Preset tests：37 项，通过。
- 本轮独立重跑合计：401 项，通过。
- JSON parse：43 个变更 JSON，通过。
- Bash syntax：17 个变更 shell 文件，通过。
- Python AST parse：22 个变更 Python 文件，通过。
- `git diff --check origin/main...HEAD`：通过。
- TypeCheck：不适用；仓库当前未为这些 Python/Bash/JSON 资产定义独立 typed checker。
- Canonical、installed、Agents、Codex、Cursor、Claude 的 `guru-sync-base` package 内容哈希一致；仅测试运行产生的 gitignored `__pycache__` 物理路径不同，不属于 managed package contract。
- `.trellis/guru-team/extension.json`：83 个 skill package managed files，76 个 preset managed assets，`conflicts=0`、`removals=0`、`sidecars=0`、`new_copies=0`、`managed_backups=0`、`status=ok`。
- Fresh Phase 2 已记录 clean throwaway 的 behind fast-forward、already-equal、rolling digest、fresh install、preview/switch、`trellis update`、workflow/preset reapply 和 zero `.new`/`.bak`；`phase2-check.json` SHA-256 与 task commit plan 004 绑定值一致。
- Task commit plan 004 证明 94 个 exact committed paths 落入 `ed5fa7b`，`parent=2def8b7`、`hook_mutation=false`，expected/actual tree 均为 `d6243458fb238477f9087a8d858539ff7b0f3529`。

## Docs SSOT

- `strategy=ssot_first`，当前 requirements、workflow specs、preset/docs specs 在实现前定义最终合同，并与 runtime/package/schema/tests 一致。
- Workflow 只拥有 mandatory invocation、typed-exit consumer 和 fail-closed route；`guru-sync-base` 独占 deterministic step-local contract。
- `guru-sync-base` 使用 schema `1.2` 的 `judgment_mode=deterministic` 三阶段；`guru-create-task-commit` 与 Phase 2、Branch Review、PR readiness 的 semantic AI gate 未降级。
- Current Docs SSOT 明确“stdout-only，无 cross-step evidence file/lifecycle”；未发现旧 lifecycle 在 active durable contract 中残留为正向要求。
- 历史 `review.md`、`review-gate.json`、Round 1-5 raw reports 和 task commit plan 003 仍如实保留当时 finding/设计历史；它们是 stale audit history，不覆盖最新用户确认 planning、fresh Phase 2 和 commit 004。

## 部署与安全

- 完整差异未修改 CI/CD workflow、Docker/Compose、Kubernetes/Helm、数据库 migration 或 Makefile。
- 未发现 secret、token、private key、`.env`、数据库 URL、签名 URL、客户数据或持久化本机绝对路径进入当前交付资产。
- 当前 #110 安全边界只覆盖 clean Git 状态、合法 ref、explicit fetch、`ff-only` 与 live HEAD equality。
- 本轮没有引入同 UID attacker、filesystem namespace race、fault injection、跨 OS 原子删除、异常文件取证或其它新的安全/攻击/并发要求；仓库中与 `guru-create-task-commit` 等既有能力相关的并发合同不属于 F-007 或 `guru-sync-base` 扩张。

## 观察项

1. Branch-pinned remote marketplace verification 必须在 reviewed HEAD push 后由发布门禁执行；当前未将其表述为已通过。
2. 主会话后续应让全新 `最终放行审查代理` 独立覆盖 `origin/main...HEAD`；本 closure report 不能替代最终放行或 passing `review-gate.json`。

## 后续候选

1. `#111` 继续作为独立 follow-up，不承担 F-007，也不得把已排除的 repo-external evidence lifecycle 重新引入 #110。
2. 若未来有明确产品场景需要跨步骤临时 evidence 文件，再通过独立 issue、需求触发与用户显式确认设计生命周期；不得从本次历史 finding 自动恢复为当前要求。

## 结论

F-007 已闭环，`findings_count=0`，`reuse_decision=new-agent`。用户批准的最终设计已在 planning、durable docs、workflow、Skill/interface/schema、runtime、tests、preset 与平台副本中一致移除 repo-external evidence lifecycle；当前 stdout facts、pre/post rolling digest 与 live Git validator 不创建 Round 5 finding 所指对象，旧 malformed cleanup 触发面已消失。

本代理只完成 Round 6 F-007 问题闭环，不承担最终放行。主会话必须另派全新最终放行代理，不能把本报告直接视为 Branch Review Gate pass。
