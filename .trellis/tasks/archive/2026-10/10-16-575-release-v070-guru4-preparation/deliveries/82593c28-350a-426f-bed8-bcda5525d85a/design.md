# #575 S2 来源准备设计

## D1. 对象、来源与固定内容范围

本 Delivery 的三规划只拥有 S2 来源切片；整体 accepted scope 仍是 Task 根 PRD。Architecture Baseline 为 `current-main-0.6.17-guru.93`，constitution 为 `guru-trellis-design-constitution-v1`，RDT 基线为 `.100`。方案复用既有 Task/Delivery、maintenance、installer、Docs 和发布 owners，不增加 Architecture 决策、contribution 或 ADR；最终设计由原 final_plan owner 独立判断。

四版本轴保持独立：目标 repository tag `v0.7.0-guru.4` 尚未发布，canonical extension/maintenance target 为 `0.7.0-guru.4`，现存基础 installed revision 为 `.3`，CLI/Core 为 `0.7.0-castbox.3`。固定 Fork `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`、tree `41ff285d857036324e480e1eb64d08fffd5956e1`、CI `38851816688`、pnpm `10.32.1` 不变。已发布 stable `.3` 保留其自身 tag、旧 lock 与历史证据。

内容基线 B 为 `b6b8c906663300547dc406c0e4ff3a7deeff450d`，来自原 content_base 的唯一先前 delivered head，且为当前 HEAD 祖先。规划观察 H0 与 B 相同；实现 H 由实际 TaskCommit 形成。完整 Review 覆盖 B→H 和真实 PR diff，PR 目标单独为 `main`。不为获得范围自动同步或重写任务分支。

## D2. 唯一 source-design disposition matrix

| 规范性来源与承诺 | 处置 | 落点、理由与影响 |
| --- | --- | --- |
| #575 正式依赖前置：明确匹配的 Fork/CLI/Core 来源与真实消费 | retain | D1、D5/V1；S1 正式锁保持，S2 检查来源和 canonical 消费者，S3 使用真实 clean committed Guru source。 |
| #575 Stage 1：版本、公开说明、完整投影与定向证明 | retain | D3/D4 与 implement P1；S2 承接来源和基础工具，S3 承接完整 .4 投影及正式样本，整体责任仍全部在同一 Task。 |
| 原 S2 三规划：一个切片先完成 .4 投影，再提交其执行来源 | change | D4/D5；用 S2 来源准备→S3 正式投影的有序独立切片替换顺序循环，不取消任何 whole-Task 验收，不放宽原 source 检查。仅改变 Delivery 归属，#575 本文要求不变。 |
| 原 maintenance 合同：formal Guru source 的 HEAD/clean/manifest/target 一致 | retain | D3/D5；S2 不从 dirty 来源执行 .4 正式安装。S2 实际提交及完整 Review 后的 clean 来源供 S3 消费。 |
| 私有 release contract：独立完整审查、serialized promotion、晋升后重新检查 | retain | D6 与 implement P2/P3；S2 独立来源审查，完整准备 contribution 在 S3 首次完整 committed Review 后晋升，晋升差额重新走门禁。 |
| 私有 release contract：准备 Task reference-only，Whole Completion/Closure/Finish 分离 | retain | D6；S2 不关闭 #575，不冒充 whole completion；S3 后仍由原 owners 作整体判断。 |
| #575 Stage 2：final main exact candidate、immutable provider、tag/smoke/Release | retain | D6；正式发布重新冻结最终 candidate，不从来源切片发布，不继承本地安装样本为 final 证明。 |
| 根规划 D5/P4：tools-only 与所选 Task 维护独立，历史事实和当前 gate 分离 | retain | D4；M 原 .3 操作、原始 Task 与历史交付保持，S3 是新的 .4 tools 操作，不重用旧备份或将旧 gate 导入当前 pass。 |
| AGENTS 6/7、preset/ownership：canonical 与投影最终收敛、受管重应用、定制保留 | retain | D4/D5；S2 记录已采用 .3 投影的实际来源，.4 剩余差额明确归 S3，完整准备结束前必须同步；不手抄生成文件或转换无关旧归档。 |
| Author/Approval：独立切片、Docs SSOT Plan 与真实 Activation | retain | implement P1/P2；同一 S2 key 返工，新规划重新审查和展示；后续 S3 由原 Creation 建立。 |
| Forbidden Persistence 与 AGENTS 10 | retain | 唯一 Test 拥有实际结果；规划保留稳定合同，不写授权、gate 台账、动态发布状态或 PR/Release handoff。 |

