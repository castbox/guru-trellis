# #599 清晰写作与入口读取 Architecture contribution

状态：`reviewed_promoted`；change_path：`target_native`。原 Architecture owner 按 expected `current-main-0.6.17-guru.94/active` 晋升 `.95`。constitution v1、project change contract v1、原 owners、GAP lifecycle 与软件四轴保持；无新 ADR。

TaskId：599-clear-technical-writing，generation0；Delivery 661412bf-0be8-4c0c-9c05-b82f31cb7160。

首次通过的独立完整 committed Review 范围为 `dev@ea9998c36a188f3afae1d7d6e5746edc07fa003f...af246dc6184e6c779f2f08ab72a4ff889c6dbc0f`。Git 对象 `af246dc6184e6c779f2f08ab72a4ff889c6dbc0f:docs/architecture/contributions/599-clear-technical-writing.md` 保留不可变的晋升前正文。新增晋升差额仍须 fresh Phase2、TaskCommit 与不同 reviewer 的完整 BranchReview。

## 决策与边界

沿用 current .94 的 Markdown 控制面、managed-spec、原 semantic owners 与受管入口装配。唯一正文位于 canonical preset spec，安装副本供 Agent 读取。加载定位接入既有 AGENTS block、workflow 与独立 Skill/平台入口；不创建语言审批阶段、runtime state、公共 DTO、wrapper 或 hook。

新增责任是 Agent 在首次实质文本前完整读取并在输出前按其现有职责自检。原生注入仅在全文完整时消费；其余由 child 自读。缺失暂停受影响正文，恢复后原请求继续。脚本只校验分发、引用和机械事实。

## 引用与并行写入

change_path=target_native。继承 ADR-005、ARCH-FND-001/002、ARCH-DOM-036/041。无新 ADR 或兼容双路径。具体加载设计由当前 Delivery design.md D3–D6 和 canonical 正文拥有；长期规则不复制到本贡献。

本次 shared-current promotion 由原 Architecture owner 在独立 committed Review 后按 expected `.94` 执行。RDT 由其原 owner 独立维护；本次不写 RDT、Planning、产品实现或其他任务状态。现有 GAP 与软件四轴保持。

## 证据

结果只由 docs/requirements-design-test-contributions/599-clear-technical-writing/test.md 拥有；源码、安装投影、实际行为及未验证边界分别记录。
