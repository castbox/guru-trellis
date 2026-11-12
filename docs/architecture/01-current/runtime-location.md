# Runtime、执行位置与Git来源职责

Identity：`ARCH-RUNTIME-LOCATION`；状态：current。适用before为main `610a810d45bb30173906d55c77709389adf1cf31`，来源为Issue #718；决定见[ADR-RUNTIME-LOCATION](../adr/runtime-location-decoupling.md)，需求/设计/验证分别由[RDT](../../requirements/current/runtime-location.md)、[Design](../../design/current/runtime-location.md)、[Test](../../test/current/runtime-location.md)拥有。

## 独立身份与原owners

worktree拥有文件和执行位置，branch拥有Git引用/历史，Task拥有accepted scope、Delivery与生命周期，Python环境拥有解释器和锁定依赖。环境可运行、分支名或目录不能建立Task身份与阶段资格。公共Task/Delivery/session及合法绑定仍由Trellis与原Guru lifecycle owners验证，环境维护不要求创建或转换Task。

工具代码来自实际采用的assets；原bootstrap单写环境选择及cache，原Sync单写Git来源事实，Discovery判断证据充分性。Markdown负责语义、scope、路由及门禁，脚本执行和校验确定性事实。source-loaded工具维护仍由原upgrade-tools从明确完整匹配来源执行，不能用来源代执行证明目标成功。

## 共享环境与选择

环境identity包含runtime API/layout、lock、Python implementation/major/minor、OS/architecture/ABI；patch/path、Git HEAD、Task或位置不进入identity。相同有效需求复用同一物理venv，不同兼容类别/依赖可并存。日常wrapper不安装依赖、不使用global site-packages。

当前checkout-private `selection-v3.json`只保存自动模式或显式兼容类别、需求指纹到runtime identity的hint。原owner优先验证当前需求有效hint；自动hint缺失/失效时按identity字典序验证已有cache。新增cache/PATH不改变有效hint；不同需求分支切回使用原hint。真实显式类别不可被自动fallback消除。

初始化及明确apply/reapply未传--python时使用当时PATH python3；显式--python优先且失效不回退。独立check只读、resolve只缓存已验证定位、repair沿原candidate/锁定安装/真实wrapper验证后成功切换。缺seed、锁来源、cache或不兼容有具体诊断；失败不提前替换合法环境/选择。位置和Task生命周期不删除共享cache；不新增GC。

## 格式切换、旧consumer与原rollback

旧local/gitdir/common `active.json` v2没有选择来源，不能据此编造历史显式意图。只有新载体不存在时，当前owner按原顺序一次读取旧来源：兼容有效则保同物理环境，失效按自动hint查兼容cache。当前显式类别由公开--python重表达。新文件成立后唯一writer只维护新格式；新文件存在但无效时拒绝，不以旧v2覆盖当前约束。旧v2原文保留供同位置旧installed继续使用，不双写。

原单checkout工具更新只写目标新选择。peer/common工具、Task/session、用户配置与新旧选择bytes及实际合法选择保持。原tools/upgrade rollback同时快照新旧载体真实preimage，先核公共tools/data兼容，恢复旧工具及载体实际存在/原文。公开print-active-pointer定位当前writer，实际选择通过公开check/resolver读取。旧完整安装继续固定原合同；匹配维护切换及退出由原runtime/installer/maintenance owners完成，历史Git来源仍可读。

## 明确Git对象与实际副作用

原guru-sync-base的operation=read以明确repo/ref/commit返回baseline_ready，固定Git tree来源与工作区候选分别绑定。对象可读时无需该分支检出或无关checkout干净；不fetch/ff、不隐式追ref变化。原operation=sync保留唯一目标、dirty/ff及HEAD/local/remote一致性，返回synced。只读成功不等于同步或正式gate。

Discovery读取固定tree的实际blob/history/archive证据，草案通过独立candidate_file字节绑定；current→history→语义审核继续由原owner执行。来源variant经原五阶段transition、Clarify回程、Wording、Readiness和实际Issue/Task创建consumer成套承接。无Task、外部worktree及正常未提交草案可以读审，不能冒充committed Review或远端发布。错基线、普通候选变化和缺正式身份回原纠正/刷新/拒绝。

