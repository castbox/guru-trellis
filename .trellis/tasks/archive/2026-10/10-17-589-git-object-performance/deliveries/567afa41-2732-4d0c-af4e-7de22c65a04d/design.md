# D5 上游来源准备设计

## 固定范围

开发基线main@3676b9e；本Delivery内容基线B=875bbd115eba3bd418c30339f69b36a0b94e7d9b，原content_base选择最大已delivered祖先；PR目标main，禁止自动追赶。D1–D4历史不重写。D5仅形成后继原source_locked安装可消费的clean committed Guru source，不执行dirty source安装。候选Architecture已独立formal baseline_current/no_architecture_impact；本设计仍须Wording→fresh final_plan。

## 唯一source-design处置矩阵

|来源与原承诺|处置、落点与影响|
|---|---|
| #589 §5.7/AC13/15 canonical来源与原安装责任 | retain：canonical source/trellis-source.json改为c7bd746、exact parents/tree/CI，三个当前README和现有项目public-docs spec同源；D5只准备来源 |
| 原tools-only owner source_locked要求clean Guru源 | retain：D5先完成Check/TaskCommit/fullReview/Publish；原Completion分配D6，D6从真实D5干净提交执行工具安装；不提前提交未检查内容 |
| #589 AC06原公开摘要与独立输入检查 | retain：snapshot残余仍属原上游，已评论#47；不导入private observation、不复制hash算法，不把local_commit收益映射为Guru PR收益 |
| #575 exact-candidate Release矩阵 | retain：本批定向source/文档/ownership；不执行或声称矩阵、业务升级 |

没有额外normative设计。当前constitution、原source lock/public tools合同为约束；原contract_incomplete只修复阶段顺序，不削减整体scope。

## 采用来源与当前映射

Fork=c7bd746b42d75f73534c85e263cd6b51fe0e5287，parents=[b0d87f952043058e21001a002b661bf2db56b1fa,bf8130fedceee907836bd0a2215854b38a8bf891]，tree=02c6ec8688920d8acb56d1467d6725b03012c0e0，mainCI38994652194。CLI/Core0.7.0-castbox.3、pnpm10.32.1不变。原2a6→c7生产diff只有#47两个owner、helper及模板注册；无Core/API/schema/session/maintenance签名变化。

当前来源段落更新；稳定.3/历史来源、D1–D4 before不变。现有public-docs落点为.trellis/spec/docs/public-docs.md，属于项目spec，不是preset canonical投影；不新增spec/docs来源或installer映射。原apply在本Task因historical archive返回upstream_delivery_migration_required，未写入投影。D5保留该首次失败和旧安装来源，D6从本批clean committed source经原source_locked tools-only更新完整目标投影及receipt。不迁移archive、不绕过预检、不手工patch.trellis/scripts。

完整c7干净checkout按pnpm正常build后记录stamp，validate_fork_source核对commit/parents/tree/CI/cli/core/packageManager/templates/build。发布tgz三份SHA256SUMS均通过；CLI两个Python模板packagemode644/source-build755但bytes一致，D6选择source-built正式路径，不修改包mode伪造一致。

## 验证与后继责任

本批执行真实Forksource验证、currentdocs/ownership/source/现有installedpackages与三平台overlaydrift、mode与sidecar检查、diff hygiene；现有installed验证只证明其原安装内容，不能证明新Fork采用。可在无历史Task代表target通过原apply验证新source投影；本Task完整投影由D6承担，原preset写入不包含本Task/session/peer或upstream-owned文件，sidecars逐个核对。完整Check和B..HEADReview覆盖本source-onlyslice。

14组×2原before及performance-contract是D6的直接工程输入：固定同GuruPython、工具、exactpool，D6source_locked安装后新Forkafter。D5不声明after/installed通过。上游44冻结门槛原evaluator复核仅证实原owner结果。手动恢复snapshot3/30paths uniqueOID1对应4/31sha256构造、oracle一致；该AC06残余保留，不以source更新代替实现。
