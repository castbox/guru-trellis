# #553 唯一 Test 与证据边界

状态：产品实现、定向回归及受控完整 installed/native 接续已完成；工程 Task 最终语义门禁分别由原 owner 判断。此文独占实际结果；规划/expected不写作PASS，fixture语义不冒充真实AIGate或原业务恢复。

| Test | 观察对象/入口 | 当前结果 |
| --- | --- | --- |
| T553-01 | 原Planning/new_pair/conflict/baselineOnlyReconcile/exactCommit/Activation同身份公开接续 | transport fixture PASS；完整installed样本经原Author/独立Architecture/Wording/Approval/Activation初次接受、官方implementation rework及同scope重规划再次批准，再经真实new_pair/add-add冲突、AI基线审查、exact executor/record/check/invoke与Activation恢复，PASS |
| T553-02 | 临时index的精确tree与无关staged/unstaged/untracked、同请求commit恢复 | 产品executor PASS：真实index字节与pending内容保持、精确双父tree、同请求返回同commit且commit数量不增加；selected add/delete/mode保持 |
| T553-03 | 普通HEAD/base/index/tree变化、unresolved、受审路径unstaged，原对象保留 | 产品executor PASS：九类正常变化分别停止并保持原Git/index/worktree内容；没有恶意篡改或竞态测试 |
| T553-04 | 原实施后resolved_candidate与no-conflict行为 | 变更后固定组合原39项runtime、新增4项runtime和8项contract，共51项/90.204s/OK |
| T553-05 | 一个完整current installed样本的原公开consumer和native current/continuation | PASS：同Task553-baseline-sample/gen0/D1唯一且phase implementing；原正式Approval token及Activation accepted result实际产生，Activation恢复同result。官方native get_context currentTask/currentDelivery匹配同key，continuation合同正确加载；没有声称Codex客户端会话或原backend恢复 |
| T553-06 | package/runtime/descriptor平台投影、reapply/bytes/modes/drift/sidecar | source package38/114校验PASS；声明平台inventory/native-load合同16项/2.115s/OK。完整Codex样本二次reapply PASS，1943个source runtime/package文件和1610个Shared/Codex投影bytes/modes一致，workflow bytes一致、零sidecar；旧dogfood拒绝和drift失败单列 |

## First failure与固定组合

本轮live main为3d68f0e4c，Issue #553 OPEN正文无新增评论。Current API组合以canonical task-delivery-migration合同绑定：CLI tar5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916，Core tar45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967。现场核对installed713+270文件bytes/modes，与tar完全相符；不是仅匹配版本字符串。

该组合的真实临时Git/module样本产生合法文档冲突，AI/fixture正常解决后存在active MERGE_HEAD、零unmerged和stage0 tree，Check slot为null。原candidate返回conflicted，原ordinary post_plan executor重复merge并返回reconciliation_failed/merge，HEAD保持。这是module first failure；当时尚没有完整已批准重规划/native链证明，变更后的完整证据见下节。

## 完整 installed 样本的实际接续

受控样本使用唯一 Task `553-baseline-sample` / generation 0 / Delivery `46d368ba-d8c5-4d1f-be05-d4b1babcbb0c`。整体source要求 `app.py` 输出 `Hello Guru`、保留双方普通Architecture贡献；验证完成时实际仍输出 `Hello`。原公开scope与Delivery创建、两轮独立candidate/final Architecture、Author、Wording、Approval均真实执行；初次Activation后由官方implementation-owner rework返回planning，再完成同scope活动重规划批准。规划token来自原Approval recorder/check/invoke实际stdout，不是caller根据文件hash合成。

本轮批准token为 `planning:a9308f1a3c81f5e881522d69be1e9f932872a45dca7c0c3a11c48c136a15fd99`。prior HEAD `3103d393433dbcb33285cdfdd537c4a1f15b46d5` 与新base `2ac93238ebf65c9efdc830f627897aca41c1292b` 在唯一merge base `4e24a53646ba552b26b17b3c635d516fe6f7cbdb` 后合法各自新增贡献文档，真实Git产生add/add冲突。当前AI逐字审查两parent和解决后的正文，保留两份贡献，确认source、Architecture和当前规划仍适用；原candidate命令执行基线assert实际exit0，未运行完整业务Check。

原exact executor创建 `0fe138efb92c16c56a0e713066a3e6b46013f9bc`，精确父序为上述prior/new base，tree为 `a3b610bd713b1cda49d8fcdb6b0b6ca4de26cd7a`，只有 `docs/architecture/contributions.md` 改变。真实index字节、无关staged/unstaged/untracked、三份规划字节保持。同请求恢复返回同commit且commit数量不变。原record/check/invoke实际返回 `reconciled -> delivery_activation`；原Activation及其恢复返回同 `planning-accepted:1445449f-08ae-4359-812c-13687b195de5`，同key回到implementing。官方native runtime的current query和continuation分别核验；Check/full_review/readiness均为null，没有提前产生业务门禁通过结果。

保留harness首次失败：已完成事务的真实receipt最初以外层intermediate transport传给recorder，被schema_mismatch拒绝。对同owner实际receipt做`.result`薄投影、fresh读取当前facts后原consumer继续完成；没有改产品、重跑executor、创建第二commit或把失败改写为PASS。该失误属于验证装配层，区别于原产品first failure。

源工作树模板的初次39项runtime通过后，切换到合同固定installed assets再次执行39项/72.249s/OK；后者为当前baseline。保留先前来源身份不同的结果，未将它升级为固定组合证据。

## 安装与未覆盖边界

一个受控clean current样本由固定CLI的native-delivery-v1初始化，采用本轮完整source canonical workflow/preset；安装成功。首次仅复制trellis目录导致source-owned manifest缺失，失败已保留；改用完整source installer恢复。该sample不是原业务树，也不是formal released source-lock。

当前source repo完整旧dogfood承载本工程Task生命周期；ordinary reapply已拒绝upstream_delivery_migration_required，旧历史未迁移，未半升级。新模型的完整installed projection另验；旧dogfood停点不计新模型同步通过。若该边界妨碍本次真实accepted验证，原Check/Completion负责判定，不自动豁免。

变更后完整sample reapply首次产生13个原Reconcile受管`.bak`，installed validator如实因sidecar/provenance未收敛而返回conflict。逐项确认替换文件等于canonical后，将旧内容移至sample外临时证据目录；第二次完整reapply返回installed，source/installed/activation validation全部通过，无`.new/.bak`。没有修改业务仓或旧dogfood的generated文件。

source dogfood drift命令实际失败于`.claude/commands/guru/finish-work.md`。对base HEAD直接读取installed entry与canonical overlay，已存在相同模型差异；本Task未修改该入口。该失败不是新模型投影PASS，现有完整旧安装的切换仍归原迁移owner。未运行全平台native host/clean-existing-update/Release矩阵。

静态验证PASS：marketplace index JSON、44个shell语法、270个Python编译、Task context validate及diff whitespace。Task context validate提示部分大文件注入会截断，语义owner另行直接读取当前完整文件，未以截断注入代替审查。

backend #148、CMS Issue #1、业务仓upgrade/cleanup、原业务会话恢复、完整多平台/Release矩阵均未执行。fixture提供的规划/owner结果只证明transport；独立Architecture、真实semanticCheck/Review/readiness以及发布结果各由原owner分别判断。
