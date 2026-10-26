# existing verifier 的 AGENTS custom 调用适配：实施与验证计划

## 1. 输入与引用

输入是根 `prd.md` 的整体 accepted_scope、本批 `prd.md` 的AC7/AC8及 `design.md` 第3节唯一来源设计处置。实施前实际读取 tools contract Forward behavior4、当前caller/compose、现有caller测试、原 `test_agents_target.py`，并按 `.trellis/spec/preset/index.md`、installer适用条款、companion-scripts、quality-guidelines 的测试价值/验证范围/语法检查和 subtraction-first 规则执行。

本批起于已完成的gen0准备交付，增量只修caller。独立Architecture candidate_assessment不是final_plan；Wording、最终Architecture、Approval和Activation仍是实施前依赖。第一轮载体按design第9节的双轮恢复路径执行，没有真实Activation不派实现Agent写源码。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原owner | 文件、动作及完成观察 |
| --- | --- | --- |
| I1 规划收敛 | 原Clarify核双轮恢复范围，原Author更新；再Wording/final_plan/Approval及Activation | 只写该Delivery规划及官方context JSONL；保留同key，不能把文件存在当批准 |
| I2 caller修复 | Activation实际成立；原Trellis implement Agent | `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py`：真实preview AGENTS row→唯一custom；从原preserve列表排除该路径，其余不变 |
| I3 回归与自检 | I2；同实施owner | `trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py`：修订现有测试，覆盖unchanged/conflict、其它preserve、原compose消费及单次冻结调用；执行V1/V2和必要静态检查 |
| I4 提供可寻址H | 原TaskCommit展示精确必要dirty提交并单独确认；原Publication再展示early Draft动作并单独确认 | 提交本批必要代码/测试/规划与Task恢复差额，保留无关修改；随后push同H并绑定Draft。无临时手工提交、无空commit、无提前Ready |
| I5 原入口验证 | H已提交且canonical源码clean，远端H可寻址；原check/实施协调者 | 新空仓外work root执行V3；与同B/H的独立early完整内容分析并行。运行期间不改源码；保留旧失败目录和新原始结果 |
| I6 第一轮完整恢复Review与整合 | 完整existing及完整candidate Check；已合法回implementing | 原独立reviewer以原early Review入口审完整固定B..H、拟写/实际空写集、全部受影响consumers和验证，零开放P0–P3才由协调者继续原candidate_checked的唯一consumer；原Architecture/RDT亲自完成no-change整合，无共享写入 |
| I7 第二轮完整正式Review | I6后实际candidate重绑，matching final Architecture/公共Check及原TaskCommit | 原独立reviewer重新完成全范围正式BranchReview并写真实公共full_review；不得用第一轮、candidateCheck或窄增量检查替代。Ready/合并再由原owners处理 |

实现Agent只拥有I2/I3的两个业务文件；主会话拥有规划、spec适用判断、提交与收尾；check/独立review按原职责操作。任何规划外观察只回candidate ref、现象、locator与最小复现，不自行扩改。当前两个非生成Python文件均低于3000行；变更后继续核对。

## 3. 验证入口、输入与预期观察

V1 / AC7：在Task cwd执行现有caller测试，更新后的测试实际消费原compose合同：

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=trellis/presets/guru-team/scripts/python \
python3 -m unittest \
test_verify_trellis_upgrade_contract.VerifyTrellisUpgradeContractTests.test_native_bootstrap_tools_freezes_one_original_owner_plan
```

V2 / AC8：设置 `GURU_UPSTREAM_DELIVERY_CLI` 为匹配F checkout的 `packages/cli/bin/trellis.js`，使用真实public maintenance API执行：

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -m unittest discover \
-s trellis/skills/guru-team/packages/guru-upgrade-tools/tests \
-p 'test_agents_target.py'
```

V2只证明受控临时fixture，不证明远端正式来源。测试前核F的HEAD/build marker，环境变量使用本次真实本地路径，不把本机workspace映射写入本计划。

