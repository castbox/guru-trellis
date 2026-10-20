# #635 可移植共享生命周期架构贡献

Identity：`architecture-contribution-635-portable-lifecycle-v1`。状态：`proposed`，未晋升。Task=`635-portable-lifecycle`，generation=0，Delivery=`826d09cb-22d6-4950-90c8-3bbf8df8d8ea`。change_path=`legacy_boundary_convergence`。唯一详细设计是同目录design.md；本文不是gate或另一份生命周期模型。

## Before authority与实际问题

before为Git `7a7b60743499653ffeb81f6b31e627a02c33f579:docs/architecture/`，authority identity `guru-trellis-architecture`，constitution `guru-trellis-design-constitution-v1`，project contract `guru-trellis-architecture-change-contract-v1`。原ADR-024/027、ARCH-DOM-032/054与ARCH-GOV-009继续约束公共模型/原owner/唯一consumer。

Reactivate的shared admission读取本机seal/manual Finish/Cleanup，合法独立clone因此不能解释已完成共享归档。Closure公共结果无法一般性还原完整Issue动作集，而Finish只从common-dir交易取得它。Publish私有交易丢失后重prepare仍要求同交易，普通Open PR定位还假定当前本地branch等于原PR head。三项都有正常单主换机consumer，不需要攻击、锁、scheduler或第二Task模型。

## 选定变化与单写边界

1. 原Reactivate语义owner解释精确Git/GitHub历史，区分Task2终态、指定正式schema1、人工历史及未完closeout。原Finish共享结果不以本机seal/退出/Cleanup为前提；本机责任继续由原资源owner管理。新current入口为闭合shared archive profile，既有准确历史而不是当前树状态决定前驱资格。
2. Task2沿公共reopen，正式schema1沿Trellis PR #55公共formal operation。source锁定准确merge1e22及成功mainCI；原始history/TaskId/source保留，g只增加一次，已存在后继继续它。Guru不复制converter/store，不制造旧C/C/gate。
3. 原Closure单写最小共享动作载体，使用原公共Closure evidence关联。字段仅为原ResultRef、Completion关联、source和完整action_set，直接consumers只有原Closure恢复与Finish。载体不记录授权或terminal pass，不是审计数据库；消费者核public关系与live required状态。
4. 原Publish新增两个精确Open PR恢复profile，远端PR身份与B本地资源分开；只补实际未完成动作，当前readiness保留原owner。MERGED沿现行manual recovery，不重复merge。原Identity/Bind及Completion无空Delivery、资源expected-head和正常并行职责保持。

## Required concerns

| concern | 实际适用性与承接 |
| --- | --- |
| authority-binding | 适用：固定before与上述稳定authority，完整候选比较共享终态/本机责任，不用新CURRENT证明自身 |
| constitution-binding | 适用：原模型/owner和直接consumer完整；仅补不可推导动作集合，移除倒置依赖；不建立全局恢复台账 |
| boundary-and-decision | 适用：窄替代ADR-027/ARCH-DOM-032旧格式接受范围与Finish seal准入片段；必要ADR候选见同目录adr-portable-lifecycle.md |
| owner-and-single-writer | 适用：Core/CLI唯一模型writer，Guru原Closure/Finish/Reactivate/Publish独占各自语义与确定性适配；新载体由Closure单写 |
| compatibility-and-exit | 适用：新闭合profiles/显式schema迁移，普通本地与manual路径保留；source、官方native及完整Guru分发成套采用，旧安装固定或原owner迁移 |
| gap-and-deviation | 适用：不声明关闭ARCH-GAP-006/008；没有多主、跨机锁或普通legacy双读。未知状态和必要输入缺失仍具体停止 |
| parallel-scope | 适用：同Task/D1隔离贡献，独立Task资源不互设准入；原并行子Agent职责不改，shared promotion仍唯一原owner |
| evidence-and-freshness | 适用：精确source/Git/PR事实、当前语义、工程执行和目标安装分层；最小载体经原public result/AuthorityRef绑定，无全链digest或授权字段 |
| review-and-promotion | 适用：原独立candidate与final_plan、完整phase2/candidate Check，原owners final_integration后刷新candidate；最终Check/commit/独立committed Review覆盖真实after |

## 拟写完整单元与晋升

命中Architecture的domain lifecycle、distribution及governance职责单元，原ADR-024/027与ARCH-DOM-032/054；RDT命中task-delivery-lifecycle和completion-closure的requirements/design/test完整单元。Planning只形成此真实贡献/必要ADR；实施按delta_first准备完整proposed正文，不在本轮写shared CURRENT、总导航或批量历史。

独立Architecture及原candidate Check审完整implementation/proposal后，原Architecture/RDT owners在final_integration读取真实targets并合成完整有效定义、readback，再由implementation刷新全candidate/begin_check。最终Check、TaskCommit、独立完整committed Review、readiness与Publication消费实际晋升结果。贡献存在不等于promotion或pass。

## 验证与退出

source构建/采用及只读真实旧样本inspect已完成，但不证明目标恢复。V1–V8按implement.md执行：独立common-dir native两条再次Finish、活动ref、三类远端副作用、资源/双Task隔离、真实缺失、旧样本及唯一代表安装profile。普通source/单元命令不能冒充原生或Release成功。

只有明确支持的旧consumer完成一次性公共收敛后，才在显式迁移中移除legacy-only入口；raw/Git历史及原资源责任保留。旧本机seal只留给原local资源consumer，不能再次成为shared admission。不存在通用定期scan、第二current或新永久协调服务。