没有 reject 项。产品或 authority 新变化回其原 owner，不通过重命名切片隐藏未完成责任。

## D3. 来源版本消费者与当前公开说明

直接演进 canonical manifest 和原 `guru-upgrade-installation` owner 的 `TARGET_GURU`；生产 upgraded() 复用该目标，public schema/example、tools example、两个 stop consumers 和表示目标的 fixture 使用 `.4`。Plan2 preset 调用保留 managed interpreter，仅补齐实际使用的模块 import。真实 predecessor、合法旧族、原 source 检查、完整 Plan2 与 rollback 保持。

新增测试从实际 upgraded() 结果进入 canonical manifest/public schema 消费链，不制造常量自比较或平行校验器。已有真实 CLI 用例验证恢复路径；fixture/preset 替身与正式安装证据分层。

README、workflow README、preset README 和 public-docs spec 的当前源码映射改为 `.4` 尚未发布；明确当前 installed `.3` 是基础工具采用，不声称最终 .4 parity。稳定安装仍用 immutable `.3` tag 及它自身的旧 Fork lock。试用未发布源码必须选择同一个真实、远端可寻址的完整 SHA 供 marketplace/preset；不预填未产生的 SHA，不使用尚不存在的 `.4` tag。

## D4. 基础工具与下一投影切片

当前 S2 保留 M 原 public tools/Guru installer 已生成的完整 `.3` 基础图：原生 Task2/session3、Guru runtime/packages、所选 Shared/Codex/Claude/Cursor 入口、workflow、receipt 与配置。Trellis 继续拥有 upstream 模板/scripts/.version/template hashes，Guru 继续拥有自身 package/spec/overlay。所有来源采用差额纳入完整 Review，不能因 generated 身份遗漏。

S2 的 current installed 校验只证明其自身 `.3` receipt/bytes 和当前 native 可用，不证明 `.4` runtime/schema parity、完整安装或升级完成。canonical `.4` 与 `.3` installed 的版本差额是显式待交付责任，S3 用新 clean source 和原 tools-only owner同步。不存在长期第二实现或新的安装 fallback。

S3 不复用 M 的 `.3` operation，不调用普通 apply 绕过旧归档 guard，不迁移全部归档。它独立准备精确 `.4` tools plan；实际 public/Guru 写集、Python pointer、sidecar、配置定制、Task/session/common/peer 状态由原 owners 审查。配置和历史 Task/Delivery、五规划与 raw migration source 保留，旧 gate 不成为当前 pass。

## D5. 没有来源循环的验证顺序

S2 提交前执行 implement V1/V2/V4/V5/V7 中属于来源与现存基础图的检查，完成本切片 RDT reconciliation 和完整语义 Check；TaskCommit 与独立 committed Review 形成实际来源 H。使用 H 的 clean checkout读取 canonical .4 manifest、source lock和原维护合同，不能用版本号或临时虚构提交代替。

S3 才以该来源执行 V3/V6 和最终 .4 V4/V5：tools-only 操作、四平台字节 parity、三平台 reapply/drift、focused Codex clean/local-workflow、真实 stable .3 predecessor 维护、目标原生 continuation/下一 consumer、同操作 resume 和不兼容单侧 tools rollback。缺少来源、环境或实际结果保持具体未验证边界；module/fixture 成功不替代这些要求。

最终 remote provider、final predecessor gate、完整 predecessor→candidate 发布审查与 tag-pinned smoke仍由发布 Stage 2 对最终 main candidate重新执行。generic verifier 与 split-maintenance 不匹配时回原 owner，不静默跳过或扩展为 verifier 重构。

## D6. Docs、交付与整体收尾

S2 采用 delta_first，原 RDT owner在独立贡献根维护当前来源/基础图事实及 S3 剩余义务，shared current 保持。S3 补齐完整 .4 证明后，原 owner 在首次完整 committed Review 后按 fresh expected-current 晋升；晋升差额重新 Check/TaskCommit/独立完整 Review。Architecture 无职责变化时走 fresh no-change，不制造 ADR。

S2 Delivery refs-only 合并后，Whole Completion从实际 accepted scope判断剩余工作，经 additional_delivery_required/原 Creation建立 S3。S3 完成不自动等于软件发布：原 Whole Completion、Closure no_mutation、Finish archive/bookkeeping和发布 Stage 2 保持独立。#577 与上游 #46 不纳入 #575 的产品实现或完成责任。
