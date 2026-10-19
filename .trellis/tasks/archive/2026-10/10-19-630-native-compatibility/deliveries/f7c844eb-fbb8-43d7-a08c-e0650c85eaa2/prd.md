# D2 Windows Codex 实际会话验证需求

## 1. 整体来源与术语

公共 accepted_scope 为本 Task 根 prd.md 的已接受版本。本批 Delivery 为 f7c844eb-fbb8-43d7-a08c-e0650c85eaa2，planning_root 为 deliveries/f7c844eb-fbb8-43d7-a08c-e0650c85eaa2。

| 来源与章节 | 角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/630 的真实 Agent 条件、AC7/AC10 | 要求；原生 Windows 正常启动、自动加载和实际 Guru Skill 调用 |
| Task 根 prd.md 第4–7节 | 已接受整体责任、原生环境及证据边界 |
| https://github.com/castbox/guru-trellis/pull/634；合并 80413052748afecc65622a38cab283aba69352bb | 历史交付；D1 产品修复与三系统脚本/安装 |
| ci/windows_codex_session.py、docs/ci/README.md | 当前采集器实现及使用合同 |
| 本次实际 Codex/Ollama 探针与 wrapper 返回 | 调查证据；用于修正验证前提，不能替代 Windows 验收 |

实际调用指模型通过 Codex 工具执行 installed Skill 的合同和公共入口。CLI 退出0、模型声称成功和宿主直接执行 wrapper 均不能单独证明实际 Skill 完成。

## 2. 整体与本批目标、非目标

本批补齐 Windows 实际 Agent 证据的采集能力并取得适用证据。修正真实调用的输入前提、模型和程序提示，保留独立配置、公开启动及失败原始记录。Skill 名不得作为 Agent 类型。本批不改 Guru 公共 Skill/validator，不用放宽判定适配模型错误，也不重做 D1 产品修复。

保持整体非目标：不执行全部平台累计发布矩阵，不处理业务数据、威胁模型、锁协议或故障注入。不创建官方版本、tag 或 Release。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 已实际 delivered，result_id 为 delivery:80413052748afecc65622a38cab283aba69352bb。合并 main run 39251774587 的三系统检查均成功。Windows 额外会话 run 39248964165 超时600秒，无工具调用，仍未通过。不能用绿色产品检查关闭整体 Task。

本地探针证明 qwen3:4b-instruct 可以调用工具，但会误填路径、authority、资格决策和命令，并把非零 wrapper 结果误述为成功。临时 clean repo 没有 HEAD，所选 Skill 的 live Git 校验返回 stale_identity。原采集器同样未准备请求草稿和初始 HEAD。这些是验证前提或模型错误，不能作为新的 Guru 路径产品缺陷。

依赖现有 driver 已成功建立的真实安装、Git for Windows Bash、官方 Codex CLI 和 Ollama。模型下载和本地预检不构成 Windows 验收。整体 Completion 仍须复核 AC1–AC10、真实 Windows 结果及长期 Test 证据，再执行 Closure/Finish；本批合并不自动完成 Task。

## 4. 本批调用方、场景与流程

| 场景 | 前置、动作与观察 |
| --- | --- |
| AS1：CI 维护者启动 | 以产品检查成功的候选安装建立隔离配置和非敏感请求，经公开 Codex 会话启动，观察自动 bootstrap |
| AS2：模型执行 | 当前 Agent 读取完整写作规范、trellis-start 和所选 Guru Skill；实际执行 startup、观察 runtime/正常路径，再独立判断并执行 wrapper |
| AS3：正常错误与超时 | 保留命令失败、错误输入、blocked、超时及未完成；不得声称通过；到时终止临时进程并保存 rollout |
| AS4：维护者验收 | 审查真实工具调用、自动上下文、输入事实、语义一致性和 wrapper 结果，在唯一 Test 记录证据与限制 |

## 5. 完整行为、条件与约束

AR1：保留正常入口自动加载，不手工注入 workflow，也不以直接 hook 代替。明确 CLI、公开命令、hooks 开关、来源审阅与一次性 trust 前提。

AR2：独立 CODEX_HOME，不复制维护者登录或凭据。本地模型不要求 OpenAI 账号，必须能实际执行工具和所选 Skill。环境不合格保持未验证；宿主不得提供候选决策、witness、gate 或 typed exit。

AR3：按当前 Skill 合同准备真实请求和必要 Git 前提。草稿保持 draft 身份，不伪造活动 Task。使用真实原生路径和已激活 managed runtime，不支持臆造的 root: 前缀，不改 validator 接纳错误输入。

AR4：startup 命令、完整合同/schema、base_selection.py、qualification_facts.py 和所选 Skill runtime 读取、正常操作观察和 stdin wrapper 调用均须能在原会话中核对。若前一轮缺少程序步骤，则经公开 codex exec resume 在原会话接续，并共用原600秒截止时间；不能通过提示指定语义结果，不能把缺失动作补成宿主执行证据。

AR5：单次会话最长600秒，不恢复45分钟超时。依赖安装/下载与模型执行分别记录。失败、取消和超时不算通过。保留 Windows 子进程清理、日志/rollout 保存和临时模型清理。

AR6：分别报告本地预检、原生 Windows 会话、脚本/安装及整体 Task 完成。实际结果唯一写入 docs/requirements-design-test-contributions/630-native-compatibility/test.md；使用说明写入 docs/ci/README.md。不制造第二审计状态或推广新的 shared authority 版本。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口、输入与预期观察 |
| --- | --- |
| AA1 | 本地独立 clean 安装预检；模型实际完成工具、startup、AR4 指定文件的读取及正常 root 观察、独立判断与 wrapper；pwd 成功不代表完整 Skill |
| AA2 | 现有 targeted-ci dispatch 原生 Windows；真实安装、独立配置、公开启动和真实请求；rollout 可见自动 Guru bootstrap、workflow/平台入口、真实 Skill 调用及语义一致的结果 |
| AA3 | 真实 collector；600秒上限、失败保留与清理有效，不上传凭据、模型或临时二进制 |
| AA4 | 对应代码定向回归和真实运行；文档/唯一 Test 写清命令、版本、退出码、失败历史及边界；D1 三系统结果保持适用 |

未决技术项为能在600秒模型执行预算内完成所选 Skill 的本地模型和提示组织，由 Author/实现 owner 通过真实预检选择。不要求用户提供模型或账号，不预填成功。未取得 AA1 前不重复启动 Windows 验收；AA2 未通过时整体 Completion 保持未完成。

## 7. Canonical 引用与本轮差额

docs/design/current/native-compatibility.md 的 D630-06 已规定 CI 只收集执行事实，模型独立判断；本批沿该责任修正环境前提。docs/test/current/native-compatibility.md 的 T630-08 继续拥有 Windows 会话要求，唯一 Test 单写结果。docs/architecture/README.md 当前 .103 及 distribution/ownership authority 沿用 D1 结论，适用性由原 Architecture owner 独立判断；不为新 Delivery 身份制造晋升。quality-guidelines 的 Validation Scope Ownership 保持定向边界。无公共 API、Task 状态模型或业务数据迁移。
