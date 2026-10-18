# #154 验证与边界

本文件是本轮唯一 Test，供原 Check、Review 和 Completion 消费。下表分开记录正文审查、真实 Agent 行为、确定性检查和安装结果；这些事实不替代主任务正式门禁。

| Test | 验收与方法 | 当前结果 |
| --- | --- | --- |
| T154-01 | AC1/AC2/AC10：source package、原 consumers 引用、上游 ownership、全部声明平台受影响投影与安装资产核对 | source package 与 upstream ownership 通过。新增 `test_planning_body_distribution.py` 经原 preset writer 安装全部22声明平台并 reapply，逐一读取共享正文、四模板和两组嵌套示例，字节一致；项目自有文件保留且无 `.new/.bak`，1项通过。此为模块/分发证据，不证明实际 Agent 加载。 |
| T154-02 | AC1/AC2/AC7/AC9：原 owners 审模板章节/字段/裁剪与详细/简略完整过程示例，核对原来源条件、例外和义务 | Trellis implement 完成写作自检；另一个只读 Trellis check 逐项对照 live #154 和已接受 D1，未发现 I1–I4 正文实现缺陷。审查覆盖四模板、两完整过程示例、来源条件/例外、九profile、原接受边界和同源消费者。20个 Author Markdown 的83个相对链接及锚点可解析。此为正文审查，不是正式 Phase 2 Check 或 V1–V7。 |
| T154-03 | AC3/AC4/AC5/AC6/AC7/AC9：V1 详细技术来源、V2 简略 Issue、V3 无 Issue、V4 多来源冲突、V5 部分及后续 Delivery 的实际 Agent 写作和审核 | V1–V5 的实际写作与原 Planning 审核通过。详细来源保留完整要求并展开设计；简略 Issue #615 和 no_issue 请求均先调查再成文。多来源冲突得到处置，建议/历史角色保持。partial D1 经真实 PR #616 交付，原 Completion 返回 `additional_delivery_required`，原 Creation 建立不同 UUID 的 D2，后续三正文经原链取得 `approved`。已逐份核对生成正文与真实出口，不以 schema/安装代替写作证据。 |
| T154-04 | AC6/AC8：V6 来源更新/草稿/新原生会话恢复，V7 普通遗漏经原审核返回 Author 修订 | V6/V7 通过。新原生会话经 Bind/Selection 恢复同一 Task/gen/D1，实际读取当前模板和必要引用；新增来源经 Clarify/Author 更新整体 scope，仅调整 D1 的关联引用并将新增验收归 D2。后续从 PRD-only 阶段按原 Author 完成方案。V1 中 Clarify 发现重复章节，Wording 发现验证入口/来源指向等具体缺口；实际回 Author 修订并刷新 Wording、final Architecture、Approval。修订保留源语义，没有宿主篡改已接受正文。 |
| T154-05 | AC10：一个代表性完整 matching installed 环境、clean/reapply、用户内容保留、sidecar、dogfood drift | 本 worktree 原 tools-only owner 返回 `tools_upgraded`，local_candidate 的 `formal_fork_source_lock` 限制保留；dogfood drift 通过。一个 Codex throwaway 在真实 marketplace Guru 初始化后采用当前本地候选，完成 CLI update、preset reapply、用户文档保持、零 `.new/.bak` 和实际 source-lock一致检查。既有平台load检查只证明projection_parity；既有session probe是原生绑定的确定性探针，均不冒充V1–V7写作。结果见临时环境 `matrix/codex/current-focused-summary.json`。完整多平台升级与 Release 矩阵不在本轮范围。 |

本轮规划已由原 owners 完成来源到设计的语义审查；此事实不作为 T154-01–05 的实施通过证明。完整 Release 矩阵、其他平台实际行为、软件发布和业务仓库采用尚未验证。

## 已执行的定向命令与首次失败

- `GURU_UPSTREAM_DELIVERY_SCRIPTS=<匹配 CLI .4 的 dist/templates/trellis/scripts> .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-author-task-plan/tests -p 'test_*.py'`：Author 12项通过，18.165秒。首次未设置该环境变量，10项在setUp中失败；补充真实匹配provider后重跑，不将初始化失败计为通过。
- 同一环境变量下，从仓库根执行 `python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_planning_body_distribution.py -v`：1项通过，110.590秒。首次从脚本子目录运行，临时生命周期runtime按cwd查找失败；改用原合同要求的仓库根执行，未修改生产runtime。
- `bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`：passed。`bash trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`：ok。`git diff --check`：通过。
- 普通 `apply.sh --repo .`：被历史归档的 `upstream_delivery_migration_required` 前置拦截。没有把这次失败当作同步成功，也没有迁移或删掉历史任务；由原 tools-only维护owner处理。
- 原 `verify_trellis_compatibility_matrix.py validate-source`：匹配 Fork `7bcbeaad31380e7a29c97898cb947c6120a61775` 与 CLI/Core `.4` 校验通过。该 source事实不是当前候选 clean安装或Agent行为证据。
- 原 focused verifier 仍为失败：它在 local-sample路径显式选旧 `native`，生成schema1 bootstrap后被当前preset前置拒绝。另一次 `native-delivery-v1` 初始化虽可安装，但其manual bootstrap Delivery阻塞Guru切换后的update。两次失败现场保留，未修改生成器或verifier。成功路径用同一代表性临时根、匹配CLI的官方 `init -y --codex --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#855f236850714edc4b78169218c09568c823f336`，随后沿既有local-sample机制采用未发布canonical。它证明当前候选的定向安装/update/reapply，不声称原verifier命令通过或远端exact-candidate已发布。

