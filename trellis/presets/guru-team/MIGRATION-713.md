# 公开执行合同与匹配采用

本迁移直接演进 #713 固定范围内的原 owner。采用时，公共合同、原执行器、
workflow consumer、共享 runtime、示例及声明平台必须通过原 installer 或
`guru-upgrade-tools` 成套切换。源码变更不证明目标已采用。

## 保留的调用与新增承接

现有 Skill、profile、typed exit、command 和 schema id 保留。当前 source 的
Issue/no_issue 定义、当前 profile 导航、authoring 与完整结果用途、实际输入载体
及三字段错误合同由各原 package 声明。既有合法结果和同 owner 恢复保持原义。

原 Candidate 构造命令复用原 `content_base/candidate`。AI 仍选择范围、固定 B
和 paths；原 Delivery operation 拥有阶段转换。公开构造不替代原 candidate
引用入口，也不新增 Git-free Delivery 支持。Planning freshness 与 qualification
file-set identity 的公开配方只说明各自现有算法，不互换 token 或提供语义判断。

| 原入口与直接 consumer | 匹配采用后的精确行为 |
| --- | --- |
| Closure `--input` / `--semantic-result` → 原 Closure invocation | 两个参数保持现有 regular UTF-8 JSON object 文件路径域。公开说明和 help 明确文件载体，并将 metadata 的 `stdin` 校正为 `none`。inline JSON 与 `-` 原本不属于成功调用域；本次只收敛文案与 metadata，不改变 profiles、action set、ResultRef 或原恢复语义。 |
| C4 `discover-candidates.sh` → Closure `binding_ref` | 当原 resolver 返回 `already_established` 时，现有中间 receipt 的 `result.binding_ref` 公开 TaskId、generation、实际 `binding_revision`。Closure 原样消费三字段。未建立时不提供引用；`binding_established` typed output 不扩展，建立、ownership 和恢复校验不改义。 |
| Check `planning_stale` → 原 Author `delivery_approval_revision` | 旧非空 `proposal_refs` 分支保持。仅 `planning_route=reapprove_plan` 且无 scope decisions 时，新增 `proposal_refs:[]` 与非空 `revision_actions`；动作原样承接 Check AI 在既有 `reason` 中给出的具体修订要求。workflow 复制 TaskRef、DeliveryKey 和 actions，并补当前 mode/固定 profile。无 scope 变化不得制造 scope proposal。 |
| Check 输出 → 原 Delivery operation | 先构造并校验完整公开输出，再执行原 `rework/record_gate`。普通输出形状错误不先改变阶段。AI 仍拥有 finding、scope、动作和 route 判断。 |
| legacy `finalize --review-input` → 原维护 owner | 公开现有 `native_argv`、按 profile 需要的 `next_owner_argv`、`observations` 和 `output`。原 observe receipt 的 `result.result` 是 observations；不是 receipt 本身。缺必需字段在重跑命令前具体诊断。保留 history/task 两种成功形状、额外 caller 字段、双层 receipt 及原观察、route、identity 比较。 |

新的 no-scope Check 分支必须与 producer output schema、workflow consumer schema、
router 和 Author 导航一起采用。旧 consumer 不接受它时，不能只 patch producer。
原非空 refs 成功 payload 不增加字段。Check 正常 recorder 仍是 #710 的 11 字段
语义输入；完整 6.0 结果继续由原 checker/invocation 消费，不新增第十二个字段。

Publication 在原 public entry 解析 JSON 参数，再把已解析对象薄传原 schema、plan
和执行流程；私有 Task、transaction、Gate 与 recovery 文件读取保持原域。公共参数的
inline JSON、常规 UTF-8 文件或 stdin 只解析一次，profile 选择不耗尽后续调用的 stdin。
原文件调用与参数相对路径继续支持，非法载体给具体输入诊断。

六个 legacy intermediate 的初次公开输入使用既有公共 JSON reader。
Publish/Merge/Finish 恢复固定 B 已明示的 inline/file/stdin 承诺；
Approval/Check/Branch Review 是本次明确的 additive 表示收敛，不能宣称已有历史
inline 成功证据。旧文件优先、相对路径、symlink 文件与 stdin 成功域保持，原
schema、execute、正式 retirement loader 和私有 plan/recovery 读取不变。
Maintain legacy 自身仍按声明的文件或 stdin 输入，不扩大其通用私有读取域。

Discovery 执行 AI 先核 Sync transition 与原 Git 公开事实；record/check 的原 observer
在语义 Gate 后重读并派生观察。该说明不增加 observer API 或 pre-task artifact。
本地文本 draft 的来源捕获例只说明一种合法选择，保留其它合法 capture、实际 producer
identity 及 Issue binding；不建立唯一新摘要投影或用示例值补当前输入。

## 原结果、恢复与旧完整安装

旧完整安装可以固定在原合同。切换前先由实际原 owner 判断尚未完成的 operation；
保留它的原 recovery identity、输入与结果。不得读取另一 owner 的 private checkpoint
补造 handoff，也不得猜 binding revision 或重算旧 Gate 摘要来延长结论。

已发生 rework 后的输出失败不是一次未执行操作。先读取原 Delivery 当前阶段和
结果，再由实际当前 owner 判断合法接续；不得为了补新输出重复旧 transition 或
手改 Task。新的语义轮次使用当前输入和原 owner。原失败和修订后新 run 分别保留。

采用不迁移业务数据或无关历史 Task，不增加新持久状态、第二 parser 或权限记录。
Task/session、用户内容、模式、template hashes、`.new/.bak` 由原安装 owner 保护。
普通 apply 的历史数据阻塞不授权绕过、手拷受管副本或扩大迁移。

## 验证边界

分别验证原输入/输出和 consumer、错误发生前的副作用边界、旧成功 payload 与恢复、
canonical/dogfood/受影响平台、matching 安装、reapply/drift/sidecar/mode，以及实际
native 行为。新公开示例是调用资料，不是当前 Gate 或通过证据。

本说明不是验证报告。受控 Git/provider 不能证明真实 GitHub、部署或业务采用；
local candidate 不证明 formal source lock。完整 Upgrade/Release 多平台矩阵仍由
专门 owner 承担，当前未验证项必须在实际结果中保留。
