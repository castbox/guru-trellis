# D1：公共方法实施与验证计划

## 1. 输入与引用

本批输入为整体 accepted_scope 的 AC693-01..04、本目录完整 PRD、design 第3节唯一来源设计处置及实际独立 Architecture candidate_assessment。B/H0 为 `e514770dfa03711a4606046232593b9bf782695a`，没有前序 Delivery。

实施前读取 design 第4节列出的当前 canonical 方法、原 owner contracts、RDT knowledge-maintenance 完整单元及必要关联，另读项目 constitution/change-contract、current-knowledge 与适用 preset/spec。方法引用必须实际加载；原事故材料和命令只读，不能将历史事实直接称为本批执行。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原 owner 与实际文件 | 行为及完成观察 |
| --- | --- | --- |
| S693-01 取证与净差额 | 已激活方案；implementation/原语义 owner；本批 design 的事实部分与原 source locators | 核当时规则、消费者、参数对象/时序、测试入口与 E30；补可得最终 public/PR事实，记录不能恢复的理由，不改原始证据或伪造根因。 |
| S693-02 共享方法 | S01；原共享规则 writer；canonical workflow-contract/quality-guidelines | 补 design §4 的具体方法；保留原全范围、独立性、工程事实适用性、合法 fixture/局部测试和最小验证边界。 |
| S693-03 原 consumers | S02；原 Author/Architecture/Check/Review/Delivery contracts | 各自在原职责内加载并应用唯一正文，明确当前 consumer 可用性与证据判断；不增步骤、public字段、runtime分类器或证明账本。 |
| S693-04 隔离知识 | S02/03；原 RDT 与 Architecture owners；本 Task 两类 contribution/proposed targets | RDT 准备 knowledge-maintenance 三层完整定义与稳定关系；Architecture 准备完整 change-contract。shared current 尚未写入，保留完整 before 和必要来源。 |
| S693-05 分发与定向验证 | S02..04；原 preset/implementation；当前 checkout 受管副本 | 完整 apply，同步 installed/声明平台/spec，执行§3定向检查并处理实际 sidecar；不覆盖用户或并行改动。 |
| S693-06 完整候选检查 | S05；原 implementation → independent Architecture phase2 → Check candidate profile | 构造实际完整 candidate/begin_check，审全部实现/拟写/未改 consumers；通过后沿原合法 rework 返回 implementing，不能写最终 Check pass。 |
| S693-07 最终整合与质量链 | S06；原 Architecture/RDT final_integration，然后 implementation/最终 Check | 固定真实目标，比较组合语义，写入读回；同 B 对实际全部 after 重绑，完成匹配 Architecture/Check、精确 TaskCommit、独立 committed Review、Delivery Review/PR readiness。 |
| S693-08 公共交付与剩余责任 | S07；原 Publication/Merge 与 Completion/Upgrade owners | 仅以真实当前 gates 进入精确 push/PR/merge 边界。D1 合并后以完整公共源交原正式升级；后端安装和项目指导差额另核目标并显示写集，未完成前不做整体完成声明。 |

没有业务数据或执行状态的临时限制需要解除。本批的尚未验证项按实际证据层保留，不制造新开关、恢复状态或限制台账。

## 3. 验证入口、输入与预期观察

依 design §8 的 V693-01/02，由当前原 owners 实际完成只读取证与语义检查。工程入口如下；它们是计划，不是已执行结果：

```sh
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
python3 -m json.tool trellis/index.json
for script in trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh; do
  bash -n "$script" || exit 1
done
python3 .trellis/scripts/task.py validate .trellis/tasks/10-31-693-contract-evidence-adoption
git diff --check
```

另按 `.trellis/spec/workflow/quality-guidelines.md#python-syntax-check` 原 in-memory 命令检查其声明 Guru 源码范围，不使用写 bytecode 的 py_compile/compileall。对真实受影响文件做 Markdown 路径/引用及敏感内容核对；不新增只锁定文本或镜像实现的测试。受管 `.new`/`.bak` 的判断以实际前像、用户修改及 ownership 为依据，不统一覆盖或删除。

