# D1 设计：正式来源与原发布准备入口

## 对象、基线与唯一职责

本 Delivery 为 `919ce11d-5422-4ad7-adf6-0d376dced420`，属于 `575-release-source-adoption/generation0`，完整承接本 Delivery PRD 的 R1–R5 / AC1–AC6。正式目标为 `castbox/guru-trellis:main`。development baseline 与 public content_base 均为 `66d31cd33f75d4a73277ec252add6e10e56ad977`；B 为明确选定开发基线，不随远端 ref 前进替换。后续 Check 覆盖 B..实际HEAD 和本Task dirty增量；PR target 与B分开。

Architecture candidate_assessment 由独立 owner 实际返回 `baseline_current/no_architecture_impact`。阶段适用 baseline 为 `current-main-0.6.17-guru.98`，constitution 为 `guru-trellis-design-constitution-v1`。候选保持 ARCH-INT-057 / ADR-027 的来源、工具、数据、原native与下一owner职责；没有新增Architecture contribution或ADR要求。方案变化须回受影响原owner；这项candidate结果不能替代Wording后final_plan或Phase2/committed Review。

## Source-design disposition matrix

| 具体来源与原承诺 | 处置与实际落点 | 理由、影响与上游处理 |
| --- | --- | --- |
| Issue575「正式依赖前置」：正式匹配、干净且可构建的来源；不以版本相同或local_candidate代替 | retain：唯一source lock固定PR52 merge7bcbeaad及真实tree/parents/成功CI，matching clean workspace build；原source validator和source_locked采用入口 | source锁升级不自动证明目标安装。CLI/Core同源、manifest/API/bytes/modes门禁保持；不改上游。 |
| MIGRATION577「依赖与采用边界」：local_candidate仅证明隔离开发，正式采用由原来源owner完成 | retain：保留原历史段落，追加本次workspace正式采用与独立验证边界；README当前来源映射更新 | 不将旧packed mode差异改写为已修复，不冒充真实业务恢复。 |
| Issue575 Stage2第4/6项：原preset reapply、原正常旧安装迁移、数据保留、真实native消费 | retain：原Plan2全inventory历史审查与history_only操作；delivery_upstream只修Core package定位 | 固定相邻目录假设阻止正常source workspace，Node依赖解析直接替换该假设；原公共迁移算法、原owner和Task数据写集不变。 |
| Issue575 Stage2第6项与原tools合同：正常升级及source rollback保持 | retain：原Guru prepare首次apply前合成公开AGENTS target，public原writer冻结与恢复 | 共享内容保留Core/Guru原owner；不改source/guard/兼容检查、旧checkpoint或Core template hash含义。 |
| Issue575四版本轴及同源predecessor升级：不同tag/CLI/source不可混用 | retain：私有release四份合同从predecessor tree自身manifest/lock推导predecessor_cli_version，与其Fork commit配对 | `--before-cli`不再错误使用当前official_cli_version。只修命令的来源轴，不增第七输入，不改verifier。 |
| Issue575 Stage1准备与Stage2发布分离，reference_only | retain：Refs-only准备PR、Task正常Completion/Closure/Finish；tag/smoke/Release/Issue关闭回Stage2 | 本Task完成不关闭575，最终candidate fresh gates不被本地准备结果替代。 |

没有将规范性设计降为建议。没有拒绝或改变来源承诺；本表为唯一源设计处置矩阵，PRD与implement仅引用本表。

## 正式来源与版本映射

保持Guru extension revision `0.7.0-guru.4`，目标tag `v0.7.0-guru.4` 仍未发布。CLI/Core为 `0.7.0-castbox.4`；正式Fork source改为 `7bcbeaad31380e7a29c97898cb947c6120a61775`。从同一真实Git对象和成功CI读取完整parents/tree/CI/package manager，写入既有source lock字段；不增加机器路径或安装成功状态。

当前根README、preset/workflow README及public-docs直接映射更新到该来源。稳定Guru `.3` 的旧lock、历史tag/Release与#577唯一Test不改。正式source_locked采用前须使用已提交、干净、matching Guru来源和干净同源Fork build。在隔离throwaway Git source中，以当前完整canonical候选树的精确bytes/modes创建clean本地验证提交，并保留来源parent；原source_locked tools和Plan2真实调用仍执行全部校验。这个验证提交不是正式Task提交或远端release candidate。验证完成后再做完整Check/TaskCommit，并证明实际交付canonical bytes/modes与验证source一致；Stage2仍从真正final main远端SHA重跑provider。不得以dirty source或较早partial Check绕门禁。

## 原 Plan2 Core 定位修正

