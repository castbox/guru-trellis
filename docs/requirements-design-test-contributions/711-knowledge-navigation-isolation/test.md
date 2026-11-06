# #711 实际验证记录

观察截止：2026-11-04，本 Task 候选 Check 前。规则及完整隔离 proposed 已准备；下表分别记录已取得和仍待完成的结果，不从文件存在推断通过。

## 结果归属与待整合证据

原始 native 轨迹保留 repo 外 run-root。测试 worker 完成后，由主会话将实际模型/CLI、旧新同权限/起点、原公开入口、首次命令/输出与完整文件集、具体语义观察和证据 locator 整合到本文件。首次失败、execution gap 和修订重跑分别记录，不改名首次。

| 验证 | 当前记录状态 | 需要的真实证据 |
| --- | --- | --- |
| V711-1 / T711-01 | 合规旧新 A/B 及两序观察已取得 | 下节固定候选、完整文件集、首次与重跑区别及语义核对 |
| V711-2 / T711-02 | 实际读取、既有修订及纯评估补证完成 | 合并后 reader、原四层 UTC 修订；原失败与修复后的真实链分别保留 |
| V711-3 / T711-03 | 原 owner 真实整合与纯评估补证完成 | 100 行、UTC、空结果及全部原约束在组合完整正文中保留 |
| V711-4 / T711-04 | 迁移、在途、结构及补证完成 | 未达/已达切换、旧 Task 集成、改名/合并、稳定引用与状态措辞修复 |
| V711-5 / T711-05 | 已取得下节所述定向证据 | matching source/dogfood/installed/平台/reapply/drift/mode/sidecar及代表安装；保留锁源与完整矩阵边界 |
| V711-6 / T711-06 | 尚待正式 owners 结果 | 本 Task 的候选审查、真实晋升/readback、after重绑及最终质量/交付 |

## 实际 Agent 的配置与首轮边界

native run-root 标识为 `guru-711-native-20261103T210234`，原始输入、事件流、命令输出和完整文件集合保留在仓库外。旧新侧均使用实际 `codex 0.162.1`，配置模型 `gpt-6.1-sol`、provider `sub2api`、reasoning `medium`，权限为 danger-full-access / never approvals。该记录只确认实际配置/tag，不声称 provider 未公开的后端 revision。两侧业务请求、来源条件和 Task/Delivery/Plan 起点等价，允许布局与相应维护指令变化。

初始无 remote 的 no-Issue Intake 在 `stale_identity/base_current.repository` 停止；另一未完成首轮被终止。两次原日志保留。后续按设计第 8 节建立合法阶段前置 fixture，受测边界从 maintenance phase2 implementing 开始。fixture 不证明 Intake 或 Planning owner 已实际运行，也没有替当前 Architecture、Check 或晋升预填通过。

首轮旧 A/B 已留下物理候选与 `old-merge-first/merge-observations.json`：A→B、B→A 的 Git return code 均为 1。两候选共同写入五条导航路径；实际冲突仅三条，即 Design README、Test README 与 `docs/traceability.md`。Requirements 和 Architecture README 在该固定快照自动合并成功，不能将五条共同写入全称为冲突。

读取轨迹随后发现部分首轮 Architecture 在正式结果前加载了整份 Task/Planning 叙事；其中另有一轮在形成初步职责判断前已读 Task PRD。原 wrapper/Check 成功不能补足其独立方法。相关首轮只保留为实际执行和物理观察，不作为合格端到端验收。原 owners 随后以隔离上下文、合法同 key rework 和唯一 before/after 完成重入；合格重跑单列，不改写首次日志或把重跑称为首次。

最终独立复核另发现 structure、overlap A、overlap B 和 overlap 组合的首次 Architecture actor 在 formal 前参与了规范性拟写。它们的原 Check、写入/readback 和 reader 是实际执行及内容观察，不能无条件计为未参与写作的独立评估。四个 case 随后沿原合法 rework 保留完整 proposed、恢复自身唯一 before，由全新纯评估 reviewer 只读审查，再由原 writers 实际晋升，重绑 after 后完成匹配最终评估与 Check。原 green 不追认为方法合格；其余已核七个 case 不为此重跑。补证结果及新发现的具体缺陷见下节。

