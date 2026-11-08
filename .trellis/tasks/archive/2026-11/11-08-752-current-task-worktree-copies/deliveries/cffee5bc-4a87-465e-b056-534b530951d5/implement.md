# #752 D1 实施与验证计划

## 1. 输入与引用

整体范围为根prd.md的R1–R5/AC1–AC5，本批prd.md覆盖全部；方案与唯一来源设计处置见本目录design.md第3节。固定B=2ab135ed2d3908966785bb23ad42ada0790f0c81，目标main，无前序Delivery。

实施前实际读取原delivery-migration完整合同、Fork PR66 public migration2 schema/executor、相关Guru preview/private exclusion/resume/rollback、当前source lock及原source validation。数据owner和失败条件见design第4–7节；验证选择遵循quality-guidelines的Test And Validation Value。文档正文规则来自已加载planning-body与本批模板。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原责任 | 文件/动作与可审核产物 |
| --- | --- | --- |
| I1 | Activation完成；实施worker | 核PR66精确源码/CI与已存在实现，不改他方并行worktree；采用已审source pair，补必要public-contract差额，不复制Fork算法 |
| I2 | I1接口可用；实施worker | trellis/skills/guru-team/packages/guru-upgrade-installation/runtime及tests：仅必要consumer适配，扩展test_delivery_upgrade.py为current peer真实多workspace；证明private exclusion、raw/session保留、resume/rollback |
| I3 | I1成功merge/main CI；主会话source owner | 更新trellis/presets/guru-team/source/trellis-source.json真实commit/parents/tree/ci_run_id及受影响当前说明；使用完整clean同源CLI/Core build，不patch安装依赖或tag |
| I4 | canonical候选完成；原tools owner | guru-upgrade-tools对本Task checkout做tools-only dogfood同步，保留Task/session/peer；原validators核source/installed、platform、ownership、drift/sidecar/mode |
| I5 | 实现可核验；原RDT/Architecture owner | 完整隔离贡献与proposed，实际Test观察；独立phase2与candidate Check后各原owner final_integration/readback，implementation重绑实际after |
| I6 | 最小自检与敏感检查；原TaskCommit/Publish | 形成早期真实commit与同PR Draft，固定B/H独立完整分析及命中验证；formal source_locked代表性安装消费干净已提交source，必要修复回原owner |
| I7 | 全部内容与V1–V4足够；原最终质量owners | actual candidate/begin_check、finalArchitecture/Check、精确TaskCommit、完整committedReview、readiness/Ready/Merge，随后整体Completion、Closure、Finish/Cleanup |

I2/本地测试可在正式source固定前进行；I3和正式V3不可用时不声称完成。实际来源或方案变化回最早受影响owner，保留本Delivery identity和固定B。

## 3. 验证入口、输入与预期观察

- V1：Fork已核source的pnpm CLI migrate2.integration.test.ts定向执行及相关Core migration-v2测试；现有CI和原执行事实按精确输入/依赖采用。观察defer2合法路径、complete parsed equality、原binding/unique authority、peer raw/mode不写入和普通mismatch拒绝。
- V2：设置GURU_UPSTREAM_DELIVERY_CLI和GURU_UPSTREAM_LEGACY_CLI为明确匹配安装bin，运行Guru test_delivery_upgrade.py及必要package tests。current peer场景必须实际进入Core Plan2；断言preview零写入、peer原bytes/modes/metadata、session、无peerDelivery/private转换、same-plan resume/rollback。SKIP保留真实缺失，不计通过。
- V3：原guru-upgrade-installation完整source-loaded公开入口，source_locked匹配干净Guru/Forksource，至少两个registeredworktrees含同currentTask；完整preset和targetowninstalledruntime验证。保留Task/session前后原始快照，核binding选择的实际checkout和peer排除；验证same-plan恢复和rollback。使用独立临时目标，不修改真实业务Task/session。
- V4：原Fork source-lock validator/实际build、check-skill-packages source/installed、check-upstream-ownership、check-dogfood-overlay-drift、递归.new/.bak和mode扫描；命中Python语法/JSON/shell、git diff --check。只补实际变化命中的回归，不执行完整多平台Release矩阵。
- V5：独立Architecture phase2和candidate Check审完整实现及proposed；原RDT/Architecture晋升后actualafter重绑，最终Check/TaskCommit/独立B..HReview覆盖实际文件。

执行顺序随依赖I1–I7推进，首次失败和真实修复保留在唯一Test。不要求同质重复红绿或反复回退；设施失败改用能回答同问题的受支持入口，具体缺口仍阻塞对应AC。源码、组件、installed、外部CI和原生Agent结果分层，不互相代替。

## 4. 停止条件与适用回退点

PR66未合并或mainCI未成功，停止正式source-lock采用而继续独立实现；source/hash/build不匹配在写前阻塞。需求/authority/机制变更回Clarify/Author/Architecture原owner。Task identity、binding、checkout或selection不一致回原resolver，不创建替代Task或空Delivery。

Upgrade真实目标操作先审精确写集和原backups，普通暂停同recovery_ref；rollback由原owner检查managed/business/topology后恢复原preimages，不resetGit、不删其他工作。任何laterbusinesswork阻塞恢复/回滚并保留。工具dogfood用原tools-onlyowner，不用普通apply绕过历史Task阻塞。source/code/user并行改动不覆盖、不提交。

达到对应AC所需充分证据且原checks通过后停止可选实验。未验证边界如实报告，不能用投入成本或绿色组件测试豁免实际installed验收。

## 5. Delivery Policy（唯一）

policy=full。本批覆盖整体R1–R5与AC1–AC5，没有预定后继切片。完成条件是匹配公共语义与Guruconsumer/source-lock落地，V1–V4获得足够当前证据，RDT/Architecture完整拟写晋升，最终独立质量与交付通过。Delivery合并只产生切片事实，TaskCompletion仍审全部已接受scope和必要外部/installed证据。

临时限制只作用于正式source_locked采用：PR66核准merge/mainCI和clean已提交Gurusource到位前，本地候选可测试但formal_fork_source_lock保持未验证。条件满足后同实施/source/Upgradeowners执行V3、更新当前说明与实际Test；不把该限制泛化为停止所有实施。真实业务仓升级、Gurutag/npm发布、远端immutablemarketplace和完整累计平台矩阵不在本批责任内。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原RDTowner负责docs/requirements-design-test-contributions/752-current-task-worktree-copies/{manifest.yaml,requirements.md,design.md,test.md,traceability.md}及唯一proposed目标；新current-copy迁移能力落原职责的完整R/D/T单元，不建立第二scopeauthority或逐Issuecurrent账本。必要native-compatibility当前来源表达按真实新pair修订，历史.6采用观察保留。

Architecture原owner负责docs/architecture/contributions/752-current-task-worktree-copies.md及同名proposed：ARCH-INT-046和ARCH-DOM-043承接currentpeer语义与采用证据边界；ADR-024/017继续有效，无新ADR、根入口或共享索引登记。Author只准备真实隔离贡献，不直接改sharedCURRENT。

直接consumers为独立Architecturephase2、原candidateCheck、final_integration和最终质量链。candidate_checked后原RDT/Architectureowner重读实际目标，整合完整定义、必要关系及readback；implementation重绑所有真实after再最终Check/commit/独立Review。实际执行观察由本贡献唯一test.md拥有；计划、Architecture贡献及PR正文只准确引用分层结论，不复制日志或授权信息。
