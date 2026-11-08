# Current-schema Task copies：实际验证观察

本文件是本批执行观察的唯一正文。测试策略由 [完整 proposed Test](./proposed/docs/test/current/native-compatibility.md) T752-01..05，双向关系由 [traceability](./traceability.md) 定位。当前观察截止为本批 source build、Fork 集成与 Guru 组件回归完成后、正式 source_locked 多 worktree 安装执行前。下列工程结果采用主会话及实施 owner 的本批实际命令输出；本 writer 另读回精确 source lock、Fork HEAD/clean status 与 build marker，不重复执行仍适用的验证。

## 已核实来源与构建

本 writer 通过 live GitHub 查询读取完整 Issue #752、[PR #66](https://github.com/castbox/Trellis/pull/66) 和 [main CI 42440325190](https://github.com/castbox/Trellis/actions/runs/42440325190)。PR 状态为 MERGED，merge commit为 `b4f1665143bd4ecf3a290d426ad62293fc13ea42`；该 main CI 的 headSha 相同、status=completed、conclusion=success。canonical lock 的 parents为 `d9ffdf526988cad7b34da38d280fcbf893e77305` / `501e7137e6d19c1eaa5793fa8887cb5702d228d6`，tree为 `9ba2f6c8a32f63fe9a6ca36ccc90f12b50d9cb67`，CLI/Core仍为 `0.7.0-castbox.6`。

主会话从该 merge 建立干净 Fork worktree `/private/tmp/guru752-fork-b4f16651`，运行 `pnpm install --frozen-lockfile && pnpm build`，exit 0；build成功后将实际HEAD写入 `packages/cli/dist/.guru-source-commit`。本 writer读回marker为上述merge且Git status为空。原 `validate_fork_source` 返回lock匹配、template_count=212、ci_run_id=42440325190。来源、CI及本地build不证明目标安装、恢复/回滚或Task Completion。

## 实际回归观察

| 策略 / 验收 | 命令、观察与有效边界 |
| --- | --- |
| T752-01 / AC1–AC3 | 在上述精确干净 Fork source运行 `pnpm --filter @mindfoldhq/trellis exec vitest run test/commands/migrate2.integration.test.ts`，168/168通过，49.03秒；包含current-peer public schema/executor集成。该结果是公共迁移层证据，不替代Guru完整安装。 |
| T752-02 / AC1–AC4 | 实施 owner设置真实successor merge build CLI及匹配legacy3 CLI后运行 `test_delivery_upgrade.py`：首批全文件22项通过，77.914秒；随后新增的 `test_current_peer_business_content_mismatch_reaches_core_and_blocks_zero_write` 单项通过，4.386秒。当前文件23项的上述执行均无skip；这里不是声称修订后的23项又整套重跑。新增current-peer路径覆盖preview零写入、实际Core迁移、peer raw/modes和Task/session保留、同plan恢复/rollback及private conversion拒绝。 |
| T752-02 的组件边界 | 测试确实进入真实 CLI/Core Plan2；source/installer 依赖采用既有mock隔离。该结果只证明Guru原Upgrade协调与Core集成，不能声明完整preset或target own installed validation通过。T752-03仍需真实完整安装。 |

## 首失败与归因

Fork集成首轮误用路径 `test/migrate2.integration.test.ts`，因无该测试而exit 1。改用真实 `test/commands/migrate2.integration.test.ts` 后取得上述168/168。首轮未到达产品行为，不作为缺陷比较或产品测试失败。本观察截止没有可记录的其它本批产品测试失败；后续实际失败仍保留原观察，不能把SKIP或设施错误记为通过。

## 尚待本批实际执行与边界

T752-03的完整匹配clean committed Guru/Fork `source_locked` 代表性多workspace安装、target own installed runtime、同计划恢复与rollback尚未执行。T752-04的dogfood工具更新、source/installed package、ownership、drift/sidecar/mode和其余命中回归仍待实际结果；已有source lock/build事实只覆盖该策略的来源部分。

T752-05的完整候选质量、原owner晋升、actual-after重绑及最终质量结果由各原owner/public结果证明，不要求本文件追写自身最终pass或HEAD。既有 #630/#687 Test 的环境、旧失败与截止保持原样。本批不验证完整多平台 Release 矩阵、远端immutable marketplace、Guru tag/npm发布、真实业务仓升级或实际Agent会话。目前证据不能据此声明AC1–AC5整体完成。
