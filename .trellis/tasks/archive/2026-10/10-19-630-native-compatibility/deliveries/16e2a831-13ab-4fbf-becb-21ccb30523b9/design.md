# D1 三系统兼容修复设计

## 1. 设计目标、需求承接与内容基线

承接本批 DR1–DR12、DS1–DS9、DA1–DA11。保留已实现的精确选择和诊断，补齐标准 Merge 必需的产品兼容检查。Task 没有前序 Delivery。development baseline B 固定为 main `0543731bf52aa80842fde5db47332380de513cf0`，来源为原显式基线；原 Planning H0 等于 B，当前修订观察 HEAD 为 `10da9be7c976ac210ec3a8afc42077f5e709bd7f`。内容范围仍为 B...最终 HEAD，PR #634 目标 main，不能把当前观察当最终实现。

本轮实际 Architecture candidate_assessment 返回 architecture_impact/target_native，baseline=`current-main-0.7.0-guru.102`、constitution=`guru-trellis-design-constitution-v1`。适用合同为 docs/architecture/06-governance/change-contract.md。受管文本 LF 策略与精确 EOL 恢复需要真实贡献和 ADR；不复用原纯 CI no-impact 结论。Windows Codex 实际会话与官方发行继续作为整个 Task 的最终完成条件。

## 2. 当前系统、边界与目标差额

现有 ci/unittest_report.py 已支持文件::用例，ci/runtime_diagnostic.py 已观察目标固定 capability fixture。run 39223843984 证明三系统 driver 通过；Windows 原 fixture 的裸 bash 实际进入 WSL，macOS/Linux 原安装通过。本轮修复目标 fixture 的真实调用，不让 driver 替换产品。

base_selection.py 的 Git root 字符串比较、schema.py 的 file URI 转换、TaskCommit execute.py 的默认编码读写与 installer 原 raw hash 路径是实际修改点。正常初装后以 core.autocrlf=true clone 已重现 installed validation 漂移和 reapply conflict；两个历史 CRLF 摘要能由该正常流程产生。源码锁仍为 Fork .4，目标接入已发行的 .5。

不新增公共 Skill、exit、用户授权字段或持久化诊断 authority。不管理上游 trellis-* 资产，不修改全局 npm/node_modules。existing manifest、依赖 lock、二进制与 Git candidate 身份仍按原始字节校验。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置与正文落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #630 R1：系统路径身份、Windows file URI/相对引用 | retain；第4节 D1/D2 | 使用标准 Path/url2pathname，继续区分不同 checkout |
| #630 R2：真实 Python→Bash→managed Python、保留公开输入 | retain；D3/D6 | 绝对 Git Bash、POSIX path、stdin JSON仅修fixture；公开inline形式保留 |
| #630 R3：UTF8及候选字节，不忽略Git错误 | retain；D1/D3/D4 | 显式协议编码及消息字节/最终commit核对；保留hook与index检查 |
| #630 R4：--python单executable、仅python3 Unix、上游py -3分责 | retain；D3/D7 | 不全局替换python3，不解析任意shell命令；#53负责原生选择 |
| #630 R5/R6：正常换行可恢复、用户编辑/精确身份保持 | retain；D5 | raw校验保持，限定声明文本可精确恢复；新ADR说明旧规则窄替代 |
| installer.md/upstream-ownership.md：只有raw等canonical/previous才更新 | change；D5及architecture-adr.md | 在现有owned inventory内增加精确CRLF→LF恢复条件，恢复后仍raw校验。#630正常复现提供必要性；Phase2原Architecture晋升后生效 |
| 两历史提交的python3→python大范围替换与active pointer改写 | reject/retain-equivalent；D3/D7 | 既有显式选择及pointer.as_posix已承接，不复制76项替换或重复patch |
| C1 base_selection/bootstrap、C2 schema/message修改 | change；D1–D4 | 吸收行为，采用本仓真实owner和完整读写/传输修复，代码和原生证据逐项记录 |
| C2 checkout-index --index | change；D4 | 先经正常真实TaskCommit fixture判断。确有必要才采用，否则保持并说明排除证据 |
| #630/#631：独立driver/target、基线具体失败、matcher不接受任意安装错误 | retain；D6及第8节 | 复用原三系统runner，安装日志独立验收，不削弱门禁 |
| #53/README当前来源维护：fixed source、正常workspace build、实际采用 | retain；D7 | 固定7f050fa及.5，遵循selected source自身pnpm lock；不改上游生成资产 |
| #630：Windows Codex真实自动加载/Skill、hooks前提、全部完成后发布 | retain；第7–8节 | 真实会话单独验收；直接hook或静态投影不替代，环境缺口阻塞最终Completion |

## 4. 模块、职责与设计取舍

### D1 路径与 Git 协议

