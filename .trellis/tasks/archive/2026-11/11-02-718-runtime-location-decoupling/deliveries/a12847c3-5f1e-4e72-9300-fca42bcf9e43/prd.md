# #718 D1：共享环境与通用操作前置解耦

## 1. 整体来源与术语

整体authority为 `.trellis/tasks/11-02-718-runtime-location-decoupling/prd.md` / `sha256:8d4fe87d981429d2f2e7730984ca5e6cb0e360ab4a9a4f19e9aef61addc1294a`。本D1 scope_ref选择A1—A8；planning_root为 `deliveries/a12847c3-5f1e-4e72-9300-fca42bcf9e43`。Direct Source为[Issue #718](https://github.com/castbox/guru-trellis/issues/718)完整正文。术语与四概念职责引用[整体PRD](../../prd.md#1-来源与术语)，其完整条件适用。

## 2. 整体与本批目标、非目标

本D1为full交付。当前共享环境存在但wrapper受位置指针阻塞；通用只读入口继承同步的checkout/dirty门禁。D1交付环境发现、稳定选择、独立恢复，以及Git基线读取/候选/同步的职责分离和直接consumer迁移。整体PRD第3节非目标全部保持。

## 3. 本批起点、前序结果、依赖与剩余责任

首次D1，没有前序Delivery。起点为固定main `610a810d45bb30173906d55c77709389adf1cf31`；当前bootstrap identity/cache/probe、source-loaded工具更新与公共Task/Delivery模型继续复用。D1覆盖全部现行范围，不把本仓验收转交业务仓。合并后原Completion还须核对所有A1—A8与剩余责任；Release完整矩阵和业务采用是本项之外的边界。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为和可观察结果 |
| --- | --- | --- |
| S1 | Agent从普通Git/外部工具预建的worktree调用installed wrapper；无Task、无自动指针，已有兼容cache | 选择匹配共享环境并运行目标代码；不创建venv或Task |
| S2 | 同一用户切换依赖不同的工具分支，再切回 | 按有效兼容要求选择并存环境；已有合法选择保持，patch/path不制造identity |
| S3 | 用户显式选择环境；入口发现该环境不可用或不兼容 | 明确拒绝并给出原owner恢复命令；不静默fallback |
| S4 | Agent从含未提交/未跟踪草案、无Task的位置审核明确Git基线 | 只读读取所选提交并绑定草案候选，真实consumer继续；不要求commit/push或移动其他checkout分支 |
| S5 | 原Sync同步目标dirty或历史不能ff | 原必要拒绝保持，错误基线通过原入口纠正 |
| S6 | 缓存缺失/损坏，或source-loaded维护旧目标入口不可运行 | 原环境owner公开检查/恢复；匹配来源维护后由目标自身wrapper验证；失败保留可用选择和环境 |
| S7 | Task换合法位置、结束或worktree删除 | 原身份/绑定owner核资格；这些资源动作不创建或删除共享环境 |


## 5. 完整行为、条件与约束

### 共享环境发现、选择和恢复

1. 对固定实施集合内的 canonical/installed/platform 公开入口，依据本次实际采用工具的 manifest、lock、runtime API/layout 和平台/解释器要求，选择并验证共享环境。环境选择不要求 Task/session binding、特定分支名或由 Guru 创建的位置；各操作自身所需身份仍在原 owner 检查。自动生成的 checkout-local/gitdir/common 指针缺失或失效，不能单独阻止发现已存在且符合当前选择要求的环境。
2. 在同一操作系统用户和平台范围内，相同有效环境需求复用同一个有效环境。有效环境需求包含工具声明的依赖/API/layout、平台/ABI，以及本次适用的解释器兼容类别；仅 manifest 相同不表示不同兼容类别的合法解释器选择必须合并。保留 #556：Python patch 版本和可执行文件路径本身不进入环境 identity；同一兼容类别的不同路径或 patch 不因此分配独立环境。跨仓库、外部/已有/新 worktree、分支、Task 和 Agent 均遵守该复用合同。不得为每个位置或任务复制/创建 venv，也不得按 Git HEAD 或每次工具源码变化无条件创建环境。
3. 只有真实依赖、运行接口/布局、Python implementation/major/minor、OS/architecture/ABI 等兼容要求变化，才选择对应 identity；不同需要可并存。正常目标入口执行该目标实际采用的工具代码，不能借用其他 checkout 的新版代码冒充目标安装成功。原 source-loaded 工具维护继续从明确选择的完整匹配来源执行，其来源代码、共享环境和被维护目标分别校验；维护不依赖损坏的旧目标 dispatcher，写后由目标自身入口验证恢复。
4. 明确多个兼容缓存、默认解释器和显式选择的优先级、稳定性及失配行为。区分安装器自动生成的解析缓存与用户显式选择，不能把旧自动指针当成不可替代的用户意图。合法显式选择继续优先；所选环境不可用或与当前工具不兼容时准确拒绝并指向恢复，不能静默改用另一环境。日常运行无显式选择时按公开的稳定规则复用兼容缓存；增加缓存、切换分支或 PATH 更新本身不触发已有合法选择变化。保留 #556 的入口区别：初始化及显式 apply/reapply 未传解释器时，默认取执行当时 PATH 的 python3；显式 --python 优先且失效不回退。日常 wrapper 调用保留已有合法选择，不因 PATH 变化重新选择或重建环境，也不回退全局 site-packages。
5. 缓存缺失、损坏、旧自动指针失效及依赖失配有准确诊断和公开、独立可达的检查/恢复入口。恢复不依赖损坏的目标环境、当前 Task、旧任务转换或完整工具重装；由现有环境 owner 使用公开合同及必要的可用 CPython3/锁定依赖来源执行。缺少这些真实前置时报告具体缺口。Agent 无需读取私有源码或手写指针；普通调用不会因缺失自动安装依赖，安装/更新沿原副作用边界执行，失败保留此前可用环境与合法选择。
6. worktree/branch/Task 的创建、采用、切换或结束不直接决定环境的创建、迁移或删除。调用时若依赖要求改变，按要求3重新解析；只有环境确实缺失且独立维护操作获准后才构建或恢复，不能按资源数量分配 venv。位置移动或Task结束不删除共享环境。缓存清理保留原独立维护边界，本项不新增缓存GC或调度系统。

### 基线、候选及通用操作边界

7. 区分执行工具位置、审核基线、工作候选和副作用目标。对声明支持的只读基线操作，依据明确仓库、ref/commit 与实际读取内容定位来源；Git 对象可读时不要求该分支已检出或其 checkout 干净。需要最新来源时，明确刷新哪条远端引用、采用哪个提交及适用性，不能静默更换来源。未提交内容作为单独候选读取，不能冒充已发布或已提交 authority；来源的发布状态要求仍归其原 owner。
8. 基线读取、候选审核、分支同步和外部发布分别使用自身必要前置。实际同步/快进继续检查目标 checkout、dirty、历史关系及身份一致性。未提交候选审核只受其原 profile 的内容与范围条件约束；正式 Branch Review 的已提交范围、发布所需的实际远端候选及正式Task/阶段前置继续有效。本项仅移除与当前操作无因果关系的同步条件，不允许未提交候选冒充 committed Review 或远端交付。
9. 外部或已有 worktree、无 Task、含未提交/未跟踪草案是必须支持的正常组合。审核准确绑定实际采用的内容、来源和范围；普通内容变化刷新受影响结果。通用 Issue 创建保留最终正文、目标仓库、重复判断、当前审核及真实副作用边界，不为获得调用资格强迫草案先 commit/push 或隐式移动其他 checkout 的分支。
10. 错选基线等调用方错误提供准确诊断与原入口纠正；框架不能把错误输入当作放宽全部门禁的依据。逐项审查 Sync、Discovery 及其真实 consumers，完成相同职责的成套调整，避免把失败从一个阶段转移到下一阶段。
11. 明确迁移现行 local/gitdir/common 指针、公开输入/出口及原升级回滚的兼容承诺；区分自动解析状态、真实显式选择和仍受支持的旧入口，并给出适用版本、原 owner、切换及旧路径退出条件。单 checkout 工具更新不写非目标工具、Task/session、用户配置或私有选择状态；仅新增共享缓存也不能改变其他位置的合法有效环境选择。回滚后工具与选择仍兼容，真实显式选择及旧版本消费者有迁移证据。旧格式未记录选择来源时，Planning 必须给出公开可执行的兼容规则，覆盖旧有效选择保留及旧失效指针处理；不依赖历史聊天、不编造未记录的用户选择，也不新增授权或来源认证账本。不永久叠加另一套 fallback 或状态 authority。

## 6. 本批验收、验证方式与未决项

以 Guru Trellis 本仓实现、文档和隔离验证自闭环为完成条件。真实消费者提供的既有材料用于提取回归；不要求业务仓提供新现场、重跑动议链或实际发布 Issue 作为本项完成前置。

按不同调用行为选最少充分代表场景，不展开所有组合。复用本仓与隔离临时Git仓库；真实 Task 数据由原受支持路径形成，不能手写身份或gate冒充前置。

| 验收 | 入口与可观察结果 |
| --- | --- |
| A1 任意位置启动 | 从普通Git/外部工具预建、已有复用和新worktree运行实际installed wrapper；没有自动指针但已有兼容缓存时成功。相同有效环境需求跨仓库和位置选择同一物理环境，不新增venv；不同兼容类别的合法解释器选择按各自 identity 并存；patch/path 单独不同仍复用相同 identity。无Task调用成立，有Task操作仍校验原身份。 |
| A2 切换与独立生命周期 | 合法切换同/不同依赖分支及切回时选择兼容环境；Task换位置、完成与worktree删除不创建新Task身份或删除共享环境。受支持位置/绑定变更由原owner验证；不要求不受支持的任意组合通过。 |
| A3 稳定选择与版本并存 | 覆盖多个兼容缓存和显式选择；日常运行时新增缓存/PATH 更新不改变已有合法选择，显式失配不 fallback。显式 apply/reapply 的默认 PATH 与 --python 优先规则保持 #556 合同。不兼容依赖版本并存，切回可继续使用原兼容环境。 |
| A4 通用读审 | 从已有worktree、无Task且含未提交/未跟踪草案的实际公开入口，读取明确Git基线并审核候选；基线无检出或其位置有无关dirty均按只读合同可运行。草案保留、来源身份明确、无需为入口资格commit/push、不隐式快进其他checkout。至少一个代表案例经原公开调用及实际基线consumer继续到该操作的声明结果；仅底层Git对象读取成功或新增无人消费的读取接口不算通过。 |
| A5 必要拒绝与纠正 | 实际同步仍拒绝dirty/历史关系不满足的目标；错误来源、候选漂移、正式阶段缺少必要Task/提交/远端事实仍按原合同拒绝。公开诊断能纠正错选基线；只读放行不转化为正式gate通过。 |
| A6 独立恢复 | 在隔离且由测试拥有的缓存中，通过原安装/维护路径形成缺失、损坏或旧指针组合；公开检查/恢复及原命令重试可用。无可用seed或锁定依赖来源时准确报告；实际恢复不依赖Task迁移，失败保留可用环境和选择。 |
| A7 维护与迁移 | 原single-checkout工具更新、reapply和回滚保持工具/依赖组合兼容；非目标工具/Task/选择状态和实际合法环境选择保持。对真实受支持旧指针/入口完成迁移与退出验证。source-loaded维护覆盖“旧目标入口不可运行→匹配来源维护→目标自身入口恢复”，不以来源代执行证明目标成功；本仓准备该样本。 |
| A8 分发 | 对本次命中的package/runtime、canonical/dogfood/installed、声明平台投影、mode、reapply/drift及sidecar给出证据；需要安装样本时最多一个代表性样本。完整多平台升级/Release矩阵仍由专门工作承担。 |

每条验收给出实际入口、观察与覆盖边界，行为等价的场景共享证据，不要求每项跑完整Task/Delivery链。Markdown路由或Agent调用责任变化时，仅补受影响入口的代表性Agent行为验证；确定性环境与Git行为用真实命令验证。测试及替身由本仓准备，不调用原业务Task或真实产品Issue发布。

验收保留正常复现的before/after、正确正向结果及必要拒绝，证明失败没有转移到后续consumer。schema、文件存在、测试专属补偿或最后一次成功不能代替对应真实入口证据。A1—A8的适用义务在本仓完成，不转交业务仓补现场；本项之外的完整Release矩阵与业务采用分别记录，不成为额外完成前置。

没有需求层未决项。实际选择算法、固定consumer集合与公开迁移合同在独立candidate_assessment后进入design；当前没有实现或验收通过声明。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/README.md`、`docs/design/current/README.md`、`docs/test/current/README.md`：定位完整当前单元；本次更新环境和基线consumer的定义与验证。
- `docs/requirements-design-test-contributions/566-single-checkout-upgrade/design.md` D3—D7及 #556 历史设计：保留隔离维护、解释器与失败保护；D1 design第3节拥有唯一来源设计处分。
- `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`：由独立Architecture owner评估职责变化，当前不修改共享authority。
- `.trellis/spec/preset/installer.md`、`.trellis/spec/workflow/data-contracts.md`、`quality-guidelines.md`：受管分发、最小DTO与验证范围。
