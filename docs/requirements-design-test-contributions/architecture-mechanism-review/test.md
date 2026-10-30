# 机制审核实施验证

观察截止点：本轮两项缺口修正、V2 原生复核及本 worktree 安装读回已完成，尚未进行重绑后的候选检查与最终晋升。前两节保留修正前的实际观察；本轮结果在「缺口修正与当前观察」。后序正式检查与晋升由原 public result 承接，本文不追写自己的最终通过。计划在 D1 implement/design，当前 Test 策略在本贡献完整拟写，不以计划填通过。

## 原生案例：修正前观察

V1/V2/V3 使用原 Architecture adapter，V4 使用原 Completion adapter。原/新每组各一次，共八次；事实、host 预期和有效配置在改方法前冻结，受测输入不包含预期、另一侧输出或轨迹。原规则为 B=`2f70796103406683a2f63adfb6b54d247a7433a5` 的真实正文。共同事实 v2 与冻结原预期位于 repo 外运行目录 `guru-mechanism-comparison-hvlgeh4h`；实际配置为应用内 codex-cli `0.165.0-alpha.1.2`、gpt-5.6-sol/openai、reasoning effort none、approval never、原 workspace-write 隔离、`--ephemeral --strict-config` 起点，permission probe 通过。原/新方法还未形成完整可比语义结果，不报告改善。

首次 PATH CLI `--version` 返回137；原 runner 第一轮因缺少 external isolated CODEX_HOME 未进入模型执行。恢复后 V2/V3 暴露 fixture 缺 mandatory descriptor，按原2.0事实补齐并对两侧使用共同输入。随后 V2 原Agent因 Interface 声明的 consumer projection 不在模型投影内而返回 blocked；源包文件实际存在，该轮保留为运输缺口，正在修正。

V1 原侧实际拒绝无依据的 page/quote 签名、保留真实 export 保密；V4 原侧识别同 Task 的旧 writer 适配尚未实施并返回 remaining_work，明确不是外部补证。它们的这些能力属于原有能力。完整原生输出与新侧逐次核对结果如下；host 固定预期出口不匹配不独立构成语义错误。


### 逐组实际观察

主会话逐份读取实际 transcript、AI 自己编写的 owner gate/Completion review 和 wrapper stdout，再与冻结 host 语义期望对照。runner 的 `evaluation_failed` 若仅因缺少外部 semantic grading 或固定出口不匹配，不独立代表错误；下表由实际内容判断。

| 案例与实际轮次 | 原方法 B | 新方法 | 证据支持范围 |
| --- | --- | --- | --- |
| V1 `old-v3` / `new-v3`，case `native-mechanism-cursor` | `architecture_conflict`，wrapper成功 | 同出口，wrapper成功 | 均指出page签名/精确签发限制无依据、quote已有完整摘要/归属/过期保障、export真实保密必须保留；拒绝两个不合适候选，认可保留现状候选。属于已有能力。此前old-v2选定可行候选后返回baseline_current，不以出口差异判错 |
| V2 `old-v3` / `new-v3`，case `native-mechanism-coordination` | `fitness_regression`，wrapper成功 | wrapper拒绝：blocking failed check 与 baseline_current 自相矛盾 | 均实际指出跨账号共享revision在配置稳定时造成首次竞争失败、重试恢复不消除代价，保留库存全局约束，指出去协调替代仍缺disable提交校验/同账号幂等。新侧具体原因判断可观察，但正式结果未成立，不能算完整语义通过 |
| V3 `old-v3-r1` / `new-v3`，case `native-mechanism-reuse` | `fitness_regression`，wrapper成功 | `baseline_current / architecture_impact / legacy_boundary_convergence`，wrapper成功 | 均识别无diff Utility被新search采用仍须重审、可比较去AES/协调的替代、同类export论证仍适用、无完整消费者/窗口证据不得删recovery-cookie。新侧要求经贡献生命周期修订过宽旧技术条款。只证明本planning候选的具体判断，不把不同出口推为收益或证明后续Author/实施正确 |
| V4 `old-v4-stock` / `new-v4-stock`，case `native-stage-mechanism-stock` | `remaining_work`，wrapper成功，239119ms | 同出口，wrapper成功，295898ms | 均识别同Task旧writer未实施、后继Delivery不抹责任、代码缺失非外部证据；均具体判断search独立共存、owner/D2、零旧客户端触发、退出证据，export现有保密依据仍成立。属于已有能力；本次数值不构成性能比较 |

V4首轮旧/新仅判断R2未完并将其它路径判scope外，不能证明后两类存量处置。复核确认可见trace没有进一步AI判断；不能从读取事实反推。原Author在已接受V4责任内修正synthetic scope：只追加R3处置评估责任，保留实际迁移实施在范围外，不给处置答案。原R2及files/观察/required_reads保持，`frozen-corpus-v4/frozen-inputs-v4.json` 记录该差额，双方同输入重跑；不重复其它组。

