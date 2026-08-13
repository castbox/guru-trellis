# 实施计划

## 顺序

1. 建立 current consumer inventory：枚举五个 stable boundaries、Finalizer base-only mismatch、Branch Review/Publicaton/Finalizer current schemas/runtime/tests、registry counts 与 installed projections。
2. 定义 `guru-reconcile-task-base` Interface、独立 input/output schemas、六 exits、consumer projections、commands/errors、examples/evals 与 package-local runtime skeleton。
3. 实现 deterministic pair guard、临时 integration candidate executor/checker、owner result recorder/checker 和最小 private checkpoint lifecycle；保持 AI/script 边界。
4. 实现 semantic contract 与 evals，引用 #169 SSOT，覆盖三时钟、影响分类、验证充分性、state matrix 与 fail-closed。
5. 在 canonical workflow 中接入所有 eligible boundaries、单 router 与 mapped exits；同步 dogfood workflow，不复制 step-local internals。
6. 扩展 `guru-review-branch` bounded continuity profile；修改 Check/Commit/Publication/Finalizer 只委托 base-only classification，并新增 Finalizer `base_reconciliation_required`。
7. 实现 current legacy migration adapter，删除被替代、冲突、重复或无 consumer 的 old fields/helpers/wrappers/schemas/examples/tests。
8. 更新 workflow/preset/docs SSOT、registry/manifest、installer managed inventory、README 与平台 discovery copies。
9. 运行 preset apply/reapply，处理 `.new/.bak`，验证 dogfood overlay/managed-copy/ownership 无漂移。
10. 执行 package/unit/schema/eval、stateful boundary integration、performance counts、#132/#161 current replay 与完整 Guru graph validation。
11. 执行 clean marketplace workflow init/preview/switch、preset install/reapply、Trellis update/upgrade、README commands 与跨平台 discovery/behavior。
12. 运行 `trellis-check` 和 `guru-check-task` 完整语义检查；finding 修复后全 scope 重跑，只有 `passed` 才进入 commit。

## 文件所有权拆分

- 新 package owner：`trellis/skills/guru-team/packages/guru-reconcile-task-base/**` 及其 package-local tests/evals。
- Workflow/registry owner：canonical workflow、registry/contracts、manifest、全局 route 与 graph validation。
- Existing consumer owner：Check/Commit/Branch Review/Publication/Finalizer 的 canonical packages 与直接 integration tests。
- Distribution owner：preset installer、managed inventory、README、overlay、dogfood/platform projections、throwaway/update/upgrade tests。

并行实现时每个 worker 只修改其 owner 范围；cross-owner schema/projection 先由主会话冻结 public contract，再分派。任何公共字段变化由主会话统一更新 consumer inventory，避免并行生成不同合同。

## 重点验证

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-13-172-base-evolution-gate
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py --repo .
python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p 'test_*.py'
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

还需运行新增/受影响 package 的 contract/runtime/eval tests、finish-family/stateful workflow integration、pair performance fixture、historical replay、registry/discovery counts、workflow init/preview/switch、preset reapply 与 update/upgrade scenarios。完整命令以实施时 current package entry 为准。

## 验收追踪

- R1/R3/R5：new package semantic eval、bounded continuity 与 stateful replay。
- R2/R4：guard unit/performance counts 与全部 boundary integration。
- R6：consumer inventory、legacy migration/negative source scan 与 Finalizer/Publication route tests。
- R7：schema/projection/private lifecycle、terminal artifact scan 与 authorization-field negative tests。
- R8：canonical/installed/platform/marketplace/preset/update/upgrade validation。
- AC1-AC14 必须在 `guru-check-task` evidence 中逐项有 current code/test/install 证据或明确的环境阻塞，不能用静态检查冒充 live 验收。

## 完成门槛

- 三份 planning 文档与 Docs SSOT Plan 通过 wording 与 `guru-approve-task-plan`。
- 实施不创建 `implementation-handoff.md`、tracked base-evolution report、raw search transcript 或授权 artifact。
- 所有 public exits、consumers、projections、registry/workflow counts 与 installed copies 一致。
- 完整 throwaway/update/upgrade 验收通过；无法运行的外部证据明确标为未验证。
- 只有 `guru-check-task` 返回 `passed`，workflow 才进入 commit 准备步骤。
