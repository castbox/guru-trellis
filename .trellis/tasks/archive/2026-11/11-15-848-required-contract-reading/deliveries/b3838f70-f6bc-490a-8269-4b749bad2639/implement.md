# D1：实施与验证计划

## 1. 输入与引用

- [整体 PRD](../../prd.md) 是已接受整体 authority，当前 revision 为 `sha256:a922f8c7e39c567fb2f954087826c16ddfe57888e7875d7df9bad65941eee3de`；[本批 PRD](prd.md) 展开同一 Delivery 的 R1—R7、AC1—AC6。
- [design §3](design.md#3-来源设计处置唯一) 是唯一规范性来源设计处置；实施前读取其完整条件，不能只按编号实现。
- design §1 的固定 B/H0 与真实 candidate_assessment 是本批起点；没有前序 Delivery。最终 H 在实现、知识整合和 TaskCommit 后由原 constructor 绑定。
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md#reading-required-contracts-in-full` 及 Intermediate Command Stdout 1.0：原方法、prose 与结构化结果恢复边界。
- `.trellis/spec/preset/{installer,upstream-ownership,overlay-guidelines}.md`：原 canonical/managed 分发、22个入口、三平台 dogfood、用户内容/sidecar 与 upstream 不可改边界。
- `.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value`、Validation Scope Ownership：行为导出的最小充分验证；静态、实际 Agent、安装和外部证明分开。
- 原 `guru-upgrade-tools` 完整 source contract：本 checkout 的 tools-only 同步、一次 prepare、精确写集确认、原恢复和 local_candidate 限制。
- `.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`：所属完整单元、隔离候选与原 final_integration/readback。Architecture 同源 contract、宪法和 change-contract 的适用内容按 design §1/9 消费。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原 owner | 实际动作与产物 | 完成观察 |
| --- | --- | --- | --- |
| I1 进入实施 | 当前 Wording、独立 final_plan、Approval 和用户对完整 Planning 的接受；原 Activation | 通过原公共入口进入 implementing；实施 owner 重新读取当前 key/scope、规划和命中 specs，遵守 trellis-before-dev | 公共 current 精确 key/phase；计划不等于已启用 |
| I2 原方法正文 | I1；原 canonical Markdown owner | 只替换 companion-scripts 原 Reading Required Contracts In Full 小节；写直接读取顺序、两层参数例子、真实容量核验、跨调用原内存与补读分支；保留 JSON/receipt 和 mutation 原恢复 | 逐项对照 design §3，不添加 schema/reader/ledger；周边节与 owner 保持 |
| I3 首读导航 | I2；原入口/分发 owner | 在 installer 的 AGENTS_AI_FIRST_BLOCK、canonical workflow Phase Index/continuation、22个已有 finish native payload 和 guru-review-change provider 段加入同源短节导航。独立入口先解析 provider，再短方法、写作及 review-sufficiency。检查 design §4 M6 指定的两份 README，补齐读取方法导航和采用边界 | 导航先于首个长规范请求；JSON/TOML 仍可解析，方法正文未被复制；不改 upstream trellis-* |
| I4 分发回归与真实 transport | I2/I3；原 implementation/test owner | 扩展原 test_clear_technical_writing 真实安装/reapply fixture，使其验证原短节定位、入口顺序与同源正文；执行 V1—V3 和命中机械检查 | 保存真实初失败与补齐结果，断言来自需求而非固定参数自证 |
| I5 本 checkout 采用 | 源码稳定、已有定向自检；原 source-owned guru-upgrade-tools | 完整 matching source、local_candidate 模式；inspect/preview→一次 prepare→展示实际 target/source/写删集并取得确认→invoke/原 recovery；保留 Tasks、session、controls、配置、peer。原 writer 同步 workflow、AGENTS、spec、packages/overlays 和必要 manifest/pointer | tools_upgraded 后验证目标自身 resolver/installed/native、三平台投影、drift、mode、sidecar 与 preservation；声明 formal_fork_source_lock 未验证 |
| I6 实际 Agent 采用 | I5 实际可用；原独立 review 入口 | 无继承 generic Agent 对 V4 固定文件执行实际只读 review，prompt 只给入口、目标和只读范围。保留初次真实动作；若失败，原 owner 正常修订/重入并保留首失败 | 可核验先短节后长文及实际预算/分段，不以静态引用或父历史替代 |
| I7 知识整合 | 完整实现和真实工程/行为结果；原 RDT owner | 按§6准备完整隔离 R/D/T 候选及实际验证边界，走原 impact/promotion final_integration，写当前目标并逐项 readback；Architecture 无新影响则保持 no-change，扩张则回原评估 | 实际整合仅 integrated_pending_review，不产生质量通过 |
| I8 提交与完整独立审核 | I2—I7 完整，原 TaskCommit owner | 展示本批精确本地提交写集并按边界确认；提交所有真实 after。原 constructor 固定 B/H/全内容，原 begin_check。新的独立 Review owner 先 Architecture before/after，再九维与完整差额，真实记录 check/full_review | 冻结候选期间不改内容；finding 交原 owner 修复后提交和补受影响独立审核 |
| I9 Delivery 与整体终态 | 当前 Review/readiness；原 Delivery、Completion/Closure/Finish | 每次发布/推送/PR、合并及最终终态动作保留原门禁。业务 PR 以 Refs #848 引用；合并前停止等协调器。交付后原 Completion 核全部 AC，再走 Closure/Finish | Delivery merged 不替代 Task 完成；不关闭或改动 #847 |

源码预期写集为 I2/I3 指定 canonical 文件、原分发测试及两份 README。I5 的投影写集由原真实 preview/prepare 决定并另行展示，不手抄受管副本。I7 的真实文档写集见§6；本 Task/Delivery 规划只写自身目录。没有新的临时能力限制或后继解除步骤。

## 3. 验证入口、输入与预期观察

验证采用 design §8 的 V1—V6，下面给出执行入口，不预填 pass。

### V1—V3：真实当前 transport 与恢复

固定来源 `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`。材料为：

1. `trellis/presets/guru-team/spec/workflow/clear-technical-writing.md`；
2. `trellis/skills/guru-team/packages/guru-review-change/references/contract.md`；
3. 同 package 的 `references/review-method.md`；
4. 同 package 的 `interface.json`。

用 `git show <固定SHA>:<精确路径>` 读取公开原文。真实 functions.exec 首行请求外层24,000，每条 exec_command 请求20,000；保持来源原同形分组（一份写作规范、另三份一组），只输出 .output。原调用在平台已提供的 store 中保留两组完整结果，观察实际返回与文件尾。合并完整才记录一次显示成功；仍截断则保留原失败，下一独立调用从同一 store 分组或连续范围补显，不新开读取命令。若补显仍截断，继续缩小显示批次，覆盖缺失全文；消费后释放引用。不能把较短新材料的成功写成该合并场景成功。

V2 针对同组材料已观察的内层超量，保留内层不足的真实返回，再足额提高外层观察其不能恢复内层丢失。使用原连续相邻范围补齐必需内容和文件尾。对照只回答这一缺口，不新增任意长文、并发或 fault matrix。判断实际可见全文，命令退出0/原始stdout完整/请求参数存在不能独立算通过。

### V4：无继承新 Agent 的原独立入口

目标固定为当前 checkout 的 `trellis/presets/guru-team/scripts/python/guru_platform_inventory.py`（该文件不属于本批修改）。使用同步后的完整 installed `guru-review-change` provider，fork_turns=none 的 generic Agent 正常启动。prompt 只给实际入口、固定对象与只读权限，不提示“先读短节”、预算、预期 findings 或本批先前结论。原 Skill 自行消费适用方法、调查目标并满足其不同 subagent perspectives。

执行方保留真实首次工具调用、所用参数、实际返回及最终结论；验收方核对 short-method→写作/审核长文顺序、未先读整本 companion-scripts、实际容量选择和缺失补齐。只报告该真实样本及平台层级，不外推所有模型/工具或完整业务项目采用。该 review 是行为实验，不写本 Task 的正式 check/full_review。

### V5/V6：定向 source、安装与投影

- 在原受管 Python 环境运行 `test_clear_technical_writing.py` 的真实安装/reapply 用例。新增检查解析实际 installed 引用/anchor 和 native JSON/TOML payload，检验首读导航与正文位置、用户内容和再次 apply 结果。它证明分发，不证明 Agent 实际执行。
- 通过现有 `check-skill-packages` 原 source/installed 入口检查真实公共 package/graph，`check-upstream-ownership.sh --repo . --json` 检查原 owner inventory。按脚本实际 --help/contract 组装参数，不导入 private runtime 替代 public entry。
- 采用后运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`，核 Claude/Codex/Cursor exact selected projections、实际 mode、sidecar 和 target native context 入口；不执行专门 Release 多平台矩阵。
- Python 源文件使用 quality-guidelines 的内存 compile；JSON/TOML 用标准 parser；`git diff --check` 检查实际候选。没有 runtime/schema/typed exit 差额时，不为凑数量重跑全部 lifecycle suite。

V5 长期回归服务真实引用与分发缺陷；V1—V3 是定向诊断，V4 是本项要求的真实采用观察。完整输入、工具层级和剩余局限必须分别表达。仅当当前证据不能回答具名的验收/归因问题时追加最小实验；证据充分即停止，不要求惯例性红绿/回退或统计改善。

必要验证结论及原失败可在本 Delivery 的 `validation/reading.md` 由实际执行 owner 简洁记录，直接供 Check/Review/Completion 消费。记录真实输入、行为观察、结果及限制，不建逐文件读取 ledger、hash/mtime bundle、授权过程或长期 reviewer 审批记录。完整原工具输出仍按原调用/平台保存，不伪造 stdout。

## 4. 停止条件与适用回退点

- source/scope、必要真实场景或机制实质变化：停止依赖工作，回原 Clarify/Author/Architecture；不改已接受整体 PRD 的 hash 来延长旧结论。
- 缺 complete provider、公共 API、固定对象、工具实际能力或目标冲突：回原 source/tools owner 的具体诊断，不回退旧 target dispatcher、不制造 schema/影子 reader 或迁移无关 Task。
- 工具写入后的 output loss/partial failure：用原 frozen operation/recovery_ref 恢复，保留已有实际写入，不重复 prepare/mutation。rollback 是另一个原 owner 审查的精确副作用；不 reset/stash 或回退并行内容。
- 真实 transport 仍截断：保留首失败，按原内存/连续范围完成；不能因 nominal 参数宣称通过。若仍不能获得所需全文，暂停依赖它的判断并保留受影响 AC 缺口。
- V4 未实际采用：保留初样本，修正原方法/入口或原 scope 问题并按实际差额重入；不把静态结果改称采用。基础设施反复失败时重评复现入口，缺失验收保持未通过。
- 当前验证已足以证明选定行为和命中回归时结束追加实验。没有业务数据迁移，因此不设计数据库回滚；远端写入尚未发生，不预设远端恢复已成功。
- 保留所有并行内容和 #847 的原资源。合并前必须停止等协调器；未获本次精确确认，不创建 commit、push 或 PR。

## 5. Delivery Policy（唯一）

**full**：本 D1 覆盖整体 R1—R7、AC1—AC6，无延期到 D2 的已接受实现责任。完整交付包含方法、所有命中首读导航、实际 transport/新 Agent 验证、受管采用和必要 RDT 整合；全部经当前 committed Check/独立 full Review 和 readiness。

local_candidate 的 formal_fork_source_lock、完整多平台/升级/Release、宿主内部容量原因及其它业务仓库实际采用属于已声明边界，不是假定本批通过。原需求要求的新 Agent 行为或当前目标采用未完成时，不能以“源码已交付”关闭本 Task。

Delivery 合并后，由原 Completion 读取全部实际结果判断 whole-Task 完成；Closure 才处理 source Issue，Finish/归档和 Cleanup 另由原 owners 执行。本地 branch/worktree 为 caller_owned，不能因 Task 完成而自动删除。

## 6. Docs SSOT Plan（唯一）

**strategy：delta_first**。原 `guru-maintain-requirements-design-test-ssot` 是 R/D/T 唯一 writer；直接 consumers 为实施、完整 Check/Review、Completion 及后续读取该能力的 Agent。实现及真实工程验证后、TaskCommit 前，由该 owner 完整审查并沿 final_integration 写入/readback；整合仅 integrated_pending_review，待实际 committed Review。

计划在独立能力 `required-contract-reading` 的原 RDT 隔离 contribution（`docs/requirements-design-test-contributions/848-required-contract-reading/`）准备完整需求、设计、测试和 traceability/必要 manifest，不拷贝未变 authority。真实拟写目标为 `docs/requirements/current/required-contract-reading.md`、`docs/design/current/required-contract-reading.md`、`docs/test/current/required-contract-reading.md`；原 owner 先核 bounded multilingual/literal 发现结果，若已有同能力完整单元则整合原单元，不创建第二 current。

需求单元说明能力、适用入口、完整性及验证边界，精确引用唯一 canonical 方法；设计单元说明原 owner、provider/target、导航与受管分发职责；测试单元承接真实 transport、首次失败、跨调用补显、Agent 采用与安装实际观察，并保留未验证项。三层只维护自身完整定义和真实关系，不复制方法全文、不改全局 README/index、system/ownership 汇总或无关版本。

canonical managed-spec 与原 workflow/Skill 导航由 I2/I3 的原 owner 维护，preset 安装到 `.trellis/spec/workflow/companion-scripts.md` 及对应投影；两份 README 说明原短节与采用方式。命中 review-sufficiency 的 R/D/T provider/真实行为/分发边界保持，不借本项改其审核职责。必要关联由原 RDT owner 判断后在所属正文维护。

Architecture 当前 candidate_assessment 为 no impact，故不新增 Architecture contribution、ADR 或逐项登记。final_plan、实施发现与 committed before/after 仍各判断真实差额；若边界发生变化回原 Architecture，不由 RDT 代写 Architecture authority。
