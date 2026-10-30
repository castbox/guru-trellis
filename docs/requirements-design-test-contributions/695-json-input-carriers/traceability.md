# #695 双向追踪与替代边界

适用基线 `8d746ce561c464ca28af4dc91adf085132e4098c`；authority identity 保持 guru-trellis-rdt。`proposed/` 镜像最终 repo-relative target，其内部相对链接按最终路径解释。三个正文与三个 current 导航只在原 final_integration 写回。

| 整体范围 | 完整需求 | 完整设计 | 完整测试 |
| --- | --- | --- | --- |
| R1/R2/R5；AC1/2 | R695-01 | D695-01/02 | T695-01/03 |
| R3/R5；AC1/2 | R695-02/04 | D695-01/02/04 | T695-01/03 |
| R4；AC3 | R695-03 | D695-03 | T695-02 |
| R5/R6；AC4 | R695-04/05 | D695-04/05 | T695-04/05 |

完整 [Requirements](proposed/docs/requirements/current/json-input-carriers.md)、[Design](proposed/docs/design/current/json-input-carriers.md)、[Test](proposed/docs/test/current/json-input-carriers.md) 是新增单元。必要前驱为同基线 docs/{requirements,design,test}/current/native-compatibility.md 的 R630-02、D630-02、T630-02/07；这些仍有效条件和历史三系统矩阵保持。没有删除/拆分/合并既有知识，不制造第二公共输入协议。

canonical reusable 合同在 trellis/presets/guru-team/spec/workflow/companion-scripts.md Error Handling、Bind references/json-inputs.md 和 MIGRATION-695.md。Architecture entry/distribution 保持原 authority；Planning no-impact 不替代 Phase2/Review 独立结论。candidate Check 消费完整 proposed；原 RDT final_integration owner 晋升；final Check/Review 审实际写入；Completion 只消费其原交付及实际验证结果。