## 合规重跑、组合与实际读写

下表四个独立主题 case 的合格重跑由 fresh generic Architecture carrier 先读取 authority、完整候选和必要消费者，完成当前项目检查及正式 Architecture 调用，再由原 Check 读取完整 Task scope。old A 在尚未读叙事时真实中断并纠正，随后由同一仍隔离的 carrier 继续，不称中断后重新空历史。身份、Plan 和固定 B 保留；原公开 rework、候选检查、实际晋升/readback、after 重绑与最终 Check 均实际执行。读取轨迹、provider rollout 和原 wrapper stdout 分别保留；混入自制读取观察的一份 M events 文件标为 mixed，不单独当作原始 CLI stdout。

| 方案 | 固定独立 A | 固定独立 B | 完整变更集与两序结果 |
| --- | --- | --- | --- |
| 旧结构 | `45795256557c8a57fdd4746fea471d0939e63d96` | `8a2d067475f5a40fab99f463ae88dca80c82acdc` | 同 B `8df3b2b14d38b9c20de8e48ee464f4119e82b195`；25/30 paths；共同写五条根/追踪路径。A→B、B→A 均 return code 1，本轮实际冲突为 `docs/traceability.md` |
| 新结构 | `8b6b96972049987c647056c5415e0fe52b29d9ab` | `92019a621ac4b80e3812cca92172f37918a1e6be` | 同 B `aed7e74cc363078b56277d756ccbfae923f088cd`；19/21 paths；共同路径为零。两序均 return code 0，同 tree `0d2103937fdf988961d73ed22b11e89c806b4123` |

四个 case 都有实际最终 Check `passed`。完整 paths、Check result id 和候选身份由 `old-{A,B}-snapshot-qualified.json`、`new-{A,B}-snapshot-qualified.json` 定位；两序完整 diff/stdout/tree 文件在 `old-merge-qualified/` 与 `new-merge-qualified/`。旧侧重跑补充来源/关系并调整根行位，不能称与首轮逐字相同；差额保存在 `*-qualified-vs-first-docs.diff`。首轮三文件冲突不被本轮单文件冲突覆盖。

新侧审计 CSV 保留拥有者、同租户、管理员不授权、无 secret、两列顺序及只读/失败无副作用；locale preview 保留 profile locale 匹配、无匹配回 en、两路径无 token 及成功/失败不写状态。四层稳定身份、来源与必要关系均在所属完整单元。完整文件集未把登记转到根、current README、共享 metadata 或下一层索引。`new-qualified-vs-first-knowledge.json` 确认合格组合与首轮组合的整个 docs 差额为空，八份 current 正文逐字相同；因此下面实际读取及后续 fixture 的知识起点可按适用性复用。

实际合并后 reader 从稳定入口执行六组原命令，依次限定目录/稳定 ID 检索并读取完整 R/D/T/Architecture。仓外结构样本的 `reader-before.md` 及其六组 stdout/stderr 保存原回答：两新增主题、原审计 current、未实现 CSV accepted target/open GAP、未晋升按天分组 proposal 和历史管理员定义分别解释，未形成第二 current。旧账单只回答 supplied-1 的原保留边界，不推断字段、流程或业务实现。

既有修订由 overlap B case 实际写入：沿原 `REQ/DES/TEST/ARCH-AUDIT-CSV` 四个单元写三列 `event_id/action/occurred_at`、UTC 和空结果仍有列头，保留原查询、权限、保密及只读条件。原轮实际 Check 为 `check:24aeb3d4d21fd3a57fe50619838db135b40900a8ead2b3e2767f4cddbd09b869`，固定内容快照 `36922b3f07f4e1dabd89fe4f9480b789210ae62a`；`overlap-B-snapshot.json` 保存 21 条完整 paths，四份 current 外为本 Task 的贡献、规划和元数据，不新增每 Issue current 或根登记。补证又修正三层来源段，故旧快照不表示本轮精确 after，实际新结果见下节。

