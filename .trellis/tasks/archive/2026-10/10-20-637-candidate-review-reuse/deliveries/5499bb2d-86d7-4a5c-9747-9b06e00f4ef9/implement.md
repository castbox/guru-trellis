# #637 D1 实施与验证计划

## 1. 输入与引用

整体为 `../../prd.md` 公共accepted_scope，本批为同目录PRD的AC637-01..10；唯一来源设计处置见design §3。独立candidate评估已完成，仍需Wording→Architecture final_plan→Approval→展示/接受→Activation。B=`39169628f5f79cb48673eae96a36670e73f4dbbb`，无前序Delivery，#636实际接口已在B内，#638未来组合未验证。

必要输入包括canonical workflow固定候选/Phase2/Review/Publication routes、workflow-contract的SSOT/Interaction Budget、quality的Test And Validation Value/Validation Scope、subtraction-first-compatibility、七package Skill/contract/current schema、#578事实规则、#636早期入口及MIGRATION-578/600/636。RDT `.113`生命周期三完整单元及Architecture `.104` constitution/change-contract/current/domain/integration/governance约束拟晋升。实际读取引用条件，JSONL引用不证明已读。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖、责任、文件 | 行为与完成观察 |
| --- | --- | --- |
| I637-01 | 计划接受/激活；实现owner；canonical workflow-contract和七package Skill/references | 写唯一适用性定义，修订冲突、finding复核和共享引用；保留首次独立完整及当前结果，脚本不判断语义。 |
| I637-02 | I01；实现owner；canonical workflow、preset overlays的continuation/prompts/派发、trellis/workflows/guru-team/README.md和trellis/presets/guru-team/README.md、MIGRATION-637.md | 入口仅加载路由，明确wire值后继及matching在途迁移；删除重复无consumer条款，不加reader。 |
| I637-03 | I01；测试owner；七package原tests、runtime/delivery_projection/tests和命中eval | 复用原harness扩展真实public wrappers/Git测试V01/04/06，不造平行框架；含退休checkpoint/绑定/#636组合。 |
| I637-04 | I01/02可运行；实际独立Agent和原命令owner；临时matching安装 | 执行V02/03/05，真实判断/正式调用；记录检错、覆盖差额、分阶段elapsed。旧/新同构，fixture不冒充Agent。 |
| I637-05 | I01..04；原installer/验证owner；独立matching source dogfood/单clean仓库 | apply/reapply、installed wrappers、声明平台、sidecar/mode/drift；开发Task不热迁移。 |
| I637-06 | 实现/证据充分；原RDT/Architecture owners；§6贡献及拟晋升完整targets | 独立Phase2比B中原authority并审完整候选/拟写内容；原owners expected-current晋升/读回适用；最终Check包含实际写入。 |
| I637-07 | 最小自检后可早期反馈；原TaskCommit/Publication/Review owners | 经#636原入口，分别展示commit和push/PR；V07同PR组合。最终Check→精确commit→独立committed Architecture/完整当前Review→Ready/Merge，各自边界保留。 |
| I637-08 | 交付与证据充分；原Completion/Closure/Finish/Cleanup | 核全部AC及satisfying PR，逐owner完成整体关闭/归档/资源；合并不代替Task完成。 |

每写批次核Task/generation/key、branch/cwd/registered checkout，只改本次文件并保留无关dirty。新责任/字段/compatibility先回原qualification/Architecture/Author，不临时扩范围。

## 3. 验证入口、输入与预期观察

使用任务root的Python3、实际`.trellis/scripts/common`；包根为`trellis/skills/guru-team/packages`。先命中小集，只有新改动/失败/未决风险才扩展；以下尚未执行。

