# 独立审查启动与恢复整体需求

## 1. 来源与术语

| 来源 | 章节及角色 | 用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/929 | 交付范围与行为要求、可执行验收：requirement | 本Task完整范围与验收 |
| 同Issue的“已核对事实与因果链”“来源讨论附录” | 历史事实及证据 | 说明实际失败、来源限制及状态纠正，不替代本次验证 |
| 同Issue的“候选改进与待定问题” | advisory | 规划比较方案，不预先接受writer拆分或沙箱参数 |
| trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md#independent-assessment-entry | 当前设计约束 | 保持独立性、authority首读及各purpose合法入口 |
| trellis/skills/guru-team/packages/guru-review-branch/references/contract.md#single-post-commit-independent-review | 当前设计约束 | 保持一次独立双槽判断、同候选恢复与适用工程证据复用 |
| docs/requirements-design-test-contributions/679-session-continuation/test.md | 历史证据 | 同类common-dir失败与额外写范围后原生成功，不推断本Task已通过 |

reviewer指实际作独立语义判断的Agent；writer指现合同声明的正式结果/会话写入owner。执行条件预检只判断能否运行，不是质量门禁通过。B/H为固定候选基线与提交。

## 2. 背景与问题

linked worktree之外的Git common-dir保存正式session。来源案例通过workspace-write启动独立CLI，未配置额外目录。reviewer完整读取固定B三份authority后，Identity/Ensure通过，Bind返回official_session_write_failed，未调用正式Architecture或Review。原CLI正常退出不等于审查通过。

后续发生prelude包含当前任务叙述的worker报告、其他Task历史pass误判、嵌套调度长时间无结果及更换reviewer，放大前置读取与恢复成本。源侧临时会话无法取得完整逐字记录；原始启动与部分结果已在建单时只读核对。固定B三份authority为2935/165/170行，共3270行；不能以当前文件行数替代。主会话后来报告独立审查通过并发布PR，故“尚未返回”仅是历史状态。该后续成功不证明Guru已修复。

当前adapter将projection读取、旧session读取和写入多类异常合并为同一错误码，底层I/O也可能只返回False。current final_plan已有显式对象只读特例；正式branch_review仍需合法绑定与选择。现有一次独立审查、同reviewer续审及测试事实适用性规则保留。

## 3. 目标与非目标

目标是在声明的候选只读/最小必要元数据范围内，独立审查从启动走到真实正式结果；执行条件失败尽早定位；普通中断或结果写入失败后延续同候选的有效工作。降低重复读取与无变化等待，不牺牲完整authority、独立判断和合法writer。

本Task只承担Guru的workflow/Skill/preset/runtime及采用指引。排除原后端源码、业务Task/session、Mongo、进程和部署；排除Codex/provider上游修补、多模型矩阵、通用调度/遥测/缓存切片、审批链或ledger、授权持久化、攻击/伪造/故意绕过、压力竞态和非常规crash/fault矩阵。普通范围只做必要受影响投影/reapply/drift验证，不继承完整Release/多平台安装矩阵。

## 4. 真实调用方、场景与流程

S1：协调者在linked worktree派发fresh reviewer。先检查实际prelude、B/H可读、checkout与职责读写能力；失败定位原owner且不进入昂贵读取，修正后同对象继续。预检成功后按authority-first读序作判断。

S2：独立reviewer对固定候选读取完整authority、diff及必要unchanged consumers，最后读取任务规划来源并形成独立判断；合法writer按最终合同将其投影成同Task/Delivery/B/H的正式结果。源码候选不变，协调者不得改造或自造pass。

S3：同候选普通中断、结果写失败或部分投影后，原owner恢复有效覆盖，合规reviewer优先继续；覆盖丢失补足必要判断，工程事实按适用性采用。实际未执行或无反馈时有界诊断再恢复/停止，不递归转派同一职责。

S4：架构入口含其他任务历史pass时，完整当前authority仍可取得，历史可追溯但不证明当前pass，也不一律判为污染。若入口组织变化，保留必要引用、旧入口兼容或迁移。

## 5. 行为要求

R929-01：大规模authority/候选读取前轻量核验执行条件。只读最小工程规则与对象定位，不提前引入任务叙述，不改变语义authority-first顺序；错误含真实原因和原恢复owner，不生成quality pass。

R929-02：正式review在声明权限内可完成。候选文件只读；元数据实际writer、位置与最小范围明确且实测。是否将语义review与writer分离由原Author/Architecture确定；若分离，先修订适用合同/public I/O/provenance，不借prompt绕过。实现者或协调者不能改写独立判断。