共享来源观察 `shared-source-byte-observation.json` 确认原输入、固定旧 B 的 source blob 和 11 个实际 fixture 仓内来源逐字相同。old A 本人只比较了固定 B 仓内来源，未亲自重跑外置 acquisition cmp；外置比较与共享观察由实际执行者完成，最终 consumer 只能按这些真实边界采用。

以上 snapshots 是真实质量链后的本地确定性 Git 快照，不是 fixture 的 TaskCommit、committed Review 或远端 Delivery。它们不代替本 Task 的 V711-6。

## 真实重叠的组合观察

两个任务从同一 `0467ee12d6c122a4e57456a782a6d81f9b79e7e6` 独立修改审计导出。A 固定为 `8c1b07c8bf59d60ac178e26fed53ba15ebdcaf43`，增加最多 100 行、超限整次拒绝；B 固定为 `36922b3f07f4e1dabd89fe4f9480b789210ae62a`，增加 UTC 时间列和空结果列头。`overlap-merge-first/` 保存两序四份 current 正文的真实文本冲突。两侧都称 v2，不能按版本大小或 Git 自动合并决定有效规则。

实际整合以 A 为 selected base/target，完整读取共同前驱、A 和 incoming B，再由原 owners 形成 v3。组合保留 A 的 100 行限制和 101 行整次拒绝、不截断；以 B 的三列替换旧“恰有两列”规则，保留 `event_id/action/occurred_at` 顺序、同一时刻 UTC 和零记录三列列头。零结果仍须先校验拥有者和同租户；管理员不授权、跨租户拒绝、无 secret、只读和失败无副作用均继续适用。旧 v1 与两份 v2 的精确 Git 引用各保原义，原查询和通知没有被扩张规则。

原轮实际最终 Check 为 `check:e7807c5f73bfd5e657a4b61051a5366310c93bff52c22f045eb537b8b0a44232`；`reader-final.md`、完整字节副本与 `actual-write-paths.json` 位于该整合的原执行目录。相对实际 A 有 21 条 Git 可见路径：四份 current、十份贡献、七份 Task/Planning 元数据；根和共享索引差额为空。参与拟写的 reviewer 所留方法缺口已由下节纯评估补证闭环，原 Check 不单独建立合规结论。

## 迁移、在途和结构变化

迁移样本先由实际 RDT owner 对尚缺测试关系的候选返回 `revision_required / traceability_revision`，共享 current 未提前切换。补齐后，合规 fresh Architecture、候选 Check、原 owners 实际晋升/readback、after 重绑和最终 Check 完成；最终结果为 `check:165fd77cdcf7304ee1cbf93fe96e6e50ab5283f955c81f86a68a551cb0ec9201`。13 个实际目标与原 `aed7e74cc363078b56277d756ccbfae923f088cd` 迁移快照逐字相同，原未迁移账单、历史、proposal/target 与旧阶段引用边界保留。该等价观察只支持后续样本起点采用，不追认为首轮方法通过。

在途 `navigation-inflight` 保留原 Task key、Plan 和阶段适用 `8df3b2b14d38b9c20de8e48ee464f4119e82b195`。最终集成真实重读已迁移目标，原 owner 识别旧索引 proposal 与目录发现合同的差异，整合后不恢复旧索引双写。合规重跑最终 Check 为 `check:d1c0bc7a7c92e03ccc73914f1174e7d41e61d735a663bfbe966c525d1c30974a`；原首次与重跑调用分别保留，不把旧读取兼容解释为旧写入许可。

旧侧冲突后的实际整合也完成了合规重跑，最终 Check 为 `check:3d10c10978863de2baa72a5809cac0606055904260863872357c1b744a521c03`。该轮消费 qualified A/B，整合 18 个真实目标及其来源/关系差额；稳定入口 reader 读取 30 份完整正文，保留双方全部条件和非 current 边界。它与首轮 14 目标/104 链接观察不同，未冒称逐字等价，也未改写两个独立候选来制造无冲突。

结构样本实际完成四层 `audit-csv.md` → `audit-export.md`，保留 `REQ/DES/TEST/ARCH-AUDIT-CSV`、原版本及全部原条件。旧路径只定位转换与固定旧义，没有第二份完整 current。通知四层 `notification-copy.md` 合并 COPY 与 PREVIEW 的完整定义；双方所有业务身份和原版本存活，一般文案的 profile locale/en/token 条件与预览成功/失败不写状态的额外限制分别保留。退役的是独立 preview 正文位置，旧位置只指向后继小节；没有删除业务身份，也没有把预览只读扩到一般文案。

