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
  profile/input/schema/命令/exit/consumer保持。classified只回原owner继续判断；原
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
