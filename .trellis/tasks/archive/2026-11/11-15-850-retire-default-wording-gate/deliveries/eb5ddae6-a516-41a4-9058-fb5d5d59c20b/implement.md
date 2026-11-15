# D1 实施与验证计划

## 1. 输入与引用

整体scope见根prd.md，本批完整行为见本目录prd.md。唯一来源设计处置是design.md第3节；接口、流程、在途/安装和验证分别由第5–8节定义。固定B=a72981db56d2070d8140b468cab3a97ae82effd3，目标main；D1无前序交付。完整加载原workflow/skill、清晰写作、内容方法和必要authority后执行，不凭模板存在开始实施。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner与文件 | 具体产物与完成观察 |
| --- | --- | --- |
| I01 | Planning已批准并激活；原implementation owner | 固定当前key/B，核scope/checkout；完成consumer及历史/当前分类，保持其它Task和并行分支 |
| I02 | I01；Clarify/Readiness原packages、shared stage0 schemas | 实现design5.1的新source identity、后继full-chain/local合同、bounded review；实际wrapper能够输入三类来源，去除Wording专属前置 |
| I03 | I02；Author/Architecture/Approval/Discovery/Create/review-change及workflow/routing | 移除默认Wording路由、补审和返工依赖，保留原实际语义方法；新content_revision及只读路由唯一consumer；review-change新增aggregate2.0/explicit_files1.0，按选定Markdown全文snapshot并限定wording_only方法；原range方法/wires、Create target与评论保留 |
| I04 | I02–03；Wording包/registry/wrappers、eval/tests、current specs/docs | 删除专属scanner/分类/回执和无consumer资产；发布MIGRATION-850/version表；迁移真实caller/fixture，不搬旧证明链或预留optional scanner |
| I05 | I02–04；原tests/runtime/package validation | 执行V01–03/V06生产entry回归；保正常stale/mismatch与源当前检查；只删除无价值退役测试，不以green代替semantic方法 |
| I06 | I04–05；原tools owner和preset installer | 用完整matching local candidate preview/prepare/invoke/readback/reapply，同步dogfood/声明平台，验证V07退役/冲突/Task与session保持；如确需干净安装仅一个代表目标 |
| I07 | matching新provider；真实Agent原内容/审核owner | 执行V04/V05并读取完整输出及正常返工，分开记录实际semantic与formal出口，失败不改称通过 |
| I08 | 实现及工程事实充分；原RDT/Architecture maintenance owners | 执行delta_first的真实完整拟写与final_integration/readback，文档只记integrated_pending_review；逐个读回共享变更并保旧authority |
| I09 | I08；TaskCommit原owner及独立Review | 展示精确提交计划再提交；原constructor用完整B..HEAD/dirty内容形成candidate并begin_check；同次独立Review先Architecture再完整Check/Review，不偷跑提交前candidate Check |

I02–I04必须同批闭合后才能宣称路径退出。不得发布尚未闭合的中间状态。每项Git/GitHub副作用沿原边界由其owner独立展示和确认。

## 3. 验证入口、输入与预期观察

V01：更新并运行`trellis/presets/guru-team/scripts/python/test_readiness_transition_integration.py`，真实writer安装后执行生产producer链；补current_issue/standalone及Create写前projection，适用测试不得从旧fixture手填新token。

V02/V03：更新`trellis/skills/guru-team/runtime/tests/test_issue_review_intake.py`及`test_intake_projection.py`、`test_intake_semantic_authoring.py`的实际变更范围；增加同Delivery content revision、focus/context-return和实际旧待办接续的生产wrapper观察。V03只覆盖本次改变的合法在途，不枚举无关failure matrix。

V04/V05：通过matching安装的Clarify `standalone_wording_review`、local focus、Readiness及原Author/Approval内容入口执行真实Agent审核；显式文件使用原review-change的explicit_files/wording_only，输入含有Git差额和无差额的选定Markdown。核完整当前bytes进入snapshot，结论只覆盖本次表述及含义保留；不要求实现完整度、测试或三subagent实现审核，原range profiles仍保原方法。验收侧保留原来源和独立预期，被测Agent只取得正常请求与材料。核具体遗漏/修订owner、无词命中语义缺口、合法清楚文字和只读副作用；不能预填通过替代执行。

