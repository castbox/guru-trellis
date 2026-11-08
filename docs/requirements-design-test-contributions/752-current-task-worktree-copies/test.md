# Current-schema Task copies：实际验证观察

本文件是本批执行观察的唯一正文。测试策略由 [完整 proposed Test](./proposed/docs/test/current/native-compatibility.md) T752-01..05，双向关系由 [traceability](./traceability.md) 定位。当前观察截止为本批 source build、定向回归、dogfood工具采用，以及正式目标pair的多workspace完整安装、同计划恢复和rollback完成后、候选Check与知识晋升前。工程事实采用原执行owner实际输出；本writer读回精确source lock、Fork clean status/build marker及V3下述实际JSON与fixture driver，不将工程结果当正式质量或Task Completion。

## 已核实来源与构建

本 writer 通过 live GitHub 查询读取完整 Issue #752、[PR #66](https://github.com/castbox/Trellis/pull/66) 和 [main CI 42440325190](https://github.com/castbox/Trellis/actions/runs/42440325190)。PR 状态为 MERGED，merge commit为 `b4f1665143bd4ecf3a290d426ad62293fc13ea42`；该 main CI 的 headSha 相同、status=completed、conclusion=success。canonical lock 的 parents为 `d9ffdf526988cad7b34da38d280fcbf893e77305` / `501e7137e6d19c1eaa5793fa8887cb5702d228d6`，tree为 `9ba2f6c8a32f63fe9a6ca36ccc90f12b50d9cb67`，CLI/Core仍为 `0.7.0-castbox.6`。

主会话从该 merge 建立干净 Fork worktree `/private/tmp/guru752-fork-b4f16651`，运行 `pnpm install --frozen-lockfile && pnpm build`，exit 0；build成功后将实际HEAD写入 `packages/cli/dist/.guru-source-commit`。本 writer读回marker为上述merge且Git status为空。原 `validate_fork_source` 返回lock匹配、template_count=212、ci_run_id=42440325190。来源、CI及本地build分别提供其覆盖层事实，不能自行证明目标安装或Task Completion。

## 定向回归与dogfood观察

| 策略 / 验收 | 命令、观察与有效边界 |
| --- | --- |
| T752-01 / AC1–AC3 | 在上述精确干净 Fork source运行 `pnpm --filter @mindfoldhq/trellis exec vitest run test/commands/migrate2.integration.test.ts`，168/168通过，49.03秒；包含current-peer public schema/executor集成。Core `pnpm --filter @mindfoldhq/trellis-core exec vitest run test/task/migration-v2.test.ts` 为9/9，161ms。该结果是公共迁移层证据，不替代Guru完整安装。 |
| T752-02 / AC1–AC4 | 实施 owner设置真实successor merge build CLI及匹配legacy3 CLI后运行 `test_delivery_upgrade.py`：首批全文件22项通过，77.914秒；随后新增的 `test_current_peer_business_content_mismatch_reaches_core_and_blocks_zero_write` 单项通过，4.386秒。当前文件23项的上述执行均无skip；这里不是声称修订后的23项又整套重跑。新增current-peer路径覆盖preview零写入、实际Core迁移、peer raw/modes和Task/session保留、同plan恢复/rollback及private conversion拒绝。 |
| T752-02 的组件边界 | 测试确实进入真实 CLI/Core Plan2；source/installer 依赖采用既有mock隔离。该结果只证明Guru原Upgrade协调与Core集成；完整preset及target own installed validation由下述T752-03实际验证。 |
| T752-04 / dogfood工具采用 | 原guru-upgrade-tools返回真实 `tools_upgraded`、installed `0.7.0-guru.8`；该次为 `local_candidate`，仍报告 `formal_fork_source_lock` 未验证。3082项Task/common文件原bytes/modes保留，原owner核peer/common pointers不变；主会话current Task/Delivery仍匹配implementing。该结果不冒充正式source_locked采用。 |
| T752-04 / 投影与源码检查 | 主会话实际source package入口 `trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json` 为passed，`check-upstream-ownership --repo . --json` 为ok。dogfood drift/ownership、Claude/Codex/Cursor投影、native与source-installed检查均exit0，递归sidecar为0。质量worker完成384个Python文件内存语法、JSON/AST、固定B..H diff check、Bash/index/projection一致检查，均通过；这些工程检查不提供正式Check语义结论。 |

## 正式目标pair的多workspace安装、恢复与回滚

原 Upgrade owner使用已提交且可远端定位的干净 Guru `51b3f36a53f6c10bf4fc3f99fbc5ab3645f2a487` 与上述精确干净Fork merge build，按原完整source-loaded `preview.sh` / `invoke.sh` 执行 `source_locked`。真实样本有两个registered roots、四个current Task rows、两个identity groups；每组一个`current` authority和一个`defer/source_task_schema=2.0` peer。原binding/live checkout决定各组唯一authority，完整inventory不裁剪；原私有迁移调用列表为空，未为peer生成调用。

