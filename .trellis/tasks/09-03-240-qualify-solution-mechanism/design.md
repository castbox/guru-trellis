# 设计：解决机制资格 Skill

## 1. 设计结论

新增 `guru-qualify-solution-mechanism`，声明 `judgment_mode=semantic`。它与现有 `guru-qualify-normal-scenario` 并列：场景 owner 先判断“问题是否有资格进入 scope/test/finding/implementation/publication”，机制 owner 再判断“拟采用机制是否可以承接该已资格化问题”。两个 owner 不共享语义结果，也不互相替代。

Skill 采用 `forward_behavior -> AI Review Gate -> conditional human confirmation -> recorder/validator -> typed exit`。正常路径不要求用户选择禁止机制；AI 直接返回 remove/replace。只有真实 scope 或副作用选择才进入对话。

## 2. 机制合同

### 2.1 禁止族

AI 必须沿调用图判断机制实际承接的 authority。命中以下任一族即为 `mechanism_revision_required`：

- OS advisory/mandatory lock：`flock`、`fcntl`、lock file、inode ownership；
- kernel/process identity：`/proc`、PID/PGID/SID、process tree、进程存活扫描；
- descriptor/process control：FD identity/inheritance、signal/kill/process-group control；
- 同类以 kernel、process 或 descriptor primitive 作为业务 authority 的封装或 shared implementation。

普通文件和目录操作只有在保存/读取普通 state、artifact、日志、cache 或配置时 qualified；若其存在性、inode、FD 或打开状态参与业务互斥、fencing、leader election 或 authority，则禁止。

### 2.2 允许族

具体方案不由 Skill 硬编码。AI 在 current requirement、architecture、dependency/caller graph 和终态语义基础上判断，例如数据库事务/唯一约束/durable state machine、明确 controller protocol、run-scoped identity/cancellation request、消息/任务/工作流系统的正式状态与控制 API。

## 3. Public I/O

输入是一个 profile-specific candidate set，包含固定 caller、target identity、candidate refs 和每个 candidate 的 live locators；不接受 severity、预设 decision、关键词扫描结果、worker report、授权文本或旧资格结果。

输出采用四个独立 typed exit：

| Exit | Consumer |
| --- | --- |
| `qualified` | 原调用方继续其自身阶段判断 |
| `mechanism_revision_required` | 原调用方删除/替换机制后 fresh 重跑 |
| `blocked` | workflow stop |

其中 `qualified` 可承载“机制 qualified”或“候选被拒绝/不适用”的最小结果，但不得预先决定 caller 的 severity、implementation route 或 publication readiness。若现有 graph 对 qualified 语义已有 `qualified_application_mechanism`，保持该稳定命名并让 serializer 映射为一个明确 exit；不引入一个总 artifact 冒充全部 exit。

## 4. 接入点

在 global workflow 中增加稳定 invoke/exit marker 和唯一 target：

1. task-free 首次写入与机制演化；
2. planning approval 的关键机制/新架构依赖；
3. implementation 中发现或引入 planning 外机制；
4. Phase 2 当前完整实现依赖机制集合；
5. Branch Review 完整 diff 中新增、升级或暴露为合同的机制；
6. Publication Review 将进入公开合同、部署、运行或验证结论的机制。

调用方负责 candidate set，Skill 只负责机制语义；worker/checker/reviewer 只能返回 candidate，不得自行判定资格、severity 或 route。

## 5. 分发与验证

canonical package 位于 `trellis/skills/guru-team/packages/`，由 registry 和 extension manifest 管理，preset apply 同步到 `.agents/.codex/.claude/.cursor` 以及 dogfood runtime。workflow 与三个平台入口只保留路由，不复制 contract、AI gate、recorder/checker 或 private state。

测试分为：package contract/runtime、workflow graph/projection、preset source/installed parity、dogfood drift/reapply/sidecar、真实 wrapper paired eval。普通 Issue 只跑本范围的定向验证；完整多平台 throwaway/upgrade/release matrix 留给专门 owner。

## 6. 风险与取舍

- 机制“看起来安全”但实际由 OS identity 承 authority：通过真实 caller/dependency graph 的 semantic reread 识别，不能靠字符串扫描。
- 一个候选同时包含合格场景和违规机制：场景资格保持独立，机制仅返回 remove/replace。
- 业务仓库已有违规实现：保留报告边界，不跨仓库改动，避免本 Issue 变成迁移总任务。
- 现有 21-package/89-exit 图谱和多平台投影规模较大：复用现有 package/runtime/manifest substrate，新增资产必须成套同步，禁止局部激活。
