# 实施计划

## Docs SSOT Plan

- 决策：`no_docs_update_needed`。
- 理由：现有 `.trellis/spec/workflow/companion-scripts.md` 已拥有 deterministic identity、标准库、错误处理和 fail-closed 边界；Issue #186 修复的是该既有合同下对 deinitialized-clean Gitlink 的错误状态分类，不新增 workflow、public Skill I/O、配置或用户操作合同。
- Phase 3 复核：若实现引入新的长期 helper contract 或改变合法 overlay 语义，则改为更新 `.trellis/spec/workflow/companion-scripts.md`；否则记录无需 durable docs delta 的具体证据。

## 实施步骤

- [ ] 使用 `trellis-before-dev` 加载 workflow/preset 规范和任务上下文。
- [ ] 在 canonical runtime 中分离 recorded Gitlink identity 与 initialized worktree validation。
- [ ] 仅为无 overlay 的 deinitialized-clean 状态保留 recorded OID；其他状态继续 fail closed。
- [ ] 更新 reviewed-content Gitlink 单元测试，覆盖 deinitialized-clean、initialized-clean、initialized-dirty、HEAD-drift、pointer-drift 及歧义 root。
- [ ] 运行目标 Python 测试与完整 companion runtime 测试。
- [ ] 运行 preset `apply.sh --repo .` 同步 installed dogfood copy，处理所有 `.new` / `.bak`。
- [ ] 运行 dogfood overlay drift、Python compile、shell syntax、JSON/schema、task validation 与 `git diff --check`。
- [ ] 在 isolated throwaway 场景执行 task-bearing extension verification，生成并校验 schema 3.0 `marketplace-verification.json`。
- [ ] 由独立 check sub-agent 复核需求、设计、完整 diff、测试与开箱即用/upgrade-update 边界，再调用 `guru-check-task`。

## 重点验证命令

```bash
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-08-186-uninitialized-gitlink-identity
git diff --check
```

## 风险文件与停止条件

- `guru_team_trellis.py` 是多阶段共享 runtime；任何非 Gitlink 路径行为变化都必须停止并缩小 diff。
- 若 deinitialized fallback 需要读取 remote、初始化 submodule、修改 public schema 或绕过 existing overlay binding，停止实施并重新进入需求澄清。
- 若 preset apply 产生未预期的 `.new` / `.bak` 或大范围 dogfood drift，停止并逐项核对 canonical ownership。
