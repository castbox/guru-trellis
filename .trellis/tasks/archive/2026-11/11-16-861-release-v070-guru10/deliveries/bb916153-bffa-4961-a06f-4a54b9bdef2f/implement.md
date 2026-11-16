# #861 gen2 D1：实施与验证计划

## 1. 输入与引用

采用整体 `../../prd.md` 的当前 accepted_scope及本批 `prd.md` B1–B4/BC1–BC4；本批 `design.md` 第3节是唯一来源设计处置。原 candidate_assessment 为 no_architecture_impact，只评估当前机制，不替代最终规划审核。B/H0及PR目标分别见 design 第1节，四个历史Delivery只提供已交付事实。

实施／审核加载 `.agents/skills/guru-author-task-plan/references/planning-body.md`、适用 design/implement模板、`.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value`、私有发布合同 Complete Source Before Actual Adoption / Whole Preparation Completion / Stage 2，以及 design 第9节列出的当前R/D/T与Architecture关系。实施前另经 trellis-before-dev 加载实际包规范。当前三份规划完成后，仍必须 final_plan→Approval→展示接受→Activation；本轮停在Activation前。

## 2. 有依赖顺序的步骤与文件责任

1. **I1 前置核对**：原实施owner确认同Task/gen2/bb916…、当前checkout与approved plan；重读三处源码和生产helper/runtime。核当前source/installed差额，不把旧安装当新源已采用。不改sealed checkout、历史结果或installed manifest。
2. **I2 测试消费**：只在 `trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py` 迁移M1观察；保留所有原派生/duplicate断言，新增必要record/check envelope来源与同一recorded绑定观察。运行V1。
3. **I3 命令声明和回归**：只在 `trellis/skills/guru-team/packages/guru-discover-change-context/commands.json` 修四处context-request引用；在同包 `tests/test_runtime.py` 补M3。保留supplement1.0的正常输入兼容，不修改生产runtime/Interface/schema。运行V2/V3。
4. **I4 完整源分发**：原安装writer在一个新临时项目执行V4的完整三平台安装及同源reapply，比较全部预期内容，不手工复制受管产物。该样本是local_candidate，不从dirty源对准备checkout执行source_locked。
5. **I5 知识与提交前门禁**：核完整变更与Docs Plan；真实规则差额交原RDT/Architecture owner整合/readback。原trellis-check工程质量职责完成后，由原TaskCommit展示精确文件及commit动作取得其独立确认；不混入并行改动。
6. **I6 独立交付**：原constructor固定完整B..H，原begin_check→一次独立Architecture before/after及完整Check/Branch Review→Delivery Review/readiness→Publish→Merge。各Git/GitHub动作保留原精确预览和独立确认，不预授权。PR用中文具体内容及Refs #861。
7. **I7 后继责任**：D1实际delivered后原Completion确认采用尚未实施，返回additional_delivery_required后才由原Creation规划D2；D2完成后才判断整体Completion/Closure/Finish。本批不预建D2或把实际采用降为evidence_pending。

## 3. 验证入口、输入与预期观察

所有Python执行禁写bytecode；使用项目原managed resolver，或已存在的Python3.12运行测试。命令在当前source根执行，临时目标参数只指本批创建的throwaway。

