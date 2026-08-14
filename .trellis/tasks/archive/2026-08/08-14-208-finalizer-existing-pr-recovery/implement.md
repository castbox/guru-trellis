# 实施计划

## 1. 合同与数据模型

- [ ] 更新 Finalizer `SKILL.md` 与 `references/contract.md`，定义 `existing_pr_recovery` eligibility、preview、确认、transaction、恢复和 fail-closed语义。
- [ ] 更新 `.trellis/spec/workflow/{data-contracts.md,companion-scripts.md,skill-package-contract.md,quality-guidelines.md}`，保持职责单一且不复制 step-local流程。
- [ ] 设计并迁移 current transaction/gate/preview schema与examples；保留明确 legacy identity，stable Skill id与external exits不变。

## 2. Runtime 实现

- [ ] 扩展 PR候选与live facts读取，保持唯一、同 repo/head/base、非 fork、canonical identity门禁。
- [ ] 增加 PR/remote HEAD与publication HEAD的相等/严格祖先判定及稳定 reason code。
- [ ] 在普通首次发布与显式 recovery之间建立互斥 classification；不放宽 `pre_finalizer_remote_state_exists`普通路径。
- [ ] 在首次 mutation前记录 exact PR、initial Draft/Ready、pre-push HEAD与publication identity。
- [ ] 实现 exact fast-forward push、Publication title/body convergence、Ready保持或Draft-to-Ready、archive和三方HEAD校验。
- [ ] 实现每个transition的幂等恢复，禁止重复push、PR create/edit、archive或Ready mutation。
- [ ] 保持业务Finalizer verifier不可达。

## 3. 测试

- [ ] 扩展 Finalizer package tests覆盖preview、首次mutation、Ready/Draft recovery、已推送/已更新/已归档幂等恢复。
- [ ] 增加真实Git祖先拓扑fixture与GitHub mutation计数断言。
- [ ] 覆盖multiple/fork/closed/merged、repo/head/base mismatch、非祖先/未知ancestry、force-push、scope/payload/Publicaton/archive/transaction drift矩阵。
- [ ] 扩展 installed closeout fixture，验证canonical wrapper与single JSON `ready_for_merge`输出。
- [ ] 增加current graph不含`verification_required`/verifier的回归断言。

## 4. 投影、版本与文档

- [ ] 更新必要的 Interface、commands、schemas、examples、evals、managed inventory与extension version SSOT。
- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步dogfood副本，逐个处理 `.new/.bak`。
- [ ] 运行 source-installed/platform byte identity、ownership、registry/workflow graph与dogfood drift检查。
- [ ] 仅在安装/升级行为可见变化时更新preset/workflow README。

## 5. 验证命令

```bash
python3 trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
python3 trellis/presets/guru-team/scripts/python/verify_installed_closeout.py --help
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root .
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-14-208-finalizer-existing-pr-recovery
git diff --check
```

根据实现后的测试入口补充targeted package/runtime/integration命令。完整clean throwaway install/update在功能与投影测试通过后执行；若环境阻断，记录为未验证边界。

## 6. 风险与回滚点

- Transaction schema升级是最高风险点；先完成schema/validator/test，再接入mutation路径。
- 普通首次发布与recovery必须有独立测试，防止已有Open PR被静默接管。
- 每个外部mutation后立即验证live facts；测试必须证明恢复不重复mutation。
- 回滚通过恢复canonical package/spec并重新apply preset完成，不直接编辑或单独回退installed/platform副本。
