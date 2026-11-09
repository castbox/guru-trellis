# D1 实施与分发观察

Canonical 已落实 JQ-R1—R6：Clarify 连续动作、Author 阶段/交接、共同验证方法、原 owner 独立问题推导、必要模板和 Phase2 引用，以及去敏 teaching source/process。没有 runtime、公共 schema 或生命周期接口改动。教学例子的就绪本地选择明确只有编辑器持有，后台 Future 另列；例子不是实际验收输入。

定向验证实际通过：source check-skill-packages（43 packages/128 commands）、planning-body distribution（1 test，187.180 秒）、review-sufficiency distribution（1 test，65.045 秒）、diff --check、变更 Python 内存编译及 Markdown 链接核对。两个 distribution 测试使用匹配 0.7.0-castbox.6 模板脚本和受管 Python，覆盖分发、reapply、用户内容保持及 sidecar。最初缺少上游脚本、system Python 缺 jsonschema 是装配失败，没有当作行为失败。测试后教学前提仅作文字精度修订，路径/分发机制不变，重读与链接检查适用；未重复全平台分发。

V1—V4 真实 Agent 观察见同目录 behavior-evals.md；它们与机械分发结论分开。

V6 原 guru-upgrade-tools 实际返回 tools_upgraded，installed_version=0.7.0-guru.7，recovery_ref=023b474c-078e-45d8-8bff-dbfe89ceee2b，unverified=[formal_fork_source_lock]。精确采用 GitHub 固定上游 3c37c75897f530c3ae8c5c4d85f6c1f3455b2e5f 的完整源并构建匹配 CLI/Core 0.7.0-castbox.6，local_candidate 同步本执行 checkout；上游受管脚本字节未回退。较早候选会删除已有 gitlink 修复，写前审查发现后未执行，重新选择已被基线采用的固定源。未更改其他上游 checkout 或全局安装。

实际目标自身 native/API 检查由原工具 owner 执行并成功，后续 public current 仍为相同 Task/Delivery，planning gate applicable。check-dogfood-overlay-drift 与 check-upstream-ownership 通过；canonical、dogfood 和当前选定 claude/codex/cursor 投影一致。Task/session 和 peer pointer 的保持由原 maintenance 检查；未更新业务仓库。

这些结果不证明正式 source lock、完整 Release 矩阵、真实业务安装或 QA 缺陷率改善。候选知识尚须原 candidate Check 后 final integration，最终 Check 尚未执行，不把本观察写作最终通过。


## 本轮三方法文件修订及受管采用（追加）

本轮只修改 Clarify contract、Author planning-body 和 journey/process 三个 canonical 方法文件，沿原 upgrade-tools 生成受管投影。改动具体化最终结果反推、原承诺正向核对、未决分支依赖和适用方法单元完整加载；没有新增 runtime/schema/DTO/阶段或通用 reviewer。教学来源只有文本内容，最终保存例子采用“文本内容与已确认附件一致”，没有为教学 source 新增标题字段；原业务 V1 的标题/附件要求保持。

实际定向结果：Author 合同2项测试通过（`/tmp/guru-747-revision/author-contract.log`）；Clarify 合同21项通过（`clarify-contract-managed.log`）；planning-body 分发1项通过，178.488秒（`planning-distribution-managed.log`），覆盖匹配 preset 安装/reapply、声明投影和用户文件保持。review-sufficiency 方法本轮未变，原验证仍适用，没有为阶段变化重复运行其分发测试。这些机械检查只证明各自结构、合同和分发边界，不能证明 E2 的规划语义遗漏消失。

首轮设施失败保留：`planning-distribution.log` 缺匹配 reviewed scripts 环境，`current.log` 的 system Python 缺 jsonschema，`source-validation.json` 返回 runtime_dependency_missing；Clarify 初轮缺 PYTHONPATH。随后修复设施并使用匹配受管入口，未改变业务断言，也没有将设施失败计作目标产品失败。

原 tools owner 实际返回 tools_upgraded，installed_version=0.7.0-guru.7，recovery_ref=b0a2660c-aade-496f-a6bd-9fe161259592，unverified=[formal_fork_source_lock]，实际输出为 `/tmp/guru-747-revision/tools/result.json`。`dogfood-drift.log` 与 `upstream-ownership.log` 均为 ok，canonical 与本 checkout 当前选定投影一致。local_candidate 仍不证明正式 source lock、完整 Release 矩阵、业务仓库采用或真实 QA 改善。