- **V1**：`PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_verify_trellis_upgrade_contract.py -k NormalPhase0AuthoringTests`。预期四例执行完成，原helper envelope与source断言有效。无需为重复历史测试清零整文件suite。
- **V2/V3**：`PYTHONDONTWRITEBYTECODE=1 python3 -B trellis/skills/guru-team/packages/guru-discover-change-context/tests/test_runtime.py`。观察新回归从四个真实help取得声明，并由当前正常输入通过声明schema和原验证边界；context返回身份不丢失，supplement1.0不被错误升级。执行 `bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`，保留真实errors。Python改动用内存compile检查，另执行 `git diff --check`。
- **V4 建立样本**：新建无历史Task的临时Git项目。使用固定Fork的已构建 `packages/cli/bin/trellis.js init -y --claude --codex --cursor --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#5dc0708a1d817fb9fb02edb64419b7b3c3f7cc10`。先确认该固定来源workflow与当前canonical字节一致；它只供应未改workflow，不能代替本批source。随后从本批source运行 `bash trellis/presets/guru-team/scripts/bash/apply.sh --repo <临时项目绝对路径> --platform claude --platform codex --platform cursor --python <已验证解释器> --json`，再以同一命令reapply。预期两次均无冲突、new_copies和managed_backups为空。
- **V4 读回**：用原installer的 `managed_source_projections` 取得完整声明映射并比较每一实际目标bytes及可执行位、预期集合与registry平台适用性；核完整package/runtime、shared/.agents、Claude、Cursor和overlay。运行目标installed validator与四个实际installed help，按V2合法输入核声明。单独比较workflow、source lock、canonical/installed版本与真实local candidate来源；私有tests及private release Skill不得进入分发，旧受管Codex根不得恢复，`.new/.bak/__pycache__/*.pyc`不得遗留。临时样本的锁/CLI须对应原固定Fork；发现差额按原owner处理。该验证不调用仅支持单一平台选择的native-load profile来冒充三平台样本结果。
- **V5**：原独立完整Review按实际三源码差额和必要未改消费者审核，读取V1–V4真实结果及未验证边界。没有新的完整Release矩阵、真实客户端Agent或外仓采用证明。本批不执行正式发布门禁，D1/D2及Finish合并后Stage2重新最新main执行。

V1/V2是长期回归，V4是临时分发观察。先执行便宜且直接命中缺陷的测试，再安装；不要求旧版本重复失败或回退红绿。原三文件之外若出现必要修复，先判断同scope及机制影响，刷新受影响规划/审查后再实施。

## 4. 停止条件与适用回退点

identity/checkout/scope不符时回原owner，不自行重新选Task；候选机制变化先回Author/Architecture。V1/V2仍失败时保留原输入及第一次偏差，不删断言、不改生产shape换取通过。安装冲突、来源不明、CLI/lock差额或sidecar未处理时，停止该验收并交原installer/tools owner；普通apply的历史Task guard不得绕过。

没有数据库、发布或生产副作用，因此不创建数据回滚协议。保留源码diff和失败观察，只定向修本批内容，不能reset或覆盖并行修改。设施反复失败时重评复现入口，保留尚未满足验收；证据已足够则结束该项验证。TaskCommit、push/PR、merge、Finish、tag、smoke、Release、Issue关闭及cleanup仍各按原边界执行。

## 5. Delivery Policy（唯一）

选择 **partial**：本批独立交付两项发布消费者修复的完整可分发源、直接回归和完整临时安装证明，完成当前选定R/AC及BC1–BC4。其完整性不依赖D2先执行，不能把源缺陷推给采用批。

剩余责任是准备checkout从本批实际delivered的完整干净源完成source_locked采用。临时限制只作用于本批未交付源的正式采用；原因是完整源必须先独立交付。解除条件为D1真实delivered，直接后继为原Completion→Creation→D2 Planning/Activation→guru-upgrade-tools。D2承担实际installed内容、provenance、CLI/lock、native入口、全量bytes/modes、reapply/drift/sidecar及Task/session/配置/peer保留；不以临时安装补成已采用。

整体完成仍需后继交付、whole Completion、reference-only no_mutation Closure与Finish精确簿记进入main。Task外Stage2再冻结届时最新main并完成tag/smoke/Release和发布后选定本地目标收敛，最后处理#861。没有其它Issue状态前置。

## 6. Docs SSOT Plan（唯一）

选择 **no_docs_update_needed**：当前R850/D850/T850的完整匹配采用责任、R735/D735/T735及R868/D868/T868的行为验证与最小边界已经正确，本批不改语义方法、业务能力或生命周期。只修测试消费和命令对既有schema的公开引用；规范性schema、runtime、Interface及发布合同保持。旧验证观察保持历史截止，不把本批结果写回旧结论。

命中引用为 `docs/{requirements,design,test}/current/issue-content.md` 和 `behavior-validation-method.md`，具体identity及差额见design第9节；Architecture authority、constitution和change-contract见design第1节。原RDT writer是guru-maintain-requirements-design-test-ssot，原Architecture writer是guru-maintain-architecture-baseline；直接consumer为后继实施/Review与Completion。若工程结果揭示真实规范差额，回原owner准备完整拟写并在TaskCommit前final_integration/readback，刷新相关规划；当前不预建空贡献、ADR或共享导航。
