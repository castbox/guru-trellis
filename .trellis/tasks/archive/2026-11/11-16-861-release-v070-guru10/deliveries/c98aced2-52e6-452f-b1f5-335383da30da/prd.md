# #861 gen2 D2：完整交付源的正式工具采用

## 1. 整体来源与术语

本批身份为 Task `744a637b-a044-46cd-8cdd-77ddd85ded8e` / generation 2 / Delivery `c98aced2-52e6-452f-b1f5-335383da30da`。planning_root 为本目录。公共 accepted_scope 是 `../../prd.md`，revision `sha256:0b58a6f33c687290d842d6de14e74ed6b77e52d49106a328c2161080382ec12c`。本批选定 R1、R3、R4、R5、R6、R7、R13 及 AC1、AC2、AC3、AC4、AC5、AC11；整体定义仍由根 PRD 拥有。

| 来源与章节 | 角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/861 全文及创建审核评论 | 要求；没有其它 Issue 状态前置，Stage 2 最终候选来自届时最新 main |
| 根 PRD §5–8 | 当前已接受要求；有序采用、状态保留、验证及整体 Completion 边界 |
| `.agents/skills/release-guru-trellis-version/references/contract.md`：Complete Source Before Actual Adoption、Whole Preparation Completion、Stage 2 | 规范性设计；D1 delivered 后独立采用，准备结果不作为最终发布 pass |
| `.agents/skills/guru-upgrade-tools/references/contract.md`：Forward behavior、write boundary、target evidence、same-operation recovery | 规范性设计；完整 source_locked 来源、一次准备、原 writer、实际目标验证与保留 |
| `.agents/skills/guru-sync-base/references/contract.md`：Sync Profile | 既有执行合同；未来取得 clean main canonical source，不把 Git 同步当作 tools 安装 |
| 前序 `../bb916153-bffa-4961-a06f-4a54b9bdef2f/implement.md`、PR #877 及公共 delivered 事实 | 历史交付事实；完整源已交付，临时安装不代表本 checkout 已采用 |

M 指 PR #877 的 merge commit `2938801829c8b8862e71d522891c79e8efb2d47a`。正式采用指原 tools owner 更新本准备 checkout 并验证实际安装；不是手改 manifest 或复制四个文件。

## 2. 整体与本批目标、非目标

整体 Task 准备 `.10` 完整源、真实采用及准备收尾。本批独立交付 M 的真实 source_locked 采用，消除本 checkout 的旧来源和四个旧 Discovery 命令声明，同时验证完整安装及保留责任。Guru 仍为 `0.7.0-guru.10`；CLI/Core 为 `0.7.0-castbox.6`，Fork lock 不变。

本批不重新实现前序消费者修复，不改 runtime/Interface/schema/manifest 定义，不改变平台选择或公共 API，不重做累计多平台矩阵。primary 仅拟作为 clean canonical source，正式发布后的 primary 安装仍在 Stage 2。本批不 tag、smoke、Release、关闭 Issue、清理资源或修改历史正文。

## 3. 本批起点、前序结果、依赖与剩余责任

gen2 D1 的内容提交为 `343bc3100ea8f157bfd20d7a6a226455dbe482f4`。PR #877 已实际合并为 M，M 与该内容提交 tree 相同。前序已修复 authoring envelope 测试和四个 context_request schema 引用，完成直接回归及三平台临时完整安装/reapply；这些结果只证明其明确对象。原 Completion 已实际返回 `additional_delivery_required`，原因是正式采用尚未实施；原 Creation 已创建本 D2，不重复创建。

本 checkout installed provenance 仍为 `79c25b5eaafdbcf415393535a16a7b1c0d281284`。只读比较发现四个平台/installed Discovery commands.json 仍旧。配置与模板仅注释/空白不同，必须保留配置原 bytes。目标是当前 gen2 注册 checkout，不是旧 repair checkout或所有 peer。

依赖为本批独立规划/审核/接受/Activation、完整 clean M source及匹配 Fork build/API。正式采用和必要验证后，仍由原质量与交付链交付本批全部 installed after。整体 Completion、reference-only Closure no_mutation、Finish 终态归档及簿记另由原 owner 完成；其后 Stage 2 冻结最新 main，不锁定为 M。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、条件和触发 | 处理与可观察结果 |
| --- | --- | --- |
| A1 取得来源 | 实施 owner 在 Activation 后请求 clean M | 原 Sync 同步 clean primary main；验证来源 HEAD、canonical bytes和 Fork lock。若 main 超 M，先判断差额与刷新来源，不能用 M 的 source_ref 执行另一 HEAD |
| A2 正式采用 | 原 tools owner 从完整 source 进入；目标为本 checkout | 只读 preview、实际 maintenance inspection、prepare 一次；展示真实冻结写删集并取得该安装确认后 invoke。原 installer 生成 manifest/projections，返回真实结果 |
| A3 验证和恢复 | tools 写入完成或部分失败 | 成功核目标自身 resolver/native continuation、完整内容及保留；失败沿同 operation/ref/source/plan 恢复，不重复 prepare、不篡改 checkpoint |
| A4 兼容及交付 | 实际新源采用后 | 同操作真实 reapply/drift及一个 `.9→M` Codex existing cell完成；原质量交付链审全部 after。未通过则保留缺口，不以 tools_upgraded 替代 |