Task Creation的固定来源消费承接Issue #813，适用before为main `5c6a4591db7165ece045e6b0eb789c21d06d7d38`，落实既有ADR-RUNTIME-LOCATION。当前creation输入明确reviewed_base_source的kind/selected_ref/commit；git_object的固定commit决定审核起点，selected_ref只定位所采用来源，不以其当前指向或本地同名branch HEAD判定freshness。独立selected_base_ref保留Task基线branch及非base/target资格职责，delivery_target保留未来交付仓库/分支职责。原AI读取实际ready来源并完成薄projection；脚本只校验对象和关系，不选择来源语义或重建上游通过。

原Creation/composition在record/create及check/recover共用来源归一化和commit/acquisition绑定。git_object验证同repository可用的精确commit对象及acquisition.decision_head一致；synced_branch从实际同步输出薄投影，新建前保留来源branch标准化一致及local HEAD相等检查。两者继续原exact source、common-dir、TaskId/generation、branch binding、注册位置和ownership/session约束。固定对象来源不要求移动或清理primary。真实对象/acquisition不一致给出字段级原owner恢复，不通过放宽身份条件制造成功。

已完成创建的check/recover重读原结果和原control/session关系，不再执行precreation uniqueness，不重复创建Task、branch、worktree或C4/C5；原source.commit须与真实acquisition起点一致。恢复保留原session分流：同Task/generation/ref保持原绑定；session_record_missing仅由原session owner重新attach；不同或无效session阻塞；context_key_unavailable保留explicit-task模式。后来正常ref前进不把原结果改成缺失。当前输入版本和旧schema/API退出由MIGRATION-813单写：新版本成套迁移受控consumer，旧schema字节保留验证，旧成功操作由完整固定旧provider恢复，旧待执行输入以实际上游来源经当前原owner重审。不新增current旧parser、自动kind猜测、来源台账或第二恢复writer。

代价限定为原创建合同的一个必要source值、共享归一化、原错误投影和直接consumer迁移。对象可读性与本地同步状态分别检查，减少无关primary同步等待；不增加协调阶段、锁或跨Task状态。只有来源语义、合法创建/恢复consumer、原Task基线或同步副作用合同变化时重评。RDT拥有完整需求/设计/验证，Architecture拥有本责任定义；实际链路、目标安装、Delivery和Task整体完成各由原owner以真实结果证明。

## 代价、替代与重新评估

本机制只增加原owner必要的需求匹配/hint与局部来源variant，以及真实旧reader的格式切换。hint可重建，显式选择只在原checkout私有载体，不建立全局偏好或业务authority。没有时间排序、每位置venv、通用绑定器、第二恢复台账、上游patch或永久双writer。

只有实际兼容类别、依赖/API/layout、受支持旧consumer或原副作用合同变化时重新评估。ADR-027单目标/peer隔离/source-target/data先校验、ADR-006实际Sync约束仍有效；仅其被用于环境启动/独立只读的组合解释由本单元和新ADR替代。Architecture/RDT先完整proposed，经candidate Check后原final_integration/readback，实际after重绑最终质量链。知识接受、实现、目标安装、Release与业务采用分开；实际观察仅由Test拥有，完整Release矩阵独立。

## 配置驱动的新建位置（#760）

本节承接 Issue #760，适用 before 为 main `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`。原 AI owner 判断位置策略、命名、冲突和副作用；共享 runtime 只提供 live Git topology 与项目配置的确定性路径事实。环境查询、正式 Task 新建、task-free 新建消费同一解析能力。Task 继续原 acquisition/绑定；task-free 继续普通 Git，不引入 Task validator、Task身份或位置映射。

项目锚点是 live Git 事实唯一确认的 primary；不能将调用 cwd.parent、porcelain 首行 metadata 或 common-dir.parent 直接当作主仓库。读取确证 primary 的 `.trellis/guru-team/config.yml`：空 worktree_root 为 primary.parent / (primary.name + '-worktrees')，相对值对 primary 解析，绝对值直接采用。linked 空模板不独立竞争；非空配置解析与 primary 项目配置冲突时准确诊断。锚点不可唯一确认则报告原 owner 可处理的缺口，不猜测或新增映射。

配置生成新位置由 root 与本次已审目录名形成，在任何 branch/worktree/Task 创建前核对计划路径。真正显式新位置保持原合法合同；已有外部 checkout 采用及原 Task 恢复先分流，不受生成 root 限制或重定位。旧绝对输入的兼容与新字段迁移由原 create-task 合同和 MIGRATION-760 拥有，绝对值本身不证明用户选址。

该共享能力有三个当前 consumer，避免复制解析且不建立第二执行或状态authority。代价限定为位置事实模块、原接口差额和定向验证；不引入缓存、锁、清理进程或长期证明。只有 Git topology、配置语义、公开位置策略或真实旧 consumer 边界变化时重新评估。配置与普通Git行为验证、分发、业务采用和Release分别成立，实际观察由对应Test单元拥有。