V06：执行原source/installed package validator、`discover-skill-contract`逐受影响exit、当前Task context validation、变更Python的内存语法、JSON/Bash与`git diff --check`；根据真实invocation失败补受影响回归。shared Interface schema保其真实其它consumer，不机械删除历史字面匹配。

V07：原tools更新与reapply必须保完整Task/session/配置/用户内容，检查retired managed files、modified local侧car和声明平台投影。运行适用`test_apply_guru_team_trellis_preset.py`、`test_issue_content_distribution.py`、`test_planning_body_distribution.py`、`test_review_sufficiency_distribution.py`及`check-dogfood-overlay-drift.sh`的受影响验证；不因常规Issue执行完整多平台installer矩阵。实际需要clean proof时只一个代表性throwaway。新source不代表已有安装更新。

V08：原RDT/Architecture owners按完整actualtargets整合/readback后，独立committed Review核变更及必要未变consumer，最终与AC01–05对应。raw失败、partial和unverified保留原观察，最终报告按源码、机械、实际Agent、安装与外部事实分别说明。

以上入口、输入及独立观察对应design第8节。计划不预填pass；已有适用工程事实可复用，但本Task新增语义行为和安装退役必须有真实对应证据。

## 4. 停止条件与适用回退点

来源/范围变化回Clarify；机制/owner/持久化/SDK/外部边界扩张回原Architecture及最早受影响Planning；正常错配回原producer，不手改hash/state或重标结果。API/profile混用先按MIGRATION-850恢复同一旧操作或从当前对象重入，不继续串联失败出口。

受管更新先preview，保原backup和同操作恢复；冲突或不明用户内容沿原tools/installer处理，不能手抄managed文件。未提交的本Task源码修订由原writer纠正，保并行内容；不新建通用rollback协议或清理其它Task。若选定验证重复遇设施错误，重新判断足够观察方式或保留具体缺口，不无限修设施或放宽验收。

证据足以支持design第8节映射的验收后停止额外实验。未解决的行为/安装缺口不能宣称AC通过。固定旧provider恢复不得被新envelope冒充，合并前仍待协调器处置。

## 5. Delivery Policy（唯一）

Policy：full。当前slice为整体accepted scope的R01–R04、AC01–AC05；D1负责默认退出、语义责任、显式只读、直接API/在途/安装迁移及全部验收。没有把必要迁移留给未指派后继。

独立可交付条件：全部当前受影响入口/consumer/version同步闭合；退役专属资产退出；合法在途保原identity与有效覆盖；真实Agent和适用安装验证支持五项AC；完整docs整合与原质量gate通过。验证边界为design V01–08，完整多平台Release矩阵未覆盖。

剩余责任：Delivery后的whole-Task Completion、source Closure、Finish及适用Cleanup仍由原owner承担；合并不自动关闭Issue或完成Task。源码、实际安装、Agent、外部调用和终态结果不能互相替代。

## 6. Docs SSOT Plan（唯一）

Strategy：delta_first。原RDT owner在`docs/requirements-design-test-contributions/850-wording-retirement/`准备完整requirements/design/test/traceability差额，实际目标为current issue-content、local-fix-intake及task-delivery受影响关系。原始历史证据、旧版本和无关能力不追溯改写；不向根/current README追加逐Issue登记或无关global version。

Architecture真实隔离贡献为`docs/architecture/contributions/850-wording-retirement.md`，ADR候选由本目录`architecture/adr-wording-retirement.md`拥有。原Architecture owner更新system/ownership/issue-review-intake必要完整单元、change-contract两个完整受影响章节、runtime-location明确Git对象章节、ARCH-INT-044/ARCH-DOM-061及ADR窄替代关系，保留#819历史before及九concerns/check合同；原RDT不写Architecture正文。canonical workflow/spec/README的运行说明随真实接口修改，dogfood由原tools分发。

直接consumer是工程完成后的原final_integration与独立committed Review。整合前重读live target与expected-current，合并实际重叠，写后逐个readback；结果只为integrated_pending_review。TaskCommit包含全部after，Review判断实际before/after后才可reviewed_promoted。Planning不写shared current，不制造空contribution、审计账本或授权字段。
