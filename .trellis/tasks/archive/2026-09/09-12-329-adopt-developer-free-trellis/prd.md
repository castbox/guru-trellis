# #329 承接无 developer/workspace 的 Trellis 0.6.17

## 目标

将 Guru Team 的框架来源固定到已经退役 developer identity 与旧
`.trellis/workspace/**` journal/index 机制的
`castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`，并让 canonical、
dogfood、installed/runtime、平台入口、文档和验证统一使用 Trellis CLI `0.6.17`
的正式生成与迁移语义。

完成后，Guru Team 的正常 task 生命周期只依赖明确 task metadata、当前 Git checkout /
worktree / branch facts、GitHub caller authority 或显式输入，不再读取、创建、恢复、复制、
迁移、索引或写入全局 developer identity、workspace index 或 journal。

## 已确认事实

- GitHub Issue `castbox/guru-trellis#329` 是本次唯一 primary/close scope。
- `castbox/Trellis#3` 已于 2026-09-12 关闭；PR #4 已合并，merge commit 为
  `3f078854d6c39ca2cf02ee08c1b83b167fa1cfaa`。
- `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc` 包含 PR #4，
  `packages/cli/package.json` 声明 `0.6.17`，root package manager 为 `pnpm@10.32.1`。
- 当前 Guru source lock 仍为
  `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291` / CLI `0.6.16`。
- 当前 worktree 已由 `task.json`、两份 Guru runtime mapping 与 live Git worktree 闭合；
  stock `get_context.py` 仍按旧 developer identity 报告无 current task，属于本 Issue 的直接
  adoption 缺口，不是重复 Intake 的依据。
- 上游 `0.6.17` 保留少量 retired command stub 和历史数据，但其迁移合同明确禁止新 runtime
  消费旧 identity/workspace 数据；这些正式迁移 stub 不应由 Guru 手工删除或重新实现。

## 需求

| ID | 要求 |
| --- | --- |
| R329-01 | canonical source lock、source/installed projection、构建器、验证器和当前文档统一绑定 `castbox/Trellis@a2003296...`、CLI `0.6.17`、`pnpm@10.32.1`；不得使用可变 `main`、原 npm 包、全局 CLI 或其它 ref fallback。 |
| R329-02 | 使用固定 Fork 的正式 build、init、update/migrate 与生成模板替换当前 upstream-managed dogfood 文件；不得把全局包、`node_modules`、wrapper、空 accessor 或手工 patched generated file 作为最终实现。 |
| R329-03 | Guru canonical workflow、preset、skills、hooks、runtime、installer、active fixture 和 current docs 不得把 `.trellis/.developer`、`TRELLIS_DEVELOPER`、`init_developer.py`、`get_developer`、`add_session.py`、`.trellis/workspace/**`、workspace index、journal、journal rotation 或 `--mine` 当作正常路径依赖。 |
| R329-04 | task creator、assignee、owner 和 actor 仅来自显式 task metadata、显式参数或经过仓库访问预检的 Git/GitHub caller authority；无法解析时在写入前要求显式输入，不建立新的全局 identity、环境变量或唯一候选隐式 fallback。 |
| R329-05 | 保留 Guru task checkout/worktree authority：`task.json.worktree_path`、branch/base、live `git worktree list` 和 ignored task/workspace runtime mappings 继续闭合 task identity；文档必须明确它与退役的 journal workspace 机制不同。 |
| R329-06 | 既有 `.trellis/.developer`、`.trellis/workspace/**`、workspace index、journal、`.trellis/agent-traces/**` 及这些路径内的历史文件原字节保留；不迁移、不删除、不重写、不重新索引、不作为恢复或 owner 输入。 |
| R329-07 | 直接演进所有受控消费者并删除失去 supported consumer 的 Guru 旧路径、配置、schema 字段、fixture 和文档；不保留双读、双写、adapter、fallback 或旧 runtime compatibility 分支。上游 `0.6.17` 的正式 retired stub 仅作为迁移提示保留。 |
| R329-08 | current Requirements/Design/Test 与 Architecture authority 必须通过各自 owner 承接 source、identity-free lifecycle、task-worktree 边界与测试合同；task 规划和 contribution 不得冒充 promoted current。 |
| R329-09 | canonical、dogfood、installed/runtime 与 Codex、Claude、Cursor 声明平台投影一致；preset reapply 不留下未处理 `.new` / `.bak`，不静默覆盖用户修改。 |
| R329-10 | 分别报告 source build、生成文件 adoption、Guru focused regression、完整安装/update/reapply/lifecycle matrix 和远端发布状态；任何缺失证据不得被 fixture PASS 掩盖。 |