## 实际 Agent 证据定位

一个 Codex 代表环境沿正常 installed owners 执行。共享正文与四模板在 flow、detailed、brief 三个 linked checkout 中均与本轮 canonical 字节一致；实际读取及写作仍以原生 trace 和正文为证据，不由该一致性检查代替。

- V3/V4：`/private/tmp/guru154-planning-validation/native-flow/resume-dist-trace.jsonl`、同目录 `resume-dist-final.md`；原生线程 `01a14dbd-10cd-74d1-b543-91bc9c96834d`，Task `154-validation-flow`，D1 `8be0fd96-f68a-47fd-aad5-789391cbb01c`。正文在该验证根的 `worktrees/flow/.trellis/tasks/10-18-154-validation-flow/`。
- V1/V7：`/private/tmp/guru154-planning-validation/native-detailed/trace.jsonl`；原生线程 `01a14dbe-283a-7b73-97bd-8da74864eb57`，D1 `399b6ea2-f32d-4e9c-919a-78db274de652`。正文在该验证根的 `worktrees/detailed/.trellis/tasks/10-18-154-validation-detailed/`。
- V2：真实简略来源为隔离 [Issue #615](https://github.com/castbox/guru-trellis/issues/615)；原 CreateIssue 返回 created 后重新经过完整 Intake，不直接跳到 Task。轨迹为该验证根 `native-brief/resume-fixture-trace.jsonl`，D1 `1b80b883-00a0-465a-904f-c265bcc53029`，正文在 `worktrees/brief/.trellis/tasks/10-18-154-validation-brief/`。此前 #331 的 advisory 分类调用未取得正式 Wording exit，不计 V2 通过。
- V6：该验证根 `native-flow-new-session/trace.jsonl` 的实际 `thread.started` 为 `01a14dda-936b-7ae3-a348-f6a6326ce9ce`；这是普通新 exec，不将 native resume 误称新会话。既有 TaskId/generation/D1 保留；原来源更新、D1 交付、Completion 分流和 D2 Planning 均已实际完成。

原 Architecture 首轮曾因 fresh reviewer 自己的原生会话未绑定而返回 `stale_identity/delivery_key`；其原 Bind/Selection 恢复后重新独立判断，失败调用未计通过。原生日志保留于本机，不复制进公共 package 或作为第二份范围 authority。

当前 marketplace index JSON、新分发用例编译及官方 `task.py validate` 均通过。两份官方 context 各11条；clear-writing/quality全文超过自动注入字节上限会产生警告，因此各执行者仍按原合同实际完整读取必要正文，不将自动注入等同于完整读取。

V5 的真实前序为 [验证 PR #616](https://github.com/castbox/guru-trellis/pull/616)：reviewed head `b77abeda29a843f44e1f07d1b582519593e216f4`，merge `45b95c15ca90831a6d4ccac815925cc3030b3967`，target `codex/154-validation-base`。原 Merge 已写公共 delivered 并释放所选 D1；不是宿主补造前序事实。D1 四项 fixture CLI 测试通过，远端 checks 为空，不声称 CI 通过。该 PR 不合 main、不关闭外部 Issue，也不证明 #154 主实现已交付。

V5/V6 后续 D2 为 `0acc4592-3d58-463c-a7f1-d3fe542357bf`，planning_root 为同 UUID 的独立目录。它沿原 `content_base` 消费真实 D1 reviewed head `b77abeda29a843f44e1f07d1b582519593e216f4` 作为 B2，没有采用 target merge commit 或重复 D1 增量。原 final Architecture 返回 `baseline_current/no_architecture_impact`，原 Approval 返回 `approved`；完整轨迹和最终输出为上述 `native-flow-new-session/trace.jsonl`、`final.md`。D1 的 Policy、已交付事实和原 planning_root 保留，D2 的 partial Policy 明确当前 dry-run、集成回归及整体 Completion 责任。

这些实验只证明本轮要求的 Planning/读取/审核行为。D2、brief 和 detailed 的 fixture 功能未被当作完成，D2 未 Activation，实验 Task 及来源资源保留供核查。主任务的实现与全量交付另由其正式 Check、Review、Delivery 和 Completion 判断。原生调用中的参数、identity/receipt 缺失均由原 owner fresh 重入处理；失败未计通过，未修改 runtime 来取得结果。

主会话在修改前已成功读取三份指定官方 Trellis 文档；原始成功输出可由本会话记录核查。后续 native 对同三 URL 的 HTTP 403 仍是各次真实失败，不倒写为成功，也不据此推断官方行为。
