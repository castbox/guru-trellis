# #600 整体需求

Direct Source：https://github.com/castbox/guru-trellis/issues/600。本 Task 完整负责原文 AC1..AC8。以下为当前需求正文，关联工作仅按原文用途承接。

## 1. 问题与目标

当前合同要求先完成独立完整 Branch Review，再晋升共享 CURRENT 架构基线。晋升产生新差额后，流程要求重新执行 Phase 2、Task Commit 和完整 Branch Review。

已核验案例：[ai-chat-roleplay-backend#649](https://github.com/castbox/ai-chat-roleplay-backend/issues/649) 的实现候选 `8caf0a5ee81217dd17841c247c197014453632d2` 完成完整 Branch Review 后，[晋升提交 bd0d6f9a](https://github.com/castbox/ai-chat-roleplay-backend/commit/bd0d6f9a16ff5b771e480666ecbc407ff4753244) 只修改架构 README、Runtime 和 Source Map。该提交新增 34 行、删除 5 行。流程随后要求再次完成 Phase 2 和全部 34 个文件的完整 Branch Review。本案例记录当时的流程重复，不证明业务实现存在缺陷，也不证明部署完成。

本 Issue 将独立架构审查和分支内晋升前移到最终 Phase 2 检查之前。当前 Delivery 的最终完整 Branch Review 必须一次覆盖实现、文档和晋升后的基线。

“一次”只约束候选稳定、审查通过且无后续实质修订的正常路径。它不限制 Task 的合法多次 Delivery，不限制 finding 修复后的必要重审，也不承诺每种工程命令只执行一次。

当前规则来源：

- `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md` 及 `references/contract.md`。
- `trellis/skills/guru-team/packages/guru-review-branch/SKILL.md` 及其结果适用性合同。
- `trellis/workflows/guru-team/workflow.md` 的 Architecture、Check、Task Commit、Branch Review 和 Delivery 路由。
- 上述 package 的晋升、当前结果绑定和 consumer 接续测试。

## 2. 对象与职责

本文的 owner 指既有 Skill 所拥有的职责，不新增人员角色。协调会话切换后，该职责必须按原 entry、独立输入和结果适用性合同继续执行。finding owner 闭环、真实未完成事件后的 replacement 和 fresh-final 分离继续遵守原合同；本 Issue 不改变 reviewer 替换条件，也不得用新会话身份代替真实独立审查。

| 对象 | 定义与职责 |
| --- | --- |
| 晋升前基线 | 本次变更的架构比较起点。它包含适用的 constitution、change contract 和原架构事实。原 Architecture owner 必须定位其可重读版本。 |
| 拟晋升差额 | 准备写入的完整架构正文、必要 ADR、来源和验证边界。草稿不得作为已接受架构事实供其他任务消费。 |
| 独立架构审查 | 现有 Phase 2 Architecture 评估职责。独立 reviewer 必须对照晋升前基线，审查实际候选、未修改但受影响的消费者、贡献和拟晋升差额。 |
| 分支内晋升 | 原 Architecture owner 核对 expected-current 后，把受审差额写入当前执行分支。该动作不更新目标分支，也不表示交付、部署或实际采用完成。 |
| 最终 Check | 原 Check owner 对包含晋升差额的完整当前候选执行正式 Phase 2 检查。 |
| 完整 Branch Review | 独立 reviewer 对最终固定 base-to-HEAD 范围执行完整语义审查。它必须独立判断架构与实现，不能继承前序 semantic pass。 |

整个 Delivery 合入目标分支后，该分支上的架构基线才更新。源码接受、本地验证、合入、部署和实际采用必须分别表述。

## 3. 正常顺序

1. Planning 必须明确架构方向、基线影响和必要 ADR。Planning 不得提前声明实现已完成。
2. 实现进入可审查状态后，原 owner 必须准备完整贡献和拟晋升差额。该候选必须包含本次需要交付的实现、测试、文档及 Docs SSOT 更新。
3. 独立 reviewer 必须执行现有 Phase 2 Architecture 评估，并审查拟晋升内容。它必须先依据原 authority 和实际候选形成判断，再核对任务说明及贡献。不得新增一个与该评估内容相同的独立审批阶段。
4. 审查通过后，原 Architecture owner 必须重读 expected-current，并执行分支内晋升。实际写入必须与受审内容一致。晋升不得以事先取得完整 committed Branch Review 为前提，也不得要求虚构未来提交范围。
5. 原 Check owner 必须完成最终 Phase 2。Architecture owner 必须核对实际晋升差额和晋升前审查结论的适用性。候选语义、依赖和验证义务未变且写入符合受审内容时，不得仅因基线版本或身份变化重复派发同内容的独立 Architecture 评估。正式 Check 仍须覆盖晋升后的完整候选。晋升前结论只用于本次晋升及适用性承接，不能冒充晋升后结果；后续正式输出必须绑定实际候选和实际已执行的审查。
6. 原 Task Commit owner 必须提交当前完整候选。提交后检查和结果绑定沿其现有合同处理。不得把既有合法绑定刷新误算为本 Issue 保证删除的检查。
7. committed 阶段的独立 Architecture 判断和完整 Branch Review 必须保留。它们必须覆盖最终固定范围，包含贡献、晋升文件及受影响的未修改消费者。它们不得使用前序通过结论代替当前判断。
8. Delivery Review 和 Publication 必须消费当前候选上适用的正式结果。正常路径不得在完整 Branch Review 后例行补写架构正文。Completion 和 Finish 不得重复晋升已经接受的同一贡献。

无架构影响时，原 owner 必须执行现有 no-change 路径。该路径不得为满足流程新增 contribution、ADR、晋升写入或额外阶段。

## 4. 审查依据与结果适用性

### 4.1 保留变更前后的比较

晋升后的 CURRENT 也属于受审变更。Phase 2 和 committed 架构审查必须保留晋升前基线到当前候选的比较。

不得仅以新基线已经接受当前实现为由，认定实现符合架构。不得把新基线当作本次变更原有的约束，掩盖新增职责、扩大后的偏离或失效的原约束。真实架构决策变更必须有当前需求依据，并按原合同完成必要 ADR 和独立审查；不得把原基线解释为永久禁止演进。

expected-current 只用于核对这次写入的前映像。它不得替代独立架构判断，也不得绑定用户授权。

### 4.2 先判断变化，再选择回程

| 当前变化 | 必须执行的动作 |
| --- | --- |
| 实际晋升与受审内容一致，且候选语义和依赖未变 | 原 owner 核验写入及结论适用性，继续最终 Check。不得因晋升动作整体回退。 |
| 写入超出受审内容，或发现新的架构事实 | 返回受影响的架构评估。完成后继续同一 Delivery。 |
| 修订改变职责、行为合同、兼容性、实现或验证义务 | 返回最早受影响的既有 owner。重做受影响判断和检查，保留仍适用的工程执行事实。 |
| expected-current 因正常外部更新而不匹配 | 原 Architecture owner 判断差额、冲突和依赖。不得覆盖新 current，不得仅因版本推进重跑全部业务验证。 |
| 旧结果缺失、过期或不能证明适用 | 沿原 owner 的恢复或补审路径处理。不得从版本号、路径相同或旧 passed 推导新通过。 |

本 Issue 不改变 requirement authority。基线引用更新不自动使需求、设计和测试结论失效。实际义务变化仍须经原 owner 判断。

晋升后的 finding 修复若改变架构判断、贡献内容或基线陈述，Architecture owner 必须更新本次受影响的贡献和基线差额，完成受影响审查，并返回适用于当前候选的结果。旧 reviewed_promoted 不得为变化后的内容放行。未变化的贡献和已完成写入不得重复晋升。修复未影响架构内容时，不得仅因 HEAD 变化重复晋升。

### 4.3 完整审查后的窄范围修订

本段只覆盖本次晋升所需的来源引用或状态表述修正，不建立通用增量审查平台。修正必须对齐已有可核验事实。它不得新增架构接受、验证通过、部署完成或实际采用的事实主张。出现新的事实主张时，原 owner 必须核对其证据并选择受影响的审查路径，不得仅按“状态表述修正”放行。

原审查 owner 必须先确认：原完整审查可定位；最终候选相对受审候选的全部差额已识别；该差额没有改变职责、行为合同、兼容性、实现或验证义务。

满足上述条件时，原 owner 必须审查差额及受影响依赖，并通过原正式结果出口覆盖最终候选。当前结果必须明确承接原完整审查和新增差额，不能把旧 passed 直接标记为新 HEAD 已通过。

实施必须明确该窄路径的输入、绑定和唯一 consumer。现有仅适用于真实 Git 整合的 continuity 出口不得被直接套用于普通文档修订。原证据无法恢复或变化超出上述条件时，必须返回既有恢复或受影响审查路径。

## 5. 晋升恢复与迁移

晋升写入未全部完成或输出丢失时，原 Architecture owner 必须读回实际状态，区分已完成、未完成和冲突内容。

原晋升意图可唯一恢复且不存在冲突时，Architecture owner 必须沿同一操作完成尚未完成的写入，并核验最终结果。原意图不能唯一恢复或存在冲突时，必须停止写入，并沿该 owner 的既有阻塞及处置路径处理；不得猜测目标内容。已经完成的写入不得重复晋升。恢复不得重复创建后继版本，不得覆盖冲突内容，也不得把未完成写入作为完整成功结果发布。超出原受审内容的恢复必须返回架构审查。

新合同必须说明进行中 Delivery 的承接方式，覆盖尚未晋升、已经晋升但最终审查未完成、最终审查已经完成这三类正常状态。

已经晋升的同一贡献不得仅因安装升级再次晋升。仍适用的审查事实必须保留。真实缺失的审查必须补齐。旧结果不得改写为新合同下的通过。安装和升级沿现有完整安装合同执行，不热替换活跃任务的少量受管文件。

## 6. 实施与验证边界

复用现有 Architecture、Check、Task Commit、Branch Review 和 Delivery owners。Markdown 必须定义判断、顺序和回程。脚本只执行确定性动作并校验 identity、freshness 和结果一致性。

修改范围限于本 Issue 直接影响的 canonical workflow、Skill、public I/O、consumer 路由、validator、测试和文档。晋升入口必须绑定真实可审查候选，不能继续要求尚未发生的 committed Review 结果。破坏性语义变化必须提供明确的版本和迁移合同，不得静默修改公共 Skill、exit、schema 或 command 的既有含义。

必须同步 dogfood、声明平台和安装投影。Overlay 变更必须执行既有 apply/reapply/drift 检查。必须逐项处理 sidecar，并保留用户本地修改。

架构正文必须记录事实、决策、必要来源和验证边界。不得仅为补写最终 Branch Review 通过或最终提交 SHA，再新增一次文档提交。必要来源仍须可定位；审查结果沿现有正式结果及 Git/PR 事实承接。

不新增审批链、审查账本、长期审查日志、通用增量审查平台或第二套状态机。不持久化用户授权。不修改业务仓代码或生产环境。不扩展恶意篡改、竞态压力或额外故障注入场景。

验证范围限于受影响 package/runtime、实际 AI 正常路径、平台投影和 reapply/drift。有干净安装证明义务时，最多执行一个代表性 clean throwaway。完整累计 Upgrade/Release 矩阵不属于本 Issue。未验证边界必须如实记录。

## 7. 验收条件

- [ ] AC1：当前 Delivery 的稳定正常候选完成“现有 Phase 2 独立架构评估及拟晋升审查 → 晋升 → 最终 Check → Task Commit → committed 架构判断及一次完整 Branch Review → Delivery”。完整范围包含晋升差额；无晋升导致的整体回退或同内容架构加审。
- [ ] AC2：实际实现、未修改消费者或拟晋升内容存在未获当前需求及必要架构决策支持的偏离时，独立 reviewer 阻止通过。即使新基线正文声称接受该实现，也不能抹去前后比较中的违规。缺失或不匹配结果不能供后续 owner 放行。
- [ ] AC3：受审差额一致时正常前进。超出受审内容时返回架构评估。expected-current 更新先处理真实影响。未完成写入和输出丢失在原意图可唯一恢复且无冲突时沿同一操作恢复；无法唯一恢复或存在冲突时停止写入。不重复创建版本、不覆盖冲突、不误报成功。
- [ ] AC4：无架构影响的 Delivery 使用 no-change，不新增 contribution、ADR、晋升写入或额外阶段。一个 Task 的多次合法 Delivery 各自使用其正常路径，不受 Task 级“一次审查”限制。
- [ ] AC5：晋升后的 finding 修复按实际影响返回 owner。架构内容变化时，贡献、基线和当前结果必须同步承接修复；架构内容未变时，不因 HEAD 变化重复晋升。完整审查后的窄修订只对齐已有事实，并取得覆盖最终候选的正式结果；新事实主张、行为或架构合同变化不能走该窄路径。不得仅依据文件后缀、代码 tree 相同或旧 passed 放行。
- [ ] AC6：基线正文不因补写最终审查通过或最终 HEAD 产生循环提交。必要来源可定位，源码、本地验证、合入、部署和实际采用的状态分别准确。
- [ ] AC7：三类进行中 Delivery 按明确迁移合同继续。已完成晋升不重复执行，仍适用事实保留，真实缺失审查补齐，旧结果不伪装为新合同通过。协调会话切换不改变 Skill 职责；finding owner 闭环、replacement 条件和真实独立审查继续遵守原合同。公共入口及 consumer 使用匹配版本。
- [ ] AC8：canonical、dogfood、声明平台和安装投影一致。行为验证观察实际独立判断、晋升写入、Check、完整 Review 和 consumer 接续。文本关键词、schema 通过或预填绿色 DTO 不能单独作为行为证明。

## 8. 关联工作

- #283 已建立贡献和晋升治理。本 Issue 保留治理职责，调整晋升时机和直接消费路由。
- #404 已交付独立架构审查方法。本 Issue 保留其输入边界、读取顺序和独立判断，不重建 reviewer 体系。
- #578 已交付工程执行事实的适用性判断。本 Issue 沿用该能力，不得把命令复用视为语义审查结论继承。
- #575 负责自身版本发布。本 Issue 不自动成为整项发布前置，不接管发布矩阵。
