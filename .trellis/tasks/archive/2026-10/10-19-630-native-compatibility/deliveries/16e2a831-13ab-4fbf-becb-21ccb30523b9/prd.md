# D1 三系统产品兼容修复与原生诊断

## 1. 整体来源与术语

整体 authority 为 Task 根 `prd.md` 及公共 accepted_scope。本批 Delivery `16e2a831-13ab-4fbf-becb-21ccb30523b9`，planning_root 为 `deliveries/16e2a831-13ab-4fbf-becb-21ccb30523b9`。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/630 | 整体 R1–R6、AC1–AC10；要求 | 本批代码、原生安装/脚本和上游集成；Windows Agent及发行仍为整体义务 |
| https://github.com/castbox/guru-trellis/issues/631 / PR #632 | 已交付证据 | 复用 targeted-ci.yml 的三系统 runner、目标隔离和 artifact |
| 整体 PRD 第5–7节 | 全部行为与验收；要求 | 保留后继产品修复、三系统与 Agent 责任 |
| docs/ci/README.md | 当前 driver 使用合同 | 扩展选择语法，保留旧选择方式和失败语义 |

本批的诊断成功指观察并记录原始调用结果，不能表示被测产品通过。baseline、candidate 和 driver 是独立身份。

## 2. 整体与本批目标、非目标

整体目标仍是 #630 全部三系统兼容修复和验收。本批交付 CI 精确选择、真实诊断及产品兼容修复。原纯诊断切片不能独立通过标准 Merge 的失败检查门禁，因此在同一 Delivery 纳入原整体需求内的产品修复与上游集成，不改变 Task accepted scope。

本批覆盖 Guru canonical runtime、必要 installer/受管字节策略、TaskCommit、固定上游来源接入、直接回归、声明投影和使用说明。Guru 不改上游 hooks/skills/agents/commands；上游只通过 #53 已发行来源采用。全部平台累计 Release Gate 不在范围内。Windows Codex 实际会话及正式发行保留为同 Task 的整体完成义务，不能用本批代码合并替代。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 无前序 Delivery。开发基线为 main `0543731bf52aa80842fde5db47332380de513cf0`。现有 #631 Windows artifact 的 smoke-preset 只给出 managed_runtime_check_failed，未保留内部公开 wrapper 的返回码和输出。现有 unittest_report 支持文件或模块名，不能精确加载包外文件中的单个用例。

当前代码事实为提交 `10da9be7c976ac210ec3a8afc42077f5e709bd7f` 和 PR #634；尚无已交付 Delivery。原生 run `39223843984` 的 driver/candidate 为该提交，baseline 为上述 main。三系统 driver 回归通过；macOS/Linux 两目标完成安装和 wrapper 两例；Windows 两目标的 collector completed，但原 bare bash 调用返回 WSL 未安装发行版，继而 JSON 解析失败。该结果不是缺少 jsonschema 的证据。原安装失败保持非零。

