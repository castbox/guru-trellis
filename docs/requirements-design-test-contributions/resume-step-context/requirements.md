# 正常续接与实际出口查询需求

知识单元：`RDT-REQ-RESUME-CONTEXT`。检索别名：current context、delivery_current_task、current_context_ready、discover-skill-contract、--exit。语义 owner：`guru-maintain-requirements-design-test-ssot`。状态：proposed，尚未晋升，不表示实现、安装或验收通过。适用来源为 Git `26630149070e2988ad08102679931468b3535ef8` 的既有 RDT 和本 Task D1 当前批准计划；精确来源与拟晋升位置见同目录 `traceability.md`、`manifest.yaml`。

本单元定义新增的两项只读查询。Task 身份、Delivery 生命周期、接收者绑定和选择、完整合同读取及原恢复职责继续由 `docs/requirements/current/task-delivery-lifecycle.md` 的 R531、R657、R679、R694、R713 拥有；本单元不替代这些定义。对应设计为 `RDT-DES-RESUME-CONTEXT`，测试为 `RDT-TST-RESUME-CONTEXT`；三层同名目标文件均位于各自 `docs/<layer>/current/resume-step-context.md`，晋升前读取本贡献内同名层正文。

## RSC-R1 / RSC-BEH-CURRENT：查询自己的当前执行对象

调用者需要定位自身当前 Task 时，在原 `guru-ensure-task-checkout` 公共入口显式选择 `delivery_current_task` profile。查询复用上游公共 current 和原 Guru TaskId/generation、branch binding、ownership、唯一注册 checkout 及 live Task 校验，不建立第二 resolver，不从目录、inventory 或唯一候选猜选。

成功 `current_context_ready` 仅公开 `task_id`、`task_ref`、`lifecycle_generation`、`checkout_path`。有可用当前 Delivery 时，`current_delivery` 仅含 `delivery_key`、`phase`、`planning_root`，并核对属于同 Task/generation；没有 Delivery 则省略，不创建选择。不转发完整 results、candidate paths、历史或审计树。成功仅表示客观定位通过，不表示 Planning、Check 或其它语义阶段通过，也不授予写入资格。

## RSC-R2 / RSC-BEH-DIAGNOSTIC：无对象与真实错误保持区分

确认存在真实 context 且没有 Task 绑定时返回 `no_current_task`。无法取得 context key 时返回 `context_unavailable` 并保留原 `context_key_unavailable` 原因；二者交原 current checkout router 报告事实，不自动进入 Intake。不得删改环境变量、借用其它会话或从 checkout 路径补造 context。

已知 Task 的 binding、checkout、ownership、generation 或关系失配，保留原诊断和恢复 owner。原读取/API 错误保留实际 code、field_path 和 remediation，不按非零退出码统一改报无 Task。缺失由原 Identity、Bind、branch binding、checkout 或生命周期 owner 处理；本查询不绑定、不切换、不修复。恢复后由调用者重读当前事实。

## RSC-R3 / RSC-BEH-EXIT：查询实际出口的唯一 consumer

调用者已经取得真实 Skill/typed exit 时，在原 `discover-skill-contract.sh` 显式指定 `--skill <id> --exit <actual_exit>`。查询使用原 Interface 声明与 workflow marker 的共同解析结果，核对声明一致且映射唯一，返回 Skill/exit/consumer、该出口 output contract、consumer input/projection 及原入口定位。

Skill consumer 定位其原公开入口和输入合同；workflow/stop consumer 定位原 workflow target。存在动态 `profile_selector` 时保留原 selector，不提前求值或猜测目标 profile。未知出口、缺失或多重映射、Interface 与 marker 不一致均明确非零失败，不任选 consumer，不执行下一业务动作。原无 `--exit` discovery 行为保持。

## RSC-R4 / RSC-BEH-CONSUME：定位之后仍完整消费原合同

查询只提供定位。调用者随后完整读取当前适用入口条件、合同和必要依赖，按原 mandatory 顺序进入唯一 owner；不以摘要、固定行数摘录或 schema/example 代替完整行为。profile authoring 沿原命令 help，不另建 profile 导航、wrapper Skill 或路由表。原显式 `delivery_active_task` 输入、输出、错误和 consumer 保持兼容。

## RSC-R5 / RSC-BEH-BOUNDARY：状态、分发与证据边界

两项查询不改变 Task/Delivery、session、Git 或业务状态，不产生资源或绑定。原 managed Python launcher 可能刷新 ignored selection cache；应单列该设施事实，不宣称零落盘，也不借此重构 launcher。没有业务数据或数据库迁移、长期缓存、第二状态 authority 或账本。

新增合同只在 Guru canonical 维护，由原安装 owner 经受管工具同步，保留 Task/session、并行修改、mode 和 sidecar/冲突处理。source、package/runtime、installed、实际 Agent 及 Release 证据分别报告；本 D1 只要求命中验证和一次代表性安装投影，不扩大完整多平台矩阵。

上游 start/default get_context 不在本次修改范围。短原生比较使用同模型、输入、环境及共同 `26630149` 旅程方法，保留首次失败、合法非通过、不利观察、重复查询、装配错误、读取量和人工介入。准备 context/fixture、待测查询及 launcher cache 成本分列。旧 `43d8/unbound` 结果保留历史含义，不作新控制组或节省比例依据。查询、安装或机械通过均不能证明产品缺陷下降；实际效果待验证。
