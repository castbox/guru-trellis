# 必需正文读取的验证策略与观察

Identity：`RDT-TST-REQUIRED-CONTRACT-READING`；检索别名：`T848`、长文 transport、跨调用补显、首读采用。原语义 owner：`guru-maintain-requirements-design-test-ssot`。关联 `docs/requirements/current/required-contract-reading.md` 的 R848 与 `docs/design/current/required-contract-reading.md` 的 D848。repository-relative locator 从仓库根解析。

知识状态：本能力的验证策略及下述提交前观察；它不是正式阶段结果。

## T848-01 / SC848-TRANSPORT：两层请求与同形材料

对实际工具使用本次确需的长正文，核内层和外层各自预算、正文载体以及实际可见全文。失败须保留初返回；不能缩短材料后声称原合并一次通过。缺失仅在显示层且原结果跨调用可用时，由后续独立调用从同一原内存补显；补显过程不能包含新读取命令。完成后释放原内存引用。

本批固定样本为 Git `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa` 的写作规范，以及 guru-review-change 的 contract、review-method、interface；保持一份/另三份两组。真实内层20,000、外层24,000请求下，两组原结果8,548与10,599 token完整，19,147 token合并显示仍缺7,159。后续独立调用从原 store 完整补显10,599 token组，无新读取命令。结论是原合并显示失败、补显完成全文，不是宿主容量修复或统计改善。

## T848-02 / SC848-INNER：内层缺失回退

内层已经遗漏正文时，提高外层不能恢复它。对该真实缺口用足额全文或连续相邻范围补读，核实际末尾，包括无末尾换行；不扩为任意长度压力矩阵。

本批同一历史 contract 的4,781 token/303行，在内层2,000时缺2,781 token；外层从4,000增至24,000显示同一原结果，遗漏保持。实际读取1—150及151—303两段后覆盖全文和文件尾。

## T848-03 / SC848-AGENT：原入口实际采用

使用无继承上下文的 generic Agent，从实际完整 provider 的原独立入口启动。启动输入只给真实入口、固定对象和正常只读范围。核本轮原生工具事件，观察短方法先于必需长正文、实际预算/载体及缺失处理。原独立审核所需视角和最终 invoke 保持；静态引用、父会话标记或预填结论不能替代该证据。

本批固定未改对象为 `trellis/presets/guru-team/scripts/python/guru_platform_inventory.py`。首次实际工具先定位/读取 installed 短方法，第1—130行覆盖方法及少量相邻正文，没有先读整本；随后用内层20,000、外层24,000及 `.output` 读取写作规范/Skill，后续按实际材料选择预算和范围。首次回应误将自己视为单视角 worker，澄清最终 owner 职责后完成三个独立视角、capture 和 invoke，返回 reviewed。首读行为在职责澄清前已发生。保留首轮误解；不称所有步骤一次成功，也不把该只读样本当本 Task 正式 Review。

## T848-04 / SC848-INSTALL：分发与当前目标采用

长期回归执行原 asset installer/reapply，解析实际声明平台的 native payload，并核 source/installed 的真实路径、短节 anchor、首次长文前的顺序、用户内容和 sidecar。包的平台范围来自 registry，合法 provider-relative/installed 短名引用仍须解析到实际正文。固定预算字符串本身不是行为断言。

本批扩展原 `test_clear_technical_writing.py`，在同一临时仓库覆盖22个入口 payload、原 AGENTS/workflow、独立 Skill、CRLF 用户字节、reapply及零 sidecar；最终通过。fixture 替代 Python runtime 创建，资产 writer 和 installed package validation 实际执行，不证明 fresh CLI init。首次全局包缺 Delivery 模块的 fixture 错误，以及原测试绝对引用/所有平台包假设导致的失败均保留；修正后完整重跑通过。

原 tools owner 对本 checkout 实际采用当前 canonical local_candidate，返回 tools_upgraded。目标 resolver、installed package、原生 continuation、三平台 drift、212项 public target bytes/mode、用户配置/正文和零 sidecar均通过。原 owner 完成807项 peer/runtime preservation；另行复核569个 common/peer pointer 文件保持，238项 peer 自身 runtime 观察由原 owner核验。该结果不代表 formal source lock。

## T848-05 / SC848-CONTINUITY：合同和证据边界

审查原全文、provider、JSON/receipt、mutation 恢复和公共 graph 未弱化。按实际影响运行 source/installed packages、ownership、内存编译、原生格式解析及 diff 检查；它们不代替 AI 对条件、语义和覆盖的判断。本批 source package、ownership、400个 Python 文件内存编译、JSON/TOML及 diff 检查通过，声明平台和实际目标采用分别报告。

本观察截止于 TaskId `848-required-contract-reading`、generation 0、Delivery `b3838f70-f6bc-490a-8269-4b749bad2639` 的提交前工程验证；详细初失败与观察由该 Delivery 的 `validation/reading.md` 承接，活动/归档位置由原 Task identity 解析。本单元是当前策略和当时观察，不复制后续正式结果账本。

RDT 整合只为 integrated_pending_review；TaskCommit、committed Check/独立完整 Review、readiness、Delivery、whole-Task Completion、Closure/Finish 由原 owners 实际判断。`formal_fork_source_lock`、完整多平台升级/Release、宿主内部限制原因、其它业务安装及所有模型的普遍效果保持未验证。固定历史样本是本能力的定向诊断，不成为其它 Task 的通用测试矩阵。
