# Issue #125 最终放行独立审查原始报告

## 一、审查身份与边界

- 逻辑角色：`最终放行审查代理`
- 技术身份：`/root/trellis_final_review_125`
- 审查来源：独立代理；未参与本任务规划、实现、Phase 2 检查、finding 修复或 commit 创建
- 审查模式：Branch Review，只报告 finding，不修改实现
- reviewed HEAD：`e4937dfe19c9e3d889144ca5ef9d7afd42a429b5`
- intake base ref：`origin/feat/122-guru-create-task-commit`
- base HEAD / merge base：`49bf572e6a89bff9c63416bea64254cda0c20bf0`
- 完整 diff：`origin/feat/122-guru-create-task-commit...HEAD`
- committed diff：1 个 commit，78 个路径，`5279 insertions / 326 deletions`
- 审查时工作树：仅 `agent-assignment.json` 与 `task-commit-plans/001.json` 有 task-local metadata 变更；实现、spec、durable docs、测试和分发副本没有未提交改动
- 禁止动作遵守情况：未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh`、任何 `record-*` 或其它 Branch Review recorder；未修改 planning、spec、实现或测试

Live GitHub 事实：Issue #125 为 OPEN，六项需求与 `prd.md` 一致；PR #124 为 OPEN / MERGEABLE / CLEAN，head 为 `feat/122-guru-create-task-commit@49bf572e...`。本分支继续以该 HEAD 为 stacked base。

## 二、读取范围与证据

完整读取并交叉核对：

- `.agents/skills/trellis-check/SKILL.md`
- task `prd.md`、`design.md`、`implement.md`
- `implementation-handoff.md`
- `phase2-check-report.md`、`phase2-check.json`、`phase2-findings.json`
- `issue-scope-ledger.json`
- `task-commit-plans/001.json` 的计划、路径分类、AI review、授权、freshness、commit result 与逐路径 tree evidence
- 四份变更 spec：`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`
- durable requirements：`docs/requirements/README.md`、`requirement-main.md`、`guru-team-trellis-flow.md`
- public docs：根 `README.md`、workflow README、preset README
- canonical workflow、dogfood workflow、canonical Skill `SKILL.md` / interface / contract
- interface schema 1.1、canonical/fixture/installed extension manifests
- package wrappers、shared Bash dispatcher、Python source/installed validators 与 runtime resolver
- preset installer、throwaway verifier、package/source/runtime/installer tests
- canonical、audited installed、shared、Codex、Cursor、Claude 副本及 committed task artifacts
- commit message、完整 committed path set、stacked base 和当前工作树

## 三、逐项判断

### 3.1 需求与设计承接

- R1 mode 与 dependency metadata：`workflow` / `standalone` id 保持稳定，routing 分别为 `global_workflow` / `direct_discovery`；schema 1.1、extension capability、active interface 已同步。存在下述 F-001，导致 source/installed validator 对一个确定无效的 runtime command 映射仍会错误通过，因此 R1 的机器校验闭环尚未完全成立。
- R2 共享 runtime SSOT：通过。package wrappers 只定位 dispatcher、传 package root / fixed validator id / 原参数；parser、task/gate、Git snapshot、staging、transaction、rollback 仍只在共享 runtime。
- R3 fail closed：当前 production interface 的 missing manifest/dispatcher、API/dependency/unknown-command、discovery drift 路径由测试覆盖；package-only copy 返回 2 并给出完整 preset remediation。F-001 证明 source validation 与 invocation validation 对 dispatcher self-mapping 不一致，完整安装可以先被判为 valid、再在入口 blocked。
- R4 canonical 与分发：通过。canonical、audited installed、shared、Codex、Cursor、Claude 五个 package copy 均为 8 files，bytes/executable mode 一致；canonical/dogfood runtime dispatcher、Python runtime、workflow 一致；无 `.new` / `.bak`。
- R5 durable/public docs：通过。四份 spec、三份 durable requirements、三份 public README、workflow/package contract 对 routing independence、完整 runtime dependency、non-portable 边界、dispatcher 与 remediation 的描述一致。

### 3.2 Docs SSOT

- Docs state：`partial_docs`
- Strategy：`ssot_first`
- 已把 task delta 写回 durable spec、requirements、workflow/package contract 与 public README，task history 仅保留 stacked base、代理/临时验证与未 push exact-ref 事实。
- 未发现 durable docs、task planning、production interface、runtime 或测试之间除 F-001 外的当前范围冲突。
- Docs SSOT reconciliation 结论：实现路径符合批准策略；F-001 是机器合同实现缺口，不是文案缺失。

### 3.3 Schema、runtime dispatcher 与路径安全

- schema 使用 Draft 2020-12、closed objects、schema id/version 1.1；mode routing、runtime dependency 与 validator `runtime_command` 为 required。
- extension `0.6.5-guru.6` 发布 `skill_runtime` API 1.0、dispatcher id 与 manifest path，且 companion inventory 包含 `run-skill-command`。
- resolver 从 audited runtime path 推导 repo，限制 package 为 installed/shared/Codex/Cursor/Claude layout，执行 component-wise `lstat`，调用 `validate_skill_installed(..., require_workflow=False)`，因此 standalone 不消费 global workflow route，但仍消费完整 installed inventory。
- runtime resolver 拒绝 dispatcher self-mapping；source validator 只检查 command pattern 与 published membership，没有承接同一机械约束，形成 F-001。
- 当前 production mapping `candidate_validator -> check-commit-messages`、`exact_executor -> create-task-commit` 正确；没有 legacy fallback 或任意 runtime path 输入。

### 3.4 Installer、upgrade/update 与开箱即用

- dispatcher 已进入 `MANAGED_ASSET_PATHS`、executable handling、manifest companion inventory、preset installed-file list 与 initial/update-reapply probe。
- Phase 2 原始报告及 JSON 记录：public marketplace discovery + unpublished local sample 的 clean throwaway、初装 probe、`trellis update --force`、workflow re-selection、preset reapply、第二次 probe、source/installed validation、recursive sidecar scan 与 closeout smoke 通过。
- 本轮独立复核 installer/throwaway 代码与 36 个 installer tests；未把 public canary 提升为 exact feature-ref remote pass。
- exact feature-ref remote marketplace verification 尚未执行，因为 reviewed content 尚未 push；按设计应由 `trellis-finish-work` 在 push 后生成 immutable evidence。这是后续强制门禁，不是把当前 F-001 降级的理由。

### 3.5 测试与验证

独立执行结果：

| 命令 | 结果 |
| --- | --- |
| `python3 trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py` | 5 tests passed |
| `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'` | 64 tests passed |
| `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 36 tests passed |
| `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 275 tests passed |
| `git diff --check origin/feat/122-guru-create-task-commit...HEAD` | passed |
| canonical JSON parse、target Bash `bash -n`、Python `py_compile` | passed |
| canonical/5 package copies/runtime/workflow bytes + executable mode audit | passed |
| recursive `.new` / `.bak` scan | 0 |
| `.agents/.../check-task-commit-plan.sh --help` | 经 shared dispatcher 成功进入 companion command |
| committed plan / current result / committed diff 交叉核对 | 78 diff paths = 78 exact stage paths = 78 classifications；result commit/tree/preservation 匹配 |