V3 / AC8：先从真实前驱tag读取manifest/lock，核CLI一致后派生版本和commit；核F/P的HEAD、tree、build marker与clean。设置 `TRELLIS_FORK_SOURCE`、`TRELLIS_PREDECESSOR_SOURCE`、`TRELLIS_PREDECESSOR_COMMIT` 为匹配本地构建和前驱commit，`TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#H`。`VERIFY_ROOT`为新仓外空位置，保留旧失败root。然后执行原入口：

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh \
  "$VERIFY_ROOT" --mode existing --platform codex \
  --before-tag v0.7.0-guru.5 --before-cli 0.7.0-castbox.4
```

必须核原maintenance、reapply、retired assets、local-edit conflicts、sidecar及终态；prepare成功或exit0但缺原断言不能替代完整结果。真实错误保留首失败、返回码和输出，交原owner判因。所需Git、Node、CPython及managed bootstrap/marketplace网络缺失只阻塞依赖项，不伪报通过。

V4：按quality-guidelines的Guru范围内存syntax检查，并对两个changed Python文件补同一compile操作；运行source Skill validator、ownership、实际managed/dogfood drift及 `git diff --check`、residue检查。先读实际inventory确定是否存在安装投影差额；不通过修改旧archive、官方资产或runtime guard消除preflight拒绝。无overlay变更不制造overlay写入。

V5：原Check按当前完整slice判断测试充分性、Docs、减法与证据边界。第一次完整恢复审查在candidate Check之后、no-change整合之前，实际调用early Review入口，并独立确认零开放P0–P3。第二次在重绑、final公共Check与原TaskCommit之后，实际执行完整正式Review并记录full_review。两次均覆盖各自完整B..H及未改consumers；early DTO不转为formal gate。准备H的结果不转为新的最终Release候选通过；修复和Finish合并后，Stage2重新冻结并验证。

## 4. 停止条件与适用回退点

实际source/scope变化、候选Architecture冲突或缺当前Approval/Activation时，不开始I2。design第9节承接要求实际Architecture/RDT均no-change且无shared writes；出现真实共享变更、候选改变或未闭合finding时，停止当前承接并回原owner修正刷新。

caller测试、真实tools测试或existing失败时，保留首失败和原root；只在原原因/范围判断后修复，不编辑生成input/frozen plan、过滤合法输入或放宽guard。正式来源不可用时保留未验证，不改用本地provider冒充。普通source或计划变化回原受影响owner刷新；不沿用旧候选pass。

本批无业务数据迁移或生产发布，因此不新增业务回滚协议。已有tools维护的恢复/回滚归原同计划owner；本地源码修订保留并行差额，不reset/stash/revert无关修改。Git/GitHub动作继续逐项展示精确对象和当前确认。

## 5. Delivery Policy（唯一）

本批为full：完整交付所选AC7/AC8，包含唯一custom caller适配、现有合同回归、真实tools target测试和完整stable existing验证。缺其中一项时不能以prepare成功或代码完成声称slice完成。原gen0交付保留；本slice不承担Stage2。

整体Completion由原owner核全Task要求与历史/当前Delivery后决定。Release、最终candidate/tag/smoke/Issue关闭仍归#656的Stage2 owner。第一轮载体只解决本切片的恢复承接；整合前后两次完整独立审查及最终真实公共full_review均为必要条件。没有其它延期实现或隐藏后继切片。

## 6. Docs SSOT Plan（唯一）

strategy为`no_docs_update_needed`：本批让release verifier遵从tools contract已有行为，不新增产品能力、公共输入/状态、架构职责或安装机制。命中的native R/D/T完整单元见PRD第7节；AGENTS custom细则由原tools contract拥有，本批不复制为第二SSOT。测试修订与原始执行结果由实现/Check在其证据层消费，不创建tracked发布进度或Test摘要账本。

原RDT owner仍在phase2判断实际完整候选及当前知识适用性；原Architecture owner保持各阶段独立判断和no-impact纪律。只有两者实际确认no-change且没有共享写入时，design第9节承接才适用；真实Docs差额回原owner和Clarify，不因本计划选择strategy强行忽略，也不先写共享CURRENT、空contribution或ADR。当前两文件修复不扩张完整多平台Release、真实业务或生产矩阵。
