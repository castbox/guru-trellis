# #495 旧安装迁移架构贡献

Identity：`architecture-contribution-495-legacy-installation-upgrade-v1`；state：`reviewed_candidate`；task：`.trellis/tasks/10-06-495-legacy-installation-upgrade`；requirement：castbox/guru-trellis#495。expected current：`current-main-0.6.17-guru.71`。绑定 `guru-maintain-architecture-baseline:2.0`、`guru-trellis-architecture-change-contract-v1` 与 `guru-trellis-design-constitution-v1`；change path：`legacy_boundary_convergence`。

## Required concerns

| Concern | Applicability / decision |
| --- | --- |
| authority-binding | applicable：live #495 修订 #481 迁移拒绝，完整继承无人员/current-only；共享 .71 和历史 tag 不先行改写。 |
| constitution-binding | applicable：官方 Fork/core extension 与 source package、完整 task 身份、单 writer、局部私有备份和单向出口；无原则例外，不建立评分表。 |
| boundary-and-decision | applicable：Fork core/task writer，Guru 资产转换/编排，既有生命周期 owners；ADR-015 不变，迁移拒绝的修订仅为候选。 |
| owner-and-single-writer | applicable：migration 无新的 task binding/session store；current preset 唯一 current Guru 安装 writer，shared current 只由串行 promotion。 |
| compatibility-and-exit | applicable：旧 parser 只在 standalone migration；成功后 current-only，历史 bytes保留且不成为 authority；停止旧来源支持时删除局部 parser。 |
| gap-and-deviation | applicable：旧仓无法升级的实际差距；正式 Fork source lock/CI 已验证，本地实现不证明同一远端 Guru HEAD 的正式安装与全部旧交付验收，未完成目标保留 unverified。 |
| parallel-scope | applicable：此 task 只写隔离贡献/已批准 source/code/tests，真实 downstream及其它worktrees只读，不竞争 shared current。 |
| evidence-and-freshness | applicable：真实 core0.6.16/Guru41 到后继；public安装、两个 owner接续、普通部分恢复、写后rollback、preservation和distribution；每个gate fresh读取。 |
| review-and-promotion | applicable：完整 Phase2、committed独立BranchReview之后 expected-current-bound promotion；其新增diff再次check/commit/review。 |

## Before / after 与 evidence

Before：update 拒绝旧安装，current task writer 拒绝 personnel/缺 generation/source；拒绝证明数据不变，不证明升级。
After候选：独立 semantic migration 明确旧格式投影、真实 managed更新、current owner接续与最小恢复/回退；普通入口保持严格。脚本不判断 scope、source disposition、gate pass 或 rollback适用性。

本轮范围来源：[混合库存说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6014030676)。current reader 正向区分 known-legacy，仅保留旧 id/ref 占用且排除 current candidate；direct old/目标冲突/坏 current 保持拒绝，不将普通错误码作为万能 legacy skip。独立 migrate 的 reviewed deferred 私有 TaskRef/hash 仅供原字节 preserve 与 installed inventory consumer，不成为 lifecycle/session/恢复 authority。current-installed 与 migration-continuation 均须真实混合库存样本。rollback 直接 consumer 使用 core 成功时固定的 task-content token 与相关 control 初始基线，resume 不吸收部分迁移期间的新业务工作；不新增全链状态、锁或 writer。

本轮 Planning impact、两类 qualifications、wording、Architecture/RDT owners 与 Planning Approval 已实际重新执行；它们只审查当前规划，不证明正式依赖或完成验收。shared current `.71` 不在本轮写入范围。

Project check：`guru-trellis-architecture-convergence:repository:1` applicable/blocking。实现候选维持 Fork core/task schema、Guru migration/preset、current lifecycle 各自唯一 writers；known-legacy 仅作 reservation，deferred 没有恢复 authority。实际 public 六场景、current owner/Planning 接续、partial resume、eligible rollback/旧 runtime smoke、新工作保护及 source/installed/dogfood/reapply 已通过。固定 task-content 锚点覆盖 converted 与 deferred，失败 resume 不吸收新增 notes；没有额外 state/schema/公开字段。

正式 Fork PR #27 已合并至 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / `0.7.0-castbox.2`，成功 main CI `37473087582`。真实干净 built checkout 的 `validate-source` 通过，official collector/hash 的 dogfood 183 文件投影与 9 项回归通过；canonical apply/reapply/source/installed/drift 通过且 sidecars 为零。正式 Fork 下 public lifecycle 六场景最终 6/6，通过普通 partial recovery、实际写后精确 rollback、native meta/deferred notes 新工作保护和 current owners/Planning 接续。真实业务仓 10 个 checkout 与 Fork HEAD/status 保持；共享 managed Python cache 是已说明的 bootstrap 写入边界。installer 最终完整 101、upgrade contract 73、ownership 9、migration package 14 均通过；runtime 完整 64 中 62 pass、2 dependency-install 失败后原样重试 2 pass，没有修改代码/测试。

已迁移隔离 fixture 还实际执行同一 `.2` Fork 的 current dry-run（无写入）与 preserve-mode update、同源 canonical 本地 workflow projection 和 current preset apply/reapply；安装/ownership/hash/零 sidecar与数据保留均通过，重复应用无漂移。manifest 如实声明当前 Guru HEAD 的 dirty 本地来源，因此仍是 local_candidate，不能升格为正式远端同源证明。

本轮审查对象为[顺序说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6018378988)与正式规划确定的“正式验收用迁移候选代码与合同”首个 slice。该 slice 的 project check 须 fresh 判断实际实现及本地证据；不把整个迁移目标或 GAP 标为完成。完整目标仍缺同一远端 Guru HEAD 的正式 source_locked/provider，以及 MIG-495-06 完整来源/真实旧在途代表证据。已实际读取 PR #195 open、#210/#58 merged，但真实终态不代替在途样本。独立 committed full-diff review、expected-current 候选 promotion、publication 与最终 merge/Completion 尚未执行；发布/真实业务升级保持独立边界。
