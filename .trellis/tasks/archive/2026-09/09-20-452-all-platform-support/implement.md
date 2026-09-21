# #452 实施计划

## Phase 1 产物与直接消费者

- `prd.md`：Issue #452 的范围、约束和验收合同。
- `design.md`：`.57` #443 Architecture/RDT promotion、`.58` #452 RDT promotion、两层平台 authority、全平台 projection、升级保真、失败策略和验证分层。
- 本文件：实施顺序与命令边界。
- `research/official-trellis-platforms.md`：上游平台 registry/AI_TOOLS 与 OpenCode native path 的当前证据。
- `implement.jsonl` / `check.jsonl`：Phase 2 agent 的 spec、research 和验证上下文。

## 实施顺序

1. 以 live #452 scope amendment、closed #443、current `.56` authority 与 live registry 为输入，完成 fresh scope-change clarification 和 Planning Architecture/RDT 判断。
2. 复制 immutable `.56` 为新的 `.57` RDT version，修订 current delta、manifest、traceability、decisions、capability inventory 和 test strategy/plan，使其只吸收 #443 capability。
3. 更新 Architecture CURRENT/DOMAIN/INTEGRATION/GAP/GOVERNANCE/PLAN/ADR/EVIDENCE 与 #443 contribution promotion 状态，并同步三个 `.trellis/spec` current projection；验证 32/142/102 与 22/98 边界。
4. 将 #452 RDT contribution 以 `.57` 为 predecessor 提升为 `.58/active`，Architecture 保持 `.57/active` 与 `reviewed_candidate` contribution；重新执行 Planning Architecture/RDT，promotion-created diff 进入 fresh Phase 2，旧结果全部作废。
5. 读取并锁定 upstream Trellis `AI_TOOLS` 证据，形成全部 22 个平台的 canonical `AITool` id、唯一 public `cliFlag`、template/native destination 与 projection descriptor；public `--platform` 和 installed selection 使用 `cliFlag`，例如 `claude-code -> claude`；OpenCode 继续记录真实 command/skill discovery 和 actual-load 入口。
6. 删除 `guru_supported_platforms` / `deferred_platforms` 中间层；canonical inventory 只保存 upstream complete set，installer policy 单独保存 Claude/Codex/Cursor 三平台缺省值。
7. 为全部 upstream 平台补齐 registry-bound canonical projection、managed path/ownership、manifest mapping、mode 与 package-private test 排除；不同 native surface 使用显式 descriptor，不按目录名或统一 overlay 形状猜测。
8. 在增加行为前先拆分三个接近 3000 行且会被修改的 Python 文件：把 inventory/selection resolver、compatibility descriptor/adapter helpers 和新增平台选择测试分别移入职责单一的模块，保持行为等价并让所有 touched non-generated files 不超过 3000 行。
9. 更新 installer：重复 `--platform <cli-flag>` 接受任意 upstream subset；删除 `--all-platforms` argparse option、选择分支、manifest/JSON 状态和调用参数；未提供 `--platform` 时选择 `claude,codex,cursor`。
10. 更新 installed upgrade/provenance：从目标 manifest 读取 exact `cliFlag` selected set，验证 install/skill/platform sections 一致，并始终以重复 `--platform` 传递，不使用 source dogfood 或缺省集合覆盖目标选择。
11. 将 guru-trellis dogfood reapply 改为显式 `--platform claude --platform codex --platform cursor`；drift checker读取 active selected set，仅比较 shared 与已选平台，同时继续验证完整 canonical ownership inventory。
12. 更新 compatibility helper、throwaway helper、OpenCode 代表性 actual-load、subset reapply/update、ownership/cardinality、README/spec 和负例测试；22 平台只验证 inventory/selection/projection，不重复上游 native compatibility matrix。
13. 运行 Architecture/RDT、targeted unit/integration/source-installed/platform/throwaway checks，按结果修复，再运行完整 `trellis-check` 所需验证。

## 预期重点文件

- `docs/architecture/{README.md,01-current,03-domains,04-integrations,05-gaps,06-governance,07-plans,adr,evidence}/**`
- `docs/architecture/contributions/443-task-identity-session-binding.md`
- `docs/{requirements,design,test}/README.md`
- `docs/{requirements,design,test}/versions/current-main-0.6.17-guru.57/**`
- `docs/{requirements,design,test}/versions/current-main-0.6.17-guru.58/**`
- `.trellis/spec/architecture/baseline-usage.md`
- `.trellis/spec/docs/{requirements-design-test-ssot,public-docs}.md`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- installed provenance/platform-selection resolver and its tests discovered by Phase 2
- new focused Python modules produced by the mandatory under-3000-line split for inventory/selection, compatibility helpers, and platform-selection tests
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
- installer fixtures: 无参数三平台默认、重复 `--platform` subset、OpenCode 显式选择与 unknown platform 写前拒绝；descriptor/ownership parity 不启动 22 个外部平台客户端
- dogfood reapply: `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --platform claude --platform codex --platform cursor --json`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh --platform opencode ...`
- no-flag default selection and generic unknown-argument assertions.
- exact-selection upgrade fixtures for one platform, arbitrary subsets, guru-trellis three-platform dogfood and the complete upstream set.
- OpenCode representative actual-load；其余平台只执行 source/installed/ownership projection parity。

## 未覆盖边界

Issue #452 不包括正式 release/tag、业务仓库生产验证或 #434 lifecycle 切图；`.57` promotion 只建立 #443 capability current authority，不构成 #434 activation。pinned `castbox/Trellis` 已拥有上游 22 平台 native 验证，本仓不重复承担该矩阵；这不允许把任一可显式选择平台的 Guru projection implementation 从本 Issue 延后。
