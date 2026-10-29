# #630 三系统运行与安装一致性需求增量

状态：current；适用基线 RDT current-main-0.7.0-guru.111 / Architecture .102。来源为 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的行为1–6、CI证据责任及十项验收。当前完整定义单元为 native-compatibility；不替代Task/Delivery、Completion、知识维护或其他未迁移定义。

| Identity | 完整行为与边界 |
| --- | --- |
| R630-01 / BEH630-01 | macOS/Linux/原生Windows支持中文空格repo和已注册worktree；按本机Path语义识别同一root，保留真实不同checkout身份；本地file URI正确解析盘符、中文空格与schema相对引用。 |
| R630-02 / BEH630-02 | Python→原生Bash→activated managed Python保持路径和JSON语义，明确Git for Windows Bash实际来源及执行；公开inline与stdin形式保持既有支持。Guru UTF8文件/JSON/提交消息及Git协议明确编码，真实错误不被忽略或掩盖。 |
| R630-03 / BEH630-03 | 安装/维护使用既有单executable --python合同，显式失败不fallback；Unix仅python3和Windows命令/含空格路径可用。日常wrapper只用activated hash-locked runtime。激活前失败保留旧pointer和可用环境。上游py -3命令串由固定Fork原生owner解析，不成为Guru executable。 |
| R630-04 / BEH630-04 | Guru-owned声明文本从canonical到安装/正常checkout具有明确LF策略。仅精确CRLF→LF匹配canonical或有效previous-managed字节身份时恢复；原raw installed hash校验保持。binary/lock/精确身份排除，用户真实编辑与attributes块外内容保留，unknown仍.new并阻塞，既有升级.bak规则保持。 |
| R630-05 / BEH630-05 | 自有修复来自canonical并同步dogfood/声明投影，正常apply/reapply及当前固定Fork update/tools_install后仍生效（#630 的 .5 来源观察保持历史身份；本轮 .6 采用要求见 R687-01..03）；不得patch上游trellis-*资产。source lock、实际build、目标安装身份和新进程维护证据分别核对。 |
| R630-06 / BEH630-06 | 复用#631定向CI，以独立driver/target和受影响baseline证明具体失败及候选通过；真实三系统安装/脚本、Windows非UTF8中文提交、正常LF/CRLF及解释器可见性分层记录。不放宽matcher接纳任意安装失败。验收聚焦命令行Python runtime、目录相关脚本和实际公开wrapper；三系统均不要求真实Codex或其他Agent会话，不要求OpenAI账号、模型推理或GPU。脚本结果不声明实际Agent会话成功；已有会话失败不阻塞本Task完成。 |

上述要求不增加全Agent×全OS/全部installer历史组合、hostile输入、竞态/锁或额外fault-injection义务。规范性安装细则分别归canonical installer/upstream-ownership；本单元定义其必要行为与边界，不复制公共Skill接口。知识晋升、实现验证、Task Completion及软件Release分开判断。

本单元修订：`630-script-validation-2026-10-20`。当前验收以 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的脚本范围为准。前驱定义见 [cf07d082固定正文](https://github.com/castbox/guru-trellis/blob/cf07d082c046b8e5e3c5050a603f22285821b215/docs/requirements/current/native-compatibility.md)；其真实Agent会话义务仅在该历史版本成立。本次直接修订当前完整单元，不改历史贡献或全局RDT版本入口。

## #687 当前固定来源采用

本节来源为 [Issue #687](https://github.com/castbox/guru-trellis/issues/687)。适用完整前驱为 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea:docs/requirements/current/native-compatibility.md`。本节只接续当前来源采用关系；上文 #630 义务与其历史 .5 观察保持原义。

| Identity | 完整行为与边界 |
| --- | --- |
| R687-01 / BEH687-SOURCE | 当前 Guru 来源采用锁定 castbox/Trellis `17015f987166f4106034f115d23212446f16d536` / CLI-Core `0.7.0-castbox.6`。canonical source lock、受管投影和当前公开版本映射一致；核对真实 merge parents/tree/main CI、Release 四附件与 CLI 精确 Core 依赖。同版本号不代替来源身份；已发布 Guru .6 的历史 .5 配对不改写。 |
| R687-02 / BEH687-TOOLS | 原 tools-only owner 至少在一个隔离已有目标完成真实 source_locked 采用。完整、干净、匹配 Guru/Fork source/build、API、字节和 mode 校验继续生效；Task/session、用户内容和 peer 保留。来源不匹配时沿原合同阻止写入，普通失败仍用原恢复入口；来源锁更新不等于目标已安装。 |
| R687-03 / BEH687-STOP | 当前 workflow 仅支持 pull_request 时，原阶段 owner 仍可通过已安装公开 Core/Python stop 撤回合法保留的 manual/local_commit。原 owner、阶段、evidence 和匹配重试约束保持；peer/history 保留，selection 合法释放。stop 不新增不支持 profile 的创建能力，不表示 delivered、Task Completion 或 Closure。 |

本轮来源采用以定向 source/installed、ownership、reapply/drift、sidecar 和实际安装回归验证；它不重新承担 #630 全部三系统验收。设计和测试分别由[同一当前设计](../../design/current/native-compatibility.md)、[同一当前测试](../../test/current/native-compatibility.md)定义，实际观察由 [#687 Test](../../requirements-design-test-contributions/687-adopt-castbox6/test.md) 单写。原生命周期 [R657-03](task-delivery-lifecycle.md) 保持；完整累计矩阵、Guru 软件 Release、真实业务升级和原 Backend 收尾保持独立范围。
