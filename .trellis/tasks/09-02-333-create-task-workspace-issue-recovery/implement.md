# #333 Implementation Plan

## 1. Pre-implementation Gates

- [ ] Live Issue #333 仍是 Open，title/body identity 与 Planning authority一致。
- [ ] Base、task branch、worktree 和 task status仍与 approved Planning identity一致。
- [ ] Planning wording profile=`planning_artifacts` 返回 `pass`。
- [ ] Normal-scenario profile=`planning_scenario_set` 返回 `classified`。
- [ ] Architecture planning result返回 fresh `baseline_current/no_architecture_impact`。
- [ ] `guru-approve-task-plan` 返回 `approved`。
- [ ] 用户在最终 planning summary 之后发送新的实现确认。
- [ ] 仅在上述 gate 完成后运行 `task.py start`。

## 2. Canonical Runtime

- [ ] 在 canonical `runtime/execute.py` 把 command execution 与 output decoding分离。
- [ ] 新增 strict JSON read/list decoder；保留 `invalid_json` behavior。
- [ ] 新增 strict canonical Issue URL text decoder；只消费 `gh issue create` stdout。
- [ ] 新增 exact reviewed-draft open-Issue lookup，绑定 capture time、title、body、labels 和 state。
- [ ] 实现 0=create once、1=recover、>1=fail closed。
- [ ] 抽取 shared live reread/binding helper，让 create 与 recover产生同一 binding/result shape。
- [ ] 保持 existing Issue mutation boundary 与 workspace/task code path不变。
- [ ] 保持 result schema、public interface、typed exits、consumer IDs不变。

## 3. Canonical Contract And Tests

- [ ] 更新 package contract，明确 command-declared output format、search completeness 和 retry semantics。
- [ ] 替换 reviewed-draft test 中 `{"url": ...}` JSON create mock。
- [ ] 增加 strict JSON/plain-text adapter tests。
- [ ] 增加 0/1/>1 exact candidate matrix。
- [ ] 增加 999-row exhausted success 与 1000-row completeness blocked tests。
- [ ] 增加 title/body/labels/state/capture mismatch matrix。
- [ ] 增加 stateful fake-`gh` partial-success retry scenario，断言 cumulative create count=1。
- [ ] 增加 live binding 和 checker drift regressions。
- [ ] 保留 issue-only、current workspace、worktree workspace、reuse 和 zero-write regressions。

## 4. Docs SSOT Execution

- [ ] 先更新 canonical package contract。
- [ ] 检查 `.trellis/spec/workflow/workflow-contract.md` 的 `gh` output prose；只在其声称全部 stdout
  是 JSON时修改。
- [ ] 检查 `.trellis/spec/workflow/companion-scripts.md` 与 `quality-guidelines.md`；只在 current durable
  contract无法覆盖本 task 的 recovery/test ownership时修改。
- [ ] 不修改 Requirements/Design/Test current version body，不创建 RDT contribution。
- [ ] 不修改 Architecture shared current，不创建 Architecture contribution 或 ADR。
- [ ] 不修改 public README、workflow README 或 preset README，除非实现发现 user-visible command/route变化；
  该发现触发 Planning re-entry。

## 5. Projection And Installation Consistency

- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
- [ ] 核对 canonical 与 `.trellis/guru-team/skills/packages/guru-create-task-workspace/**` affected bytes。
- [ ] 核对 `.agents`、`.codex`、`.claude`、`.cursor` affected contract copies。
- [ ] 运行 upstream ownership、source/installed package contract 和 dogfood drift checks。
- [ ] 扫描 recursive `.new`/`.bak`，count必须是0。
- [ ] 核对 executable modes未漂移。

## 6. Validation Commands

先用 live repository discovery确认 runner路径，再执行下列 focused set：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  trellis.skills.guru-team.packages.guru-create-task-workspace.tests.test_contract \
  trellis.skills.guru-team.packages.guru-create-task-workspace.tests.test_runtime

PYTHONDONTWRITEBYTECODE=1 python3 \
  trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py --help

python3 -m py_compile \
  trellis/skills/guru-team/packages/guru-create-task-workspace/runtime/*.py

trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

Implementation phase补充 existing installed verifier 的真实 supported invocation；`--help` 只验证 CLI
discovery，不计入 behavior PASS。

## 7. Phase 2 Evidence

- [ ] Source package contract/runtime suite PASS。
- [ ] Installed dogfood package suite PASS。
- [ ] Fake-`gh` partial-success retry PASS，create count=1。
- [ ] Existing issue-only route PASS。
- [ ] Workspace/task-only current/worktree routes PASS。
- [ ] Canonical/installed/platform parity PASS。
- [ ] Preset apply、ownership、drift、mode 和 recursive sidecar checks PASS。
- [ ] Python compile 与 `git diff --check` PASS。
- [ ] `guru-check-task` 独立审查完整 task scope 与 before/after behavior。

## 8. Stop And Re-entry Conditions

- Live Issue #333、base、task scope 或 planning content material drift。
- 实现需要改变 public schema、typed exit、consumer、Skill id 或 result shape。
- Exact recovery需要 raw API、MCP、App、browser 或 PATH workaround。
- Search completeness无法在 supported `gh` CLI path中证明。
- 实现发现 owner、persistence、SDK、external boundary、single-writer 或 compatibility exit变化。
- Canonical/installed/platform projection无法收敛且产生未处理 sidecar。
- 任何 stop condition 触发 Planning/Architecture owner fresh re-entry，禁止继续实现。

## 9. Explicitly Unverified Boundary

- #249 staged replacement 与 #247 cutover。
- #267 exact-candidate multi-platform release matrix。
- Annotated tag、GitHub Release、tag-pinned smoke。
- Business repository production proof。
- Hostile-input、lock、TOCTOU、concurrency stress、fault injection 和 crash-consistency hardening。
