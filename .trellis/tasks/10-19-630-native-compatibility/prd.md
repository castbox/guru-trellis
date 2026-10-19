# Guru Trellis 三系统运行与安装一致性整体需求

## 1. 来源与术语

| 标识 | 来源与章节 | 角色与用途 |
| --- | --- | --- |
| I630 | https://github.com/castbox/guru-trellis/issues/630 全文 | Direct Source；全部行为、约束与验收 |
| I631 | https://github.com/castbox/guru-trellis/issues/631 与 PR #632 | 已交付原生 CI 的证据与复用边界 |
| T53 | https://github.com/castbox/Trellis/issues/53 | 上游原生入口修复与集成前置 |
| C1 | https://github.com/castbox/chengtuo-resume/commit/4319b9e4624cf61117ad1d36f8518b88154d68d2 | 历史工具修改；逐项处置，不整包复制 |
| C2 | https://github.com/castbox/chengtuo-resume/commit/0b3c3c28735859fde09dfe6fb41a87c84422994e | 历史 URI、编码、checkout-index 线索；须独立验证 |
| OWN | .trellis/spec/preset/upstream-ownership.md | 当前 canonical/preset 所有权与用户修改保护 |

managed runtime 指由 Guru 激活的 hash-locked Python 环境；安装解释器与日常 runtime 是不同职责。原生 Windows 不包含 WSL。实际 Agent 自动加载必须由 Codex CLI 正常会话入口产生；直接运行 hook 只证明脚本调用。

## 2. 背景与问题

Windows 开发机上的 chengtuo-resume 在使用 Guru Trellis 执行任务期间，Agent 为继续工作修改了工具文件。本 Issue 从这些真实使用记录中提取通用兼容问题，在 Guru canonical source 修复，并验证 macOS/Linux 的已有行为。

参考来源：

