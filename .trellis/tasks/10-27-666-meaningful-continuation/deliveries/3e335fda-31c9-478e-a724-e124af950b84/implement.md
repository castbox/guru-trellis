# D1实施与验证计划：#666

## 1. 输入与引用

整体accepted scope为本Task根PRD，当前D1完整PRD覆盖R1–R7、AC1–AC7/S1–S7。实际方案见同目录design.md；规范性来源设计仅在其第3节维护处置。实施/检查必须读取完整三正文、源#666及相应条件，不能从编号或链接猜要求。

当前原Architecture candidate_assessment仅评估有界诊断；当前阶段只允许有界调查，不是修复通过。引用现行workflow/Interaction Budget的唯一consumer、对话边界及原恢复；RDT当前三层task-delivery-lifecycle完整单元用于身份/owner/阶段/分层证据，Architecture authority由原owner读取。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、责任与实际动作/文件 | 可审核结果与退出 |
| --- | --- | --- |
| P1 来源与样本准入 | 当前方案经Wording→final_plan Architecture→Approval展示并接受后，由原实施owner核source-lock Fork/Guru完整来源、当前安装和前序实际边界；每写批次先check-task-checkout-boundary | 来源/采用/证据缺口准确分开；缺真实依赖仅阻断受影响项，不改上游/全局安装 |
| P2 正常入口调查 | P1适用；Trellis implement子Agent只执行本批准规划的调查。至多一个代表clean目标，源用固定B和matching Fork现成build；README local workflow sample +完整preset。隔离材料放本Task ignored `.trellis/.runtime/guru-team/666-validation/` 或实际生成的 `/tmp/guru666-*`，不复制业务敏感记录 | V1–V4实际原生轨迹和提示，定位首次不当停顿、直接owner及竞争解释；不得写产品修复/扩大用例或severity |
| P3 因果与方案收敛 | 原主owner读取P2原始事实，执行实际问题/必要性/机制/根因资格；有当前失败保等价before/after起点；无当前失败核历史因果/当前正向及必要停止 | 形成具体机制候选或准确证据缺口。保留同Task/gen/D1/规划/适用结果；不新建替代身份 |
| P4 具体修复规划 | 仅P3真实候选；原Author在同D1改实际design/implement并经独立Architecture、Wording/final_plan/Approval；实质方案变化重新展示接受 | 本步骤结束前无产品源码修复授权。明确命中文件、原加载/调用/消费/恢复边和定向回归；不全生命周期重写 |
| P5 最小实现及完整验证 | 仅适用的P4方案被接受；Trellis implement子Agent改命中canonical Markdown及必要定向测试，原RDT/Architecture按实际差额准备隔离完整proposed；同步受影响dogfood/installed投影 | V1–V6及等价after成立；无当前新修复时只完成有依据的既有修复核验，不制造源码改动 |
| P6 正式质量与交付 | 原完整candidate→独立Architecture phase2→candidate Check→原owner final_integration→重绑actual candidate→最终Check→精确TaskCommit→完整独立committed Review→Delivery Review/Publish/Merge | 逐owner真实结果；commit、push/PR、merge保持各自独立边界，历史/native结果不代替门禁 |
| P7 整体收尾 | D1事实或原Completion适用入口；原Completion审核全部scope及证据，再Closure、Finish和适用Cleanup | #666仅在全部目标真实满足后按原owner处置；不清链外资源，不凭merge/目录/未复现关闭 |

P2/P5的worker只处理已批准步骤；发现范围外候选时在编辑/测试/severity前返回candidate_ref、observed_behavior、locators、minimal_reproduction_hint，由主owner资格和原路由处理，不自行扩写。

## 3. 验证入口、输入与预期观察

V1–V6的行为预期及证据限制以design第8节为准。本节给可执行入口和环境，不预填通过。