## 5. 完整行为、条件与约束

- **A-R1 来源**（R1/R3）：从已交付的完整 clean M canonical source 使用 source_locked；Fork 为 lock 指定的 `e3793251fad8bd261d0c370d408c7675b9f6a140`，核真实 CLI/Core build 与 maintenance capability。同版本号不替代来源证明。
- **A-R2 写入**（R4）：只通过 M 原 tools preview/prepare/invoke。tools_input 来自实际 public inspection；workflow custom/install 使用 canonical 内容和 immutable provider。AGENTS 恰一 custom 决定，由实际 source snapshot及完整原文 base交原 renderer。平台保持 Claude/Codex/Cursor，配置 preserve。禁止手改 installed/hash/manifest。
- **A-R3 保留**（R4）：原 owner 核 Task、archive、workspace、session、用户配置、peer tools与 common pointers 原 bytes保持；仅允许目标 checkout-local pointer及原操作 recovery 写入。普通 full apply 的历史 Task guard 不授权迁移历史或绕过。
- **A-R4 验证**（R4/R5/R13）：完整 managed 集合/bytes/modes、来源/CLI/lock、真实 target resolver及 native entry、四个实际 help 的合法输入和返回身份、无私有测试泄漏/退役 Codex 公共根/未处理 sidecar。完整 reapply 必须真实执行；complete 后 resume 仅验证不能冒充它。
- **A-R5 兼容**（R5）：根 AC9 的 whole-source 条件要求新源实际采用后、Whole Completion 前完成完整 existing。本批把一个 `.9→M` Codex cell作为 R4/R5/AC3 必要兼容验证，不重选或重做 R8–R11 的历史源码责任，不扩累计矩阵。
- **A-R6 交付与失败**（R6/R7）：本批所有实际安装 after 纳入自己的固定内容范围及原完整质量交付链。来源、scope、机制或必要验证变化回原 owner；不伪写旧 pass。最终候选和发布后 primary 收敛留 Stage 2。规范性来源设计唯一处置见后续 design §3。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 输入、入口与预期观察 |
| --- | --- | --- |
| A-AC1 | A-R1/A1 | live D1 delivered、M clean source、matching lock/build经原入口核实；不是 dirty source或仅计划 |
| A-AC2 | A-R2/3、A2/3 | 原 tools install/source_locked 的真实目标操作完成，无正式 lock 未验证项；原保留集合不变，manifest provenance指向实际 M |
| A-AC3 | A-R4/A3 | 目标自身执行 installed validator及 continuation；完整映射逐项bytes/mode/集合正确，四个 help 声明 context_request 2.0且 supplement 1.0仍合法；正常输入与原返回身份一致 |
| A-AC4 | A-R4/5、A4 | 原 same-operation installer真实reapply、完整 drift/sidecar；原 `.9` predecessor existing driver和 aggregate 完整通过。tools exit、focused或临时安装单独不替代 |
| A-AC5 | A-R6/A4 | 必要知识整合/readback及本批原完整质量与交付事实覆盖全部 installed after；原 Completion另判断整体准备，不从本批 merge推出 Task完成 |

没有待用户决定的需求选择。实际 frozen writes、maintenance facts和工程结果只能在未来原步骤取得，属于执行前置，不预填通过。当前停点为完整 Planning/独立 Architecture/Approval 后、Activation 和工具写入前。

## 7. Canonical 引用与本轮差额

`docs/{requirements,design,test}/current/codex-skill-distribution.md` 的 R724-01–06、D724-01–04、T724-01–05约束共享根、平台选择、原维护 writer、冲突及证据分层；本批只采用现行定义，不改变它们。`.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value` 与 Validation Scope Ownership约束最小有效验证及事实采用。Architecture `docs/architecture/04-integrations/distribution.md` 的 ARCH-INT-001/006/014/015定义完整投影、锁定配对和独立采用顺序；本批沿原 owner，无新模块或共享 authority。实际知识差额由原 RDT/Architecture owners在 after 时复核，不预建空贡献或改共享导航。
