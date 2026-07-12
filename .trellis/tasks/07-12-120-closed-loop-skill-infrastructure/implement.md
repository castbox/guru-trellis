# #120 实现计划

## 1. 实现前门禁

- [ ] 展示并取得 `prd.md`、`design.md`、`implement.md` 的 explicit post-planning confirmation。
- [ ] 记录并校验 schema 1.2 `planning-approval.json`，保证 `ambiguity_review.status=passed`、`unchecked_normative_hits=[]`。
- [ ] 运行 `task.py start` 后再派发 `trellis-implement`。
- [ ] 运行 `trellis-before-dev`，加载 workflow、preset、docs spec 和当前 task context。
- [ ] 验证 workspace boundary，禁止向 source checkout 写 task artifact。

## 2. Durable Docs SSOT

- [ ] 更新 `docs/requirements/README.md`、`requirement-main.md` 与 `guru-team-trellis-flow.md`，定义公共 skill 基础设施的产品/流程合同。
- [ ] 新增 `.trellis/spec/workflow/skill-package-contract.md`，并更新 workflow/preset/docs spec index 和交叉引用。
- [ ] 更新 `.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/docs/public-docs.md`。
- [ ] 更新根 README、workflow README、preset README，写清 marketplace/preset 分工、安装、upgrade/update、conflict 和作者指南。
- [ ] 在代码前复核 docs 对 canonical root、registry/interface、marker、hash state machine 和 validator command 的定义一致。

## 3. Canonical registry 与 schema

- [ ] 创建 `trellis/skills/guru-team/registry.json`，只登记 `guru-create-work-commit` 为 reserved。
- [ ] 创建 `skill-registry.schema.json` 与 `skill-interface.schema.json`。
- [ ] 建立 test-only representative active package 和 invalid fixtures；production registry/package 不包含 fixture id。
- [ ] 更新 `trellis/guru-team-extension.json` 的 version、managed paths、artifact/schema/command public API。

## 4. Validator

- [ ] 在 canonical Python runtime 实现 `check-skill-packages --mode source|installed`。
- [ ] 新增 `check-skill-packages.sh` wrapper，并纳入 preset managed assets/executable 清单。
- [ ] 实现 registry/package/interface/schema/path/id/marker/exit mapping 的 objective checks。
- [ ] 实现 installed manifest、selected platform、file hash、executable bit、drift、sidecar checks。
- [ ] 保证错误输出不暴露文件内容、secret 或绝对路径。

## 5. Preset 分发与 manifest

- [ ] 扩展 installer，从 canonical root 安装 `.trellis/guru-team/skills/`。
- [ ] 将 active package 分发到 shared root 和已选择 platform roots；未选择平台不得创建。
- [ ] 实现 previous managed hash 状态机：missing、unchanged、known upgrade + `.bak`、unknown/invalid + `.new`。
- [ ] 扩展 installed extension manifest，记录 registry/package/destination hashes 和 platform selection。
- [ ] 公共 skill copy 禁止使用 overlay heuristic overwrite。
- [ ] 保持现有 user-owned `.trellis/guru-team/config.yml` 和 overlay 冲突语义不变。

## 6. Workflow 与 dogfood 同步

- [ ] 在 canonical workflow 写入公共 skill authoring/marker/fail-closed 合同，不添加 reserved skill route。
- [ ] 同步 `.trellis/workflow.md`。
- [ ] 运行 canonical preset apply `--repo . --all-platforms`，生成 dogfood installed registry/schema/wrapper/manifest。
- [ ] 逐个处理 `.new` / `.bak`，不得提交未解释 sidecar。
- [ ] 运行 `check-dogfood-overlay-drift.sh`，结果必须通过。

## 7. 自动化测试

- [ ] 增加 registry/interface/route/installed validator unit tests。
- [ ] 增加 installer managed hash、invalid provenance、platform selection 和 fixture discovery tests。
- [ ] 运行 targeted Python unittest、`py_compile`、`bash -n`、JSON/schema 校验。
- [ ] 运行 `check-skill-packages --mode source` 和 dogfood `--mode installed`。
- [ ] 运行完整现有 preset/companion test suite，修复回归。

## 8. 开箱即用与 upgrade/update

- [ ] 扩展并运行 clean throwaway verifier，覆盖 workflow init、preview、switch 与 preset apply。
- [ ] 在 throwaway 中验证 representative active fixture 的 shared/Codex/Cursor/Claude discovery，但 production install 不得包含 fixture id。
- [ ] 执行 `trellis update --force`、workflow reapply、preset reapply 和 installed validation。
- [ ] 最终递归扫描 `.new` / `.bak`，结果必须为空。
- [ ] 远端 current-ref marketplace 验证必须在 branch push 之后执行；Phase 2 报告必须明确 local throwaway 覆盖与待 finish-work verifier 项，禁止提前宣称 remote branch 通过。

## 9. Phase 2 Check 与提交边界

- [ ] 派发独立 `trellis-check`，覆盖 R1-R8、AC1-AC12、Docs SSOT、公共 API、source/installed validator、platform drift、throwaway、security。
- [ ] 所有 finding 必须由实现代理修复并由 checker 复验关闭。
- [ ] 只 stage #120 的 durable docs、canonical package/schema、workflow/preset、dogfood installed copy、tests 和 task evidence。
- [ ] 不 stage source checkout 文件、其它 worktree 状态、未处理 sidecar 或无关用户改动。
- [ ] commit/push/PR/issue close 继续按 Phase 3、Branch Review Gate 与 `trellis-finish-work` 执行。

## 10. 验证命令清单

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-12-120-closed-loop-skill-infrastructure

python3 -m unittest \
  trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py

python3 -m py_compile \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py

bash -n trellis/presets/guru-team/scripts/bash/apply.sh
bash -n trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
bash -n trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh

trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed

git diff --check
git status --short
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

## 11. 风险与回滚点

| 风险 | 阻断/回滚点 |
| --- | --- |
| Installer 误覆盖用户 skill | unknown/invalid provenance fixture 必须证明 target 保留且只生成 `.new`；失败则回滚 installer 变更 |
| Reserved fixture 泄漏到 production | production install 断言发现 fixture id 即失败 |
| Workflow marker 与 interface exit 漂移 | source validator 在 preset apply 前阻断 |
| `trellis update` 恢复旧平台文件 | throwaway 必须在 update 后重放 workflow/preset 并通过 installed validation |
| Dogfood 与 canonical 漂移 | apply + drift checker 不通过时不得进入 Phase 2 pass |
| 公共 API 静默破坏 | extension manifest/version 和 durable migration contract 缺失时不得提交 |
