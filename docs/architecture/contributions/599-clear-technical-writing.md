# #599 清晰写作与入口读取 Architecture contribution

状态：task-owned contribution；等待当前 Phase 2 和独立 committed Review。不是 shared CURRENT。

TaskId：599-clear-technical-writing，generation0；Delivery 661412bf-0be8-4c0c-9c05-b82f31cb7160。

## 决策与边界

沿用 current .94 的 Markdown 控制面、managed-spec、原 semantic owners 与受管入口装配。唯一正文位于 canonical preset spec，安装副本供 Agent 读取。加载定位接入既有 AGENTS block、workflow 与独立 Skill/平台入口；不创建语言审批阶段、runtime state、公共 DTO、wrapper 或 hook。

新增责任是 Agent 在首次实质文本前完整读取并在输出前按其现有职责自检。原生注入仅在全文完整时消费；其余由 child 自读。缺失暂停受影响正文，恢复后原请求继续。脚本只校验分发、引用和机械事实。

## 引用与并行写入

change_path=target_native。继承 ADR-005、ARCH-FND-001/002、ARCH-DOM-036/041。无新 ADR 或兼容双路径。具体加载设计由当前 Delivery design.md D3–D6 和 canonical 正文拥有；长期规则不复制到本贡献。

本次仅写 task-owned contribution；shared-current promotion 由原 Architecture owner 在独立 committed Review 后按 expected-current 执行。现有 GAP/软件四轴和其他任务状态保留。

## 证据

结果只由 docs/requirements-design-test-contributions/599-clear-technical-writing/test.md 拥有；源码、安装投影、实际行为及未验证边界分别记录。
