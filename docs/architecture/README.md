# Architecture Baseline SSOT

Identity：`guru-trellis-architecture`；状态：`active`。适用范围是 Guru Team Trellis 扩展仓库的 Architecture authority。精确内容由完整 Git revision 与 repository-relative locator 定位；普通 Task 不递增全局知识版本，也不登记独立主题。

## 职责范围与发现入口

下表只给出稳定职责范围。Agent 在本阶段适用的 Git revision 中，通过目录、稳定 identity 或概念定位完整单元，再读取必要关系。表中不枚举所有知识单元。

| Role | Scope / status | Discovery scope |
| --- | --- | --- |
| FOUNDATION | accepted_constraints / accepted_selection | `docs/architecture/00-foundation/` |
| CURRENT | evidence_bound；逐单元核已验证或未验证范围 | `docs/architecture/01-current/` |
| TARGET | accepted_target；不表示已实现 | `docs/architecture/02-target/` |
| DOMAIN | current_boundaries | `docs/architecture/03-domains/` |
| INTEGRATION | current_integration_boundaries | `docs/architecture/04-integrations/` |
| GAP | 由实际差距及其 owner/退出条件决定状态 | `docs/architecture/05-gaps/` |
| GOVERNANCE | current；含项目 change contract 与 project-check protocol | `docs/architecture/06-governance/` |
| PLAN | execution_dependencies；不表示完成 | `docs/architecture/07-plans/` |
| ADR | 历史决定及其接受/替代范围 | `docs/architecture/adr/` |
| EVIDENCE | 各自观察截止点和验证范围 | `docs/architecture/evidence/` |

先用 `rg --files docs/architecture/<职责目录>` 确定文件范围，再在该范围按稳定 ID、alias 或概念检索。读取命中的完整单元及问题所需的 R/D/T、Architecture 关系；不因搜索排序、文件存在、日期或版本更大而选 authority。单元自身的原 owner、状态、适用来源、晋升依据和替代范围确定其可用含义。缺来源、晋升依据、完整定义或有效引用，或存在重复 current 时，说明受影响结论并回原 repair/澄清。

`contributions/` 是隔离候选或历史来源，不属于上述 current 发现范围；其 proposed 正文不能因位于本仓库而生效。TARGET、ADR 和 EVIDENCE 分别保留目标、决定理由和观察职责，不能替代 CURRENT。已迁移单元直接承载完整适用定义，普通查询不回放贡献链拼接其含义。完整共享读取方法仍由 `.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md` 单写，原 Architecture package 加载同一合同。

## 维护与关联 authority

原 Architecture owner 在本方 Task 隔离贡献中准备完整拟写。Planning 批准、实施和真实工程验证完成后，由原 maintenance owner 在提交前 final_integration 重读真实目标、整合、写入并读回；整合只表示 integrated_pending_review。TaskCommit 纳入全部真实 after，随后固定 committed candidate 的同一次独立 Review 先判断 Architecture before/after，再承担九维与完整区间职责；实际通过后才是 reviewed_promoted。Planning 独立 candidate/final 判断保持，文件位置或整合事实不产生独立 semantic pass。当前时机与窄替代范围见 [ADR-POSTCOMMIT-INDEPENDENT-REVIEW](adr/postcommit-independent-review.md)。

独立主题只维护自身正文或自身目录内的局部导航，以及真实受影响的引用和关系。不向本入口、下级共享 README、system/ownership 汇总、ADR index、共享 manifest 或生成需提交索引逐项登记；不追加无关全局版本或合并历史。同一能力或真实共同关系仍由原 owner 语义整合，不复制关系规避重叠。只有本入口自身的身份、scope/status、位置、发现合同或必要跨体系关系实际改变时，才维护本入口。

RDT authority identity 为 `guru-trellis-rdt`；其稳定入口为 [Requirements](../requirements/README.md)、[Design](../design/README.md) 和 [Test](../test/README.md)。各原 owner 分别拥有自身正文及必要关联，不在本页复制另一 authority 的业务定义。

## 迁移范围与历史来源

[采用与退出合同](../../trellis/presets/guru-team/MIGRATION-711.md)定位 `knowledge-navigation-1` 的切换条件、失败恢复和旧写退出。安装新规则不等于项目文档已迁移。本仓本次切换的是 RDT 与 Architecture 入口发现及独立主题维护；原完整正文路径、稳定 identity、原始证据和真实 public API 版本保持。

未列入既有完整单元迁移的能力，仍读取原完整正文及其必要来源。[MIGRATION-331](../../trellis/presets/guru-team/MIGRATION-331.md)定位既有未迁移范围，[MIGRATION-638](../../trellis/presets/guru-team/MIGRATION-638.md)定位最终整合和身份切换。这里不声明全部历史语料已改写为新的完整单元；既有 `adr/README.md` 仍可解释其历史导航，普通新增不继续向它登记。

在途 Task 继续按其阶段适用版本读取。最终集成触及已迁移单元时，原 owner 重读实际目标并写当前完整定义；旧读兼容不授权继续写旧共享索引。Task Finish、合法 Reactivate 重选或真实依赖变化按原合同结束其旧普通读取；历史 Git 快照保留原含义。

| Historical identity | Status | Exact source | Relations |
| --- | --- | --- | --- |
| ARCH100-PINNED-TASK | historical_applicable | [固定旧authority](https://github.com/castbox/guru-trellis/blob/bdb5185c673c91b2fb5cfc66ffbb33849904a69c/docs/architecture/README.md) | immutable Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c:docs/architecture/` |
| ARCH101-PREDECESSOR | historical_applicable | [前驱完整 authority](https://github.com/castbox/guru-trellis/blob/33f18a768c9c8d901f34b899934ac40c3d97cc5b/docs/architecture/README.md) | `current-main-0.6.17-guru.101`；successor `current-main-0.7.0-guru.102`；immutable Git `33f18a768c9c8d901f34b899934ac40c3d97cc5b:docs/architecture/` |
| ARCH102-PREDECESSOR | historical_applicable | [固定前驱 .102](https://github.com/castbox/guru-trellis/tree/0543731bf52aa80842fde5db47332380de513cf0/docs/architecture) | immutable Git `0543731bf52aa80842fde5db47332380de513cf0`；同tree解析完整authority和必要引用 |
| ARCH104-PREDECESSOR | historical_applicable | [固定前驱 .104](https://github.com/castbox/guru-trellis/tree/39169628f5f79cb48673eae96a36670e73f4dbbb/docs/architecture) | immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb`；同tree解析完整authority和必要引用 |
| ARCH105-PREDECESSOR | historical_applicable | [固定前驱 .105](https://github.com/castbox/guru-trellis/blob/9cec623833b61814f1175f31acde4fa81334cdb0/docs/architecture/README.md) | immutable Git `9cec623833b61814f1175f31acde4fa81334cdb0:docs/architecture/`；同tree读取原完整正文和必要关系 |

这些历史行只保留原来源与版本边界，不随普通 Task 追加。知识接受不证明 Delivery、Completion、安装采用、业务效果或 Release。
