# #695 需求差额

状态：proposed；authority 为 guru-trellis-rdt，适用基线 `8d746ce561c464ca28af4dc91adf085132e4098c`。来源为 live Issue #695 与整体 Task R1–R6/AC1–AC4。

新增完整能力单元 [R695/BEH695](proposed/docs/requirements/current/json-input-carriers.md)，覆盖载体、诊断、Bind、原错误合同和分发。原 R630-02 的合法 inline/stdin 兼容仍有效；其他现有单元、稳定身份、历史定义不变。不递增全局版本，共享 current 尚未写入。

完整关系和保留边界见 [traceability](traceability.md)。这里不复制公共 schema，不将 source 修复或知识接受称为安装/业务/Release 成功。
