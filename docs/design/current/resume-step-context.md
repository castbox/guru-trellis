# 正常续接与实际出口查询设计

知识单元：`RDT-DES-RESUME-CONTEXT`。别名：current projection、exit consumer discovery、delivery_current_task、profile_selector。语义 owner：`guru-maintain-requirements-design-test-ssot`。状态：current，表示已整合的规范；实现、安装和最终质量事实由原结果证明。适用前驱为 Git `26630149070e2988ad08102679931468b3535ef8`。完整来源与隔离拟写见[贡献追踪](../../requirements-design-test-contributions/resume-step-context/traceability.md)及该目录 manifest。晋升依据为同 D1 candidate_checked 后、Architecture 实际晋升之后的原 RDT final_integration。

本单元承接[需求 RDT-REQ-RESUME-CONTEXT](../../requirements/current/resume-step-context.md)的 RSC-R1～R5，对应[测试 RDT-TST-RESUME-CONTEXT](../../test/current/resume-step-context.md)的 RSC-T1～T6。既有[生命周期设计](task-delivery-lifecycle.md)保留原 owner、阶段、恢复与单 writer 职责。

## RSC-D1 / RSC-CON-CURRENT：组合查询而不增加身份解析器

原 `guru-ensure-task-checkout` package 拥有 `delivery_current_task` profile 的执行与公开 I/O。输入为明确 profile 和 `mode=workflow|standalone`，不接受猜测身份。先沿上游公开 context resolver/session adapter 判断载体，再调用公共 current；有 Task 时复用原 Ensure 的 C4 branch binding、C5 ownership、唯一注册 checkout 和 live Task 校验。共用逻辑可抽内部函数，原 `delivery_active_task` 合同与 consumer 不变。

完成校验后用字段白名单产生 `current_context_ready`：Task 的 `task_id/task_ref/lifecycle_generation/checkout_path`，以及存在时 `current_delivery.delivery_key/phase/planning_root`。Delivery 必须属于同 Task/generation；没有 Delivery 不补 null 对象或 selection。上游完整 current 只作事实输入，不原样公开其 results/candidate 树。精确公共形状由原 package Interface/schema/example 单写，本文拥有组合职责和行为边界。

## RSC-D2 / RSC-CON-RECOVERY：保留真实首失败

无 context key 在公共 current 读取前返回 `context_unavailable` 及原原因。真实 context 无绑定返回 `no_current_task`。两个出口由原 `guru-current-task-checkout-router` 报告，不替调用者选择 Intake。已知 Task 的 `binding_required/checkout_required/invalid_task_state` 沿原恢复 owner；terminal、stale、关系冲突和读取/API 错误保留原实际诊断，不包装成成功或无对象。

查询不执行 Bind、Selection、branch/checkout 修复或生命周期动作。原 owner 完成合法恢复后重查；不修改 context 环境来绕开缺失，不借另一个 session，不从路径取得身份。客观查询成功仍须由实际阶段 owner 判断当前动作资格。

## RSC-D3 / RSC-CON-EXIT：共享解析与动态 selector

原 `runtime/installed.py` 提供已有 workflow marker 的共用解析结果；`workflow_facts` 继续保留既有全局校验，`runtime/discovery.py` 在原 discovery 内增加可选 exit 查询，原 shell 入口透传。原 Interface 与 workflow marker 共同决定声明及唯一 consumer，不建立独立注册表、resolver、wrapper 或缓存。

查询先按原 discovery 校验 source/installed 合同，再核 Skill 的真实出口声明、唯一 marker 和一致性，然后返回 `skill_id/exit_id/consumer`、该出口 output contract、consumer input/projection 及原入口 locator。Skill consumer 返回原公开入口和输入定位；workflow/stop 返回原 target。定位引用原 Interface 合同，不携带全部合同正文。动态 `profile_selector` 作为未求值的原合同返回，由后续 caller 按实际 payload 选择；查询不执行目标动作。

未知出口、未映射、多重映射或 Interface 不一致返回明确非零诊断。开发测试只在局部 fixture 准备正常声明差错，不损坏生产安装。无 `--exit` 的原发现功能及原 help 保持兼容。

## RSC-D4 / RSC-CON-CONSUMER：唯一 authority 与采用成本

Global workflow 只维护 mandatory 调用顺序、marker 和唯一出口 consumer；step-local package 单写执行合同。原 current checkout router 和相邻调用点只作必要适配。取得 locator 后 caller 完整加载当前适用合同和必要依赖，再进入原 owner；schema、例子、查询摘要不替代语义判断。profile authoring 保留原 help，不增加第二导航。

选用组合投影和共享 parser 的理由是复用现有身份及路由 authority，避免重复解析和完整上游树外传。维护成本是原 Ensure 的新增 profile/独立出口、Interface/schema/examples/help、原 router、discovery 和共用 parser 的成套兼容，以及命中回归和一次受管安装验证。不存在新增持久化状态、迁移或缓存失效成本。上游 public current、marker/Interface、动态 selector 或共享校验职责真实变化时，由原 owner 重评受影响合同；无关 CURRENT 前进不要求重写本方案。

## RSC-D5 / RSC-CON-INTEGRATION：生产、候选与验证分工

canonical 修改由对应实现 owner 负责；installed/dogfood 由原工具 owner 按 matching 维护入口同步，保留 Task/session、并行修改和实际冲突。launcher 原 ignored selection cache 可能刷新，仅单列设施事实。查询本身不修改 Task/Delivery/session/Git/业务状态；不改上游 start/default get_context，也不扩全平台 Release 矩阵。

身份与单 writer 架构由[Architecture ownership](../../architecture/03-domains/ownership.md)的 ARCH-DOM-016/019/038 及原 Architecture owner 定义。原 D1 `architecture-contribution.md` 保留来源；本单元不创建第二 Architecture authority 或 ADR。

完整实现与隔离拟写先交独立 Architecture 和原 candidate Check。实际 `candidate_checked` 后，原 RDT owner 在 final_integration 固定真实目标、重读贡献和命中单元、协调并发有效条件、写入并读回；Architecture 保留自己的同阶段职责。implementation 随后将全部实际 after 差额重绑 candidate/begin_check，进入最终 Check 及后续质量链。RDT `candidate_ready` 只说明完整拟写可供候选检查，不表示实现、Architecture、Check 或共享 authority 已通过；实际知识晋升也不替代最终 Check。
