# D1：固定 Fork 来源并验证 Guru context/tools 采用

## 1. 整体来源与术语

整体 authority 为 `.trellis/tasks/11-13-814-context-validation/prd.md`，revision `sha256:ab389a1a02b14d550f0fcb53f3c66a0a526f455146eb289097bc517cf4dc17a8`。本批公共 key 为 Task `814-context-validation/gen0`、Delivery `fca8647f-14d0-436d-8298-1b561036f8e4`，planning_root 为 `deliveries/fca8647f-14d0-436d-8298-1b561036f8e4`。选定范围是整体 R1–R6、AC1–AC5；整体 R7/AC6 的 Completion/Closure/Finish 责任仍保留在 Task。

| 来源 | 章节、角色及本批用途 |
| --- | --- |
| [Guru #814](https://github.com/castbox/guru-trellis/issues/814) | 完整正文、要求1–4和验收；Direct Source。保留原超时、性能、身份和同事务接续要求。 |
| [Fork PR #68](https://github.com/castbox/Trellis/pull/68) | 改动、验证、安全与部署影响、证据边界；已交付前置和规范性约束，具体处置由本批 design 第3节单写。 |
| [固定 Fork e379](https://github.com/castbox/Trellis/commit/e3793251fad8bd261d0c370d408c7675b9f6a140) | 实际合入身份及 [CI 43341080020](https://github.com/castbox/Trellis/actions/runs/43341080020)；必须采用的 dependency 来源。 |
| `trellis/presets/guru-team/source/trellis-source.json`；同目录 README 的构建、tools-only、官方投影检查章节 | 当前 lock 与原 source/target 采用合同。 |
| `trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md` | forward、formal source pair、未终结操作、目标验证和恢复；原 tools owner 的完整约束。 |

正式 successor 指实际包含新 lock 的完整 Guru commit H；H 在实施后产生，当前不虚构其值。`local_candidate` 是开发证明，必须保留 `formal_fork_source_lock` 未验证边界；正式采用使用 H 和它自身 lock 配对的 `source_locked`。

## 2. 整体与本批目标、非目标

整体目标是解决正常多工作区 context 开销及 tools 等待接续问题。本批独立交付目标是将已合入的 Fork 修复纳入 Guru 正式来源，沿原 owner 同步实际目标，并完成所选技术范围的原生、恢复和保持验证。

本批覆盖来源身份、正常规模性能、当前会话/显式 Task、必要身份拒绝、原10秒 probes、同候选同 ref 恢复、安全诊断以及 canonical/dogfood/installed/声明平台同步。Fork 已交付能力直接采用，不在 Guru 复制身份解析实现。

不实施 #815，不承担 Release 或业务仓采用，不修改其他 Issue，不引入新持久格式或恢复框架。保留整体对攻击、压力、锁、并发/crash 加固的排除。Task 完成、关闭和归档不作为本批合并前已经完成的结果。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 没有前序业务 Delivery。本批 B/H0 均为 `ce4644392d1ed9815d59071388b9bff9978d1cee`；未来 PR 目标为 `castbox/guru-trellis:main`，实际内容 H 在原实施/TaskCommit owner 处固定。当前 lock 为 Fork `aa898d090fc27c9ce6145cfa3c787a6f400da4e2`。

Fork PR #68/#69 是跨仓前置交付，不是本 Task 的已交付 Delivery。其受控169工作区结果可作为因果和复用依据；Guru 目标安装及自身验收尚未执行。目标来源固定为 e379，CLI/Core 保持 `0.7.0-castbox.6`，pnpm 保持 `10.32.1`。

本批依赖精确 Fork 构建、完整原 tools API1.0、原 owner 的真实 preview/prepare，以及实际产生的 Guru H。未终结操作若与拟写集重叠，必须先回原操作处理。H 产生前不能声称正式 source_locked 通过；H 变化后按实际 delta 刷新相关证据。

本批完成后仍由 Task 原 Completion 审核全部 accepted scope，Closure/Finish 处理 Issue 和归档；这些整体责任不另造空 Delivery。未验证完整 Release 矩阵保持独立边界。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置、动作与可观察结果 |
| --- | --- |
| D1-S1 来源配对 | 原 source-lock/tools owner 读取 e379 与完整 Guru candidate，构建匹配 CLI/Core；实际版本、源码标记、lock identity 和正式 H 对应，不能仅比较版本字符串。 |
| D1-S2 多工作区原生校验 | 约169个合法注册工作区与小规模拓扑，经实际 installed native/context 和公开 tools probes；当前会话、显式 Task、唯一 checkout 正确，记录 Git 调用来源和耗时，不跳过 peer 校验。 |
| D1-S3 普通拒绝 | 支持的 stale/conflict/非唯一关系从原入口被拒绝；没有借用其他会话、手工改 artifact 或取消必要校验。 |
| D1-S4 等待与恢复 | 外层等待结束先检查 executor；仍运行时继续原 handle，实际恢复使用原 operation/ref/plan/preimages/candidate。完成后重读目标自身入口，原失败保持。 |
| D1-S5 分发与保持 | 原 tools owner 更新所选 Task checkout 的官方与 Guru 受管投影；实际目标自身 resolver、installed/native、官方 projection 和 drift/sidecar 通过，Task/session/peer/common 保持。 |

本批的工程结果、正式候选结果和实际安装结果分别记录。没有自然复现旧内部超时时，不增加 fault injection，也不将新操作证明写成旧历史事务恢复。

## 5. 完整行为、条件与约束

- D1-R1（整体 R1）：将 canonical lock 的 commit/parents/tree/CI 更新为整体 PRD R1 的 e379 组合，保留 schema、repository、CLI version 和 pnpm；由原 owner 生成 installed lock 与 receipt。
- D1-R2（整体 R2）：采用 Fork 单次解析内事实复用与既有分支拓扑筛选，保留所有 eligible peer 校验、原 prunable 例外、唯一性和选中分支独立查询；Guru 不增加平行 cache/store。
- D1-R3（整体 R3）：真实 contract/context probes 和两个10000ms预算保持。验证必须到达实际目标入口，记录正常大小规模输入、身份结果、调用来源与耗时；没有所有机器的固定延迟保证。
- D1-R4（整体 R4）：等待结束、executor 终态和原操作恢复分别观察。原 ref/candidate/plan/preimages 不替换，cross-candidate mismatch 保留；不 reprepare 掩盖失败。
- D1-R5（整体 R5）：诊断不回显敏感原文或原始 stderr；历史超时和真实首次失败保持，未知原因不编造归因，未验证项明确。
- D1-R6（整体 R6）：完整匹配来源通过原 tools owner 维护；Task/session/历史及并行状态不转换，peer/common pointer 不写。实际冲突和 sidecar 按原 owner 处理，缺依赖停止其真正依赖的工作，不降级 validator。

各来源设计承诺在 design 第3节逐项给出唯一处置。当前不新增公共 Skill id、schema、命令、Task/session/operation 持久字段；若实施发现真实合同变化，先返回原规划/兼容 owner，不能静默增加适配。

## 6. 本批验收、验证方式与未决项

| 本批验收 | 整体对应 | 入口、输入与预期观察 |
| --- | --- | --- |
| D1-AC1 | AC1；D1-S1 | 精确 Fork build 与真实 Guru H，canonical/installed lock、官方身份和依赖一致；H 未产生前仅开发证明。 |
| D1-AC2 | AC2；D1-S2 | 正常169/小规模实际 installed 入口覆盖当前会话和显式 Task，正确 owner/checkout、必要 peer 校验与预算保持，计时/Git来源可核。 |
| D1-AC3 | AC3；D1-S3/S5 | 普通必要身份拒绝仍成立，独立前后比较 Task/session/peer/common 的内容、mode 与实际合法选择。 |
| D1-AC4 | AC4；D1-S4 | 公开 tools 校验和同候选原 ref 接续成功，原 plan/preimages 不变；未知结果读取原操作，历史未自然复现边界保持。 |
| D1-AC5 | AC5；D1-S5 | 实际目标 resolver、installed/native；官方 projection checker 及其测试；声明 Claude/Codex/Cursor 投影、drift、必要 reapply/sidecar。每类结果独立，不以源执行替代目标成功。 |

没有产品需求未决项。正式 H、后续实际 tools 写集与可执行验证参数由 solution planning 明确顺序和获取方式，不预填未来事实。当前只完成 requirements 阶段，不代表实现或安装通过。

## 7. Canonical 引用与本轮差额

| Authority | 适用章节与本轮差额 |
| --- | --- |
| `docs/requirements/current/runtime-location.md` / RDT-REQ-RUNTIME-LOCATION | R718-03/08/10/11、R769 原 source/target/恢复边界继续；本批增加 context 正常规模采用与证据差额，不改身份 owner。 |
| `docs/design/current/runtime-location.md` / RDT-DES-RUNTIME-LOCATION | D718-01/03/06/07、D769；保留实际资产执行、原维护和提交后审核责任，新增来源采用与验证安排。 |
| `docs/test/current/runtime-location.md` / RDT-TST-RUNTIME-LOCATION | T718-05/06/07 与 T769；采用仍适用的身份/保持设施，补 #814 的大小规模及正式来源目标证据，不改写旧观察截止。 |
| `docs/architecture/README.md`；`docs/architecture/01-current/runtime-location.md` | 原 Architecture authority 和工具/位置/来源职责；实际候选影响由独立原 Architecture owner 判断，不在需求正文预判。 |

后续 Docs SSOT Plan 由 implement 第6节单写，Planning 不修改共享 current、README/index/manifest 或预建空贡献。实际变化由原 RDT/Architecture owners 在其合法阶段整合并读回。