原协调 owner 发现等义替换分配新 ID 的候选缺陷，实际经 `implementation_required` 修订后才重新 `candidate_checked`、晋升与最终质量链。原轮实际 Check 为 `check:471e302c7888ab6cf32f6b6656dd77f5411e0bb49fbbb57839caaf0d1c35bffd`。`structure-final-observation.json` 保存 45 条完整 paths，六个根/traceability 的差额为空。`reader-after.md` 及九组真实检索/全文命令验证当前定义和存活消费者；另实际 `git show` 读回 12 份完整前驱。历史未改，当前普通读取不拼接贡献链。输入中的 planning digest 构造错误、原失败和修订结果均保留。后续纯评估补证又发现并修复五处状态歧义，不以本原轮 Check 覆盖新 after。

## 四个 case 的纯评估补证终态

补证使用相同实际 Codex 模型/provider/推理配置与权限。新的纯 Architecture reviewer 不写规范性 proposed/current、Task 阶段或 Planning；原 implementation/Check/writers 分别执行其原公开职责。各原 provider、prompt、实际输入、正式 stdout 和写入/readback 保留于对应执行目录的 `independence-repair-01/`，Main 独立 reviewer 已读取原对象并核对实际消费者与业务正文。该原始行为验证不替代本 Task 的正式 Gate。

下面给出本机原始证据的准确根路径，供本次原质量 owner 取得实际命令和输出。它们是仓外验证素材，不是公共安装路径、另一份业务 authority 或新 runtime 合同。

| Case | 原证据根路径；后文文件名相对此根解释 |
| --- | --- |
| overlap A | `/private/tmp/guru-overlap-a-execution-u5z_tqo4/independence-repair-01/run-01/`；表中 `run-01/` 前缀即此根 |
| overlap B | `/private/tmp/overlap-b-native-owners-dp7w03r6/independence-repair-01/native-owner-20261104T005104/` |
| structure | `/private/tmp/guru-structure-evidence-x9jn5wst/independence-repair-01/` |
| overlap 组合 | `/private/tmp/overlap-owner-logs-kx2eYK3W/independence-repair-01/carrier-01/`；表中 `carrier-01/` 前缀即此根 |

结构最终 reader 的六组实际目录依次为 `20261104T015829.671852-final-reader-entries`、`20261104T015829.696758-final-reader-discovery`、`20261104T015835.254362-final-reader-requirements-design`、`20261104T015842.279151-final-reader-test-architecture`、`20261104T015849.970479-final-reader-boundaries`、`20261104T015909.721906-final-reader-stable-identities`。每组均保留原 `argv.json`、`stdout`、`stderr` 和 `exit-code`；无需等待另写长报告来证明已执行的读取。

| Case | 新最终 Check | 实际 after 与必要读取 |
| --- | --- | --- |
| overlap A | `check:b27a4613e7acb7c7ca9d2aa7293f307d2ce8c19509409fda26bddc4523f8a949` | 四 current 等于原 A；61 docs 中只改本 Task Architecture contribution metadata。`run-01/final-reader.md` 与 `final-docs-byte-comparison.json` 保存读取和差额 |
| overlap B | `check:542e2d27344d46c90160d9c95641a3fdd3d97cc06172fd14548825152e19ee59` | 64 docs 中仅三层来源段不同：区分初次 B0467 与本轮实际 target H36922。`reader/reader.md`、`byte-comparison/result.json` 记录真实读取；原 v2 业务正文/Architecture 条件不变 |
| structure | `check:6d386ab4c47bed1651bc71fb99201ccb059b5a89052fb0c1fd4dcec9ee3bba1e` | 80 docs/16 targets 中仅五 current 状态句改变。`final-docs-byte-comparison.json`、`final-target-byte-comparison.json` 与 `final-docs-byte-diff.patch` 保完整差额；实际稳定入口、限定发现、四层全文、边界和 ID 读取的六组原 argv/stdout 均保留 |
| overlap 组合 | `check:8e86776b6a788032a2de69b893e68b99928e7a8165e4837d36d5966f278d6201` | 71 docs 与修复起点全部相同，四 current 的组合定义不变。`carrier-01/reader-final.md` 与 `docs-byte-comparison.json` 保存当前完整读取与字节依据 |

