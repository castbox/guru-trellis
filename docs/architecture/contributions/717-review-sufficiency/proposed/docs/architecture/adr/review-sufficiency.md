# ADR-REVIEW-SUFFICIENCY：共同审核规则的唯一 owner 与读取方向

状态：accepted。来源：[Issue #717](https://github.com/castbox/guru-trellis/issues/717)。

## 背景与决定

原共享 review-method 从 Check/Branch 私有阶段合同组合方法，这两个阶段又加载共享方法。已有候选承接、专业、测试及知识规则各有职责，不能把阶段差异一律看作冲突。本项把共同充分性行为收敛到独立 managed spec，删除旧共同定义并改引用；原专题保持唯一 owner，原阶段保留 formal contract。

共同 spec 由完整 Guru provider 分发，原审核 owner 读取并作判断。共享 review-method 保留工程方法组合与 provider/target 边界，退出对 Check/Branch 内部方法的依赖。共同规范不读取任何阶段 private artifact、recorder 或 exit，不拥有修复、验收或 Delivery 调度。

## 替代、代价与适用性

保留现有互读会使共同规则继续与阶段实现耦合；增加“优先级文档”而保留原正文会形成双权威；新 wrapper Skill、gate 或长期覆盖台账会增加没有当前必要性的路由和状态。采用既有 managed spec/package 分发只增加一个共同正文的读取责任，并通过删除重复规则抵消长期维护负担。收益须由真实 old/new Agent 案例说明，文件减少或绿测不能证明改善。

现有公共 I/O、schema、出口与阶段 pass/block 条件不变。外部专业 Skill 仍独立维护，Guru 只在自身职责中读取完整 provider 与专业证据，不批量修改外部仓库。合法 in-flight task 继续使用其原适用版本；新变更不向旧 current 双写。

## 替代范围与重新审查

仅替代共同规则在旧共享方法/阶段合同中被重复维护或反向读取的关系，不替代 ARCH-FND-002、ARCH-GOV-012、ADR-034 的首次独立、工程事实、当前正式结果与最终质量边界。具体迁移集合保留在该 Task 的规划与验证，不增长期清单。若共同源开始决定阶段 route/pass、要求 target 安装、持有私有状态或复制专业正文，回原 Architecture/Author 重新评估。
