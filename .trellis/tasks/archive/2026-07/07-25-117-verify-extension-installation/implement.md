# #117 实施计划：`guru-verify-extension-installation`

## 1. 执行原则

- 只在用户看过三份 planning artifacts 并再次明确确认、`planning-approval.json`
  schema 2.0 checker 通过、`task.py start` 完成后进入实现。
- 实现由 `trellis-implement` 独立 agent执行，Phase 2 由 `trellis-check` 独立 agent
  审核；主会话只协调和消费 handoff。
- 每次编辑前读取 current canonical source；不得修改 Trellis upstream、全局 npm 或
  `node_modules`。
- 每个实现批次同时维护 canonical source 与 durable docs；task artifacts 不取代 Docs
  SSOT。

## 2. 有序实施清单

### Phase A：合同与 package skeleton

- [ ] 基于 `guru-review-task-publication` 的 Interface 1.3 package pattern，新建
      `guru-verify-extension-installation` canonical package。
- [ ] 编写 `SKILL.md` 与 `references/contract.md`，固定 semantic stages：
      forward behavior -> AI Review Gate -> conditional human confirmation ->
      recorder/validator -> typed exit。
- [ ] 定义 `verification_required` workflow input schema/example/fixture。
- [ ] 定义 structurally distinct `standalone_verification` input schema/example。
- [ ] 定义 `verified`、`not_required`、`return_to_task_work`、`blocked` 四个
      `exit_id` output schema/example；每个 schema用 closed `oneOf` 固定 workflow
      handoff与 standalone session report分支。
- [ ] 定义 workflow/stop consumer schemas 与 deterministic projections。
- [ ] 定义 package-owned private `marketplace-verification.json` schema。
- [ ] 更新 `interface.json`，声明 private artifact、platform destinations、eval
      bindings、runtime dependency、re-entry 与 unique consumers。
- [ ] 编写 package contract tests，先证明 schema/example/projection/discovery
      contract闭合。

验证：

```bash
python3 -m unittest \
  trellis.skills.guru-team.packages.guru-verify-extension-installation.tests.test_contract
```

实际 Python module 路径若因连字符无法 import，则使用 package 当前统一的 direct test
runner命令；不得新增第二套 test harness。

### Phase B：Runtime 分层与 private evidence

- [ ] 将 `marketplace_verification_required` 收敛为 changed-surface facts provider，
      删除其 semantic route authority。
- [ ] 将 `execute_marketplace_verification` 拆成 preflight、profile executor、
      recorder、checker 可复用函数，保持一个 runtime implementation。
- [ ] 新增 dispatcher command ids与 package wrappers：
      record、check、execute、public invoke。
- [ ] Recorder 只接收已完成的 AI applicability/profile/adequacy/findings/route，重建
      current machine facts 后写 owner result。
- [ ] Checker 校验 schema、task/workspace、plan/ref/HEAD、remote、redaction、
      consumer、retry/supersession 与 actual exit。
- [ ] 无 task standalone 使用 stdout/session-only result；验证前后 repository
      verification artifact inventory相同，且 task-work route不可达。
- [ ] Top-level compatibility wrapper若仍有 current consumer，改为 dispatch 到同一
      runtime command。
- [ ] 更新 canonical marketplace verification schema路径与 extension artifact
      inventory，避免存在两个 private schema owner。

验证：

```bash
python3 -m unittest \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
```

定向测试必须覆盖 early failure、partial failure、exit 0 + adequacy failure、remote HEAD
drift、session-only、stale/retry 和 redaction。

### Phase C：Clean-install executor

- [ ] 参数化 remote repo/ref 与 closed capability catalog。
- [ ] 执行 remote HEAD freeze、safe URL normalization、clone HEAD复验。
- [ ] 在独立 new/existing temp repo执行 marketplace index、init、preview、switch。
- [ ] 执行 preset initial apply/reapply、Trellis update、再次 workflow select/apply。
- [ ] 校验 packages、schema、config、scripts、executable modes 和 platform copies。
- [ ] 校验 `.new/.bak`、managed hashes、obsolete/ownership inventory。
- [ ] 校验 #128 upstream/Guru owner边界与 frozen `transitional_legacy`。
- [ ] 将 README command转成真实执行 assertion；文档命令变化时 test同步失败。
- [ ] 只保留 sanitized argv、exit code、digest、size 与 asset digest；清理 temp repo/raw
      logs。

验证：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

实现期间先运行 profile定向 fixture；Phase 2 必须运行完整 throwaway。

### Phase D：Registry、workflow 与分发

- [ ] Registry 新增 active Interface 1.3 package，`guru-finalize-task` 保持 planned。
- [ ] Extension manifest 更新 active ids、package file/hash inventory、private artifact、
      schema 与 runtime command。
- [ ] 更新 canonical workflow 中 contract graph 所需 marker/target/route；不激活
      #118 producer edge，不提前实现 #119 integration。
- [ ] 同步 `.trellis/workflow.md` dogfood copy。
- [ ] 更新 preset installer/package manifest，使 package分发到 installed/shared/Codex/
      Claude/Cursor roots。
- [ ] 更新 source/installed package validator 与 live-registry closure，按 actual graph
      计算 invoke/exit/target counts。
- [ ] 更新 #146 migration/closure regression，使新增 active Interface 1.3 package通过
      `new` closure path；不改写已发布 migration identity。
- [ ] 运行 preset apply，同步 dogfood copy，逐个处理 `.new/.bak`。

