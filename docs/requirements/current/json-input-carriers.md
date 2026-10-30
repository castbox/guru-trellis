# JSON 输入载体

Identity：`RDT-REQ-JSON-INPUT`；来源为 [Issue #695](https://github.com/castbox/guru-trellis/issues/695) R1–R6/AC1–AC4。适用来源 revision 为 `8d746ce561c464ca28af4dc91adf085132e4098c`。本单元新增具体载体与读取行为，不替代 [R630-02](native-compatibility.md) 的原公开输入兼容条件。知识接受、实现通过和实际安装采用分别判断。

| Identity | 完整要求与正常边界 |
| --- | --- |
| R695-01 / BEH695-CARRIER | shared mixed reader 保留普通 UTF-8 文件优先、原 symlink-to-regular、合法 inline 和单 stdin。顶层必须为 object。明确拒绝非普通文件，包括 zsh 进程替换，给出原入口支持的普通文件/inline/单 stdin 替代；不读取任意设备或流。各命令原准入保持，package-local envelope-only 和 stdin-only 入口不因此增加 inline。 |
| R695-02 / BEH695-DIAGNOSTIC | 能可靠观察时区分明确路径不存在、读取或 UTF-8 失败、载体不支持、空输入、已读正文语法错误和可解析非 object。无法区分的 mixed 字符串保留歧义；绝对或本机 ./、../ 是明确路径，斜杠或后缀不单独构成证据。合法长 inline 不因路径探测失败失效。错误不回显 JSON、OS exception 或敏感路径。 |
| R695-03 / BEH695-BIND | Bind 在任一读取前拒绝 --input 和 --owner-result 同为 -，返回 conflicting_arguments、arguments.--owner-result、exit 2；恢复说明点名两参数并要求一个 -、另一份 inline/普通文件。两参数仍必填，正常双文件及 stdin+inline 调用可执行。原语义 gate、Task/session 身份与同 Task Delivery selection 保持。 |
| R695-04 / BEH695-CONTRACT | shared invalid_json 保留原 code、parameter field、exit 2 和原错误形状；通过 remediation 细分真实错误，不添加类别字段。读取成功后原 schema/身份/业务 owner 继续负责。commands/catalog/schema/help 与真实调用一致；无新成功 DTO、状态或 parser mode。 |
| R695-05 / BEH695-DISTRIBUTION | canonical、installed/dogfood 和实际声明平台通过原 preset/tools-only 机制保持一致。原 managed hash、用户内容和 sidecar 保护保持。源码改动不证明安装采用。验证为定向 package/runtime、真实 wrapper、source/installed、mode、drift/reapply、sidecar；不承担完整多平台升级或 Release 矩阵。 |

公共参数与调用合同由 [canonical companion spec](../../../trellis/presets/guru-team/spec/workflow/companion-scripts.md#json-carriers-and-already-read-content) 和 [Bind 调用](../../../trellis/skills/guru-team/packages/guru-bind-task-session/references/json-inputs.md) 拥有；本单元不复制 schema。具体设计见 [D695](../../design/current/json-input-carriers.md)，测试见 [T695](../../test/current/json-input-carriers.md)。本项不处理后续串行 Issues、业务现场 #961、FD/总 envelope、对抗输入、并发压力或额外安装矩阵。
