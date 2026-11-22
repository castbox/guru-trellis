# D2：真实 source_locked 采用实施与验证计划

## 1. 输入与引用

整体 [Task PRD](../../prd.md)；本批 [PRD](prd.md)；实际方案和唯一来源处置见 [design §1～9](design.md)。TaskId `744a637b-a044-46cd-8cdd-77ddd85ded8e`、generation 0、D2 `26fc4284-00db-4347-b5df-35ad7845905c`。B/来源为 D1 已 delivered head `b3525d4b052f79f7d9cb4a18f827ff7c990f1983`，不是 D1 最早开发基线或最终 Release candidate。

实施前完整加载本批三正文、原 tools SKILL/contract/profile/schema、私有 release 的 Stage1/真实采用/副作用边界、quality-guidelines 的 Test And Validation Value/Validation Scope Ownership，以及 design §9 的实际知识 authority。来源/Fork由原tools检查。修改官方扩展源码不在本批方案内；若出现必要源码缺陷，回原规划/Architecture，并按 trellis-meta 和官方 index/custom-workflow/custom-spec-template-marketplace 读取，不临时补丁上游。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner 与执行 | 文件责任、完成观察及停点 |
| --- | --- | --- |
| S1 规划 | 原 Author、独立 candidate/final Architecture、Approval | 本批 PRD/design/implement 和官方 JSONL；完整计划展示后停在接受/Activation前 |
| S2 安装前事实 | actual Activation；原 tools owner从完整D1 canonical执行 | 确认source H/trellis clean、D1 delivered、Fork配对/build/API、目标/peer隔离、未完成相交事务、配置和冲突；只读preview后准备真实per-path决定 |
| S3 固定一次计划 | S2 facts；原 tools owner | 构造private-prepare，保留两个config、custom AGENTS、canonical custom workflow及目标三平台；prepare一次，消费完整 frozen plan。展示完整写删集合及原invoke命令，停在独立安装确认前 |
| S4 真实采用 | S3安装确认；原tools invoke | 原public维护和Guru installer生成全部after/manifest/pointer；按实际exit恢复同operation，不重prepare、不手改受管副本 |
| S5 真实目标验证 | S4 usable result；原tools与实施owner | V2～V5真实resolver/installed/native、完整投影/mode、同operation reapply/drift、保存和sidecar；历史观察保留，当前证据如实报告 |
| S6 知识与质量交付 | 本批完整工程事实；原RDT/Architecture、TaskCommit、Review、Delivery owners | 按§6整合真实必要知识并读回；TaskCommit另确认，constructor/begin_check固定B..H；新独立完整Review两槽，readiness、Refs #861 Publish/Merge各走原边界 |

本批没有新增canonical逻辑、schema、脚本或业务文档目标。installed实际改动及manifest/runtime由原owner产生；Task文档只记稳定计划，不写动态状态、授权、Release ledger或PR body handoff。

## 3. 验证入口、输入与预期观察

### V1：完整来源、preview、prepare

设 TASK_CHECKOUT 为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10`；命令从该目录执行。TOOLS_INPUT 是本 tools owner 的临时 regular JSON，完整公开内容为：

```json
{"profile":"install","source_ref":"b3525d4b052f79f7d9cb4a18f827ff7c990f1983","dependency_mode":"source_locked","checkout":"/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10"}
```

UPSTREAM_SOURCE 以原transport核出的真实CLI/Core bytes/mode身份绑定 `/Users/wumengye/Documents/GoProjects/Trellis/packages/cli`、实际配对Core和完整Guru/Fork roots；Fork HEAD/build必须是canonical lock的 `e3793251fad8bd261d0c370d408c7675b9f6a140`，CLI/Core均`.6`。只读命令：

```bash
bash trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/preview.sh \
  --root "$TASK_CHECKOUT" --input "$TOOLS_INPUT" \
  --upstream-source "$UPSTREAM_SOURCE"
```

实际解析完整receipt.result后检查全部真实managed edit、sidecar、public files、平台和peer事实，不只看计数。旧事务由其原owner先处理。设计§4已识别public config.yaml显式preserve，以及Guru config.yml作为非受管用户配置由原owner自动保留；后者不得进入guru_decisions，当前该数组为空；AGENTS source来自当前public inspection、content来自当前目标全文，action custom；workflow install/custom和同一immutable provider。新变化回原tools gate审查，不猜测覆盖。

Activation后，仅一次prepare：

```bash
bash trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/prepare.sh \
  --root "$TASK_CHECKOUT" --input "$TOOLS_INPUT" --plan "$PRIVATE_PREPARE"
```

PRIVATE_PREPARE字段完全来自原schema：upstream_source、selected_platforms、guru_decisions、tools_input。读取完整result.plan，保留原upstream operation/id/actions不改，目标AGENTS必须renderer幂等；保存为本owner临时FROZEN_PLAN，不写Task artifact。预期无Task/session/user/peer/common写入；展示精确真实writes/deletions，再独立确认。

### V2：真实invoke和原恢复

```bash
bash trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/invoke.sh \
  --root "$TASK_CHECKOUT" --input "$TOOLS_INPUT" --plan "$FROZEN_PLAN"
