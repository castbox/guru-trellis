# #630 三系统运行与安装一致性需求增量

状态：proposed；适用基线 RDT current-main-0.7.0-guru.111 / Architecture .102。来源为 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的行为1–6、CI证据责任及十项验收。当前完整定义的拟承接单元为 native-compatibility；不替代Task/Delivery、Completion、知识维护或其他未迁移定义。

| Identity | 完整行为与边界 |
| --- | --- |
| R630-01 / BEH630-01 | macOS/Linux/原生Windows支持中文空格repo和已注册worktree；按本机Path语义识别同一root，保留真实不同checkout身份；本地file URI正确解析盘符、中文空格与schema相对引用。 |
| R630-02 / BEH630-02 | Python→原生Bash→activated managed Python保持路径和JSON语义，明确Git for Windows Bash实际来源及执行；公开inline与stdin形式保持既有支持。Guru UTF8文件/JSON/提交消息及Git协议明确编码，真实错误不被忽略或掩盖。 |
| R630-03 / BEH630-03 | 安装/维护使用既有单executable --python合同，显式失败不fallback；Unix仅python3和Windows命令/含空格路径可用。日常wrapper只用activated hash-locked runtime。激活前失败保留旧pointer和可用环境。上游py -3命令串由固定Fork原生owner解析，不成为Guru executable。 |
| R630-04 / BEH630-04 | Guru-owned声明文本从canonical到安装/正常checkout具有明确LF策略。仅精确CRLF→LF匹配canonical或有效previous-managed字节身份时恢复；原raw installed hash校验保持。binary/lock/精确身份排除，用户真实编辑与attributes块外内容保留，unknown仍.new并阻塞，既有升级.bak规则保持。 |
| R630-05 / BEH630-05 | 自有修复来自canonical并同步dogfood/声明投影，正常apply/reapply及固定Fork .5 update/tools_install后仍生效；不得patch上游trellis-*资产。source lock、实际build、目标安装身份和新进程维护证据分别核对。 |
| R630-06 / BEH630-06 | 复用#631定向CI，以独立driver/target和受影响baseline证明具体失败及候选通过；真实三系统安装/脚本、Windows非UTF8中文提交、正常LF/CRLF及解释器可见性分层记录。不放宽matcher接纳任意安装失败。Windows实际Codex自动加载workflow/平台入口和正常Skill调用单独必需，直接hook/静态投影不可替代；缺项阻塞Task最终完成与正式发行。 |

上述要求不增加全Agent×全OS/全部installer历史组合、hostile输入、竞态/锁或额外fault-injection义务。规范性安装细则分别归canonical installer/upstream-ownership；本单元定义其必要行为与边界，不复制公共Skill接口。知识晋升、实现验证、Task Completion及软件Release分开判断。
