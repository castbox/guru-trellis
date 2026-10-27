# #679 验证结果

本文件记录当前实际观察；尚未执行或完成的项目明确保留缺口，不预填通过。完整测试策略见 [test proposed target](proposed/docs/test/current/task-delivery-lifecycle.md)，相对引用按最终目标 `docs/test/current/task-delivery-lifecycle.md` 解释。

## 已观察的 package / fixture

- Author 完整 suite 21 项通过；包含接收者状态、原 Bind/Selection 接续、已有方案、五 Planning consumer、真实 scope/phase/generation 变化与 no-context，以及前置安装/API错误保留。
- Approval 完整 suite 31 项通过；包含从 canonical Human artifacts 文案提取 argv 的真实执行，selected/missing、Task-only不创建/选择、正常公共 closeout及官方 archive 后的实际 ref/key 解析。
- Creation 有/无 context 原 chain 2 项通过；保留 #548 transport，不能代替未绑定原生接收。
- Readiness package 26 项、ReadinessAdapterTests 9 项通过。公开 recipe 两 mode × 两 profile 实际执行，standalone 错 request_id 真实拒绝后完整重建到 ready；fixture语义结果不是原生 Agent 验收。
- Architecture 首次完整 suite 44/46；两项失败来自原测试：全仓 byte snapshot 纳入 Git 派生临时缓存，以及旧精确 eval 清单未包含现有三个合法 native 场景。两项必要适配已由原 owner 资格并修正，定向两项 4.383 秒通过；其余 44 项执行事实经当前适用性核定后采用，没有冒称重新执行完整 suite。
- 独立 Trellis quality 另执行 364 个 Python AST、两个错误目录 JSON、`git diff --check`、dogfood drift、49 个受改 package 投影 bytes/mode 以及 workflow/eval parity，均通过；此方法结果不记录正式生命周期 Gate。

## 首失败与恢复边界

原 Readiness fixture 缺当前 managed runtime public-wrapper 所需 selector package，setup 首先返回 `managed_runtime_check_failed / jsonschema`；只补原拷贝集合的 `guru-select-workflow-mode` 后 suite 通过，没有修改 runtime 或依赖。

原 Approval 断言把整个 Interface 当成仅四个业务出口；现有独立 `legacy_controls_retired` 使 suite 误报。原测试已承接当前出口，Interface/业务出口未改。Author 的早期 API 错误原先被统一 task_ref 诊断掩盖，现保原条件；相应 unit 只证明错误边界。

修复前真实原生接收在同一隔离 Task/D1、初始无当前绑定下，Author 首次返回 `stale_identity / delivery_key`（exit 3）。随后原 Bind 实际返回 `binding_blocked / official_session_write_failed`；当前 workspace-write 未覆盖 linked worktree 的 Git common-dir。此为原生环境限制，不能计作修复后成功。原始输出保留于本仓 ignored validation runtime；未改环境身份或手写 session。

## 安装与待完成证据

代表 clean 样本由 source-lock Fork `79a97ed60fe19e8f287eaddfa74722b5250ced35` 的 built CLI `0.7.0-castbox.5` 初始化，并按当前 README 的本地 workflow sample 方式加载 canonical 正文、安装完整 Codex preset，原 installer 返回 `status=ok`。CLI 不接受本地目录作为 marketplace provider；该被拒调用不是远端 marketplace 安装通过。

dogfood 普通 apply 在原历史归档 current-schema precondition处停止。随后原 `guru-upgrade-tools` tools-only 同操作成功返回 `tools_upgraded`，公共 Trellis 文件内容差额为空，当前三个平台的 Guru 投影匹配；Task/归档与 common-dir/trellis 控制状态共 2829 文件的复合内容在维护前后完全保持。模式为 local_candidate，正式输出仍列 `formal_fork_source_lock` 未验证，不把本地 dirty source 当成正式发布来源。dogfood drift、source/installed/ownership 检查均通过。

代表 linked target 的 matching apply 首次因 PATH 解释器锁定 wheel 安装失败停止；明确复用原 clean 安装实际采用的 managed 解释器后，安装返回已知 managed 更新的 33 份 `.bak`。逐项核 backup 等于 B 来源、目标等于当前 canonical，再移到 ignored validation/native-backups 保留；重跑原 reapply 返回 `status=ok`、installed validation passed、zero sidecars。未编辑 lock、依赖或安装 manifest。

## 实际原生结果

修复后的主接收会话初始为 `no_current_task`，其 prompt 只提供对象、来源、目标和边界，没有恢复步骤或 expected pass。Agent 自行执行原 Identity→Ensure→Bind→Selection，重读同 key/planning，再原 Author `delivery_initial_review` 正式返回 `requirements_ready`（exit 0）。其工具沙箱只额外加入该隔离 linked checkout 的 Git common-dir 可写范围，没有预绑定/预选或修改 context 身份。独立 quality owner 已核原始命令、stdout 与提示。

R3 真实回放使用 `mode=workflow / target.kind=standalone_request`。执行的 AI owners 在隔离源上实际完成 Sync→Discovery→Clarify→Wording，通过原 wrappers 得到真实 producer；初始错误 consumer 实际 record 返回 `stale_identity / target.request_id`（exit 3）。之后原 native runner 启动的 Agent 独立重审十维、完整重建 consumer，经真实 record/check/invoke 全部 exit 0 到 `ready`，再读取唯一下一 owner `guru-create-task` 入口后停止。source/producer/业务源字节前后保持，未用 fixture semantic builders 充当 producer。重复查询使用受控样本 provider，此结果不证明 GitHub live duplicate 状态。

fresh Architecture 原生样本已完成：先读实际 authority/constitution/change contract，再读真实 Author 输出和候选；它自身初始 no_current_task，经原 Identity/Ensure/Bind 后 no_current_delivery，再原 Selection 到同 key/planning，正式 invoke 返回 `baseline_current / candidate_assessment / no_architecture_impact`（exit 0）。实际消费既有 requirements_ready，继续原未完候选评估，没有重跑 initial Author。driver 对比确认 Task record、切片 PRD、Git refs/worktree 均保持；独立 quality owner另核实际 transcript和首读顺序。首次 Bind 普通缺 owner-result 参数被拒后，由该 Agent补完整原调用，未借用其他会话或绕过 writer。

这两条 R1 原生轨迹覆盖初始接收和已有 Author 进度的后继恢复；后段 plan_ready→新 Wording/Approval→新 Activation由 package chain证明，没有冒称为额外原生模式。原生实际样本在本仓 ignored validation/native-checkout 中，R3 在 validation/readiness-native；仓库贡献只保必要结果，不复制工具 transcript。

当前剩余正式 candidate Check、shared-current final_integration及final Check；结果由对应原 owner实际产生，本记录不预填。本文也不提供 Task完成、业务采用、完整多平台Release/Upgrade、生产或远端发布证明。
