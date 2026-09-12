# #329 Developer-free Trellis adoption Requirements contribution

状态：`reviewed_candidate`；expected current：`current-main-0.6.5-guru.48`；candidate
successor：`current-main-0.6.5-guru.49`。本 contribution 仅属于 #329 task，在 serialized
promotion 前不修改或代表 shared current authority。

- `R329-01`：framework source 必须固定为
  `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`，CLI 必须为 `0.6.17`，
  package manager 必须为 `pnpm@10.32.1`；build、generation、source marker、installed
  record 和 current docs 使用同一 immutable source identity。
- `R329-02`：Trellis-owned managed files 必须来自固定 Fork checkout 的正式 build、init、
  update/migrate 和模板生成结果；不得以全局 CLI、npm fallback、`node_modules` patch、wrapper
  或手工 generated-file patch 承载 adoption。
- `R329-03`：Guru canonical、dogfood、installed/runtime、平台入口、installer、fixture 和 current
  docs 的正常生命周期不得读取、创建、恢复、复制、迁移、索引或写入 developer identity、旧
  `.trellis/workspace/**` journal/index、agent trace、session recording 或 `--mine` 路径。
- `R329-04`：creator、assignee、owner 和 actor 仅来自显式 task metadata、显式输入或通过 repository
  access preflight 的 authenticated GitHub caller；无法解析时必须在任何 write 前停止并要求输入。
- `R329-05`：Guru task checkout/worktree authority 继续由 `task.json.worktree_path`、branch/base、live
  Git worktree facts 与 ignored task/workspace mappings 共同验证；该 authority 不读取旧 journal workspace。
- `R329-06`：既有 identity/workspace/index/journal/agent-trace 数据保持 path、mode 和 bytes 不变，
  不作为 current task、owner、recovery 或 migration 输入。
- `R329-07`：所有受控 consumer 直接迁移到 developer-free contract；失去 supported consumer 的 Guru
  旧 entry、schema/config field、fixture、test 和 current docs 同 task 退出，不保留 adapter、fallback、
  dual-read 或 dual-write。上游正式 retired command stub 仅保留迁移提示职责。
- `R329-08`：Requirements/Design/Test 与 Architecture 通过 task-isolated contribution 和 serialized
  promotion 承接 source、identity-free lifecycle、task-worktree boundary 与 verification contract。
- `R329-09`：Codex、Claude、Cursor 的 canonical/installed 投影以及 clean install、existing update、
  reapply、linked worktree、session resume 和完整 task lifecycle 使用同一 candidate，且无 unresolved
  `.new`、`.bak` 或其它 sidecar；未发布 candidate 的 local workflow sample 必须显式标记本地边界，
  不得冒充远端 marketplace publication proof。
- `R329-10`：验证结果按 source build、generated adoption、Guru focused tests、installed matrix 与
  remote/release boundary 分层报告；installed closeout 必须从排除 legacy/runtime/task/backup 的 clean
  candidate Git source reapply，capability comparison 必须 subtraction-first，纯新增受支持能力不得被误报为
  regression；本 task 不创建新的 Guru tag 或 GitHub Release。

`BEH-018`：在相同 task/Git/caller authority 下，legacy 数据 absent、present-A 与 present-B 的
developer-free lifecycle 结果相同；present fixture 的 path、mode 与 bytes 在 update/reapply 前后不变。

以上 candidate 不处理恶意伪造、TOCTOU、锁、并发压力、分布式协调或额外 fault injection。
