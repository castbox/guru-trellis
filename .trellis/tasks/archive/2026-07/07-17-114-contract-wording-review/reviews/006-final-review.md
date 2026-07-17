# Round 6 最终放行审查报告

## 审查身份与 freshness

- 逻辑角色：fresh 最终放行审查代理；本轮发现新问题后成为 finding owner
- Technical agent id：`issue114_final_review_r6`
- Reuse decision：`new-agent`
- Primary issue：`#114`
- Base ref：`origin/main`
- Base SHA：`2528a0762b84159f802e5b258daa7ff55e17b4a5`
- Reviewed HEAD：`088300a7b3ee33816ec0d96fb3c09d4215ccbae8`
- Diff range：`origin/main...HEAD`
- 审查期间 HEAD 保持不变；仅写本 raw report，未修改 source、规划、gate、assignment 或 commit metadata
- 未运行 `review-branch.sh`、`check-review-gate.sh`、`record-*` 或其它 Branch Review recorder/validator extension script

## 审查范围

- 独立读取 live GitHub Issue #114；确认需求明确声明 replacement-first、三个固定 profile、AI/script 边界、content revision 后 rescan/hash、三个 typed exits、#93 without-weakening、分发与 update/reapply 验收范围。
- 审查 `origin/main...HEAD` 全部 91 个 committed paths和 4 个 task work commits；没有把 Round 5 closure 结论当作最终结论。
- 读取 `prd.md`、`design.md`、`implement.md`、fresh `contract-wording-review.json`、`planning-approval.json`、`phase2-check.json`、implementation/check handoff、`issue-scope-ledger.json`、task commit plan 004、`review.md` 与 Round 1-5 原始报告。
- 审查 canonical Skill/interface/schema/example/runtime、planning approval adapter、workflow router、extension manifest、preset installer、throwaway verifier、durable requirements/spec/README，以及 installed/Agents/Codex/Cursor/Claude 副本。
- 对照 #93 archived contract 与 pre-#114 implementation，检查 replacement-first 删除、archive 边界、deployment/security 与 normal-operation boundary。

## 历史 Finding 生命周期复核

### Round 1 P2：extension artifact contract

保持 `closed`：canonical 与 installed extension manifest 均登记 `contract-wording-review.json`，preset tests 同时断言两侧 public artifact inventory。

### Round 2 P1：live comment `updated_at`

保持 `closed`：runtime 通过 GitHub REST comments adapter 使用 `node_id` 对齐 selected authoritative comment，并绑定 `user.login`、真实 `updated_at`、body/hash。独立读取公开 Issue #120 时，`gh issue view` 的 comment node id 与 REST `node_id` 一致，REST 返回真实 `updated_at`。

### Round 4 P1：planning semantic dimensions projection

保持 `closed`：

- Canonical contract 对 `planning_artifacts` 明确要求 #93 七项 planning dimensions。
- Schema 仅对该 profile 条件必填 exact seven-key object；另外两个 profile 禁止该字段。
- Runtime 对 missing、false、extra、wrong-profile fail closed，projection 只逐项复制 current evidence，不默认生成 `true`。
- Fresh wording evidence 同时记录 6 个 common dimensions 与 7 个 planning dimensions；`facts_sha256=9b5d6882724a86e4ca7c49db56eeb10d27cb99f74251de5d5914f283758d7c0e` 可重算，planning approval 与其逐值一致。

Round 5 已正确关闭 Round 4 finding，但下面两个问题来自本轮对完整 diff 的 fresh final review，不是 Round 4 finding 的重开。

## Requirements 与 Design

Issue #114 的需求已经写清楚，无需补充产品选择。当前实现大部分正确承接：

- `change_request` 强制 title/body，AI 选定 comment 绑定稳定 metadata；
- `planning_artifacts` 固定 current task 的 `prd.md`、`design.md`、`implement.md`；
- `explicit_paths` 仅 standalone，拒绝 absolute/traversal/non-Markdown/symlink/repo 外路径；
- vocabulary v2 与九类 classification 由 canonical contract/shared runtime 拥有；
- scanner 输出 objective facts，rewrite/classification/reason/pass/block 由 AI Review Gate 决定；
- `pass`、`content_changed`、`blocked` 在 interface/workflow 中各有唯一 consumer；
- planning approval 只投影 current `planning_artifacts:pass` evidence，并完整保留 #93 七项语义审查。

但设计要求 `planning_artifacts:content_changed` 进入完整 re-entry，最终再产生可供 planning approval 消费的 `pass`。当前 task-local artifact replacement contract 与这条 route 不相容，构成本轮 P1。

## Code 与 Cross-layer

### 已确认通过的实现

