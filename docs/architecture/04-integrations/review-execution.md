# 独立审查的执行条件与正式结果

Identity：`guru-review-execution-boundary`。状态：`integrated_pending_review`。Owner：原 Architecture 维护方；公共执行方法由原 Architecture／Review／Bind packages 拥有。本文记录提交前整合定义，独立 committed Review 尚未完成。

## 适用来源与整合边界

本单元来自 [Issue #929](https://github.com/castbox/guru-trellis/issues/929)、Task `929-review-startup-recovery/g0`、Delivery `166dac49-79f1-4190-82e3-fd51ca1915a0` 的已接受 Planning，以及[原隔离贡献](../contributions/929-review-execution.md)和其[完整 proposed leaf](../contributions/929-review-execution/proposed/docs/architecture/04-integrations/review-execution.md)。固定 before authority 为 Git `63e71ffd72300dee4f5bfdc030c2a5f342b97f32` 下的 Architecture Baseline、design constitution 和 change contract。根 authority identity 保持 `guru-trellis-architecture`。

原 Architecture maintenance owner 在 `final_integration` 消费实际实现、工程结果和完整 proposal，写入本单元并读回。该整合不产生独立质量 pass、发布资格或整体完成结论。TaskCommit 应纳入真实 after，随后由独立 committed reviewer 判断固定 B..H 的 before/after。原贡献保留其当时的候选状态和观察截止，不成为第二份 current 定义。本次沿用 ADR-POSTCOMMIT-INDEPENDENT-REVIEW、ADR-KNOWLEDGE-NAVIGATION-ISOLATION 和 ADR-EXPLICIT-REVIEW-OBJECT，不新增 ADR 或共享登记。

## 责任与顺序

独立 review 的实际执行者先在最小工程规则下核 actual prelude、对象定位与职责所需读写能力，再按原 authority-first 顺序作语义判断。Task／Delivery 和实际 design_facts 是待审对象，不是实施者先前 pass；不预载本 Task PRD、验收、实现总结、先前通过或 scope defense。其他 Task 历史 authority 只保其原范围，不替代当前判断，也不一律表示污染。

能力查询只报告当前对象读取与所需目录的唯一临时 create/write/rename/delete 事实。它不建立 Task／Delivery 选择，不写正式 session／Task 记录，不产生 semantic pass、发布资格或未来权限承诺。临时对象用后清理，已有文件保持；失败保留实际操作、脱敏位置、异常类别及可取得 errno，无法取得时不猜测。没有读过证明、能力 ledger 或授权持久化。

## 最小写集与单写

原 Bind／Selection 使用 Git common-dir 下的 `trellis/sessions`。正式 Review 使用原 Task 的 `task.json` 和 JSON writer 同目录临时项，以及本 checkout 的 `.trellis/.runtime/guru-team/owner-checkpoints/<task-directory>/<Delivery>/review-gate.json`。必要 call-local carrier 使用后清理。源码、测试、文档与其他 Task 不属于 reviewer 写入职责，固定候选需保持。启动者按实际载体配置必要范围，不以全盘访问替代最小范围判断。

这些写集按原实际职责适用：`candidate_assessment` 有 context 时保留原绑定／选择职责，confirmed no-context 保留原显式对象路径；`branch_review` 保留完整正式写集。`final_plan` 遵从 ADR-EXPLICIT-REVIEW-OBJECT，完整显式对象可只读校验，合法已有选择复用；无绑定／选择时不恢复、不写选择、不探测上述写能力，即使 session 目录不可写也不能据此阻塞。不同选择、损坏绑定和真实冲突仍回原 owner；例外不扩展到 Author／Approval／Activation 或其他 stage。

目录 probe 不等于正式写入成功。实际需要绑定／选择的原入口仍由 Identity／Ensure／Bind／Selection 完成状态校验；原 reviewer 独立判断，原 recorder/checker/invoke 顺序记录 check 与 full_review 及其真实 predecessor。不同合法选择、真实身份／阶段／内容错误由原 owner 处理，不借环境身份或绕过 public API。

保留原 writer 可直接修正本次启动写范围遗漏，并复用既有双槽和恢复边界。迁移只读语义 reviewer 与结果 writer 会增加结果交接及 owner／provenance 变更，本次未采用。能力 probe 增加一次当次临时 I/O，只在实际写职责需要时使用；它不要求长生命周期状态或完整读取缓存。若真实职责需要扩大写集、增加结果 owner 或持久状态，回原 Author／Architecture 重新判断，不能靠扩大权限掩盖变化。

## 失败与恢复

原 Bind 对 projection 读取、既有 session 读取、写入及读回保留真实分层。稳定 `official_session_write_failed` 不专指写权限；最小技术诊断供当次 caller 定位，不能泄露 payload、context 或原异常敏感文本。底层官方 API 已丢失 errno 时明确未知，不编造故障原因。

同 candidate 部分结果写入后，原同 owner checkpoint 承接未完步骤，恢复采用真实已写公共槽，只补缺步。checkpoint 退休后，原 public results 承接 lost stdout。没有完整语义覆盖时必须补真实审查；不得空写 pass、重复 gate 或无因重跑全套工程命令。合规同 reviewer 优先续审，覆盖丢失或影响无法界定时按原合同补足。

generic／CLI 已承担审查职责则直接完成，不递归派发同职责。无反馈时核本次原句柄、事件和阻塞／结果缺失，存活不能证明完成；沿原 blocked/re-entry，不作无变化循环等待或新开。actual prelude 不合规时不能假装遗忘来恢复独立性，应选择可满足原条件的干净受支持设施。

## 知识与证据边界

完整当前 authority 与必要关系由 current-knowledge 发现与读取；根入口不逐 Task 追记历史。历史按影响追溯，不能用摘要缓存、路径剪枝或父 read marker 替代实际全文。未迁移业务仓由其原 owner 按匹配知识采用，Guru 修复不直接改业务私有文档。R929／D929／T929 的完整需求、设计与验收分别由 RDT 原 owner 维护在 `docs/requirements/current/task-delivery-lifecycle.md`、`docs/design/current/task-delivery-lifecycle.md`、`docs/test/current/task-delivery-lifecycle.md`；公共方法及精确接口仍由原 packages 和 [MIGRATION-929](../../../trellis/presets/guru-team/MIGRATION-929.md) 拥有。

本次维护采用的工程观察及首次失败见 [#929 验证记录](../../requirements-design-test-contributions/929-review-execution/test.md)。query 10 项和 postcommit recovery 11 项通过；后者使用 fixture 语义，只证明组件正式写入、前驱和恢复逻辑。Bind runtime 15、contract 3、portable 2、control 19、composition 20 项通过来自实施方结果，不以数量推断真实 Agent 或 sandbox 通过。

真实 Codex sandbox 的 query 样本中，缺 sessions 写范围时 `create_temporary_file` 失败，异常为 PermissionError、errno 为 1；只增加精确 sessions 范围后，四处必要目录 probe 成功。另一个有 context、无绑定的 `final_plan` 样本在 session 不可写时只读完成，没有 write probe 或新建绑定。三组正式 Task／session 字节保持，且没有 probe 残留。这些观察只证明该对象、载体和目的下的当次能力，不替代完整 Review。

本次 matching tools 正式返回 `tools_upgraded`，安装版本为 `0.7.0-guru.12`。已读取的原结果覆盖 source／installed、ownership、drift、native、help 及 preservation；选定平台为 Claude／Codex／Cursor，无 sidecar，106 个保持 roots 无变化。首次 target-resolver 的 runtime_dependency_missing／rc2 与最终 sequential resolver rc0 均保留；底因未定位，不推断为并发或权限问题。`formal_fork_source_lock` 仍未验证，local candidate 采用不代表正式源锁或 Release 通过。

能力、正式 Bind、完整独立 Review、恢复与安装／采用各自记录真实观察，任何一项不能替代其他项。截至本次整合，V3 的真实 fresh Agent 完整正式 Review、V5 的真实直接执行／历史处理和中性方法对照仍未验证；平台额外委托注入及内部 worker 无反馈底因仍未知。进行中的 call-local 对照不提前计入结果。不将源码、fixture 绿色或后续一次成功写为普遍 `root_cause_fixed`，不声明通用时间或 token 成本降幅。完整多平台 Release 矩阵与业务后端修复不在本次证据范围。
