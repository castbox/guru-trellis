# D1 历史 Delivery 查询与手动恢复对象读取

Direct Source：https://github.com/castbox/guru-trellis/issues/589 第3.2、3.3第一项及第5–8节；整体范围见 Task 根 prd.md。

本批盘点全流程Git对象操作，并优化 HistoryContext.candidate、commit_candidate 及真实调用方，消除逐候选路径 ls-tree/cat-file 和同批重复blob请求。候选摘要、路径/mode/删除、原错误、固定截点、对象准备隔离、手动合并与stdout丢失恢复结果保持。必须先取得两档候选及多Delivery完整基线，再固定本批耗时/内存标准后改生产实现。

本批交付后仍剩 D2 bounded continuity、D3生命周期与全流程联合验证。上游不可分离前置不计为完成，不修改上游或历史Task。
