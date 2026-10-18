# Delivery Creation 1.0

`judgment_mode=semantic`：正向行为 → AI Review Gate → 真实选择或副作用的当前对话确认 → recorder/validator → 单一 typed exit。两种 mode 使用相同前置。完整 Guru 安装、公共 Task schema 2.0/API 1.0、唯一 Task checkout 和当前整体 accepted scope 必须存在。

## 正向行为与判断

首次 D1 与后继 D2 在 Planning 写入前调用本 owner。读取 Task 整体需求、历史 Delivery、尚未分配范围和局部依赖；判断一个明确切片是否必要、独立可交付以及与整体责任的关系。局部 provider 缺口只阻塞该场景，不能阻塞已经确认必要且独立的工作。方案返工、base 演进或同 PR 更新保留原 Delivery，不能创建新 identity 掩盖旧结果。

`delivery_creation` 输入明确 TaskKey、task_ref、scope_ref、交付 profile、一次 continuation_id 与 create/recover_creation 动作。公共 scope_ref/profile 直接交上游 parser，不复制其 schema。创建时一次分配 UUID，然后在同 owner ignored checkpoint 写入该公共 operation 的最小恢复输入，再调用公共 create_delivery/select。它只创建 Delivery 及上游自己的 planning_root，不创建 Task、branch 或 worktree。

`delivery_selection` 输入明确 DeliveryKey 与 task_ref。AI 判断原切片适用并读取现状，真实不同current选择在本owner解决后，有 context 时保留官方 select 的明确切换语义。创建/原创建恢复遇到不同合法current或stale/error先停止，不能静默覆盖或先创建另一个空 Delivery。无 context 时原 projection 校验明确 key、当前 generation、C4 注册 checkout 与官方公共 record/profile/applicability，只返回调用期身份，不写 session。Selection 不产生 Planning pass、不改变公共阶段，也不要求新工作树。

创建新切片的 scope 判断、选择分歧与真实资源变化在 AI Gate 内解决。已授权同范围工作及正常恢复自动继续，不持久化用户确认或过程。

## 恢复与退出

创建成功但 selection/输出未完成时，从本 owner checkpoint 使用原 UUID 继续；不可从 inventory 唯一项猜身份。有 context 的 create/select 与输出校验完成后删除 checkpoint；此后 recover_creation 只从当前公共 session 明确 selection 恢复，同 Task generation、scope_ref、profile 必须相符。

无 context 时 `created` 返回相同最小 key/root，原 pending operation 保留供同 continuation 的输出丢失恢复。成功 initial Author 消费其 requirements_ready 后调用本 owner 的 `runtime/creation_result.py:retire_creation_result`，只传 task_ref/key；本端口复核官方当前关系、phase/scope/profile/原operation后退休匹配输入。Author 不读 private 格式，不保留消费或授权记录。缺原pending及适用明确selection时 recover_creation 停止；consumer完成后的接续使用实际public key，不能重新分配 UUID 或推导旧切片判断。

整个切片撤回先进入 Clarify；由实际当前阶段 owner 使用公共合法 stop 接口，保留 commit/PR/history 并自动 release selection。关闭 PR 与清理资源有其独立 owner/必要确认。Creation 不把停止当交付，不替 Task Completion 判断全部完成。

## 公共出口与唯一 consumer

- `created`：明确身份已建立并选中；最小 key、task_ref、上游 planning_root 交 `guru-delivery-planning-author-router`。首次与选择已有对象走同一出口。
- `scope_revision_required`：AI 判断整体 authority 必须澄清；明确 TaskKey/task_ref 交原 Clarify owner。
- `selection_required`：存在真实切片/身份选择；明确 TaskKey/task_ref 交 `guru-delivery-selection-router`，读取公共列表并完成真实选择后以明确 key 调本 owner，不由 script 或 inventory 唯一项选择。
- `blocked`：具体缺失事实或不支持版本，停止。

Owner result 只含当轮 typed_exit 与具体理由，供本 wrapper 消费，不形成新状态 authority。公共阶段、文件存在或 checkpoint 不能代替语义 Gate。新 graph 不接旧 Task-status 开发入口；旧安装以固定旧完整发行继续，公共 D2 与 Guru 私有迁移齐备才切换。

### Unsupported-profile correction in the original Creation interval

The Creation owner checks the actual workflow declaration's supported profiles
before allocating a UUID or writing a new pending operation. A schema-level
local_commit capability does not add it to Guru's declared pull_request profile.
A normal rejected older invocation may already have written an unsupported
pending operation. This same owner parses that exact operation, verifies the
same current Task/generation/scope and proves its explicit key has no public
Delivery; only then it retires the unapplied interval and processes a freshly
reviewed supported create input with the same continuation_id. The caller never
deletes a checkpoint or changes a token to hide this error. recover_creation
without either a valid pending operation or actual selected identity still
stops. If that key already exists publicly, preserve its identity and pending
input and recover the original slice; changing its profile is not correction.