base_selection.py 原 owner 对 rev-parse --show-toplevel 的有效输出构造 Path 并 resolve，再与当前root按本机语义比较；authority_checkout同样处理。未处于repo或输出为空时保留原错误。Git文本调用显式UTF8，保持returncode/stderr；不ignore错误、不做斜杠替换。真实中文/空格root及注册worktree通过原入口验证。

### D2 Schema URI

schema.py 将 file URI 的path经标准urllib.request.url2pathname转成本地Path，保留schema本地相对引用与错误合同。使用真实盘符、中文空格路径和相对$ref验证，不能只测试路径对象。无需新URI协议或远端schema能力。

### D3 Bootstrap 真实 transport

bootstrap_check.py 在Windows明确定位Git for Windows安装的bin/bash.exe（从实际git来源及标准Git安装路径定位），运行uname验证MINGW/MSYS。Unix沿PATH bash并保留缺失失败。调用使用验证后的绝对Bash executable，wrapper与pointer/cache路径按POSIX表示传递；JSON由原--invocation -读取stdin，子进程文本按UTF8。只从固定manifest cases转换其已声明--invocation JSON参数为--invocation -并将相同JSON传入stdin，其他参数保持；不删公开inline入口，不引入通用shell parser。指针JSON和fixture文件显式UTF8写入且LF；激活前失败继续不改变旧pointer/环境。具体来源解析放同职责小helper，避免重复跨系统选择实现。

### D4 TaskCommit

execute.py 对message采用明确UTF8字节写入与按同协议读回；换行不能由系统TextIO改写。最终Git commit验证继续比较原candidate消息。保留真实hook执行、transaction index/tree、live ref检查及清理。真实fixture覆盖cp1252/UTF8模式关闭、中文消息、消息被hook改动；checkout-index调整仅按正常fixture实际失败决定，不随历史提交附带采用。

### D5 受管文本 LF 与恢复

由现有installer唯一管理。canonical .gitattributes只声明Guru source目录的明确文本类别为text eol=lf；依赖lock和二进制保留自己的精确策略。目标attributes通过现有安全配置维护方式增加有界Guru块；规则只覆盖实际installed inventory、Guru namespace与明确managed spec，不覆盖整个平台root或trellis-*。保留用户块外原始字节，无法合并/冲突时报告并停止激活，不无条件覆盖。用户拥有.gitattributes整体；bounded block是唯一受管区域，不把该文件列成整文件managed asset。

新cohesive installer helper负责文本类别、attributes块及EOL等价判断，原2941行installer仅接入；不把其继续堆至3000行。限定文本包括Guru的Markdown、Python、shell、JSON/schema/config-template及受管spec；lock和精确字节身份文件显式排除。安装复制/生成写LF，manifest仍sha256(actual bytes)，validator仍读raw bytes。目标checkout在attributes生效后保持LF；更深目录attributes产生真实冲突则不能声明稳定通过。

旧目标恢复只接受声明文本且current.replace(CRLF,LF)精确等于canonical LF bytes，或其raw hash精确等于current manifest记录的previous-managed hash。后一条件只证明同一受管旧内容的换行差异，不猜旧版本正文、不新增旧源码cache。canonical-equal恢复不制造内容升级；旧受管内容升级保留原.bak规则及原字节。其他未知差异继续.new和阻塞；原.removals及sidecar规则不扩大。不能仅重算manifest接纳漂移。恢复完成后执行原raw installed validation，不给validator增加宽松等价分支。

### D6 CI 观察与专项 driver

保留file::selector和原失败继续行为。diagnostic按目标实际声明的transport观察：旧target bare bash/inline、新target绝对bash/stdin均可识别固定wrapper cases。记录真实stdin/encoding所需非敏感fixture信息；supplemental使用该target相同transport/cwd/env，仅补余下声明case，保留原first error。目标新helper可被driver调用来构造剩余case，但不得以candidate helper替代baseline。独立compatibility driver通过target import/公开wrapper/真实Git fixture验证产品，不能复制候选实现进基线。适用专项接入原targeted_ci入口，当前候选失败仍使检查失败。

### D7 固定上游采用

source lock更新到7f050fa11ddd8569e5db4f728ea1b745b7500a98，tree/parents/CI由真实GitHub事实确定，CLI/Core .5。使用该commit干净workspace及其pnpm@10.32.1 frozen lock正常build并记录.guru-source-commit。三系统clean init、随后新进程update/maintain tools_install→Guru apply/reapply，核对实际版本及原生解释器argv；Windows用上游合法py -3场景和Guru单executable路径分别验证。同provider/template preview --create-new后显式--force应用；成功工具安装原recovery_ref以新进程recover/resume核对幂等。不patch生成上游入口；具体命令以固定CLI --help合同为准。

## 5. 接口与数据

公共Skill输入/exit、managed-runtime identity、Task/Delivery模型均不改。file::selector是已有本批新增CI语法；diagnostic报告继续分driver/target identity和original/supplemental结果，增加transport事实只供诊断consumer。source lock保留现schema。manifest/hash不增加第二文本摘要authority。installer报告沿现有操作/冲突结果表示attributes与EOL恢复，具体字段仅在确有直接consumer时使用，不记录授权。

