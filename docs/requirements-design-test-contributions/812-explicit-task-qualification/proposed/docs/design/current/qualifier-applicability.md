# qualifier 条件调用设计

Identity：RDT-DES-QUALIFIER-APPLICABILITY；aliases：DES-793、conditional qualification。
原语义 owner：guru-maintain-requirements-design-test-ssot。来源 Issue #793；状态 current，
适用源 Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。原 RDT owner 在原
final_integration 从隔离完整拟写晋升并读回本单元。需求为 [REQ-793](../../requirements/current/qualifier-applicability.md)。

## 完整职责与路径

- DES-793-01 承接 REQ-793-01/02：三个原包各自 `references/applicability.md` 是加载前
  条件唯一正文；SKILL/contract/Interface既有入口说明引用该文件。caller 先读短条件，
  只判断是否进入专属owner，不给完整资格verdict。短条件不进入脚本classifier。
- DES-793-02 承接 REQ-793-01..03/05：原十类lifecycle及Author边界各自作触发/采用/
  刷新。满足条件且无适用结论才全文load、原stable Skill、实际适用非空subset和原Gate。
  未触发无输入/输出；原阶段继续完整判断。normal管场景准入；solution管实际业务
  authority承载，普通计算不因影响正确性全部触发；root管真实诊断/缓解/修复/保护。
  精确判据只读三原包短reference和完整合同，不在本单元复制。
- DES-793-03 承接 REQ-793-03/05/06：root使用caller当前场景/authority-placement判断，
  normal/solution真正触发时消费真实outcome；正确未触发时不强求两项结果。公开
  profile/命令/exit/consumer保持；input/schema的#793保持范围由DES-812-04显式窄替代。classified只回原owner继续判断；原
  mechanism/diagnosis/scope/blocked按原唯一consumer承接，不由脚本成功替代语义。
- DES-793-04 承接 REQ-793-04：适用结论保在当前会话或本已需要的原owner gate；不
  新建资格存储。材料变化刷新依赖部分，阶段/caller/无关字节变化不单独重判。
  新正式调用保当前facts校验，不能重放旧envelope；丢失结论回原producer。
- DES-793-05 承接 REQ-793-05/06：完整matching source同步caller/workflow/三原包/spec/
  示例/诊断；MIGRATION-793说明语义切换与同Task/gen/key/root恢复。原tools owner
  保Task/session同步真实受管投影，保用户修改并处理sidecar；没有新旧双reader或
  运行时兼容层。源码修改不代表目标项目已采用。

## 决定、代价与重审

选择在原owner内减去不适用的全文加载和装配，保必要判断。只删global条款会遗留
step-local/root前置；统一wrapper/问卷会复制职责和增加维护。新增三个短reference
有真实caller consumer，保持单一条件源；不新增状态、字段或算法分支。

仅窄替代原固定调用和root两上游结果普遍前置。ADR-008/020的场景/authority/因果
分工仍在；新决定由 Architecture `ADR-CONDITIONAL-QUALIFICATION` 承接。触发规则、
真实消费者或authority改变须回原owner评估，不自动泛化。验证为
[TST-793](../../test/current/qualifier-applicability.md)；源码、native行为、安装和
业务效果分别陈述。

## explicit-task 对象传递（DES-812）

来源 [REQ-812](../../requirements/current/qualifier-applicability.md#explicit-task-完整身份req-812)；
适用前驱 Git f16bb562e4ea844939786cebd5c6c20e686914b2。本节由原 RDT owner 在 #812 final_integration 整合，
独立 committed Review 尚待执行；DES-793-03 的“输入保持”保留其 #793 观察含义，
本次按 MIGRATION-812 窄演进七类输入，其余分工与出口保持。

- DES-812-01（REQ-812-01/02）：author、planning、implementation、base-impact、
  phase2-recovery、branch-review、publication 七类原 caller，从自己实际原身份/
  选择 owner 或 current 取得完整 key，传给三个 qualifier 的 target.delivery_key。
  phase2_candidate_set 只保既有 pinned-old/recovery 边界，不恢复退休 Check 阶段。
  四类非 Delivery profile 保原形状。精确 profile/接口由三个原 package Interface 独占。
- DES-812-02（REQ-812-01/02）：共享 qualification_facts 复用原 active-checkout
  与 DeliveryProjection.current(key)。无 context 经原显式对象校验，不写 session；
  有 context 要求原 current 完整 key 相同。Planning 从真实 planning_root 解析，
  supplied planning_paths 必须等于该目录三文件集合；author 只要求实际已选来源/
  候选文件，不要求尚未写出的设计。原 HEAD、路径、file-set、candidate 校验保留。
- DES-812-03（REQ-812-03）：三个 owner 自己完成语义、recorder/checker/invoke。
  不扩大 output DTO；caller 在内存保留调用对象，以原出口/consumer 返回当前义务。
  同机制既有结论只在仍适用条件下采用，新 invocation 仍校当前 facts。
- DES-812-04（REQ-812-04）：每包七类 current profile 为输入 2.0、aggregate 为3.0，
  Interface/commands/runtime/examples/evals 同步选择新版本。旧公开 schema 与输入
  示例路径/id/bytes 保留，无 current runtime consumer；不提供双 reader 或缺 key
  推断。已结束旧结论保原适用边界，旧未完操作在固定原 provider 恢复，待调用输入
  由原 caller 依据真实当前对象重装。采用和回退完整合同由 MIGRATION-812 独占。
- DES-812-05（REQ-812-04/05）：原 tools owner 冻结完整 canonical 写集并同步本
  checkout 的受管投影，保 Task/gen/key/root/session、peer、common pointer 与用户
  修改；逐项处理 sidecar。RDT/Architecture 原 owner 在工程验证后整合、readback，
  固定提交后的独立完整 Review 才判断 actual after。安装一致不证明实际 caller 行为。

选择显式传参和原 model 校验，复用已有 current(key)。inventory 推断会新增选择；
新 session writer 会复制 authority；跳过 Planning 会删除必要一致性检查；复制
resolver 会增加漂移。因此不采用这些替代。代价是三个包的七类版本与真实 caller
同步维护；无第二存储、fallback 或未来字段。原对象/API/consumer 或实际支持条件
变化时，由原 owner 重审。Architecture 关系为 ARCH-DOM-QUALIFIER-APPLICABILITY /
ADR-EXPLICIT-TASK-QUALIFICATION；验证见 TST-812。
