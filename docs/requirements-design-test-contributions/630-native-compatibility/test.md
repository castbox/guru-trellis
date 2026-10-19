# #630 测试策略与证据

状态：current，验证进行中。本文件拥有本贡献实际执行结果及未验证边界；requirements/design和traceability只定义行为、责任和关系，不复制结果为第二authority。

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

## 当前执行事实

- 原始run [39223843984](https://github.com/castbox/guru-trellis/actions/runs/39223843984)：driver/candidate 10da9be7、baseline 0543731。三系统driver通过；macOS/Linux clean安装及两wrapper cases通过；Windows原bare bash进入WSL导致JSONDecodeError，安装失败。该run是修复前证据，不是产品修复通过。
- 本轮固定Fork源码7f050fa11ddd8569e5db4f728ea1b745b7500a98已在独立干净workspace以pnpm10.32.1 frozen lock正常build，CLI/Core .5，marker等于源码HEAD。该事实只证明本机build；三系统Guru实际采用仍待验证。
- 产品源码与定向质量检查：CI driver 9例、原生runtime 6例、EOL完整5例、TaskCommit 15例、SyncBase 15例通过。source runtime.validate通过40 packages/124 commands；400个Python文件内存语法检查及diff whitespace检查通过。这些是本机macOS证据。
- macOS真实clean init、固定.5安装、新进程update、同provider workflow preview/force、tools prepare/preview/apply、同recovery_ref recover/resume、公开wrapper及实际hook脚本执行通过。用户AGENTS/config保留，零sidecar。脚本执行不替代实际Agent会话。
- 独立EOL比较：固定B正常clone命中normal_checkout_raw_drift，当前candidate通过。实际source-loaded tools-only upgrade将执行checkout更新为0.7.0-castbox.5；canonical/dogfood漂移检查通过。普通apply因历史归档Task旧schema触发upstream_delivery_migration_required，未迁移归档。tools-only reapply是本次实际维护路径。
- 既有test_install_assets_writes_installed_extension_manifest因旧artifact-contract名单缺少guru-maintain-legacy-task-input-archive_resume-1.0而失败；新增source metadata断言已通过。该项不记为通过，也不在本次改写无关名单。
- Unix使用受支持的python3命令名完成维护验证。上游在绝对TRELLIS_PYTHON_CMD重复维护时存在hook前缀重复限制，本任务未泛化修复该上游边界。
- 最终candidate的三系统CI、Windows实际Codex会话与官方Release仍待执行。未完成项不勾选，不能由本贡献晋升推导通过。

- 首次独立Phase2发现ARCH630-F1：三个RDT active .112入口误指旧.111。原owner修正为已存在的.112版本；逐层读取版本入口与native完整单元核对，历史.111页未改。正式Architecture须以修正后的新候选重新判断。

- 最终候选首轮 [39236746140](https://github.com/castbox/guru-trellis/actions/runs/39236746140) 绑定driver/target `2555e5e78583b06f900786fb19c1ee4a76e03917`。Ubuntu/macOS/Windows的独立runtime均6项通过、无failure/error/skip，包含真实root/worktree/schema/wrapper/TaskCommit。Windows Server2025 build26100、镜像20261007.264.1、Python3.12.10，utf8_mode=0/preferred_encoding=cp1252，Git2.56.0.windows.2，Git Bash来自C:/Program Files/Git/bin/bash.exe。
- 该轮三系统整体仍失败：BR630-F1把CLI更新提示首行误当版本（实际完整版本行是正确.5），BR630-F2平台CLI测试mock缺少真实text_attributes字段，11项中2个KeyError。clean安装尚未开始；Windows实际Codex commands=[]，因candidate未通过而诚实阻止。该轮不算安装、维护或Agent通过。
- 原owner修正版本输出的完整末行精确比较及mock协议；直接driver10项和platform inventory11项通过，三系统原始版本输出回放通过，raw logs未改。新candidate仍须原生安装/维护与实际Agent验收。用户更新目标为Issue630及Task闭环；正式软件发行是独立动作，现不执行，也不据本轮声明Release Gate通过。
