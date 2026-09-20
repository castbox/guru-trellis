# #452 实施计划

## Phase 1 产物与直接消费者

- `prd.md`：Issue #452 的范围、约束和验收合同。
- `design.md`：`.57` Architecture/RDT promotion、三层 capability inventory、OpenCode projection、失败策略和验证分层。
- 本文件：实施顺序与命令边界。
- `research/official-trellis-platforms.md`：上游平台 registry/AI_TOOLS 与 OpenCode native path 的当前证据。
- `implement.jsonl` / `check.jsonl`：Phase 2 agent 的 spec、research 和验证上下文。

## 实施顺序

1. 以 live #452 scope amendment、closed #443、current `.56` authority 与 live registry 为输入，完成 fresh scope-change clarification 和 Planning Architecture/RDT 判断。
2. 复制 immutable `.56` 为新的 `.57` RDT version，修订 current delta、manifest、traceability、decisions、capability inventory 和 test strategy/plan，使其只吸收 #443 capability。
3. 更新 Architecture CURRENT/DOMAIN/INTEGRATION/GAP/GOVERNANCE/PLAN/ADR/EVIDENCE 与 #443 contribution promotion 状态，并同步三个 `.trellis/spec` current projection；验证 32/142/102 与 22/98 边界。
4. 重新执行 Planning Architecture/RDT；promotion-created diff 进入 fresh Phase 2，旧结果全部作废。
5. 读取并锁定上游 Trellis 当前平台 registry/`AI_TOOLS` 证据，确定 OpenCode 的 native root、command/skill discovery 和实际加载入口；对其余平台形成 upstream/deferred inventory。
6. 在 canonical preset authority 中拆分 upstream/Guru-supported/default-dogfood 集合，定义 capability inventory 的 schema/manifest 绑定和稳定 deferred/unsupported 语义。
7. 补齐 `.opencode` canonical projection、registry/manifest、ownership claims、managed paths、mode 与 package-private test 排除规则；保留已有三平台兼容性。
8. 更新 installer、`--platform`、`--all-platforms`、reapply/removal/sidecar provenance 和 installed validation；确保无平台参数仍为 Codex/Cursor。
9. 更新 compatibility matrix、throwaway helper、actual-load 和 drift/update checks，加入 OpenCode clean/existing/reapply/update 代表性断言。
10. 更新 preset/spec/README、fixtures、cardinality assertions 和 unknown/deferred negative cases。
11. 运行 Architecture/RDT、targeted unit/integration/source-installed/platform/throwaway checks，按结果修复，再运行完整 `trellis-check` 所需验证。

## 预期重点文件

- `docs/architecture/{README.md,01-current,03-domains,04-integrations,05-gaps,06-governance,07-plans,adr,evidence}/**`
- `docs/architecture/contributions/443-task-identity-session-binding.md`
- `docs/{requirements,design,test}/README.md`
- `docs/{requirements,design,test}/versions/current-main-0.6.17-guru.57/**`
- `.trellis/spec/architecture/baseline-usage.md`
- `.trellis/spec/docs/{requirements-design-test-ssot,public-docs}.md`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- `trellis/presets/guru-team/ownership/upstream-ownership.json`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`
- `.trellis/spec/workflow/quality-guidelines.md`

实际修改集合以 Phase 2 discovery 和上游证据为准；不提前承诺不存在的 upstream platform paths。

## 验收命令族

- Architecture/RDT current locator/version/traceability/cardinality validation and fresh semantic gates.
- `python3 -m unittest discover trellis/presets/guru-team/scripts/python -p 'test_*.py'`
- `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh --platform opencode ...`
- OpenCode actual-load and source/installed/platform parity checks from the updated compatibility matrix.

## 未覆盖边界

Issue #452 不包括正式 release/tag、业务仓库生产验证、#434 lifecycle 切图，以及尚未完成 Guru projection 的 upstream-only 平台的完整实现；`.57` promotion 只建立 #443 capability current authority，不构成 #434 activation。这些边界必须在最终验证报告中标为 deferred/unverified，而不是推断为通过。