补证没有隐藏发现：B 的实际 target 来源误写先正式返回 `contract_incomplete / repair`，原 RDT 修三来源句后，同一纯 reviewer 当前评估才返回 `baseline_current`，最终 Check 消费修复后的结果。structure 的已晋升正文仍写未限定时点的“本 proposed 未晋升”，先正式返回 `fitness_regression`；原 writers 修三 RDT、两 Architecture 状态句，明确当前定义已写/readback、隔离 proposed 是历史来源，再由同一纯 reviewer 当前完整评估与最终 Check 闭环。业务条件、身份和关系没有因此改变。

部分纯 reviewer 在必要会话选择恢复前读了指定候选；原 owner 让同一仍隔离的 reviewer 在合法同 key 选择后完整重读 authority、候选和消费者，重新形成当前项目判断并正式调用。首轮顺序偏差保留，不称严格同序或换名为空历史。绝对 evidence locator、同值 stale identity 和其他输入错误均保留，后续真实 re-entry 单列。必要的贡献来源读取不因目录名被误判为叙事污染。结构末尾可选长报告包装被中断时，正式 Check 与六组实际 reader 均已完成；中断不冒称成功进程，也不新增报告门禁。

## 已取得的分发与工程证据

canonical source checker 通过：43 个 active packages、128 个 commands。主 Task 的原 `guru-upgrade-tools` 已返回 `tools_upgraded`；实际安装为 `0.7.0-guru.7`，采用 `local_candidate`。installed checker 通过：Claude、Codex、Cursor 三个平台共 8566 个 managed files，conflict 与 sidecar 均为零。两个受影响 package 的 832 条文件记录与 canonical 的 bytes、digest 和 mode 一致；managed RDT spec 一致。原 dogfood drift checker 通过。

代表安装只建立一次，后续 native 场景复制匹配的已安装 snapshot。该安装的原 tools upgrade 与 reapply 均返回 `tools_upgraded`。实际在途 Task 的九份 Task/Plan 文件及 session、C4、resources 在 upgrade/reapply 前后保留；reapply 的 tracked 差额只有 extension 安装时间。受改正文的 21 项安装投影 bytes/mode 一致，没有遗留 sidecar。首次平台名称映射错误及误用不存在脚本的执行失败均保留；后续使用正确公开入口的结果分别记录。

RDT 定向套件的 11 项测试通过。Architecture 定向套件执行 54 项，6 项失败，不能记为整组通过。六例的唯一文件差额均为 launcher 冷启动生成的 `selection-v3.json`；固定 B 导出的原代表例复现同一失败，相关 Python 源码与 B 相同。因此保留为既有 fixture/launcher 边界，不归因于本次导航规则改动，也不扩张实现范围。

上述工程结果来自 `guru711-source-packages.log`、`guru711-installed-packages.log`、`guru711-dogfood-drift.log`、`guru711-rdt-package-tests.log`、`guru711-architecture-package-tests-matching.log`、`guru711-architecture-failure-paths.log` 与 `guru711-architecture-baseline-case.log`。代表安装的原始观察位于 native run-root 的 `upgrade-preserved-{before,after}.json`、`reapply-preserved-after.json`、`reapply-content-observation.json`、`new-affected-projection.json`、`new-sidecars.json` 及对应原公开入口 stdout。

`formal_fork_source_lock` 仍未验证。分发和代表安装结果不证明正式锁源、完整多平台 Upgrade/Release 矩阵或业务项目采用。

确定性 merge、实际 Agent 语义、分发/安装、文档切换和业务采用分别报告。完整多平台 Upgrade/Release 矩阵与业务仓迁移不在本项；本任务不新增业务部署或数据库写入。晚到正式结果来自其原公共结果和 Git/PR，不要求受审正文循环填写自身最终 pass。
