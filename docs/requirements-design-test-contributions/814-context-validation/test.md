# #814 验证差额

适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee:docs/test/current/runtime-location.md`。完整拟写为固定正文原样保留，再追加下方完整章节。原有测试数量、失败、安装、CI 和未知状态保留各自观察截止。本文件提供原 RDT 整合与后续独立 Review/Completion 所需的验证定义和实际观察，不保存另一份完成台账。

## 原生 context 采用的验证与观察（#814）

本单元追加定义修订：`context-adoption-814`。来源为 [Issue #814](https://github.com/castbox/guru-trellis/issues/814) 及 D1 已接受规划，适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee`。承接 R814-01/02、D814-01/02，并复用 R718-03/11、R769 的来源/目标及保持条件。以下工程观察截止于本 Task 未提交的 `local_candidate`，没有正式 Guru H 或 `source_locked` 结果。

### 验证策略

| Test / Scenario | 需求→设计 | 入口、输入及独立观察 |
| --- | --- | --- |
| T814-01 / S814-SCALE | R814-01→D814-01 | 用原 native init、Task/Delivery/session writers、原 Guru C4 writer 和正常 Git 建立3/169合法注册工作区。执行实际 installed runtime-contract 的 key miss/bound remote、continuation 和公开显式 Task 入口；独立 listing/current 读回正确 owner/Task/Delivery/唯一 checkout。audit 只观察真实 Git subprocess，记录次数、来源与耗时，确认 eligible peers 和选中分支独立查询。 |
| T814-02 / S814-REJECT | R814-01；R718-11→D814-01 | 正常 Git switch 造成绑定分支 stale，普通 Task commit cherry-pick 造成非唯一身份；原入口须准确拒绝，正常恢复后成功。前后比较 workspace Task/session/peer、linked gitdir 和 common 相关文件的内容与mode。不手写内部身份/hash，不引入故意绕过或 fault injection。 |
| T814-03 / S814-PROBES | R814-02；R718-03/11；R769→D814-02 | 核 lock、精确 Fork Git/build/package/API，再执行 public tools prepare/apply 的真实两项10000ms probes。实际目标原 tools 操作终结后，用同 recovery ref 续接并读回；核同 operation/plan/preimages 与目标自身结果。H形成后才验证匹配完整源的新 source_locked 操作，不以开发成功代替正式采用。 |
| T814-04 / S814-DISTRIBUTE | R718-03/11；R814-02→D718-07/D814-02 | 采用原 owner 的目标 resolver/installed/native 读回，执行官方 upstream projection checker 及其测试、声明Claude/Codex/Cursor投影与drift/sidecar检查，比较原Task/history/config及peer/common保持。只做 accepted scope 所需验证，不扩展完整多平台 Release 矩阵。 |

### 本次实际观察

精确 Fork 为 `e3793251fad8bd261d0c370d408c7675b9f6a140`，parents 为 `7a9c62e842001b1d91d6b7feeed36ddd38370da7` 和 `cd1d5064f3ec8f97c19cf61f2193694edd4c3ba0`，tree 为 `8d7d0c3fe28a3464d92f723539a63da241e5485e`；main CI [43341080020](https://github.com/castbox/Trellis/actions/runs/43341080020) 成功。独立精确构建、成功后 source marker、实际 CLI/Core 身份和 public API1.0 已核；CLI/Core 为 `0.7.0-castbox.6`，使用 pnpm `10.32.1`。这不是正式 Guru H 的证明。

| 观察 | 实际结果 | 覆盖边界 |
| --- | --- | --- |
| T814-01 / 带审计测量 | 3工作区：key miss/bound remote/continuation/explicit Task 分别4/5/5/7次Git，0.1329/0.1370/0.1332/0.2863秒。169工作区：170/171/171/173次，5.8857/5.9306/5.7821/5.7361秒 | 耗时包含audit/profile。每个eligible工作区一次身份查询，bound/continuation另查选中分支；explicit有其额外入口查询。独立注册数、Task/generation、Delivery和peer-1 checkout正确，bound owner为fixture-owner-1，miss为caller的fixture-owner-0。没有旧新同机计时对照或全机器SLA结论。 |
| T814-01 / 额外身份读回 | 169工作区 task current 为344次Git/12.1384秒，Delivery current 为173次/7.0081秒，均成功 | 这是额外带审计的current身份读回，分别保留；不是两项public probes的耗时，不能概称所有native命令低于10秒。 |
| T814-02 / 普通拒绝与保持 | 正常分支switch被拒为current_task_checkout_unresolved；正常Task commit复制被拒为ambiguous_task_identity。恢复Git状态后原绑定入口成功；最终测量与拒绝样本内容/mode保持 | 原Task/Delivery/session/C4均来自真实公开writer，没有手工伪造state。按原快照比较workspace .trellis、linked .git、common trellis/worktrees；fixture-local Git commits只建立隔离拓扑，不是实际Task分支提交。 |
| T814-03 / 公开tools链 | 3/169样本的真实inspection→一次prepare→apply总链分别1.9521/3.5923秒，均applied、pending_paths=[] | 实际执行两个10000ms native probes，未mock或改预算；总链与带审计native测量分别成立。Task/session/peer/common内容及mode保持。 |
| T814-03 / 实际目标与同ref接续 | 原guru-upgrade-tools返回tools_upgraded 0.7.0-guru.8；operation为23270227-774b-471e-8be4-7b225d9d74d1，recovery_ref为76023da6-cb94-4878-a581-923cf8e4ff65。目标自身resolver/installed/native成功，原public recover读回applied/no pending；同ref resume再次返回tools_upgraded | 原冻结plan和preimages保持，没有重新prepare；原3913项Task/history/config/control内容与mode保持，原727项peer/common观测由原owner核验保持。此为已完成同候选操作的接续验证，不是旧#793事务恢复；formal_fork_source_lock仍unverified。 |
| T814-04 / 投影与回归 | 官方projection checker通过201文件，精确e379来源及Claude/Codex/Cursor均ok；对应9项unit通过，无skip。原drift检查退出0，目标sidecars为0 | canonical与原owner生成的installed lock、session_storage、template hashes和extension receipt对应；实际Task仍gen0/D1 implementing、Planning适用。限定quality检查未发现需修复项，但没有正式Check/Review、readiness或Task完成结果。 |

本轮Task-owned driver为 `.trellis/tasks/11-13-814-context-validation/deliveries/fca8647f-14d0-436d-8298-1b561036f8e4/research/verify-context-adoption.py`。原始结果保留在该checkout的 `.trellis/.runtime/guru-team/814-validation/`；定义和结论不要求普通读者重放这些临时样本。

三项首次设施错误保持：首个fixture authority revision为普通文本，被原validator拒绝，随后改用真实PRD SHA；首次explicit start清空同会话已选Delivery，随后使用独立explicit会话；stale已正确拒绝，但driver初次预期了另一诊断名，修正断言时复用原拒绝结果。它们不是产品修复前后对照，也不能被后续成功抹去。

旧#793内部timeout没有自然复现，历史首次失败及Fork历史观察保持各自截止。本轮没有fault injection，也未执行正式H/source_locked、完整多平台安装/升级/Release矩阵。后续独立committed Review、Delivery、Task Completion/Closure/Finish和live main可达性分别由原owner建立，不在本节预填。
