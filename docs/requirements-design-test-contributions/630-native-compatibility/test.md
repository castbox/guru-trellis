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

## 历史执行快照

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


## 固定候选的原生验收

[候选执行 39240156056](https://github.com/castbox/guru-trellis/actions/runs/39240156056) 与[独立基线对照 39240160455](https://github.com/castbox/guru-trellis/actions/runs/39240160455) 的 driver/candidate 均为 `c6b620db9f9d90b26d201542e89f8da8bca8744f`；后者 baseline 为 `0543731bf52aa80842fde5db47332380de513cf0`。三个 artifact 以 `targeted-{ubuntu-24.04,macos-15,windows-2025}-<run>-1` 命名，保存环境、实际 argv/cwd、返回码、source lock 和原始输出。以下结果来自下载后核读的各 `candidate/result.json`、installed wrapper 及维护日志，不由 Actions 总状态推导。

| 原生环境 | 本候选实际观察 |
| --- | --- |
| Ubuntu 24.04，Python 3.12.15，Git 2.55，/usr/bin/bash | inventory 11、runtime 6、真实 EOL 1 均通过，无 failure/error/skip；clean 安装及全部维护阶段返回 0。 |
| macOS 15，arm64，Python 3.12.10，Git 2.55，/bin/bash | 同上；真实 wrapper 两例为 0/2，并保持原 JSON。 |
| Windows Server 2025 build 26100，镜像 20261007.264.1，Python 3.12.10，Git 2.56.0.windows.2 | 同上；UTF8 mode 0、preferred encoding cp1252，Bash 为 C:/Program Files/Git/bin/bash.exe。root/worktree、含中文和空格的 schema 相对引用、真实 TaskCommit UTF8 消息及 hook 修改检测均通过。 |

三系统均沿固定 Fork `7f050fa11ddd8569e5db4f728ea1b745b7500a98` / CLI-Core `0.7.0-castbox.5` 正常 build/init/apply，随后在新进程执行 update、同 provider/template 的 workflow create-new 预览和 force 应用、tools_install prepare/preview/apply、原 recovery_ref recover/resume、Guru reapply、installed validation、wrapper 及原生 hook。各实际步骤返回 0；wrapper 的普通 schema 不完整输入保持 2。Windows 另有原生 `py -3` probe，Guru 安装仍使用单一 executable 路径，二者未混用。日志记录实际目标版本和依赖身份，不仅修改 source lock。

Windows baseline 的 root 入口实际拒绝合法 root（unsafe_path）；file URI 相对引用为 child%20schema.json unresolved；TaskCommit 在 cp1252 读回报 charmap decode；公开 fixture 的 bare bash 返回 WSL 未安装发行版并使 preset 安装失败。候选在相同原生环境通过对应入口。Ubuntu/macOS baseline 在正常 autocrlf=true clone 中出现受管文本 CRLF/raw drift，候选通过；旧 native fixture 另有 JSONDecodeError，保留其实际错误，不额外推断根因。基线任意安装错误未被 expected matcher 接纳，对照 run 整体保持红色、comparison.established=false；candidate 结果为 passed。

本机最终补充检查：官方 upstream projection 对固定 .5/source 通过 201 文件及 9 项测试；driver 10、platform inventory 11 通过。旧 installer artifact-contract 名单失败与其 baseline 一致，仍单列未通过；不据定向结果声明全仓、全部历史组合或累计 Release Gate 通过。

## 两个参考提交的最终处置

以下处置对应 Issue 中的 C1 `4319b9e4`、C2 `0b3c3c28`，不整包复制业务仓库工具修改。证据为上节的实际原生 artifact 及对应直接回归。

| 来源修改 | 最终处置、代码与证据 |
| --- | --- |
| C1：76 个 python3→python 命令/提示替换 | 保持现有等价能力，不批量替换。沿已有显式解释器与 activated runtime 合同；native interpreter visibility、Windows executable/py -3 维护入口通过。 |
| C1：Git root/authority 路径及文本读取 | 吸收行为，以[原 base owner](../../../trellis/skills/guru-team/runtime/base_selection.py)的本机 Path/UTF8 直接演进；Windows B 合法 root 被拒，候选真实 root/worktree 通过。 |
| C1：Bash/path/JSON fixture | 替代为[原 bootstrap check](../../../trellis/skills/guru-team/runtime/bootstrap_check.py)及[同职责 transport](../../../trellis/skills/guru-team/runtime/bootstrap_transport.py)的 verified Git Bash/POSIX path/UTF8 stdin；保留公开 inline。B 命中 WSL，候选真实两例及 inline/stdin 等价回归通过。 |
| C1：正式 active pointer 的 POSIX 写入 | 保持已有等价能力。[bootstrap.write_active](../../../trellis/skills/guru-team/runtime/bootstrap.py)原本已用 as_posix，未重复改写；内部 fixture 与正式 pointer 分开。原生失败选择/旧 pointer 保留回归通过。 |
| C1：extension manifest 中的 CRLF 摘要 | 替代为[限定 LF/精确恢复](../../../trellis/presets/guru-team/scripts/python/managed_text_eol.py)；manifest 与 validator 继续读取原始字节。正常 Git clone 的 B drift/候选通过，与本机直接 EOL 5 例共同覆盖恢复及用户修改保护。 |
| C2：file URI 转换 | 吸收为[原 schema owner](../../../trellis/skills/guru-team/runtime/schema.py)的标准 url2pathname。Windows B 的相对 child schema unresolved，候选同环境通过。 |
| C2：中文提交消息字节写入 | 吸收并补齐[原 executor](../../../trellis/skills/guru-team/packages/guru-create-task-commit/runtime/execute.py)的写入、UTF8 读回与最终 commit 检查，以及[Git 文本协议](../../../trellis/skills/guru-team/packages/guru-create-task-commit/runtime/common.py)。cp1252 下真实消息/hook/index 回归通过，消息变化仍被检测。 |
| C2：checkout-index --index | 排除，不引入。原 executor 继续 checkout-index --all --force；原生 Windows 的真实 TaskCommit、hook 修改检测及无关 index 保留均通过，未证明支持场景需要该额外参数。 |


## Windows Codex 实际会话与当前边界

run 39240156056 使用官方 Codex CLI 0.163.0、Ollama 0.40.6 和本地 qwen3:4b。依赖与模型安装成功，隔离 CODEX_HOME 未使用 OpenAI 账号凭据；会话在 2700 秒后超时失败。原始事件显示模型把 guru-qualify-normal-scenario Skill 名作为 spawn_agent 的 agent_type，收到 unknown agent_type，随后未完成公开 wrapper 调用。该会话不满足 T630-08，也不能作为自动加载与 Skill 执行的完整验收。

采集器将纠正 Skill 与 Agent 类型的提示，改为当前 Agent 读取 Skill 全文及合同并直接调用其公开 wrapper；单次模型会话上限为 600 秒。重试结果仍须核对实际工具事件及 typed stdout，不由进程退出码或提示文本推定通过。三系统产品原生安装、维护与 wrapper 证据已通过；Windows Agent 验收及 Task 闭环尚未完成。当前目标不执行正式软件发行，也不声明累计 Release Gate 通过。