1. 写入前：`.trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh --json --task .trellis/tasks/10-27-666-meaningful-continuation`。public current用`python3 .trellis/scripts/delivery.py current --json`；对象或checkout失配先回原owner。
2. P1核实已定位的Fork `79a97ed60fe19e8f287eaddfa74722b5250ced35` 现成CLI/Core build。使用`node <matching-fork>/packages/cli/bin/trellis.js init --codex --yes`在唯一代表目标初始化；按当前README local sample核对/加载canonical workflow，执行`trellis/presets/guru-team/scripts/bash/apply.sh --repo <target> --python <实际managed-compatible解释器>`。记录真实provenance及拒绝，不将全局0.6.17混为matching CLI。若需构建或依赖缺失，保留具体缺口，不下载/修改全局工具绕过。
3. V1–V5使用实际`codex exec --json -m gpt-6.1-sol -c model_reasoning_effort='"high"' -s workspace-write -C <target> -`或该CLI的原resume入口；linked sample仅额外授予其真实Git common-dir写权限以满足原session writer。工具参数如版本不同先读实际help。禁止手改context环境或预绑定/预选来制造native成功。
4. 样本prompt只给真实目标、来源、明确对象、上一步操作事实及边界，不给正确owner/恢复路线/预期pass。入口前置通过原writers建立真实公共facts；测试driver不执行本应由被测Agent调用的下一owner，不注入semantic pass。read-only/setup/fixture与真正Agent执行分开报告。
5. 四类行为与恢复沿真实原生对话观察，必要本地Git操作只在隔离样本内执行，真实业务remote不被调用。延迟/重复回复保持原问题关系；结果丢失/部分完成只选原合同已支持的实际路径，不新增故障注入协议。已完成动作核count/HEAD/refs等事实而不重复执行；归属不明保stop。实际确认/方案提示交原Check及独立Review语义审核。
6. 有当前失败时保留同对象/目标/入口及等价条件；修复后只改matching来源/命中机制并沿原owner接续，保原失败样本和适用结果。无当前失败时为每个历史主张给原始定位、真实修复和因果边，并运行当前正向/必要停止；缺少任一证据不能记通过。
7. V6实际命中后选最小package/runtime suite；运行source/installed package校验、声明平台投影、mode/sidecar、原apply/reapply及`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。涉及overlay时必须原apply同步；若本仓历史归档阻止普通apply，保首失败，进入原guru-upgrade-tools的有界tools-only路径，不批量改旧Task或手写manifest。
8. 规划/最终内容运行`python3 .trellis/scripts/task.py validate <TaskRef>`及`git diff --check`；命中workflow时执行get_context的phase、1.1、2.1、3.5读取。实际改Python/Bash/JSON时执行quality-guidelines规定的命中语法/schema检查。上述机械结果不证明Agent行为。

未覆盖的客户端/平台/mode、远端marketplace下载、业务升级采用、完整Release/Upgrade矩阵及生产明确列出；一个Codex代表安装不泛化为全部平台原生通过。

## 4. 停止条件与适用回退点

- P1缺matching来源/构建/完整安装：停依赖项，回原安装/工具owner，不用旧CLI、单文件patch或假manifest替代。
- P2首失败是正常等待、真实选择、独立副作用或目标完成：按真实类型处理，不为制造修复扩scope；其它独立必要观察继续。
- 根因/历史因果或等价条件不足：P3保diagnosis_incomplete及具体证据缺口，不能推进未经支持修复或Closure。
- source/authority/scope/机制/风险实质变化：回受影响Clarify/Author/Architecture，保同D1；产品源码在P4完成前停止。
- 原操作结果不唯一/未知出口/真实冲突：原owner准确stop，不重发mutation。原普通错误/声明恢复自动承接，不增加例行确认。
- 原Check/Review失败：回最早受影响owner，不制造成功DTO或删除重建身份。不覆盖并行dirty或链外资源。

当前没有业务数据迁移/部署；回退仅是原安装/候选owner对本Task局部材料的合法处理，保原始失败事实。源码、commit/push/PR/merge及cleanup仍保持原独立边界。

## 5. Delivery Policy（唯一）

选择 **staged**，仍为同一个全量D1及整体R1–R7/AC1–AC7，不新增运行模式或公共阶段。

- 当前阶段为A：有界诊断（P1–P3）。进入条件是当前三份规划完成原门禁并被接受；退出条件是形成可定位首停/因果/具体owner候选，或完整已有修复核验结论与真实证据缺口。A结束不允许把未知修复记通过，也不独立宣称D1/Task完成。
- 阶段B：因果方案与最小修复（P4–P5）。进入条件是A支持具体机制，原资格/Architecture/Planning刷新并接受实质新方案；或A证明不需新改动而仍有可执行的核验工作。退出条件是对应全部行为/提示/恢复证据及必要before/after成立。
- 阶段C：完整质量、交付与收尾（P6–P7）。进入条件是全部本批要求有足够实现/行为证据；最终条件是原完整质量/Delivery/Completion/Closure/Finish及适用Cleanup真实结果。没有当前新修复不自动取消任何验收。

真实临时限制只作用于“未知产品修复”及其完成声明：原因为首失败/因果尚未知；解除条件为P3证据、P4具体方案与原门禁；后继责任属于同D1原Author/实施/质量owners。不冻结已确认必要的独立诊断、不要求新Task或Delivery。剩余全部修复/分发/质量责任由本Task整体保留，不能把诊断完成算为#666完成。

## 6. Docs SSOT Plan（唯一）

当前阶段选择 **no_docs_update_needed**：仅运行有界诊断及收敛task-owned规划，没有已确定的共享规范、接口或实现机制变化；现行RDT/Architecture、workflow及历史test.md保持，不能为填模板造空贡献/ADR或直接写shared current。当前结果只保必要task/验证事实，测试原文与前序历史不回写。

命中的当前authority为`docs/requirements/current/task-delivery-lifecycle.md`的R531/R657/R679、对应design/test完整单元，以及`docs/architecture/README.md`定位的现有owner/constitution/change-contract。直接consumer为原Author、Check、Review及Completion，使用实际三正文和后续真实结果，不读另一owner私有artifact。

若P3支持真实修复或必要的新当前行为定义，P4须在本唯一Docs Plan内改为适用策略并列出命中的完整单元、使用指南及派生说明、原RDT writer、Architecture结论、实际隔离贡献与proposed targets。该实质设计变化刷新原门禁后才实施；delta在candidate Check后由原maintenance final_integration晋升，再重绑actual candidate和最终Check/committed Review。不存在未经计划的shared-current写入或无关全局版本递增。
