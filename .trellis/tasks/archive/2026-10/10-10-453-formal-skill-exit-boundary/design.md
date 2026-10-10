# #453 设计候选

## 当前事实与对象
canonical：trellis/skills/guru-team/packages/、trellis/skills/guru-team/runtime/、trellis/skills/guru-team/schemas/。
安装副本：.trellis/guru-team/skills/packages/；平台 discovery projection 经 preset 生成。
当前 live inventory 有 34 semantic 与 2 deterministic package。清点从 interface.judgment_mode 出发，不以成功字符串或命令名称判定 Skill 类型。
runtime/command.py 是 package CLI stdout 的统一确定性 transport。现有 commands.json 的 stdout 均为 single_json_object，尚不能区分正式和中间结果。
Discovery/Wording 的 recorder 返回闭合 owner result；Plan Approval/Phase2/Delivery checker 返回 receipt；Create Task 与 branch-binding 的 atomic helper 复用 invoke.py 并返回 typed 形状。不能靠 runtime 文件名分类。
public scripts/invoke.sh 已是当前 Markdown 定义的正式出口边界；本设计落实该现有边界，不把语义判断交给 dispatcher。

## 选定机制
采用显式 command stdout 分类与中间 receipt envelope，保留内部 owner/checkpoint schema。
1. command metadata 新版本声明每条命令为 intermediate_receipt 或 single_typed_exit；由当前 package public invocation 声明及真实 wrapper 映射逐个审查，只有正式 wrapper 对应命令为后者。
2. dispatcher 仅对 intermediate command 的 stdout 序列化为新的闭合 receipt：schema_version=1.0、formal_exit=false、result=原完整 payload。新 schema identity 为 guru-intermediate-command-receipt-1.0；不增加 task/source/digest/owner/reviewer/授权字段。
3.正式 command 继续返回当前闭合 typed DTO，不包 envelope、不增加 formal_exit=true、不改变 positive/non-pass exit。dispatcher 不决定 route、不判 semantic pass。
4. receipt.result 是同 owner 的输入材料，由具名当前调用方执行固定薄 projection。它不是 downstream handoff；正式 workflow router 只消费实际 public invoke stdout。
5. package-local Python helper 的内部返回与 checkpoint bytes 不包 receipt；仅 CLI stdout transport 包装。因此 invoke 内部直接调用 record/check 不受影响。
6. atomic record/check/execute/recover 能力保留参数、动作和内部结果，只将对外中间 stdout 包装；需要正式接续时回到当前 public invoke。运行恢复仍按原 owner/profile 的条件，不能因为包 envelope 重执行副作用。

新 commands schema 使用 guru-team-skill-commands-1.1，与旧 1.0 有显式迁移说明。所有当前 command metadata 与当前 test fixture 同步迁移；旧 schema 只作历史身份，不建立旧 metadata runtime fallback。当前 validator、installer 与 dispatcher 使用新完整安装合同。

## 真实消费者与迁移
- CLI owner：record 输出的 result 投给当前 owner_result；check 输出的 result 中 validation_receipt 投给 invoke 的原字段，保持 digest/schema 意义。
- eval/native authoring：IntakeCommands 与所有读取本次中间 stdout 的当前 transport caller 接收真实 stdout 后先验证 receipt，再投影 result；trace 保留真实外层 stdout，不能把投影产物标成正式 invoke。
- integration tests 与 public CLI 文档：所有真实 subprocess 输出消费者按 command 类别作同一 projection；内部 helper unit tests 保持内部合同。
- executor/recovery caller：保留结果中原 resource/task identity 与恢复条件；不因 receipt marker 改 ownership 或重新执行已发生动作。
- downstream router：拒绝把 receipt 外层作为 formal DTO；只有实际 invoke 输出与 current interface declared exit/consumer 相符才接续。
- 外部旧安装：完整 reapply/受支持 upgrade 后同步 runtime、schemas、packages、平台 projection 和当前 CLI caller；调用示例明确旧 stdout 与新 envelope 的版本边界。混合安装沿现有安装校验阻塞，不增加永久 dual-read。
该方案是受控 direct evolution，不引入兼容例外、额外 legacy adapter 或双运行路径。public Skill input/output 不迁移。

