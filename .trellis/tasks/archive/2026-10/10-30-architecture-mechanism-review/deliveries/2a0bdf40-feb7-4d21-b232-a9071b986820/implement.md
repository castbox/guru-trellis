# D1 实施与验证计划

## 1. 输入与引用

先读本批 [PRD](prd.md)、[design](design.md)第3节唯一来源处置及整体 [PRD](../../prd.md)。完整宪法与原 change-contract 决定架构取舍和写边界。公共规则的实际落点、既有能力与本轮差额见 design §2/§4；验证事实、次数和证据限制见 design §8。

这是无前序的全量 D1，固定 B=`2f70796103406683a2f63adfb6b54d247a7433a5`，不以新的 target HEAD 改写内容范围。候选 Architecture 已正式选 target_native，最终方案仍须 Wording、final_plan 与 Approval。Planning 不激活实施。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置 | 原 owner 与实际文件 | 行为与完成观察 |
| --- | --- | --- | --- |
| P0 冻结及原方法观察 | 计划接受并激活 | 测试执行者；Architecture/Completion 的原 native fixture、host corpus、repo 外运行目录 | 先在原 adapter/corpus 增加四组共用 fact-only staging 与必要运输检查，再固定 design §8 事实、host 预期与配置；取得 B 的实际规则，先运行原方法。记录首次失败、有效模型/权限/起点与输出；答案不进入事实输入 |
| P1 原合同修订 | P0 事实与原观察已保留 | Trellis implement 子 Agent；Architecture `references/contract.md`、root `references/contract.md`、RDT `references/current-knowledge.md` | 写实际采用机制、提出方举证、取证、旧规则受审与存量处置；保留完整宪法和原 routes，不生成新状态或评分 |
| P2 直接 consumers | P1 | 同 implement owner；Author `references/authoring.md`、Approval 原 contract、Check/Branch Review 的 `Current constitution consumption`、Completion `SKILL.md` | 按实际职责补引用与完成义务，替换新增能力/单项原则的局部强调；不复制主方法 |
| P3 知识拟写 | P1/P2 | 主会话原 RDT/Architecture owners；隔离贡献和完整 proposed targets | 准备六个 RDT 完整目标和一个 Architecture change-contract 完整目标，保留有效前驱条件；事实运输已由 P0 建立，本步不改共同输入，不写 shared current |
| P4 新方法行为与源验证 | P3 | 测试执行者和原语义审核 owner | 同口径执行四组新方法，与原输出逐次核对；失败先归因，再沿原 owner 修方法或运输，保留首次记录；两边都正确记已有能力 |
| P5 分发 | P4 中源规则/事实已稳定 | 原 preset writer 与验证者 | 完整 apply 同步 dogfood，source/installed 和声明平台字节/mode、reapply/drift/sidecar 检查；一个代表性临时安装即可 |
| P6 候选质量与最终整合 | P1至P5及完整拟写 | implementation → 独立 Architecture/原 Check → 原两维护方 | 固定 B/实际 H/全量 paths candidate/begin_check；独立审全部实现和拟写；候选通过后合法回 implementation，再 final_integration 写入读回，原实施重新绑定 after 并进入最终 Check |
| P7 最终内容审核与交付准备 | P6 | 原 Check、TaskCommit、独立 Architecture/Branch Review、原 Delivery owner | 最终结果覆盖实际 after；commit/push/PR/merge 各沿原精确副作用边界。没有当前授权不执行这些动作；Delivery/Task 完成分别判断 |

实施子 Agent 只负责明确分配的 canonical 方法、直接引用与测试事实运输；主会话负责范围/设计取舍、SSOT 原 owner 写入和副作用协调。Trellis check 子 Agent 按实际完整候选检查，保留必要的独立 Architecture；不得回滚他人改动。本计划不创建后继 Delivery，也不引入临时兼容例外。

## 3. 验证入口、输入与预期观察

所有命令从本 checkout 执行；Python 测试经原受管解释器，参数以当前真实 --help/合同为准。下列是计划，尚未通过。

