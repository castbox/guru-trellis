# #452 提升 #443 Architecture/RDT authority，并完成全平台可选 projection

## Goal

在同一交付单元内先修复过期的 Architecture/RDT current projection，将已完成的 #443 task identity/session binding capability 提升为 `.57` current authority；随后让 Guru Team preset 对 pinned upstream `AI_TOOLS` 全部平台形成可显式选择的 projection，并保证业务仓库升级严格保留其已安装平台集合。

## Requirements

- 将 `docs/architecture/` 与 Requirements/Design/Test authority 从 `.56` 提升为 `current-main-0.6.17-guru.57`，吸收已完成的 #443 contribution 并保持 `.56` 为 immutable superseded history；随后只把 #452 RDT delta 提升为 `.58/active`，Architecture 保持 `.57/active` 直到实现后的独立 committed-range review 与 serialized promotion。
- `.57` current authority 必须绑定 live canonical registry 的 `32 packages / 142 exits / 102 commands`；production workflow 继续保持 `22 mandatory invokes / 98 exits`，不得借 promotion 激活 #434 graph。
- 同步 `.trellis/spec/architecture/baseline-usage.md`、`.trellis/spec/docs/requirements-design-test-ssot.md` 与 `.trellis/spec/docs/public-docs.md` 到 `.57`，消除 `.55` projection 与 `.56` Docs authority 的漂移。
- #443 contribution 的 lifecycle、Architecture decision、owner、current/target boundary、evidence 与 RDT traceability 必须进入新的 current authority；不得只替换版本号或 registry 数字。
- `.57` promotion 完成后必须重新执行 Planning Architecture/RDT、Phase 2 Architecture、完整 task check、Task Commit 与独立完整 Branch Review；promotion 前的 pass 不可复用。
- 平台 authority 只有两层：pinned upstream `AI_TOOLS` 完整平台集合，以及目标业务仓库 manifest/provenance 中记录的 exact installed selection；不得再引入独立的四平台 Guru-supported 或 deferred/unsupported 集合。
- 上游完整集合固定绑定 Trellis 当前 `AI_TOOLS` registry；当前证据为 22 个平台。inventory 必须同时保留 canonical `AITool` id 与 public `cliFlag`、template/root、native entry；不得通过目录名猜测或把 `claude-code` 与 `claude` 混为同一字段。
- 完整删除公开 `--all-platforms` 选项及其 installer、manifest、upgrade、throwaway、文档与测试语义；旧参数必须在目标仓库写入前被 argparse 拒绝，不保留隐藏的全集安装分支。
- `--platform <cli-flag>` 可重复，用于显式选择一个或多个 upstream 平台；public 参数与 installed `selected_platforms` 使用 registry `cliFlag`（例如 `claude`），canonical inventory 仍保留 `AITool` id（例如 `claude-code`）。
- 未指定 `--platform` 时，缺省选择固定为 Claude/Codex/Cursor。该缺省值是新安装入口策略，不是第三层 capability inventory。
- 业务仓库升级必须先从 current installed manifest/provenance 读取以 registry `cliFlag` 记录的 exact selected platform set，再以重复 `--platform <cli-flag>` 原样应用；不得扩张为 upstream 全集或缺省三平台，也不得依据当前 source repository 的 dogfood 文件反推目标选择。
- `guru-trellis` 是业务仓库特例，其 active dogfood installed selection 固定为 Claude/Codex/Cursor；dogfood reapply 和 drift 必须消费该 exact selection。
- OpenCode 是 upstream complete set 的普通成员，仍须具备 `.opencode` projection、managed paths、ownership、manifest、reapply/update 与代表性 actual-load 验证，但不自动进入 guru-trellis dogfood。
- 上游 22 个客户端自身的 native 行为、模板正确性和逐平台兼容矩阵由 pinned `castbox/Trellis` 的测试权威负责；本仓只验证 Guru inventory/selection、生成投影、ownership、upgrade preservation、三平台 dogfood，以及 Issue 明确要求的 OpenCode 代表性 actual-load，不重复执行 22 平台逐一 native 验证。
- 更新全部 upstream 平台的 canonical/installed/platform projection、registry/manifest/cardinality、ownership、reapply/update 与 drift 检查；平台 projection 必须按 registry 声明的真实 native surface 生成，不能假设每个平台拥有相同目录或相同 overlay 数量。
- `tests/` package-private 内容必须继续只存在于 source validation，不得进入 installed/shared/platform public projection。
- unknown platform、缺少 projection、projection 漂移、installed-only 缺失、sidecar/removal provenance 不一致必须 fail closed。
- 不修改上游 Trellis、全局 npm、`node_modules` 或业务仓库代码；不激活 #434 及其后续 Delivery/Completion/Closure/Finish 图；不执行 Release/tag/GitHub Release。