现有 64-test suite 的 negative matrix 覆盖 unknown `runtime_command`，但没有覆盖 published dispatcher id 被误用为 validator target 的情况；F-001 的复现证明测试矩阵存在对应空白。

### 3.6 安全与部署影响

- 未发现 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或本机绝对路径进入 public package/docs/manifest。
- 当前 production command mapping 为 closed validator id + published command + managed relative executable；路径执行前有 component-wise `lstat`，无 legacy fallback。
- 未变更服务、API、worker、schedule、queue、数据库 migration、Dockerfile、Compose、Kubernetes/Helm/Kustomize、CI/CD 或 Makefile；部署形态不变。
- F-001 主要影响 public validation/install correctness：错误 package 可被发布和安装，随后入口必然 fail closed；未观察到当前 production mapping 触发越权或业务副作用。

### 3.7 Issue ledger、commit message 与 stacked base

- ledger：`close_issues=[125]`、`related_issues=[122]`、`followup_issues=[]`，分类正确；#122 保持 related-only。
- `acceptance_evidence[]` 仍为空，符合 artifact 中“publish 前补齐”的已声明状态；finish/publish 前必须填写真实证据。
- work commit subject 为中文 Conventional Commit：`feat(trellis): #125 明确 Skill standalone runtime 依赖`。
- body 按 `背景：`、`变更：`、`边界：`、`验证：` 顺序，footer 仅 `Refs #125`，无 close keyword；安全、部署、未完成 exact remote verification 的描述真实。
- commit parent 精确等于 intake base HEAD；没有把 #122 archive/task 重新计入或修改。
- PR #124 合并后，#125 必须 retarget 到 `main` 并对新的 `origin/main...HEAD` 重新执行 freshness-sensitive Phase 2、Branch Review 与 remote marketplace verification。

