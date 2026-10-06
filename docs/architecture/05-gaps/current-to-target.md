# GAP

| Gap | CURRENT | TARGET | Owner / evidence gate |
| --- | --- | --- | --- |
| `ARCH-GAP-001` | current main `.37` / Trellis `0.6.15` verified compatibility | published `.37` immutable source | 独立的重构前稳定版 Release Issue；`unverified` |
| `ARCH-GAP-002` | stable release `v0.6.5-guru.10` / `.36` / Trellis `0.6.5` | next stable `v0.6.15-guru.1` / `.37` / Trellis `0.6.15` | 独立的重构前稳定版 Release Issue；`unverified` |
| `ARCH-GAP-003` | six-cell `public_plus_local_candidate` proof | `.37` tag-pinned install/update proof | 独立的重构前稳定版 Release Issue；`unverified` |
| `ARCH-GAP-004` | current Phase ownership | possible further owner decoupling | later accepted Issue；`inferred` |
| `ARCH-GAP-005` | no `.37` tag/Release or tag-pinned release smoke | exact frozen-main stable publication and smoke | 独立的重构前稳定版 Release Issue；`unverified` |
| `ARCH-GAP-006` | `.37` 缺设计宪法 identity、双维 change contract、全阶段 project-check consumption 与 next-task successor binding | `.38` 已建立 current authority、single-writer promotion 与 promotion 后 re-entry | #283 reviewed promotion；`closed`，fresh post-promotion gates仍绑定最终 HEAD |
| `ARCH-GAP-007` | installed Finalizer 曾把 business target checkout 当 canonical extension source，verifier failure detail 又在 cleanup 后丢失 | `.41` 使用双 checkout、closed mode、独立 provenance validation 与 cleanup 前 structured evidence | #311 Architecture implementation/review promotion `closed`；真实 fixture、生产发布和错误文件重试仍 `unverified`，Issue OPEN |
| `ARCH-GAP-008` | task-local Issue classification aggregate曾跨多个lifecycle owner传递reference与closure状态 | current authority由Publication、Finalizer、GitHub与Merge各自单写并通过最小DTO连接 | #247历史promotion `closed`；`.54`不携带该aggregate的capability、compatibility identity或current successor claim |
| `ARCH-GAP-009` | `.67` 已原子激活重复 Delivery/Completion/Closure/Finish/Cleanup/Reactivate 图，旧 Publication/Finalizer/Restore 不再是 current | 保持单图和唯一 consumer；独立验证完整 Release matrix | #434 production 子缺口 `closed`；专门 Release matrix/业务仓验证 `unverified` |
| `ARCH-GAP-010` | 平台选择曾混用固定 dogfood overlay、四平台中间层与全集安装语义，升级无法由目标 manifest 保真重放 | upstream 22-platform inventory + target-installed exact selection；重复 `--platform`、三平台新装缺省、OpenCode explicit-only dogfood boundary | #452 Architecture promotion `closed`；implementation evidence 已定向通过；22-client native matrix、Release 与业务生产验证仍由外部 owner 负责 |
| `ARCH-GAP-011` | `.67` 已将 C2-C7/D443/D436 与七个 E434 packages 组合，零 planned，旧 mapping/前驱 active edge 已退出 | 保持 current 单图；专门 gate 再验完整多平台兼容 | #454 substrate 和 #434 activation 子缺口 `closed`；Release matrix/业务仓验证独立 `unverified` |

GAP 不是 #266 的 implementation backlog，也不自动授权开始后续 Issue。

`.65` 对 `ARCH-GAP-011` 的 D443 子缺口记录为 canonical package ready，但旧生产接线仍保持不变；
D436/E434 package/graph activation、#434 的受控切换和 #410 Release matrix 仍是独立剩余边界。

`.66` 记录 D436 五个 terminal lifecycle canonical package 子缺口 `closed`，但只有 source
package-ready；E434 完整 owner packages、旧 mapping 退休、#434 production graph/selector/installed
原子激活和 #410 Release matrix 仍为 `ARCH-GAP-011` 的 `partial/open` 剩余边界。

`.67` 以 #434 原子激活七个 E434 owner packages、旧 predecessor 退休、registry/graph/manifest/
installed/声明平台投影，`ARCH-GAP-009` 的 production graph 子缺口和 `ARCH-GAP-011`
的 E434 activation 子缺口均 `closed`。以上表格的 `.64/.66` CURRENT 与 `partial/open`
为各自 predecessor 快照；本版两项只保留完整多平台 Release matrix 与业务仓生产验证的
独立 `unverified` 边界，不把它们算为 #434 activation 失败或完成证明。

`.68` 的 #454 generation 7 消除 TaskId/Git-ref 混同、official writer/source
与 five-field reader 漂移，并完成 terminal ledger-loss 显式 Cleanup/Reactivate
边界；`ARCH-GAP-011` 的本次局部缺口 closed。完整多平台 Release matrix、业务仓
生产验证仍为独立 `unverified`，不得从本次结果推定通过。

`.69` 的 #467 preparation 关闭无关旧状态阻断新 TaskId 的局部缺陷，保留
目标身份冲突 fail-closed。前一版本退役受管资产的真实升级清理、exact-candidate
发布 gate、tag、smoke 与 GitHub Release 尚待 Stage 2/3；完整多平台 Release
matrix 和业务仓生产安装仍属独立 `unverified` 边界。

`.70` 的 #481 关闭任务人员字段/接口与 PR #24 官方 task schema 不匹配的局部缺陷；
旧归档仅保留 TaskId 防复用和严格只读拒绝诊断，#454 绑定与资源归属仍由原 owner
持有。旧 `0.6.17` Trellis 安装无法由当前 `0.7.0-castbox.1` Fork update，前驱
升级、远端 marketplace、完整多平台 Release matrix 和生产安装均为独立
`unverified` 边界，不因代表性新装通过而关闭。

`.71` 仅关闭 #490 当前 C6 disposition 拒绝/source未采用的局部缺陷，不新建或重新打开GAP；ARCH-GAP-006/008闭合保持。release/native-host/remote/predecessor refusal证据保持#489独立未验证边界，knowledge promotion不关闭它们。

## ARCH-GAP-012：受支持旧安装升级验收

状态：`open`。CURRENT：#495迁移候选代码/合同与本地public迁移、任务owner接续、普通恢复、写后rollback及current update/reapply已验证；TARGET：全部MIG-495-01..09真实证据齐备。Owner：#495同一任务；closure condition：固定same-remote-GuruHEAD的source_locked public升级与同源marketplace/provider，以及完整MIG06旧PR/merge处置/genuine支持来源旧Finalizer/Finish在途代表验证。exact PR195旧安装来源已读取，不是public处置完成；PR210/58历史merged终态不提供在途证明。知识`.72`只提升候选，不能关闭本GAP或允许merge/Completion；其它GAP及Release/真实业务安装独立边界不变。
