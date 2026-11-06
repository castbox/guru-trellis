# D1 实施与分发观察

Canonical 已落实 JQ-R1—R6：Clarify 连续动作、Author 阶段/交接、共同验证方法、原 owner 独立问题推导、必要模板和 Phase2 引用，以及去敏 teaching source/process。没有 runtime、公共 schema 或生命周期接口改动。教学例子的就绪本地选择明确只有编辑器持有，后台 Future 另列；例子不是实际验收输入。

定向验证实际通过：source check-skill-packages（43 packages/128 commands）、planning-body distribution（1 test，187.180 秒）、review-sufficiency distribution（1 test，65.045 秒）、diff --check、变更 Python 内存编译及 Markdown 链接核对。两个 distribution 测试使用匹配 0.7.0-castbox.6 模板脚本和受管 Python，覆盖分发、reapply、用户内容保持及 sidecar。最初缺少上游脚本、system Python 缺 jsonschema 是装配失败，没有当作行为失败。测试后教学前提仅作文字精度修订，路径/分发机制不变，重读与链接检查适用；未重复全平台分发。

V1—V4 真实 Agent 观察见同目录 behavior-evals.md；它们与机械分发结论分开。

V6 原 guru-upgrade-tools 实际返回 tools_upgraded，installed_version=0.7.0-guru.7，recovery_ref=023b474c-078e-45d8-8bff-dbfe89ceee2b，unverified=[formal_fork_source_lock]。精确采用 GitHub 固定上游 3c37c75897f530c3ae8c5c4d85f6c1f3455b2e5f 的完整源并构建匹配 CLI/Core 0.7.0-castbox.6，local_candidate 同步本执行 checkout；上游受管脚本字节未回退。较早候选会删除已有 gitlink 修复，写前审查发现后未执行，重新选择已被基线采用的固定源。未更改其他上游 checkout 或全局安装。

实际目标自身 native/API 检查由原工具 owner 执行并成功，后续 public current 仍为相同 Task/Delivery，planning gate applicable。check-dogfood-overlay-drift 与 check-upstream-ownership 通过；canonical、dogfood 和当前选定 claude/codex/cursor 投影一致。Task/session 和 peer pointer 的保持由原 maintenance 检查；未更新业务仓库。

这些结果不证明正式 source lock、完整 Release 矩阵、真实业务安装或 QA 缺陷率改善。候选知识尚须原 candidate Check 后 final integration，最终 Check 尚未执行，不把本观察写作最终通过。
