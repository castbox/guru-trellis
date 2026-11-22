# #861 gen2 D1：发布门禁消费者完整源修复

## 1. 整体来源与术语

整体 authority 为根 `prd.md` 的 `sha256:0b58a6f33c687290d842d6de14e74ed6b77e52d49106a328c2161080382ec12c`。当前 DeliveryKey 为 Task `744a637b-a044-46cd-8cdd-77ddd85ded8e` / gen2 / `bb916153-bffa-4961-a06f-4a54b9bdef2f`；规划根为本目录。R/AC 指整体 PRD 的稳定编号；本批 B/BC 只展开选定切片。

| 来源 | 角色 | 用途与必要章节 |
| --- | --- | --- |
| 整体 `../../prd.md` | 要求 | R1–R3、R5–R7、R12–R13；AC1/2/4/10/11与SC5 |
| https://github.com/castbox/guru-trellis/issues/861 | 要求 | 执行范围、最新 main 与无其它 Issue 前置、发布写入边界 |
| `.agents/skills/release-guru-trellis-version/references/contract.md` | 约定设计 | Complete Source Before Actual Adoption、Whole Preparation Completion、Stage 2；源与采用分片及后续重新冻结 |
| `trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py:clarification_owner_for_issue` | 当前接口事实 | recorder/checker 均消费 owner envelope，记录结果与来源上下文分开 |
| `trellis/skills/guru-team/packages/guru-discover-change-context/{interface.json,runtime/issue_review.py,schemas/public-issue-context-request-input-2.0.schema.json,schemas/public-issue-readiness-supplement-input-1.0.schema.json}` | 当前规范性接口 | context_request 2.0 的 focus/返回身份与 Discovery supplement 1.0 各自的合法形状；不选择新业务行为 |

## 2. 整体与本批目标、非目标

整体目标是完成 `.10` 的全部发布准备及真实采用，之后由独立 Stage 2 从最新 main 冻结发布候选。本批独立交付完整可分发源：修复 Phase 0 回归测试对 envelope 的过期消费，以及 Discovery 四命令帮助对 context-request schema 的过期声明，补足直接正常回归和源分发验证。

本批覆盖上述选定 R/AC；不执行准备 checkout 的 tools 采用，不创建 D2，不更改版本/Fork lock，不恢复旧生产 envelope 或将历史 schema 重新设为 current，不修改实际业务路由。tag、smoke、Release、主目录最终安装、Issue close 和 cleanup 均不属于本批。

## 3. 本批起点、前序结果、依赖与剩余责任

本批从 `main@5dc0708a1d817fb9fb02edb64419b7b3c3f7cc10` 的 gen2 新 checkout 开始。历史 gen0 PR #865/#866 和 gen1 PR #871/#875 均 delivered，gen1 终态由 PR #876 持久化；四个历史 Delivery 的原结果保持，不是本批质量通过。

前驱 `.9` 到上述候选的完整独立审核确认：`NormalPhase0AuthoringTests` 四例中一例在读取 `review_target` 时 ERROR；四个 Discovery 实际 help 的 context-request 仍指 input 1.0，缺少 focus 的旧形状被 runtime 2.0 拒绝，加入当前字段又被 closed 1.0 拒绝。Discovery 自己的 supplement 1.0 仍合法，保持原声明与无 review_focus 的形状。生产 helper 和 Interface 已是目标合同，本批只修直接消费者。

D1 的源完整性由其自身回归及临时完整安装证明，不依赖未创建的 D2。D1 实际 delivered 后，原 Completion 对未实施的准备 checkout `source_locked` 采用返回 `additional_delivery_required`，原 Creation 才创建 D2。整个 Task 还需 D2、whole Completion、no_mutation Closure 与 Finish；其后 Stage 2 重新冻结。源安装样本不代替实际采用，旧 release gate 结果不转为新 SHA 的通过。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、条件、动作 | 处理与可观察结果 |
| --- | --- | --- |
| BS1 | 原 authoring 回归调用当前 clarification helper，mock 仅隔离外部 recorder/checker | 从真实 helper 发出的 envelope 检查 owner 与 context；派生字段和同一 recorded 绑定断言均可执行 |
| BS2 | 正常调用者读取 record/check/invoke/read-source 四命令的 help，并按当前声明装配两个既有 profile | 公开 schema 与实际 runtime/Interface 一致；context_request 2.0 的 focus/返回身份和 supplement 1.0 的原有形状分别通过原输入验证边界 |
| BS3 | 源分发验证者从本批完整 canonical source 执行临时完整安装及 reapply | Shared/Codex、Claude、Cursor 得到同源合同，完整预期集合、字节/权限、manifest、workflow/lock及 sidecar 一致 |
| BS4 | 本批实际交付后原 Completion 核验剩余责任 | 保留正式采用缺口并路由后继；不把 source-only 结果写成整体完成 |