## 四、问题清单

### P0

无。

### P1

无。

### P2

#### F-001 Source validator 接受 runtime 明确拒绝的 dispatcher 自指 command mapping

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- 位置：source validator `validate_skill_interface()` 约 12925-12945 行；runtime resolver `resolve_skill_runtime_command()` 约 13746-13759 行
- 问题：source validator 只要求 `runtime_command` 符合 id pattern 且属于 extension `companion_scripts`。`run-skill-command` 本身属于该 published inventory，因此把 validator 的 `runtime_command` 改为 dispatcher id 后，source validation 返回 `passed`。同一文件的 runtime resolver 又明确执行 `runtime_command == dispatcher` 拒绝，完整 preset 安装后的 wrapper 必然返回 blocked。
- 复现：复制 representative-active fixture 到临时目录，把第一个 validator 的 `runtime_command` 改为 `run-skill-command`，调用 `validate_skill_source(temp_root, workflow)`；实际输出为 `{"status":"passed","errors":[]}`。
- 影响：一个机械上确定不可调用的 active package 可以通过 source validation、进入 installer/installed inventory 并被分发到平台副本，直到用户直接调用时才失败。这违反“source/installed validation 证明 compatible package”以及命令映射不匹配应在分发前 fail closed 的合同，也使 clean install validation 可能与真实 standalone 可用性分离。
- 必须修复：source interface validation 应拒绝 `runtime_command == runtime_dependency.dispatcher`，并增加 source/schema semantic negative test；修复后重新同步 canonical/dogfood runtime，重跑完整 Phase 2、创建新的 task commit sequence，并由新的 finding closure/final review 链审查。
- 状态：open，阻塞。

### P3

无。

任意 P0/P1/P2/P3 finding 均阻塞，本报告不做降级处理。

## 五、观察项

1. Exact feature-ref remote marketplace verification 正确留待 reviewed content push 后的 finish-work gate；public latest/canary sample 不能替代。
2. 审查时两个 task-local metadata 文件处于未提交状态：`agent-assignment.json` 与 `task-commit-plans/001.json`。它们是 commit/review 编排结果，不属于 committed implementation diff；main session 仍需在 gate 记录前验证 freshness。
3. Issue #125 的真实 acceptance evidence 尚未写入 ledger；这是 publish 前必做项。

## 六、后续候选

无独立范围外候选。F-001 属于当前已批准机器合同范围，必须在当前任务闭环，不能转为 follow-up。

## 七、最终结论

- `findings_count: 1`
- finding 分布：`P0=0, P1=0, P2=1, P3=0`
- reviewed_head：`e4937dfe19c9e3d889144ca5ef9d7afd42a429b5`
- 结论：`blocked`
- 理由：F-001 使 source/installed validation 与 runtime invocation 对同一 command mapping 的客观判断不一致，当前 Branch Review Gate 不得通过。
