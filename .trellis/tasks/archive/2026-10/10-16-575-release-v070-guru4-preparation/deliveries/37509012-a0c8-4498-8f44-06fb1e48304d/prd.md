# #575 S4：工具安装、平台证据与 focused 验证器修复

## 来源与边界

继承整体根 PRD R575-01..07 / A575-01..08。直接来源为 live castbox/guru-trellis#575 的正式依赖前置、Stage 1 与非目标；私有 release-guru-trellis-version 的 Two-Stage Lifecycle 是规范设计约束。当前 Delivery 不改变整体 accepted scope、TaskId 或 generation；S1/S2/S3 的已交付内容及历史失败保留原归属。

S3 已交付可消费的 ownership 来源修复；本切片负责从完整 `.3` 运行安装采用 canonical `.4`。本切片必须从真实 clean committed 修复源建立新的 source_locked 工具操作，完成先前保留的完整安装与证据，不把旧操作恢复、模块回归或相同版本输出当成正式安装。原已回滚操作保持终态，不更换其 source/plan/preimages。

## R575-S4-01：正式完整工具投影与目标自身运行

采用现有 guru-upgrade-tools 及其原 public/Guru owners，从实际已提交且 canonical clean 的修复源，使用其正式 Fork lock、匹配 CLI/Core/package roots 和 managed runtime，更新当前准备 worktree 的 upstream tools、Guru packages/runtime/schema/workflow 及 Shared/Codex/Claude/Cursor 投影。工具更新只在本 checkout，不能同步或升级 caller/main、peer、业务仓或 common Python pointer。

保留当前 Task2/session3、整体 accepted scope、Delivery 历史和规划、raw source、旧 archives、用户配置/定制及 peer/common pointer。工具安装不能转换无关 Task 或历史归档；当前合法旧归档不能成为绕过 current-only guard 的理由。未知本地受管修改必须由原 owner 明确处理；不得手工复制工具文件、制造 manifest 或热替换单一 Skill。

成功须由目标自己的 resolver、installed validator、实际 native entry/continuation/current 与下一真实 owner 证明；source runtime、外部 DTO 或 JSON 解析不能替代。目标 native 与下一 owner 的可观察结果分别记录，不提前宣称整个 Task 完成。

## R575-S4-02：平台、ownership 与 A/B 验证对象

完整 source/installed graph、四平台 source parity 与私有 release Skill 四份 bytes、一致 ownership、权限、sidecar、退休资产、bytecode/residue 和只读 dogfood drift 均覆盖当前实际来源。对 archive-bearing 当前对象 A 使用受支持的 tools-only 路径；普通三平台 apply/reapply 在同来源、无旧归档的代表性隔离对象 B 执行。不得通过转换 A 的无关 archives、放宽 guard 或换用design D4 未定义的 preset 替身求绿。

出现真实不匹配时由原 owner 判断实际依赖与前置，不把 FAIL/SKIP 改称通过，不修改原测试/timeout/样本只为消除失败。

## R575-S4-03：修复正常 focused 输出捕获

正式 CLI 合法 stdout 与 stderr 必须都可被 verifier 完整消费。修复当前 focused 初始化路径中两流先合并字节、再解码所造成的 UTF-8 失败；输出捕获不得改变 CLI 输入、正常警告、真实退出码和现有超时分类，不得以 quiet、过滤、容错替换解码或放宽超时消除现象。回归同时证明成功输出、真实失败诊断和既有超时行为；实际同一正式 Fork 的正常初始化须可经过修复后的 helper，保留首失败与诊断层次。

修复仅限 source-side verifier helper 及其必要直接消费者、定向测试；不改公共 Skill/API/state/owner、正式 Fork 或 installer guard，不要求重装未变化的受管工具。不变的安装/平台运行资产按依赖复核采用，仍注明实际安装来源。旧 operation source 冻结不变，不从改变后的 source 恢复旧 operation。

## R575-S4-04：本切片证据与剩余准备责任

沿既有 `docs/requirements-design-test-contributions/575-release-preparation/` 收敛本切片 requirement/design/Test/双向 trace，Test 记录 A 工具安装、B 平台、正常捕获修复及其直接回归。此前 focused 的真实 FAIL 保留；诊断或 helper 回归不能改称完整 clean 样本成功。

本切片的独立交付价值是完整工具采用、平台证据和可被后续 clean committed source 消费的 verifier 修复。当前交付后 WholeCompletion 必须保留并路由整体根要求中尚未完成的 focused clean/local-workflow、真实 stable predecessor 的分离维护及目标 native/下一 consumer/同操作恢复/不兼容回退、最终唯一 RDT 全量收敛和必要晋升。后续切片只能在实际交付与 WholeCompletion 后经原 Creation 建立；本计划不预造 identity 或重写历史 Delivery。

完整 focused 必须从含修复的真实 clean committed source 使用同一正式 Fork 与原受支持参数执行；临时样本自建提交、dirty run 或绕过 source 校验均不充当正式源。其原失败阶段、真实退出分类及最终结果分别观察。真实 predecessor 继续由原 tools/selected-task owners 执行受支持分离维护，generic existing 链不能冒充联合证明。

最终晋升仍须先有完整准备候选的 committed 独立 Review，原 owners 串行晋升后 fresh Check/TaskCommit/完整独立 Review。所有准备交付保持中文 Refs-only；准备 Task 整体 Completion/Closure/Finish 与软件 Stage 2 独立，当前切片不宣称全部准备完成。

## 验收

| 验收 | 可观察结果 | 整体责任 |
| --- | --- | --- |
| A575-S4-01 | 新正式 source_locked 操作完成实际 `.4` 安装，目标 native/下一 owner 可运行，保留对象与 pointer 可核实 | R575-01、03、04 |
| A575-S4-02 | A tools-only、B 三平台 reapply、四投影/ownership/权限/退休资产/sidecar/卫生均有当前真实结果 | R575-02..04 |
| A575-S4-03 | 正常 Unicode 双流初始化可由修复 helper 完整消费；success/nonzero/timeout 与诊断回归保留真实语义 | R575-03、04 |
| A575-S4-04 | 本切片唯一 Test/trace 完整，剩余正式样本与最终 Docs/晋升经 WholeCompletion 路由，Refs-only 不冒充整体完成 | R575-04..07 |

## 明确不属于本切片

最终 main exact-candidate、远端 immutable provider、predecessor→最终candidate发布diff、annotated tag、tag-pinned smoke、GitHub Release 与关闭 #575 继续归 Stage 2。完整累计多平台/native-host 矩阵、真实业务安装升级与生产效果均不声明已验证。不实施 #577/上游#46 人工旧归档激活，不改上游/global/node_modules，不增加公共 owner/API/schema/state/兼容 reader/恢复框架或非常规加固。

本 PRD 定义要求，不记录动态 gate/安装进度。Design 独占机制与 source-design disposition matrix，implement 独占 Delivery Policy 与 Docs SSOT Plan。副作用只由各原 owner 展示实际写集并按其边界确认。
