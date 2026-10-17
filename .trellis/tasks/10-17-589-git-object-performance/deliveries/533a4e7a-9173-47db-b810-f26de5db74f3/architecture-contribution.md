# #589 D7 公开不可变摘要消费收敛

identity=architecture-contribution-589-public-git-content-v1；state=proposed；Task589-git-object-performance/gen0/D7；change_path=dedicated_refactor_slice。适用baseline=current-main-0.6.17-guru.94，constitution=guru-trellis-design-constitution-v1/current，change-contract=guru-trellis-architecture-change-contract-v1。贡献尚未晋升；晋升时由原owner fresh读取live expected-current，不预置未来identity。

Before：manual recovery与history query2通过Guru CandidateObjects读取并物化临时snapshot，再交上游filesystem candidate_content_ref；相同blob在路径间重复读取/hash，history还有准备预读。After目标：同一操作直接调用Fork9f40公开GitCandidateContent，其仅负责不可变对象读取与摘要复用；原业务owner逐输入保留结构、身份、关系、祖先、expected摘要、PR/merge/cutoff及恢复判断。摘要字节/公开结果不改。完整.4来源由原source_locked维护消费，版本current断言与能力检测一致；原历史来源支持不变。

| Concern | 适用性及本批职责 |
| --- | --- |
| authority-binding | applicable：根PRD与live#589、D7设计为行为authority；Planning3.0 candidate/final，后续2.0阶段按原owner执行。ADR-024/027、ARCH-FND-001/002约束不变。 |
| constitution-binding | applicable：官方public API集中技术职责，删除无consumer快照实现；minimum-necessary-complexity/cohesion-change-isolation/debt-one-way-convergence，不新增通用框架、持久缓存、公共DTO或第二摘要authority。 |
| boundary-and-decision | applicable：只改变Guru至Fork的调用与资源生命周期；source lock精确9f40、CLI/Core.4；语义门禁仍Markdown，script只做确定性事实。无新决策例外，不需要新ADR。 |
| owner-and-single-writer | applicable：上游delivery_store独占摘要算法；manual/history保留业务判断与对象准备；Author独占规划；原installer写投影/receipt；Architecture owner独占shared-current晋升。 |
| compatibility-and-exit | applicable：移除两个caller与CandidateObjects/snapshot专属tests，保留其他consumer使用的git_object_batch；不保留新旧摘要双路fallback。filesystem mutable API不改；.3历史支持不全库替换。最终目标完整投影由后继原tools owner完成。 |
| gap-and-deviation | applicable：本批目标消除重复物化/hash的实现偏移；无关ARCH-GAP不关闭、新增或恶化。未完整核对当前读取/计算观测、未完成正式安装及未晋升前保持未验证，不凭上游CLOSED关闭本Task。 |
| parallel-scope | applicable：仅本Task canonical来源/consumer、测试与隔离贡献；允许worker按文件划分，不竞争shared current。禁止改peer#575、业务安装、上游脚本/global/node_modules及历史Task。 |
| evidence-and-freshness | applicable：保留before及历史阈值/FAIL为观测；当前按live#589§6以冗余读取/计算消除、必要独立检查与有界资源验收，不设耗时改善百分比。使用同输入after、正式公开链、actual-root volume与独立hash/RSS；per-input检查保持。新context按actual repo、完整commit/blob与规则绑定；prepare切root关闭重建，退出关闭，可变输入下次操作刷新。 |
| review-and-promotion | applicable：首次完整committed独立Review后原owner按live expected-current晋升；新增diff须fresh Phase2/TaskCommit/完整Review，Publication只接受reviewed_promoted。当前proposed不证明完成。 |

项目check采用guru-trellis-architecture-convergence:repository:1，入口docs/architecture/06-governance/change-contract.md，id/version=guru-trellis-architecture-convergence/1，result-contract=guru-project-architecture-check-result-2.0；范围为九concern、原writer/资源生命周期、before/after、旧路径删除、完整来源及review/promotion；绑定ARCH-GOV-006..009、ADR-005/009及ARCH-GAP-006/008并按ADR-028阶段适用解释。Planning审查真实设计/贡献，Phase2检查实际差额和证据，完整Review独立检查B...H，不能由脚本pass替代。

回滚仅通过原维护owner采用完整匹配旧source/pair并恢复相应canonical consumer，不混装版本；原Delivery事实不改。后继正式安装、最终盘点及整体Completion是明确剩余consumer，本贡献不能替代其交付或#575矩阵。