上述覆盖 V693-03..05/D1-AC04。原 candidate Check、final-integration/readback、实际 after 重绑、最终 Check 和独立 committed Review 覆盖 V693-06。只复用可核验且仍适用的实际工程事实；任何输入/分支变化或适用性未知的命中验证重新执行，采用结果不写成当前执行。

不跑业务回归、现场复现、付费 provider、部署或 QA；不跑专项 replay/A-B/native eval/固定数量或完整矩阵。完整 apply 是当前 dogfood 受管同步，不是另建安装环境；后端唯一正式采用属于后续原升级操作。

## 4. 停止条件与适用回退点

身份、generation、branch/checkout、当前 key/scope/root 或原输出不匹配时回对应 Identity/Ensure/Selection/producer，不换 Task 或借别的会话。范围/来源改变回 Clarify；方法或真实职责改变回 Author/Architecture；普通正文或实现缺陷回当前原 owner，刷新其实际依赖。

缺验证依赖只阻塞依赖它的判断；失败保留首失败与实际层级，修复不掩盖原观察。shared-current 或 expected-current 冲突回原 maintenance，保留并行内容。不凭脚本通过、历史 green 或 phase 恢复 pass。

本批没有 DB、配置、部署或业务状态迁移，不新增回滚协议。公共文件按本 Task 精确 diff 修订，Git/GitHub 与清理仍沿原 owner 的独立操作边界。正式升级先 read-only preview 和状态保护计划，当前步骤不写 backend。

## 5. Delivery Policy（唯一）

策略为 **partial**。D1 独立交付整体 AC693-01..04：有来源的历史原因/未知边界、合同与证据方法、原 owners 与 Guru 项目指导承接、canonical/dogfood/平台分发及原质量链。公共源码与规范一致后可独立合并，PR 为 Refs #693。

剩余 AC693-05 为公共交付后 ai-chat-roleplay-backend 的正式升级和项目原 Architecture/Design 指导采用。原 Upgrade owner 固定完整 source，核安装、在途 Task/会话、工作区与精确写集，沿原合同执行并验证；必要项目指导差额回其原 authority，领域定义不复制。该外部采用证据不以空 Delivery 或公共合并替代。若实际存在独立代码/文档交付需求，由原 Completion/Creation 判断真实切片，不自动创建。

Task Completion 必须同时满足整体 scope、各 Delivery 真实结果和后端采用证据；权限/环境阻塞如实保留，不能宣布 #693 完成。安装成功仍不证明业务修复、部署或 QA。#692 不由本 Task 启动，也不因与安装无关的工作自动继承其阻塞。

## 6. Docs SSOT Plan（唯一）

选择 **delta_first**。共享方法由 canonical workflow-contract/quality-guidelines 单写，step-local 行为仍归各原 package。原 RDT owner 在 `docs/requirements-design-test-contributions/693-contract-evidence-adoption/` 准备完整 proposed requirements/design/test knowledge-maintenance 单元与 R693/D693/T693 关系；原 Architecture owner 维护 `docs/architecture/contributions/693-contract-evidence-adoption.md` 及完整 change-contract proposed target。真实差额与来源处置只按 design §3/4/9 消费。

直接 consumers 是当前实施、原独立 Architecture/Check/Review/Delivery 判断与后续安装采用。原 candidate Check 后，两 maintenance owners 才 final_integration 写 shared current 并读回；实际 after 重新绑定，最终质量链覆盖所有正文/关系/投影。Planning 不直接写共享导航或 current。没有新 identity/导航关系时不改总 README；必要引用和平台说明由实际影响判断，不为形式制造额外文件或全局版本。

历史 contribution、命令、失败与当时未知保留原义；本批实际结果在原 RDT Test contribution 中记录一次，当前单元只定位该来源，不构造永久审核或逐测试台账。后端采用由原升级结果提供其实际证明，不复制其私有 transaction 或用户授权。
