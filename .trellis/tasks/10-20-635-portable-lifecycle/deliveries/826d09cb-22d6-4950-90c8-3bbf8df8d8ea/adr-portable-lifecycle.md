# ADR 候选：共享生命周期与本机执行责任分离

Identity：`ADR-PORTABLE-SHARED-LIFECYCLE`。状态：`proposed`，未晋升。属于Task `635-portable-lifecycle` / generation0 / D1 `826d09cb-22d6-4950-90c8-3bbf8df8d8ea`。最终authority由原Architecture promotion写入；本文件不改变当前ADR。

## 背景

现行Reactivate以common-dir seal/manual Cleanup作为共享Finish准入；同一已合并归档在独立clone会失败。原Closure完整动作集只在私有交易，public结果不足以支持Finish逐Issue重核。原Publish恢复又依赖原私有交易及本地branch。原Task/Delivery模型已能携带身份、scope、历史结果和Artifact AuthorityRef，无需新生命周期数据库。

## 决策

共享Task终态由可移植记录、精确Git历史和live GitHub证明；本机session/binding/ownership/事务只拥有当前执行和资源责任。原seal/退出/Cleanup未完成不撤销已成立的shared Finish，确实复用同一未完资源仍保留原冲突。

原Reactivate审schema2终态及明确指定的正式schema1历史资格。schema2沿公共reopen；schema1只用matching Trellis formal operation一次增代，保留原历史与source，不制造旧Completion/Closure/gate。人工历史和未完closeout仍有原分路。

仅为Closure→Finish确实不可重新推导的动作集合补原Closure单写的最小task-local载体，经现有public Closure evidence关联；原Closure/Finish核准确result/key/Completion/source及live required states。载体不授予关闭权限，不断言terminal，不含逐轮审计或授权。当前远端恢复只补已发生子动作，Publish/Review仍亲自判断readiness。

## 窄替代范围

保留ADR-024的公共模型/Trellis writer与Guru语义边界。窄替代ADR-027/ARCH-DOM-032中‘符合指定正式前驱格式仍仅只读诊断/不能Reactivate’的接受限制，允许一次性公共收敛；其余任意旧格式拒绝、独立maintenance和current-only正常执行保持。窄替代shared Finish准入必须有本机seal/manual Cleanup的片段，不取消原资源ledger或Cleanup规则。

ARCH-DOM-054的真实native/下一consumer证明、ARCH-GOV-009的单写/项目检查及#636/#637/#638最终质量链保持。精确public I/O、profile迁移和格式退出见design第5/7节，不引入双主、锁、scheduler或退役映射。

## 比较与理由

搬运原机runtime不能解决原机不可用。为已正式完成旧归档重新做保代Completion/Closure/Finish是可合法形成新结果的组合，但多出旧代收尾、bookkeeping和既有同代ledger/archive冲突；直接公共一次增代更符合真实consumer。仅增加Reactivate fallback遗漏活动/副作用/资源和再次完成。扩Core Closure模型或建全局台账也非必要，原Artifact evidence足以承接Guru独有动作语义。

## 后果、验证与迁移

matching source/capability及完整Guru/官方native安装必须实际核验；同版本或源码合并不证明安装成功。旧完整安装固定原source或经原维护owner成套切换，原Task/D1和真实历史不改。原必要输入仅在A未发布时仍可能无法无损恢复，必须准确报告；该边界不能泛化为索取原机隐藏目录。

V1–V8和最后完整候选/committed Review覆盖本决策after；本文件没有预填其结果。原Architecture final_plan先审真实设计、贡献与本候选；实际shared promotion仍在独立candidate检查后的final_integration发生。
