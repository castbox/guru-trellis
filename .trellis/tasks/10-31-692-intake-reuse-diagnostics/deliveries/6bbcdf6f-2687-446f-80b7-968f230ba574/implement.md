# D1 实施与验证计划

## 1. 输入与引用

输入为当前 Task accepted_scope、[本批 PRD](prd.md)、[设计](design.md)和其第3节唯一来源设计处置。固定 B 为 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`，D1 id 为 `6bbcdf6f-2687-446f-80b7-968f230ba574`，没有前序 Delivery。

实施前读取命中包的实际当前文件、`.trellis/spec/{workflow,preset,docs}/` 适用规则、canonical current-knowledge、project authority 和真实引用条件。原 #693 的 Candidate Applicability And Coverage/Test And Validation Value 继续由各原 owner 消费，不复制或重建方法。当前 candidate Architecture 已实际返回 no_architecture_impact；最终规划尚须 Wording/final_plan/Approval/用户接受。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与原 owner | 文件、动作与完成观察 |
| --- | --- | --- |
| I692-01 | 当前规划接受并由原 Activation 激活；实施 owner | 复核同 Task/D1、checkout boundary、固定 B 和全部 dirty；按 canonical matching source同步本 Task dogfood，处理原 managed provenance/sidecar。基线 #706 投影单独说明，不计 #692 功劳。真实 helper错误保留首错，沿原升级/恢复owner，不手改hash或换身份。 |
| I692-02 | I01；各原 Markdown owner，当前实施者执行其已审方案 | 修改 selector、Create Issue、Discovery、Clarify、Author 的上述 SKILL/reference 源；每处明确触发、必须重读、可继续用事实、亲自重审和consumer。按设计第4节具体落点；global workflow保持原图，只调整实际必要的定位文案。README提供原入口定位。 |
| I692-03 | I01；Discovery deterministic owner | `runtime/common.py` 拆原复合比较并补 base/目标的现有诊断；`check.py` additive diagnostic，`invoke.py` stderr承接被收窄错误。保留原拒绝/code/status/typed DTO；修改必要 `commands.json`、`errors/catalog.json` 与合同说明。无新provider读取。 |
| I692-04 | I02/03；Discovery tests owner | 在原 `tests/test_runtime.py` 真实录制/wrapper场景补普通结果配错、完整/分块输出读取和原base/目标类别的可观察诊断。优先复用现有 setup，不新建全局 fixture/evaluator；不增加故意改digest/state场景或只锁文字的测试。 |
| I692-05 | I02/03；原 RDT maintenance owner | 按第6节建立完整隔离 R/D/T proposal、稳定关系与唯一 Test 结果落点。由原 Architecture 对真实实现及拟写目标评估，不用规划no-impact代替当前判断。 |
| I692-06 | 完整代码/合同/隔离proposal；实施与原 Check owners | 同步 canonical→dogfood，执行第3节定向验证；以固定B、实际HEAD和全部dirty建完整candidate/begin_check，执行独立Architecture phase2及完整candidate Check。 |
| I692-07 | 原 candidate_checked；原 maintenance owners | RDT final_integration读取并写入真实目标/必要导航，读回并核适用性；Architecture no-change则无空写入。实施重新绑定包含所有晋升/关系/导航的candidate，最终Architecture/Check。 |
| I692-08 | fresh最终Check；原 Commit/独立 Review/Delivery owners | 精确TaskCommit、独立完整B..H Branch Review、PR readiness、原Publish/Merge；各Git/GitHub副作用按当时精确计划处理。保留same Delivery/分支/工作树。合并后回整体Completion/Closure/Finish/资源处置。 |

每次 source/test/task 写入前运行 checkout boundary。当前工作者独占 #692 文件，不 revert、格式化或提交并行内容。没有真实临时能力限制或需延期的实现，不制造后继切片。

## 3. 验证入口、输入与预期观察

依赖顺序为基础语法/目标行为 → source/installed与分发 → 完整candidate Check → 原最终整合及重绑 → 最终Check/独立完整Review。planned 命令不预填 pass。

| ID | 原入口/输入 | 预期结果与范围 |
| --- | --- | --- |
| V692-01/02/03 | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-discover-change-context/tests -p 'test_runtime.py'`；配对运行 `test_contract.py` | 真实record/check/invoke、两种mode、普通错配/内容读取及原base/目标路径按design第8节观察；一致结果成功、错误仍拦截、字段/恢复准确、无内容泄露。依赖缺失记环境阻塞，使用原managed interpreter恢复，不伪报pass。 |
| V692-04 | 原Check/独立Review亲自读取完整当前需求、五个受影响owner、diff和未改consumer；命中的既有 Intake/Author tests定向运行 | 判断语义承接、真实减重差额及兼容；机械断言不代替该判断。不新建专项Agent replay/A-B/native eval或固定数量。 |
| V692-05a | `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`，随后 `--mode installed --json` | 实际registry/interface/commands/error、source/runtime和installed均有效；不以source通过推定installed。 |
| V692-05b | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`；同一Task checkout reapply；`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .` | 原managed机制同步完整preset；声明平台的实际选定投影bytes/mode一致，无未处置 `.new/.bak`。有真实provenance冲突回原升级owner，不扩大安装矩阵。 |
| V692-05c | 命中Python语法、JSON解析、Bash语法、Markdown引用、`task.py validate`、`git diff --check` 与递归sidecar检查 | 当前实际变更可读、上下文有效、无格式/sidecar残留；不增加无关全仓测试。 |
| V692-06 | 原fresh最终Check、独立B..实际H Branch Review、PR readiness及liveGit/GitHub读回 | 真实最终候选覆盖全部义务；满足expected-head/base/可合并门禁后才合并。最终issue/PR/main事实与Completion/Closure/Finish分别核对。 |

实际命令结果只进入第6节指定的 Test contribution；本文件更新必要执行状态与指向，不复制完整日志或另造审核台账。业务现场、外部安装、完整多平台升级/Release保持未验证；本Task不负责增加这些证据。

## 4. 停止条件与适用回退点

- checkout、TaskId/generation、当前D1、scope或binding不一致：停止该写入，回原Identity/Ensure/Bind/Selection/scope owner，保留同一身份和Git资源。
- 新scope/authority/机制义务或原候选不再适用：回最早受影响Clarify/Author/Architecture/qualification，重审真实差额；不因为普通ref前进重跑无关工作。
- 原helper/recorder/validator失败：报告实际code/field/remediation及已发生副作用，沿同操作恢复；不弱化验收、手改receipt/hash、伪造DTO或创建新Task/Delivery。
- 测试/分发失败：先定位真实归因和受影响consumer，保留首错；缺环境不计pass。没有业务数据或外部部署迁移，不创建额外rollback协议。源码恢复只针对本批，保留无关dirty。

## 5. Delivery Policy（唯一）

Policy 为 **full**。D1 覆盖 R692-01..04 全部实现、文档、分发和 AC692-01..05 的正常质量证据。独立交付条件是具体减重合同与诊断行为完成，原子能力和门禁保持，source/dogfood定向验证及fresh Check/完整独立Review/readiness通过，实际同PR合并。

剩余整体责任为 AC692-06：原 Completion 核全部accepted scope、原Closure处理live #692、原Finish归档和bookkeeping、原Cleanup处置精确资源或说明非阻塞。其owner各归原Skill；不要求这些terminal动作先完成才允许D1交付。未取得的历史现场、业务根因与节省时间不是隐藏延期实现；不宣称已验证。

## 6. Docs SSOT Plan（唯一）

Strategy 为 **delta_first**。当前AI在实施阶段按原 `guru-maintain-requirements-design-test-ssot` owner 执行；该owner判断完整性、关系与晋升，原Author不提前写shared current。隔离贡献根为 `docs/requirements-design-test-contributions/692-local-fix-intake/`，包含必要 manifest、完整 requirements/design/test 与traceability、唯一proposed-target定位。实际验证结果唯一由其中 `test.md` 拥有。

拟写完整current单元：`docs/{requirements,design,test}/current/local-fix-intake.md`，分别定义 R692/BEH692、D692/CON692、T692/SC692 稳定关系；三份current导航添加identity/status/locator/关系，不复制摘要。既有 lifecycle 的通用入口、Task/Delivery和恢复定义仍适用；新单元拥有本批具体事实复用与诊断差额，引用原canonical完整接口，不建立第二step-local方法。原JSON载体单元保持；原knowledge-maintenance的#693方法保持且通过必要引用承接。按完整unit读取选择实际必要关系，不遍历无因历史。

独立candidate Architecture和candidate Check先审完整实现及隔离拟写内容；candidate_checked后由原RDT owner读取真实当前目标、合成完整unit及必要导航，执行final_integration并读回。随后implementation重新begin_check绑定全部actual after，最终Architecture/Check、TaskCommit和完整committed Review覆盖真实晋升内容。无全局版本递增、无空contribution、无绕开candidate Check的共享写入。

Architecture当前候选为no-impact，无ADR/贡献；真实实现产生边界变化时回其原owner。canonical Skill合同与runtime拥有实际行为，workflow/README只维护真实路由/定位；dogfood通过原preset生成。历史Task/ADR和原时间线不追写，外部项目安装采用不由本Task替代。