## 5. 完整行为、条件与约束

- **B1 / R12**：修订既有测试的 owner 取值和 checker envelope 断言。仍执行真实 helper；保留不预填 recorder 派生字段、duplicate 输入事实、checker recorded 对象及匹配来源上下文的检查，不删除断言换取通过。
- **B2 / R13**：四命令各自的 context-request 引用，共四条，改指已有 2.0；四个 supplement 1.0 引用保持。两个 profile 的实际验证保持各自当前语义。历史 schema 文件、固定旧 provider 恢复和其它 schema/output 声明不变。
- **B3 / R2/R5**：现有 package/preset writer 是分发 owner。必要回归观察 help 所公开合同对正常输入装配及实际验证的作用，不只锁定文本常量。D1 用临时目标证明完整源及三种选定平台的分发/reapply；不手抄 dogfood/installed 副本或手改 manifest。
- **B4 / R1/R3/R6/R7**：`.10` 和 CLI `.6` 各保原轴与来源。D1 完成原完整提交/Review/交付链；准备 checkout 实际采用独立留给后继。只使用 `Refs #861`，不把其它 Issue 状态设为前置。

来源设计的具体 retain/change 及设计落点由后续 design 第3节单写。当前需求没有新的产品选择；技术细化由原 Author/Architecture 承接。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应行为 | 入口、输入与预期观察 | 边界 |
| --- | --- | --- | --- |
| BC1 | B1/BS1 | 原四例 NormalPhase0AuthoringTests 调用当前 helper，原派生字段断言、上下文及 recorded owner 绑定完整执行，无该 KeyError | 单元层不证明真实 GitHub或Agent调用 |
| BC2 | B2/BS2 | 四个实际 help 的 current 声明与 runtime/Interface一致；context_request 2.0 的两种正常 focus 输入经原验证路径成功并保留返回身份；Discovery supplement 1.0 原有形状通过声明 schema 与原输入验证边界，不附加 Clarify 的 focus 字段 | 不新增 profile 或改变业务路由 |
| BC3 | B2/B3/BS3 | source package及受影响 Discovery 回归通过；一次完整三平台临时安装/reapply与完整投影核验无旧 current 声明、私有测试泄漏或 sidecar | 临时安装不证明目标实际采用或真实客户端 |
| BC4 | B4/BS4 | 原 D1 完整交付事实及 Policy 明确源已交付、采用仍未实施，Completion依实际缺口分配后继 | D2、整体收尾及Release均未完成 |

必要验证集限定这两项缺陷和直接消费者，不清零历史 suite，不执行累计完整矩阵；环境或行为失败保留原始事实并回原 owner。当前无阻塞需求的未决产品问题，Architecture候选评估及最终规划审核尚未发生。

## 7. Canonical 引用与本轮差额

- requirement/behavior：`docs/requirements/current/issue-content.md` 的 R850-01/04、R868-03；`docs/requirements/current/behavior-validation-method.md` 的 R735-01..03/R868-04。保留现有输入、分发及最小充分验证责任，只修过期消费者。
- design：`docs/design/current/issue-content.md` 的 D850-01/04，`docs/design/current/behavior-validation-method.md` 的 D735-01..03/D868-03。复用 envelope、现有 schema、原安装 writer，不新增 writer或状态。
- test：对应两个 `docs/test/current/` 单元的 T850-04、T735与T868；当前差额是实际 helper/envelope断言与命令公开输入消费回归，不改历史观察。
- Architecture：`docs/architecture/README.md`、`docs/architecture/00-foundation/design-constitution.md`、`docs/architecture/06-governance/change-contract.md`。本批候选须由原独立 owner 作当前判断，不继承 gen1/no-impact。
- 共同验证方法：`.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value`。不增加新的证据表、gate、release ledger 或空 contribution；是否命中共享文档差额由后续完整设计与原维护 owner 判断。
