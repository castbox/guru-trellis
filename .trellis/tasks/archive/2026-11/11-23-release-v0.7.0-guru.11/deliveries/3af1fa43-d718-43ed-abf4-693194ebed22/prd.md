# D2：准备 checkout 的正式 source_locked 采用

## 1. 整体来源与术语

整体权威为 [Task PRD](../../prd.md)，公共 accepted scope revision 为 `sha256:5add93db60209f876e4e1cfbf2715dec719c5b2f3313da65c7925407c2f71f6d`。本 Delivery 为 `3af1fa43-d718-43ed-abf4-693194ebed22`，选择 R5、R7 与 AC4、AC5。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| [Issue #908](https://github.com/castbox/guru-trellis/issues/908) | 发布范围与发布后收敛，要求 | D2 只完成准备 checkout 的真实采用，不替代 Stage 2 |
| [Task PRD](../../prd.md) | R5、R7、AC4、AC5，要求 | 完整源先交付、后继真实采用、Task 收尾和正式发布边界 |
| `.agents/skills/release-guru-trellis-version/references/contract.md` | Complete Source Before Actual Adoption、Whole Preparation Completion，设计约束 | D1 delivered 后创建 D2；使用真实干净源与 `source_locked` |
| `.agents/skills/guru-upgrade-tools/references/contract.md` | preview、prepare、invoke、保存与恢复，设计约束 | 单目标完整安装、同操作恢复与真实目标验证 |
| [PR #909](https://github.com/castbox/guru-trellis/pull/909) / merge `df638d19d458bbab11642b5626d293df30075ea1` | 已交付事实 | D1 已完成 Review、Publication 和 Merge；准备 checkout 尚未采用 `.11` |

“真实采用”仅指原 `guru-upgrade-tools` 在本 Task checkout 上执行 `dependency_mode=source_locked` 及其验证，不代表主 checkout 更新、正式 tag/Release 或业务项目采用。

## 2. 整体与本批目标、非目标

整体 Task 仍需完成真实采用、whole-Task Completion、reference-only Closure 和 Finish。本批目标是让当前准备 checkout 的 installed extension/source/projections 与已交付 `.11` canonical source 一致，并交付全部实际 installed after。

本批不修改 D1 canonical 业务源，不创建 Task/branch/worktree，不升级 peer 或普通主 checkout，不执行 tag、tag-pinned smoke、GitHub Release、Issue closure、业务部署或 Stage 2。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 已 delivered，Delivery result 为 `delivery:df638d19d458bbab11642b5626d293df30075ea1`，candidate head 为 `13d72b5425070fe841c1046d1e677d8323481eec`。当前准备 checkout 的 installed extension/source 仍为 `.10`，是已批准 staged Policy 明确留给 D2 的未实施工作。

D2 的来源为该 delivered head 的完整 clean canonical tree。Fork source lock 保持 `castbox/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140`，CLI 保持 `0.7.0-castbox.6`。原 tools owner 仍须验证实际来源、构建、API、目标选择、事务和保留边界。

D2 delivered 后，原 Completion 重新判断整体准备；reference-only Closure、Finish/Cleanup 和 Stage 2 各有独立副作用与确认边界。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置和动作 | 可观察结果 |
| --- | --- | --- |
| D2-SC1 | D1 delivered；实施 owner 在原 tools owner preview 中读取完整来源与唯一目标 | 返回 actual target、source/CLI/lock、平台、受管写删集合、保存项与未完成事务 |
| D2-SC2 | preview 事实经审查；原 tools owner prepare 一次并展示精确计划 | frozen plan 包含完整写入/删除、平台、用户配置和来源配对 |
| D2-SC3 | 安装动作经当前对话授权；原 tools invoke 执行 | installed extension/source、workflow、Skills、spec 和平台投影真实更新 |
| D2-SC4 | 安装后；实施 owner 从目标自身入口验证 | resolver、installed/native、provenance、完整受管 bytes/mode、reapply/drift 和 Task/session 保留成立 |

## 5. 完整行为、条件与约束

- **D2-R1 来源**：使用 D1 已 delivered head 的完整 clean source，`dependency_mode=source_locked`；来源 canonical `trellis/**` 无未提交差额，Fork/build/API/lock 和 CLI 精确匹配。
- **D2-R2 写入范围**：只更新本 Task checkout 的 installed extension、workflow、Skills、managed specs 和声明平台投影。平台选择从目标实际状态读取；AGENTS 用户正文、用户配置、Task/archive/workspace/session、peer tools 和 common pointers 按原 owner 规则保留。
- **D2-R3 事务与恢复**：原 tools owner 独占 preview、一次 prepare、invoke、same-operation resume 和必要的兼容回退。不得手工修改 installed manifest、复制 source 或重建 frozen plan。
- **D2-R4 实际验证**：目标自身 installed validator、manifest/source/CLI/source lock、完整受管 bytes/mode、native continuation、ownership、reapply/drift、零未解决 sidecar 和配置保留均须实测。
- **D2-R5 交付边界**：D2 完整 installed after 经 TaskCommit、固定 B..H、独立 Review、Publication 和 Merge 形成 delivered；准备 PR 使用 `Refs #908`，不关闭 Issue。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口与可观察结果 |
| --- | --- | --- |
| D2-AC1 | R1 / SC1-SC2 | 原 tools preview/prepare 绑定 D1 source、Fork/build/API、目标平台和精确写删集合 |
| D2-AC2 | R2/R3 / SC3 | 原 tools invoke 实际返回 `tools_upgraded`，避免普通 apply、手写 manifest或历史 Task 迁移 |
| D2-AC3 | R2/R4 / SC4 | target installed/native/validator、完整资产与 mode、reapply/drift、sidecar 和保留结果通过 |
| D2-AC4 | R5 / SC4 | D2 自身提交、独立完整 Review、D2 PR 与 Merge 完成；不替代整体 Completion 和 Stage 2 |

当前没有阻塞产品选择。实际冲突、未知修改和事务问题由原 tools owner 在 Activation 后 preview 中返回。

## 7. Canonical 引用与本轮差额

RDT 的 `codex-skill-distribution` 与 `native-compatibility` 当前单元继续定义共享发现根、平台选择和证据分层。Architecture 的 `ARCH-INT-009/014/015` 定义来源交付和真实采用分层。D2 只执行既有维护能力，不新增公共行为、schema、owner 或长期知识。实际采用若揭示真实 current 正文差额，回到原 RDT/Architecture owner 与 Author Docs Plan，不能直接改写历史结果。