| 验证 | 具体入口 | 输入、预期与边界 |
| --- | --- | --- |
| V1至V4 / V6 | `trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill <Architecture或Completion> --adapter codex --case <本批事实case> --run-root <repo外目录> --json` | 原 adapter，Architecture 三组与 Completion 存量一组；原/新各一次。事实和 host 预期分开，正式 wrapper stdout 与实际语义逐次核对。只声明被执行场景 |
| V5a package | `trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests -p 'test_*.py'`；同方式运行 root-cause tests，以及发生实际改动的 adapter/Completion 定向 tests | 保持旧公共 schema、wrapper 和 routes；如公共 I/O 未变，不为方法 prose 造字符串镜像测试。实际改了哪个事实运输就测哪个运输行为 |
| V5b source | `trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` | 验证真实公共 inventory/引用/闭包；不提供语义通过 |
| V5c dogfood | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，随后 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 和 `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json` | canonical、完整安装和声明投影无漂移；保留用户内容，逐个处理实际 .new/.bak；不手改副本 |
| V5d 代表安装 | 复用 `test_planning_body_distribution.py` 的真实 preset fixture/原 installer测试支持，在同一个临时目标安装并 reapply 本次命中的完整 package assets | 目标中实际读取新正文，全部声明平台投影和 mode 一致，用户文件保留，零未处置 sidecar；不跑完整 throwaway/Release 矩阵 |
| V5e 内容与文档 | `git diff --check`、命中文档本地链接/完整拟写追踪核对、变更非生成代码3000行限制 | 链接有效、R/D/T关系与来源职责一致，无未替换模板占位；语义完整由原 owners 核 |
| V7 最终质量 | 原完整 candidate Check、final_integration/readback、after 重绑、最终 Check 与精确 B..H committed Review | 旧候选不能证明实际写后内容；历史绿色、计划与 baseline 晋升均不代替当前工程、行为或整体完成 |

原方法侧使用 B 的真实规则文本，与新侧共享同一新增去敏事实和运输；对比只改变受审方法。记录实际有效模型配置，不比较模型不同的两侧。native/配置不可用属于 execution gap，不从 schema 成功推导正确。raw logs 放 repo 外临时目录；长期唯一 Test 只存当前 consumer 必需的来源、逐场景观察、首次错误/修复、验证结果及限制，不保存授权过程或无 consumer 全量轨迹。

## 4. 停止条件与适用回退点

- 必要 authority、真实 native 入口或完整拟写缺失：暂停依赖它的结论，报告具体缺口；不扩大成无关工作阻塞。
- 事实输入、约束或候选机制实质变化：回原 Author/Architecture 和命中资格；真实 scope 改变回 Clarify。同 scope 的运输/schema修正沿原恢复，不重复询问。
- 发现新增字段、writer、长期状态或兼容路径需求：在写入前回原设计判断，说明直接 consumer；本计划没有为它们预授权。
- 语义样本错误：保留失败事实，由原 owner 修订方法或候选并同口径复核。不能用更严格安全规则、重试或删合法样本掩盖失败。
- 分发产生 sidecar：按原受管冲突机制逐个核原文和本地变更，不能静默覆盖。此处没有业务数据迁移、部署或线上回滚；本地修订只针对本 Task 文件并保留并行内容。
- shared-current 或目标推进：原维护方只处理命中实际差额，不追最新 SHA 或覆盖他人贡献。候选失效回最早受影响 owner，部分写入按原唯一 intent 恢复。

## 5. Delivery Policy（唯一）

选择 `full`：D1 覆盖整体 R1至R8、AC1至AC6，当前没有延期到其他 Delivery 的责任。独立交付条件是公共方法、必要 consumers、两类知识完整拟写/实际整合、分发与当前测试、四组真实 Agent 观察及最终质量链全部满足。

规则改完而真实行为或安装验证未完成，不算 full 交付。更少代码、key 或 finding 不证明改进。当前 Task 的外部实际交付仍沿原 PR流程，不把本地成功宣称为安装采用、软件发布或后端业务效果；Delivery 合并后 Completion 再判断全部 accepted scope。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。原 RDT owner 在 `docs/requirements-design-test-contributions/architecture-mechanism-review/` 维护实际 manifest、requirements、design、test、traceability，并准备以下六个完整 proposed targets：

- `docs/requirements/current/knowledge-maintenance.md` 与 `completion-closure.md`：采用机制、举证和纠正决策的存量/整体责任。
- `docs/design/current/knowledge-maintenance.md` 与 `completion-closure.md`：原模块归属、取证/晋升/完成承接。
- `docs/test/current/knowledge-maintenance.md` 与 `completion-closure.md`：四组事实及对应要求/设计/观察、唯一实际结果定位。

原 Architecture owner 独占 `docs/architecture/contributions/architecture-mechanism-review.md` 及其 `proposed/docs/architecture/06-governance/change-contract.md`。完整拟写只更新原 Constitution applicability consumption 的项目方法投影，引用公共主方法；不复制五原则正文，不新增 descriptor/check/result identity。实际贡献与必要 ADR 判断见 design §9。

实现与全部隔离拟写先进入独立 Architecture/原候选 Check。通过后，分别由原 RDT 与 Architecture final_integration 在真实命中目标上保留有效前驱及其他变化，写入并逐一读回。implementation 用同 B 和全部 after 路径重新 candidate/begin_check，再完成最终 Check/commit/committed Review。没有定位、身份或关系变化时不更新总 README，不递增全局版本；历史证据不回填。本批实际测试结果唯一写上述贡献的 test.md，当前 Test 单元只拥有策略和结果定位。
