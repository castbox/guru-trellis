# #712 精简 legacy 正式归档恢复整体需求

## 1. 来源与术语

| 来源 | 定位 | 角色及用途 |
| --- | --- | --- |
| Direct Source | https://github.com/castbox/guru-trellis/issues/712 全文，2026-11-05 | 整体要求、正常路径、两仓责任、验收和非目标 |
| 公共前置 | https://github.com/castbox/Trellis/issues/64 及 https://github.com/castbox/Trellis/pull/65 | 已交付公共家族解释及转换；固定候选按 source/build/API 核验 |
| 历史案例 | #712 来源表中的 guru_ai_roleplay Task 130、PR #220 与精确 Git archive | 历史事实及代表性样本条件，不授权真实业务恢复 |
| 当前合同 | docs/requirements/current/completion-closure.md、docs/design/current/completion-closure.md、docs/test/current/completion-closure.md | 原正式恢复及人工历史恢复边界 |

“精简 legacy”指公共 owner 明确支持的 known_legacy 家族；不是任意缺字段记录。正式恢复增代一次；人工 archive_resume 保留 generation。二者保持区别。

## 2. 背景与问题

当前 Guru shared_finish 在公共检查前要求原档显式 generation，并排除 creator/assignee。真实历史样本保留十个旧字段，没有 schema_version、generation 或 structured source，因此被拒绝。既有 schema1 测试不能覆盖此形状。公共前驱支持已由 Trellis #64 提供，Guru 仍须完成历史资格判断、接线和 native 续接。

## 3. 目标与非目标

让经过 AI 历史资格审核的精简正式归档，通过原 Reactivate owner 消费公共解释，以同一 TaskId 增代一次并续接。整体完成包含公共转换、Guru 控制绑定、目标自身 native 会话和下一 scope owner 消费，以及再次归档后的受影响前驱读取。

不复制公共 parser 或 generation 算法；不修改原档，不批量迁移，不恢复人员体系，不实施 Opening V4，不把旧基础阶段扩大为完整来源 Issue 已完成。不隐含操作真实业务仓库。只处理诚实正常路径、普通遗漏和状态变化；不引入攻击、锁、竞态压力或 crash 加固。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与条件 | 动作及可观察结果 |
| --- | --- | --- |
| S1 | Reactivate，具有完整正式历史的原样精简档 | 审核历史资格及当前请求，调用公共正式恢复；得到同 TaskId 的下一 generation，原档字节不变 |
| S2 | 公共 applied 后本地绑定未完成，或 operation pending | 续接原 operation，完成真实 key/ref 的获取与绑定，不重复 prepare、资源或增代 |
| S3 | 私有结果丢失，真实后继存在 | 核验后继关系及阶段；继续后继实际 owner，后继已归档时不误判保留前驱为重复身份 |
| S4 | source、历史资格、PR/Git 或后继关系不一致 | 报具体缺口并回原 owner；保护原档和其他任务，不补造 source 或 gate pass |
| S5 | 既有 schema1/schema2、人工历史或未完 closeout | 保留原路由与语义，不因格式支持改变终态资格 |

## 5. 行为要求

- R1：AI 实际读取精确归档、原安装/Finish 合同、source、规划、summary、真实 PR/Git，区分正式历史、人工历史与未完成事务。单个 status、MERGED PR 或私有 receipt 不决定资格。同一 PR 可包含交付与归档，不要求独立 bookkeeping PR。
- R2：只消费公共声明支持的 family、前驱 key 和 source 关系。Guru 不给所有缺 generation 记录补 0，不自建格式分类器。人员字段仅为历史资料。普通 current Task reader 保持严格。
- R3：共享归档准入、实际后继发现及保留前驱消歧使用一致公共解释。旧规范 scope 的来源语义由原 source owner 核验，不回写历史。
- R4：保留 TaskId、历史 scope、原归档字节及可核验交付。旧 Planning/Check/Review/Finish 不充当当前 gate pass。恢复后范围交原 scope owner，不增加来源关闭权限。
- R5：只有公共 applied 后才绑定真实 key/ref 并 native 续接。pending、绑定中断和私有回执丢失均按 S2/S3 恢复；不重复创建 Task、branch、PR 或 generation。
- R6：目标自身的匹配安装必须可完成 Identity、Bind、continuation 与下一 scope owner 的真实消费。再次归档后的 TS/Python/Guru 受影响消费者有定向验证；不要求第二次真实增代或完整重复生命周期。
- R7：工具更新由原 tools owner 核验固定 source/build/API/native；同步 canonical、managed projection、合同、测试，保留配置、无关任务和会话。分别报告源码、安装、转换、绑定、后续范围状态。

## 6. 约束与依赖

公共 CLI/Core 固定为 Trellis PR #65 source `619133c62d1487c5fbecbf9e00cea9e3f5ea52a6` 的成对候选，版本 `0.7.0-castbox.6`、maintenance API 1.0；版本号本身不能区分旧同名包。候选 release 为 https://github.com/castbox/Trellis/releases/tag/issue-64-candidate-619133c62d14 。本会话已校验下载 hashes、隔离安装并读取 capability；这尚不代表 Guru native 联合验收。

流程由 Markdown 定义，脚本只做确定性操作和校验。通过现有 maintenance transport、acquisition、binding、session 和 continuation owner 接线。验证限本项，不扩成完整多平台升级/Release 矩阵；最多一个必要 clean throwaway。#710/#713/#711 的串行排期与 #64 的功能前置保持各自性质；#711 导航迁移不是本项功能前置。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 输入、入口与预期 |
| --- | --- | --- |
| AC1 | R1–R4/S1 | 原字节或保持十字段关键条件的合法去敏样本及真实 Git、受控 PR provider；公共分类、Guru 准入、实际转换均成功，同 TaskId 增代一次，原档 bytes 相同 |
| AC2 | R5/S2 | pending 和 applied 后绑定中断；原入口恢复同 operation，key/ref 真实，不重复 generation 或资源 |
| AC3 | R3/R5/S3 | 丢失私有结果及真实后继；核验并续接。再次归档后 native 和 Guru 解析不把保留前驱当重复身份 |
| AC4 | R1/R3/S4/S5 | 普通历史/source/后继不一致与原支持家族回归；准确诊断和原路由不变，原档/其他任务保持 |
| AC5 | R6/R7 | 使用实际固定成对包的目标 native Identity、Bind、continuation 和下一 scope owner 实际消费；分别报告各层结果，mock/静态 DTO/applied 单项不能替代联合验收 |
| AC6 | R7 | canonical/managed/声明平台投影、定向测试、代表安装或 reapply/drift、sidecar、diff-check；明确完整矩阵未覆盖 |

## 8. 实际未决项

当前整体需求没有待用户决定的范围问题。实施与历史资格必须由原 owners 完成真实验证；未执行项目不能预填通过。真实业务 Task 安装与恢复不属于本 Task 的隐含副作用。