## tools peer 增长与冻结资产源恢复（#769）

本节承接Issue #769，适用before为main `a5f3ceeabbaccddae65935d97763f5a798f71ca9`，决定为[ADR-TOOLS-FROZEN-SOURCE-RECOVERY](../adr/tools-frozen-source-recovery.md)。原upgrade-tools仍是唯一工具维护owner。原common/peer已观测键的值保持；本单元下节限定已核正常退出对象的处理。正常新增registered peer在与原实际工具写集物理隔离时不因新增观测键被拒绝。新增peer不进入原备份/写入/删除集，原snapshot不刷新。#759只跳过prunable且.git不存在的失效注册条件保持。

既有install/resume/rollback继续原同源语义。新recover_frozen_source从完整修复源执行当前恢复engine；原cp.source完整源仍提供资产、legacy installation helper及preset installer，原root/source HEAD/tree token、public CLI/Core pair/plan/ref、preimages和rollback anchor继续验证。该区分只服务修复前schema1.0事务，包括#766，不改旧数据、不reprepare、不接收新源覆盖，也不吸收后续业务编辑。

原phase逐项续接；preset仍是pending，允许原installer同操作续接，不能从投影文件推断complete。complete只验证。rollback先核公共tools/data兼容，再原Guru preimages恢复。目标own resolver/installed/native与peer保持独立证明。frozen_recovery_required的原必需字段为同profile/action/ref；下节定义本次输入有退出位置字段时的加性透传。该出口回同owner，不能回旧同源resume；永久不匹配仍阻塞。工具成功不提供Task/Delivery gate。

代价限定为原比较修正、一个明示兼容profile及直接retry consumer；复用原engine避免第二阶段机，不增加checkpoint字段、registry、锁或通用迁移平台。旧事务终态且原恢复保留责任结束后，通过明确迁移移除兼容入口；不自动扫描删除API。只有原资产/执行边界、阶段协议、实际旧consumer或隔离写集变化才重新评估。原Architecture/RDT的candidate Check、final_integration/readback和最终质量链保持；目标安装与完整Release分别成立。

## 原 peer 正常退出的有限恢复（#769 D2）

适用 before 为 D1 实际 delivered head `aaf7f939e83c5a5230ecbb9d9f0827fd5c2e97ff`；决定见[ADR-TOOLS-RETIRED-PEER-OBSERVATIONS](../adr/tools-retired-peer-observations.md)。本节窄修订上一节原观测保持的适用解释；D1 历史和原冻结源恢复 ADR 保留。

只有 `recover_frozen_source` 加性支持可选 `retired_peer_roots`。AI 先读取原退出 owner 的实际结果，判断正常退出及当前恢复适用性；路径缺失或 Git 注册消失本身不提供该判断。字段只携准确对象位置，不携授权、pass、证明 bundle 或另一 owner 的 checkpoint。省略与空数组不建立退出例外，同源 install/resume/rollback 保持原义。

确定性代码核每个非空位置为原冻结 checkout-local 观测的准确绝对 root、不是目标、完整 Git 注册中不存在且 root 路径项本身不存在。完整注册包含 prunable 项，复用原 parser；原 peers 默认 `prunable && .git lexically absent` 过滤不变。只有已核 root 的已知 local active/selection 和 installed/source runtime 观测承接对象终止。此非空模式下其它缺枚举文件仍读取原路径核同值；common/gitdir 与存续 peer 真实变化继续拒绝。没有无限前缀跳过或自动退出推断。

roots 只在当前调用透传原 engine 的前后保持检查。原 source/public operation/plan/preimages/peer snapshot 不变，无新 cp 字段、退出台账或第二状态机。`frozen_recovery_required` 仅在输入实际含该字段时原样携回，包括显式空数组；唯一 consumer 以现有 presence-select 承接。终态不携 roots。新字段只由完整 matching schema/Interface/runtime/consumer 组合接受，不宣称 D1 的旧闭合 schema 接受它。

代价限定为原比较的对象细分及调用期位置列表；不接 C5、重建退出 checkout 或刷新 snapshot。原事务终态且原保留责任结束后，沿 MIGRATION-769 的原 owner 明确迁移退出。原退出依据、公共新入口回归、目标自身安装与实际 #766 恢复分别证明；没有实际恢复不得报告整体完成。注册/资产协议、对象边界或真实旧 consumer 改变时重新评估。
