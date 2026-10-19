# D2 Windows Codex 会话实施与验证

## 1. 输入与引用

实际读取Task根整体PRD、本批PRD/design及其第3节唯一来源处置。真实candidate_assessment=baseline_current/no_architecture_impact，baseline .103。必要authority为D630-06、T630-08、docs/ci当前会话合同、quality-guidelines的Test And Validation Value/Validation Scope Ownership、公共所选Skill合同及官方Codex/Ollama配置。D1已delivered，B=cc8f2564cf0a42bbd1209ec9da295412391082cb。

## 2. 有依赖顺序的步骤与文件责任

- I1：主会话继续本地完整模型预检；保留实际失败，确定能正常读取/观察/判断/调用wrapper的候选及程序提示。不得给模型语义答案。
- I2：原I3 CI实现owner独占ci/windows_codex_session.py和docs/ci/README.md的本批修改。加入真实draft/初始HEAD，选择I1验证的模型，明确程序步骤；必要resume共用600秒总截止时间。保持原依赖/清理/rollout和非敏感报告。不得修改公共runtime/validator或他人文件。
- I3：主会话核对实现、ci/test_targeted_ci.py驱动回归和唯一Test差额；原RDT职责只判断证据更新，不创建空贡献或新版本。原独立Architecture检查完整实际候选，原Check owner完成最终Check。
- I4：按标准TaskCommit、完整B...HEAD独立Review、Readiness/Publication创建真实D2 PR，执行现有三系统检查和Windows定向dispatch。若证据需要事后写入，沿原同Delivery修订/检查/提交/Review/Publication更新，不伪造已完成。
- I5：当前候选检查通过并具备本批交付条件后Merge；Completion另行对整体AC1–AC10和Windows真实结果判断，再Closure/Finish/精确Cleanup。没有版本/tag/Release步骤。

## 3. 验证入口、输入与预期观察

V1：实际官方codex exec与必要exec resume，独立CODEX_HOME、正常clean安装、Git HEAD和draft；完整raw rollout审查。首个完整本地成功后才启动Windows，新的程序组织还须重新预检。

V2：ci/test_targeted_ci.py驱动回归及collector的Python语法检查，验证真实fixture准备、错误保持、600秒总预算与原清理接续；不写镜像实现的测试，不重跑无关累计矩阵。

V3：既有targeted-ci.yml公开dispatch，windows_codex_session=true、明确candidate SHA；下载Windows artifact，核对自动上下文与模型实际Skill结果。模型/普通命令失败、非零wrapper或超时均保留未完成，不能只看CLI退出码。

V4：正常D2 PR三系统checks、docs/ci和唯一Test事实自检。此前D1产品/安装证据按依赖适用性复用；本批不改变产品runtime、installer或平台投影，不为证据更新重复apply或晋升知识版本。

## 4. 停止条件与适用回退点

没有可用模型或Windows必需证据时保持未完成，原owner继续有界调查；不要求用户提供凭据或放宽验收。真实新机制/authority变化回最早qualification/Author/Architecture。普通错误在同一Delivery修复。保留其他工作树和并行文件；每批Task/source写前执行C3 boundary。无业务数据迁移或生产写入，无额外回滚协议。

## 5. Delivery Policy（唯一）

Policy=partial。本批独立交付完整的Windows Agent采集器前提/程序组织和说明，AA1、AA3、AA4及当前PR适用检查通过才交付。真实Windows AA2是本Task最终Completion条件；取得后更新唯一Test，未取得不能关闭Issue。D1不重开，不用新切片隐藏失败。全部整体条件仍由Completion owner判断。

## 6. Docs SSOT Plan（唯一）

Strategy=delta_first。原I3 writer更新docs/ci使用说明；主会话在原RDT owner职责内更新唯一Test并判断与D630-06/T630-08的一致性，直接consumer为维护者、Check和Completion。没有requirement/design责任变化时不晋升新RDT版本，不写空贡献。Architecture按当前独立no-impact及实际delta核对，不新增贡献/ADR或 .104。证据保持本地/Windows/脚本/安装/整体完成各自层级。