V3 old-v3曾裸调 `helper invoke --stdin`，未管道JSON，也未发送wrapper请求。保留执行错误，同B/事实/配置fresh一次后得到上表原方法结果。新V2首轮正式封套矛盾；`new-v3-r1` 又裸调stdin而未发送wrapper，仍为execution gap。原native使用ephemeral会话、明确不支持resume/fork，FIFO响应后关闭，没有现成同owner继续入口；没有主机补写owner结果、替换出口或继续fresh抽样挑绿。

事实依次冻结为v2（补原mandatory descriptor）和仅V4的v4；共同运输v3补Interface已有output/consumer schema本地闭包，保留原必读语义。方法未因观察结果改变，原B和10份新方法分别在old-rules/new-rules及 `final-execution-config.json` 校验；host原期望保留。raw与客观索引在repo外 `guru-mechanism-comparison-hvlgeh4h`，包括 `execution-index-v3.json`、首轮目录及恢复轮。原/新基础各一次之外的运输修正、普通调用恢复和V4输入修正均已逐项披露；不把附加轮当独立样本统计。

在本节截止点，四组可见语义支持上述具体能力，未显示普遍改善。V2新侧缺有效正式结果，D1-AC6尚未全部满足；没有用静态规则、相同出口或后来绿色取代该缺口。

## 工程与分发：修正前观察

| 检查与实际入口 | 结果及范围 |
| --- | --- |
| Architecture `unittest discover` | 47 项通过，146.590s；显式使用 Fork 工作目录（HEAD=`17015f987166f4106034f115d23212446f16d536`）现有 CLI `0.7.0-castbox.6` 的 `dist/templates/trellis/scripts`；后续发现dist中stop条款落后src，本检查不证明完整锁定构建一致 |
| Protection/root `unittest discover` | 9 项通过，6.569s |
| Completion `pytest -q .../tests/test_completion_contract.py` | 21 项通过，19.22s；显式设置同 Fork 的 `TRELLIS_DELIVERY_API_COMMON`，pytest 依赖放 repo 外临时目录，仍用原受管解释器 |
| 原 adapter 运输检查 | 原 Architecture 10项、三项本批运输通过；V4 scope修正后的三项运输再执行通过（36.641s），真实Task PRD接收源scope并以actual revision绑定。主会话已读代码和实际执行者输出 |
| source `check-skill-packages.sh --root . --mode source --json` | passed，40 active packages / 125 commands；是公共包结构与声明检查，不是语义证明 |
| 语法与上下文 | 362 个 Guru Python 文件及四个改动 adapter 文件语法通过；`task.py validate` 通过但指出写作规范/Architecture合同超过32KiB注入上限，执行者已显式完整读正文，不能以截断注入代替；`git diff --check` 通过 |
| 一个代表 installer fixture | 复用原 `PlatformOverlayInstallerTest`，真实 `install_assets` initial/reapply 通过；22个平台标志，本次10份方法与8个wrapper每轮360次字节/权限比较通过，用户文件保留，零 `.new/.bak`。runtime bootstrap由原fixture供给，只证明本批资产投影，不是全CLI init/update或完整Release矩阵 |
| 本仓 `apply.sh --repo . --json` | 被原 `upstream_delivery_migration_required` 阻止，原因是现存历史schema1 Task需原迁移；没有修改历史或手工覆盖受管副本 |
| 本仓 overlay drift 与 installed package check | 两命令返回通过，但只证明其现有覆盖：overlay与当前安装manifest自洽。实际比对 Architecture contract，canonical为新正文，installed/shared/Codex/Claude/Cursor仍是B旧正文；因此不能声明本批dogfood已采用或source/installed一致 |

首轮 Architecture 测试未设置上游路径，随后误选当前 `.trellis/scripts` 缺包层级，均在fixture起点失败；改为上述真实锁定构建产物后47项通过。Completion首轮缺pytest，补临时依赖后因未设COMMON而2 passed/19 skipped；设置真实COMMON后21项执行并通过。以上不是规则语义失败，也未将跳过记为通过。

候选 Check、原 owners 最终整合/读回、实际 after 重绑、最终 Check、commit 与完整 committed Review 尚未发生。本仓分发缺口仍未满足本批验收，独立fixture通过不能替代。

普通apply的错误提示不自行证明历史Task必须迁移。已只读核原 `guru-upgrade-tools` 的tools-only入口并preview，确认其可保留Task/session，但当前本机Fork dist落后src：预览要求更新 `.trellis/scripts/common/delivery_operations.py` 和 `.trellis/delivery-contract.md`，实际会回退已有stop例外。该原工具/构建差额超出本批方法与投影同步，未prepare或执行，不修改官方资产、不改历史，也未预设采用全量迁移。安装维护与本批源码验证分别处理。

