# #575 S4 工具安装、平台证据与输出捕获修复设计

## D1. 内容基线与职责

内容 B 由原 DeliveryProjection.content_base 从当前 HEAD 祖先中的最大实际已交付 head 取得，为 `4096fac812b612e0fdd9c178402fc257b16c5334`；来源为 S3 实际 Delivery。PR target 为 main，与 B 分开；不为无关 target 前进同步分支。Task/generation/current Delivery不变。

A 工具安装和 B 平台样本来源为真实 clean committed Guru4096，正式 Fork 为 `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`，CLI/Core 均 `0.7.0-castbox.3`。source/version/provenance 分开；改变 source 不恢复旧冻结 operation。独立 Architecture candidate assessment 按 `.94/active` 与 constitution `guru-trellis-design-constitution-v1` 判断当前 verifier 捕获修复无架构影响，不创建 contribution/ADR；后续 owner/API/state/reader/恢复或 compatibility exit 改变须刷新原评估。

## D2. 唯一 source-design disposition matrix

| 规范来源及原承诺 | 处置 | 落点 | 理由、影响与承接 |
| --- | --- | --- | --- |
| 根 R575-01/03、#575 正式依赖：完整匹配来源与真实 source_locked | retain | D1/D3；V1 | 原 tools owner执行原冻结安装；未投影 helper 修复不修改其 source_ref 或冒充新源已安装。 |
| 根 R575-03/04：Task/session/历史/配置/pointer保留，目标自身native和下一owner | retain | D3；V1 | 工具和数据维护分开，无关archives不转换；原公共/Guru owners各写自身资产。 |
| 根 R575-04：四投影、三平台reapply、focused clean、真实stable predecessor及恢复/回退 | change sequencing, retain total | D4/D6；V2/V3 | 当前先交付未投影verifier捕获修复与工具/平台证据，后继从真实clean committed修复源完成完整样本。根验收不删减，WholeCompletion路由剩余。 |
| S4 PRD R575-S4-03：正常CLI两流、真实exit/timeout与完整诊断 | retain | D5；V3 | 两流分别strict decode解决合并字节穿插；不用quiet/filter/替换解码或timeout扩张。 |
| 私有release Stage1步骤4..9：完整committed Review后串行晋升及fresh门禁 | retain | D6；P3 | 本切片只reconcile draft贡献，不提前晋升shared；完整准备候选Review后再由原owners晋升。 |
| 根 R575-05..07、私有release Forbidden Persistence：唯一Test/trace及准备/软件发布边界 | retain | D6；P1/P2/P5 | 唯一贡献保留真实失败与剩余责任，Refs-only；不创建动态账本或新恢复状态。 |

PRD与implement只引用本矩阵，不建立第二份来源处置。

## D3. 原 A 工具采用与真实运行

原 tools owner使用完整 source launcher 执行 install/source_locked 的 preview、一次private prepare、精确写集审查与独立安装确认、invoke及同操作恢复。public owner拥有上游工具/scripts/receipt/workflow，Guru installer退休确切旧受管项并完整写packages/runtime/schema/registry/Shared/Codex/Claude/Cursor与自身manifest；不能手工receipt或单包热替换。

A含合法旧archives，采用tools-only保留原current-only guard。Task/session/规划/历史/配置与peer/common pointer保留；target resolver/installed、实际native continuation/current与下一真实owner分别证明，不以source launcher或DTO query替代目标运行。原失败并已回滚operation保持终态，不复用为本次操作。

## D4. 平台对象与工程事实适用性

A只读校验。B以同canonical、无旧archives执行三平台apply/reapply/drift，逐项审查bytes/mode、退休项和sidecar。四平台source graph与私有release Skill四份bytes独立比较。B fixture commit仅标识样本，不作正式source_ref；本地workflow不作Stage2远端immutable provider证明。

`verify_trellis_compatibility_matrix.py`及其定向测试不进入managed_source_projections或安装manifest。仅改该source-side helper时，V1/V2未依赖该helper且受管bytes/参数/工具链不变的实际结果经当轮依赖审查后采用，保留执行来源与原因；受影响、缺失或不确定检查重跑。完整trellis source token随helper变化而变化，所以不能用新source恢复旧operation，也不能把4096实际安装改称后续HEAD安装。最终扫描、source卫生和变更范围由新candidate重验。

## D5. 近因修复与直接消费者

当前 `_run` 用 stderr=STDOUT、text=True：正常CLI stderr warning可插在stdout Unicode glyph字节中，合并解码先于returncode检查失败。修复只在这一确定性capture边界，将stdout/stderr分开PIPE捕获和strict decode，不改变CLI输出、命令、环境或超时预算。

capture返回供git/版本/JSON消费者使用的stdout；log与MatrixError保留stdout/stderr完整诊断、真实exit code和既有timeout124分类。逐个核对capture消费者，不能把stderr警告混入结构化stdout，也不声称两流存在总时序。必要直接consumer适配在同一helper内完成，不创建新通用框架或公共API。timeout残留输出按原subprocess合同保留两流事实，不以解码失败覆盖timeout诊断。

定向回归用真实子进程验证双流合法Unicode、capture数据与完整log、真实非零exit和两流error、现有timeout分类与输出；真实正式Fork相同init参数经修复helper证明原失败阶段可运行。保留原focused首次失败和独立raw/separate诊断；helper成功不充当完整focused/native/session结果。实现前读Trellis官方扩展文档与本地spec，不改上游/global/node_modules。

## D6. 分阶段准备与最终门禁

当前独立切片负责工具/平台与有界helper修复；在既有575-release-preparation贡献收敛本切片RDT并reconcile，fresh Phase2 Architecture/完整Check、原TaskCommit、完整committed独立Review、publication Architecture/DeliveryReview后进入Refs-only Publish/Merge。

WholeCompletion依据根A575-01..08保留剩余完整focused、真实predecessor联合样本最终判定、最终完整RDT与晋升门禁；仅其additional_delivery_required可进入原Creation建立后继Delivery。后继从包含修复的实际clean committed source执行原focused Codex local-workflow入口，保持正式Fork lock/build/API检查；不能dirty run、自建fixture commit或绕source校验充当验收。stable `.3`样本由原tools/selected-task owners执行，观察身份/五规划/历史/配置、目标native/下一consumer、同operation恢复与不兼容单侧tools rollback；generic existing链不替代联合证明。

完整准备候选首次committed独立Review后，原RDT/Architecture owners按真实impact和expected current串行晋升，晋升差额fresh Check/TaskCommit/完整Review。最终WholeCompletion/Closure no_mutation/Finish和Stage2各走原边界；本切片既不提前晋升，也不宣布全部准备完成。