- preview通过、conflicts为空，实际前后快照一致，确认写前零变更。原begin冻结30768个anchors。
- 完整preset执行后，正式stdout为 `upgraded / installed_version=0.7.0-guru.8 / unverified=[]`。两个roots各自通过其own resolver调用实际 `runtime.validate --mode installed`，均为passed、errors=[]。
- 两个roots的实际 `get_context.py` 与 `delivery.py current` 指向同一业务DeliveryKey，`taskWorkspaceRoot` 均为原唯一authority `business-guru`。22项相关Task、planning、session及binding原bytes/modes保留；业务meta保持，未新增Task/Delivery/migration或private conversion，sidecars为0。
- 原公开 `delivery_resume` 消费同冻结plan，返回相同upgraded DTO及相同recovery_ref，30768个anchors不变；这证明同计划completed重入，没有换包或重新冻结。
- 原公开rollback返回 `rolled_back / installed_version=0.7.0-guru.8`。原owner比较两roots和common/local session/binding的全部10217个regular files，原bytes/modes快照精确恢复，消费的原backup退休。两个roots回滚后own installed validator仍passed；各自context/delivery query仍定位原业务authority与同一Task/Delivery，extension source commit回到 `2ab135ed2d3908966785bb23ad42ada0790f0c81`。

证据位于 `/private/tmp/guru752-installed-v3/`：`plan.json`、`preview.json`、`apply.json`、`resume.json`、`rollback.json`、`primary-installed.json`、`peer-installed.json`、`primary-context.json`、`peer-context.json`，以及 `rollback-0-` 和 `rollback-1-` 开头的 installed/context/delivery JSON。本writer实际读回这些结果及无mock的外部 `run.py`；`before.json` 是原raw/mode临时快照，前后比较由原owner执行。这些临时执行定位不构成新的workflow authority或完成账本。

初始Guru完整preset来自 `2ab135ed2d3908966785bb23ad42ada0790f0c81`（Guru .8、lock为ca0），但初始CLI init/public Core已使用b4 successor/.6。因此本样本证明正式目标 `51b3f36/b4f16651` 完整matching source_locked处理合法current records及真实preset/installed/resume/rollback，不声明验证了旧 `2ab/ca0` matching pair或ca0发行包替换。它也不是完整predecessor Release矩阵。

## 首失败与归因

Fork集成首轮误用路径 `test/migrate2.integration.test.ts`，因无该测试而exit 1。改用真实 `test/commands/migrate2.integration.test.ts` 后取得上述168/168。首轮未到达产品行为，不作为缺陷比较或产品测试失败。

V3首次fixture使用native workflow的manual bootstrap，与Guru现有PR-only合同不兼容；完整preflight在写前拒绝，原数据未动。原owner改用固定Guru workflow建立新的合法样本，再取得上述结果。该首失败属于fixture不适用，没有为使fixture通过修改生产逻辑、放宽profile或修补原Task数据。本观察截止没有其它已确认的本批产品测试失败；SKIP或设施错误不能记为通过。

## 尚待正式质量链与边界

T752-05的完整候选Architecture/Check、原owner实际晋升、actual-after重绑、最终Check与独立committed Review仍由各原owner/public结果证明，不要求本文件追写自身最终pass或HEAD。上述结果分别证明source、组件、dogfood与代表性正式目标pair的实际行为；不能仅凭数量宣称整体Task Completion。

既有 #630/#687 Test 的环境、旧失败与截止保持原样。本批未验证完整多平台 Release矩阵、远端immutable marketplace安装、旧ca0发行包替换、Guru tag/npm发布、真实业务仓升级或实际Agent会话。

## 来源说明修订的补充观察

完整候选检查发现，原三份README与public-docs仍将Guru `.8` 写为未发布准备版本。原实现owner在既有finding路由内修订该来源说明；Task范围、公共接口、current-peer机制、extension `0.7.0-guru.8` 和本批非发布边界保持。本writer现场执行 `gh release view v0.7.0-guru.8 --repo castbox/guru-trellis --json tagName,publishedAt,isDraft,isPrerelease,url`，确认[真实Release](https://github.com/castbox/guru-trellis/releases/tag/v0.7.0-guru.8)于 `2026-11-06T14:47:03Z` 发布，isDraft=false、isPrerelease=false。`git ls-remote --tags origin 'v0.7.0-guru.8*'` 返回annotated tag `3b45f7866581215e8a865bce8e74f06f880930f0`，peeled commit为 `2ab135ed2d3908966785bb23ad42ada0790f0c81`。`git show 2ab135ed2d3908966785bb23ad42ada0790f0c81:trellis/presets/guru-team/source/trellis-source.json` 确认该tag自身固定Fork `ca0e8b931d19ccb87802d6866abd2113a6f707c0`。

修订后的README/public-docs分别说明已发布 `.8 / 2ab / ca0` 与尚未新建Release的current-peer修复源码 `b4` 配对；稳定安装读取tag自身lock，试用修复固定真实完整Guru SHA及其lock。本次不重发已有tag、Release或同版本npm包，未来Release仍归独立owner。上文V3继续只表示 `51b3f36a53f6c10bf4fc3f99fbc5ab3645f2a487 / b4f1665143bd4ecf3a290d426ad62293fc13ea42` 的原执行及其截止，没有将本次文档修订后的source重标为重新执行。原三平台CI也只覆盖H=`51b3f36a53f6c10bf4fc3f99fbc5ab3645f2a487`，不证明本次dirty文档修订已运行CI；后续正式质量仍由原owner覆盖实际候选。