验证：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
```

### Phase E：Production eval

- [ ] 建立 workflow/standalone、四 exits、retry/unavailable package-local corpus。
- [ ] 每个 semantic case引用 checker-passed owner result并调用 real public wrapper。
- [ ] Actual exit先选择 output schema；返回后再比较 `expected_exit`。
- [ ] 为 `verification_required` target bootstrap加入完整 public-wrapper eval。
- [ ] Shared/Codex/Claude/Cursor adapters解析 byte-identical corpus。
- [ ] 断言 Codex trusted Git root、Claude input protocol、Cursor unsupported和 shared
      parsing。
- [ ] 断言 private evidence字段不进入 native request或 public DTO。
- [ ] Production eval报告明确标注：不替代 remote clean install、AI adequacy、redaction
      与 #105 failure matrix。

验证：

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
```

再执行仓库现有 production eval runner中只选择
`guru-verify-extension-installation` 的命令；命令名以 current runtime help为准。

### Phase F：Docs SSOT 同步

- [ ] 更新 `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 的 global
      route contract。
- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md` 的 target bootstrap、
      minimal handoff 与 private state说明。
- [ ] 更新 `.trellis/spec/workflow/companion-scripts.md` 的 verifier runtime边界。
- [ ] 更新 `.trellis/spec/workflow/workflow-contract.md` 的 phase owner边界。
- [ ] 更新 `docs/requirements/README.md`、
      `docs/requirements/requirement-main.md`、
      `docs/requirements/guru-team-trellis-flow.md`。
- [ ] 更新 workflow/preset README的 discovery、standalone invocation、remote clean
      install和 update/reapply说明。
- [ ] Phase 2 handoff列明每个 task delta合并到哪个 durable owner；只把 provenance和
      review evidence留在 task。

### Phase G：完整验证与回归

- [ ] Package unit tests通过。
- [ ] Shared runtime全量 unit tests通过。
- [ ] Source/installed schema、registry、manifest、package、workflow graph通过。
- [ ] Production eval四 exits与两 inputs通过。
- [ ] Redaction fixture与scan通过。
- [ ] Dogfood apply/drift通过，无未处理 `.new/.bak`。
- [ ] Clean throwaway initial install、preview/switch、update、reapply、ownership通过。
- [ ] 从已推送 remote ref执行真实 verification；remote HEAD与 reviewed content
      HEAD。
- [ ] #105 transaction failure matrix现有 tests通过且无改写。
- [ ] `git diff --check`通过。
- [ ] `trellis-check` 对 PRD、design、implementation、tests与 Docs SSOT执行完整
      cross-layer review。

## 3. Phase 2 必检场景

| 场景 | 可观察结果 |
| --- | --- |
| Workflow required + 全矩阵成功 + adequacy通过 | `verified` DTO，private artifact current |
| Standalone 非 extension target | `not_required`，session/task persistence符合输入 |
| 无 task standalone安装或覆盖失败 | `blocked` session report，不伪造 task/plan identity |
| Command全部成功但 profile缺受影响 capability | `return_to_task_work` |
| Remote HEAD与 reviewed HEAD不同 | fail closed，不复用旧 artifact |
| Task修复后旧 evidence | stale，重新进入 publication/push/verification |
| 相同 plan/ref/HEAD transient network retry | 不新增持久化 artifact，完整重试 |
| Auth/network/remote unavailable | `blocked` + stable remediation |
| Secret marker出现在模拟 stdout/stderr/URL | 原文不进入 artifact/wrapper/eval trace |
| `trellis update` 后 upstream entry | 保持官方 bytes/owner |
| Preset reapply | 只恢复 Guru assets |
| Frozen legacy inventory新增一项 | verification失败 |
| 无 task standalone | repo无 verification cache/index |
| Production eval通过但未跑remote install | 完成状态仍为 blocked |

## 4. Review gates

### Gate 1：合同闭合

通过条件：

- 两个 input profile、四个 output schema、examples、consumer inputs、projections、
  private artifact和 eval bindings全部被 source validator发现。
- #118 target bootstrap存在，#118 producer edge未激活。
- Public DTO没有 private字段。

### Gate 2：Semantic/deterministic边界

通过条件：

- AI-authored applicability/profile/adequacy决定 route。
- Runtime只执行、记录、校验。
- Changed-path与exit code均无 `verified` route authority。

### Gate 3：分发与upgrade

通过条件：

- Canonical、installed、Shared/Codex/Claude/Cursor package bytes相同。
- Apply/drift无差异。
- Update/reapply、ownership、sidecar和frozen legacy检查通过。

### Gate 4：双验收

通过条件：

- Production real-wrapper corpus通过。
- 已推送 remote ref的clean installation通过。
- 两份证据分别记录，互不替代。

### Gate 5：Phase 2 check

通过条件：

- `trellis-check` 覆盖当前 task全部 acceptance、normal-path failure matrix、Docs SSOT
  reconciliation和完整 diff。
- 所有 finding关闭或按 typed route退回task work。

## 5. 回滚点

- Contract/package tests未闭合：删除未激活 package skeleton，不改 registry。
- Runtime重构未通过旧回归：恢复到 pre-activation runtime，不保留双实现。
- Registry/manifest/distribution任一不一致：回滚整个 activation unit。
- Apply产生 sidecar：停止，逐项确认 managed conflict，不覆盖用户文件。
- Remote clean install失败：保持 task active，按 finding回到实现；不得创建 PR或归档。

## 6. Docs SSOT checkpoint

采用 `design.md` 唯一 Docs SSOT Plan中的 `ssot_first` 策略。实现 handoff 与 Phase 2
check必须列出：

- 已更新的 durable docs文件；
- 已从 task artifacts合并的行为合同；
- 仅保留为 task history的内容；
- 未更新 owner时的明确 blocker或 follow-up边界。
