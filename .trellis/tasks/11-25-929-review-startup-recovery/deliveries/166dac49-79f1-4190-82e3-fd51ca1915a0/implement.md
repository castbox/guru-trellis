# D1 实施与验证计划

## 1. 输入与引用

实际输入为本目录PRD、design第3节唯一处置及candidate_assessment的真实baseline_current/target_native；根PRD只承载整体scope。固定B=63e71ffd72300dee4f5bfdc030c2a5f342b97f32。必须实际读取design引用的完整关联条件、.trellis/spec/workflow/quality-guidelines.md的Test And Validation Value、subtraction-first-compatibility、preset installer/upstream-ownership及受改包现文件。无前序Delivery。

## 2. 有依赖顺序的步骤与文件责任

I1：原Author完成当前三份规划、真实Architecture贡献和official implement/check JSONL；原Architecture作final_plan，原Approval判断可实施，展示计划接受后由原Activation记录公共Planning。此前不改源码。

I2：trellis-implement在已绑定本Task/D1工作区实现Review package的inspect-review-execution.sh、runtime/execution_facts.py、commands/interface声明及必要行为测试。查询只输出执行事实；覆盖Task/session/checkpoint最小真实路径、必要commit读取、唯一临时项清理与失败分层；planning额外参数--planning-purpose区分candidate_assessment/final_plan，后者保原显式只读对象例外且不执行写probe/绑定恢复，不能写正式记录/选择或做semantic pass。先跑一条真实linked-worktree受限/精确写集路径，避免先扩参数矩阵。

I3：独立写域的实现子Agent修改runtime/task_lifecycle/session_adapter.py及其测试、guru-bind-task-session/runtime/invoke.py及必要package测试，保stdout，按真实操作发最小stderr。无官方session_storage/io或全局npm修改；errno已丢失必须未知，不额外重试猜测。主协调者整合共享依赖，不覆盖任何并行编辑。

I4：主协调者在原Architecture/Review step-local合同整合prelude/能力事实在前、authority语义在后，明确合法design_facts、其他任务历史及generic直接执行/无反馈原owner处置。更新两README和MIGRATION-929，复用current-knowledge，无新Skill/phase/ledger。有关公共command/稳定code、执行写集和旧完整provider接续说明保持一致。

I5：原实施owner运行V1..V5及必要受影响回归；真实Agent用代表完整候选完成正式结果与恢复。只生成本次可丢弃fixture和临时进程/文件，按实际句柄清理本次项，绝不操作原后端、别的Task或共享业务数据。首次设施/参数失败保留原输出和未验证边界。

I6：主协调者通过原guru-upgrade-tools完成matching canonical到dogfood/受影响平台采用，保持当前Task/session与peer；原RDT/Architecture maintenance在提交前完成必要完整单元整合/readback。工程自检与知识整合后准备精确本地提交预览；提交需独立具体确认，随后固定H由新的独立committed reviewer一次完成Architecture before/after及完整Review，发布另行预览确认。

## 3. 验证入口、输入与预期观察

V1：通过新增脚本--help与固定公开参数，从正常owner准备的linked fixture执行inspect-review-execution。真实sandbox采用本机支持的Codex接口，输入同目录/对象，仅改变必要额外写范围。观察仅工作区写失败、精确目录成功、probe临时项清理、候选与正式session/Task内容不变；旧命令/config解析失败不是权限失败。另验证final_plan有context但无绑定/选择，完整显式对象及不可写session目录下只读接入不被新增查询阻塞；不同选择、损坏绑定及其他stage的原错误不弱化。当前0.172.0可用codex sandbox -P <call-local-profile> -c <inline filesystem policy>，不写全局配置；实际CLI exec workspace-write --add-dir仅必要session范围已有样本。

V2：通过managed Python运行runtime/task_lifecycle/tests中的test_control_stores.py、test_composition.py及新诊断测试；guru-bind-task-session实际package wrapper测试补足stdout/stderr边界。输入分别覆盖projection读取、旧session读取、write_record/读回失败，断言原code保留、operation准确、原异常文本/本机身份不输出、可得errno保真/不可得未知。测试不能复制被测实现计算正确结果。