## 为什么不是顶层逐处加字段
闭合 owner result 与 hash consumer 不能接收任意附加字段；逐 schema 修改会把 transport 标记混进语义结果，并引入持久化/hash变化。
共享 envelope 在一个确定性 stdout owner 下表达相同职责，原 result 仍由原 owner/schema 消费。新增三个字段由 CLI owner、schema validator 和 Agent 的即时接续直接消费，无新长期 artifact。

## 其他方案与取舍
仅改 status 文本不足以建立 schema/consumer 边界，且无法处理 recorder 的无 status owner object。
仅改 Markdown 不满足 #453 的 stdout/schema 要求。
为 public typed DTO 增加 marker 会改变所有 downstream public API，而正式入口已有完整声明；本设计只迁移 intermediate command stdout。
用程序自动判断 semantic pass 或阻止 Agent 思考越界违反当前 AI/脚本 owner 分层，本设计只做明确 metadata 分类的序列化和客观校验。
统一 envelope 会改变 CLI 中间结果读取方式，因此当前真实 callers 必须同步；不能以“新增字段”声称无迁移。真实 Agent 效果仍依赖行为验收。

## 正常场景与 failure 路径
完整 scope 包含 checker-only、record+check 尚未 invoke、正向 invoke、revision/blocked invoke、stale owner、schema/consumer mismatch、output-loss recovery。
checker-only 与 record+check 使用真实 owner 生成的合法材料；若所需 owner review 尚未执行，当前 Agent 完成审查再补链。未变更的已审查材料按当前 freshness 合同承接。
schema/identity/freshness/consumer mismatch 沿原 owner fail-closed/re-entry；同范围无副作用修正自动继续。真实 scope/authority 变化、Git/GitHub 副作用沿现有交互边界。
缺 native CLI/Agent capability 或行为证据时，报告具体 unverified/blocked，不用脚本 fixture、fake CLI 或 keyword pass 代替。
不增加 hostile-input 防御、锁、retry state、签名、审批 ledger、永久 receipt 文件或证明 Agent 身份的机制。

## 验证对象
高风险重点：guru-check-task、guru-approve-task-plan、guru-review-task-delivery、guru-review-change-request、guru-review-contract-wording、guru-publish-task-delivery；Branch Review 既有非正式语义继续成立。
客观层运行当前 package/runtime/consumer/schema 定向测试；实际 dispatcher 测试证明每种输出类别，不只验证 marker 字符串。
行为层在正常业务仓风格的隔离样例中运行真实 native Agent，使用合法生成的 checker-only 与 record+check 输出；Agent 不读取 expected exit/grading，也不获得预填 semantic pass。人工 AI owner 阅读完整 transcript、实际声明、wrapper receipts 和下一步动作后判定。
正向与非通过最终 route 分别验证；实际 public wrapper、无提前 downstream/重复确认是可观察事实，语义充分性由 AI 审查。
canonical apply、reapply、drift、声明平台投影、sidecar、一个代表性 clean install、旧完整安装迁移分别报告；软件 Release/完整多平台 matrix 不在本设计内。

## Authority 与维护
当前 constitution 为 docs/architecture/00-foundation/design-constitution.md；change contract 为 docs/architecture/06-governance/change-contract.md。
公共 CLI transport 的 before/after 与消费者迁移按 architecture_impact / target_native 承接，task-owned 设计合同见 [architecture-contribution.md](./architecture-contribution.md)，identity 为 architecture-453-intermediate-transport-v1。该文件是候选贡献，不是 baseline_current、审查 pass 或 shared current；独立 owner 决定当前出口。当前方案复用既有 owner 与 direct evolution 决策，未提出新增 ADR。
共享 current RDT/Architecture 不由并行 task 直接写；必要 contribution 由当前 owner 推进，晋升产生的新 diff 必须重新审查。
此 task writer 仅修改 #453 的 canonical 与其受控 projections/callers；#396/#250/#292 的实现不进入本候选。