本轮原 A/B、E1 和 E2 结论由 behavior-evals.md 的追加部分承接：没有全面改善结论，candidate 的恢复承诺收窄和双方合同衔接缺口仍存在。结构测试和工具同步不能覆盖这些语义失败。RDT/Architecture 的真实知识维护、最终 Check/Review/Delivery/Completion 由原职责的后继实际结果建立；本报告不预填“全部通过”，也不将旧 V1—V6 结果改写成本轮修订结果。

本轮截至报告写入：方法实现、受管同步与上述结构验证已取得通过事实，E2 未证明整体收益。RDT 三份拟写仍为 proposed，尚未晋升；未执行本轮正式 candidate/final Check，没有新 commit 或 PR。历史首个实现提交 H=7b14b6f83f274bd3b08e2721be8624516374b73d 保持，当前修订未提交。工具通过不等于交付完成。


## 本轮条件等价与同对象连接方法落实（追加）

当前同 Task/generation/Delivery 在 implementing，Identity/Ensure 和本接收会话 current selection 已实际核对。原 implementation_discovery 的 Normal/Solution 均返回 classified、qualified_current，Root 返回 classified、not_incident_applicable，由 guru-resume-implementation 消费。该差额具体落实原接受设计中的 JQ-R2 交接与 JQ-R5 独立关系覆盖，没有新增 owner、状态、接口或持久化边界；未人为重开 Planning 或借用旧 readiness 返工。

只修改 canonical Author planning-body §2/3/5 和 canonical review-sufficiency 的 Form and cross-check coverage 原段：来源条件与具体场景作反例核对，新增前置或收窄结果须原来源处置；同对象内容、身份、版本和持有方沿产出、交接、读取到可见结果推演；缺合同具体列依赖和原补齐职责，不编造能力。没有将仓储答案写入通用方法，也没有新表、台账、阶段或公共schema。修改前完整 provider 和两文件原字节已冻结，2545份hash读回一致；源码 diff --check 通过。

定向分发实际通过：planning-body 1项，188.819秒（`/tmp/guru-747-continuity/planning-distribution.log`）；review-sufficiency 1项，61.889秒（同目录 `review-distribution.log`）。原 tools owner 实际返回 tools_upgraded，installed_version=0.7.0-guru.7，recovery_ref=58f70fca-83da-46e9-a125-38c099f03743，unverified=[formal_fork_source_lock]（`tools/result.json`）；`dogfood-drift.log` 与 `upstream-ownership.log` 均 ok。这些事实支持本次结构、受管分发及当前 checkout 采用，不证明正式 source lock、完整Release、业务采用或方法效果。

本轮两次原 native review 均在材料读取前因模型 provider 错误终止，行为比较不可评价，具体事实由 behavior-evals.md 本轮追加部分承接。原 E2 的 candidate 收窄及双方合同缺口结论保持。本轮未执行正式 Check、知识晋升、commit 或 publish，不能把方法候选实现及分发通过写成方法验证通过或交付完成。


## 本轮 design 展开时机的最小差额与结构事实

live Identity、Ensure、current 均核对同 Task/generation/Delivery，实际仍 implementing，Planning applicable。fresh implementation_discovery 候选 design-entry-complete-path 的 Normal/Solution 返回 classified、qualified_current，Root 返回 classified、not_incident_applicable，按 guru-resume-implementation 继续同范围工作，没有重开 Planning。

V3 已有条件反例和同对象推演，本轮没有重复添加规则。唯一 canonical 差额为 Author planning-body §3 原 design 展开句：开始 design 时先由关键行为条件/可见结果推演，再细化接口、状态和顺序；既说明不匹配结果不可采用，也说明新内容如何取得匹配结果到成功终点。不新增表、台账、身份/版本协议或领域答案。before V3 provider 的2545文件hash已冻结并读回，源码 diff --check 通过。

本轮 planning-body 分发1项实际通过，185.210秒（`/tmp/guru-747-design-entry/planning-distribution.log`）。原 tools owner 实际返回 tools_upgraded，installed_version=0.7.0-guru.7，recovery_ref=12839009-d9bb-47a9-8633-d14a5bec47fd，unverified=[formal_fork_source_lock]（同目录 `tools/result.json`）；dogfood-drift.log 与 upstream-ownership.log 均 ok。只证明当前方法资产的结构/分发及本 checkout 采用，不证明正式 source lock、完整 Release 或业务采用。

此前 attempt2 的成功 review 观察和本次维修预约 V3/V4 作者首稿结果已追加 behavior-evals.md；旧启动失败不被覆盖。本次双方七类承诺充分，没有全面优胜，V4 异步接纳只支持局部更具体。原 E2 问题及所有历史限界保持，不能用新领域结果冲销旧失败。当前未执行新的正式 Check、知识晋升、commit 或 publish；方法候选实现、分发与有界观察不能提升为整体交付完成。
