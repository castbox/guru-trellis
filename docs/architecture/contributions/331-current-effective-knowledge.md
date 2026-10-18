# #331 当前有效知识 Architecture contribution

Identity：`architecture-contribution-331-current-effective-knowledge-v1`。状态：`reviewed_promoted`。Task=`331-current-effective-knowledge` / generation=`0` / Delivery=`d9698141-1db0-444b-a43d-6fe6ccdf6b65`。写前 authority 是 `bdb5185c673c91b2fb5cfc66ffbb33849904a69c` 的 Architecture `.100/active`；constitution=`guru-trellis-design-constitution-v1/current`。本文件属于受审设计差额；实际晋升关系以当前 Architecture authority 和原 owner 结果判定，不能替代最终 Check 或 committed Review。

## 边界、责任与取舍

旧 current 通过版本继承与贡献拼接表达知识，部分治理条款仍需读取后继说明才能执行。目标由原 RDT owner 管完整的 capability R/D/T 单元，由原 Architecture owner 管 foundation/current/target/governance/ADR 及两层栈关系。导航只定位身份、状态、位置和关系，完整定义仍由唯一正文提供。贡献保留 provenance，不成为晋升后查询当前答案的永久拼接前置。

选择 `legacy_boundary_convergence`：旧 Task 继续读其阶段适用版本和不可变 Git authority，实际依赖结束或原 owner 合法改选后退出旧普通读取；历史追溯保留。不向旧 current 双写新规则，也不新增 dual-read parser。未迁移单元保留显式 legacy 来源及限制，不能谎称全量 corpus 已迁移。

实际公共技术源拟为 `trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md`，由原 Architecture 能力在源侧维护；项目 `00-foundation/stack-selection.md` 精确绑定版本，只拥有选择、范围、差异，不将本项目 Task/分支/本机状态写入公共定义。无新服务、索引引擎、脚本 planner 或公共 DTO。

## Required concerns

| Concern | 适用性及本次处理 |
| --- | --- |
| authority-binding | applicable：Planning purpose3.0；Phase2/Review 与 promotion 保留4.0/Delivery2.0；写前 `.100` 可由固定B重读，新 CURRENT 作为 delta 受审。 |
| constitution-binding | applicable：完整语义不能靠摘要删除；原 owner 内聚；不用无consumer通用机制；旧依赖有退出。 |
| boundary-and-decision | applicable：当前完整单元与历史分开；沿 ADR-005/009/028/030；ADR-031候选解释新的正文组织及兼容决策。 |
| owner-and-single-writer | applicable：两个维护 Skill 各管其 authority；Task writers 隔离；原 promotion writer 单写共享current。 |
| compatibility-and-exit | applicable：旧Task固定适用来源；完整matching安装采用；公共I/O不改；旧普通读取按真实依赖退出，不改历史。 |
| gap-and-deviation | applicable：保留未迁移范围的显式差距，不以三个样本谎称全部历史已迁移；不关闭无证据GAP，不新增双authority。 |
| parallel-scope | applicable：各Task只写自己的贡献，串行晋升完整单元；不竞争共享current或其他Task贡献。 |
| evidence-and-freshness | applicable：三组RDT实际迁移、架构后继、两层栈及24次native对照分开验证；唯一Test记录first failure/成本/限制。 |
| review-and-promotion | applicable：独立candidate/final；独立Phase2评估完整candidate与proposed targets；原owner expected-current晋升；最终Check和committed全范围Review覆盖实际写入。 |

## 验证和晋升

project descriptor=`guru-trellis-architecture-convergence:repository:1`，check=`guru-trellis-architecture-convergence/1`，result contract=`guru-project-architecture-check-result-2.0`。本文件记录已纳入 authority 的设计差额；实际判断由原 Architecture owner 正式调用。完整结果将由 `docs/requirements-design-test-contributions/331-current-effective-knowledge/test.md` 唯一维护，不把目录、样例或静态检查当真实Agent/安装/Release证明。

本轮 authority 为 Architecture `.101`、RDT `.110`；原 expected-current 和独立 Phase2 仍是晋升约束，不由知识版本推定后续门禁通过。完整多平台矩阵、远端正式版本发布和业务采用不在本次证明内。