1. V01/04：以 `TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-check-task/tests -p test_delivery_flow.py` 起步；运行 `guru-review-branch/tests/test_promotion_alignment.py`、`runtime/delivery_projection/tests/test_fixed_candidate.py`及新增差额用例。观察当前gate/predecessor、同Delivery恢复与零无因整合；fixture不证明AI。
2. V06：对受改七package运行其现行tests与命中eval；读取真实入口依赖，缺公共common导致skip不算pass。TaskCommit/Publication `test_early_draft.py`必须命中。没有代码改变不为计数加镜像文本断言；受改非生成代码超过3000行先原规范拆分/小解耦审查。
3. V02/03/05：actual Agent读matching installed入口。A首次完整，B同树/定位/无关target，C真实文档冲突含未改consumer，D正常共享依赖错误，E原命令不可得/环境变化，F finding修正。每轮由原owner判断并正式invoke，不导入eval私有helper制造结论。样本经真实公共Task/Delivery创建/选择/Planning建立状态，不手改state/hash。旧/新同初始样本分语义、命令、正式记录、远端等待计时并比较检错。临时资源沿测试原生命周期释放。
4. V08：独立matching source验证位置执行 `bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .`，再 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 和 `bash .trellis/guru-team/scripts/bash/check-skill-packages.sh`；完整reapply再查drift。复用installer声明平台/parity/ownership/mode检查，核逐个`.new/.bak`。单clean安装还运行V01的真实installed wrappers，不只比源码。执行前展示精确验证位置，开发活动安装不热替换。
5. V07：matching installed原#636 early commit/Draft候选接续正式Check/Review；本Task真实PR动作在其分别获准后用于同PR组合与readback。未执行远端时保持未验证，不以fixture代替；Merge前读真实required checks并记录实际等待。#638未来接口明确未验证，由后项组合。
6. 最终 `git diff --check`、完整当前candidate Check及独立固定B..H Review。采用命令注明原实际结果/对象及依赖环境适用理由；缺单项补单项，不用旧pass/token填新结果。

早期commit最小自检为diff hygiene、被改package/runtime命中unit/contract和原consumer graph检查；重型样本/完整安装可Draft后继续。真实失败和风险要求检查不能省略。精确执行、首次失败只由唯一Test记录，不能预填green。

## 4. 停止条件与适用回退点

身份/selection/checkout错配停止写入并回原Identity/Checkout/Bind/Delivery selection；不遮蔽官方session。scope/source变化回Clarify，机制/职责变化回Author/Architecture；普通实现缺陷由实现/Check修复。缺原覆盖补审，不能界定组合影响则完整审。缺原工程结果补跑对应检查；外部环境不可用如实blocked/SKIP，不称pass。

promotion target/current错配由原RDT/Architecture按实际差额处理，冲突停止，不覆盖并行贡献。安装冲突保留用户内容和sidecar，由原installer恢复；产品验证在隔离位置修正。没有业务数据迁移/部署/生产写入，不新增业务回滚协议；只撤本次可逆内容，保留其它worktree。

commit、push/PR、merge、Closure、Finish、Cleanup各有原边界。脚本错误保留具体诊断，同owner新round重入；授权不写任何文件。

## 5. Delivery Policy（唯一）

`full`。D1承担全部八项行为和十项AC，无延期实现责任。固定B..最终H及受影响依赖完整覆盖，实际Agent/命令/安装/#636组合证据充分后，才可判本批独立交付。没有前序Delivery，不以新切片掩盖返工。

外部边界为#638未来组合（后项owner负责）、业务采用/队列、生产效果、完整Release/升级多平台矩阵，均非本Task范围。Completion仍逐项核AC、全部Delivery和证据，Closure/Finish另真实完成。full计划、PR或MERGED都不表示这些验收已经完成。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。原 `guru-maintain-requirements-design-test-ssot` 唯一写RDT，隔离贡献根为 `docs/requirements-design-test-contributions/637-candidate-review-reuse/`。requirement/behavior承接R637-01..08，design承接候选适用性和七owner，test承接V01..08/AC。`test.md`唯一维护本轮实际结果、首次失败、耗时和未验证边界，不复制全套原始日志或授权。

目标是RDT `.113` 的 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 中固定内容/最终审核/早期反馈关联完整单元。原RDT owner执行task impact/reconciliation，保留#567/#578/#636仍有效条件，按写前live expected-current晋升完整后继及必要导航/版本。Planning不写共享导航或空贡献，普通读者不回放增量链。

Architecture真实贡献和ADR候选见design §9。原owner维护`.104`的current/domain/integration/governance完整定义及必要窄决策后继，保持constitution v1、九concern、descriptor1/result2.0与single-writer。独立Phase2先审全部候选/拟写targets，原owners晋升并判断实际适用性后，最终Check、TaskCommit、独立committed Review覆盖实际差额。无关live版本先判适用性，不触发无因整合/重复晋升。

直接consumer是Planning/Check/Review/Publication/Completion及后续Task知识读取。共享spec由canonical单写并原preset投影，README只导航。旧全新重审条款同批退出，历史ADR/归档可追溯而非current兼容consumer；知识晋升不证明Release或外部采用。
