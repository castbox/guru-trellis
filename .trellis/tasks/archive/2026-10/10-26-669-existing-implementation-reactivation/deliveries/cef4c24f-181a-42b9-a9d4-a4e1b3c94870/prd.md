# D1：已有实现分支的归档 Task 恢复

## 1. 整体来源与术语

整体 accepted_scope 指向本 Task 根 `prd.md` 的已接受版本；本 D1 的 scope_ref 覆盖 AC1–AC5。规划目录为 `deliveries/cef4c24f-181a-42b9-a9d4-a4e1b3c94870`。Direct Source 是 https://github.com/castbox/guru-trellis/issues/669 全文，角色为要求。backend #802/#825/#838 仅作真实案例证据，不引入业务实现义务。

base HEAD、实际实现 HEAD、已审核工作区状态分别是三个对象。恢复结果是同一 TaskId 的真实后继 key/ref 及后续 owner；历史结果不作为当前 gate。

## 2. 整体与本批目标、非目标

本批全量承接 R1–R7，补齐原 Reactivate/acquisition 对已有实现分支及原 Draft PR 的合法接入口。当前不足是 decision_head 被绑定到 base，且 checkout 只接收 clean，因此已有提交不能恢复。

本批实现同身份恢复、完整内容保留、同操作接续、明确失配停止，并同步最小公共合同、canonical/dogfood/installed 与架构/RDT正文。不承担业务实验、原业务 PR 发布、云操作、通用迁移框架或完整 Release 安装矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次 Delivery，无前序交付。起点为 `main@83512901506409f59016121aebc2d0b0bbe98059`。根 PRD 已由原 Clarify 通过公共 accept_scope 接受；尚未形成当前实现或任何 Check/Review pass。

依赖原公共 Task2 reopen、同身份后继查询、branch/resource ownership、Establish/Ensure/Bind、完整 matching preset 与 Fixed Fork CLI/Core。D1 完成全部 AC 后交整体 Completion；实际业务后继仍由业务仓库自己的 owners 承担。安装后的受控原生恢复验证不授予业务 #802 写入权限。

## 4. 本批调用方、场景与流程

- D1-S1：原 Reactivate owner 读取合法归档、当前 base、既有实现 HEAD、完整本地改动、原 Draft PR 和资源归属。事实一致时经原 acquisition/public reopen 建立同 TaskId 的下一 generation，返回真实 key/ref，再交缺失的环境或 Task/Delivery owner。
- D1-S2：输出丢失或重试时，原 owner 查找公共后继及原操作，继续实际后继，不另建 incarnation 或 PR。
- D1-S3：所选仓库、前驱、分支、HEAD、PR、ownership 或已审本地内容不符时，报告具体诊断并保留现场。只测试诚实操作中的普通失配，不构造恶意 artifact。
- D1-S4：安装 matching 源码到受控独立 Git 案例，原生 Agent 从公开入口审核并恢复。分别记录安装、恢复和后续门禁状态。

## 5. 完整行为、条件与约束

R1：保留原 TaskId/source/Completion/Closure，只通过原公共 writer 增代；前驱必须已正常归档并合入准确目标。R2：分别绑定真实 base 与实际实现 HEAD，完整审核本地改动、PR repository/base/head 和资源 ownership。R3：恢复不改写实现提交，不丢失 staged/unstaged/untracked，不自动提交或推送工具升级改动，不改变原 Draft PR。

R4：普通输出丢失接续原操作；已有合法后继时复用，冲突后继停止。R5：已审事实发生失配时停止，保留工作区和远端。R6：只建立恢复身份与后续路由，当前业务变更仍进入正式 Delivery 流程。R7：分层验证并通过原长期文档 owners 同步合适完整正文。

Markdown 定义 AI 的语义审核和后续 route；脚本只记录并验证事实。既有 clean-base 恢复入口保持原义；如扩展公共合同，以独立明确 profile/schema 和迁移说明表达。新机制先交独立 Architecture candidate assessment，不能仅通过删除 clean/HEAD 校验实现本需求。

## 6. 本批验收、验证方式与未决项

| AC | 场景 / 要求 | 入口、输入与观察 |
| --- | --- | --- |
| AC1 | D1-S1 / R1/R2/R6 | 原公开 Reactivate：已有实现 HEAD 与 base 不同，合法前驱且无后继；返回 generation+1 与真实 ref/owner |
| AC2 | D1-S1 / R3 | 已审核 staged/unstaged/untracked 与工具升级差额；比较恢复前后内容与提交，原 Draft PR 和远端引用无写入 |
| AC3 | D1-S2 / R4 | 丢失首次输出后同操作重试及已有后继；返回相同后继，不重复增代 |
| AC4 | D1-S3 / R5 | 由正常 Git 操作形成 HEAD/branch/dirty/ownership/PR 失配；具体停止且保留现场 |
| AC5 | D1-S4 / R7 | 源码定向套件、真实 Git 与安装后原生公开入口分别留实际结果及限制 |

需求无阻塞未决项。机制细化由 Author 和 Architecture 承担；缺少实际安装/原生验证时不能声明 AC5 完成。

## 7. Canonical 引用与本轮差额

- `docs/architecture/03-domains/ownership.md`：ARCH-DOM-060 及 shared archive/Reactivate 完整职责；本批扩充原 owner 对既有实现状态的承接，不新增 writer。
- `docs/architecture/06-governance/change-contract.md`：适用 concern、project-check 与独立评估；本批按原 promotion 路径同步真实架构差额。
- `.trellis/delivery-contract.md`：Task reopen 与历史保留；本批复用，不修改上游公共模型。
- `trellis/skills/guru-team/packages/guru-reactivate-task/SKILL.md` 及 `runtime/invoke.py`：当前入口与实现；本批添加必要合法恢复分支。
- `trellis/skills/guru-team/runtime/task_lifecycle/checkout_acquisition.py` 和 `checkout_resolution.py`：原 acquisition、准确 HEAD 与工作区判断；本批仅补本恢复场景需要的确定性事实承接。
- `trellis/skills/guru-team/packages/guru-reactivate-task/tests/test_delivery_reactivate.py`：现有真实 Git/public writer 回归；本批补已有实现、已审核本地差额和原 PR 保留场景。
- `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`：现行 RDT 导航；差额通过原 owner 的 task contribution 和 final integration 收敛，不复制第二套规范。
