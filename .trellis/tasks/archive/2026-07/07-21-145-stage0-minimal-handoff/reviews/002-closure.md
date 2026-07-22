# #145 Branch Review Round 2：F-001 闭环审查

## 审查身份与轮次

- Technical agent id：`/root/issue145_final_review`。
- 角色：Round 1 finding owner / Round 2 问题闭环审查代理。
- `reuse_decision: reuse-for-closure`。
- 本轮只判断 Round 1 F-001 及其修复是否闭环，不是最终放行审查；本代理后续不得担任最终放行轮次。
- 审查结论：`findings_count: 0`。F-001 已关闭，当前 reviewed HEAD 未发现其它 current-scope P0-P3 finding。

## Reviewed HEAD 与 diff

- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/145-stage0-minimal-handoff`。
- Task：`.trellis/tasks/07-21-145-stage0-minimal-handoff`。
- Base：`origin/main@096d1889a511969d5ff09ef4d198ac2825110148`。
- Round 1 reviewed HEAD：`72326953e4df36a91201f10f581361b045e8c6f0`。
- Round 2 reviewed HEAD：`ded63e71e5bab787c5d795a300e3507142b18521`。
- 完整审查范围：`origin/main...ded63e71e5bab787c5d795a300e3507142b18521`，1257 paths，106058 additions，2013 deletions。
- Finding-fix 增量：`72326953...ded63e71`，6 paths；实现变更仅在 preset installer 与其测试，其余 4 paths 为 agent / Phase 2 / commit-plan task evidence。
- `task-commit-plans/002.json` 的 6 个 exact stage paths 与 `ded63e71` 实际 committed paths 一致，expected/actual tree 均为 `007ca0e496a6e94f8c413db90bf31b050b308de5`，逐路径 blob/mode 全部匹配。
- 当前 worktree 中由主代理维护的 `agent-assignment.json`、`task-commit-plans/002.json`、Round 1 rollup/gate 等未提交控制面变更不属于 reviewed HEAD；本轮未修改、覆盖或纳入其语义结论。

## Round 1 Finding 生命周期

### F-001 [P1] Preset upgrade conflict 留下 mixed 1.2/1.3 graph

- Round 1 状态：open / blocking；证据见 `reviews/001-final.md`。
- 修复 commit：`ded63e71e5bab787c5d795a300e3507142b18521`。
- Round 2 状态：**closed**。
- 闭环理由：installer 先复制目标 repo 到临时 staging repo，在 staging 内完成完整 install 与 installed validation；未知编辑或 validation failure 不激活 staging，只向目标物化 `.new`；仅完整 validation 通过，或 known managed `.bak` graph 在暂时移除 backups 后完整 validation 通过，才激活 staged tree。
- `activate_staged_repository()` 在写入前完成所有 path/type preflight，并把 `.trellis/guru-team/extension.json` 排到最后；任务正文明确不要求锁、并发竞态、crash consistency 或跨 OS 原子性，因此本轮不把这些排除场景重新引入 finding。
- `.trellis/.developer`、`.trellis/.runtime`、`.trellis/workspace`、`.git` 与 Python cache 被 transaction copy / comparison / activation 全程排除，现有 developer identity 不会进入 staging、不会被覆盖或删除。

## 审查范围

- 重新核对 PRD R6 / AC7、design 8.2 / rollback、implement Step 5 / RP4。
- 重新审查 `origin/main...ded63e71` 的完整代码、测试、task artifacts、Docs SSOT、issue scope、upgrade/update、部署与安全影响。
- 重点逐行审查：
  - `apply_guru_team_trellis_preset.py:1229-1256` transaction ignored roots 与 staging copy；
  - `apply_guru_team_trellis_preset.py:1259-1350` staged/target inventory、preflight 与 activation；
  - `apply_guru_team_trellis_preset.py:1353-1386` unknown conflict `.new` materialization；
  - `apply_guru_team_trellis_preset.py:1389-1449` known backup candidate 与无-backup activation validation；
  - `apply_guru_team_trellis_preset.py:1452-1503` transaction orchestration 与 activate/preserve 分支；
  - `test_apply_guru_team_trellis_preset.py:1225-1490` pre-#145、unknown edit、known backup、reapply、forced validation failure 与 developer no-copy tests。
- 未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh`、`record-subagent-liveness-event.sh`、其它 Guru Team recorder/gate validator，也未修改实现、Docs、Phase 2、assignment、rollup 或 gate artifact。

## 证据

### 独立行为验证

- `PresetTransactionInstallerTest`：6/6 通过，覆盖 developer identity staging exclusion、known managed upgrade、unknown local edit preserve-old-graph、unknown-edit recovery/reapply、backup acknowledgement、forced installed-validation failure。
- 完整 preset test file：45/45 通过。
- 真实 pre-#145 unknown-edit 路径：从 `git archive origin/main` 安装成功；修改一个受管 `guru-sync-base/SKILL.md` 后用当前 preset upgrade，返回 2 / `unknown_local_edit`；升级前完整 managed graph bytes/modes 不变，六包 registry 仍为 `1.2+legacy`，五个 installed/platform roots 的 interface 均为 1.2，仅生成 `.trellis/guru-team/skills/packages/guru-sync-base/SKILL.md.new`，developer identity bytes 不变。
- 真实 pre-#145 known-managed 路径：首次 current upgrade 返回 2，`conflicts=[]`，产生 118 个 skill package backups 和 1 个 companion managed backup；目标六包 registry 与五个 roots 同时成为 `1.3+minimal_handoff`，未出现 mixed graph，developer identity bytes 不变。处理全部 119 个声明 backup 后 reapply 返回 0，`status=ok`，installed validation=0，recursive `.new/.bak` 数量为 0。
- Forced installed-validation failure test 保持升级前完整 1.2 graph，证明事后失败不会激活 staged candidate。

