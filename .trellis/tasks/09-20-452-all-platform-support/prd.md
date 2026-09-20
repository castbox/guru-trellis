# #452 提升 #443 Architecture/RDT authority，并补齐 OpenCode projection

## Goal

在同一交付单元内先修复过期的 Architecture/RDT current projection，将已完成的 #443 task identity/session binding capability 提升为 `.57` current authority；随后补齐平台能力分层、OpenCode projection、ownership、reapply 与 actual-load 验证。

## Requirements

- 将 `docs/architecture/` 与 Requirements/Design/Test current authority 从 `.56` 提升为 `current-main-0.6.17-guru.57`，吸收已完成的 #443 contribution，并保持 `.56` 为 immutable superseded history。
- `.57` current authority 必须绑定 live canonical registry 的 `32 packages / 142 exits / 102 commands`；production workflow 继续保持 `22 mandatory invokes / 98 exits`，不得借 promotion 激活 #434 graph。
- 同步 `.trellis/spec/architecture/baseline-usage.md`、`.trellis/spec/docs/requirements-design-test-ssot.md` 与 `.trellis/spec/docs/public-docs.md` 到 `.57`，消除 `.55` projection 与 `.56` Docs authority 的漂移。
- #443 contribution 的 lifecycle、Architecture decision、owner、current/target boundary、evidence 与 RDT traceability 必须进入新的 current authority；不得只替换版本号或 registry 数字。
- `.57` promotion 完成后必须重新执行 Planning Architecture/RDT、Phase 2 Architecture、完整 task check、Task Commit 与独立完整 Branch Review；promotion 前的 pass 不可复用。
- 建立显式的平台能力清单，区分：
  - 上游 Trellis 当前声明的平台/模板集合；
  - Guru Team 已完成 canonical、installed、platform projection、ownership、reapply、update 和 actual-load 验证的平台集合；
  - 无参数 dogfood 安装集合。
- 上游能力来源固定为 Trellis 当前 `AI_TOOLS` registry，不得通过目录名猜测。
- Guru Team 必须补齐 OpenCode 的 public projection：`.opencode` skill/command discovery、managed paths、ownership、manifest、reapply/update、throwaway 和 actual-load 验证。
- `--platform opencode` 必须在支持范围内完成安装并返回完整、可验证的 projection；不在支持范围内的平台必须返回稳定、明确的 deferred/unsupported 结果，不得伪装成成功。
- `--all-platforms` 必须表示 Guru Team 当前支持的全部 platform projection，不得继续把无参数 dogfood 集合命名为上游全平台集合。
- 无参数安装仍保持 Codex/Cursor，不能因为补齐 OpenCode 而隐式改变 dogfood 行为。
- 更新 canonical、installed、Shared/Codex/Claude/Cursor/OpenCode projection、registry/manifest/cardinality、ownership、reapply/update、throwaway helper、actual-load 和 drift 检查。
- `tests/` package-private 内容必须继续只存在于 source validation，不得进入 installed/shared/platform public projection。
- unknown platform、缺少 projection、projection 漂移、installed-only 缺失、sidecar/removal provenance 不一致必须 fail closed。
- 不修改上游 Trellis、全局 npm、`node_modules` 或业务仓库代码；不激活 #434 及其后续 Delivery/Completion/Closure/Finish 图；不执行 Release/tag/GitHub Release。

## Acceptance Criteria

- [ ] Architecture、Requirements、Design、Test 的唯一 active authority 为 `.57`；`.56` 及更早版本保持 immutable，README、manifest、traceability 与 `.trellis/spec` projection 一致。
- [ ] `.57` 完整承接 #443 task identity/session binding capability，current registry 为 32 packages / 142 exits / 102 commands，production workflow 仍为 22 mandatory invokes / 98 exits。
- [ ] #434 production graph 未激活；#443 promotion 只建立 current capability authority，不切换 Delivery/Completion/Closure/Finish/Cleanup/Reactivate 全局路由。
- [ ] promotion-created diff 已重新通过 fresh Architecture/RDT 和 Phase 2 gate；旧 `.56` 或 promotion 前验证不被复用为当前 pass。
- [ ] capability inventory 明确记录 upstream、Guru supported projection、default dogfood 三层，并由 source/installed 校验消费。
- [ ] OpenCode `.opencode` projection 与 Shared/Codex/Claude/Cursor public projection 遵循同一 public contract，mode、manifest、ownership、reapply/update 结果一致。
- [ ] `apply.sh --platform opencode`、重复平台选择、`--all-platforms`、unknown platform 和互斥参数的行为有确定性测试。
- [ ] `--all-platforms` 与无参数 dogfood 选择解耦；无参数安装保持 Codex/Cursor，显式全平台行为包含 Guru 已完成的平台集合。
- [ ] compatibility/throwaway helper 可对 OpenCode 执行 clean、existing、reapply/update 和 actual-load 验证；静态目录存在不能单独通过。
- [ ] ownership inventory、installed manifest、platform roots、registry cardinality 和 package-private test 排除均通过 fail-closed 校验。
- [ ] canonical apply + dogfood reapply + drift check 无 `.new`/`.bak` 残留，且 source/installed/platform bytes 与 executable mode 符合合同。
- [ ] `trellis/presets/guru-team/README.md`、`.trellis/spec/preset/`、`.trellis/spec/workflow/quality-guidelines.md` 与对应测试全部同步；未覆盖的完整 Release Gate 或其他上游平台 deferred 边界在最终报告中明确列出。

## Notes

- Scope amendment authority: https://github.com/castbox/guru-trellis/issues/452#issuecomment-5745730445
- `.57` authority repair/promotion 与平台支持是本次明确接受的同一交付单元；不再拆成额外 Issue/worktree。
- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