本批继续依赖 hash-locked Python、原生 Git for Windows Bash 和既有三系统 CI。上游 #53 固定源码为 `7f050fa11ddd8569e5db4f728ea1b745b7500a98`，发行 `castbox-v0.7.0-castbox.5`，须沿现有来源维护合同验证后采用；source lock 改动不能代替目标更新。Windows Agent 环境和认证尚未就绪时，只阻塞其验收与整体 Completion，不掩盖缺口、不转交 #631。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置 | 动作与可观察结果 |
| --- | --- | --- |
| DS1 | 维护者，包外测试文件已存在 | 选择 `path/to/test.py::Class.test`，只执行指定真实用例；未选中的无关失败不参与结果 |
| DS2 | 维护者，原文件或模块选择 | 继续使用旧语法，保留原结果；缺文件、类、用例和导入错误保持非零 |
| DS3 | CI，目标依赖环境已建立 | 在目标实现上运行其 bootstrap public-wrapper capability check，记录真实子进程 argv、返回码和 stdout/stderr；不替换产品实现 |
| DS4 | CI，一个目标测试或安装失败 | 继续其他独立阶段及另一个目标；最终产品/基础设施失败保持原非零，artifact 区分诊断和产品结果 |
| DS5 | 三系统开发者，中文/空格仓库及已注册 worktree | 真实公开 root/base 与 schema 相对引用入口接受合法路径；不同 checkout 身份继续按原合同区分 |
| DS6 | 安装者，明确 Python 3 与原生 Bash | 真正进入目标 wrapper；JSON 到 managed consumer 后语义相同；日常调用只使用已激活 runtime，激活前失败保留旧 pointer/环境 |
| DS7 | TaskCommit owner，隔离 Git fixture 与非 UTF-8 默认编码 | 中文消息文件、发布前读回及最终 commit 按同一 UTF-8 候选协议；真实消息变化、hook 和索引校验保持 |
| DS8 | 安装/维护者，正常 LF/CRLF checkout | 真实初装、checkout、installed validation 和 reapply 一致；真实用户修改继续保护，不重算摘要掩盖差异 |
| DS9 | Windows 维护者，固定上游 .5 与新进程 | 原生 update/tools_install/workflow preview-force/recover-resume 后，Guru reapply 和公开入口仍可用 |

## 5. 完整行为、条件与约束