## Acceptance Criteria

- [ ] Architecture 的唯一 active authority 为 `.57`；Requirements、Design、Test 的唯一 active authority 为 `.58`，完整继承 immutable `.57` 并吸收 #452 current contract；README、manifest、traceability 与 `.trellis/spec` projection 一致。
- [ ] `.57` 完整承接 #443 task identity/session binding capability，current registry 为 32 packages / 142 exits / 102 commands，production workflow 仍为 22 mandatory invokes / 98 exits。
- [ ] #434 production graph 未激活；#443 promotion 只建立 current capability authority，不切换 Delivery/Completion/Closure/Finish/Cleanup/Reactivate 全局路由。
- [ ] `.57` 与 `.58` promotion-created diff 已重新通过 fresh Architecture/RDT 和 Phase 2 gate；旧 `.56`、`.57` predecessor 或 promotion 前验证不被复用为当前 pass。
- [ ] capability inventory 精确绑定 pinned upstream `AI_TOOLS` 的全部 22 个平台；不存在独立的四平台 Guru-supported 或 18 平台 deferred 集合。
- [ ] `apply.sh --all-platforms` 不再是公开参数，调用时 argparse 在目标仓库写入前失败；manifest、upgrade、throwaway 和 JSON 输出均不再携带 `all_platforms` 状态。
- [ ] `apply.sh --platform <cli-flag>` 可重复选择任意合法 subset；canonical `AITool` id 与 public `cliFlag` 映射精确且唯一。未指定时 selected set 恰为 `claude,codex,cursor`。
- [ ] installed upgrade 从 parent/current manifest 读取并以重复 `--platform` 保留 exact selection；单平台、任意 subset、三平台 dogfood 和完整 22 平台均不会被扩张或收缩。
- [ ] guru-trellis active dogfood manifest、installed packages、overlays 和 drift selection 恰为 Claude/Codex/Cursor；OpenCode 或其他 upstream 平台不会因 canonical support 被安装进 dogfood。
- [ ] OpenCode `.opencode` projection、explicit install、reapply/update 与代表性 actual-load 通过；其他 upstream 平台由 descriptor 驱动生成 Guru projection 并完成 source/installed/ownership parity，不在本仓重复其上游客户端 native compatibility matrix。
- [ ] ownership inventory、installed manifest、platform roots、registry cardinality 和 package-private test 排除均通过 fail-closed 校验。
- [ ] canonical apply + dogfood reapply + drift check 无 `.new`/`.bak` 残留，且 source/installed/platform bytes 与 executable mode 符合合同。
- [ ] `trellis/presets/guru-team/README.md`、`.trellis/spec/preset/`、`.trellis/spec/workflow/quality-guidelines.md` 与对应测试全部同步；正式 Release Gate、22 平台逐一 native compatibility 与业务生产验证属于上游/后续 owner，不得把 platform implementation 本身标为 deferred。

## Notes

- Scope amendment authority: https://github.com/castbox/guru-trellis/issues/452#issuecomment-5745730445
- Platform contract authority: https://github.com/castbox/guru-trellis/issues/452#issuecomment-5747785875
- Superseding platform contract authority: https://github.com/castbox/guru-trellis/issues/452#issuecomment-5748684130
- `.57` authority repair/promotion 与平台支持是本次明确接受的同一交付单元；不再拆成额外 Issue/worktree。
- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
