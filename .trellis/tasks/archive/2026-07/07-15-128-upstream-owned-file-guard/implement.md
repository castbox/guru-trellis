# #128 实现计划

## 1. 前置门禁

- [ ] 再次运行 workspace boundary check，确认编辑根目录是 issue #128 worktree。
- [ ] 运行 planning approval validator；未通过时实现代理必须停止。
- [ ] 读取 `prd.md`、`design.md`、本文件、preset/workflow/docs specs 与 research evidence。
- [ ] 确认两个 workflow 文件和 43 个 overlay 的 base hashes，建立实施前非回归快照。

## 2. Durable SSOT first

- [ ] 新增 `.trellis/spec/preset/upstream-ownership.md`，写入四类 ownership、frozen baseline、迁移状态、script boundary、update/upgrade 与 gate checkpoint。
- [ ] 更新 `.trellis/spec/preset/index.md`、`installer.md`、`overlay-guidelines.md`，移除“新增 upstream override 是常规扩展面”的含义，保留当前 legacy 行为事实并标注冻结。
- [ ] 确认 durable spec 已覆盖 `design.md` 的 Docs SSOT Plan 后，再编写 validator。

## 3. Inventory 与 schema

- [ ] 新增 ownership JSON Schema，使用 closed objects、明确 enum、required fields、path/hash/issue number constraints。
- [ ] 生成 43 条 frozen legacy entry，填入 base commit SHA-256、upstream producer、current behavior、replacement owners、blocking/removal issues、update/upgrade、dogfood、business repo 字段。
- [ ] 记录 37 条 current generated 与 6 条 legacy Codex not-generated 状态。
- [ ] 记录 extension manifest managed claims 与 Guru-owned anchored rules。
- [ ] 计算并写入 sorted path-set digest 与 active payload aggregate digest。

## 4. Validator 与命令入口

- [ ] 新增 `validate_upstream_ownership.py`，实现纯读取、结构化 JSON 输出和稳定错误 code。
- [ ] 新增 `check-upstream-ownership.sh` thin wrapper；wrapper 只传递参数与退出码。
- [ ] 校验 schema/inventory、43 条 frozen baseline、active hash、状态矩阵、manifest managed claims、installer managed destination、skill ids 与 Guru discovery rules。
- [ ] 在 `apply_guru_team_trellis_preset.py` 的首个 target mutation 前调用 validator。
- [ ] 增加 target mutation sentinel 测试，证明 validator 失败时 target tree 不变。

## 5. Fixture 与测试

- [ ] 新增 positive baseline 与 Guru-owned path fixtures。
- [ ] 新增 upstream overlay、expanded legacy、payload drift、missing owner/removal、unclassified negative fixtures。
- [ ] 新增 validator 单元测试，校验 status、exit code、错误 code、path 与 facts digest。
- [ ] 扩展 preset installer 测试，覆盖 pre-mutation gate。

## 6. Validation chain 接入

- [ ] 在 `check-dogfood-overlay-drift.sh` 接入 ownership gate，保留原 missing/changed 行为。
- [ ] 在 `verify-throwaway-install.sh` 的 initial apply、update 后、reapply 后 checkpoint 接入 gate。
- [ ] 确认 gate 未出现在 workflow、Skill package、platform entry 或业务 task runtime 调用链。

## 7. Public docs

- [ ] 更新 `README.md`，说明 upstream-owned path 冻结、maintainer command 与 upgrade/update 责任。
- [ ] 更新 `trellis/presets/guru-team/README.md`，说明 inventory、pre-mutation gate、fixture 与 throwaway checkpoint。
- [ ] 更新 `trellis/workflows/guru-team/README.md`，说明 workflow authoring 只能使用 Markdown route 与 `guru-*` packages，不得新增 upstream overlay。

## 8. 验证命令

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/skills/guru-team/tests/test_skill_packages.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --exit-code 291b57b6c02872320a4dce0626a2f718399b8f56 -- trellis/workflows/guru-team/workflow.md .trellis/workflow.md
git diff --exit-code 291b57b6c02872320a4dce0626a2f718399b8f56 -- trellis/presets/guru-team/overlays
```

若完整 throwaway 因远端 marketplace branch 尚未 push 而只能使用 public sample，Phase 2 报告必须明确该限制；finish-work 的 remote marketplace verification 必须在 branch push 后补齐 exact branch evidence。

## 9. Phase 2 检查重点

- [ ] Requirements：R1-R7 与 AC1-AC8 全部建立代码、测试或文档证据。
- [ ] Design：inventory 状态矩阵、anchored classification、pre-mutation gate 与 fixture 设计没有平行实现。
- [ ] Docs SSOT：durable spec 先于 validator，README 与 spec 一致，task delta 已合并。
- [ ] Cross-layer：schema、inventory、validator、installer、dogfood、throwaway、manifest claims 完整连通。
- [ ] Non-regression：workflow、43 overlay payload、两个 public Skill packages、upstream discovery semantics 无 diff。
- [ ] Deployment：无 API service、CLI runtime、worker、queue、DB migration、Docker、Compose、Kubernetes、Kustomize、CI workflow 或 Makefile 形态变化；本次只增加 source maintainer gate。
- [ ] Safety：无 secret、token、private URL、`.env` 或客户数据写入 fixture、日志、task artifact。

## 10. 回滚点

- Inventory/schema 无法覆盖 43 条记录时，停止在第 3 节，不接入 installer。
- Validator 出现语义判断时，删除该分支并把判断移回 durable spec/AI Review Gate。
- Apply/dogfood/throwaway 任一阶段改变 overlay payload 或 workflow，恢复该阶段改动并重新执行完整 Phase 2。
- 发现 scope 需要修改现有 Skill/runtime routing 时，停止 #128，将变化路由到 #129、#130、#131 或 #132。

## 11. 完成出口

- 实现代理提交 implementation handoff，明确 changed files、R1-R7 承接、Docs SSOT merge、验证状态、未验证项与风险。
- Phase 2 检查代理形成完整 task-scope 结论后，主会话记录 `phase2-check.json`。
- 主会话调用 `guru-create-task-commit`，不得直接绕过 commit Skill。
- 独立 Branch Review 必须检查 `origin/main...HEAD` 完整 diff，并明确记录 runtime routing、Skill behavior、platform trigger、invocation scope 无变化。
- Branch Review Gate 通过后，本会话停止在显式 `trellis-finish-work` 入口前。
