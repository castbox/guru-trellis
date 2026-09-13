# #247 Issue Scope Ledger retirement Test contribution

本文件定义稳定验证合同，不记录尚未执行的 PASS，也不把 focused install/update 证据表述为完整
Release matrix 或生产业务验证。

Promotion status：`reviewed_promoted`；稳定 Test contract 已合并到
`docs/test/versions/current-main-0.6.5-guru.50/`。本文件保留 promotion source与既有验证边界，
不作为第二 current Test authority。

- `T247-01`：fresh inventory 验证 current active graph 中 ledger 名称/schema id、writer、reader、
  precondition、registration 与 Issue aggregate consumer 数量为零；历史 archive/ADR/version evidence排除。
- `T247-02`：验证 task/workspace creation 不生成、登记或返回 ledger；current task identity/worktree/mapping
  仍闭合，mixed old/new package fail closed。
- `T247-03`：验证 Planning、qualification、Phase 2、Commit 与 Branch Review 不读取 ledger，且
  Issue-backed/no-Issue reference 由 current authority fresh形成。
- `T247-04`：验证 Issue-backed completed、reference-only empty close set、no-Issue 三路 Publication 判断，
  以及默认/非默认分支 closing-keyword 路径；Finalizer/Merge 不重判、不调用 Issue close API，live post-merge
  facts与 GitHub 自动效果一致；Finalizer archive/Ready、normal/terminal path生成同一 exact reviewed body SHA-256，
  Merge在closing-scope推导和mutation前拒绝body-only drift，standalone profile不接受该Publication identity。
- `T247-05`：验证 existing PR、archive-month、post-archive Ready、lost-result、reprepare、terminal recovery、
  Merge 四 exits 与 archived Restore 仅消费 current owner facts且不重复副作用；没有 ledger fallback 或替代 aggregate。
- `T247-06`：对 current lifecycle 比较 ledger absent、present-A、present-B；结果一致且 active runtime
  无 open/read。preset/update因路径不受管理而不主动删除或改写 present 文件。
- `T247-07`：验证 ledger-only Skill Markdown、interface/schema、eval/example JSON、DTO、runtime/script、
  fixture/test、manifest/registry 内容已删除；不执行旧 task migration/compatibility scenario。
- `T247-08`：验证 canonical/dogfood/installed/Shared/Codex/Claude/Cursor parity、preset apply/reapply/update、
  `guru-ledger-free-runtime@1.0.0` exact shape、source/installed validation、managed byte/mode、ownership/drift、
  recursive sidecar，以及真实 production wrappers 串联旧流程到 current terminal 的代表性 installed fixture。

## Fixed Scenarios

| Scenario | Expected result |
| --- | --- |
| `SCN-085 issue-backed completed` | Publication 默认判定应关闭；默认分支 PR body 写入 closing keyword并由GitHub自动关闭，Merge只验证live facts。 |
| `SCN-086 issue-backed remain-open` | live Issue含合并后仍待完成条件或当前交付不完整；Publication仅引用并记录具体原因。 |
| `SCN-087 no-Issue` | Commit/PR不制造Issue reference、primary Issue或关闭效果。 |
| `SCN-088 inert legacy present` | absent/present-A/present-B不影响current lifecycle；active runtime无read，preset/update不主动触碰。 |
| `SCN-089 recovery` | Finalizer archive/Ready、existing PR、lost-result、reprepare、terminal 与 archived restore/re-entry 使用 current task/Git/PR/provider facts且无重复副作用。 |
| `SCN-090 distribution/non-default publication and body continuity` | canonical、dogfood、installed与四平台current package/capability一致；非默认分支PR只引用，后续目标默认分支Publication fresh判断并编码closing keyword；Finalizer后body-only edit在Merge mutation前fail closed。 |

完整多平台 exact-candidate Release matrix、tag、GitHub Release 和生产业务仓验证保持 deferred。

## r24 Corrective Validation Evidence

2026-09-13 r24 corrective candidate 已完成实现侧 pre-Phase-2 验证；此前 r19-r22 的 Architecture、
qualification、task check 与 Branch Review 结论均不作为 current gate：

| Validation | Result | Coverage |
| --- | --- | --- |
| fresh Phase 2 Architecture | `baseline_current / architecture_impact / dedicated_refactor_slice / reviewed_promoted` | r24 corrective working tree 的 project check 通过；旧 lifecycle owner/edge/target/stop 保持，ledger authority active-zero，未重开 GAP、引入双 writer 或未来 lifecycle owner。 |
| Phase 2 qualification | `classified` | normal-scenario 五项与 solution-mechanism 四项均按 r24 current authority、真实 supported graph、完整 candidate 和 subtraction-first contract fresh 分类；无 scope confirmation、mechanism revision 或 blocked candidate。 |
| fresh task check | `passed` | schema 5.0 checkpoint 绑定 `HEAD 235b5eb8ca60859344e468c812999a1582c5c90f`、完整 991-path candidate、九 adequacy dimensions、code subtraction 与 Docs SSOT subtraction；无 open P0-P3 finding。 |
| related package/runtime/integration | `534 tests / PASS` | Workspace 52、Commit 26、Branch Review 26、Publication 51、Finalizer 93、Merge 39、Restore 23、runtime 52、shared integration 41、workspace invocation 1、installed closeout boundary 3、preset apply 77、upgrade contract 50。 |
| active-zero / ownership / drift | `PASS / status=ok` | ledger writer、reader、precondition、schema registration、aggregate DTO consumer为零；upstream ownership、dogfood overlay drift及canonical/installed/platform parity通过。 |
| focused install/update | `PASS` | 固定 `castbox/Trellis@a2003296...`、Codex 平台、本地未发布 workflow sample、clean install 与两次 same-candidate update/reapply；明确不等同完整 Release matrix。 |
| legacy equivalence | `PASS` | installed fixture 的 absent/present-A/present-B 与 parallel finish/recovery 均通过，legacy ledger 不参与 current authority。 |

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
| preset reapply / dogfood | `status=ok` | fresh `--all-platforms` reapply 全部 unchanged；canonical/installed source validation通过，未生成 `.new` / `.bak`，sidecar/conflict为0。 |
| static hygiene | `PASS` | relevant Python compilation、JSON parsing与 `git diff --check` 通过。 |

针对 `T247-01..08` 的 current active graph扫描未发现 ledger writer、reader、schema registration、
public DTO consumer或兼容 fallback；保留的命中仅属于明确排除的历史 archive、ADR、released/superseded
RDT、release evidence或本 #247 contribution 对退役边界的说明。legacy absent/present fixture均不参与
current runtime authority，preset/update不主动打开、迁移或删除旧 task ledger。

未验证边界保持不变：完整多平台 exact-candidate Release matrix、tag、GitHub Release、生产业务仓验证。
这些是 Release/production proof，不阻塞 #247 current-version 小幅优化的 Phase 2 完成，也不得由上述
focused/complete repository suite推导为已通过。

Production eval 的 deterministic cases 已通过，但 external semantic grading 当前不可用，因此未伪装为
eval PASS；该缺口与完整多平台 exact-candidate Release matrix、tag、GitHub Release、生产业务仓验证均为
明确 non-blocking deferred boundary。

Serialized promotion 已建立 `.50` RDT/Architecture successor与accepted `ADR-009`；r24 corrective candidate
已完成 fresh Phase 2，仍须单独授权 Task Commit，commit 后再执行独立完整 Branch Review。上述证据不证明
Publication、push、PR、merge、tag、Release或Issue closure。
