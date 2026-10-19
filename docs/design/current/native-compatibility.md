# #630 三系统兼容设计责任增量

状态：current；继承RDT .111、Architecture .102及本Task已审设计；实现/采用状态与知识接受分开。需求由[当前需求](../../requirements/current/native-compatibility.md)单写，测试关系由[追踪](../../requirements-design-test-contributions/630-native-compatibility/traceability.md)定位。

| Identity | 原owner、输入→行为→输出及边界 |
| --- | --- |
| D630-01 | shared runtime base_selection拥有Git root/authority/worktree事实读取，以本机Path比较并按Git UTF8协议读结果；schema owner按标准本地file URI转换读取相对引用，不新增远端schema能力。 |
| D630-02 | bootstrap capability owner选择并验证原生Bash，使用POSIX路径与--invocation -的同JSON stdin进入现有公开wrapper；只调整内部fixture，公开inline输入保留。Python激活owner继续先probe/真实wrapper/staged installed validation后激活，失败保留旧pointer。 |
| D630-03 | TaskCommit原executor按UTF8候选字节写入、读回与验证最终commit，继续真实hook、transaction index/tree/live ref检查。index物化参数仅在正常fixture证明必要后采用；不通过旁路提交绕过这些检查。 |
| D630-04 | installer原owner维护canonical和target scoped attributes及文本copy/generate；bounded block保留用户块外字节，更深规则冲突明确失败。精确EOL恢复仅限声明文本与已知受管来源，恢复后原raw validator验实际字节；不增加第二manifest/hash authority。完整细则由canonical spec/preset/installer.md、upstream-ownership.md及本Task必要ADR拥有。 |
| D630-05 | 来源owner固定castbox/Trellis #53交付commit/.5，按该源码声明pnpm frozen lock正常workspace build及marker验证；原native update/maintain/workflow/recovery接口采用该实际build后Guru reapply。Guru不管理上游entry。 |
| D630-06 | 原CI driver负责目标隔离/环境/执行事实，target负责产品实现；诊断观察目标已声明cases与其真实transport，supplemental保持同target transport且保留首失败。原expected unittest matcher及安装失败状态不弱化。实际验收使用命令行Python脚本及公开wrapper，工程脚本不生成AI语义结果。已交付的windows_codex_session入口保留为维护者显式诊断工具；其独立配置、正常启动及真实结果单独报告，不成为本Task必需验收。 |

没有公共Skill/exit/Task数据模型变更，没有业务DB迁移。受管文本LF/恢复改变原raw-only更新判定的窄条件，由原Architecture独立Phase2和晋升合同承接；其他原owner不变。具体实现、验证与采用状态以真实候选/测试证据为准，本单元的知识接受不证明实现或采用已完成。

本单元修订：`630-script-validation-2026-10-20`。当前验收以 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的脚本范围为准。前驱定义见 [cf07d082固定正文](https://github.com/castbox/guru-trellis/blob/cf07d082c046b8e5e3c5050a603f22285821b215/docs/design/current/native-compatibility.md)；其真实Agent会话义务仅在该历史版本成立。本次直接修订当前完整单元，不改历史贡献或全局RDT版本入口。