## 6. 状态、顺序、正常与失败流程

先完成本批Planning→独立final-plan→Approval→Activation。实现D1–D7后收敛RDT差额，独立Phase2评估完整候选及真实贡献/ADR，再由原Architecture owner串行晋升共享authority、核对实际落盘，之后最终Check、TaskCommit、完整committed Review、Publication更新原PR和原生CI。当前候选原生检查全部通过后才Merge。

安装仍是source/ownership校验→准备runtime并执行真实wrapper→staging→managed配置/字节投影→原installed validation→激活。Bash/解释器失败、schema错误、unknown edit、sidecar保持原非零和旧pointer。CRLF-only恢复仅在D5精确条件成立时执行；无法证明就走原conflict。缺原生环境或Agent认证记未验证，不能改matcher/放宽Check绕过。

## 7. 恢复、兼容、迁移与集成

同一Delivery/PR保留，不新建切片掩盖失败；标准rework已回planning。受管文本在本版本apply/reapply时迁移；不迁移业务数据或Task状态。未知用户attributes/内容修改原样保留。日常wrapper仍只用activated runtime；显式安装选择失败不fallback。公开inline参数兼容保留。

Windows Codex验证使用独立配置与安装候选；固定实际CLI版本并记录公开codex exec/交互入口、hooks开关与原生一次性启用/审阅前提，选择guru-bind-task-session的正常只读resume/explicit模式或另一个无外部副作用的已安装Guru Skill。必须由正常会话自动加载workflow/平台入口并实际路由调用，不能手工注入文本或直接hook代替。当前未具备Windows认证；不复制维护者凭据。该环境缺口不阻塞独立产品修复，但阻塞Task最终Completion与官方发布。

## 8. 验证设计

| ID/对应验收 | 入口与输入 | 预期观察和边界 |
| --- | --- | --- |
| V1 DA1–DA5 | 原driver七项回归及目标真实diagnostic | 精确选择、旧入口、失败继续和transport记录保持；基线失败保留 |
| V2 DA6 | 独立driver载入目标base_selection/schema；真实中文空格repo/worktree、相对$ref | 原生Windows基线命中路径/URI偏差，候选成功；Unix正常结果保持 |
| V3 DA7 | 三系统既有targeted-ci clean安装与安装后wrapper两manifest case | 成功0/普通schema2和JSON；明确Git Bash，不能WSL；原输入形式兼容 |
| V4 DA7 | 既有bootstrap定向失败/显式解释器fixture、Unix仅python3可见性 | 真实解析命令、缺失失败与旧pointer保留；mock单测不替代native |
| V5 DA8 | 隔离repo真实TaskCommit execute入口，Windows cp1252/PYTHONUTF8=0，中文消息与真实hook | 候选文件UTF8 bytes、读回/最终commit一致；修改检测与index/hook保持 |
| V6 DA9 | 正常Git clone core.autocrlf=true/false；真实preset apply→commit→clone→validate→reapply | LF策略稳定、旧CRLF精确恢复、真实编辑.new、原.bak及user attributes保留；不造manifest |
| V7 DA10 | 固定.5正常build/CLI init、new-process update/maintain、preview/force/recover/resume | 来源及目标实际身份、解释器argv、sidecar与真实入口；不以source lock替代安装 |
| V8 DA11 | canonical/source/installed、ownership、声明投影、apply及drift检查 | dogfood匹配，零未解决sidecar；只跑本Issue相关组合 |
| V9 整体AC7/AC10 | Windows实际Codex会话与official release owner | 真正自动加载/Skill与单独发行证据；本批代码合并不预填通过 |

原生runner沿windows-2025、ubuntu-24.04、macos-15，记录实际镜像/OS/Python/Git/Bash/locale、driver/target/upstream SHA、命令/返回码及Actions artifact。不同缺陷基线可以不同，但必须命中具体机制。安装失败独立对照，不强求expected unittest matcher建立。

## 9. Canonical 引用、本轮差额与实际未决项

installer.md/upstream-ownership.md的精确字节规则按D5和ADR窄替代；runtime/TaskCommit测试与使用文档同步。Architecture task-owned贡献为同目录architecture-contribution.md及architecture-adr.md，现为proposed，目标共享domain/distribution/current及必要ADR由原Architecture在独立Phase2后晋升，不在Planning直接修改shared current。RDT原owner在最终Phase2前判断并收敛docs/ci、安装、源码采用和测试差额。

无需求选择未决。checkout-index必要性与原生产品证据由实现/测试确认；若机制改变，回最早qualification/Architecture owner。Windows Codex认证/启用仍为真实外部缺口，不能声明完成。官方发布继续由release-guru-trellis-version独占，未满足整体验收前不创建正式tag/Release。
