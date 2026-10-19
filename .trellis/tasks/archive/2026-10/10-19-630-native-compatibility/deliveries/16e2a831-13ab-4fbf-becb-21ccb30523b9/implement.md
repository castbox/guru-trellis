# D1 三系统兼容实施与验证计划

## 1. 输入与引用

读取整体Task PRD、本批PRD/design全文；唯一来源处置为design第3节。Architecture实际candidate_assessment=architecture_impact/target_native，baseline .102、constitution-v1。行为合同为installer.md受管hash/恢复、upstream-ownership.md边界、README当前框架来源、quality-guidelines的Test And Validation Value和Validation Scope Ownership。共享planning-body及三个当前模板是实施/Check上下文，不能只看旧CI计划。

固定B=0543731bf52aa80842fde5db47332380de513cf0。已有同批10da9be7的CI代码继续使用，没有前序已交付Delivery。原PR #634保留，分支codex/630-native-compatibility；所有写入先C3 boundary。

## 2. 有依赖顺序的步骤与文件责任

- I1 runtime implement worker：独占canonical runtime/base_selection.py、schema.py、bootstrap_check.py及同职责必要helper、TaskCommit runtime/execute.py和直接包级回归。执行D1–D4；先正常fixture证据再决定checkout-index。读取完整批准计划及必要spec，不自行改public合同。
- I2 installer implement worker：独占canonical preset Python installer及新cohesive LF helper、其直接测试、canonical .gitattributes及installer/upstream-ownership spec差额。执行D5；不修改runtime/CI/上游。2941行installer仅薄接入，不超过3000；用户attributes块外与真实编辑保护完整。
- I3 CI/integration implement worker：独占ci/runtime_diagnostic.py、targeted_ci.py及专项driver/测试、docs/ci/README.md、source lock与README对应来源说明。执行D6/D7。依赖I1的实际transport接口和I2真实install合同；先协调契约再接入。现有三系统入口不重建、不弱化matcher。
- I4 主会话协调同一Task隔离贡献/ADR与必要操作文档，原RDT writer收敛delta；使用现有apply同步dogfood，处理每个.new/.bak并验证drift。各worker不单独重应用dogfood或写shared architecture current，不revert他人改动。
- I5 完整候选提交独立Phase2 Architecture；原owner基于真实贡献/ADR和完整proposed targets晋升，实际落盘适用性核对后最终Check。实现checker使用配置trellis-check agent，原Check owner作完整语义判断，不以少数命令代替。
- I6 TaskCommit→完整B...HEAD独立Architecture/BranchReview→更新同PRPublication→三系统当前候选原生检查→Ready/Merge。整体Completion另验WindowsCodex和正式发布，Issue不能因本批合并自动关闭。

## 3. 验证入口、输入与预期观察

V1：`python3 -m unittest discover -s ci -p 'test*.py' -v`及file::selector；保留七项已交付行为，新增transport专项必须实际观察target。V2/V5：通过独立driver在target导入根下执行真实Git/schema/TaskCommit fixture；Windows显式`PYTHONUTF8=0`并记录cp1252，读回最终commit与hook/index。V3/V4：现有targeted-ci.yml三系统hash-locked依赖及clean安装；明确Bash路径、单executable解释器、仅python3可见性和实际两case wrapper。旧baseline安装失败与候选成功分别核对。

V6：installer定向测试加真实正常LF/CRLF clone/apply/reapply；初装、checkout、installed validation、真实编辑保护、attributes冲突和原sidecar规则分开观察。V7：采用固定Fork .5并正常pnpm frozen build，运行CLI --help定义的init、update --dry-run/--skip-all、maintain tools_install及原recovery_ref recover/resume、同provider --create-new/--force，然后Guru apply/reapply和实际入口。Windows上游py -3与Guru executable路径分别验证，不能相互混用。

V8：运行source/installed validation、ownership、受影响package及投影检查；`trellis/presets/guru-team/scripts/bash/apply.sh --repo .`后`check-dogfood-overlay-drift.sh`，零未解决.new/.bak。用当前canonical和installed真实bytes核对，不能只验证旧安装。三系统运行绑定driver/target/upstream、环境、命令、返回码，artifact链接进入最终证据。V9：Windows实际Codex会话单独记录CLI版本、hooks开关/一次性审阅前提、启动命令、自动加载与所选Skill真实调用；不以直接hook或静态投影替代。official release由原release skill执行，不在产品CI中伪造。

## 4. 停止条件与适用回退点

产品新机制、范围或authority变化回qualification/Author/Architecture原owner；普通实现缺陷原地修复并刷新受影响检查。依赖安装失败、缺Bash/解释器、schema普通错误、bootstrap失败保持真实非零，不能算缺陷复现或通过。unknown edit/attributes冲突保留原文件，停止activation并报告sidecar。保留其他并行工作区，不跨Task清理。无业务DB/data迁移；源码返工和preset原staging/activation/sidecar承担恢复，不另造事务协议。WindowsCodex缺认证只阻塞依赖验收与最终完成；不得上传维护者凭据或用手工注入规避。

## 5. Delivery Policy（唯一）

Policy=partial。本批现在独立交付完整产品代码、CI回归、受管字节策略、固定上游集成和三系统脚本/安装证据；可交付条件为DA1–DA11满足且当前PR所有适用checks通过。原CI-only政策已因真实Merge门禁不可分离而合法返工，本修订保持同一key/PR与整体accepted_scope。

剩余责任为同Task的WindowsCodex实际会话、整个AC1–AC10最终证据核对以及官方生产发布/任务Closure。它们是整体完成条件，不能用本批合并替代，不能转交#631。Task Completion需原owner按真实事实决定剩余工作；未具备Agent环境不得关Issue或声称Release Gate通过。

## 6. Docs SSOT Plan（唯一）

Strategy=delta_first。I1–I3维护原runtime/installer/source/CI说明和直接测试；installer/upstream-ownership窄新规则须显式与D5/ADR一致。原guru-maintain-requirements-design-test-ssot writer在最终Phase2前判断并reconcile本批真实需求/行为/设计/测试差额，直接consumer为安装者、维护者、Check与Completion；若需要真实RDT contribution则由原writer写并晋升，不能只以文件存在宣称。

Architecture task-owned贡献与必要ADR由Author本次写作，Phase2独立评估完整候选后原Architecture owner负责expected-current绑定晋升和实际落盘核对；随后才最终Check/TaskCommit/独立committed Review。不在Planning直接改共享导航，不制造空贡献或审计缓存。软件release与知识authority版本分离；所有未验证native/Agent/发行边界如实保留。
