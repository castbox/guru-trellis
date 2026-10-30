# JSON 输入载体设计责任

Identity：`RDT-DES-JSON-INPUT`；需求由 [R695](../../requirements/current/json-input-carriers.md) 定义。适用来源为 `8d746ce561c464ca28af4dc91adf085132e4098c`；继承 `guru-trellis-architecture` 的原 runtime/package/distribution 边界。本项在既有确定性读取职责内直接修改，不建立第二状态或语义 authority。知识定义不证明实际实现或安装。

| Identity | Owner、输入、行为与输出 |
| --- | --- |
| D695-01 / CON695-READER | shared runtime/io.py 的 mixed reader 先处理单 stdin，再探测普通文件并保持文件优先；未定位普通文件时仍允许合法 inline。路径探测异常不能破坏合法长 inline。仅明确路径可报告缺失；其他失败按已知载体/读取事实或 mixed 歧义说明。非普通文件不打开读取。成功返回原 dict，失败使用原 CommandError，不增加持久化或协议。 |
| D695-02 / CON695-TEXT | shared 正文 decoder 直接检查已经读取的文本：空正文、语法、顶层 object。read_json、read_json_file 和 Publish/Merge/Finish stdin profile 预读复用它，已读内容不再次探测为路径。read_json_file 保留其 regular/non-symlink contract 检查；三个 wrapper 的后续 loader 和业务 profiles 保留。 |
| D695-03 / CON695-BIND | Bind package execute 在两个 shared read_json 调用前检查双 -。冲突属于参数层，使用原 conflicting_arguments、arguments.--owner-result、exit 2；不把两个必填参数声明为无条件 conflicts。原 Bind semantic owner 仍决定 profile、route 和充分性，runtime 保留原 schema、生命周期及 session/selection 校验。 |
| D695-04 / CON695-ERROR | 各真实 shared-reader consumer 拥有自身 commands/catalog/schema/help，准确声明其参数准入及 invalid_json 的读取/内容范围。原 field/status/形状保持，Bind 非法双 - 变化由 MIGRATION-695 显式说明。独立 envelope-only loader 不统一替换，stdin-only qualifiers 不放宽准入。 |
| D695-05 / CON695-INSTALL | canonical package/runtime 与 companion spec 是长期来源；原 tools-only/preset owner 生成 installed 和选定平台投影及 managed provenance，处理用户改动和 sidecar。不得手改 manifest/hash 或通过 archive 迁移绕开 preflight。官方 update 后仍沿 matching workflow/preset reapply，不 patch 上游或全局包。 |

完整实际消费者清单和诊断合同由 canonical reader 调用及 [companion spec](../../../trellis/presets/guru-team/spec/workflow/companion-scripts.md#json-carriers-and-already-read-content) 承载；[Bind 文档](../../../trellis/skills/guru-team/packages/guru-bind-task-session/references/json-inputs.md) 拥有完整正常两输入调用。该方案拒绝任意流支持，以避免引入无直接 consumer 的 descriptor/lifecycle 协议；成本限于原 helper、三个已读 consumer、Bind 与声明分发。若未来明确要求流支持或新增 consumer 准入，须返回原需求/方案 owner 重新判断。现有 [D630-02](native-compatibility.md) 的公开 inline/stdin 兼容保留；测试关系见 [T695](../../test/current/json-input-carriers.md)。
