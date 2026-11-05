# Issue739 Architecture contribution

Status：proposed；change_path=target_native。Task：resolved-gitlink-check，generation0；Delivery：95896a2b-7c5f-4aa2-b201-46b62573f94f。来源为Issue739、本Task整体PRD及所选Delivery设计，不是shared-current成功声明。

本贡献提供两个完整拟写：739-parent-git-content/proposed/03-domains/parent-git-content.md → docs/architecture/03-domains/parent-git-content.md；739-parent-git-content/proposed/adr/parent-git-content.md → docs/architecture/adr/parent-git-content.md。新增独立主题不修改共享根或ADR索引。原Authority在这些目标尚不存在时保持现有baseline/constitution/change contract，不以新文件自证通过。

替代范围为父仓流程对子仓HEAD/root/clean/初始化的准入和重复捕获；保留父index/tree内容、stale、exact commit、独立child root及破坏性清理边界。必要data-contracts和各包合同由原规范owner同步替代，不能仅靠领域文档解除旧规则。RDT原owner维护自己的完整当前定义。

独立final_plan审本贡献和当前design；实际实现后原candidate Check审完整实现及全部拟写，原Architecture owner在final_integration写前核live targets并晋升/readback，实现owner重绑after，再执行最终Check/commit/独立Review。上游API和目标工具采用未完成时如实保持外部能力边界，本Task完成仅覆盖Guru侧，不能宣称外部恢复。尚未修改shared CURRENT。
