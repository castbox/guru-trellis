# 独立审查执行条件与失败诊断

本次直接演进原 Architecture、Branch Review 和 Bind 的启动、诊断与接续方法。
保留原 session、Task 和结果 writer，不迁移公共结果模型，不新增 Skill、阶段、
审批状态、持久能力记录或第二恢复机制。

## 执行入口与最小范围

完整方法由原 [Review 合同](../../skills/guru-team/packages/guru-review-branch/references/contract.md#review-execution-conditions)
和 [Architecture 独立入口](../../skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md#independent-assessment-entry)
拥有。实际执行者在大规模读取前检查 native prelude 和必要执行事实；随后保持
authority-first 的独立语义顺序。合法候选 design/design_facts 在其原读取位置接入，
其他 Task 的历史通过既不是当前通过，也不一律是污染。

原 Review package 新增 `scripts/inspect-review-execution.sh`。它接受明确的
`--root`、`--task`、`--delivery-key`、`--purpose planning|branch_review`。
planning 必须提供 `--planning-purpose candidate_assessment|final_plan`；
branch_review 提供固定 `--base-ref` 和 `--head-ref`。
`--probe-writes` 仅执行原职责需要的唯一临时 create/write/rename/delete，
不触碰正式记录；没有探测不能宣称能力已验证。返回值是 intermediate receipt
中的操作事实，不是 typed exit、语义通过或未来写入保证。原 AI owner 解释事实，
正式调用仍校验自己的当前关系并处理实际失败。

正式 Bind/Selection 的位置为 Git common-dir 下 `trellis/sessions`。
正式 Review 还使用本 Task 的 `task.json` 及其同目录临时项，以及 checkout 内
原 Delivery-scoped `owner-checkpoints`；必要 call-local carrier 使用允许的临时目录。
候选源码、测试和文档保持职责只读。linked worktree 的默认 workspace 写范围
不能证明 common-dir 可写。启动者按实际载体补最小所需范围，并实际验证；
不将整个 `.git` 或 `danger-full-access` 作为永久配置。

`final_plan` 严格保留 #694 的完整显式对象只读例外：不执行 session/Task/checkpoint
写 probe，不因有 context 而恢复缺失绑定/选择。合法已有选择复用；不同选择、
损坏及真实错误保原 owner。该例外不扩展到其他 stage、Author、Approval 或 Activation。

## 诊断、直接执行与恢复

Bind 保留原 stdout、typed exit、reason_code 和 reason_refs。
`official_session_write_failed` 跨多个操作，不能仅凭名字判为权限错误。
原 adapter/runtime 对 projection 读取、旧 session 读取、写入和读回提供最小
stderr 技术信息：操作、匿名化位置、异常类别及可取得的 errno。如果官方读接口仍给出已知原因，stderr 的可选
`read_reason` 保留该值，用于区分读取失败与内容无效。底层官方 bool
接口已丢失 errno 时明确未知，不另做探测猜测原失败；不输出 raw exception message、
context key、payload、本机身份、凭证或业务内容。原 caller 可忽略新增 stderr，
也可用它定位原失败；它不是公共结果字段或新的状态 authority。

generic/CLI 已承担审查职责则直接执行，不再转派同一职责。启动者通过本次原句柄、
阶段事件和真实 blocker/result 有界定位无反馈；进程存活或等待时长不代表质量结果。
不能以无变化等待或循环换人代替诊断。无法满足独立性、实际未执行或缺结果时，
走原 blocked/re-entry；平台注入或内部 worker 底因未知时保持未知。

保留一次独立审查的 check → full_review 及前驱关系。同候选部分投影沿原 checkpoint
只补缺步；退休后丢输出沿原 public results 恢复。仍合规 reviewer 优先续接，采用
适用覆盖和工程事实；覆盖丢失实际补审，不能空写 pass 或无因重跑全套测试。

## 采用、知识与验证边界

由原 `guru-upgrade-tools` 从完整 matching source 更新 packages/runtime、workflow、
受管 Shared 和选定平台投影，保留 Task/Delivery/session 及用户修改。处理真实
`.new`/`.bak` 并验证 installed、drift、ownership 与恢复保持；普通 apply 的历史任务
阻塞不授权历史迁移、手改 manifest 或覆盖运行副本。旧在途操作在其完整 provider
完成或恢复，再采用新方法；不混装，不新增双 reader。

本次不改变全局跨 Skill 图；公共命令/schema 注册及源合同需成套采用。稳定发布仍
采用同一不可变版本的 workflow 与 preset，本地候选验证不是正式 Release。

知识组织沿现 current-knowledge 的完整单元、薄导航和历史追溯规则。不建立缓存、
路径剪枝、已读证明或逐 Task 共享登记。业务仓的大 README 由其原知识 owner 在
自己的合法边界迁移并验证，Guru 源仓不直接改写业务私有正文。

真实 linked-worktree 沙箱、完整独立 Review、普通恢复、Agent 行为和安装投影分别
报告实际观察。probe/Bind 成功、fixture 语义和 exit 0 均不能替代完整正式结果。
本项只承担受影响的定向分发和采用验证，不承担完整多平台升级或 Release 矩阵。