### 静态与 artifact 验证

- `git diff --check origin/main...ded63e71`：通过。
- 完整 diff 中 1084 个 changed JSON：全部解析通过。
- Finding-fix installer/test 的 SHA-256 与 fresh Phase 2 `reviewed_paths` 精确匹配；commit-plan 002 再绑定到 `ded63e71` tree/blob/mode。
- `phase2-check.json`：schema 2.0，`skill_id=guru-check-task`，`typed_exit=passed`，semantic findings=0，Docs strategy=`ssot_first`。
- Phase 2 snapshot 的 checked HEAD 为 `72326953`，并把 finding-fix code/test 作为 dirty reviewed paths 绑定；随后 task-commit plan 002 将该候选与 Phase 2/task evidence 一并提交为 `ded63e71`。因此该 pre-commit HEAD 表达不是 stale：code/test hashes 与 commit blobs一致，commit tree evidence 为 exact match。
- Phase 2 记录的全量验证包括 preset 45/45、Skill 159/159、runtime 548 passed / 13 skipped、ownership 6/6、shared production eval 24/24、package parity 30/30、source/installed validators、dogfood drift 与 throwaway install/update/reapply；本轮没有用这些 deterministic pass 替代语义审查，而是独立复现了 F-001 关键行为。

## Findings

- P0：0。
- P1：0。
- P2：0。
- P3：0。
- `findings_count: 0`。
- Round 1 F-001 生命周期已从 open/blocking 转为 closed；未发现可在受支持正常路径中复现的 current-scope defect。

## 观察项

- Exact remote feature-branch marketplace install 在分支发布前不可验证；默认 marketplace guard 按合同返回 2。本地 current-source clean install、真实 pre-#145 upgrade、update/reapply 与 zero-sidecar 已通过。该外部时序限制留给 publish gate，不阻断本轮 closure。
- Authenticated Claude native probe 未在本地完成；repository adapter、argv/stdin/output protocol、fake-native 与 declared unsupported 路径已有测试证据。该外部能力限制不影响 F-001 closure。
- Known managed upgrade 首次返回 2 并保留声明 `.bak` 是既有人工确认合同，不是 mixed graph；必须处理 skill package 与 companion 两类全部声明 backups 后再 reapply，最终 zero-sidecar 证据已通过。

## 后续候选

- #146 继续拥有 planning / Phase 2 / task commit 三包的 Interface 1.3 minimal handoff 迁移；本轮未将其并入 #145。
- 后续最终放行必须分派给新的独立 Branch Review agent；`/root/issue145_final_review` 已用于 Round 1 finding ownership 与 Round 2 closure，不得担任最终轮。
- Publish gate 在 branch 可远程解析后补 exact remote marketplace evidence；不得用 public main sample 冒充当前 feature-branch proof。

## Docs SSOT

- `phase2-check.json` 的 Docs strategy 为 `ssot_first`，15 个 durable paths 已纳入 fresh reconciliation，task delta 已合并。
- `.trellis/spec/preset/installer.md:463-483` 明确规定完整 staging transaction、activation 前统一验证、failure 保留 prior complete graph、pre-activation upgrade 与 zero-sidecar；当前实现与真实复现一致。
- `.trellis/spec/preset/installer.md:135-147`、README 与 requirements docs 明确规定 Guru apply/update/reapply 不读取、不创建、不复制、不恢复或删除 `.trellis/.developer` / workspace，existing bytes 保持不变；transaction ignored roots 与行为证据兑现该合同。
- 六包 / 24 exits 继续为 `1.3+minimal_handoff`；`guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三包继续由 #146 保持 `1.2+legacy`。
- #145 是唯一 close issue；#144/#147 仅为 closed authority refs，#146 为 follow-up，#98/#127/#132 为 related，未发现关闭语义漂移。

## 部署与安全判断

- 完整 diff 未修改 CI/CD、container、K8s/Kustomize、Helm、DB migration、Makefile 或 dependency lock/config paths。
- Finding-fix 不改变 public Skill I/O、schema id、workflow route、部署配置、权限、生产数据或生产写入行为。
- secret-shaped diff scan无命中；报告不包含 token、credential、`.env`、签名 URL、客户数据或原始 provider payload。
- Staging 使用受控临时目录并在作用域结束时清理；`.git`、developer identity、runtime/workspace 与 Python cache 不进入 transaction copy。未发现 secret 输出、权限扩大或外部副作用。

## 结论

- `reuse_decision: reuse-for-closure`。
- `findings_count: 0`。
- Round 1 F-001：**closed**。
- Round 2 问题闭环审查：**passed for closure**。
- 当前结论只允许进入新的独立最终放行审查，不等同于最终 Branch Review pass，不授权 finish-work、push、PR 或 issue close。
