# Issue #125 F-001 Finding 修复交接

## 1. 身份与边界

- 逻辑角色：`实现代理`
- 技术身份：`/root/trellis_fix_125_f001`
- Finding：Round 001 / P2 / F-001
- Working HEAD：`e4937dfe19c9e3d889144ca5ef9d7afd42a429b5`
- Worktree：Issue #125 独立 worktree；workspace boundary 与 planning approval 均为 `ok`
- 禁止动作：未 commit、push、创建 PR、archive，未运行任何 review/recorder/gate recorder
- 冻结 artifact：未修改 `prd.md`、`design.md`、`implement.md`、Round 001 raw review、`review.md`、`review-gate.json`、issue ledger、agent assignment 或既有 task commit plan

## 2. F-001 Root Cause

`validate_skill_interface()` 对 validator `runtime_command` 只校验：

1. 字段为合法 route id；
2. command 出现在 extension manifest 的 `companion_scripts[]`。

`run-skill-command` dispatcher 本身按合同必须出现在该 published inventory，因此
`runtime_command=run-skill-command` 能通过 source validation。另一方面，
`resolve_skill_runtime_command()` 已明确拒绝 validator target 等于 dispatcher。结果是同一个
interface 能先通过 source/installed validation 与分发，再在 standalone 调用时 blocked，source
validator 与 runtime resolver 的机械语义不一致。

## 3. 修复内容

### 3.1 Canonical runtime

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - 新增共享判定 `skill_runtime_command_maps_to_dispatcher()`；比较 validator
    `runtime_command` 与当前 interface `runtime_dependency.dispatcher`。
  - source/interface validator 命中 self-mapping 时追加唯一、稳定的错误：
    `runtime_command must not equal runtime_dependency.dispatcher`。
  - runtime resolver 改为复用同一判定，避免 source 与 invocation 再次漂移。

### 3.2 Permanent negative regression

- `trellis/skills/guru-team/tests/test_skill_packages.py`
  - 新增 `test_validator_runtime_command_cannot_self_map_to_dispatcher`。
  - Fixture 把 validator `runtime_command` 改为 interface 自身 dispatcher；该值仍符合 schema
    pattern 且属于 published companion inventory，因此验证的是 cross-field semantic 约束。
  - 测试精确断言完整 `errors` 数组只含 self-mapping 错误，不接受“存在任意 errors”的泛化断言。

### 3.3 Dogfood runtime

- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - 由 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 从 canonical
    source 生成同步，没有手工维护第二份语义。
  - Apply 生成的旧受管 runtime `.bak` 已先确认与 `HEAD` 旧文件字节一致，再清理。
  - Apply 产生的非语义 `installed_at`、source HEAD 与 backup-list manifest 噪声已移除；未扩大
    production manifest 或平台 package 范围。

Production interface 保持不变：

- `candidate_validator -> check-commit-messages`
- `exact_executor -> create-task-commit`
- dispatcher 仍为 `run-skill-command`

## 4. Changed Files

本代理新增/修改的路径只有：

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
3. `trellis/skills/guru-team/tests/test_skill_packages.py`
4. `.trellis/tasks/07-14-125-skill-standalone-runtime-dependency/finding-fix-handoff-001.md`

工作区中既有 `agent-assignment.json`、`task-commit-plans/001.json`、Round 001 review artifacts
属于 main session/前序 review metadata，本代理未修改、覆盖或清理。

## 5. 验证结果

### Tests

- 精确 F-001 targeted regression：1 test passed。
- Canonical package contract：5 tests passed。
- Skill package suite：65 tests passed；原 64 tests 加本次 1 个永久 regression。
- Preset installer suite：36 tests passed。
- Shared runtime suite：275 tests passed。
- 四个完整 suite 合计：381 tests passed。

### Contract、sync 与 workspace

- `check-skill-packages.sh --json --mode source`：passed。
- `check-skill-packages.sh --json --mode installed`：passed；43 managed files，0 sidecar、
  0 removal、0 conflict。
- `check-dogfood-overlay-drift.sh`：passed。
- Canonical 与 dogfood `guru_team_trellis.py`：字节完全一致。
- Canonical 与 dogfood Python runtime `py_compile`：passed。
- `check-workspace-boundary.sh --json`：`status=ok`，source checkout clean，0 suspicious artifact。
- `check-planning-approval.sh --json`：`status=ok`，三份 planning digest 未变化。
- Recursive `.new` / `.bak` scan：0。
- `git diff --check`：passed。

## 6. Docs SSOT Judgment

- 批准策略仍为 `ssot_first`。
- Durable specs 已要求 source/installed validation 在分发前绑定 runtime dependency、published
  target command 与 fail-closed invocation；Round 001 也已判断 F-001 是机器合同实现缺口，
  不是 durable 文档缺失。
- 本修复只让 source validator 与既有 runtime resolver/SSOT 语义一致，没有新增或改变 public
  mode、schema、runtime API、installer、remediation、typed exit 或 upgrade 合同。
- 因此无需修改 `.trellis/spec/**`、durable requirements、public README 或 planning artifacts；
  task-history-only 内容保留在本 handoff 和后续 review evidence。

## 7. 安全与部署影响

- 安全：新增逻辑只比较已解析 interface 中两个稳定 id，不读取任意 runtime path，不改变
  executable 映射，也不输出 secret、token、private key、签名 URL、`.env`、数据库 URL、客户
  数据或本机绝对路径。
- Fail-closed 时机提前到 source validation；没有新增 fallback 或业务副作用。
- 部署：不改变服务、API、CLI 业务入口、worker、schedule、queue、数据库 migration、CI/CD、
  Dockerfile、Compose、Kubernetes/Kustomize/Helm 或 Makefile；部署形态不变。

## 8. Remaining Risks

1. 本报告不是 Phase 2 check。代码、generated runtime 与测试发生变化后，必须由新的独立
   `阶段二检查代理` 对完整 Issue #125 范围重新执行 Phase 2，并生成 fresh evidence。
2. Phase 2 通过后必须创建新的 task-local commit plan sequence，不能复用 sequence 001；由
   main session mandatory invoke `guru-create-task-commit` 创建 revision commit。
3. F-001 finding owner `/root/trellis_final_review_125` 只能作为 `问题闭环审查代理` 复核 closure；
   之后仍需从未参与前序 round 的全新 `最终放行审查代理` 完成 fresh final review。
4. Exact feature-ref remote marketplace verification 仍只能在 reviewed content push 后由
   `trellis-finish-work` 完成；public canary 不能替代。
5. #125 仍 stacked 于 PR #124；若 #124 合并并 retarget 到 `main`，必须按新 base 重新执行
   freshness-sensitive Phase 2、Branch Review 与 remote marketplace verification。
6. Issue #125 `acceptance_evidence[]` 仍需 main session 在 publish 前依据真实验证补齐；本代理
   按边界未修改 issue ledger。

## 9. Phase 2 Focus

- 精确复现 fixture self-mapping，确认 schema/published membership 仍合法但 source semantic
  validation 只返回指定 self-mapping error。
- 确认 production mappings 未变化，source 与 runtime resolver 共用 dispatcher 判定。
- 覆盖 canonical source、dogfood runtime、source tests 与完整 stacked-base diff；不要只检查
  最新三行判断。
- 复验 5/65/36/275 suites、source/installed validation、dogfood drift、canonical/dogfood bytes、
  recursive sidecars 和 `git diff --check`。
- 复核 Docs SSOT no-change judgment、安全、部署以及 exact remote verification/stacked base 限制。
