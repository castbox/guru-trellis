# #93 实施计划：planning ambiguity scanner

## 前置检查

- [x] 已读取 issue #93 正文。
- [x] 已读取 #83 archived task artifact，确认现有 planning ambiguity review gate 边界。
- [x] 已对照 Trellis 官方 custom workflow 与 spec marketplace 文档。
- [x] 已读取 `trellis-meta`、`trellis-brainstorm` 和本仓库 workflow/spec 说明。
- [ ] 用户完成 post-planning approval 后，记录 `planning-approval.json` 并进入实现。

## 实施步骤

1. 更新 scanner/data contract 常量。
   - 扩展 `PLANNING_AMBIGUITY_CONTROLLED_TERMS` 为 v2 词表。
   - 新增 `PLANNING_AMBIGUITY_SCAN_SCOPE`。
   - 新增分类白名单常量。
   - 保持 canonical 与 dogfood Python 脚本一致。

2. 实现 deterministic scanner。
   - 新增扫描三份 planning artifacts 的 helper。
   - 新增 `--normative-hit` 解析和分类合并逻辑。
   - `record-planning-approval` 在写入前扫描正文并写入 `scan_scope`、`hits`、`unchecked_normative_hits`。
   - 未分类或 `contract_violation` 命中阻塞写入。

3. 扩展 validator。
   - `check-planning-approval` 重新扫描三份 planning artifacts。
   - 校验 artifact 中 `controlled_terms`、`scan_scope`、`hits`、`unchecked_normative_hits` 与当前扫描结果一致。
   - 保留 #83 的 reviewer、summary、status、checked dimensions、digest freshness 校验。

4. 更新 unit tests。
   - v2 词表完整性。
   - canonical / dogfood 词表一致性。
   - `推荐`、`可选`、`至少`、`默认` 阻塞路径。
   - 八类允许分类通过路径。
   - `至少`、`默认`、`可选`、`相关` 缺少确定性信息时作为 `contract_violation` 阻塞。
   - artifact 手工篡改或 planning docs 变化时 `check-planning-approval` 阻塞。
   - 旧 #83 缺失 ambiguity evidence 与旧 schema 阻塞测试继续保留。

5. 更新 workflow 与 durable docs。
   - `trellis/workflows/guru-team/workflow.md`
   - `.trellis/workflow.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - `docs/requirements/requirement-main.md`
   - `docs/requirements/guru-team-trellis-flow.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/data-contracts.md`
   - `.trellis/spec/workflow/companion-scripts.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/preset/overlay-guidelines.md`

6. 更新 preset overlays 并同步 dogfood。
   - 修改 canonical overlay 中 planning、before-dev、continue、implement/check entry 文案。
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
   - 逐个处理 `.new` / `.bak`，若出现则记录原因。

7. 自举刷新 planning approval evidence。
   - 实现 scanner 后，若当前 task 三份 planning artifacts 未变化，用同一 post-planning confirmation 重新运行 `record-planning-approval`，写入新版 scanner evidence。
   - 若 planning artifacts 变化，重新展示三份链接并等待 fresh confirmation。
   - 重新运行 `check-planning-approval.sh --json --task .trellis/tasks/07-10-093-planning-ambiguity-scanner`。

8. Phase 2 check 与提交前验证。
   - 运行 targeted unit tests。
   - 运行 Python compile、Bash syntax、JSON validation。
   - 运行 `task.py validate`。
   - 运行 workflow phase context read。
   - 运行 `git diff --check`。
   - 记录 Phase 2 check evidence 后提交。

## 验证命令计划

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m json.tool trellis/index.json
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-093-planning-ambiguity-scanner
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.5
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

如时间或环境无法完成 throwaway install，最终报告必须列出未覆盖的开箱即用 / upgrade-update gate。

## Review Gate 范围

Branch Review Gate 必须覆盖：

- `origin/main...HEAD` 完整 diff。
- Python scanner / validator / recorder 实现。
- canonical 与 dogfood 脚本一致性。
- workflow / README / durable docs / spec / overlay 文案一致性。
- 单测覆盖 issue #93 验收标准。
- `planning-approval.json` 自举 evidence 是否通过新版 validator。
- preset apply / dogfood drift 结果。
- 部署、安全、secret、CI/CD、容器、K8s、DB migration、Makefile 影响判断。

## 回滚点

- commit 前：直接还原本任务改动。
- commit 后：revert PR 恢复 #83 行为；target repo 已生成的新字段不含 secret，旧脚本会忽略额外字段，但进入实现仍按当时 workflow gate 重新确认。
