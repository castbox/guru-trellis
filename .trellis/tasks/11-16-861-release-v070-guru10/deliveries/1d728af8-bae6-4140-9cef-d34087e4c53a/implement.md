# 正式采用与完整 existing 实施计划

## 1. 输入与引用

整体`../../prd.md`、本批`prd.md`及`design.md`全文，唯一来源设计处置在design§3。Task/gen1/current DeliveryKey与root由原public current读取；fixed B=f09afb891cfae105ee808c137301e182804b6092，已交付完整源C=79c25b5eaafdbcf415393535a16a7b1c0d281284，不互换。

实施前完整加载原tools Skill/contract/install输入及private-prepare/current public maintenance协议、原Sync、私有release Stage1/真实采用/独立确认；quality Test And Validation Value/Validation Scope Ownership及#868新责任边界方法。design§9的完整RDT/Architecture必要单元和historical schema边界保留。所有Python显式PYTHONDONTWRITEBYTECODE=1与适用-B；每批Task写前fresh checkout boundary，失败即停。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 原owner/动作与完成观察 |
| --- | --- |
| I1 | Author完成本三正文/official context，经独立candidate/final Architecture、Approval；展示完整计划后停Activation前 |
| I2 | 计划接受并原Activation后，原Sync只对clean primary main fetch/ff-only取得C；不安装primary，不动repairH/Task。实际超C先评差额刷新source绑定 |
| I3 | 从完整C canonical tools launcher只读preview，核目标/Fork/API/事务/用户编辑/peer；按实际inspection形成tools_input，不借旧dispatcher |
| I4 | 原tools prepare一次，完整读取frozen plan，展示全部写删/保留及invoke命令，独立确认后真实安装；新写集仍须原独立确认；已成功原操作不重复 |
| I5 | 原tools/实施owner验证目标自身可用、全部资产、配置/Task/session/peer保持、同operation reapply/drift及零sidecar；有失败原ref恢复 |
| I6 | 新规划接受后先修design§4.4原verifier与直接回归，核全部driver依赖，再执行V4真实`.9→.10 existing`；完整输出通过才满足本批该承诺，不以focused/tools exit替代 |
| I7 | 原RDT/Architecture实际after复核、必要整合/readback；TaskCommit另确认后constructor/begin_check保B，新独立完整Review，readiness/Refs-only Publish/Merge逐项边界 |

本次返工先完成规划；未接受前不实施driver修复或提交。已成功原Sync/tools只消费实际结果，不重复副作用。实际files由I4原plan决定，主要managed根见design§2；新增canonical仅design§4.4的verifier与直接test。出现源缺陷回原Author/Architecture，不在安装中临时补丁。

## 3. 验证入口、输入与预期观察

### V1 来源与一次计划

原Sync public invoke使用operation=sync、base_branch=main，唯一clean注册authority为主目录。它只做Git同步，不做tools安装。取得后要求HEAD==C、canonical干净，实际源与本计划一致；不一致先沿原源差额判断刷新，不用source_ref=C运行新HEAD。TARGET唯一repair路径，SOURCE为经核实的完整C根。正式tools input：

```json
{"profile":"install","source_ref":"79c25b5eaafdbcf415393535a16a7b1c0d281284","dependency_mode":"source_locked","checkout":"/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10-repair"}
```

upstream_source从原transport实际绑定Fork CLI/Core roots、完整Guru/Fork roots和bytes/mode身份；Fork为`/Users/wumengye/Documents/GoProjects/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140`。沿该完整source调用：

```bash
bash "$SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/preview.sh" --root "$TARGET" --input "$TOOLS_INPUT" --upstream-source "$UPSTREAM_SOURCE"
bash "$SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/prepare.sh" --root "$TARGET" --input "$TOOLS_INPUT" --plan "$PRIVATE_PREPARE"
```

JSON载体为原owner临时regular文件；不写Task。PRIVATE_PREPARE的tools_input来自实际public inspection：workflow custom/install、canonical内容与immutable C provider；AGENTS恰一个custom、actual source snapshot、原全文base交renderer；真实config preserve与Guru decisions分别按原owner允许集合。selected platforms来自target，不从source猜。prepare只一次，完整result.plan写本owner临时FROZEN_PLAN并核所有writes/deletions/保留和AGENTS幂等。无Task/session/peer/common写入。展示真实plan后再独立安装确认。

### V2 正式invoke与目标观察

```bash
bash "$SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/invoke.sh" --root "$TARGET" --input "$TOOLS_INPUT" --plan "$FROZEN_PLAN"
```

