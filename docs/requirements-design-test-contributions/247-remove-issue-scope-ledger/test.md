# #247 Issue Scope Ledger retirement Test contribution

本文件定义稳定验证合同，不记录尚未执行的 PASS，也不把 focused install/update 证据表述为完整
Release matrix 或生产业务验证。

- `T247-01`：fresh inventory 验证 current active graph 中 ledger 名称/schema id、writer、reader、
  precondition、registration 与 Issue aggregate consumer 数量为零；历史 archive/ADR/version evidence排除。
- `T247-02`：验证 task/workspace creation 不生成、登记或返回 ledger；current task identity/worktree/mapping
  仍闭合，mixed old/new package fail closed。
- `T247-03`：验证 Planning、qualification、Phase 2、Commit 与 Branch Review 不读取 ledger，且
  Issue-backed/no-Issue reference 由 current authority fresh形成。
- `T247-04`：验证 Issue-backed completed、remain-open、no-Issue 三路 Publication 判断，以及默认/
  非默认分支 closing-keyword 路径；Finalizer/Merge 不重判、不调用 Issue close API，live post-merge
  facts与 GitHub 自动效果一致。
- `T247-05`：验证 existing PR、terminal recovery、restore/re-entry、Finish 与 Cleanup 仅消费 current
  owner facts且不重复副作用；没有 ledger fallback 或替代 aggregate。
- `T247-06`：对 current lifecycle 比较 ledger absent、present-A、present-B；结果一致且 active runtime
  无 open/read。preset/update因路径不受管理而不主动删除或改写 present 文件。
- `T247-07`：验证 ledger-only Skill Markdown、interface/schema、eval/example JSON、DTO、runtime/script、
  fixture/test、manifest/registry 内容已删除；不执行旧 task migration/compatibility scenario。
- `T247-08`：验证 canonical/dogfood/installed/Shared/Codex/Claude/Cursor parity、preset apply/reapply/update、
  source/installed validation、managed byte/mode、ownership/drift、recursive sidecar与一个代表性 install/update。

## Fixed Scenarios

| Scenario | Expected result |
| --- | --- |
| `SCN-085 issue-backed completed` | Publication 默认判定应关闭；默认分支 PR body 写入 closing keyword并由GitHub自动关闭，Merge只验证live facts。 |
| `SCN-086 issue-backed remain-open` | live Issue含合并后仍待完成条件或当前交付不完整；Publication仅引用并记录具体原因。 |
| `SCN-087 no-Issue` | Commit/PR不制造Issue reference、primary Issue或关闭效果。 |
| `SCN-088 inert legacy present` | absent/present-A/present-B不影响current lifecycle；active runtime无read，preset/update不主动触碰。 |
| `SCN-089 recovery` | existing PR、terminal、restore/re-entry使用current task/Git/PR/provider facts且无重复副作用。 |
| `SCN-090 distribution/non-default publication` | canonical、dogfood、installed与四平台current package一致；非默认分支PR只引用，后续目标默认分支Publication fresh判断并编码closing keyword。 |

完整多平台 exact-candidate Release matrix、tag、GitHub Release 和生产业务仓验证保持 deferred。

## Phase 2 Validation Evidence

2026-09-13 fresh Phase 2 finding-fix round 的 current-candidate 验证结果：

| Validation | Result | Coverage |
| --- | --- | --- |
| fresh Phase 2 Architecture | `baseline_current / architecture_impact / target_native / reviewed_candidate`，`ADR required=true` | 完整 current candidate、九 concerns、project check、owner/single-writer、GAP/compatibility exit与promotion boundary。 |
| Phase 2 qualification | normal-scenario与solution-mechanism均为 `classified / qualified_current` | current requirement、supported lifecycle、target-native owner-native mechanism及排除的migration/compatibility/hostile assumptions。 |
| fresh task check | `passed` | schema 5.0 freshness、完整 reviewed path set、九 adequacy dimensions、code subtraction与Docs SSOT subtraction。 |
| related package/runtime/integration | `392 tests / PASS` | Workspace、Commit、Branch Review、Task Check、Architecture、Publication、Finalizer、Merge、Restore、Clarification、Plan、qualifiers与通用runtime。 |
| active-zero / ownership / drift | `PASS / status=ok` | ledger writer、reader、precondition、schema registration、aggregate DTO consumer为零；upstream ownership、dogfood overlay drift及canonical/installed/platform parity通过。 |

同一实现候选此前还完成过以下较早完整回归；这些事实用于补充广度，不是本次 fresh Phase 2 的唯一
gate，也不替代上表的 Architecture、qualifier、freshness checker与public wrapper结果：

| Validation | Result | Coverage |
| --- | --- | --- |
| prior preset Python complete suite | `203 tests / OK (skipped=1)`，961.219s | 较早的 canonical package、runtime、eval、installed verifier 与 integration 完整 Python 回归；唯一 skip 保持既有条件性外部场景。 |
| parallel finish integration | `2/2 PASS`，551.930s | parallel finish/recovery 不读取 ledger，current owner facts闭合。 |
| workspace invocation integration | `1/1 PASS` | task/workspace plan、result 与 invocation 不含 ledger-era `scope`、`task_artifacts` 或 writer字段。 |
| adapter Stage 0 | `3/3 PASS` | current task identity/path构造不依赖 ledger compatibility shim。 |
| installed closeout owner boundary | `3/3 PASS` | Publication closing keyword、Finalizer绑定与 Merge live closure verification owner边界。 |
| Python routing suite | `42/42 PASS` | current command/skill route inventory与删除后的 package graph一致。 |
| live routing inventory | `status=ok` | generated-shebang fingerprint与 current inventory一致。 |
| preset reapply / dogfood | `status=ok` | canonical/installed source validation通过；审计并删除本次生成的3个 `.bak` 后，sidecar/conflict为0。 |
| static hygiene | `PASS` | relevant Python compilation、JSON parsing与 `git diff --check` 通过。 |

针对 `T247-01..08` 的 current active graph扫描未发现 ledger writer、reader、schema registration、
public DTO consumer或兼容 fallback；保留的命中仅属于明确排除的历史 archive、ADR、released/superseded
RDT、release evidence或本 #247 contribution 对退役边界的说明。legacy absent/present fixture均不参与
current runtime authority，preset/update不主动打开、迁移或删除旧 task ledger。

未验证边界保持不变：完整多平台 exact-candidate Release matrix、tag、GitHub Release、生产业务仓验证。
这些是 Release/production proof，不阻塞 #247 current-version 小幅优化的 Phase 2 完成，也不得由上述
focused/complete repository suite推导为已通过。
