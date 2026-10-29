# #630 三系统兼容设计责任增量

状态：current；继承RDT .111、Architecture .102及本Task已审设计；实现/采用状态与知识接受分开。需求由[当前需求](../../requirements/current/native-compatibility.md)单写，测试关系由[追踪](../../requirements-design-test-contributions/630-native-compatibility/traceability.md)定位。

| Identity | 原owner、输入→行为→输出及边界 |
| --- | --- |
| D630-01 | shared runtime base_selection拥有Git root/authority/worktree事实读取，以本机Path比较并按Git UTF8协议读结果；schema owner按标准本地file URI转换读取相对引用，不新增远端schema能力。 |
| D630-02 | bootstrap capability owner选择并验证原生Bash，使用POSIX路径与--invocation -的同JSON stdin进入现有公开wrapper；只调整内部fixture，公开inline输入保留。Python激活owner继续先probe/真实wrapper/staged installed validation后激活，失败保留旧pointer。 |
| D630-03 | TaskCommit原executor按UTF8候选字节写入、读回与验证最终commit，继续真实hook、transaction index/tree/live ref检查。index物化参数仅在正常fixture证明必要后采用；不通过旁路提交绕过这些检查。 |
| D630-04 | installer原owner维护canonical和target scoped attributes及文本copy/generate；bounded block保留用户块外字节，更深规则冲突明确失败。精确EOL恢复仅限声明文本与已知受管来源，恢复后原raw validator验实际字节；不增加第二manifest/hash authority。完整细则由canonical spec/preset/installer.md、upstream-ownership.md及本Task必要ADR拥有。 |
| D630-05 | 来源owner按唯一canonical source lock选择当前固定Fork（#630 当时为castbox/Trellis #53交付commit/.5，本轮采用关系见D687-01）；按所选源码声明pnpm frozen lock正常workspace build及marker验证；原native update/maintain/workflow/recovery接口采用该实际build后Guru reapply。Guru不管理上游entry。 |
| D630-06 | 原CI driver负责目标隔离/环境/执行事实，target负责产品实现；诊断观察目标已声明cases与其真实transport，supplemental保持同target transport且保留首失败。原expected unittest matcher及安装失败状态不弱化。实际验收使用命令行Python脚本及公开wrapper，工程脚本不生成AI语义结果。已交付的windows_codex_session入口保留为维护者显式诊断工具；其独立配置、正常启动及真实结果单独报告，不成为本Task必需验收。 |

没有公共Skill/exit/Task数据模型变更，没有业务DB迁移。受管文本LF/恢复改变原raw-only更新判定的窄条件，由原Architecture独立Phase2和晋升合同承接；其他原owner不变。具体实现、验证与采用状态以真实候选/测试证据为准，本单元的知识接受不证明实现或采用已完成。

本单元修订：`630-script-validation-2026-10-20`。当前验收以 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的脚本范围为准。前驱定义见 [cf07d082固定正文](https://github.com/castbox/guru-trellis/blob/cf07d082c046b8e5e3c5050a603f22285821b215/docs/design/current/native-compatibility.md)；其真实Agent会话义务仅在该历史版本成立。本次直接修订当前完整单元，不改历史贡献或全局RDT版本入口。

## #687 当前固定来源采用责任

适用完整前驱为 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea:docs/design/current/native-compatibility.md`。本节承接[当前需求](../../requirements/current/native-compatibility.md) R687-01..03；公开 Architecture identity 及原 source/installer/maintenance owners 不变。

| Identity | 原 owner、输入→行为→输出及边界 |
| --- | --- |
| D687-01 / CON687-SOURCE | 原 source owner 通过唯一 canonical trellis-source.json 采用 `17015f987166f4106034f115d23212446f16d536` / `0.7.0-castbox.6`，同步原 manifest 与精确版本检查及受管 source 投影。正常同源 Core→CLI build 和原 marker 验证保持；历史 .5 来源和已发布 Guru .6 配对不回写。 |
| D687-02 / CON687-TOOLS | 原 guru-upgrade-tools 的 install/source_locked 消费完整、干净、匹配 source/build，沿原 preview→prepare→invoke 执行 tools-only 维护并使用原恢复入口。public maintenance owner 更新官方工具；原 preset 更新 Guru 资产。实际目标 API/字节/mode 与 Task/session/用户内容/peer 保留分别核对；不新增 Guru converter 或来源协议。 |
| D687-03 / CON687-STOP | stop 由所选固定 Fork Core 和匹配 Python 实现。Guru 保持 PR-only 声明及原阶段 owner，通过已安装公开入口消费合法保留的 manual/local_commit 与所需 evidence，核对 stopped、selection、peer/history 和匹配 retry；不修改上游生成资产或以 stop 生成 Completion/Closure。原 D657-03 的生命周期分工保持。 |

测试策略由[当前 Test](../../test/current/native-compatibility.md) T687-01..05 定义，实际采用观察由 [#687 Test](../../requirements-design-test-contributions/687-adopt-castbox6/test.md) 拥有。#630 原 .5 构建及三系统观察保持历史身份。本轮无新 API、持久化字段、Task 数据迁移或 ADR；原严格 source_locked、mode、所有权、解释器、用户编辑和恢复条件保持。