预期tools_upgraded、installed_version `.10`、unverified无formal_fork_source_lock。读取实际installed extension的source/provenance、current清单及完整受管内容，不用版本号相同推断采用；全部C的#868/#872及11项修复均存在。manifest由原installer产生，source tree_state按真实source status记录，不伪写。

目标自身managed resolver执行installed package validator、`get_context.py --mode continuation`和public Delivery current/Identity/Ensure原入口，核同Task/gen1/本Delivery与Planning仍可接续；不要用source resolver替代。结合原public postvalidation，完整managed_source_projections expected集合/bytes/mode、manifest inventory、workflow/lock/版本、声明三root及无旧Codex public根/私有test泄漏。AGENTS比原renderer结果；配置比preserve后的原bytes，不把所有raw模板当生成结果。

原tools在安装区间冻结并核Task/archive/workspace/session/public facts/user config、peer tools/common pointers保持；只允许目标自身runtime pointer与原recovery写入。这些保存观察仅原consumer短期使用，不进Task ledger。客户端Agent及生产未验证如实保留，不是新增本批验收。

### V3 同操作reapply与drift

采用原tools owner的同frozen public source/plan/recovery_ref、`tools_only=true` reapply路径；不再prepare，不普通full apply绕历史Task guard。消费真实结果，再核目标installed/native、完整asset map/modes、dogfood drift与递归`.new/.bak/.pyc/.pyo/__pycache__`。实际合法owned编辑或sidecar按原owner处理，不手修产物制造pass。无法合法reapply时保具体gap回原owner。

执行入口复用 `trellis/skills/guru-team/packages/guru-upgrade-tools/tests/test_native_install.py` 的真实same-operation调用：同一个tools owner从自己的operation读取actual public `upstream_ref`，保其原值；以FROZEN_PLAN的upstream_source/upstream_plan和selected_platforms调用C原installer的`install_assets`，明确`python=目标resolver实际解释器, checkout_local=True, tools_only=True, tools_maintenance={source:upstream_source,plan:upstream_plan,recovery_ref:actual_upstream_ref}`。source/dst/repo依次为C workflow目录、目标`.trellis/guru-team`、目标root；真实preserve/retirement参数沿同operation原决定保留。观察skill_packages/overlays status和skill_installed_validation.returncode及V2全部保存项。此为原确定性installer执行，不创建新wrapper、复制算法或修改recovery checkpoint。complete后的`resume`仅验证，不能报告成reapply。

原repair dogfood脚本的H canonical→C installed差额保留原失败输出；本采用drift用design§4.4完整C expected map核全部实际目标，不修改H或副本制造同源。Stage2的最终main自身dogfood门禁不被此比较替代。

### V4 完整真实前驱existing

前驱`.9` peeled commit `ac1c823857ad6695c106daeedd25aafce4c50934`，manifest/lock一致为CLI`.6`、Fork e379325。先按design§4.4在repair原canonical verifier修复阶段前像传递及直接test；保init前像、仅tools_upgraded分支用真实维护前像、保原精确hash/renderer和其它维护分支。组件测试观察原coordinator的阶段承接、用户块外保留及未知编辑拒绝，不声称mock外部maintenance是真实writer。

原C shell入口的首次失败、bootstrap/routing/inventory原输出保留。PATH默认解释器不可用时选择实际验证的3.12解释器，不改lock/依赖。逐项核design§4.4命中siblings/loader与C等价，仅verifier/test差额后，用C原managed resolver执行repair原公开完整driver CLI：

```bash
PYTHONDONTWRITEBYTECODE=1 TRELLIS_PYTHON_CMD=python3 PATH="$ORIGINAL_C_SHELL_WORK/source-managed-python-path:$PATH" bash "$SOURCE/trellis/skills/guru-team/runtime/resolve-python.sh" \
  "$SOURCE" "$SOURCE/trellis/skills/guru-team/runtime" -B \
  "$TARGET/trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py" run \
  --repo-root "$SOURCE" --work-root "$WORK/matrix/codex" \
  --workflow-source gh:castbox/guru-trellis/trellis#79c25b5eaafdbcf415393535a16a7b1c0d281284 \
  --fork-source "$FORK" --predecessor-source "$FORK" \
  --predecessor-commit e3793251fad8bd261d0c370d408c7675b9f6a140 \
  --mode existing --platform codex --before-tag v0.7.0-guru.9 --before-cli 0.7.0-castbox.6
```