## 缺口修正与当前观察

原独立 Architecture 对前述候选正式返回 blocked，原因是 V2 新侧无有效 wrapper 结果与本仓仍采用旧正文。本轮保留该结果及原失败，先完成工具采用，再按原 Check public rework 回到 implementation 修正实际候选；没有将 blocked 或安装结果改称 Check 通过。

V2 trace 显示两处可定位问题：`new-v3` 以 Planning 不晋升 shared current 为由，把 authority 仍 current 与 candidate 可接受混在一起；`new-v3-r1` 的裸 stdin 命令没有传 JSON。原 normal、solution、root 资格判断均已实际调用，允许在 P4 既有范围内作最小修正和一次原路径验证。Architecture Planning 3.0 增加身份有效、审查完成、候选可继续三者的区别；原 adapter 在已有 heredoc 示例旁解释 stdin 必须接收 Agent 自己编写的 JSON。未修改 schema、validator、typed exit、事实或 host 预期，未新增恢复框架或镜像文字测试。

| 实际检查 | 本轮结果与边界 |
| --- | --- |
| V2 `new-v5-v2` | 同冻结 v2 事实、原有效模型/权限配置，仅执行一次。native return 0，原 wrapper return 0，正式 `fitness_regression`。Agent 说明新入口把共享 Offer revision/CAS 扩到独立账号，稳定配置下其它账号写入仍可耗尽8次重试；竞争停止后成功不取消首次代价。它同时保留独立库存的有限存量不变量，指出候选 B 仍缺 disable 提交期校验，候选 C 不应移除库存约束。主会话亲读实际判断、AI 编写的管道封套及正式 stdout；没有主机代写或追加抽样 |
| 实际方法采用 | 本轮 Planning 段在模型实际投影中、stdin 说明在原调用上下文中；permission probe return 0。V2 两份输入与冻结 v2 相同，case 行和 host 原预期保持。原/新具体机制判断均正确，不能据本轮成功或相同出口宣称普遍改善 |
| matching 构建 | 原 Fork `17015f987166f4106034f115d23212446f16d536` 经 git archive 固定到 repo 外，原 Core→CLI build 成功；CLI/Core 同为 `0.7.0-castbox.6` 且真实解析同一临时 Core，212 项模板 src/dist 字节及权限一致。未修改原 Fork、全局包或历史 Task |
| 本 worktree 采用 | 原 `guru-upgrade-tools` tools-only 事务实际返回 `tools_upgraded`，installed version `0.7.0-guru.7`。首轮10份正文在 installed/shared/Claude/Codex/Cursor的50次字节及权限比较一致；随后新8行方法与1行调用说明沿新的同范围原事务同步，6份内容投影及 installed adapter 语法通过。正式源锁仍是 `formal_fork_source_lock` 未验证，不冒充 release proof |
| 保留与目标入口 | 首轮2802项 Task 文件与307项peer/common pointer字节及权限保持；后续事务的Task/AGENTS/config与305项操作期pointer保持。本仓 `.trellis/.runtime/sessions` 无普通文件；未取得首轮独立common session/branch-binding前快照，不补称逐字证明。较早快照的并行peer/session变化不在本事务写集合，也不据此归因于安装或修改其它会话。目标自身resolver、native continuation和runtime合同可执行；主会话的public current仍为本Task/Delivery，合法rework后phase为implementing |
| 定向检查 | 两轮 installed package check 与 dogfood drift均通过，40 active packages /125 commands，0 conflict、0 sidecar。原逻辑测试事实继续按未变依赖承接；此次adapter只增调用说明，AST通过。未运行CI、镜像或完整Release矩阵 |

本次 runner 仍返回 `evaluation_failed`：冻结 host 期望 `architecture_conflict`，实际为 `fitness_regression`，且未附外部 semantic grading。主会话依据原始理由及合法出口判断本案例满足机制区分和正式调用要求，没有将 runner 改记绿色，也没有修改预期。117008ms 只记录本次耗时，不作性能比较。

原始记录、实际配置与客观索引保留在 repo 外 `guru-mechanism-comparison-hvlgeh4h/new-v5-v2/`、`new-v5-v2-config.json` 和 `new-v5-v2-index.json`；安装实际 frozen plan 与输出在原临时构建根及 `v2-delta/`。本轮补齐两项原阻塞所缺的工程与行为事实，完整候选是否可通过仍由重绑后的独立 Architecture 与原 Check 判断。六个 RDT 和一个 Architecture proposed 在该判断前保持未晋升。

## 证据限制

单次/侧支持所执行案例观察，不支持统计改善或普遍纠偏结论。执行失败不评为语义通过；两侧都正确记已有能力。源码、分发、真实 Agent 行为、业务安装采用及生产效果分别报告。本项不证明后端去密钥、业务迁移或生产效果，不运行完整 Release/多平台升级矩阵。
