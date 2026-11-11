# ADR-POSTCOMMIT-INDEPENDENT-REVIEW：本地提交后一次独立完整语义审核

状态：`proposed`。所属Task：`794-postcommit-review` / generation 0；Delivery：`8c5534bb-2d8a-4e3a-be58-4ad853a2e3e0`。拟晋升：`docs/architecture/adr/postcommit-independent-review.md`。本候选尚未成为共享current，不能据此跳过当前安装的任何门禁。

## 问题与适用约束

[Issue #794](https://github.com/castbox/guru-trellis/issues/794)要求实现、自检、必要文档整合和本地提交后一次独立完整审核。固定before `4d565c97b5abf634d76ede2d18eed0a57f13bb76` 的活动链分设candidate Check、知识整合、final Check和committed Branch Review。原知识晋升依赖独立候选Check；原TaskCommit最终profiles依赖Check，early Draft另可提前远端发布。只删除一段workflow会留下消费者循环和不完整恢复。

必须保留上游Task schema2/API1的真实check/full_review/readiness及predecessor、固定B..H、新独立reviewer、Planning Architecture、原知识single-writer、阶段适用authority、工程采用、后继覆盖与终态责任。当前旧协议没有要求check/full_review由不同Skill或两次独立审核完成。

## 决定

1. 由原 `guru-review-branch` 同时拥有公开check/full_review角色。首次审查者新开且未参与实现，冻结已提交B/H，先读before Architecture authority，再读实际after和全部受影响consumers，最后读任务叙述解释归属。在本次先完成一次实现后Architecture before/after判断，再完整承担原Check九维及Branch Review职责。
2. 一次实际语义判断通过后顺序记录真实check和full_review；full_review以前一个check为predecessor。只有两槽均完成才输出passed。它们是上游必需结果投影，不能由脚本、同树、digest、历史pass或空白true代替判断。
3. 原RDT/Architecture maintenance在本地提交前根据Planning、完整实现和真实工程结果整合必要文档，保留完整拟写、expected-current、原writer、readback与普通部分操作恢复。整合事实明确为integrated_pending_review；独立提交后判断成功才形成reviewed_promoted。提交前不另做独立candidate Check/实现后Architecture pass。
4. 原TaskCommit新增版本化pre-review commit/clean reentry，复用exact executor、hooks、路径隔离与同提交恢复；去除Check前置，结果交固定候选审核。当前新链在独立通过前不push、不建PR。原Delivery Review完成并记录readiness，返回ready；Publication只消费其当前ready/readiness并发布。Merge和终态保持。
5. 原Reconcile判断Task/base归属、冲突与集成影响；caller不缩固定区间。原reviewer仍独立时可接续后继，保留可核验覆盖并补审差额/影响；覆盖丢失或影响不明时补足完整审查。工程事实先判适用性，只补真正缺口。
6. MIGRATION-794成套切换公共版本、workflow、packages、runtime、schemas、consumers及平台。完整旧provider处理真实旧阶段和已执行动作恢复；pending远端动作回当前审核/readiness。禁止current fallback、双authority或旧pass改名。已发生PR/HEAD/metadata保持，不重复副作用。

## 窄替代与保持

- 窄替代 ADR-KNOWLEDGE-FINAL-INTEGRATION 的独立candidate Check/提交前独立Architecture晋升前置，以及整合后再次完整Check的顺序。原writer、expected-current、完整targets/readback、before/after、普通恢复及真实审查职责保持。
- 窄替代 ADR-033 的审核前新Draft push/PR资格。旧事务已执行结果的恢复与准确历史保持；Draft不产生最终交付或通过语义。
- 原TaskCommit/Review中Check先验consumer迁入本决定的新版本，不静默改旧profile语义。
- 保持 ADR-028 固定内容、阶段适用authority、真实base阻塞判断；保持 ADR-034 工程采用、后继覆盖与合规独立reviewer复用。Planning candidate/final、Delivery Review、Publication、Completion、Closure、Finish保持各自责任。

## 取舍与代价

选择直接演进原Review及原提交/维护owners。另建质量Skill没有新增独立consumer，却增加owner与迁移表；不采用。修改上游schema/phase扩大支持范围；不采用。保留两套开发Check路径会继续重复并增加语义分叉；不采用。以旧check自动复制full_review会丢失真实完整判断；不采用。

代价是必须同步迁移真实消费者，并在原Review中处理两个公开结果的中间恢复。短期private结果仅服务同owner恢复，消费后删除。不得新增授权字段、审计账本、覆盖DTO、锁、攻击模型或非常规crash协议。普通状态/HEAD不一致仍需按原owner处理。

## 验证与重评

D1设计V1–V7要求真实公开入口顺序、未审远端阻塞、后继/base覆盖、旧事务恢复、pending/真实review状态区别、实际Agent读取及matching安装采用。确定性测试不证明AI已审，源码/安装不证明外部采用。当前只有候选方案，无实现或发布pass。

当上游真实结果协议、当前支持的旧事务、职责边界或accepted scope发生实质变化时，由原owner重评必要投影和迁移出口。不能从未来可能变化推导新接口或第二状态机。正式晋升及共享定义仍由原Architecture owner在合法边界执行。
