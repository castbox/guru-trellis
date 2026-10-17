# #575 S5 同源 exact-provider clean 验证与最终RDT设计

## D1. 身份、来源与内容范围

本切片使用既有Task/gen0与当前公开Delivery；根accepted scope不变。通过原DeliveryProjection.content_base从实际已交付且为当前HEAD祖先的最大head取得B=`07884d05d746d398c290cd834a9a03192a0e7205`，来源为实际S4 Delivery；规划观测H0同该值。main只是PR target，不为远端main前进同步分支，不把merge commit用作新内容基线。

初次完整focused的Guru source为包含捕获修复的真实提交07884d05。执行前在仓库外取得该提交的干净checkout，HEAD必须指向该真实OID；保留正式origin与真实commit/tree，不创建fixture commit冒充source。Fork由同源码source lock解析为2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0，CLI/Core0.7.0-castbox.3，pnpm10.32.1；实际source验证、构建及CI归既有validator/原工程事实依赖审查。source helper不进入managed projection；不从改变后的source恢复4096旧operation。

独立candidate_assessment消费当前PRD与真实机制候选，Architecture .94/current、constitution v1，结果no_architecture_impact/no_change；不制造贡献/ADR。final_plan在全量Wording后独立执行；scope、owner/API/store或兼容机制改变则刷新原评估，不继承候选结论作最终证明。

## D2. 唯一 source-design disposition matrix

| 规范来源及承诺 | 处置 | 落点 | 理由、影响与承接 |
| --- | --- | --- | --- |
| live #575 Stage1与根R575-04/A575-05：正式来源完整代表性clean样本 | retain | D1/D3；V1 | 使用真实已提交修复源，保留原profile全部阶段；init/helper不能替代。 |
| 旧S5 local-sample先native init后复制workflow的验证机制 | change | D3；V1 | 实际正常bootstrap为legacy而guard拒绝；改用已可寻址的同07884 exactprovider让CLI按真实Guru contract建Task，root完整clean要求不变，不修复或宣称原local分支通过。 |
| 根R575-01/03/04与S4 PRD R575-S4-04：工具/平台/真实predecessor联合证据 | retain | D4；V2 | 原owners事实按依赖复核，缺失或变化补验；不把旧来源改称新执行。 |
| 私有release Two-Stage Lifecycle步骤4..8：完整committedReview后串行晋升及fresh门禁 | retain | D5；P3 | 本切片先完整收敛draft，首次Review后原owner晋升；实际晋升diff重新Check/commit/Review。 |
| 根R575-05/A575-06：唯一长期Test与双向trace | retain | D5；P2 | 原preparation五文件承接最终准备责任，S1独立贡献与历史immutable版本保持。 |
| 根R575-06/07与私有release Stage1步骤9..11及Forbidden Persistence | retain | D6；P1/P5 | Refs-only交付；WholeCompletion/Closure/Finish各归原owner，不制造动态状态/授权账本。 |
| live #575 Stage2/非目标：最终main/provider/tag/smoke/Release独立 | retain | D6；P1/P5 | 本地样本/准备Review不充当最终candidate或业务生产证明，累计矩阵不扩入当前。 |

PRD及implement引用本矩阵，不复制另一份来源处置表。

## D3. 同源 exact-provider 的既有完整focused入口

从D1真实clean source运行原 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`，模式focused、平台codex。workflow provider固定为 `gh:castbox/guru-trellis/trellis#07884d05d746d398c290cd834a9a03192a0e7205`，`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=0`，Fork通过 `TRELLIS_FORK_SOURCE` 指定同一实际匹配构建。该07884真实提交已经远端可寻址，preset checkout也固定该真实HEAD；不改成本次尚未提交Docs、main或未来tag。沿bootstrap原支持环境选择CPython3.12.8 seed，仅在该单次命令PATH前置其bin；不改系统、主Task/common或peer指针。指定全新仓库外work directory保留全部logs/样本，不复用前两轮target。

