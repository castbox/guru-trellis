# 第 1 轮最终放行审查报告（阻塞）

## 审查身份

- 逻辑角色：`最终放行审查代理`
- 技术身份：`/root/issue_113_final_release_review`
- 审查来源：`independent-agent`
- 审查 HEAD：`2bf9317d2fa838aff40f250f770e6e51f4439aab`
- Base：`origin/main@96ba63b8c0fab175f6b02997c8799b36bec64e20`
- 完整 diff：`origin/main...2bf9317d2fa838aff40f250f770e6e51f4439aab`
- 结论：`blocked`
- Findings 数量：`6`

## 审查范围

独立审查覆盖完整 110 个 committed paths，包括 83 个 package/runtime/distribution 路径、14 个 durable docs/spec 路径和 13 个 task artifact 路径。审查内容包括 live GitHub issue `#113`、`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、implementation handoff、`phase2-check.json`、`issue-scope-ledger.json`、Docs SSOT Plan、canonical/dogfood/各平台 package 副本、runtime/schema/tests、workflow 路由、preset installer/update、部署与安全影响。

## Findings

### P1：pre-task/standalone 可用无法验证的 draft/context 摘要伪造 `clear`

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19897`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19922`
- 问题：`draft` target 不执行 live authority 验证；`task_dir=None` 时 context freshness 直接返回成功。`review_target.body_sha256` 和 `context_evidence.snapshot_sha256` 均没有可解引用内容或 upstream snapshot payload。
- 证据：提交内公开 standalone example 使用虚构的 `111...` draft hash 和 `333...` context hash，实际执行 `check-requirements-clarification.sh` 仍返回 `status=passed`、`typed_exit=clear`。
- 影响：违反 PRD R2/R3/R8 和 interface 声明的 current authority/context freshness，可绕过 evidence-first 门禁。
- 状态：`open`

### P1：partial answer 可通过空 question lifecycle 直接 `clear`

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19454`
- 问题：reducer 没有要求每轮 `question_id` 必须出现在 `opened_question_ids` 或既有 open set 中。
- 证据：构造 `answer_status=partial`、`opened_question_ids=[]`、`closed_question_ids=[]`、`open_questions=[]` 后，structural/live/typed-exit errors 全为空，`clear` 被接受。
- 影响：部分答案可以绕过“只有形成确定合同时才能关闭”的核心收敛合同。
- 状态：`open`

### P1：GitHub live mutation 未绑定用户确认的 exact payload

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:20036`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:20070`
- 问题：body/comment live checker 只比较 `mutation_results.content_sha256` 与 GitHub live 内容，不比较 live 内容与已确认的 `source_actions[].payload.body`。
- 证据：action 中确认 `CONFIRMED PAYLOAD`，GitHub live 内容模拟为 `DIFFERENT LIVE CONTENT`，body edit 和 comment 两条路径仍无 fatal error。
- 影响：用户确认的 exact payload 与实际写入内容可不一致，破坏 mutation integrity 和安全合同。
- 状态：`open`

### P1：active-task Scope Change 仍绕过新 Skill，且 `clear` 无法恢复 caller

- 路径：`trellis/workflows/guru-team/workflow.md:914`
- 支持路径：`trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md:38`、`trellis/skills/guru-team/packages/guru-clarify-requirements/interface.json:82`
- 问题：active-task 路径仍直接复制分类、确认、ledger/GitHub 更新步骤。唯一 mandatory invocation marker 位于 Phase 0 的 `workflow.md:675`，active-task Scope Change Gate 未 mandatory invoke `guru-clarify-requirements`。同时所有 mode/invocation 的 `clear` 均硬编码到 `guru-review-contract-wording`，与 `prd.md:94` 要求按 invocation context 恢复合法 progression 冲突。
- 影响：initial 与 active-task 共用 Skill SSOT 未完成，active-task 能力实际不可闭环。
- 状态：`open`

### P2：repository-answerable `answered` 不要求 evidence ref

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19427`
- 问题：`not_answerable` 强制非空 evidence，但 `answered` 只检查 answer summary。
- 证据：将公开 example 的 `evidence_refs` 清空后，structural/live/typed-exit errors 全为空并允许 `clear`。
- 影响：repository-answerable question 可以没有任何已检查仓库证据，违反 evidence-first 合同。
- 状态：`open`

### P2：ownership 稳定事实 pin 未随 public API 扩张更新

- 路径：`trellis/presets/guru-team/scripts/python/test_upstream_ownership.py:224`
- 问题：新增 active Skill 和两个 managed assets 后，测试仍固定期待旧 facts SHA。
- 证据：完整 preset discovery 为 `44/45 passed`；实际 facts 从 `47da...` 变为 `9cd9...`，差异是 `active_skill_count: 3 -> 4`、`managed_asset_count: 35 -> 37`。Phase 2 的 `39/39` 只覆盖 apply tests，遗漏 6 个 ownership tests。
- 影响：当前提交保留一个确定性测试失败，Phase 2 覆盖声明不完整。
- 状态：`open`

## 验证结果

- Package tests：`6/6 passed`
- Focused runtime tests：`14/14 passed`
- Registry/distribution tests：`71/71 passed`
- Preset apply tests：`39/39 passed`
- Full preset discovery：`44/45 passed`，1 项为上述 ownership pin finding
- `git diff --check origin/main...HEAD`：通过
- Canonical、dogfood、Codex、Cursor、Claude package payload：字节一致
- TAB/LF/CR 正例及 NUL/其余 C0/DEL 负例：现有 focused tests 通过
- Phase 2 中 `482/482` full runtime、throwaway initial/update/reapply、drift/ownership/zero-sidecar 证据已审阅，本轮未重复执行长链
- `.new` / `.bak`：未发现

## Docs SSOT 判断

`ssot_first reconciliation: failed`。Durable specs、workflow、package contract 已同步大量 `#113` 内容，但批准 PRD R7 的 active-task/standalone caller resume 合同与 interface/durable docs 的统一 Phase 0 consumer 冲突；active-task workflow 又保留旧的直接 Scope Change Gate。该差异属于当前 scope 的阻塞 finding。

## Scope、安全与部署

`issue-scope-ledger.json` 的 `close_issues=[#113]`、related `#55/#98/#109/#111/#114/#101/#112/#127`、空 follow-up 与 live issue 状态一致。由于 findings 未关闭，`#113` 当前不能进入 close/readiness。

未发现 CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile、服务配置或部署资产变更；未发现 secret、private key 或 token。安全主要风险是 exact-confirmed payload 与 GitHub live mutation 未绑定，已记录为 P1。

## 观察项

- Remote current-branch marketplace verification 尚未执行，按现有流程留到 push 后的 `trellis-finish-work`；该项本身不是 finding。
- Working tree 的 tracked 变化仅为主会话维护的 Trellis metadata tail。
- 审查代理未编辑 tracked/reviewed 文件。普通测试生成了 ignored `__pycache__`；其中一次比较 main/worktree ownership facts 时触发 source checkout ignored cache，已即时披露并纠正，source checkout tracked 状态保持 clean。

## 后续候选

无。本轮 6 项均为当前 `#113` scope 的阻塞 finding，不能移入 follow-up。

## 结论

当前 6 个 finding 均阻塞 Branch Review Gate。流程必须返回 implementation，修复后重新执行完整 Phase 2、创建新 task work commit，并依 finding closure 规则完成闭环审查；不得记录 passing Branch Review Gate。
