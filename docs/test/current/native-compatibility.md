# #630 测试策略与证据

状态：current。本单元拥有测试策略；实际执行、首失败与未验证边界由文末定位的贡献Test单写。需求、设计和追踪只定义行为、责任与关系，不复制实际结果。

| Identity | 入口与可观察结果 |
| --- | --- |
| T630-01 | 独立driver在原生三系统真实中文空格repo/注册worktree运行root/authority、file URI schema相对引用；Windows受影响基线命中具体差异、候选通过，Unix结果保持。 |
| T630-02 | 原targeted CI clean CLI init/preset安装；安装后的真实公开wrapper运行manifest成功与普通schema不完整两例，核对返回码/JSON；旧inline和新stdin均按公开合同工作。记录实际Git Bash而不是WSL。 |
| T630-03 | 真实解释器可见性和失败恢复：Unix仅python3、Windows显式命令/含空格路径、显式无效失败不fallback，日常wrapper只用activated runtime；bootstrap失败保留旧pointer/环境。 |
| T630-04 | Windows cp1252/PYTHONUTF8=0及三系统真实TaskCommit fixture：消息文件bytes、发布前读回与最终commit一致，真实hook修改仍被检测，index/tree检查不旁路。 |
| T630-05 | 正常Git LF/CRLF clone/checkout与真实apply/reapply/installed validation；声明文本稳定或精确恢复，真实编辑.new、原.bak及用户attributes块外保护，更深冲突不被忽略。不得伪造manifest/hash构造通过。 |
| T630-06 | 按当前source lock核对固定Fork clean build及实际目标版本（#630 当时的 .5 观察保留在原Test；本轮 .6 采用见T687-01..05）；新进程update、maintain tools_install→Guru reapply→入口，Windows上游py -3与Guru单executable分开；同provider --create-new预览/--force应用和同recovery_ref新进程recover/resume。 |
| T630-07 | driver file::selector、旧选择/错误和失败继续回归；canonical/dogfood/installed、ownership及受影响声明平台投影、reapply/drift和sidecar。安装缺陷不冒用unittest expected matcher。 |
| T630-08 | withdrawn：原Windows真实Codex会话验收义务已撤销；旧定义及已有失败只作历史观察，不重新赋予Python测试含义。当前必需脚本能力由T630-01..07覆盖。 |

实际执行、首失败、修复与未验证边界只由 [#630唯一Test](../../requirements-design-test-contributions/630-native-compatibility/test.md) 维护。知识晋升不证明实际执行；脚本验收不宣称Windows实际Agent或正式发布完成。

本单元修订：`630-script-validation-2026-10-20`。当前验收以 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的脚本范围为准。前驱定义见 [cf07d082固定正文](https://github.com/castbox/guru-trellis/blob/cf07d082c046b8e5e3c5050a603f22285821b215/docs/test/current/native-compatibility.md)；其真实Agent会话义务仅在该历史版本成立。本次直接修订当前完整单元，不改历史贡献或全局RDT版本入口。

## T687：当前 .6 采用的定向策略

适用完整前驱为 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea:docs/test/current/native-compatibility.md`。本策略承接 R687-01..03 / D687-01..03 和原 R630-03/05、D630-05 的有效条件，不将 #630 的旧执行重标为本轮结果。

| Identity | 入口与可观察结果 |
| --- | --- |
| T687-01 → R687-01/D687-01 | 核对真实 .6 merge/parents/tree/main CI、Release 四附件 SHA256 和 CLI 精确 Core 依赖；所选 Fork 正常 build 与 canonical lock 匹配。上游 CI、附件、源码 build 与本轮目标安装分别报告。 |
| T687-02 → R687-01/D687-01 | canonical/installed source lock、manifest target/requires/tested、原精确版本检查与当前说明一致；已发布 Guru .6 的历史 .5 配对保持。 |
| T687-03 → R687-02/D687-02 | 一个隔离已有目标运行原 source_locked preview/prepare/invoke，取得真实 tools_upgraded、unverified=[]；目标 API/字节/mode 匹配，Task/session/用户内容/peer 在前后比较中保持。干净本地来源快照只证明本地匹配采用，不冒充远端 marketplace 安装或 Guru 发布。 |
| T687-04 → R687-03/D687-03 | 在实际维护后的 installed Core/Python 公开 stop 分别处理合法历史 manual/local_commit；核 stopped、peer/history、selection 合法释放、匹配重试及空 evidence 拒绝，无 Completion/Closure。样本由原合法路径形成，不手改业务 Task 或扩大 workflow profiles。原 R657-03/D657-03/T657-05 仍拥有整体 stop/release 原则。 |
| T687-05 → R687-02/D687-02 | 运行受影响维护/source-contract 回归、source/installed、ownership、reapply/drift 与递归 sidecar 检查；保留原严格 source/build/API、字节/mode 及用户内容规则。 |

本轮实际执行、首失败与未验证边界仅由 [#687 Test](../../requirements-design-test-contributions/687-adopt-castbox6/test.md) 维护；原 [#630 Test](../../requirements-design-test-contributions/630-native-compatibility/test.md) 的环境、旧失败和观察截止保持。新 Guru 软件 Release、完整累计平台矩阵、真实业务升级、实际 Agent 会话和原 Backend 收尾未由本策略声称已验证。知识 promotion 不代替实际安装或任何正式生命周期结果。
