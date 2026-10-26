# existing verifier 的 AGENTS custom 调用适配：Delivery 需求

## 1. 整体来源与术语

本批属于 Task `656-release-v070-guru6-preparation` 的 generation 1。整体要求为根 `prd.md`；当前公共 scope_ref 只选择 AC7、AC8，对应 R9、R10 和 S6。这里的 snapshot 是原 preview 返回的 AGENTS.md 字节、SHA-256 和 mode；custom base 是同一字节解码后的已审查 UTF-8 正文。

| 来源 | 章节、角色及用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/656 | 准备与发布行为、范围与完成条件；Direct Source，要求保留稳定 existing 入口及两阶段发布边界 |
| 根 prd.md | R9/R10、AC7/AC8；当前整体 accepted_scope，定义本批输入修复和必要验证 |
| trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md | Forward behavior 第4步、执行与恢复；规范性设计，定义 capability、唯一 custom、原 renderer/public prepare/冻结计划 |
| .agents/skills/release-guru-trellis-version/references/contract.md | Stage1/Stage2、内容有效性、独立动作边界；规范性约束，定义准备与发布职责 |
| trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py | `_upgrade_native_bootstrap_tools`；当前实际 caller |
| trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py | `test_native_bootstrap_tools_freezes_one_original_owner_plan`；现有调用合同测试 |

## 2. 整体与本批目标、非目标

整体目标仍是 reference-only 的 .6 发布准备。本批独立目标是让稳定 existing verifier 正确调用已经支持 AGENTS custom 的 tools owner，并完成原路径验证。原 caller 只选择 optional conflict；AGENTS.md 为 unchanged 时没有对应 decision，原 prepare 因而拒绝。

本批交付 caller 适配和现有测试修订，不改 tools runtime、Fork、公共 I/O/schema、installer 或 workflow 行为。不重新实现 gen0 的版本与文档准备，不迁移历史 archive，不更改旧失败，不执行真实业务安装、生产部署或完整多平台矩阵。最终 candidate、tag、smoke、Release 与 Issue 关闭仍在本 Task 之外。

## 3. 本批起点、前序结果、依赖与剩余责任

gen0 Delivery `5517d58c-9d7e-43d2-9bbc-b3b00a8e19a2` 已通过 [PR #672](https://github.com/castbox/guru-trellis/pull/672) 交付，后续 [PR #673](https://github.com/castbox/guru-trellis/pull/673) 承接原归档。其公共 Delivery/Completion/Closure 保留在当前 Task record；这些历史结果不为本批提供 Check 或 Review。

依赖为 canonical source lock 对应的当前/前驱本地 Trellis 构建、原 tools owner、真实前驱 .5 和新空验证 work root。当前为 Fork `79a97ed60fe19e8f287eaddfa74722b5250ced35` / CLI-Core .5；前驱为 `7bcbeaad31380e7a29c97898cb947c6120a61775` / CLI-Core .4。实际命令执行前各自重读来源。构建使用新版 pnpm 的 current 选择，不锁定执行版本，也不新增 clone。

本批覆盖全部新增实现责任。整体 Completion 仍需判断原要求、当前切片及全部历史结果，再走原 Closure/Finish；本批合并不证明 Task 或 Release 完成。修复与新收尾合并后，Stage2 owner 重新冻结最终候选并取得该候选自己的门禁结果。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置 | 触发、处理及观察 |
| --- | --- | --- |
| D2-S1 unchanged | stable existing → `_upgrade_native_bootstrap_tools`；固定 init fixture 已有 AGENTS.md | preview 返回 unchanged；caller 从该 source 形成唯一 custom，原 compose 消费后 prepare/invoke 各一次 |
| D2-S2 conflict | 同一 caller；AGENTS.md 为 optional conflict，同时存在其它 optional conflict | AGENTS.md 仍只出现一次 custom；其它文件按原 preserve 规则保留，source/base 不被替换 |
| D2-S3 原始端到端入口 | 真实前驱、匹配本地构建、独立新空 work root | 原 `verify-throwaway-install.sh --mode existing --platform codex` 完成 tools maintenance、reapply、退休资产、sidecar 与终态断言；逐层报告原始结果 |

执行顺序为 preview → caller 构造输入 → 原 tools renderer → 一次 public prepare → 原冻结计划 → 原 invoke。没有新增持久化状态或恢复协议。

## 5. 完整行为、条件与约束

- D2-R1 / D2-S1/S2：始终从本次 preview 的 AGENTS.md row 取得 source；唯一 custom decision 保留其全部 snapshot 字段，content 等于同一 bytes 的 UTF-8 base。不能仅在 conflict 时处理 AGENTS.md。
- D2-R2 / D2-S2：从 optional conflict preserve 列表排除 AGENTS.md，其余原规则保留。不增加 duplicate decision、替代流程或缺失 AGENTS fallback；固定 init fixture 的文件已存在。
- D2-R3 / 全场景：capability 核验、Guru block renderer、原 public prepare、冻结计划及执行/恢复继续由原 owner 单写。不改 guard、不静默把 preserve/replace 转换为 custom，不复制 updater，不手改已生成的输入或计划来制造 verifier 通过。
- D2-R4 / D2-S3：验证必须保留原稳定入口和真实来源，准备成功不能代替完整 existing 的终态成功。发现新失败时保留首失败并交原 owner 判因；原 candidate 的失败不回写成通过。
- D2-R5 / 全场景：本批遵守整体 R5–R8 的前后独立 Review、原晋升与生命周期边界。来源设计的唯一处置由本批 design 第3节承接，PRD 不另建处置矩阵。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应要求/场景 | 入口与输入 | 预期观察及边界 |
| --- | --- | --- | --- |
| D2-AC7（整体 AC7） | D2-R1–R3；D2-S1/S2 | 现有 caller 合同测试；真实 source 形状的 unchanged/conflict preview；原 `compose_agents_input` | 恰一 AGENTS custom，snapshot/base 正确，其它 preserve 保留，prepare/invoke 各一次，原 frozen plan 不改 |
| D2-AC8（整体 AC8） | D2-R3/R4；D2-S3 | 原 `test_agents_target.py` 配真实本地 CLI；新空 root 的完整 stable existing | 原 public prepare、renderer 幂等与回滚满足合同；stable existing 完成原 maintenance/reapply/retired-assets/sidecar/终态检查。结果只覆盖该验证层，不证明最终 Release 或真实 Agent 会话 |

本批没有必要未决产品问题。候选 Architecture、方案、执行与质量判断仍由各原 owner 完成；来源、依赖或新失败的真实缺口按原路线处理，不能预填通过。

## 7. Canonical 引用与本轮差额

- Requirement/behavior：`docs/requirements/current/native-compatibility.md` 的 R630-05/06 保留 source/build/target 分层；本批不改变其三系统范围。AGENTS custom 的具体现行行为由 tools contract 第4步拥有。
- Design：`docs/design/current/native-compatibility.md` D630-05/06 保留原来源和 tools/update 入口；本轮差额只在 release verifier caller 的输入构造，原 owners 不变。
- Test：`docs/test/current/native-compatibility.md` T630-06/07 保留真实维护与投影的证据层次；本批新增 caller 合同回归，并定向重跑 existing，不承接累计多平台职责。
- Architecture：`docs/architecture/README.md`、`docs/architecture/00-foundation/design-constitution.md`、`docs/architecture/06-governance/change-contract.md` 由独立 Architecture owner 判断实际候选；规划本身不预判 impact 或晋升结果。