- DR1：选择器新增文件与用例的明确组合；路径包含空格时按一个 argv 传递。只从指定文件加载所选类/方法，不在全仓 discover 后过滤。旧文件和 unittest ID 选择保持可用。
- DR2：驱动与目标分离。测试文件来自明确被测目标；诊断驱动来自本次 driver。不得复制候选产品代码进基线或将 ImportError/runtime 未激活/WinError 193 算缺陷命中。
- DR3：诊断执行目标自身 bootstrap_check 及真实 Bash→managed Python wrapper。仅观察已声明 fixture 的调用和结果，保持调用参数和产品返回行为。普通 schema 不完整输入也执行，不能只验证成功情况。
- DR4：目标 checkout、Python/Bash/OS、driver 与目标 SHA 分别记录；日志只包含本 fixture 的非敏感命令和输出，不收集环境变量、凭据或业务数据。
- DR5：诊断失败、产品失败、环境缺口分别保留；不给 expected_test/expected_message 增加“任意安装失败即预期”的含义。候选失败和未执行不能变成通过。
- DR6：沿原 targeted-ci.yml 接入，不建第二套 runner；macOS/Linux/Windows 各取得原生诊断和当前候选产品回归结果。本批代码合并仍不可替代整个 #630 的真实 Agent 和发行义务。
- DR7：承接整体 R1。按系统 Path 语义比较 root/authority/worktree；本地 file URI 正确转换盘符、中文和空格，并解析 schema 相对引用，不靠斜杠字符串替换掩盖身份差异。
- DR8：承接整体 R2–R3。修复实际 Python→Bash→managed Python 首偏差，明确原生 Bash 来源及实际执行方式；固定 capability fixture 的路径和 JSON 传输不得改变 consumer 语义。公开原输入形式继续支持，fixture 调整不成为公共接口删减。
- DR9：承接整体 R3。Guru 控制的 UTF-8 文件、JSON 和提交消息显式按协议读写；Git 输出保留实际错误，不忽略解码错误。真实 TaskCommit 中文消息验证写入、读回和最终提交；checkout-index --index 先证明必要性再决定，不附带吸收。
- DR10：承接整体 R5–R6。追踪受影响 Guru-owned 文本的 canonical checkout、安装复制/生成、目标 Git checkout 和各 hash consumer。只采用有复现与必要性证据的字节策略；二进制、lock、精确身份及用户修改保护保持，不关闭校验、不无条件归一全部文件、不只重算 manifest。
- DR11：承接整体 R4/R6。保留 Unix 仅 python3、Windows 单一 executable 名/路径的显式选择合同；Guru 不解析上游 py -3 命令串，不全局替换 python3。显式失败不回退，日常 wrapper 不使用偶然全局依赖。采用上游 .5 并验证新进程的实际集成，不管理上游资产。
- DR12：产品修复由本批继续承担。对实际缺陷提供独立 driver/target 的基线失败及修复候选通过，原生 Windows 非 UTF-8、中文/空格、LF/CRLF、解释器可见性和真实 wrapper 按整体验收执行。三系统产品检查通过后才合并；Windows Codex 实际会话和正式发行仍是整个 Task 最终完成的必要条件。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口、输入与预期结果 |
| --- | --- | --- |
| DA1 | DR1/DS1 | 真实临时包外测试文件含一个选中通过用例和一个未选中失败用例；文件::用例入口只跑选中项，tests_run=1 |
| DA2 | DR1/DS2 | 旧文件与模块选择保持结果；不存在用例与真实导入错误非零并记录 error |
| DA3 | DR2–4/DS3 | 现有三系统 CI 使用独立目标实现执行真实 capability fixture，报告两种声明用例的实际调用结果，Windows 底层失败可定位 |
| DA4 | DR5–6/DS4 | 现有 driver 集成测试及实际 run 证明失败继续、独立目标身份和原始产品失败不被诊断成功覆盖 |
| DA5 | DR4–6 | docs/ci 说明精确选择、diagnostic artifact 和证据边界；不勾选整体产品验收 |
| DA6 | DR7/DS5 | 三系统中文/空格 repo、真实注册 worktree 和带相对引用 schema，通过实际 root/base/schema 链路验证基线缺陷与修复 |
| DA7 | DR8/DR11/DS6 | 三系统代表性 clean 安装，安装后 wrapper 两声明用例返回预期码/JSON；解释器/Bash缺失、普通schema错误和激活前失败保持原语义及旧pointer |
| DA8 | DR9/DS7 | Windows 非 UTF-8 默认配置及三系统真实 TaskCommit fixture，核对消息文件字节、读回比较和最终 commit；真实消息变化仍被检测 |
| DA9 | DR10/DS8 | 正常 Git LF/CRLF checkout与真实 apply/reapply/installed validation；初装、再次checkout一致，用户修改保护及sidecar原规则保持；列明实际文本类别和hash消费者 |
| DA10 | DR11/DS9 | 固定 .5 上游来源/CLI/实际目标身份，验证新进程 update、tools_install→Guru reapply→入口、同provider preview/force及原recovery_ref recover/resume；保留用户修改和.new/.bak处置 |
| DA11 | DR6/DR12 | 既有三系统入口执行本批适用产品回归，记录driver/基线/候选/上游及环境；全部当前候选检查通过，Agent/累计矩阵/发行证据分别报告 |

无未决产品选择。Windows bare bash 的首偏差已观察到，修复与反事实验证尚未发生；后续偏差继续按原 qualification/Architecture 发现路由处理。换行完整归因和 checkout-index 必要性须以实际链路确认。若目标资产/解释器/Bash缺失，保留环境失败，不能伪造调用记录。Windows Codex 环境/认证缺口不得通过复制维护者凭据或直接执行hook替代真实会话。

## 7. Canonical 引用与本轮差额

`docs/ci/README.md`、`.trellis/spec/preset/installer.md`、runtime/TaskCommit原合同及 `.trellis/spec/preset/upstream-ownership.md` 承接本批工程差额；质量规范的 Test And Validation Value/Validation Scope Ownership 继续适用。Architecture authority 为 docs/architecture/README.md（current-main-0.7.0-guru.102）、constitution 和 change-contract。本轮方案范围已从纯CI扩大到产品，旧 no-impact不能作为新方案结论，须重新 candidate_assessment。RDT 原 owner判断操作/产品文档差额，不制造空贡献或无consumer状态。
