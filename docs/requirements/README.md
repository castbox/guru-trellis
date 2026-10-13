# 验证仓 Requirements authority

版本：531-validation-rdt-1。状态：active。适用范围：此独立验证仓，首次版本，无 predecessor。
来源：仓内 README 的受控验证定位与当前 no_issue Task 整体 PRD；后者保留具体切片和执行验收，不复制到本 authority。

REQ-531-REMOTE-1：本仓承载原 Publish/Merge 真实远端成功与同结果恢复观察；观察必须维持原 producer identity 和公共状态 ownership。
BEH-531-HISTORY-1：读取的已交付历史事实与当前 gate 分开，缺少真实子场景证据时准确声明边界。
REQ-531-BOUNDARY-1：仅专用 base 与独立样本；不交付业务功能、不关闭 Issue、不改产品仓和旧样本。

设计责任分别链接 [RESP-531-RECOVERY-1、CONTRACT-531-STATE-1、RESP-531-BOUNDARY-1](../design/README.md)；对应测试策略见 [STRATEGY-531-LIVE-1、SCENARIO-531-OUTPUT-1、CASE-531-BOUNDARY-1](../test/README.md)。
Architecture 继承仅 locator/version/status：docs/architecture/README.md / 531-validation-foundation-1 / active。由本轮原 Architecture baseline_current 的实际 successor 身份继承；三层原 RDT bootstrap owner 检查来源、导航与双向追踪后激活。
