# #812：显式 Task/Delivery 资格输入迁移

## 版本与直接演进

固定前驱为 `f16bb562e4ea844939786cebd5c6c20e686914b2` 的完整 Guru provider。
本次三个 qualifier 的七类 Task/Delivery profile 从 input 1.0 直接演进到
独立 path/id 的 input 2.0，aggregate 从 2.0 演进为 3.0。新 target 必填 opaque
`delivery_key`；原 public schema、aggregate 和公开输入示例字节保留作历史验证资产。
Interface、runtime selector、当前受控输入和 caller 同批切换。四类非 Delivery
profile、输出、枚举及唯一 consumer 不变。

新 runtime 不提供旧输入双读、缺字段推断或兼容 wrapper。调用方必须从原
Identity/Ensure/Bind/Delivery Selection 或 current 取得真实完整 key；无 context
时复用原显式对象校验，有 context 时保持官方当前选择匹配。不能从 inventory、
路径、摘要或邻近字段补身份。没有 Task/Delivery 数据格式迁移或新绑定存储。

## 已完成、待调用与在途恢复

- 已完成的旧资格结论在原 applicability 仍适用时采用；它不成为当前阶段完成或
  当前 runtime pass。阶段变化本身不重跑语义。
- 尚未调用的旧输入由原 caller 重读同一真实对象并重装当前 input 2.0。旧形状
  在 current schema 处拒绝；缺失或冲突身份交原 owner，不能从 ambient state 猜补。
- 原 provider 下未完成的 recorder/checker/invoke 操作，在完整固定旧 provider
  恢复。不要把旧 process-local bytes 输入新 runtime；不要重复已发生副作用。
  恢复后若需新的资格调用，原 caller 读取当前 authority/applicability 并重新装配。
- classified、机制修订、诊断及阻塞继续原出口/consumer。调用期原对象和阶段
  由 caller 内存持有，不新增资格 ledger、checkpoint 或 public output 字段。

## 安装采用与回退

已有 checkout 通过 `guru-upgrade-tools` 从完整 canonical source 执行
preview、prepare、原语义 Gate 和精确冻结更新；保 Task、generation、Delivery、
planning_root、session、peer、配置和 common runtime pointer。不要手抄受管副本，
也不要用普通 apply 绕过旧 Task 阻塞。逐项处理真实 sidecar，执行定向 source /
installed / 平台投影与 drift 检查。安装一致不代替真实 qualifier/caller 行为验收。

原工具 owner 仅按同 frozen plan 与实际 preimage 恢复或回退工具文件；先核对
原 Task/session 和运行合同兼容。已推进的公共生命周期不通过 Git reset 或
工具回退倒退。需要恢复旧在途操作时使用完整固定旧 provider，不能混装新旧
package/runtime/caller。历史记录和已完成 Delivery 保持原样。

本迁移不声明完整多平台升级、Throwaway 或 Release 矩阵已通过；普通任务执行
本 accepted scope 所需的定向验证。