- [4319b9e4624cf61117ad1d36f8518b88154d68d2](https://github.com/castbox/chengtuo-resume/commit/4319b9e4624cf61117ad1d36f8518b88154d68d2)：80 个变更文件中，76 个仅替换命令或提示中的 python3 为 python；功能性 runtime 修改集中在 base_selection.py 和 bootstrap_check.py。
- [0b3c3c28735859fde09dfe6fb41a87c84422994e](https://github.com/castbox/chengtuo-resume/commit/0b3c3c28735859fde09dfe6fb41a87c84422994e)：另有 schema 文件 URI 转换、提交消息 UTF-8 字节写入和 checkout-index --index 调整。提交说明报告了 Windows URI、原生提交与安装验证；本轮未独立重跑其原生验证，不把提交说明当作 Guru 正式三系统验收。

在初始静态基线 `71f432f22acc78df7194a818c27b8e467ceb3048` 上已核对（#631 后续原生证据见下节）：

| 位置 | 当前实现与待解决问题 |
| --- | --- |
| trellis/skills/guru-team/runtime/base_selection.py | Git 根目录输出直接与 str(Path.resolve()) 比较；Windows 斜杠表示差异可能拒绝合法根目录及已注册 worktree。Git subprocess 文本读取未指定协议编码。 |
| trellis/skills/guru-team/runtime/bootstrap_check.py | capability fixture 将原生路径和内联 JSON 参数直接传给 Bash；文本输出读取依赖系统编码。真实 active pointer 的 bootstrap.write_active 已用 as_posix()，须区分 fixture 与正式写入路径，避免重复修复。 |
| trellis/skills/guru-team/runtime/schema.py | Path(unquote(parsed.path)) 未完成 Windows file URI 的盘符路径转换。 |
| trellis/skills/guru-team/packages/guru-create-task-commit/runtime/execute.py | 使用未指定编码的 message_path.write_text() 写提交消息，并在发布前使用 message_path.read_text() 读回比较。只改写入侧仍可能在 Windows 按系统编码错误解码或产生错误 mismatch；写入、读回和最终 commit 验证须保持候选消息合同。 |

另外，4319b9e4 的 extension.json 对 clear-technical-writing.md 和 skills/registry.json 记录的 hash，精确对应文件的 CRLF 版本；该提交的 Git blob 为 LF。已独立重算这两个实例。当前校验读取原始字节，因此需要查明正常 checkout、安装写入和 manifest 生成的完整路径，解决由换行策略不一致造成的错误漂移。

当前 main 基线为 `0543731bf52aa80842fde5db47332380de513cf0`。上游 #53 已关闭，交付记录固定源码 `7f050fa11ddd8569e5db4f728ea1b745b7500a98` 和配对 `0.7.0-castbox.5` GitHub Release；本 Task 仍须验证 Guru 集成。初始来源中的旧状态保留为历史事实。

## 3. 目标与非目标

使 macOS、Linux、Windows 的正常安装、公开 wrapper、平台启动与任务提交遵循明确一致的路径、编码、解释器和受管文本字节合同。整体完成必须满足第7节全部适用验收。

不执行所有 AI 平台、全部历史版本和所有 installer 组合的累计发布矩阵。不修改业务功能或业务生产数据。不引入威胁/攻击模型、恶意篡改、竞态压力、锁协议或额外 fault injection。Guru 不修补上游 trellis-* skills、hooks、agents 或 commands。

## 4. 真实调用方、场景与流程

| 场景 | 调用方及前置 | 触发、行为与可观察结果 |
| --- | --- | --- |
| S1 | 三系统开发者，中文/空格 repo 与注册 worktree | 公开 base/root 入口接受相同合法路径身份；不同 checkout 继续按既有身份检查 |
| S2 | 安装器及 Skill caller，原生 Python/Bash | 安装并激活 runtime；公开 wrapper 处理成功 JSON 与普通 schema 错误；路径和 JSON 到 consumer 后语义相同 |
| S3 | TaskCommit owner，隔离 Git fixture | 使用真实任务提交入口生成中文消息；候选文件、发布前读回与最终 commit 一致；真实消息变化被检测 |
| S4 | 安装/更新用户，正常 LF/CRLF checkout | 初装、再次 checkout、installed validation 与 reapply 不产生虚假漂移；真实本地改动仍被保护 |
| S5 | Windows Codex CLI，新隔离验证配置 | 显式完成 hooks 前提；正常启动自动加载 Guru workflow/平台入口并按路由调用一个 Guru Skill |
| S6 | 更新/维护用户，固定上游修复版本 | 新进程 update、tools_install、workflow preview/force 与同 recovery_ref recover/resume 后，Guru reapply 和入口可用 |
| S7 | CI driver，基线与候选独立 checkout | 精确选择包级断言并保存两目标原始结果；预期基线失败不掩盖候选失败 |

S2 的解释器/Bash 缺失、普通 schema 错误和激活前检查失败，必须保持原失败语义。激活前失败不能破坏旧 active pointer 与可用环境。

## 5. 行为要求

以下保留 I630 的六项行为及约束，编号 R1–R6 与来源第1–6项一一对应。候选机制仍为候选，由 Delivery design 决定。

使正常安装、平台入口启动、公开 Skill 调用及任务提交，在 macOS、Linux、Windows 上使用一致且明确的路径、编码、解释器和受管理文件内容合同。

1. **路径身份与 URI**：按当前系统的路径语义比较合法仓库根目录和已注册 worktree。正确把本地 file URI 转成本地路径，在 Windows 盘符、中文及空格目录中读取带相对引用的 schema。不得只靠字符串替换掩盖不同 checkout 的真实身份差异。
2. **跨进程传输**：核对 Python → Bash → managed Python 的完整调用链。以正斜杠路径、stdin JSON 为参考候选，证明路径和 JSON 到达原 consumer 后语义不变；不得因修复内部 capability fixture 而移除公开接口已经支持的输入形式。明确 Git for Windows Bash 的来源与调用方式，仅找到 bash 可执行文件不等于可用。
3. **编码与候选字节**：Guru 控制的 UTF-8 JSON、文件和提交消息显式按其协议读写，避免系统文本编码和换行转换改变内容。Git 输出按实际协议处理；不得使用忽略解码错误来把原始 Git 失败变成成功或丢失错误信息。
4. **解释器选择**：复用既有 --python、CPython 3 和 managed runtime 合同，区分一次性安装/维护解释器与日常已激活运行时。Guru 的 --python 当前接受一个可执行命令名或路径；上游 TRELLIS_PYTHON_CMD 中合法的 `py -3` 是命令加参数，不能把整串作为 Guru 的 executable 直接传入，也不因此要求 Guru 新增通用 shell 命令解析器。覆盖只有 python3 的 Unix 环境及 Windows 明确选择 Python 3 命令或路径的入口；显式选择失败不静默切换，日常 Skill 不退回全局 site-packages 或偶然激活的 venv。不得直接把所有系统的 python3 改成 python。
5. **换行与摘要一致性**：明确 Guru-owned 文本从 canonical checkout、installer 复制/生成、Git checkout 到 manifest/hash 校验的字节策略。正常 LF/CRLF 转换不得造成无法恢复的虚假漂移；实际内容不一致仍须被检测。解决方式由规划结合复现确定；不得通过关闭校验、无条件归一全部文件、覆盖未知本地修改或单纯重算 manifest 隐藏问题。二进制、依赖 lock 和原本要求精确字节的身份保持各自合同。 本次换行修复针对参考提交已暴露的 Guru-owned 受管文本；规划列出实际文件类别和写入/校验 consumer。两例换行摘要已重算确认，完整归因仍须追踪原生 checkout 与 installer 路径。对要求精确字节的文件，使用明确的 canonical/安装字节策略维持合同。
6. **维护与分发**：Guru 自有修复回到 canonical runtime、installer 和 Guru namespace 的声明平台投影，再同步 dogfood。apply/reapply、工具更新和升级后重新应用须保持修复。保留真实用户修改和既有 .new/.bak 处理规则。

## 6. 约束与依赖

[castbox/Trellis#53：修复 Windows update 与工具维护丢失已解析 Python 命令的问题](https://github.com/castbox/Trellis/issues/53) 承担原生入口修复。

当前固定的上游 `7bcbeaad31380e7a29c97898cb947c6120a61775` 已有 init 的平台解释器解析及写入时替换能力。新发现的缺口是：该解析结果只在 init 进程内存中；新进程的 update/maintenance 模板收集未重新解析，可能将 python3/py -3 回退成 python。另有原生 preflight/工具维护校验将整个命令字符串直接作为 spawnSync 的 executable；接入须同时验证选择正确、命令加参数正确执行，不能只核对渲染文本。最小平台模拟已观察到 hook 命令回退；尚未执行真实 Windows 全链路。相同选择还被 workflow 的预览/应用，以及维护操作正常回读/幂等续接的 postvalidate 消费，均由 #53 在同一机制内适配。

本 Issue 的职责：

- Guru 的 .trellis/spec/preset/upstream-ownership.md 明确禁止 preset 管理、覆盖或修补上游 trellis-* skills、hooks、agents 和 commands。原生入口问题由 #53 修复，不能用新增 overlay 或业务仓库生成文件 patch 兜底。
- 独立的 Guru runtime、URI、编码和换行工作不因等待上游而停止。只有依赖原生入口修复的版本接入及集成验收等待 #53。
- 接入时明确记录上游修复 commit、CLI 构建/版本、Guru source lock 与目标实际安装身份，并通过仓库现有来源维护合同完成验证。local_candidate 只能作为开发证据；source lock 变化本身不证明目标已更新。
- #53 不承担 Guru runtime/manifest 修复；本 Issue 不代替其关闭或声称其原生验收已完成。

### CI 与证据责任

[Guru #631：建立 Guru Trellis 三系统定向 CI 验证基础设施](https://github.com/castbox/guru-trellis/issues/631) 提供原生 Windows/macOS/Linux runner、依赖安装、PR/main 自动检查、手动版本对照入口及诊断 artifact。本 Issue 编写并维护上述兼容缺陷的复现和回归断言，将适用测试接入该入口；不另建一套重复 CI 基础设施。

- #631 已独立交付，本 Issue 直接复用其正式入口，并按下节能力边界接入缺陷回归；最终验收仍需取得修复候选的适用原生三系统证据。CI 基础设施交付或 workflow 整体绿色，都不单独证明本 Issue 验收完成，须核对具体执行用例及未验证项。
- 维护者没有 Windows 电脑不构成验收阻塞。GitHub-hosted 原生 Windows runner 可承担本 Issue 的原生 CLI、Python、Git for Windows Bash、路径、编码、换行及安装验证；WSL、Linux 容器、模拟平台和 mock 不能代替。
- 对确定的缺陷，在固定环境配置下分别运行受影响基线和修复候选。记录实际 commit、测试驱动身份、OS/runner 镜像版本、Git/Python/Bash 版本、入口、命令、退出码及断言；基线须命中对应缺陷，候选须通过。依赖安装失败或无关报错不算复现。旧版本没有回归测试时，将测试驱动与被测目标分开标识，不能把候选实现混入基线。不同缺陷可使用各自实际受影响基线，不强行要求一个基线复现全部问题。
- 控制解释器可见性时，核对被测子进程实际解析结果，防止 runner 预装 Python 掩盖场景；记录 UTF-8/locale 配置，编码用例覆盖受支持的非 UTF-8 配置，不能仅凭 UTF-8 默认环境通过判定修复。LF/CRLF 仍通过正常 checkout/安装构造。
- 上游 #53 的原生结果作为前置证据，本 Issue 仍在固定的上游修复来源和 Guru 候选上验证集成，不用上游 CI 绿色替代 Guru 安装链路。
- 真实 Agent 启动的必需组合固定为 Windows + Codex CLI。在原生 Windows runner 或临时原生 Windows 环境，使用实际安装的候选，通过 Codex CLI 正常启动/会话入口验证其自动加载 Guru workflow 与平台入口，并在该会话中按正常路由实际调用一个 Guru Skill。规划记录 Codex CLI 版本、公开启动命令、所选 Skill 及可观察结果。按所选版本的公开配置合同显式完成 hooks 功能开关和原生要求的一次性 hook 启用/审阅，并记录非敏感配置前提；验证环境不能依赖维护者机器已有的启用状态。上游 `packages/cli/src/configurators/codex.ts` 当前已提示该前提，实际操作以所选 Codex 版本合同为准。使用独立验证配置，保留维护者已有全局配置和凭据；如一次性启用需要交互，使用临时原生 Windows 环境完成，不能改用手工注入 workflow 文本代替自动加载。未具备此前提时记为 Agent 环境未就绪；不得以直接执行 hook、wrapper 或读取文件替代自动加载/调用证据。macOS/Linux 的本 Issue 必需验收为原生安装、真实脚本/wrapper 运行和 Codex 定向投影检查，不要求再启动真实 Agent。其他声明 Agent 平台仅检查本次修改涉及的投影。Windows Codex 启动条件缺失时，该项保持未验证并阻塞本 Issue 最终完成；不把该阻塞转交 #631，也不要求 #631 配置 Agent 凭据。
- 报告提供 Actions run 与脱敏 artifact 链接，区分平台模拟单测、原生脚本执行、实际安装和 Agent 启动结果。本次补入 #631 已交付的环境与失败证据，不新增本 Issue 产品修复通过结论。

### 已交付基础设施的实际边界

#631 已完成并关闭，实现 PR [#632](https://github.com/castbox/guru-trellis/pull/632) 合入 commit 为 `bf4c86630bded68a5f11e824044850e569cc129e`。归档后的 main 为 `0543731bf52aa80842fde5db47332380de513cf0`，CI 实现未改变。当前入口为 `.github/workflows/targeted-ci.yml`，维护说明为 [docs/ci/README.md](https://github.com/castbox/guru-trellis/blob/bf4c86630bded68a5f11e824044850e569cc129e/docs/ci/README.md)。[交付证据](https://github.com/castbox/guru-trellis/issues/631#issuecomment-6261004110)和下列 artifact 已于 2026-10-19 独立下载核对。

| 已执行入口 | 实际结果与使用边界 |
| --- | --- |
| [正式 main run 39208690331](https://github.com/castbox/guru-trellis/actions/runs/39208690331) | 目标为上述 merge commit。三系统各 11 项现有测试通过；Linux/macOS 完成代表性 clean 安装；Windows CLI init 成功，`smoke-preset` exit 1、`code=managed_runtime_check_failed`。证明环境与失败基线可用，不代表三系统产品兼容通过。 |
| [双版本 run 39208744493](https://github.com/castbox/guru-trellis/actions/runs/39208744493) | driver 为上述 merge commit；baseline=`71f432f22acc78df7194a818c27b8e467ceb3048`，candidate=`7d744f82ee75b0e5d7aecacc9ee3212d1b32bd63`。三系统均执行两个独立目标，报告 `baseline_matched=false`、`established=false`。证明版本隔离和失败后继续，不是产品失败/修复对照。 |

Windows 的 `test_contract.BaseSyncPackageContractTests.test_porcelain_z_parser_keeps_registered_worktree_records_separate` 真实创建仓库和 worktree，暴露 Git 正斜杠路径与原生 Path 反斜杠路径的断言差异。这是路径语义调查线索；须结合真实 root/authority 入口确认产品影响，不能仅改测试字符串就宣称路径身份修复。整文件运行还包含 runtime 未激活、Windows 直接启动 shell 文件及 fixture 前提错误，不能全部归为产品缺陷。

Windows clean 安装在 hash-locked 依赖安装和 capability probe 成功后，进入 `bootstrap.py::run_public_wrapper` → `bootstrap_check.py::check_public_wrapper` 失败。外层日志仅有 `managed_runtime_check_failed`，具体根因尚未确认，不能凭 `dependency=jsonschema` 标签断言依赖未安装。先取得该正常调用链的底层返回码和输出，再确定修复机制；保留旧环境与 active pointer 的既有失败行为。此失败尚不是上游 #53 的复现证据。

本 Issue 在已交付 CI 上完成以下接入，不重建基础设施：

- 准备选定测试所需的 managed runtime、Git fixture 和原生 Bash 调用方式，再执行缺陷断言。只修正本 Issue 回归直接涉及的 fixture 前提；ImportError、runtime 未激活或 WinError 193 不能算命中待修复缺陷，不扩张为全仓测试清理。
- 当前 `ci/unittest_report.py` 能按文件路径执行包级测试，但单独传入默认 installer 测试目录外模块的 unittest ID 会导入失败。为本 Issue 的包级回归补齐“文件 + 用例”精确选择能力或等效明确加载方式，并补充正常用法的驱动回归；不以整文件混入无关失败代替精确缺陷证据。旧目标没有新回归时，将独立测试驱动与旧目标实现分开，不把新产品实现复制进基线。
- 当前 `expected_test/expected_message` 仅匹配精确 unittest failure，并要求基线其他阶段正常；不会接受基线安装失败。安装缺陷通过相同环境配置下的原生入口、实际基线失败日志和修复候选成功日志分别验收，由 AI 对照具体失败机制判断。无需强制把 `comparison.established` 改成 true；如需自动汇总适配，只补本 Issue 必需的确定性记录，不放宽成任意安装失败均算预期，候选失败和未完成继续保留。
- 解释器可见性、非 UTF-8、LF/CRLF、公开 wrapper、中文提交和 Windows Codex 实际会话继续按原验收完成。#631 默认测试与安装尝试不替代专项结果。每次修复验证绑定实际 driver、基线、候选和上游来源；artifact 过期时按公开入口重跑，不把失效链接当作可读取证据。

本 Task 不新增 public Skill ID 或改变公共输入/出口。具体修复方案由 Delivery 规划决定；若方案需要改变公共合同，须回原 scope owner。没有业务数据模型、数据库迁移或生产数据写入。

## 7. 可观察验收与验证方式

I630 下列十项依次为 AC1–AC10，覆盖 S1–S7 与 R1–R6。保留原生环境、失败基线、独立 driver、编码和真实 Agent 证据责任；未完成项不勾选。

这是跨系统兼容专项。最低环境为 macOS、Linux、Windows 各一个原生环境；Windows 使用原生 Python 与 Git for Windows Bash，WSL 不代替 Windows 证据。规划时固定每个环境的 OS、Git、Python、Bash 和实际入口。真实 Agent 启动矩阵仅为 Windows + Codex CLI；macOS/Linux 执行原生脚本及 Codex 投影回归，其他声明 Agent 平台执行受影响投影检查。Windows 的显式解释器选择方式须写成可复制命令，涉及含空格可执行路径时验证正确传递。

- [ ] 对两个参考提交中的工具修改逐项记录吸收、保持现有等效能力、替代或排除结论，并链接代码和证据。checkout-index --index 须先证明与正常提交/平台物化行为的关系，不随附带提交直接引入。
- [ ] 三系统各完成一次代表性干净安装，使用安装后的真实公开 wrapper 运行 bootstrap manifest 已声明的成功和普通 schema 不完整输入用例，检查返回码及 JSON 合同。
- [ ] 三系统在中文和空格目录中验证根目录、已注册 worktree、schema 相对引用及 JSON 传输。路径/JSON 经过真实调用链，不能只以 mock Bash、纯路径对象测试或 import 成功代替。
- [ ] 验证 Unix 仅 python3、Windows 显式选择解释器，以及日常 wrapper 仅使用已激活 managed runtime。对缺失解释器/Bash、普通 schema 错误和 bootstrap 校验失败，保留既有错误/失败恢复语义；激活前校验失败不破坏旧 active pointer 与可用环境。
- [ ] 在隔离测试仓库通过真实任务提交入口写入中文消息，核对消息文件的实际字节、发布前读回比较与最终提交内容；写入和读回均按候选消息协议工作，不只验证 write_bytes。保留既有 hook/索引检查和真实消息变化的检测。
- [ ] 通过正常 Git checkout 配置和安装操作构造 LF/CRLF 差异，定位摘要产生与读取点。验证初装、再次 checkout、installed validation 和 reapply 结果一致；真实用户改动仍按原合同保护，不手工伪造 manifest/hash 构造用例。
- [ ] 验证 canonical、dogfood 和本次修改的 Guru 平台投影一致。在 Windows + Codex CLI 通过真实启动/会话入口证明候选安装的 Guru workflow/平台入口自动加载，并正常路由调用所选 Guru Skill，记录版本、命令和可观察结果。macOS/Linux 的 Codex 及其他受影响声明平台按上述矩阵执行定向投影检查；三系统原生安装和真实脚本/wrapper 验收仍全部保留，不扩张为全 Agent × 全 OS 运行矩阵。
- [ ] #53 修复接入后，在固定来源与实际安装身份上验证新进程的原生 update、`trellis maintain` tools_install 入口 → Guru apply/reapply → hook/Skill 入口链路。Windows 的 py -3 场景验证上游原生 executable/argv；Guru 安装另用其合同支持的单一 executable 名或路径。保留上游显式选择/跳过探测与 Guru 显式选择失败不回退的各自合同，不把两套规则混用。在受影响的 Windows 场景验证同一 workflow provider/template 的 `--create-new` 预览与显式 `--force` 应用，以及成功工具安装原 recovery_ref 的新进程 recover/幂等 resume；使用 #53 的原生结果作前置证据，再核对 Guru 集成入口。不重跑全部恢复矩阵或制造故障。记录 .new/.bak 结果，保留用户修改。
- [ ] 将适用回归接入 #631 已交付入口，补齐包级用例精确选择及直接相关测试前提，验证基线/候选实现隔离。提供指定缺陷的基线失败、修复候选通过和三系统定向结果；安装缺陷按原生安装入口日志独立对照，不冒用 unittest 匹配器。真实 Agent 入口单独报告。
- [ ] 补充实际修改的回归测试和使用说明。每项证据记录环境、入口、命令、返回码及结果；缺环境记为未验证，缺项不勾选。跨系统必需验收未完成时，本 Issue 不算完成，也不声称 Release Gate 通过。

本 Issue 不执行所有 AI 平台、全部历史版本及全部 installer 组合的累计发布矩阵。也不包含业务功能、生产写入、威胁/攻击模型、恶意篡改、竞态压力、锁协议或额外 fault injection。

生产发布属于代码完成后的独立发行步骤。只有本 Task 全部验收、发布准备及发行校验满足时，才发布 Guru 官方版本；源码与 CI 通过不能替代真实 Agent 验收。

## 8. 实际未决项

需求无未决产品选择。技术调查尚须确认 Windows clean 安装的底层失败、换行摘要完整链路，以及参考 checkout-index 修改是否必要；由 Delivery Author/implementation owner 处理。Windows Codex CLI 实际会话环境、hooks 前提和可用认证尚未验证；缺失时仅阻塞依赖它的验收与最终 Completion，不阻塞独立修复。
