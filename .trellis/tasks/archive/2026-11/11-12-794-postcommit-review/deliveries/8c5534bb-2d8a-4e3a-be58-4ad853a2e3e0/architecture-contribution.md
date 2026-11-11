# #794 提交后一次独立完整审核：Architecture 候选贡献

Identity：`architecture-contribution-794-postcommit-review-v1`。状态：`proposed`，未晋升、未实现。所属 Task 为 `794-postcommit-review` / generation 0，Delivery 为 `8c5534bb-2d8a-4e3a-be58-4ad853a2e3e0`。本文件是本 Task 的隔离候选，不能代替共享 current。Planning final_plan 审核此真实内容；实现时原 Architecture owner 再按实际候选更新及晋升。

## 1. 来源、before 与目标

Direct Source 为 [Issue #794](https://github.com/castbox/guru-trellis/issues/794)的全部行为要求和边界。固定 before 为 Git `4d565c97b5abf634d76ede2d18eed0a57f13bb76`。baseline identity 为 `guru-trellis-architecture`；constitution 为 `guru-trellis-design-constitution-v1`；change contract 为 `guru-trellis-architecture-change-contract-v1`，required concerns 为 `guru-trellis-architecture-change-concerns-v1`。精确 authority 由上述 Git 与实际 repository-relative locator 共同定位，不创建全局知识版本。

before 具有 Check→final integration→final Check→TaskCommit→committed Branch Review 链及 early Draft 旁路。目标将实现后的完整独立语义判断集中在原 `guru-review-branch`，由新独立 reviewer 在本地提交后执行。原知识 owners 在提交前按 Planning 与工程事实完成必要整合，明确等待独立审核。Planning 的独立 candidate/final 判断、原 Delivery Review/Publication 和终态责任保持。

选择唯一 `target_native`，直接演进原 owners 与现有公开 API。必要决定由同目录 `adr-postcommit-independent-review.md` 拥有，拟晋升 locator 为 `docs/architecture/adr/postcommit-independent-review.md`。该 ADR 窄替代 ADR-KNOWLEDGE-FINAL-INTEGRATION 的独立 candidate Check/提交前独立 Architecture 前置，以及 ADR-033 的审核前远端 Draft 路径；保留 ADR-028 的固定内容与阶段适用性、ADR-034 的工程采用与后继覆盖。

## 2. Owner、结果与实际消费

| 对象 | 当前责任与拟调整 |
| --- | --- |
| workflow/routing | 拥有 mandatory 顺序与唯一出口消费者。新链不调用独立开发 Check；公开角色 check/full_review 都声明原 guru-review-branch。全局不复制审核内部方法 |
| 原 Review | 一次真实完成九维、全部 Branch Review、Architecture before/after、范围/消费者/维护/兼容及有效验证判断；脚本只在该判断发生后顺序记录两槽 |
| 原 TaskCommit | 精确本地提交和干净重入；新pre-review profiles不要求Check，输出只交固定候选审核。原hook、路径隔离、commit事实与同提交恢复保持 |
| 原 implementation/Reconcile | 原公开constructor/begin_check固定B/H；Reconcile判断Task/base归属、完整范围和冲突/集成影响。caller不能缩区间，脚本不能判断语义归属 |
| 原 RDT/Architecture maintenance | 各自单写完整targets、expected-current与readback；提交前完成整合事实，不把它当独立通过。Architecture新区分integrated_pending_review与真正reviewed_promoted，后者只由实际提交后独立判断成立 |
| 原 Delivery Review/Publication | Delivery Review消费真实完整full_review，完成并记录readiness后返回ready；Publication只消费其当前ready/readiness并发布。实际PR/剩余责任/未验证范围判断保持，只有当前通过候选才可新push/PR |
| 原安装/升级 owner | matching成套切换canonical、runtime、interfaces、workflow与平台，保持Task/session/sidecar；不手工覆盖运行副本 |

上游 schema2/API1 固定槽及 predecessor 保留。Check充分性和full_review完整覆盖分别由同一reviewer真实说明；第二结果绑定第一结果，两个投影完成才输出passed。没有空白pass、通用覆盖DTO、授权状态、第二phase/authority或永久ledger。中断只留原owner有直接恢复consumer的最小短期状态，消费后删除。

提交前整合的内容属于本地待审工作。独立审核以固定B authority为约束，审H中的完整真实after。新CURRENT不能用自身证明符合原约束。发现缺陷时冻结候选不改，由原owner修复并形成后继H；适用原覆盖可以保留，真实差额和影响必须补审，无法界定时补足完整评估。

## 3. 真实目标与共享写入边界

实施时准备下列命中完整单元的完整拟写及真实必要引用，再由原Architecture owner合法整合；本轮不写这些shared targets：

- `docs/architecture/06-governance/change-contract.md`：替换旧重复门禁、早期Draft与晋升前置的活动定义，保留原九concerns、descriptor/check/result identities和Planning目的。
- `docs/architecture/06-governance/rules.md`：仅整合实际命中的晋升/审核前置规则及其来源关系。
- `docs/architecture/01-current/system.md` 内已有TaskCommit、最终整合、early Draft、candidate coverage单元，以及 `docs/architecture/03-domains/ownership.md` 内已有Phase2/Review责任：修改实际旧定义，不追加第二并行路径，也不逐Issue登记无关条目。
- `docs/architecture/README.md` 的维护顺序段：该段自身仍写独立candidate Check前置，确实受本次影响，因此只改该维护合同，不追加知识目录或版本表行。
- `docs/architecture/adr/postcommit-independent-review.md`：晋升本次必要ADR；原ADR正文保留其原观察并在实际引用处明确被窄替代范围，不向共享ADR index逐项登记。

`docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 与 `current/knowledge-maintenance.md` 的需求/设计/测试正文仍由原RDT writer拥有。对应R531/530/600/636/637/638/713的有效条件要语义整合，只有本Issue授权替代的前置/路径退出；历史证据保持。canonical spec/workflow/skills由各原owner维护并经原安装owner采用；Architecture贡献不复制其完整执行合同。

不存在独立主题导航登记、全局版本递增、其他Task重规划或共享journal清理。若共享current在实际晋升前推进，原owner判断真实影响并整合或停冲突；路径不同/文本能合并不能豁免同能力关系判断。

## 4. 九 concerns 的本批承接

| 原 concern | 适用性、理由与落点 |
| --- | --- |
| authority-binding | applicable；Issue794、固定before、Planning3.0及现行项目authority明确；实际调用绑定阶段适用版本，候选不是pass |
| constitution-binding | applicable；五原则全部在原独立判断范围：官方扩展、完整概念、原owner隔离、最小真实结果与旧重复路径退出；不复制原则正文或设评分 |
| boundary-and-decision | applicable；真实改变审核/提交/晋升/发布前置。唯一target_native与必要ADR窄替代旧时机；上游Task协议不改 |
| owner-and-single-writer | applicable；原Review负责一次独立判断，原维护方各自单写，TaskCommit执行提交，workflow只编排；没有新审批链 |
| compatibility-and-exit | applicable；MIGRATION-794逐状态处置旧Check/Review/early Draft。旧完整provider只恢复真实已执行结果，新远端动作回当前审核/readiness；无正常runtime fallback |
| gap-and-deviation | applicable；关闭重复门禁的目标不等于已实现。无新GAP、遗留双写或非功能加固；若实际出现偏移回原Architecture |
| parallel-scope | applicable；只准备本Task隔离贡献。禁止覆盖其他Task/session、shared journal及primary的#796工作；shared targets按原owner在合法时点写入 |
| evidence-and-freshness | applicable；Planning绑定真实design，实施/committed评估绑定实际B/H/完整after；工程、AI行为、安装与外部证据分开，不由hash或文件存在推定通过 |
| review-and-promotion | applicable；Planning独立评估保持。新链提交前整合只pending；提交后同一新reviewer完成一次独立Architecture及全语义审核，真实双投影后才交readiness；本Task自举由matching迁移合同处理 |

Project-check 继续使用 `guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1`、result2.0，原项目AI owner在现有before/after/evidence中判断。这里只写候选责任，不预填project-check或实现测试通过。

## 5. 迁移、代价与删除条件

原Check当前开发profiles、candidate_checked/final/postcommit回程、早期Draft新发布边在matching切换后退出。旧schema仅保留pinned验证资产；当前normal graph不读旧checkpoint、不机械改owner/版本合成通过。已完成commit/push/PR/metadata事实按原owner恢复；尚未发生的远端动作先新审核/readiness。Phase2 rollback输出丢失时恢复原cause及已清结果，不再rework。

维护代价是成套迁移真实consumers和两个必需公共结果，及维护原事务的有限在途处置。减少一次完整独立判断不承诺成本/耗时降幅。若今后上游取消双槽、旧支持事务实际退出或原职责变化，由原owner基于新的明确需求重评并删除失去consumer的投影/恢复分支；不为未知变化加配置或通用adapter。

V1–V7由D1 design/implement定义，实际工程、Agent与安装观察将由唯一RDT Test贡献记录。本轮没有实现、安装采用、远端交付或Release证据；本贡献不声明上述结果。Planning final_plan之后仍需原Approval及独立Activation边界。