现有 `_install_workflow` 对exactref正常执行 `init -y --codex --workflow guru-team --workflow-source <该完整SHA provider>`；CLI依据初始真实workflow contract生成Task，preset照常验证schema2/current-only。无需删除/转换bootstrap、修改CLI/verifier/guard或增加兼容reader。该机制复用README90..116的公开同源完整SHA安装入口，既不缩小样本也不制造成功。

完整profile独占的实际阶段保持：正常git target/init与workflow、preset初装、两轮update --skip-all及workflow preview/apply和preset reapply、source lock/template hashes与Docs保留、sidecar/版本、正式Fork来源复核、真实native platform load与focused session binding。逐层读取matrix/focused-summary与logs，真实最终exit和status均满足才记完整通过；聚合摘要不替代原失败阶段。stdout/stderr继续使用已交付helper，保留两流诊断和真实timeout124，不改预算或过滤警告。

原两轮local-sample失败由唯一Test保留：Python3.15依赖安装原因未知；3.12.8下native init先生成legacy bootstrap、随后copyGuru workflow导致guard拒绝。新配置只验证同H公开direct入口，不宣称修复原local分支。新失败继续保留首输出并走原qualification/诊断，不能先self-fix再补规划。07884只是准备source；Stage2仍对准备和Finish合并后的最终main candidate重新做remote provider与发布全门禁，当前结果不向Stage2迁移。

## D4. 既有事实的当前适用性

独立构建根A575-01..05检查集后，对A工具安装、source/installed/四平台/ownership、B无旧归档三平台reapply和真实stable predecessor逐项对照实际bytes、定义、输入、工具链、参数/期望与原始输出。当前code/definition未变且依赖可核实者采用原执行来源；变化、缺失、无法核实者补受影响检查。semantic gate每轮重做，不继承旧pass，不读其他owner private checkpoint。

predecessor链必须保留真实tag7d20a930、旧Fork5c760463与正式来源构建证明、原tools/selected-task操作与各自恢复引用；目标自身native/下一consumer、五规划/历史/用户配置保留、同ref resume与不兼容单侧tools rollback阻塞分别核实。不从新的source修改旧operation冻结内容。工具实际安装source4096不改称07884；完整trellis token变化对旧operation恢复的限制保持。

原73项suite=71pass/2FAIL的固定计数断言及其Bhelper因果对照保留，不能称全绿；不引入历史断言维护。若出现新的正常路径缺陷或current必要性，按原qualification与受影响planning/implementation路由处理。最终candidate的secret scan、语法/JSON、卫生与当前差额由当轮Check独立判断。

## D5. 原RDT唯一收敛与串行晋升

原RDT owner采用delta_first，在既有preparation贡献五文件收敛根范围、S2/S3/S4与当前S5最终结果；Test只记录实际来源、首次失败/修复/完整focused、旧FAIL/SKIP及未验证层次，双向trace连接根验收。先在最终Phase2前reconcile draft；S1 source-adoption已晋升内容保持原归属，不重复制造贡献。

完整当前S5候选经fresh Phase2 Architecture/Check、TaskCommit和首次完整committed独立Review后，开放P0-P3为零才进入原RDT owner的shared promotion。写前读取真实expected-current，原owners串行；Architecture owner判断真实影响并处理自身no_change或promotion，不由RDT猜测。不能在规划阶段晋升或预造后继版本号。

shared current实际diff使受影响门禁回到fresh Phase2、TaskCommit和不同reviewer的完整B..HEAD Review。只有post-promotion结果及publication Architecture current进入Delivery Review/Refs-only Publish/Merge。该顺序是晋升的直接consumer，不写Task-local gate/status账本；原owners只保留其最小恢复状态。

## D6. 完成层次

当前S5若达到A575-S5-01..04，交付的是完整准备证据和最终Docs收敛。WholeCompletion仍重新读取根accepted scope、所有实际Delivery与层次边界；只有其completed才进入reference_only Closure no_mutation、acceptance_finish与Finish/archive/bookkeeping。软件Stage2最终main exact candidate、provider、tag/smoke/Release及#575关闭归私有release原边界，不从当前source或PR推导通过。无新业务剩余切片被预建；新必要工作由WholeCompletion判断。
