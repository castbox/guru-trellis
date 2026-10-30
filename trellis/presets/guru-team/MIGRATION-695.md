# #695：JSON 输入载体与 Bind 双输入

共享 reader 保留普通 UTF-8 文件优先、原 symlink-to-regular、inline JSON、单 stdin
及顶层 object 要求。明确拒绝非普通文件载体，包括 zsh `<(...)` 进程替换。
改用普通文件、原入口支持的 inline，或 `-` 接收一份 stdin。

## 输入范围和诊断

这不是所有 CLI 的统一输入协议。共享 reader 的真实参数继承读取诊断；
package-local envelope-only loader 不增加 inline，三个 qualification owners
保持 stdin-only。Publish/Merge/Finish 的 stdin profile 预读直接解码已读正文，
下游原 loader、业务 profile 和语义门禁保持原职责。

`invalid_json` 继续包含读取、载体、空输入、语法和非 object 失败。原 parameter
field、exit 2 和三字段共享错误对象保持。remediation 按可观察事实说明纠正方式，
不回显正文、敏感路径或 OS 异常。明确绝对、`./`、`../` 路径可诊断文件不存在；
裸相对名与非法 inline 的剩余歧义保留，不按斜杠或后缀猜测。合法长 inline 不因
文件探测错误失效。读取成功后继续原 schema 和身份校验。

Bind 原无效调用 `--input - --owner-result -` 现在在读取前返回
`conflicting_arguments`、`field_path=arguments.--owner-result`、exit 2，
取代此前第二次读取的 `invalid_json/owner_result`。消费该无效调用错误的脚本须
按新 code/field 处理，不能把它称为 JSON 语法错误。两参数仍各自必填，合法双输入
继续支持。完整两文件及 stdin+inline 命令由
[Bind 调用文档](../../skills/guru-team/packages/guru-bind-task-session/references/json-inputs.md)
唯一维护；调用前仍须真实 Identity/Ensure、当前 session 与原 owner 语义审查。

## 采用和维护

采用完整匹配版本的 shared runtime、受影响 packages/commands/catalog/schema 和
managed companion spec。不要只 patch 已安装的 `io.py` 或平台副本。canonical 来源
经原 preset/tools-only owner 同步 `.trellis/guru-team/`、共享和实际选定平台；保留
Task、Delivery selection、session、private controls、用户内容及原解释器合同。
本项不新增 DTO、状态、FD 协议或兼容 adapter，也不改变 workflow graph。

官方 update/upgrade 后沿原 marketplace workflow 预览/显式应用及 matching preset
reapply 恢复。原 `.new/.bak` 和用户修改保护继续有效。若 plain apply 被历史数据
preflight 阻止，如实报告并沿原 tools-only owner 处理；不得 bypass、手改 manifest/hash
或迁移无关 archive。具体 tools-only 写集由原 owner 在执行前审查。

采用验证区分源码、定向单元、实际 wrapper、installed/声明平台 bytes/mode、reapply、
drift 和递归 sidecar。源码修复不代表已有安装采用，也不证明业务 #961 现场修复、
实际各平台 Agent 行为或完整升级/Release 矩阵；后者继续由专门 Issue 承担。
