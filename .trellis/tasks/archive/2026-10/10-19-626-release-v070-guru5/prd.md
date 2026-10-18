# #626 v0.7.0-guru.5 发布准备整体需求

## 1. 来源与术语

| 标识 | Locator / 章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| SRC-626 | https://github.com/castbox/guru-trellis/issues/626 / 准备与发布行为、版本与来源 | 要求 | 只承接 Stage1 准备范围；source disposition 为 reference_only |
| SRC-RELEASE | .agents/skills/release-guru-trellis-version/references/contract.md / Two-Stage Lifecycle | 约定设计 | 准备、审查、晋升、Refs-only 交付与 Finish 顺序 |
| SRC-VERSION | 用户本轮“内部版本也应该为 0.7.0-guru.###” | 要求，已整理到 Issue 正文 | 内部 current 版本前缀与后继关系 |
| RDT-BASE | docs/requirements/README.md、docs/design/README.md、docs/test/README.md | 当前知识 authority | 当前 RDT 为 current-main-0.6.17-guru.110 |
| ARCH-BASE | docs/architecture/README.md / FOUNDATION、治理与分发 | 当前架构 authority | 当前 Architecture 为 current-main-0.6.17-guru.101 |

repository tag、extension revision、Fork CLI/source、内部 RDT/Architecture identity 为独立版本轴。准备 Task 完成不代表 Stage2 release 完成。

## 2. 背景与问题

最新已发布 tag 为 v0.7.0-guru.4。main 已合并 #153、#154、#239 和 #331，但 manifest 和维护入口仍固定 extension .4，公开文档仍把 .3 标为稳定、.4 标为未发布。内部 current RDT/Architecture identity 保持旧 0.6.17 前缀。需要准备一致的 .5 软件来源及 0.7.0 内部知识后继，再交独立 exact-candidate 发布阶段。

## 3. 目标与非目标

本 Task 整体目标是完成 .5 发布准备、定向验证、Refs-only Delivery、正常 Completion 和终态 Finish 归档。承担版本与维护目标、公开文档、必要断言/投影和知识 authority 后继。Stage2 exact-candidate、tag、tag-pinned smoke、GitHub Release 与 #626 closure 不属于本 Task accepted scope，仍由 release Issue 负责。不得实现 #363/#152，不修改 Fork/global npm/node_modules，不部署真实业务，不改历史版本/归档，不清理无关资源。

## 4. 真实调用方、场景与流程

- S1 发布准备调用方：以已发布 .4 和当前 main 为前置，准备 .5 canonical manifest、维护目标和公开文档；安装维护 consumer 读取一致版本，历史来源保持原归属。
- S2 知识读取/维护调用方：读取三层 RDT 与 Architecture current 入口；建立 0.7.0 后继，旧 identity 仍可按历史 Git/版本入口读取原含义。current 入口、版本页与关系一致。
- S3 Delivery/Finish owners：消费完整规划和候选，完成适用晋升前后检查、提交与独立审查，发布 Refs #626 PR 并合并；Completion 只审准备范围，Closure 不变更 #626，然后正常归档。
- S4 Stage2 release caller：在准备和 Finish 合并后获取 fresh main；本 Task 交出一致源码和终态归档，不交出可复用的最终 release pass。

## 5. 行为要求

- R1：repository 目标 v0.7.0-guru.5，extension revision 0.7.0-guru.5；前驱 v0.7.0-guru.4。维护 runtime、const schema、消费者及示例/定向断言同步目标 .5。固定 Fork lock 7bcbeaad31380e7a29c97898cb947c6120a61775、CLI/Core 0.7.0-castbox.4、pnpm@10.32.1 不变。
- R2：根 README、workflow/preset README、public-docs 对已发布 .4 与待发布 .5 分别陈述，不混用历史 .3 来源或旧验证；准备期稳定安装使用真实 .4 tag，.5 试用使用真实远端完整 SHA。
- R3：通过原 Architecture/RDT owners 建立 current-main-0.7.0-guru.102 与 current-main-0.7.0-guru.111；保留 .101/.110 前驱和所有旧正文含义、稳定 ID、current 完整单元及未迁移范围。只改变必要版本关系，不制造功能迁移或已发布声明。
- R4：canonical source 是唯一修改源；通过官方支持的 marketplace/preset/apply 同步 dogfood 与 Shared/Codex/Claude/Cursor，受管权限、ownership、sidecar 和 drift 一致。不能用本机补丁冒充可安装来源。
- R5：准备质量覆盖实际版本修改、maintenance contract、文档、内部版本引用/链接及 source/installed/projection。所有语义 gates 由原 AI owner 审查，脚本只记录或验证。若出现真实缺陷，沿原 owner 修复或返回作用域，不静默跳过 FAIL/SKIP。
- R6：准备 PR 仅 Refs #626；Task 为 reference_only；准备 Closure 不关闭 Issue。正常 Finish bookkeeping 与后续 Stage2 保持独立。不得持久化授权、动态 release 状态、task-local release notes 或 PR/Release body handoff。

## 6. 约束与依赖

完整匹配 Fork 和 Gitleaks 已有可用来源，仍须由实际使用阶段核验。Markdown 管理语义、脚本执行事实。新内部版本由现有知识 owner 晋升，不通过重写旧快照实现。此次不改 public Skill id/exit/schema id/字段语义；目标发行版本 const 随配对 maintenance target 更新。没有业务数据字段或 DB 迁移，没有生产或网络服务部署。适用 release 验证以 #626 和私有合同为准，不扩大为完整累计多平台/native-host 矩阵。

## 7. 可观察验收与验证方式

| AC | 对应要求/场景 | 入口与输入 | 预期结果和边界 |
| --- | --- | --- | --- |
| AC1 | R1/S1 | manifest、source lock、maintenance tests | extension/target .5；Fork commit/CLI 不变，所有目标 const 与消费者一致 |
| AC2 | R2/S1 | 三个 README、public-docs 的全文 review 与版本搜索 | .4 的真实稳定身份和 .5 准备身份清楚；历史不被改写，无未来 tag 假可用声明 |
| AC3 | R3/S2 | 原知识 owners、三层 current 导航/版本页及 Architecture 关系检查 | RDT .7.0-guru.111 / Architecture .7.0-guru.102 current；前驱和旧引用可解析，完整单元保留 |
| AC4 | R4/R5 | source/installed、四平台 parity、ownership、apply/reapply/dogfood drift、定向 tests | 实际修改和声明投影通过；无未解决 .new/.bak/bytecode 或意外 dirty |
| AC5 | R5/R6/S3 | scoped Check、提交与独立完整审查、Delivery/Completion/Closure/Finish | 无开放 P0-P3；准备 PR 与 bookkeeping 正常合并；Task 正常归档；#626 仍 OPEN |
| AC6 | R6/S4 | post-merge source/终态归档读取 | 可冻结新的 exact candidate；不声称本 Task 验证替代最终 release gates |

## 8. 实际未决项

本阶段无必要产品或范围问题。实现设计、晋升检查与验证选择由 Author/Architecture/Check 按当前合同完成；Stage2 由本次原 release caller 在 Task 终态后继续。完整累计矩阵、真实业务和生产保持明确未验证边界。
