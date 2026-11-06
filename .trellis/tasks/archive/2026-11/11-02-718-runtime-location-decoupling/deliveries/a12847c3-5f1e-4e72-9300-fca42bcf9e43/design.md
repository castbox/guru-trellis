# #718 D1 设计：共享环境解析与明确 Git 基线

## 1. 设计目标、需求承接与内容基线

本批为 full D1，承接本目录 PRD 的 R1—R11、S1—S7、A1—A8。整体范围由 Task 根 PRD 的 accepted_scope 承载。没有前序 Delivery。

development baseline B 固定为 main `610a810d45bb30173906d55c77709389adf1cf31`，来源为本轮显式 main 同步结果。Planning H0 为同一提交；实现 H 随真实变更推进，内容范围始终为 B 到完整 H/工作区候选。PR target 独立选为 `castbox/guru-trellis:main`，后续无关远端变化不改变 B 或自动扩大入口集合。

阶段适用 Architecture 为 `docs/architecture/README.md` / `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。独立 candidate_assessment 的实际结果为 `architecture_impact / legacy_boundary_convergence`；其 decision_refs 为 ADR-027 与 `docs/architecture/adr/runtime-location-decoupling.md`。该结果仅允许方案写作，未证明实现或最终规划通过。

## 2. 当前系统、边界与目标差额

`runtime/bootstrap.py` 已拥有完整 identity、用户 cache、锁定依赖、真实 wrapper probe 和失败保护。`resolve-python.sh` 在进入 Python 前要求 local/gitdir/common active pointer；普通 Git 新 worktree 没有该指针时，已有兼容 cache 仍不可达。bootstrap metadata 不记录首次验证时间，故不能使用“最早环境”规则。

`guru-sync-base` 先选 base，再绑定唯一干净 authority checkout，fetch/ff 后要求 HEAD/local/remote 相等。Discovery `observe_base_current` 再检查 branch/worktree/clean/三方 identity。这些条件是同步的约束；本批将明确 Git 对象的只读来源从该约束中分离。候选工作区、所读基线、执行工具和副作用目标分别绑定。

Task/Delivery、generation、分支绑定、位置适用性、正式已提交 Review 与实际远端发布事实仍归原 owner。本批不改上游源码或公共生命周期，不引入新 Task authority、通用绑定器、缓存 GC 或资源调度。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置 | 本设计落点、理由、影响与上游处置 |
| --- | --- | --- |
| #718 行为1—3；#231 用户级完整 identity，共享而非复制 venv | retain | D4/D5：保留 identity 字段、锁和物理 cache；源码 HEAD、路径、patch、Task、worktree 不进入 identity |
| #556 D556-01/02：apply 默认当时 PATH python3，显式优先且失效不回退；日常保留合法选择 | retain | D4/D6：安装选择与日常解析分开；显式解释器类别与依赖要求共同选环境，路径/patch不制造新identity |
| #556 D556-03：candidate、锁定安装、真实 wrapper 验证先于 target/选择切换；失败保护 | retain | D6/D7：继续原 bootstrap candidate/probe/replace顺序；新增解析不自动安装，repair也不提前改原可用环境和选择 |
| #566 D4 / ADR-027：tools-only checkout-local 隔离，来源运行与目标自身验证分开 | retain | D4/D7：目标选择写集仅属该checkout；peer pointer和实际选择都核验；source-loaded维护后仍跑目标入口 |
| #566 原 local→gitdir→common active pointer 作为日常启动必要前置 | change | D4/D5/D7：旧有效v2仅作迁移hint，当前自动解析可独立发现cache；新格式明确选择来源。窄替代写入隔离contribution/ADR，经原promotion生效 |
| ADR-006 / 当前Sync：实际同步选择唯一目标、clean、ff、identity | retain | D5/D6：原同步API与结果保留；只读对象不冒充同步成功 |
| 当前base_current链把只读前置等同已检出且clean、三方相等 | change | D5/D7：对固定直接consumer成套增加明确对象来源变体及薄projection；旧完整同步路径保持原义，原owner迁移和检查 |
| #718 行为7—11：草案独立候选、显式来源、必要拒绝与兼容退出 | retain | D5—D8：固定ref/commit和candidate；不要求草案commit/push，不隐式移动分支；正式门禁继续验证真实资格 |

## 4. 模块、职责与设计取舍

### D4.1 环境 owner

唯一环境算法继续由 `trellis/skills/guru-team/runtime/bootstrap.py` 及其必要小型同owner模块承担；shell resolver只找可执行的受管解析seed并转给该算法，不复制JSON/兼容判断。seed可来自现有cache，仅运行当前assets的标准库解析；业务命令最终必须由被选环境运行当前目标assets代码，不能用seed环境代执行。日常入口不调用pip或安装。

有效需求由当前assets声明的 runtime API/layout、lock digest、平台及解释器兼容类别构成。自动解析先保留当前需求的有效hint；没有有效hint时按24位runtime identity的字典序验证现有cache，选首个兼容且probe有效者。成功选择后由原owner保存自动解析hint；新增cache或PATH变更不改变仍有效hint。按工具需求保存有直接consumer的解析结果，使不同依赖分支切回可恢复原合法选择；不按Git HEAD、Task或位置创建venv。

新选择载体为checkout-private `.trellis/.runtime/guru-team/python/selection-v3.json`，使用3.0格式，区分自动选择与真实显式解释器选择。旧 `active.json` 保留原文，供同一位置尚未更新的installed resolver独立读取；新代码不覆盖或双写该旧载体。其最小内容为：格式版本、user-cache scope、显式选择类别或自动模式，以及按工具需求指纹保存的runtime identity hints。需求指纹只包含实际依赖/API/layout要求；解释器类别由显式选择或实际选中环境提供。每个字段直接由日常resolver或原rollback owner消费，不保存授权、过程、时间或全局偏好。自动hint可丢弃重建；显式选择约束不得因hint失效或其他cache存在而消失。

显式 `--python` 表达CPython implementation/major/minor及平台/ABI兼容类别；日常解析不依赖其原可执行文件路径仍存在。同类别patch/path继续复用。工具lock变化时只在同显式类别中找匹配环境；缺失或失配明确拒绝并给恢复命令，不换另一类别。默认apply/reapply仍按当时PATH python3选本次环境并保存自动模式。受控维护caller明确传入其解释器时保留该合法类别。不新增精确runtime-id选择参数；既有 `--resolve-runtime ID` 只读能力保留。

不采用created_at排序、共享全局偏好台账、按仓/Task建立venv或日常隐式安装。旧v2迁移由D7拥有；不是第二永久选择authority。

### D4.2 Git owner

`guru-sync-base` 继续拥有明确来源解析和实际同步两个确定性profile，名称不决定是否发生同步。新增只读profile只解析明确仓库、选定ref及固定commit；它不寻找该分支checkout，不检查无关dirty，不fetch/ff。需要刷新时，caller先明确远端ref并执行原公开刷新/同步profile，再采用明确提交；没有“自动追最新”。

Discovery独占当前/历史证据充分性；其只读来源读固定Git tree中的Docs/code/tests/archive index。工作区草案单独作为candidate读取，不能混成基线。原current-state→history→语义gate顺序保持。读取Git对象的公开事实入口应直接服务Discovery及人类/Agent查看源内容，不新增无人消费Skill。

## 5. 接口与数据

### D5.1 环境公开入口

继续支持原 `bootstrap.py --repo TARGET --runtime-assets ASSETS` 初始化、`--python`、`--no-activate`、`--checkout-local`、`--resolve-runtime ID`、`--print-identity` 及原resolver ABI。增加或收敛在同owner公开命令中的三类操作：

| 操作 | 输入与副作用 | 结果 |
| --- | --- | --- |
| check | 明确repo/assets；无安装、无选择写入 | 检查当前选择及匹配cache；输出实际runtime或稳定缺失/失配诊断 |
| resolve | 明确repo/assets；不安装；仅缓存已验证自动解析结果 | 输出实际runtime identity/interpreter；显式失配停止 |
| repair | 明确repo/assets、可用CPython3 seed及必要`--python` | 经原bootstrap锁定安装/真实wrapper验证后构建或修复并切换目标选择 |

具体CLI使用现有bootstrap参数族：check为新增 `--check`，resolve沿用 `--resolve-active`/`--exec-active`，repair为新增 `--repair`；无操作flag保留原bootstrap初始化行为。独立公开shell入口定位matching assets和可用seed，不能依赖损坏目标dispatcher；缺seed/锁定依赖来源按实际阶段诊断。错误输出保持单JSON、无原始pip日志、无secret。`runtime_not_bootstrapped`只表示确实无可用环境/选择，不再等同“缺自动pointer”；cache损坏、依赖失败、显式不兼容分别可定位。

### D5.2 明确基线 DTO 与迁移集合

只读输入明确operation/profile和repo。base_ref显式给定时直接解析该ref或commit；省略时复用原base选择合同（显式base_branch、config scalar、已有ordered candidates、remote default）选定ref。解析成功后固定40位commit并明确投影来源；base_commit仅作选择时的解析断言。输出使用独立版本/明确discriminator的Git对象来源，最小字段为repo locator、选定ref、固定40位commit、选择来源，以及其直接consumer需要的局部一致性token。不得伪填checkout HEAD/local/remote三种角色为同一commit，也不得把读操作输出标为已经同步。实际Sync保留原 `synced` 与 `guru-base-sync-result-1.0`。

原 `guru-sync-base` 增加只读profile和独立 `baseline_ready` 出口，唯一consumer为原Discovery。新输出经显式薄projection进入Discovery；当前五阶段transition选择新版本的base来源union，保留同步与Git对象的不同variant。受控current consumers成套直接演进，不为旧schema增加万能nullable字段。

固定直接consumer集合为B中以下真实入口及其相应public/schema/examples/tests，不追逐后续无关新增：

1. `guru-sync-base` public invoke、Interface、原同步输出和私有同步结果；新只读来源输出/读取事实。
2. Discovery `observe_base_current`、repository/base_observation、证据blob与archive读取、history preview、context_ready与refresh返回。
3. `skills/consumers/workflow/stage0/transitions/{base,context,clarity,wording,readiness}-current.schema.json`。
4. Clarify clear/needs_context及原runtime重建base_current；Wording pass及对应consumer schemas。
5. Readiness ready/review_wording/clarify返回及实际target创建consumer；Create Issue source-chain验证，原Task Creation `selected_base_ref/reviewed_base_head` projection。
6. 兼容 `prepare-task --reviewed-base-provenance` 的实际读取consumer；只支持其原声明用途，不复活退役workflow入口。
7. canonical workflow和与上述能力直接相关的spec/README、registry/manifest/platform投影、installer staged验证与sidecar/drift。

范围包含这些模块里为同一来源语义所需的unchanged consumer适配；不包含业务仓动议编排。旧同步输入和旧完整安装保留固定版本；新只读输出不能伪装成旧同步provenance。具体新增schema/id/version和参数在原MIGRATION-718中作为可执行公开迁移合同写清，随实现一起检查，不另建入口清单系统。

## 6. 状态、顺序、正常与失败流程

环境：读取当前工具要求→读取真实显式类别或自动模式→验证本需求有效hint→无有效自动hint时稳定枚举匹配cache→probe→保存自动hint→以实际所选解释器运行当前目标代码。显式类别无可用匹配环境时停止；自动无cache时停止并指向repair。解析不安装。repair：检查seed/锁来源→原candidate构建或复用→真实wrapper检查→成功后替换cache/选择，失败保留旧可用对象。

只读：caller选明确repo/ref/commit→原基线owner核Git对象→Discovery读该tree及独立候选→Clarify→Wording→Readiness→该操作原结果。草案无Task可审核；仅任务/正式阶段写入才进入原身份与阶段检查。实际同步：原目标checkout、clean、历史可ff及identity检查→明确fetch/ff→原结果，不从只读成功推导。

错选基线、缺对象、候选普通变化分别返回原来源纠正、缺前置或刷新受影响结果；不得将所有门禁放宽。正式Branch Review仍要求已提交完整B/H，发布仍要求真实远端候选，Task操作仍核身份/generation/绑定。

## 7. 恢复、兼容、迁移与集成

旧v2没有来源字段，无法证明历史显式意图。公开规则为：对当前assets仍兼容的有效v2选择，首次切换保留同一物理环境；失效v2按可替代自动hint处理，发现现有兼容cache。需要跨更新保留显式类别的用户，通过当前公开 `--python` 入口重表达。只有新载体不存在时，当前runtime owner才按原local/gitdir/common顺序读取旧v2一次。新载体形成后只读写当前格式，不再用旧v2覆盖当前选择；新载体存在但无效时准确拒绝，不回退旧来源而丢失当前显式约束。不新增授权或来源认证账本。

新写入只作用于目标checkout的ignored环境选择，common/peer载体不改。原旧完整安装仍读取其固定v2；单目标tools更新保留这些消费者，回滚保存并恢复目标原选择载体和工具组合。原tools/upgrade rollback快照同时涵盖当前新载体和原旧local/gitdir/common载体的实际preimage；原本不存在的新文件在rollback后移除，原本存在者恢复原文。旧工具继续读取原v2原文；公共tools/data兼容性仍先校验，不能先回退半边。`--print-active-pointer`返回当前writer的versioned locator；实际选择由公开`--check`/resolver提供，不从旧文件猜测。peer比较同时覆盖其新载体与旧载体bytes及实际选择。默认完整apply的目标激活也保持peer已成立的合法选择；本批不更新common选择载体。

source-loaded维护从选定完整matching source运行，source/环境/目标分别核实，保留Task/session/用户配置/非目标工具。目标旧dispatcher不可运行时，先由公开环境入口恢复；需要工具修复时继续原upgrade-tools。成功后调用目标自身resolver、installed验证和实际native入口，不能用source代执行证明目标恢复。

public I/O成套迁移在MIGRATION-718说明旧完整版本、当前新schema、生产者/消费者projection、运行时旧路径退出、原owner及rollback。普通legacy Task不为环境维护而转换。旧版本验证样本由本仓隔离资源建立，不借业务Task。

## 8. 验证设计

| 验证 | 对应验收与入口 | 观察和证据边界 |
| --- | --- | --- |
| V1 | A1/A2；原bootstrap→普通Git linked→实际installed wrapper | 相同有效需求同物理venv；无hint仍成功；无新venv/Task；不同依赖分支切回；位置删除不删除环境 |
| V2 | A3；bootstrap/apply默认与显式Python、多个合法cache | PATH变化/新增cache不改有效hint；显式不兼容拒绝；patch/path复用、不同类别并存；真实minor与模拟identity证据区分 |
| V3 | A6；隔离owner cache，公开check/repair及原wrapper重试 | 缺失、损坏、旧失效自动hint可恢复；缺seed/依赖来源准确诊断；repair失败保持旧环境/选择 |
| V4 | A4/A5；真实原基线→Discovery→Clarify/Wording/Readiness公开链 | 无Task、外部worktree、untracked草案、基线未检出/dirty；固定对象与候选分别绑定；走到声明结果，无commit/push/隐式ff |
| V5 | A5；原Sync及正式Task/Review入口 | dirty、非ff、错来源、普通candidate漂移及缺Task/提交/远端事实仍拒绝；只读通过不制造正式gate |
| V6 | A7；source-loaded upgrade-tools/rollback真实隔离样本 | 旧目标入口不可运行→matching来源维护→目标自身恢复；peer实际选择及原bytes保持；旧v2有效/失效、同位置新canonical与旧installed正常共存、显式重选和新旧载体rollback验证 |
| V7 | A8；source/installed/package、一个代表安装与reapply/drift | 命中模块测试、真实wrapper、所有声明投影机械一致、模式、sidecar与Task状态保留；不运行完整Release矩阵 |
| V8 | Markdown路由变化 | 代表性Agent通过新公开只读来源调用原consumer；与确定性链证据分开报告，不能只断言文本或schema |

修复前已拥有同源隔离样本：旧installed bootstrap checkout-local成功后，普通linked调用原wrapper返回`runtime_not_bootstrapped`。样本保留作V1/V3/V6前后比较；不把原失败改名或迁移到后续consumer作为成功。

## 9. Canonical 引用、本轮差额与实际未决项

requirement/design/test authority从 `docs/{requirements,design,test}/current/README.md`定位；runtime/baseline未迁移完整单元须结合B中原约束和本次Direct Source承接。原RDT owner编写完整runtime-location当前单元及关系，原Architecture owner维护受影响职责/集成定义和ADR；在candidate Check前仅写隔离proposed定义。实际共享promotion在final_integration，经原Architecture及candidate Check后执行，再重建candidate、final Check、commit和完整Branch Review。

task-owned contribution位于本Task `architecture/contribution.md`；ADR candidate位于 `docs/architecture/adr/runtime-location-decoupling.md`，在晋升前明确candidate。它们拥有对ADR-027和原只读/同步组合的窄替代及退出条件。现阶段无实现结果、Release或业务采用结论。

没有产品层未决项。实现者若发现上述真实consumer集合还需同职责适配，沿implementation discovery给出具体差额；原scope不自动扩为无关新入口。新增authority/接口或实质机制变化回最早受影响owner；普通可执行细节由原实现和Architecture核实，不向用户索取代码。