V3/V4：采用guru-review-branch/tests/test_postcommit_review.py及其现public-owner fixture，必要新增test_execution_facts.py和定向恢复用例。执行原recorder/checker/invoke真实逻辑，观察check→full_review同candidate及predecessor、部分失败只补缺步、retired checkpoint后原public结果恢复。fixture语义输入只说明组件层；AC02另由真实fresh Agent在正常owner准备的最小Task/Delivery/B..H完成完整独立Review，不手写或预填pass，不把工具exit0当完成。

V5：真实Agent按修复后入口读取带其他Task历史pass的authority、在authority后审实际candidate对象，直接执行不递归；保actual prelude及关键阶段/正式stdout。对无反馈/未执行只补代表caller处置，进程存活不证明结果。涉及新旧方法对行为的判断时，按design第8节的最小中性对照执行：固定材料/请求及事先判据，独立副本用B方法和本批方法，尽量同模型/配置；执行者不见判据/期望/优选标签，评价方先盲读真实输出和工具轨迹，再揭示映射核对。采用现native执行和采集，不建runner协议或固定轮数。当前已观察的native污染、prompt误读和CLI成功接续用于归因，不能将失败样本删去或推导通用成本降幅。环境无法提供必要真实行为时保该AC未验证。

V6：通过原source/installed package validator及唯一public graph检查、check-upstream-ownership.sh、check-dogfood-overlay-drift.sh、递归sidecar检查及git diff --check，验证实际受改commands/Interface/平台投影。preset工具采用前后核当前Task/session与无关peer保持；遵从原tools owner的完整源及冲突处置，普通apply旧任务阻塞不转为历史迁移。不做完整多平台Throwaway/Release矩阵；若普通accepted范围确需clean，仅一个代表。

所有planned检查未执行均不标通过。managed运行方式及新增脚本argv按design第5节固定，在I2用真实--help/公开command注册验证一致；发生实质方案变化回原Author而非临场扩张。必要工程命令、Python AST/JSON/shell语法与真实差异检查按命中spec运行，不跑无关全套CI/业务测试。

## 4. 停止条件与适用回退点

缺实际Task/Delivery/checkout、不同合法选择或真实identity error回原owner，不能重建Task或覆盖session。若完整writer写集超出既有必要元数据，或要迁移结果authority/新增持久状态，则回Author/Architecture，不靠扩大sandbox或新ledger掩盖。

probe只能证明当下能力；正式写入失败仍保真实原因及原checkpoint，不重试已成立槽或用新pass覆盖。真实candidate/authority/机制变化刷新受影响判断；相同对象无新证据不循环重启。测试设施缺失保未验证并重评最小复现；证据充分即停，不加惯例反事实或固定连续通过轮数。

本步没有部署、数据迁移或已发布新结果，无业务回滚协议。仅清理本次probe/fixture/进程；源改动仅本Task范围，保无关变更。commit、push、PR与Issue关闭保留原独立边界。

## 5. Delivery Policy（唯一）

full：D1一次覆盖R929-01..06与全部AC。完成包含真实声明权限内正式Review、普通恢复、诊断及authority/直接执行行为与必要分发兼容；不把source或candidate通过当全部完成。无延期到D2的已接受能力。外部注入实现或无反馈底因不在本仓可修范围时据实写边界，Guru本身的检测/原路由仍必须交付；不以外部未知自动豁免本仓AC。

Delivery合并不等于Task完成；Task Completion核全部结果与未验证边界。业务后端部署/账号恢复及完整Release矩阵不属于本Task。当前未激活/未实现/未交付。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。RDT原writer维护docs/requirements-design-test-contributions/929-review-execution中的真实需求/设计/测试差额及必要完整proposed目标，再在final_integration重读docs/{requirements,design,test}/current/task-delivery-lifecycle.md的实际相关定义、整合/readback；不向共享根登记逐Issue条目或复制历史增量链。

Architecture原writer消费docs/architecture/contributions/929-review-execution.md及完整proposed leaf，实际晋升为docs/architecture/04-integrations/review-execution.md。该完整单元承接执行事实与语义authority边界，不重写不受影响的root/system/ownership或ADR index；若实现发现现定义真实冲突，先回原owner核差额。

canonical Skill/README/MIGRATION-929由各原source owner维护，原安装/tools owner成套采用；TaskCommit前原owners整合并读回所有目标，保持integrated_pending_review。提交后新独立reviewer审核真实after及before；无旧结果或脚本成功替代。历史#679及本轮失败样本保持原含义，不上传原始会话/凭证/业务内容。
