# #220 实施与验证计划

## Phase 1

- [x] 读取 live Issue #220、Issue #52/#129/#161/#164、官方 Trellis workflow/spec marketplace 文档、当前 canonical/dogfood/spec/tests 和 #52 历史实现。
- [x] 确认根因是 workflow-owned `approved -> activation` transition 缺少用户 review pause。
- [x] 明确保留 Skill/public API/schema/runtime，禁止授权持久化和 upstream-owned entry 修改。
- [x] 将分支 fast-forward 到 `origin/main@903bfe13031c69208ae78112ba68593e0f0bf583`，
  合并保留 #237 normal-scenario qualification 与 #236 managed Python throwaway 合同。
- [x] 以 `planning_scenario_set` 资格化 Issue #220 的九类对话回归候选，并由 Planning owner
  独立判断其 acceptance 充分性。
- [ ] 完成 planning wording review 与 `guru-approve-task-plan` semantic review。
- [ ] 展示 `prd.md`、`design.md`、`implement.md`，停在当前 Phase 1 方案确认边界。
- [ ] 确认后才运行 `task.py start` 和派发 `trellis-implement`。
- [x] Phase 2 发现并通过 `implementation_discovery` 资格化 shared eval 缺少 `write_json`
  的正常路径缺陷；因涉及原计划排除的 runtime 范围，已暂停并返回 Phase 1。
- [ ] 将受限 staging helper 纳入当前规划，重新执行 wording/planning review 并展示新方案。

## 实现顺序

1. 修改 canonical workflow：
   - planning breadcrumb 明确 semantic approval 后固定 presentation/pause；
   - `phase-1-task-activation` target 增加三文档、AI 结论、选择/替代/取舍/边界展示要求；
   - 定义肯定、提问、修订、scope change、autonomous 和旧确认失效规则；
   - 保留 consumer id 和既有 base pair/workspace/task-start 链。
2. 修改 `guru-approve-task-plan` canonical SKILL/contract：
   - 删除“checked approved 自动激活/不增加 routine stop”的冲突文案；
   - 明确 Skill pass 与 workflow-owned user pause 是两个独立条件；
   - public input、四 exits、schema 3.0、recorder/checker 不变。
   - 保留 #237 新增的 `planning_scenario_set` 调用和 caller/consumer mapping；不得让
     qualification 结果代替 planning approval 或 Phase 1 review pause。
3. 更新 durable requirements、workflow/preset README 和 canonical preset specs：
   - 记录四/五次 happy-path confirmation budget；
   - 记录修订、autonomous、scope-change 与零授权持久化规则；
   - 说明 upstream-owned platform entry 不修改，平台通过 live workflow和 managed Guru package 一致。
4. 补充 targeted tests/evals，覆盖 Issue #220 Acceptance 11 场景和零授权字段。
5. 运行 preset apply，同步 workflow、spec、installed package 与四个平台 managed copies，
   并重建 extension manifest；逐个处理任何 `.new`/`.bak`。
6. 移除 `guru-approve-task-plan/runtime/common.py` 中本轮临时加入的 `write_json` alias；在
   canonical native adapter 增加受限 production fixture composition，从现有
   `guru-review-task-publication` owner 复用 `write_json`、`load_config`、
   `write_runtime_mappings`，不复制实现或污染 production common。
7. 补 composition ownership/不覆盖既有能力回归，并运行 source/installed Shared、Codex、
   Claude 四出口真实 wrapper eval；Cursor 保持现有未认证 `unsupported`。
8. 将当前 review-branch composition 内的通用 `run_component` 和 planning/check/review command
   bindings 提取为独立 production-owner command composition；在 staging 前仅补缺失 bindings，
   review-branch 复用同一实现，不改变现有 wrapper argv 或 public contract。
9. 补 command composition 单一来源、不覆盖既有 capability、planning 真实 record/check wrapper
   回归，再执行完整 adapter matrix。
10. 修复 `guru-approve-task-plan/runtime/invoke.py` 的 `clarify_scope` projection：直接复制
    schema-valid `scope_proposals` 字符串列表到 `proposal_refs`；补 source/installed 真实
    record/check/invoke 回归，不改变任何 schema、exit 或 consumer。

## 验证命令

- `python3 trellis/skills/guru-team/packages/guru-approve-task-plan/tests/test_contract.py`
- 受影响的 workflow/preset Python tests。
- `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-approve-task-plan --json`
- `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-approve-task-plan --json`
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- source/installed Skill contract、manifest和 managed-copy checks。
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4 --platform codex`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.5 --platform codex`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-15-220-phase1-planning-review-pause`
- `git diff --check`
- `find . -name '*.new' -o -name '*.bak'` 的 scoped 结果复核。
- Clean throwaway install/update：`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`。
- 使用 #236 后 verifier 的 managed Python 路由运行 throwaway，不直接调用未受管 PATH Python
  执行 bootstrap 之后的 helper/test module。
- source/installed 的 Shared、Codex、Claude adapter 各运行四个 declared exits，确认
  adapter transcript 不再出现 `common has no attribute write_json`，并保留真实 wrapper trace、
  exit schema 与 assertion 证据；Cursor 未认证路径只验证 `unsupported`。

## Phase 2 调度

确认后由 `trellis-implement` sub-agent 修改实现与文档；主会话负责协调、必要的 spec
收敛和后续副作用边界。实现完成后由独立 `trellis-check` sub-agent 对完整 task scope、
canonical/generated consistency、测试与未验证边界执行检查。

## 风险与停止条件

- 若需要改变 stable consumer/exit/schema/command，停止并返回 Phase 1 重新审查迁移合同。
- 若 preset apply 触碰 upstream-owned entry、产生未解决 `.new`/`.bak` 或覆盖并行改动，停止处理漂移。
- 若 semantic eval 只能通过 deterministic natural-language parser、修改 public projection/native
  trace receipt 或把更多 eval-only helper 加入 production package 实现，停止并重新审查设计。
- 若继续出现不属于已列明 fixture helper 或现有 planning record/check wrapper binding 的新缺口，
  停止并返回 Phase 1，不按报错顺序继续扩大 composition。
- `clarify_scope` 修复后若任一已声明 exit 仍出现新的 production runtime 或 projection 缺口，
  停止并返回 Phase 1；不得引入宽松兼容输入来绕过当前 schema。
- 若 clean throwaway/update 因环境限制无法完成，明确标记未验证，不能声称开箱即用。
- 任一 finding 导致 scope、authority、重大方案或风险变化时，回到 Phase 1 review pause。