## 验收标准

- `AC-329-01`：source lock、Guru manifest 的 target/required/tested CLI、installed source record、
  README 与 current Architecture/RDT source binding 在同一 candidate 上指向 `a2003296...` /
  `0.6.17`；固定 Fork 自身 build 后的 source marker 与 HEAD 一致。
- `AC-329-02`：从干净临时仓库执行固定 Fork `init` 后应用 Guru preset；不存在新建的
  `.trellis/.developer` 或 `.trellis/workspace/**`，stock/Guru session bootstrap 能从明确 task/Git
  facts 得到相同 current-task 结论。
- `AC-329-03`：从当前支持 predecessor 执行 existing-project `update --migrate`、workflow
  预览/应用和 preset reapply；Trellis-managed 文件来自 `0.6.17` 正式模板，Guru-owned 文件来自
  canonical preset，未知用户修改被保留且冲突明确，最终无未处理 sidecar。
- `AC-329-04`：Codex、Claude、Cursor 的 linked worktree、new session、resume、task creation、
  planning、implementation、check、commit、branch review、publication、finalization 和 archive
  代表链路均不要求 developer identity、journal、workspace index 或 `--mine`。
- `AC-329-05`：在 legacy 数据 absent、present-A、present-B 三类 fixture 中，同一 task/Git/caller
  authority 产生相同结果；present fixture 的 identity/workspace/index/journal bytes、mode 和文件集合
  前后完全一致。
- `AC-329-06`：task 创建使用明确 creator/assignee；缺失 owner 的 noninteractive 创建在任何
  task/artifact/runtime write 前失败；已有 task 的读取与恢复不要求重复提供身份。
- `AC-329-07`：`task.py list --assignee <name>` 取代 `--mine`；active Guru hooks、skills、commands、
  workflow、installer 和 fixture 不调用 retired identity/session-recording 命令。文本引用范围固定为
  禁止行为断言、历史说明和 upstream retired-stub migration 说明。
- `AC-329-08`：Guru task workspace checker 仍验证 `task.json.worktree_path`、两份 runtime mapping、
  branch/base 与 live worktree；不读取或派生 legacy `.trellis/workspace/**`。
- `AC-329-09`：canonical/installed source validation、ownership、dogfood drift、package/runtime tests、
  三平台投影与完整 Issue matrix 全部通过，并有独立 Phase 2 与 committed full-diff Branch Review。
- `AC-329-10`：本 task 不创建或发布新的 Guru tag/GitHub Release；当前已发布
  `v0.6.16-guru.1` 只作为 predecessor/released fact 保留，后续 release candidate 由独立发布流程
  冻结和验证。

## 非目标

- 不修改 `castbox/Trellis`、原始上游、全局 npm 安装或 `node_modules`。
- 不删除、迁移、清理或规范化用户已有 identity/workspace/index/journal/agent-trace 数据。
- 不移除 Guru 合法的 task checkout/worktree authority 或 ignored runtime mapping。
- 不保留旧 developer/workspace runtime 兼容路径，也不新增替代性的隐藏全局身份存储。
- 不处理恶意输入、故意伪造、TOCTOU、分布式锁、并发压力或额外 fault injection。
- 不在本 task 中 commit、push、创建 PR、merge、tag 或 GitHub Release；这些动作仍按后续独立门禁。

## 风险与延期项

- 上游 `0.6.17` 是固定 Fork commit，不是 npm/tag/Release 发布证明；网络、依赖安装或 build
  失败必须作为 source adoption blocker 报告。
- 当前 active 文本中既有正常路径依赖，也有必要的 negative/preservation 断言；实现不能按字符串
  机械删除，必须按 supported consumer 分类。
- upstream update 会大规模替换 managed templates；必须先保存 legacy bytes 基线，并将
  upstream-generated diff 与 Guru-owned diff 分开审查。
- 新 Guru repository release identity、完整发布 smoke 与真实业务仓库升级留给独立 release owner；
  本 Issue 只证明 source checkout candidate 和要求的安装/lifecycle matrix。

## 开放问题

无。Issue 正文、上游迁移合同和现有版本轴已确定本次产品与兼容边界。