`delivery_upstream.packages(fork)`仍从实际CLI entrypoint祖先寻找 `@mindfoldhq/trellis` package。选中CLI package后，以其 `package.json` 为基点创建Node `createRequire`，解析 `@mindfoldhq/trellis-core/package.json`，取得真实Core目录。workspace依赖和npm安装布局均走同一解析，不新增sibling fallback。

继续核验CLI/Core package identity和匹配受支持版本；后续原migration2与Core migration API导入、能力检查、source_locked和操作恢复保持。普通缺依赖、错误配对版本、不可读manifest或Node解析失败沿原MigrationError给出精确阶段诊断，不输出原始业务内容。没有重试、缓存、额外状态、锁或第二公共包定位authority。

测试实际执行该函数与Node依赖解析。workspace/pnpm式symlink和npm sibling分别检测原固定目录缺陷与既有布局保留；missingCore与versionMismatch分别检测缺依赖和错误配对。原Plan2 integration在真实CLI/Core与旧inventory观察preview、history_only实际迁移和reapply，不以mock manifest测试替代。

## 原 tools 共享 AGENTS 最终目标

原 tools prepare owner 消费 SDK 明确导出的 `PreparedMaintenancePlan`，并将其公开结构传给 `previewMaintenance(plan)` / `applyMaintenance(plan)`。这项公开 plan 消费与原 Guru installer 对 Guru block 的内容所有权共同构成投影依据；不能仅因对象可改或 validator 未拒绝而认定机制合法。首次 apply 前，原 prepare 用现有 canonical Guru block renderer 对 Core 公开 AGENTS target 计算最终 bytes/mode，再将同一 action 的 target 替换为这个确定结果。source snapshot、operation_id、candidate、guard、其它 action 与 Core 模板 hash receipt 均保持。模板 hash 继续表示上游 Core 模板基线；Guru block 是已有定制，不重算 hash 冒充上游模板。

public 原 writer 第一次 apply 写入并冻结该唯一 target；随后原 Guru installer 的 block 安装应字节不变。resume/recover/rollback 仍只用原 recovery_ref 和已冻结 plan，不重新投影，不改已失败 checkpoint。保留原 Task/session compatibility、later-work 拒绝以及 public rollback 先于 Guru restore 的顺序；不得先恢复 Guru block 来逃过 Core 检查。

B 已存在两个正常 writer 产生不同 AGENTS 结果的质量缺口，本候选并未引入双写。实际首次失败样本保持不动；修复在等价新 predecessor 样本走真实 strict source_locked upgrade、目标 native continuation/下一 consumer 和原 rollback。检查 block 外内容、原 Task/session、source snapshots 与恢复身份保持。定向测试必须调用实际 prepare/renderer/projection，删除投影后原合法双阶段写入与 rollback 冲突应重新暴露；不以复制算法或固定 hash 自证。SDK公开I/O、原tools Skill/contract和canonical/installed投影须具名说明这个首次apply前的消费边界，不新增Fork/API、state、compatibility reader或fallback。

独立 `implementation_discovery` 与新 `candidate_assessment` 已实际返回 baseline_current/no_architecture_impact；它们只判断原责任与机制适用性，不证明代码、rollback或发布通过。原Check继续要求真实修复结果。

## 私有发布前驱命令

原release owner同时读取 `predecessor_tag` 的 `trellis/guru-team-extension.json` 与source lock：manifest声明的target CLI应等于该source lock CLI，否则按原不一致诊断停止。将该值作为调用期 `predecessor_cli_version` 传给 `--before-cli`；`predecessor_fork_commit` 仍来自同一predecessor lock。

当前candidate的 `official_cli_version` 保留当前轴含义。同步 `.agents/.codex/.claude/.cursor/skills/release-guru-trellis-version/references/contract.md`；四份byte parity是分发证明，原verifier从predecessor tree检查旧CLI才是行为证明。使用真实 `.3` predecessor与当前`.4`来源执行该命令；不通过固定文本断言冒充升级成功。

## 安装、保留与验证层次

源码及受管投影由原tools/fullupgrade owner更新，不手动改receipt或复制dist。真实代表样本使用原 `guru-upgrade-tools` 的source_locked preview→prepare→invoke；旧inventory经原 `guru-upgrade-installation` delivery_upgrade的source_locked preview/history_only→apply→reapply。用户内容、历史Task/archive、现有会话/绑定和配置在其原写集与保留合同内核验。

目标自身native continuation和下一真实consumer分别观察，保留工具、数据、历史、会话和业务完成层次。首次Plan2 preview在Core定位前失败的同一inventory应重跑，观察是否进入公共迁移及后继，避免仅将错误搬后。真实业务恢复、生产、完整多平台/native-host、远端最终candidate和tag smoke仍未验证，由原业务/Stage2 owner负责。