R929-03：同候选恢复保留实际覆盖、适用测试与原结果。只补缺步，未完成审查不恢复为pass；同一合规reviewer优先继续，更换时识别真实覆盖缺失，不无因重复gate、审批状态或全套测试。

R929-04：generic/CLI已承担审查者直接执行，不再转派同一职责。无反馈有界核对载体、阶段、阻塞/结果缺失，沿原blocked/re-entry；未知原因保持未知，不以无限等待/循环新开代替诊断。

R929-05：明确当前authority、导航、历史分工，完整取得当前适用正文，必要历史按影响可追溯。若拆分保留历史原文、引用、完整条件及入口兼容/迁移。不得用摘要缓存、已读证明或按路径剪枝替代必要authority；业务仓只给采用指引。

R929-06：保留official_session_write_failed稳定兼容，同时附最小脱敏技术诊断：操作、匿名化/相对位置、异常类别及可取得errno。区分实际projection/session读取、权限、路径、内容与写入失败，不把所有该码判为写权限。不得泄露凭证、业务内容或授权信息。

## 6. 约束与依赖

Markdown控制语义、范围和路由；脚本仅查询、执行、记录与机器校验。保留原Bind/Review/恢复owner及正式Task/Delivery/B/H关系，不能以脚本exit0、schema或绿色DTO替代语义审查。公共合同变化须明确迁移，canonical改动由合法安装owner同步dogfood/受影响声明平台并处理sidecars。

#912绑定/选择、#694受限final_plan、#794一次review、#578工程事实复用为已有能力；#651关闭为not planned，非CLI fallback交付证据。#721冷热缓存、#734预算治理及#363遥测独立，不作为本Task前置。官方Trellis扩展方式需在实现前核对官方文档，不修改上游源码、全局npm或node_modules。

## 7. 可观察验收与验证方式

| 验收 | 对应场景/要求、入口与输入 | 预期观察与边界 |
| --- | --- | --- |
| AC929-01 | S1/R01，在可丢弃linked-worktree通过真实支持载体启动，普通配置缺元数据权限及实际不独立prelude | 昂贵读取前给出具体原因/owner，无quality pass；修正后同候选继续，预检不冒充审查 |
| AC929-02 | S2/R02，固定B/H和正常owner建立的Task/Delivery，候选只读及最终最小元数据范围 | 实际完整独立判断与合法正式结果匹配；若纯只读reviewer，证明不写主仓.git且承接不改判断 |
| AC929-03 | S3/R03，同候选正常写失败/部分结果/普通中断后原入口恢复 | 已完成覆盖与适用工程事实采用，只补未完步；覆盖丢失真实补审，不空写pass/重复gate/无因全测 |
| AC929-04 | S3/R04，真实generic派发及代表未执行/无反馈条件 | 直接执行，不递归同职责；有依据诊断并恢复或停止，不无限等待或循环新开 |
| AC929-05 | S4/R05，含其他任务历史pass的正常authority入口 | 实际完整读取当前authority，历史可追溯且不冒充本次pass/污染；记录读取差异，不设节省比例 |
| AC929-06 | R06，正常入口代表性projection/session读写失败 | 稳定码兼容且最小诊断足以区分处理，不泄露敏感内容；真实sandbox及恢复须实际执行，unit/mock只证明该层 |

通过可丢弃代表场景和最小可靠集合证明，不操作原业务Task，不伪造artifact/pass。文字替换、字符串parity、exit0与fixture绿色不能证明真实Agent/sandbox。对平台注入不能复现时记录实际边界及外部owner，不虚报修复。全部验收与必要canonical/dogfood/受影响平台验证完成，并由正式Review/Completion核定后才能说明整体完成；部署及业务账号恢复不属于此完成条件。

## 8. 实际未决项

需求范围已明确，无需提交者补代码设计。Author/Architecture仍需核定保持原writer并提供最小范围，或正式分离只读语义review/writer的方案及兼容影响；该技术选型阻塞实质方案定稿和实施，不阻塞整体需求接受。

实际注入环节、嵌套worker无响应底因和目标Codex受保护.git最小写入能力尚未知；由本Task规划/实现owner有界调查影响方案的部分。缺外部事实时仅依赖项保留未验证，不能把未知写成模型/网络故障或已修复。此前#679已有额外范围成功是特定样本，不替代本Task环境验证。
