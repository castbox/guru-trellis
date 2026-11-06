# 行为测试与因果验证方法的职责设计

Identity：RDT-DES-BEHAVIOR-VALIDATION；别名：D735/CON735。原语义 owner：guru-maintain-requirements-design-test-ssot。来源：Issue #735；状态 proposed，适用源 main@b78edbbdc32e77392bc3775366473971050ccb4b，候选 Check 后原 final integration 晋升。

## D735-01 / CON735-METHOD

承接R735-01/03。quality-guidelines Test And Validation Value 单写通用验证方法，Author planning-body 和 design/implement 原验证章节加载并应用；Phase2 派工、Check/Branch 原职责引用同一正文，避免复制第二套标准。确定性 runner 只运输事实和采集输入/工具/输出，AI 判断行为与证据边界。

## D735-02 / CON735-ADMISSION

承接R735-02。guru-qualify-root-cause 在原修复候选条款区分证据充分性与实验形式，并保留普通功能、诊断、缓解、修复、保护的原分类。没有新状态/字段；原阶段 owner 依据实际结果判断完成。共用 causal-completion-semantics 的证据维度不复制到本单元。

## D735-03 / CON735-ADOPTION

承接R735-03。沿现有 package/spec/preset 和 tools maintenance 分发完整 canonical/dogfood/installed 与实际声明平台。工具维护保留 Task/session；不手工覆盖受管副本。真实语义观察与结构、分发和正式交付证据分别报告。单一方法增量的维护成本为原正文/引用和定向评估，不引入固定重跑、时间限额、理由文件或兼容双读。来源行为、证据需要或原owner变更时重新判断影响。

## 关系

需求：docs/requirements/current/behavior-validation-method.md R735-01..03；测试：docs/test/current/behavior-validation-method.md T735-01..07。Architecture 当前 no impact 使用原独立结果，不制造贡献/ADR。quality/root/Author canonical 精确合同保持唯一来源。
