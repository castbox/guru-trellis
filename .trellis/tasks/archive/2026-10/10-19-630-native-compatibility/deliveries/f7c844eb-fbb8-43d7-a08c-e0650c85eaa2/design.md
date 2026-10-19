# D2 Windows Codex 会话采集设计

## 1. 设计目标、需求承接与内容基线

承接本批 AR1–AR6、AS1–AS4、AA1–AA4及整体 AC7/AC10。B=cc8f2564cf0a42bbd1209ec9da295412391082cb，来源为当前 HEAD 祖先中最近的真实已交付 D1 head；D1 merge 为80413052748afecc65622a38cab283aba69352bb。Planning H0=B，PR目标main，内容范围为B...本批最终HEAD，不重复D1产品修复。

实际独立 candidate_assessment 为 baseline_current/no_architecture_impact，baseline current-main-0.7.0-guru.103，constitution guru-trellis-design-constitution-v1。候选评估仅证明责任/机制适用性，不证明模型或Windows通过。

## 2. 当前系统、边界与目标差额

ci/windows_codex_session.py 已安装官方CLI/Ollama、隔离CODEX_HOME、验证候选安装、启用公开hooks前提并保存原会话。它固定qwen3:4b，单次执行600秒，没有真实draft和初始HEAD。首次错误agent_type已在D1修正；后续仍缺完整Skill执行。

本批只调整该collector、docs/ci/README.md及唯一Test证据。公共Skill、runtime、validator、上游hook/workflow、D1产品机制与既有三系统driver不改。文件/结果不成为新的workflow authority。

## 3. 来源设计处置（唯一）

| 来源、原承诺 | 处置与落点 | 理由与影响 |
| --- | --- | --- |
| #630真实Windows正常启动与自动加载 | retain；第4/6节 | CLI原入口、自动bootstrap和真实工具调用仍是证据 |
| 当前collector独立配置、本地模型、600秒与失败保留 | retain；第4/6节 | 无需维护者OpenAI凭据；不提高超时来制造可用性 |
| 当前固定qwen3:4b和单段宽泛提示 | change；第4/8节 | 实际会话无工具；选择经完整预检的本地模型并明确程序步骤，模型仍独立判断 |
| 正常场景Skill当前draft/HEAD/相对locator合同 | retain；第4/5节 | 补齐夹具，不改validator接纳臆造路径或活动Task |
| D630-06、T630-08：CI事实与AI判断分责、唯一Test | retain；第5/9节 | 宿主不提供semantic result，不用脚本通过代替模型证据 |

## 4. 模块、职责与设计取舍

M1：collector在现有实际clean install根目录创建非敏感请求草稿，内容只提出当前中文/空格路径是否需要额外修复的候选问题。通过正常git空初始commit建立HEAD，提交身份仅为fixture的命令局部参数，不配置维护者全局身份，不生成Task或业务提交。报告记录实际准备命令和退出码。任何准备失败停止会话。

M2：保留固定官方CLI0.163.0、Ollama0.40.6和独立模型缓存。当前4B/8B探针是候选，不因工具单步成功就固定采用。实现owner以完整本地预检选择一个可实际执行Skill的官方模型tag，再写入现有MODEL常量。使用官方provider/模型推理配置，禁止未支持参数和全局软件patch。预检不通过继续有界调查，不发Windows重复验收。

M3：提示明确当前Agent直接执行、Skill是Markdown。提供真实安装路径、原生Git Bash及安装解释器事实，要求读取完整写作规范/trellis-start、执行startup两命令、读取所选Skill完整合同/schema与实际draft/runtime、观察正常root行为，再自行选择decision/witness/gate/exit并通过stdin调用公开wrapper。可给出准确程序命令，不能提供或预选语义结果。若前一轮缺少程序步骤，则按公开codex exec resume在同一session接续，并共用原600秒截止时间；由宿主指定下一项尚未完成的程序步骤，不据错误模型陈述跳过动作。

M4：保留原始events、rollouts、命令、模型/CLI版本和真实退出码。collector的completed仍只是进程结束事实；原Task owner直接审查自动bootstrap、实际文件读取/正常观察、语义与stdout一致性。模型错误、非零wrapper和文字过度声明一律不当作通过。

## 5. 接口与数据

dispatch的windows_codex_session布尔入口、diagnostics/result.json候选输入、report.json和原artifact路径继续使用。增加的fixture命令事实只供报告consumer，不新增公共Skill/Task/schema或持久化资格结果。实际Skill使用standalone requirements_scope_set、caller guru-clarify-requirements、repo_locator为真实相对根、authority_kind=draft；其他语义字段全由模型根据当前合同填写。

request draft是输入，不含结论。资格envelope仅由模型在工具调用中通过stdin传递，不写qualification文件。原CLI运行记录是外部验证原始日志，不回灌为workflow判断authority。

## 6. 状态、顺序、正常与失败流程

候选产品检查通过→准备真实draft/HEAD→隔离配置与已审hooks→官方模型依赖准备→公开CLI正常会话→模型实际启动/读取/观察/判断/wrapper→保留结果→owner语义验收。每个依赖失败保留真实失败，不继续声称环境可用。

模型执行总预算保持600秒；若使用resume，多个调用共用同一截止时间，不能通过多次各600秒扩大为长会话。原依赖下载独立计时。到时按原Windows taskkill进程树终止，先保留rollout再删除模型/二进制。终止只控制临时资源，不作为业务完成authority。

## 7. 恢复、兼容、迁移与集成

没有业务数据/Task模型迁移；D1历史不重写。旧失败日志保留，各次结果绑定实际driver/candidate。正常重试新建隔离临时资产；同session resume只继续同次验证，不伪造自动加载或成功。未取得Windows有效证据保持整个Task未完成。仅collector/说明变化不要求重做累计installer矩阵；正常PR的现有三系统检查保持。

## 8. 验证设计

V1/AA1：本地真实clean安装、正常Git前提和独立Codex配置，观察完整Skill行为。逐项读取raw rollout，不以returncode0/pwd/模型文字替代。固定最终tag后再运行采用同一程序组织的新会话预检。

V2/AA2：通过现有targeted-ci.yml dispatch在原生windows-2025运行已发布的实际候选。核对自动bootstrap/workflow/平台入口、真实startup和Skill工具调用、模型独立判断及wrapper真实结果。保留OS/Python/Git Bash/CLI/Ollama/模型及run/artifact身份。没有OpenAI认证不构成本地provider失败解释。

V3/AA3：定向核对fixture命令失败不进入会话、总预算/剩余时间计算、原超时清理及rollout保存；已有真实600秒超时证据仍保留，只有新机制需要的新验证才重跑。不制造故障注入或额外压力测试。

V4/AA4：ci/test_targeted_ci.py驱动回归和collector的Python语法/调用检查，现有PR三系统checks；docs/ci说明实际使用，唯一Test记录最终原生结果和先前失败。未取得V2不能进入whole-task completed。

## 9. Canonical 引用、本轮差额与实际未决项

docs/design/current/native-compatibility.md D630-06及docs/test/current/native-compatibility.md T630-08已覆盖本批责任。唯一Test更新执行证据，不复制到新的贡献或推广RDT .113。Architecture独立候选无影响，沿原owner在final_plan/Phase2/Review核对实际实现，不为key/stage重复晋升 .103。

实现技术未决项为最终模型tag、是否需要公开resume以及程序提示最小组织。原I3 owner通过完整预检选择，若引入新authority/公共机制则回Author/Architecture；模型错误不能驱动公共validator修改。当前无产品范围选择。
