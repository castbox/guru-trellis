# #630 测试策略与证据

状态：current。本单元拥有测试策略；实际执行、首失败与未验证边界由文末定位的贡献Test单写。需求、设计和追踪只定义行为、责任与关系，不复制实际结果。

| Identity | 入口与可观察结果 |
| --- | --- |
| T630-01 | 独立driver在原生三系统真实中文空格repo/注册worktree运行root/authority、file URI schema相对引用；Windows受影响基线命中具体差异、候选通过，Unix结果保持。 |
| T630-02 | 原targeted CI clean CLI init/preset安装；安装后的真实公开wrapper运行manifest成功与普通schema不完整两例，核对返回码/JSON；旧inline和新stdin均按公开合同工作。记录实际Git Bash而不是WSL。 |
| T630-03 | 真实解释器可见性和失败恢复：Unix仅python3、Windows显式命令/含空格路径、显式无效失败不fallback，日常wrapper只用activated runtime；bootstrap失败保留旧pointer/环境。 |
| T630-04 | Windows cp1252/PYTHONUTF8=0及三系统真实TaskCommit fixture：消息文件bytes、发布前读回与最终commit一致，真实hook修改仍被检测，index/tree检查不旁路。 |
| T630-05 | 正常Git LF/CRLF clone/checkout与真实apply/reapply/installed validation；声明文本稳定或精确恢复，真实编辑.new、原.bak及用户attributes块外保护，更深冲突不被忽略。不得伪造manifest/hash构造通过。 |
| T630-06 | 固定Fork .5 clean build及实际目标版本；新进程update、maintain tools_install→Guru reapply→入口，Windows上游py -3与Guru单executable分开；同provider --create-new预览/--force应用和同recovery_ref新进程recover/resume。 |
| T630-07 | driver file::selector、旧选择/错误和失败继续回归；canonical/dogfood/installed、ownership及受影响声明平台投影、reapply/drift和sidecar。安装缺陷不冒用unittest expected matcher。 |
| T630-08 | 原生Windows实际Codex正常会话自动加载Guru workflow/平台入口，完成所选版本hooks前提并正常调用一个Guru Skill；记录版本、命令和可观察结果。直接hook、wrapper和读文件只算脚本证据，不能替代会话。 |

实际执行、首失败、修复与未验证边界只由 [#630唯一Test](../../requirements-design-test-contributions/630-native-compatibility/test.md) 维护。知识晋升不能证明三系统产品、Windows实际Agent或正式发布完成。