```

预期真实tools_upgraded、installed_version `.10`、unverified=[]。实际manifest/source commit/ref应为D1 immutable H且canonical trellis干净；source.tree_state按原whole-worktree观察如实保留，Task或installed after造成dirty不改写为clean；CLI记录仍`.6`，source lock相符。原API的postvalidation及actual target检查必须真实完成。遇resume_required只携原recovery_ref，从不变完整source续同operation；此结果不是成功，也不重prepare。blocked保留具体原因。原工具回退另审写集与兼容，不修改Task或reset Git。

### V3～V5：真实目标和完整保存

以下命令从更新后的目标自身入口执行：

```bash
bash .trellis/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --mode installed --json
python3 .trellis/scripts/get_context.py --mode continuation
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
python3 .trellis/scripts/delivery.py current
```

另用原target resolver运行以上需要managed Python的入口，确认实际解释器/checkout-local pointer；不借source解释器的成功冒充目标可用。实际公开Identity/Ensure按同Task/gen调用，current仍为同D2并保持原planning accepted。get_context输出是原native entry观察，不证明桌面客户端或全部平台Agent行为。

原tools owner按同frozen plan/public recovery_ref在原installer `install_assets(..., tools_only=true, tools_maintenance={source,plan,recovery_ref})` 完成合法同operation reapply；不调普通apply、不新prepare、不补历史迁移。消费实际结果，核skill/overlay/installed成功、零未解sidecar和无意外内容变化。原public plan缺失、ref失配或owner无法合法reapply则停报缺口，不能降级断言。

从canonical原managed_source_projections读取完整expected map；逐项核目标集合/bytes/执行位与原mode规则，核`.agents/skills`/`.claude/skills`/`.cursor/skills`完整根和无旧公共Codex root/private泄漏。workflow、lock、版本及真实来源分别核。public config按显式preserve、Guru用户config按原owner自动保留后的原bytes验证，AGENTS按原renderer结果验证，不把模板raw bytes当作所有生成配置的期望。manifest完整inventory与实际文件相符，无未处理`.new/.bak`。

保存观察在安装前由原tools/public owner冻结并在安装区间比较：Task/archive/workspace/session、用户配置、peer tools/common pointers和原public facts不变；仅目标tools runtime/recovery使用原许可写入。完整公共结果保持最小字段；不把保存清单或审查历史写入Task。

V1～V5是本批真实采用所需实验，不新增长期行为测试；D1未变源码的原package/source/样本结果按适用输入采用。实际安装、target native、客户端Agent、业务效果和Release矩阵各报原观察层，不互相证明。

## 4. 停止条件与适用回退点

Task/key/generation/C4/current selection、scope或source改变回原Identity/Ensure/Selection/Clarify；每批Task写前跑checkout boundary。D1来源不clean、Fork/build/API不符、未完相交事务或未知修改时停在原tools owner。prepare输入变化不重用旧冻结计划；原operation失败只同ref恢复。新的真实产品或机制差额返回原Author/Architecture，未授权源码修复不在安装内实施。

必要真实安装验证通过后停止追加。基础设施反复失败时重评入口/环境，保留具体gap；无缺口不重复D1全套或扩累计Release矩阵。保留并行工作，不覆盖或stage无关文件。TaskCommit/push/PR/merge均留原独立边界；当前只完成规划，不执行安装。

## 5. Delivery Policy（唯一）

策略为 **staged**。本Task前序D1已完整交付来源；当前D2承担真实采用和全部installed after。进入条件是实际D1 delivered、当前D2独立规划/Architecture/Approval与接受/Activation；退出条件是真实source_locked工具可用、V1～V5充分、本批完整知识/提交/独立Review及实际delivered。

本批解除D1的准备checkout旧`.9`局部限制；只有真实采用及验证成立才可写为已解除。D1的local_sample与旧installed观察保持历史。本批不留下已选真实采用给后续“补证”；未实施就是本批未完成工作。

整体准备仍由原Completion覆盖全部Delivery及accepted scope；reference_only Closure no_mutation、Finish终态归档/簿记由原owners独立处理。Stage2再取届时最新main并执行正式候选/tag/smoke/Release、选定主目录收敛和Issue关闭；本批不提前执行或宣称完成。

## 6. Docs SSOT Plan（唯一）

strategy为 **no_docs_update_needed**，限共享RDT/Architecture定义。现有R724/D724/T724、ARCH-INT-006/014/015和原tools合同已完整定义此次单目标选择、保留、来源与真实采用分层；本批只使实际installed与已交付source收敛，没有新公共语义/机制，不修改共享导航或制造空贡献/ADR。

原 `guru-maintain-requirements-design-test-ssot` 在实际采用和工程事实后复核当前指南/规范是否真有过期说明；确有差额先回Author改本唯一计划，由原writer完整整合/readback，TaskCommit前完成，再由独立committed Review审真实after。Architecture同理。历史D1说明和旧Test原观察不追改；当前public Delivery/Git结果承接后来事实，不制造一个状态提交来追自身pass/HEAD。
