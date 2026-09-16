# #418 Architecture Contribution

Identity：`418-archived-review-refresh-v1`；状态：`implementation_candidate`；change path：`target_native`。这是已实现且经过定向验证的task-owned candidate，不是shared current authority；独立committed-diff review与promotion尚未完成，不证明发布。

## Authority 与范围

- 当前 baseline：`docs/architecture/README.md` / `current-main-0.6.17-guru.52` / active。
- 当前设计宪法：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / current。
- 项目合同：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`。
- Guru owner 合同：`guru-maintain-architecture-baseline:2.0`。
- 需求：[Issue #418](https://github.com/castbox/guru-trellis/issues/418)，`R418-04/05`。
- 完整技术合同：`.trellis/tasks/09-16-418-closeout-identity-recovery/design.md` 第4节；本文件只记录架构影响、决策与提升责任，不复制DTO正文。

## Before / Target

Before：completed archive不能进入普通Publication；新archive-HEAD review不符合Finalizer原归档锚点。只有错误文案和mapping修复不能闭合复审链。

Target：在Merge、Branch Review、Publication、Finalizer四个原owner内部增加专用只读profile。三个新的success exits显式连接唯一consumer；新PR snapshot不承担批准语义；新Publication审查后才生成可供Finalizer验证的payload。H与A分离，普通mutation路径不变。

Branch Review实际base B作为最小范围身份传至Publication/Finalizer；title/body快照只服务复审内容一致性。Publication新增profile专属finding/blocked union，不把task_work或metadata问题伪装为external blocker。Architecture仍在三个原stage逐次调用，用既有source_exit的闭合集合识别只读范围，AI在需写入或证据不current时返回blocked，validator拒绝该来源下不符合边界的需写出口；普通来源路由不变。

预期图增量：0 Skill、0 command、4 profile、3 external exit。实施时从live registry/interface派生总图与所有consumer；不将旧4个Merge exits的current陈述当作已经迁移。

## Required Concerns

| Concern | Applicability | 本任务合同 |
| --- | --- | --- |
| authority-binding | applicable | 同时绑定上述Guru/project/current identities；内容漂移重新进入owner |
| constitution-binding | applicable | 命中concept-semantic-completeness、cohesion-change-isolation、minimum-necessary-complexity、debt-one-way-convergence；正文仍由设计宪法独占 |
| boundary-and-decision | applicable | 专用只读复审与普通active preparation分离；保留ARCH-DOM-002/013/015，新增边以唯一consumer闭合 |
| owner-and-single-writer | applicable | Branch Review独占复审，Publication独占payload语义，Finalizer独占archive continuity与handoff，Merge独占最终merge；只读profile零业务/远端writer |
| compatibility-and-exit | applicable | 新profile/exit独立schema，原profile不放宽；旧gate不升级为pass，不保留legacy shim，原输入消费者继续按原合同工作 |
| gap-and-deviation | applicable | 不关闭ARCH-GAP-006/008，不扩大#398/#419生命周期；修复#418归档复审缺口，无退出双写或scope ledger回潮则拒绝 |
| parallel-scope | applicable | 只改当前task隔离范围；禁止普通分支写shared current、修改业务task状态或替其它task重建mapping |
| evidence-and-freshness | applicable | 规划内容、current authority、完整候选或committed range绑定；test证明A/H、snapshot和零mutation，未运行不得写verified |
| review-and-promotion | applicable | 本贡献及ADR草案先经完整committed-diff review，Architecture owner按expected current串行promotion；promotion diff重复Phase2/Commit/Review |

## ADR-418 草案：归档复审与历史锚点分离

状态：`proposed`，不是accepted ADR。决策来源为本task完整设计；最终ADR identity及导航由Architecture promotion owner管理，避免修改shared ADR索引。

选择专用只读profile：复用原owner判断能力和底层中立校验，但不复用active preparation状态门槛或可写transaction loop。新A证明当前独立复审；原H证明既有archive历史。PR快照仅绑定读期间内容，新Publication判断不能由快照digest代替。

拒绝替代：放宽普通Publication status、A替换H、整体restore为active、手改旧gate、仅改善错误文案。前三者破坏原边界或引入额外写入，后两者不能证明当前复审和完整恢复。

代价：增加四个profile和三条public边，必须同步schema/consumer/eval/distribution；收益：不重复归档或发布，不引入第二owner或回写历史。不存在长期兼容例外；旧gate仍走原stale语义，新增profile仅fresh authoring。

## Project Check 与提升

采用当前 `guru-trellis-architecture-convergence:repository:1` descriptor；entrypoint为项目change-contract，rule refs为ARCH-GOV-006..009、decision refs为ADR-005/009、gap refs为ARCH-GAP-006/008。当前candidate的实际四owner wrapper链、三个Architecture只读阶段、A/H/B与快照绑定、零mutation及全部目标平台投影已有定向验证；结果不等于独立committed review或promotion。

Phase2验证完整candidate before/after与适用check；Branch Review在独立committed range重算。未经两阶段验证不得提升。Promotion将新的只读边写入CURRENT/DOMAIN/接口清单及ADR导航，同时更新旧“四个Merge exits”陈述，不改写其它旧profile语义。RDT贡献由其独立owner承接R418/D418/T418，两个authority的期望版本和状态必须一致。

当前验证基于task HEAD与origin/main均为 `78651e2068184e9e52a778fe33eda8b2bd7c8e0b` 的未提交candidate：五个package共301项测试、真实installed wrapper链3项、post-owner staging3项通过。三平台reapply、installed和drift通过，sidecar为0。具体命令与边界见task implement.md及RDT test contribution。

尚未验证：fresh native语义执行、原业务实例和Release矩阵；未完成独立committed review或shared-current promotion。post-owner/fixture通过不替代这些证明。
