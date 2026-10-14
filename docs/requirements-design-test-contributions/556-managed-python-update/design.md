# #556 受管 Python 更新设计增量

继承 Architecture `.89/active`，规划阶段独立判断为 no_architecture_impact；后续阶段仍需各自 fresh gate。现有 bootstrap 拥有解释器、identity/cache/pointer，preset installer 拥有完整 source/staged graph 与激活；不引入新的 owner、长期状态或更新器。

| Design / contract | 所有职责与接口 |
| --- | --- |
| D556-01 / SELECT | apply 启动入口、直接 Python installer 与 bootstrap 一致选择 PATH python3 或显式 --python；受控 managed runner 明确传入自身解释器 |
| D556-02 / IDENTITY | 删除 manifest minor 枚举约束，保持既有 identity 维度和复用判据；admission 与锁定 wheel/capability compatibility 分开 |
| D556-03 / PREACTIVATE | 原 candidate 流程在 target 替换前增加 disposable validation view；自有 pointer/cache locator 指向 candidate，执行真实公开 schema-bound wrapper 的合法能力 fixture 和普通输入错误；检查失败不覆盖旧环境。installer staged graph 另验，成功后才激活目标 pointer |
| D556-04 / DIAGNOSTIC | 以稳定阶段/安全原因和 remediation 报错，不转发可能含凭据的 pip 原始日志；不增加 fallback |
| D556-05 / DISTRIBUTION | installer managed-Python plumbing 小范围模块提取并注册原 inventory；canonical runtime、必要受控 caller、使用文档及完整 matching installed 样本按原机制同步 |

源工程 Task 保持完整 pinned-old dogfood；产品样本使用完整 matching current Task2/Delivery 安装，禁止拼接 DTO/package。source 普通 reapply 的 migration-required 与既有 drift 单列，不计为 current parity 成功。失败只清本次拥有的 candidate/view；旧 cache 不自动清理。测试结果只由 [test.md](./test.md) 拥有。
