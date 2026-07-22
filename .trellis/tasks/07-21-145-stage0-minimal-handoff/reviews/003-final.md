# #145 Branch Review Round 3：最终放行审查

## 审查身份与结论

- Technical agent id：`/root/issue145_final_release`。
- 角色：新的独立最终放行审查代理；未参与 Round 1 finding ownership 或 Round 2 closure。
- Reviewed HEAD：`ded63e71e5bab787c5d795a300e3507142b18521`。
- Base：`origin/main@096d1889a511969d5ff09ef4d198ac2825110148`。
- 完整审查范围：`origin/main...ded63e71e5bab787c5d795a300e3507142b18521`，1257 paths，106058 additions，2013 deletions。
- 审查结论：`findings_count: 1`，P1=1；最终放行 **blocked**。

## 独立性与既有证据

- Round 1 / Round 2 reviewer 为 `/root/issue145_final_review`；本轮 agent identity 不同，符合最终放行独立性要求。
- 已完整读取 `reviews/001-final.md` 与 `reviews/002-closure.md`。Round 1 F-001 的 staging transaction 修复在当前 HEAD 上仍成立，本轮未重新打开该 finding。
- `planning-approval.json` 为 schema 2.0、`typed_exit=approved`，`ambiguity_review` passed，固定范围 scanner 无 unchecked normative hit；PRD、design、implement 的 bytes/digest 与 approval 记录一致。
- `phase2-check.json` 为 schema 2.0、`typed_exit=passed`，Docs strategy 为 `ssot_first`，15 个 durable paths 已合并 task delta；finding-fix code/test digest 与 commit `ded63e71` 的 blob 一致。
- `task-commit-plans/001.json` 与 commit `7232695` 的 1256 paths 一致；`task-commit-plans/002.json` 与 commit `ded63e7` 的 6 paths 一致；两次 expected/actual tree 及逐路径 blob/mode evidence 均匹配。

## 已检查文件与范围

- 需求与任务 artifact：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`phase2-check.json`、`issue-review.json`、`contract-wording-review.json`、`issue-scope-ledger.json`、两个 task commit plan、Round 1/2 raw reports。
- Runtime 与脚本：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、installed runtime、canonical/installed bash wrappers、eval adapters。
- 六个 Stage 0 packages：canonical、installed、shared、Codex、Claude、Cursor copies 的 Interface、schemas、examples、consumer contracts、projections、wrappers、tests、eval corpora。
- Registry / migration / extension：source 与 installed registry、Interface schemas、`stage0-minimal-handoff` migration manifest、extension manifests。
- Preset 与 upgrade：installer、transaction activation、overlay、ownership inventory、fresh install、pre-#145 upgrade、update/reapply。
- Docs SSOT：Phase 2 列出的 15 个 durable paths，以及当前任务三份规划与 task delta。
- 完整 diff 的 CI/CD、container、K8s/Kustomize、Helm、DB migration、Makefile、dependency、secret-shaped material 与 sidecar 影响。

## 实现与合同复核

