# #813 D1 固定对象创建与显式迁移需求

## 1. 整体来源与术语

整体权威为 `../../prd.md` 的 accepted_scope，修订 `sha256:ca664fbf14185d2508033277c7df9897efa44954528f30861cb58ba9b31089ca`。本批 scope_ref 选定 R1—R6、AC1—AC5；DeliveryKey 为 Task `813-fixed-git-baseline`、generation 0、Delivery `f65560ac-65fa-48b8-aae3-98f8ceaf8678`。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/813 | 全文，要求 | 固定对象创建、正常 mismatch、恢复、迁移和分发 |
| 整体 Task PRD | 第4—7节，已接受要求 | 场景、行为和可观察验收 |
| `.trellis/spec/workflow/skill-package-contract.md` | Public Skill I/O And Private State 第1—6节、Fixed Git Source Compatibility | 新版闭合输入、最小薄 projection、旧 schema 保留与显式迁移约束 |
| `.trellis/spec/workflow/subtraction-first-compatibility.md` | Default Mechanism、Compatibility Exception | 受控调用方直接演进，不自行增加长期双解析 |

固定对象、同步来源、Delivery target 的定义沿整体第1节。本批不把本地分支移动作为固定对象创建前置。

## 2. 整体与本批目标、非目标

本批交付固定对象与同步来源的明确创建合同、原 owner 的确定性校验和恢复、受控调用方迁移及行为验证，完整承担整体 R1—R6。原问题是固定 read 来源进入 Creation 后又依赖本地同名 branch；修复后同一正常调用链须在 primary main 落后且有无关 dirty 时完成精确创建。

保留整体第3节的所有非目标。本批不执行 #812/#811/#814/#815/#808，不增加攻击/压力/锁/crash/并发加固，不执行完整 Release 安装矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，没有前序 Delivery。开发起点 B 与规划观察 H0 均为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`，PR 目标为 `castbox/guru-trellis/main`。原 Task 已创建、整体 scope 已接受；当前尚无实现或测试通过结论。

依赖原 Sync→Discovery→Clarify→Wording→Readiness 输出、原 Creation/acquisition/control/session owners，以及匹配完整 installer/tools owner。D1 交付不承担新的 Task 身份或第二状态源。合并后仍需整体 AC6 的 live main 可达、Completion、Closure 和必要 Finish；D1 合并不是整体完成。

## 4. 本批调用方、场景与流程

- **D1-S1**：Sync read 调用方固定可用对象，primary main 较旧且有无关 staged/unstaged 工作；完整 Intake 后调用 Creation，按同一对象采用或创建独立 checkout。观察一个 Task 与正确 binding/generation，primary refs/index/workfiles 不变。
- **D1-S2**：原创建已成功但输出丢失；原恢复 owner 回读同一 source、Task、binding 和 acquisition，返回同一结果，不再创建资源，不覆盖冲突 session。
- **D1-S3**：正常装配选错对象、对象缺失或 acquisition/repository 身份不符；原入口拒绝并指出具体字段和原 owner 修正路径，无错误创建。
- **D1-S4**：原同步型来源以当前明确输入进入 Creation；继续校验本地同步基线与审核对象的原关系。旧输入由显式迁移合同处理，不能靠猜测来源改义。

## 5. 完整行为、条件与约束

1. 创建合同分别表达审核来源与目标分支；git_object 只验证固定 commit 可用且为 commit、acquisition 起点匹配及原身份关系，不要求本地同名 branch 相等或 primary 干净。（R1、R2）
2. 同步来源保留原本地基线相等与 acquisition 检查。真实对象、common-dir、Task/generation、branch binding、source 和注册位置不一致继续拒绝；不弱化 primary 禁止采用及已有 dirty/ownership 规则。（R2、R3）
3. 原恢复读取已经建立的结果，不执行创建唯一性扫描或重复副作用；保留 session conflict、缺 context key 与原失败恢复。（R4）
4. 受控输入、schema aggregate、Interface、公开示例、调用说明及测试成套迁移；新版本和旧版本字段形状不能互换。旧已发布 schema/path/id/bytes 保留为历史验证资产；旧成功操作由匹配完整旧 provider 恢复，未执行旧输入重新经过当前原 owner 明确来源。不新增长期 fallback/双读或新持久状态。（R5）
5. 必要变更只在 canonical 源实施；原 tools owner 同步受管 dogfood/声明平台并核 Task/session、用户配置保持、drift 和 sidecar。Markdown 拥有来源与路由判断，脚本校验客观对象和关系。（R6）

Issue 的原技术约束须在本批 design 第3节逐项处置；本需求正文不批准未来方案。

## 6. 本批验收、验证方式与未决项

本批 AC1—AC5 沿整体第7节的独立预期，并采用以下必要观察：

| 验收 | 入口与样本 | 独立预期 |
| --- | --- | --- |
| AC1 | 临时真实 Git 仓库完整 Sync read→Intake→Creation；旧 main 和 primary dirty | 精确对象 Task、branch/checkout/generation；primary refs/index/workfiles 前后不变 |
| AC2 | 同一样本丢失创建输出后调用原 recover | 身份与资源数量不变、返回原结果，无重复创建 |
| AC3 | 正常错误对象/acquisition 输入与真实仓库 mismatch | 正确字段诊断与恢复，错误请求无创建；不手改内部 artifact/hash/state |
| AC4 | 当前同步来源、旧 schema 验证与新旧输入交叉替代 | 当前同步原义保持；旧资产可验证、错误代入拒绝并有迁移路径 |
| AC5 | 原安装 owner 更新实际目标，定向 source/installed/platform/drift/reapply/sidecar | 受管投影一致、原 Task/session/用户内容保持；报告实际层次与未验证矩阵边界 |

当前没有必要用户选择。具体候选机制先交 qualifier 与独立 Architecture；实现、安装和验收尚未执行，不预写通过。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/runtime-location.md` 的 R718-07—11：本批补齐固定来源到实际 Creation 终点及明确旧输入迁移。
- `docs/design/current/runtime-location.md` 的 D718-04/05/07：保留 Sync read/sync 差异、逐 consumer 薄 projection 与受管同步，补本次 Creation 输入和校验差额。
- `docs/test/current/runtime-location.md` 的 T718-04/05/07/08：补真实 Creation 和结果恢复终点，原历史观察不重写为本批通过。
- `docs/architecture/03-domains/ownership.md` 的 Task creation/acquisition 与 runtime-source 责任，及 `docs/architecture/03-domains/workflow-context.md`：本批不换 owner，独立 Architecture 决定必要当前定义差额和候选贡献。

RDT 与 Architecture 的共享正文只能由原维护 owner 在合法 integration 边界收敛；Planning 不提前写共享 current/index/manifest。