- 三 profile scope builder、UTF-8 scan、scope/scan/facts digests、revision locator/current hash、live issue mutation confirmation chain 均有结构化实现和回归。
- `content_changed` 要求 revision + current rescan，`pass` 禁止未消费 revision，Gate/exit biconditional 与 planning-only dimensions 由 checker 验证。
- Planning projection 在 `guru_team_trellis.py:8642-8692` 只读取已验证七项 evidence。
- Active source 中旧 `PLANNING_AMBIGUITY_*`、planning 专用 scanner/parser/payload/error helper 和 active `--normative-hit` usage 已删除；仅负向测试保留旧 flag 字面。
- `.trellis/tasks/archive/**` 的 branch diff 为 0，旧 #93 archived artifacts 未追溯修改。

### P1：current `content_changed` evidence 阻断 mandatory planning re-entry 收敛

正常路径复现：

1. `planning_artifacts` 中存在弱措辞，AI 在授权范围内完成 rewrite、重建 scope、重扫并记录 `typed_exit=content_changed`。
2. Recorder 将这个 post-change、结构上 current 的结果写入 task-local `contract-wording-review.json`。
3. Workflow consumer 按合同执行完整 planning review re-entry；文档 bytes 无需再次改变，本轮应记录 `typed_exit=pass`。
4. 即使显式使用 `--replace-stale`，runtime 重新验证旧 `content_changed` artifact 后发现它对当前 bytes 仍然 valid，于 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:21282-21295` 拒绝覆盖，返回：

   ```text
   Current contract-wording-review.json cannot be replaced as stale.
   ```

该问题已在干净临时 Git repo 中以真实 `cmd_record_contract_wording_review()` 路径稳定复现：existing exit 为 `content_changed`、next exit 为 `pass`、`replace_stale=true`，仍得到上述错误。它不依赖伪造、篡改、攻击者模型、并发或 TOCTOU。

影响：

- `planning_artifacts` 的正常 rewrite 路径无法从 `content_changed` 收敛为 planning approval 所需的 `pass`；
- 同一条件也会阻止 current `blocked` evidence 在用户补足 authority/confirmation、但文档 bytes 未变时被新结果替代；
- workflow 声明的 unique consumer 存在，但 task-local evidence 状态机是 dead-end；
- throwaway verifier 只覆盖 fresh planning `pass` 和独立构造的 `content_changed`，没有覆盖 `content_changed -> pass` transition，因此此前全绿未发现该缺口。

相关合同证据：

- `trellis/workflows/guru-team/workflow.md:1019-1022` 要求 `content_changed` 完整 re-entry；
- canonical contract `references/contract.md:36-39` 却只允许“旧 evidence 已被证明 stale”后替换；
- runtime 把任何结构上 current 的旧结果一律判为不可替换，没有区分已被 consumer 消费的 non-pass exit。

Severity：`P1`。这是 Issue #114 明确声明的核心 typed-exit 正常路径不可用，会阻塞包含实际 wording rewrite 的 planning task。

Required fix：

- 为 task-local artifact 定义可验证的 same-profile re-entry supersession 规则：至少允许已消费的 current `content_changed`/`blocked` 被完整 current 新 evidence 替换，同时继续保护 current `pass` 不被无理由覆盖；
- 同步 canonical contract、durable data/workflow/script contracts 与 runtime；
- 增加 recorder-level 正向回归：post-mutation bytes 不再变化时 `content_changed -> pass`；以及 blocker 通过 authority/confirmation 消除但 scope bytes 不变时 `blocked -> pass`；
- 在 throwaway 初装和 update/reapply 两段都覆盖至少 `content_changed -> pass` transition；
- 修复后重新执行完整 Phase 2、task commit、finding closure 和另一位 fresh final reviewer。

## Tests 与 Distribution

独立验证结果：

- Canonical package tests：`16/16 passed`。
- Shared runtime tests：`502/502 passed`。
- Preset installer tests：`39/39 passed`。
- Python compile、Bash syntax、JSON parse、`git diff --check origin/main...HEAD`：通过。
- Canonical、installed、Agents、Codex、Cursor、Claude 六份 package 的 8 个文件逐文件 SHA-256 一致。
- Canonical/dogfood workflow、runtime、registry 字节一致；package wrappers executable。
- Dogfood ownership/drift check：5 active skills，overlay drift 为 0。
- Live REST comment adapter：node id、author、真实 `updated_at`、body 与 URL 对齐。
- Phase 2 throwaway evidence 已核对：fresh workflow/preset install、三个 profiles、planning evidence、initial closeout、`trellis update --force`、workflow/preset reapply、after-update closeout 与 Claude/Codex/Cursor all-platform apply 均记录通过；真实 pushed ref 按合同留到 publish gate。

### P2：production skill package suite 未同步新增 active Skill，当前 71-test suite 失败

独立运行：

```text
python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py
Ran 71 tests
FAILED (failures=2)
```

失败与 #114 直接相关：

- `trellis/skills/guru-team/tests/test_skill_packages.py:76-82` 仍断言只有 4 个 active Skill，以及旧的 4/14/8 invoke/exit/target marker counts；实际已是 5/17/11。
- `trellis/skills/guru-team/tests/test_skill_packages.py:1214-1217` 的 production distribution test 仍断言旧 active id 列表，也没有在四个目标根中检查 `guru-review-contract-wording` package/schema/wrappers。

影响：repo-level production source/distribution regression suite 不能通过，且新 public Skill 缺少该 suite 原本为所有 active package 提供的显式分发断言。Phase 2 只运行了新 package 自身、runtime、preset suites 和 validation command，遗漏了这个直接受 registry 变化影响的既有 suite。

Severity：`P2`。运行时安装验证本身通过，但当前分支留下确定性 test failure，不能作为最终放行状态。

Required fix：更新 active id 与 marker counts，并在 production distribution test 中断言新 Skill 的 `SKILL.md`、schema 和 executable wrappers 安装到 shared/Codex/Cursor/Claude 目标；将该 71-test suite 纳入 fresh Phase 2 evidence。

## Docs SSOT

- Vocabulary、classification、semantic loop 与 planning-only dimensions 仍由 canonical package/shared runtime 独占；workflow、requirements、README/spec 和平台入口只引用 stable id/profile/schema/exit/consumer obligation。
- Official Trellis custom workflow 文档确认 `workflow.md` 是 phase/skill routing 的 Markdown 扩展面、hook 只作 parser；当前实现未修改 Trellis upstream、全局 npm 或 `node_modules`。
- Extension manifest、registry、installed/runtime/platform copies 和 durable docs 对新 public Skill 基本一致。
- 但 canonical contract 当前把 task-local artifact replacement 限定为 stale evidence，而 workflow 又要求 current `content_changed` 完整 re-entry。这是与 P1 同根的 blocking Docs SSOT/state-machine inconsistency。
- Task `design.md` 仍以六项 common Gate 为主体描述；fresh wording/planning evidence 和 durable canonical contract 已明确追加七项 planning-only dimensions。该历史计划表述不单独升级为 finding，但后续修订应避免把六项 common Gate 误读为 planning profile 的完整集合。

## Deployment 与 Security

- 完整 diff 对 CI/CD、Docker、Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed 和 Makefile 的 path count 为 0；不涉及服务部署或数据库迁移。
- Credential-like added-line scan 未发现 GitHub token、AWS key、private key、明文 password/token、签名 URL；diff 未新增 `.env`/credential 文件。
- 未发现 `.new`、`.bak`、`.pyc` sidecar；本轮测试产生的临时 bytecode 已清理，工作区恢复到审查前 metadata tail。
- 未扩张 #101、#112、#129、#132；未把恶意 actor、故意伪造、非常规并发、TOCTOU、锁、额外 fault injection、crash consistency 或跨 OS 原子性重新引入 acceptance/findings。

## Findings 汇总

- P0：0
- P1：1
- P2：1
- P3：0
- Findings count：`2`

## 观察项

- 分支尚未 push，真实 remote branch/tag marketplace ref 尚不存在；只能在 publish gate 验证，当前不得声称远端安装通过。
- `issue-scope-ledger.json` 中 Issue #114 的 `acceptance_evidence` 仍为空，publish 前必须补齐，当前不得 close issue。
- `review.md` 仍停留在 Round 4 rollup；main session 必须在本报告产生后追加 Round 5/6 与新 finding lifecycle，再由 recorder 绑定。
- Phase 2 R5 和 Round 5 closure 的机械/语义结论对其已覆盖范围真实有效；本轮 findings 来自此前未覆盖的 cross-exit transition 与 repo-level production package suite。

## 后续候选

无。两个 finding 都属于 Issue #114 已明确要求的 typed-exit/re-entry 与 canonical/platform/distribution 验收范围，不应转为 follow-up issue。

## 最终结论

- Round 6 fresh final review：`不通过`
- Reviewed HEAD：`088300a7b3ee33816ec0d96fb3c09d4215ccbae8`
- Diff range：`origin/main...HEAD`
- Findings count：`2`（`1 x P1`、`1 x P2`）
- 本代理已成为新 finding owner，不得承担上述问题的 closure 或下一轮 fresh final review。
- 当前结果不能支撑 Branch Review Gate，不得进入 `trellis-finish-work`、push、PR 或 Issue #114 closeout。
