# 合法 Agent Skill 的升级投影验收修复实施计划

## 1. 输入与引用

整体输入为 ../../prd.md 的R8/AC6；当前Delivery PRD和design第3节分别拥有本批要求与唯一来源设计处置。消费独立candidate_assessment，Wording后消费final_plan，再经原Approval/Activation。原失败target为 `/private/tmp/guru746-release-existing/matrix/codex/codex-existing/project`。实际前驱来源为Guru .7、Fork 79a97ed60fe19e8f287eaddfa74722b5250ced35/.5；当前正式Fork为ca0e8b931d19ccb87802d6866abd2113a6f707c0/.6。

必要规范：skill-package-contract的Instruction-Only Standalone Packages定义入口；quality-guidelines的Test And Validation Value定义验证效力；causal-completion-semantics区分机制准入、实施与真实结果。Architecture/RDT引用和差额见design第9节，实际共享更新由原owner判断。

## 2. 有依赖顺序的步骤与文件责任

I1：Activation真实delivery_started后，implementation只修改 trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py。按显式agent选择entrypoint，其余原runtime继续wrapper；共用bytes/mode检查，保留runtime可执行与私有scripts拒绝，处理合法缺scripts目录。

I2：同owner修改同目录test_verify_trellis_matrix_capture.py，增加双类型通过与普通缺失/漂移/泄漏回归；保留原stream capture测试。两个非生成文件均保持3000行以内。

I3：执行V1/V2，再运行V3完整existing；审阅差额及diff hygiene。真实新scope/authority变化先回原owner，不自动扩展补丁。verifier不在实际managedinventory，本批不手改dogfood或官方脚本。

I4：交回原主会话，由原Check、TaskCommit、独立Branch Review及Architecture/RDT晋升判断继续。此implementation dispatch不启动Check、不提交、不发布。

## 3. 验证入口、输入与预期观察

V1（AC6-A）：从scripts/python使用匹配source resolver运行 `-B -m unittest test_verify_trellis_matrix_capture`。输入为临时合法安装布局；预期混合包通过，缺失、内容/模式漂移、runtime不可执行、私有脚本泄漏抛MatrixError。模块回归不证明完整升级或Agent行为。

V2（AC6-A）：以修复后的模块对原失败target执行 `_assert_platform_projection(target, codex)`；不改target，预期完整函数通过。原首失败已在本次Author复现。

V3（AC6-U）：从当前来源执行原 `verify-throwaway-install.sh /private/tmp/guru746-g1-existing --mode existing --platform codex --before-tag v0.7.0-guru.7 --before-cli 0.7.0-castbox.5`，设置TRELLIS_FORK_SOURCE=/private/tmp/guru746-fork-ca0e8、TRELLIS_PREDECESSOR_SOURCE=/private/tmp/guru746-fork-79a97、TRELLIS_PREDECESSOR_COMMIT=79a97ed60fe19e8f287eaddfa74722b5250ced35、TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#62b75465957ad0543803bdbe98e6dc222008040e。当前source_state覆盖实际HEAD+delta；预期原existing成功并核退休assets退出。首次执行若目标已存在，则保留旧目录并选择新空临时目录，不删除旧证据。

V4：原发布owner在本批准备与Finish后重新冻结clean candidate，按Issue完整最低门禁重跑。V1–V3不作为V4的发布pass。当前只记录实际结果与具体失败，不预填成功。

## 4. 停止条件与适用回退点

源/Task/Delivery或声明合同不符，回原identity/selection/Author；真实范围变动回Clarify。验证失败保留实际原失败，判断是否命中本批机制，命中后修复再补所影响验证；新范围候选只交主会话资格判断。没有新缺口且V1–V3充分时停止重复测试。

不做生产部署或数据迁移，因此没有生产回滚步骤。保留全部并行改动与历史target，不覆盖前驱、Task历史或用户配置；必要本地修正只针对本批两文件。

## 5. Delivery Policy（唯一）

policy=full：本批完整覆盖当前选定R8/AC6，完成条件为机制修复、必要回归与真实existing验收，并经原正式质量链。generation0的R1–R7结果作为历史交付读取，不能代替本批门禁。整体准备Completion仍核全部适用责任，Closure保持no_mutation，Finish/Cleanup各归原owner。独立切片合并不等于整体准备或Issue发布完成。

本轮没有新增临时功能限制。Stage2新exact candidate、tag/smoke/Release、本地主仓安装及最后Issue关闭仍归发布owner；准备Task不会据V1–V3宣称这些完成。

## 6. Docs SSOT Plan（唯一）

strategy=no_docs_update_needed：本批修复verifier对既有公开Interface的误判，不改变requirement、设计authority、平台支持或安装规范。原RDT writer为guru-maintain-requirements-design-test-ssot，直接consumer为后续Check/Review/Completion；原Architecture owner判断no-impact。当前完整定义见skill-package-contract、docs/requirements/current/issue-orchestration.md R731-06与docs/architecture/04-integrations/distribution.md。

本批规划与两源文件是实际差额，不创建空contribution、ADR、共享导航登记或release ledger。原晋升owners在pre-promotion独立Review后核真实差额与no-change；若实际产生共享差额，必须回最终Phase2/TaskCommit及第二次独立Review。历史观察保持原含义。