- Migration manifest 精确包含 6 Skills / 24 exits；六包均为 Interface 1.3 + `minimal_handoff`。
- `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三包保持 Interface 1.2 + `legacy`，继续由 #146 拥有；active 总数为 9。
- 24 exits 均有独立 output schema、consumer input/stop contract、projection 与 eval binding；actual exit 在 output schema 选择之前来自 checker-passed owner result，`expected_exit` 未进入 wrapper/native request。
- Canonical 到 installed/shared/Codex/Claude/Cursor 的六包 bytes/modes parity 为 30/30；migration manifest/schema installed parity 通过。
- Round 1 F-001 修复使用完整 staging repo，在 installed validation 后 activation；unknown edit / validation failure 仅物化 `.new` 并保留旧图；`.trellis/.developer`、runtime/workspace、`.git` 与 Python cache 不进入 transaction copy/activation。
- 发现一处独立于上述 transaction 修复的 non-main repository re-entry correctness 缺陷，详见 F-001。

## 验证结果

- Source package validator：通过。
- Installed package validator：通过；1284 managed files，0 sidecar / removal / conflict。
- Dogfood overlay drift：通过。
- Upstream ownership validator：通过；ownership tests 6/6。
- Skill package tests：159/159 通过。
- Runtime tests：548/548 通过，13 个 capability-dependent tests skipped。
- Preset tests：45/45 通过。
- Shared production eval：六包 24/24 cases 通过。
- Full throwaway：clean current-source install、pre-#145 upgrade、workflow preview/switch、Trellis update、preset reapply、zero-sidecar 通过。
- Changed JSON parse、`py_compile`、`bash -n`、task validate、`git diff --check origin/main...HEAD`、working-tree diff check：通过。
- Secret-shaped diff scan：0 命中。
- Exact remote feature-branch marketplace install：分支发布前不可验证；default guard 按合同 fail closed，保留给 publish gate。
- Authenticated Claude native probe：本地未验证；fake-native/protocol/declared unsupported coverage 通过。该限制不影响 F-001 定性。

## Findings

### F-001 [P1] Semantic re-entry serializer 将 non-main resolver fallback 改写为显式 `main`，阻断受支持仓库

- Severity：P1。
- 位置：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19148-19155`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19258-19271`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19285-19292`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19310-19315`
  - `trellis/skills/guru-team/packages/guru-clarify-requirements/interface.json:538-591`
  - `trellis/skills/guru-team/packages/guru-review-change-request/interface.json:470-508,570-596`
- 需求证据：PRD D1 / R2 / AC3 明确要求省略 `base_branch` 时把 unspecified value 交给 formal owner resolver，保留 configured scalar -> ordered candidates -> remote default 的既有优先级；AC6 要求 refresh/re-entry/retarget families 在 clean throwaway repo 通过。Durable Docs SSOT 在 `skill-package-contract.md` 与 `companion-scripts.md` 重申 wrapper 不得复制 fallback 或把 config-candidate / remote-default provenance 改写为 explicit。
- 实现证据：`stage0_default_base()` 只读取 scalar `config.base_branch`，否则无条件返回 `main`。`guru-clarify-requirements` 的 `needs_context`、`refresh_context`、`retarget_context` 以及 `guru-review-change-request` 的 `ready`、`refresh_context` 都使用该 helper 生成必填 `handoff_base_branch`。refresh/retarget projections 再将该字段 rename 为 `guru-sync-base.base_branch`，因此 unspecified fallback 被改成显式 `main`。
- 正常路径复现：创建 clean Git repo，仅有 `develop` local/remote branch，remote HEAD 指向 `develop`，配置仅含 `base_branch_candidates=["develop"]`，不含 scalar `base_branch`。formal resolve 返回 `selected_base=develop, source=config-candidate`；`guru-sync-base` public wrapper 省略 `--base-branch` 返回 `exit_id=synced, handoff_base_branch=develop`。同一 repo 上，clarification `refresh_context` serializer 返回 `handoff_base_branch=main`；按声明 projection 以显式 `--base-branch main` 调 consumer 时返回 `exit_id=blocked`，formal explicit resolve 同时报 `selected local base branch does not exist`。
- 影响：所有没有 `main`、依赖 ordered candidate 或 remote-default fallback 的正常仓库，在 clarification refresh/retarget 和 readiness refresh re-entry 中会被错误阻断；同一 helper 还污染 `needs_context` 与 `ready` 的后续 context/workspace handoff。用户不能通过 D1 承诺的 optional path 恢复，因为 producer output schema 强制携带错误的显式 branch。该缺陷直接破坏 #145 current-scope D1、AC3、AC6 与 existing re-entry contract。
- 测试缺口：`Stage0PublicInvocationTests.setUp()` 固定 `git init -b main`，omitted-base test 只断言返回 `main`；24-case corpora 分别验证 producer exits 与 `guru-sync-base` 自身，但没有把 non-main producer DTO 经 projection 送入 consumer。现有 24/24 pass 因此不能覆盖该跨 Skill data flow。
- 建议修复：不要在 semantic producer serializer 中实现第二套 `main` fallback。优先让 refresh/retarget consumer input 保持 `base_branch` optional 并省略该字段，使 `guru-sync-base` formal resolver 独占 fallback；若 public DTO 合同确需携带 resolved branch，则必须调用同一 formal resolver并保留其 selected base，而不是硬编码。补充 `config-candidate` 与 `remote-default` 两类 clean non-main fixtures，端到端验证 producer output -> declared projection -> consumer public wrapper，覆盖 clarification refresh/retarget、readiness refresh，以及 `needs_context` / `ready` handoff。
- 处理状态：open；Branch Review 角色未修改实现。修复后须刷新 Phase 2/task commit evidence，并由新的审查轮次重新覆盖完整 branch diff。

## Docs SSOT

- Plan strategy：`ssot_first`；15 个 durable paths 和 task delta 的 digest/merge evidence 完整。
- 当前文档正确声明 optional base 必须保留 formal resolver order，但实现中的 `stage0_default_base()` 与该 current-scope SSOT 不一致；因此 Docs SSOT gate 结论为 **blocked**，不能以文档已经更新替代实现修复。
- #146 三包 legacy 边界、六包/24 exits、transaction activation 与平台分发文档均与当前实现一致；除 F-001 外未发现第二处 current-state 文档冲突。

## 部署与安全

- 完整 diff 未修改 GitHub Actions、container、K8s/Kustomize、Helm、DB migration、Makefile 或 dependency lock/config paths。
- F-001 不涉及生产数据写入、credential、权限扩大或外部发布副作用；它是正常 non-main repository workflow correctness 缺陷。
- Secret-shaped diff scan无命中；报告不包含 token、credential、`.env`、签名 URL、客户数据或原始 provider payload。

## 观察项与后续候选

- Exact remote feature-branch marketplace proof 继续由 publish gate 在 branch 可远程解析后完成；不得用 local sample 冒充 remote proof。
- Authenticated Claude live probe 可在环境恢复后补跑，但不能替代 repository contract tests，也不改变本轮 blocking finding。
- #146 继续拥有 planning / Phase 2 / task commit 三包迁移；F-001 修复不得顺带迁移这三包或扩张到锁、并发压力、crash consistency、恶意 artifact 篡改、TOCTOU 或跨 OS 原子性。

## 结论

- Findings：P0=0，P1=1，P2=0，P3=0。
- `findings_count: 1`。
- Final Branch Review：**blocked**。
- `Closes #145`：当前不得发布；D1 optional-base resolver ownership 与 AC3/AC6 尚未满足。
- `review.md` / Branch Review Gate：本报告可作为本轮 raw review evidence，但不能支持 passed gate；主会话应记录 blocking finding 并路由 finding-fix loop。