SOURCE=完整clean primary C，TARGET=repair，FORK=原matching checkout，WORK=新临时验证目录；ORIGINAL_C_SHELL_WORK由原完整C shell的真实输出/工作目录取得，不猜路径。执行前完整读取原bridge，核可执行mode、C resolver/root/runtime字面绑定及实际hash-locked解释器probe；PATH首位和TRELLIS_PYTHON_CMD同时进入driver及子进程。缺失/不符先回原环境owner取得原shell前置，不能手写wrapper或仅用父进程解释器替代。完整stdout保存matrix-existing-codex.json，非零即停。成功后在相同bridge PATH及TRELLIS_PYTHON_CMD环境经同一C resolver执行C的 `verify_upgrade_platform_selection.py aggregate --mode existing --platform codex --result <该原JSON>`，消费完整结果。该原run CLI实际执行整个run_existing：init、前驱preset、原tools source_locked升级、reapply、全部validate_cell及source/Fork前后检查。不mock、不补写producer结果，不以局部validate、focused或tools_upgraded代替。

分别报告C产品资产和repair修复driver，不称C旧driver通过。原shell前置仅在定义、来源、输入、工具环境仍适用时采用，否则补真实缺口。原helper和aggregate均现有入口，不新建wrapper、临时源commit或worktree。完整cell及aggregate均通过才满足本批AC7/9；Stage2在修复合入后从最新main重新执行其完整原门禁。

### V5 质量交付及验证停止

复用前序仍适用source/manifest/native/AGENTS回归及已合入#868/#872的范围内工程事实，不重跑175项历史suite或重复层级。原已有失败记录不改报通过；若实际C的变化影响检查输入，补该真实缺口。目标采用与完整existing是本批新增事实，不能仅采用旧临时样本。证据充分即停可选实验；原必要检查失败必须保留并回原owner，不因成本省略。

I7按原知识/TaskCommit/完整Review/交付链，全部installed after都入固定B..H；不提前新建下一Delivery或写发布状态提交。

## 4. 停止条件与适用回退点

source/root/HEAD/canonical、Fork build/API/lock不符，target/C4/selection、相交未完事务、未知编辑/sidecar、保存项差异或必要验证失败时停在原owner。sourcescope/机制实变回Author/Architecture或Clarify，正常映射/恢复自动接续。

部分操作只用原recovery_ref、原source/plan/preimages恢复，不重prepare、不刷新anchors。rollback需原owner另审当前兼容与精确副作用，不reset/rebase、改Task/history或恢复他人文件。main推进不换fixedB，不要求无影响内容重审；实际冲突经原Reconcile。当前不执行安装或任何收尾。

## 5. Delivery Policy（唯一）

**staged**：当前为source实际delivered后的正式采用切片，覆盖A-R1–6、A6及V1–V5，包含AC7必要verifier修复，不把采用再推给“补证”。进入条件为本批完整Planning/独立candidate和final Architecture/Approval、当前计划接受与原Activation；安装仍有原tools独立精确写集确认。阶段为来源取得→一次tools计划/正式采用→目标和完整existing验证→全部after完整质量交付。退出为真实source_locked/目标可用与保留、完整existing、必要知识及actual delivered均成立。

前序旧installed的局部限制仅在本批实际结果后解除。整个Task剩余责任由原Completion覆盖所有Delivery和AC；reference_only Closure no_mutation、Finish与Stage2各留原owner，不由本批安装或merge推断完成。Stage2最终候选始终最新main重新冻结。本轮修复须先接受新方案并原Activation；已成功原来源/tools不重复。后续commit、Publication和merge仍各有原独立边界。

## 6. Docs SSOT Plan（唯一）

strategy=`no_docs_update_needed`，针对共享RDT/Architecture定义。原R724/R630/current清单合同及ARCH-INT-006/014/015已定义本次采用/保留/来源/验证分层，#868/#872的已交付定义原样采用，不新增公共语义或知识版本。历史gen0和前序正文不追改为当前pass。

原`guru-maintain-requirements-design-test-ssot`在实际after及工程结果后复核真实现行规范/指南差额；如确有变更先回Author刷新本唯一策略，再由原writer完整整合/readback，TaskCommit前完成，同次独立committed Review审before/after。Architecture同理；无差额不造空contribution/ADR/导航。verifier阶段前像修复承接原R9/AC7，不新增shared current定义；实际超出此边界先回原owner。当前public Delivery/Git事实承接进展，不写动态tracked ledger或授权记录。
