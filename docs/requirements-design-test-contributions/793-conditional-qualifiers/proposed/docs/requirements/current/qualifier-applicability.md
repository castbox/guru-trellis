# qualifier 适用条件与调用需求

Identity：RDT-REQ-QUALIFIER-APPLICABILITY；aliases：REQ-793、normal/solution/root
conditional qualification。原语义 owner：guru-maintain-requirements-design-test-ssot。
来源 Issue #793；状态 proposed，适用源 Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。
原 final_integration 晋升前，本文件不是 shared current。前驱是该 Git 中的三原包、
workflow/callers 和 #382 已晋升职责；窄替代范围见下文，其他职责保持。

## 完整要求

- REQ-793-01：normal、solution、root 各自在原职责内拥有可单独读取的简洁适用条件。
  原 caller 在全文加载前按 live authority、真实候选和变化判断是否触发；条件与完整
  Skill 合同一致。未触发不加载全文、不装配形式调用或输出空判定。
- REQ-793-02：条件不能用 OS 词匹配代替全部场景、机制、因果职责。真实故障/保护
  不能改名普通 feature。没有新资格 Skill、固定问卷或逐候选证明文件；原阶段保
  自己的完整判断，真实需求/重大取舍回原入口。
- REQ-793-03：触发时显式加载原 stable Skill，给真实非空适用集合并完成原闭环。
  拒绝、机制修订、诊断、范围选择与 blocked 保原意义和唯一 consumer；脚本成功
  不证明 semantic pass。未触发也不制造替代 classified/skipped 输出。
- REQ-793-04：新建/实质改变的诊断、缓解、修复、保护仍进入 root。不变机制采用
  仍适用结论；阶段/caller 变化本身不重判。authority、机制、条件、支持路径或因果
  证据实质改变刷新依赖判断；丢失必要结论回原 producer 恢复/重新判断。
- REQ-793-05：十类 lifecycle 与已有 Author profile 同步 caller、workflow 条件、包、
  上游前置、输入/出口消费、示例和诊断；不只删除 global mandatory。三 owner 保持
  独立，不重构未受影响算法。root 不要求正确未触发的上游制造实际 outcome。
- REQ-793-06：公共语义变化有 matching 迁移，保合法在途恢复；原安装 owner 同步
  canonical、dogfood 和真实受影响声明平台，包括 Claude Code、Codex。Markdown/AI
  判断，脚本仅确定性事实；不增加无 consumer DTO、资格账本或授权持久化。

## 替代、边界与关系

本单元替代前驱 REQ-382-01 和当前调用合同中固定三项顺序的普遍前置；#382 的
目标感知因果方法、原非通过、无状态、各阶段独立和共同完成边界继续由原包/spec
独占。旧完整安装采用前保原合同，成套采用后按同Task/key/实际阶段续接。

不承接 #736 其他拆分、#734、设备/预算/额度治理或事故重放。不要求固定案例数、
成本比例、评测框架、全阶段乘积或完整安装矩阵。设计见
[DES-793](../../design/current/qualifier-applicability.md)，验证见
[TST-793](../../test/current/qualifier-applicability.md)。实现、分发和目标业务效果
不能互相代证，结果以原 Test 及公共 Gate/Git 事实为准。
