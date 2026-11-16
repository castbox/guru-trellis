# #861 当前 schema 登记修正

## 当前选择与历史文件

extension manifest 的 `public_input_schema_ids` 与 active Skill Interface 当前公开
JSON 输入集合保持一致。本次移除 11 项旧版本的独立登记；历史 schema 文件、路径、
id 和字节保留，当前 runtime selector 与 typed outputs 不变。

| 原独立登记 | 当前选择 | 原迁移合同 |
| --- | --- | --- |
| Create Task aggregate 1.0、Delivery task-creation profile 1.0（2 项） | aggregate 2.0、profile 2.0 | [MIGRATION-813](MIGRATION-813.md) |
| Root Cause aggregate 2.0、七类 Delivery profile 1.0（8 项） | aggregate 3.0、七类 profile 2.0 | [MIGRATION-812](MIGRATION-812.md) |
| Sync current input 2.0（1 项） | Interface 的 scalar CLI；call-local current input 3.0 | [MIGRATION-819](MIGRATION-819.md) |

七类 Root Cause profile 是 author、base-impact、branch-review、implementation-discovery、
phase2、planning-scenario 和 publication。其它仍被当前 Interface 选择的 profile
保持登记。Interface 1.9 的 conversation 包不贡献 JSON input/output schema；
安装验收分别按合同类型取集合，并对 JSON 输入与输出保持精确相等检查。

退出独立登记不表示删除引用。Sync current input 3.0 仍明确引用 current input 2.0
的原普通/资格确认分支；该文件继续服务当前调用，不能删除分支或替换其字节。
历史文件存在也不表示当前 executor 接受旧独立调用。

## 当前与在途调用

新调用采用完整 matching provider 及当前 Interface，由各原 owner 完成必要语义判断。
尚未执行的旧输入回原 owner 按上述迁移合同重新装配，不能把旧 schema id 当作当前
独立入口，也不增加版本探测、兼容 parser 或 fallback。

已完成操作的旧结果或丢失 stdout，使用实际执行时的完整固定 provider，沿原
check/recover 恢复同一对象。保留原 Task/generation/Delivery 和 session 身份，活动
Task 由当前 Identity/Ensure/session/Delivery 及实际阶段续接；不重复创建资源，不将
旧成功结果转换成新 gate。具体前驱、恢复和退出条件仍由上述原迁移文档独占。

## 安装采用与证据边界

新安装经原 preset installer；已有活动 Task 的 checkout 通过原 `guru-upgrade-tools`
采用完整 matching source，保留 Task/session 与用户内容。逐项处理原 owner 的
`.new`/`.bak`，再核 installed manifest、完整平台投影、文件 mode 和 reapply/drift。
本迁移文档是源码导航，不加入受管安装清单。

source/fixture、throwaway 安装、正式 source-locked 工具采用和 Release 验收分别报告。
开发 checkout 的旧 installed provenance 不因源码修复自动成为当前采用证据；正式
工具采用与后续 Release 矩阵须由原 owner 在实际交付的完整 source 上执行。
