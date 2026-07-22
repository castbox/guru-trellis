# #145 Branch Review：001-final

## 审查身份

- 审查角色：独立 Branch Review / 最终放行审查代理；发现 finding 后自动成为 finding owner。
- AI process identity：`/root/issue145_final_review`。
- 审查方式：重新读取需求、规划、Docs SSOT、完整分支 diff、Phase 2 / commit-plan evidence，并独立执行静态、行为、安装与升级路径验证；未把 Phase 2 `pass` 或 validator 返回值当作本轮语义结论。
- 结论：**阻断**。存在 1 个 P1 finding，当前 HEAD 不可进入 review gate pass、finish-work 或 PR readiness。

## 范围、HEAD 与 diff

- Task：`.trellis/tasks/07-21-145-stage0-minimal-handoff`。
- Branch：`feat/145-stage0-minimal-handoff`。
- Base：`origin/main`，`096d1889a511969d5ff09ef4d198ac2825110148`。
- Reviewed HEAD：`72326953e4df36a91201f10f581361b045e8c6f0`。
- Diff range：`origin/main...HEAD`。
- Diff 规模：1256 paths，94225 additions，2011 deletions。
- `task-commit-plans/001.json` 的 1256 个 committed paths 与实际 diff 路径集合一致；Phase 2 的 1254 个 reviewed paths 加上其后生成的 `phase2-check.json`、`task-commit-plans/001.json`，覆盖当前 committed diff。
- 审查期间未运行 `review-branch.sh`、`check-review-gate.sh`、任何 `record-*` 命令，也未修改实现或 Docs。

## 需求与 Issue

- Primary / close issue 仅为 `castbox/guru-trellis#145`。
- #144 与 #147 仅作为 closed authority refs；两项 accepted-current proposal 与已发布的 #145 authority comment 均由 `issue-scope-ledger.json` 绑定。
- #146 是 follow-up；`guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三包保持 `1.2+legacy`，不由本任务关闭。
- #98、#127、#132 仅为 related issues，不应由本任务关闭。
- PRD R6（`prd.md:138-147`）明确要求 preset 在一次 transaction 中安装完整六包 graph、registry、manifest、schemas、wrappers 与平台副本，禁止 mixed 1.2/1.3 graph。
- AC7（`prd.md:246-247`）明确要求 pre-#145 upgrade、atomic activation / adapter、reapply 与 `.new/.bak` 路径均不产生 mixed-contract graph。
- Design 8.2（`design.md:194-200`）明确采用临时 staging root，并要求 installed validation 失败时保留既有安装；该要求限定于正常 installer path，不涉及 crash consistency、锁、TOCTOU、恶意伪造或跨 OS 原子性。

## Docs SSOT

- 已核对 `.trellis/spec/workflow/skill-package-contract.md`、`data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md`、workflow index、preset installer / overlay / upstream-ownership specs、三份公共 README 和三份 requirements docs。
- 六包 / 24 exits 的 `1.3+minimal_handoff` current 状态、三包 `1.2+legacy` 的 #146 边界、optional `base_branch` fallback、production eval adapter 行为在当前 Docs 中总体一致。
- `trellis/presets/guru-team/README.md:229-232` 明确宣称 preset 使用一次 staging transaction 并对 mixed graph fail closed；实现未兑现该 current-scope 文档合同，详见 F-001。
- 文档中“九包 legacy”表述均限定为 #144 历史状态，未发现 current-state 冲突。

## 实现与契约

- 六个 Stage 0 packages 均已切换到 Interface 1.3 / `minimal_handoff`，migration manifest 精确登记 6 Skills、24 exits；planning/check/commit 三包继续 legacy。
- 六包 canonical interface、public inputs、per-exit outputs、consumer inputs、projections、examples、wrappers 与 eval corpus 已逐项核对；24 exits 的 corpus 分布为 3/3/6/3/5/4。
- `guru-sync-base` 的 optional `--base-branch` 仍调用 formal `resolve_base_selection`，保留用户要求的 fallback。
- semantic wrapper 从 checker-passed owner result 获取 actual exit；schema selection 先基于 actual exit，`expected_exit` 仅作事后断言。
- canonical、installed、shared、Codex、Claude、Cursor 六包 package tree parity 为 30/30；manifest/schema installed parity 通过。
- Preset activation 实现不符合 planning 与 Docs SSOT，详见 F-001。

## 测试与验证

本轮独立审查执行或复核了以下验证：

- source package validator：通过。
- installed package validator：通过；1284 managed files，0 sidecar / conflict / removal。
- dogfood overlay drift：通过。
- canonical 到 installed/shared/Codex/Claude/Cursor package parity：30/30 通过。
- migration manifest / schema installed parity：通过。
- changed JSON 全量解析：通过。
- `git diff --check origin/main...HEAD`：通过。
- `Stage0MigrationManifestTests` 与 `Stage0PublicInvocationTests`：19 tests，OK。
- focused eval corpus exit 计数：3/3/6/3/5/4，共 24 exits。
- secret-shaped diff scan：无命中。
- 额外执行真实 upgrade-conflict 复现：以 `git archive origin/main` 作为 pre-#145 source，在临时 repo 完成 `--all-platforms` 安装；对一个受管 Stage 0 `SKILL.md` 做正常本地编辑后，使用 reviewed HEAD 的 preset reapply。pre-#145 apply 为 `status=ok`；当前 apply 返回 2、`skill_packages.status=conflict`、installed validator 返回 2，但 registry 已变成 1.3，冲突文件仍保留旧内容并产生 `.new`，extension manifest 也已重写。

现有测试覆盖 source / installed mixed-graph rejection、known managed update/reapply、unknown edit sidecar 与最终 sidecar scan，但未覆盖“任一受管 Stage 0 文件冲突时，升级前完整 graph 原样保留”的 transaction / rollback 行为。Validator 在写入后拒绝 mixed graph 不能替代 activation transaction。

## 开箱即用与 upgrade/update

- Clean current-source install、installed validation、dogfood parity 和 update/reapply 正常路径已有通过证据。
- Default / selected platform copies、mode 与 managed inventory 在无冲突路径中一致。
- Exact remote feature-branch marketplace 安装在分支发布前不可验证；默认 guard fail closed，属于 publish gate 前的已披露限制。
- **Upgrade / update 抗漂移 gate 未通过**：正常 `unknown_local_edit` 冲突路径会在失败返回前改写其它 Stage 0 managed files、registry、platform copies 与 extension manifest，不能保留原完整安装，违反 R6 / AC7 / design 8.2。

## 部署与安全

- Diff 未修改 GitHub Actions、容器、K8s、Helm、数据库 migration 或 Makefile；无生产数据写入、配置迁移或部署动作。
- secret-shaped diff scan 无命中；未在报告中记录 token、credential、签名 URL、`.env`、客户数据或原始 provider payload。
- Claude authenticated live probe 在首 trace 前 45 秒超时且无残留进程；fake-native protocol tests 已覆盖协议。该限制不改变 F-001，也不单独构成 finding。

## Findings

### F-001 [P1] Preset 在冲突前直接激活部分新 graph，失败后留下 mixed 1.2/1.3 安装

- Severity：P1。
- 位置：
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:480-550`
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:679-835`
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:1335-1377`
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:1483-1487`
- 需求证据：PRD R6 / AC7 要求一次 transaction 且任何 `.new/.bak` upgrade conflict 不产生 mixed graph；design 8.2 要求临时 staging root、一次 apply、installed validation 失败保留既有安装；implement RP4 要求冲突时保留原完整安装。
- 实现证据：`copy_skill_managed()` 直接写 target；known upgrade 先写 `.bak` 再覆盖 target，unknown edit 只为该文件写 `.new`。`install_skill_packages()` 的 `desired_files` 循环继续逐项写入并仅累计 conflicts；`install_assets()` 随后仍安装 overlays、更新配置/ignore、写 `extension.json`，最后才运行 installed validator。`main()` 只在全部写入完成后因 conflict / validator failure 返回 2，没有 staging activation 或 rollback。
- 行为证据：真实 pre-#145 upgrade 复现中，单个 `.trellis/guru-team/skills/packages/guru-sync-base/SKILL.md` 的正常本地编辑触发 `unknown_local_edit`；apply 返回 2，但 installed registry 的 `guru-create-task-workspace` 与 `guru-sync-base` 已是 `guru-team-skill-interface-1.3 + minimal_handoff`，冲突文件仍为旧内容并保留本地 marker，`.new` 存在，extension manifest 已重写，installed validator 返回 2。即 validator 能发现坏状态，但磁盘上已经留下可被后续入口读取的 mixed graph。
- 影响：这是 #145 核心 activation invariant 的正常受支持路径失效。用户在常见 upgrade conflict 后得到非零返回，却没有得到需求承诺的“原完整 1.2 graph”；不同入口可能读取已更新 registry / extension 与未更新 package / platform copy，导致 public contract、wrapper、consumer 与 runtime 版本不一致。仅处理 `.new` 后重放无法消除失败窗口中已落盘的 mixed graph。
- 测试缺口：`test_apply_guru_team_trellis_preset.py` 未建立 pre-#145 complete install fixture，也未断言单文件 conflict 后所有原 graph bytes / inventory / manifest 保持不变；现有 installed validator rejection 只证明能在事后发现混合状态。
- 建议修复：按 design 8.2 在 repo 外或 repo-local 非激活 staging root 组装并验证完整 managed output；确认所有 managed paths 可无冲突激活后，再作为一个 activation unit 替换六包、registry、manifest、schemas、wrappers、extension 和 selected-platform copies。若任一 unknown edit / sidecar / installed validation 失败，保留升级前完整 graph，仅输出冲突证据。补充真实 `origin/main` 或等价冻结 pre-#145 fixture 的 success、unknown-edit conflict、known-upgrade、reapply 测试，并断言失败路径的所有原 graph bytes、version selections 与 manifest inventory 不变。若客观证明 transaction 不可行，则必须按已批准设计启用显式 versioned public DTO adapter 及 removal test，不能继续依赖事后 validator。
- 处理状态：open；finding owner 为 `/root/issue145_final_review`。修复后必须对新的 reviewed HEAD 重新执行完整 Branch Review。

## 观察项

- Worktree 存在 ignored `__pycache__/*.pyc`；不在 tracked diff 中，未纳入 finding，也未清理。
- Claude authenticated live probe 的 45 秒首 trace limitation 已在 Phase 2 披露；fake-native coverage 通过。发布前如环境恢复，可补真实 probe，但不得用其替代 contract tests。
- Exact remote feature-branch marketplace install 需在分支可远程获取后由 publish gate 验证；当前 local current-source clean install 证据不能冒充该远程证据。

## 后续候选

- #146 继续拥有 planning / Phase 2 / task commit 三包的 minimal handoff 迁移，不并入本 finding 修复。
- F-001 的修复范围应严格限于 #145 已批准的 preset transaction / versioned adapter 边界；不要扩张到 crash consistency、锁、并发压力、恶意 artifact 篡改或跨 OS 原子性。
- 修复后应新增 upgrade transaction negative tests，并重新执行 source/installed validators、完整 throwaway install、pre-#145 upgrade、update/reapply、dogfood drift、package parity 与 Branch Review。

## 结论

- Findings：P0=0，P1=1，P2=0，P3=0。
- Branch Review：**blocked**。
- `Closes #145`：当前不得发布；AC7 与原子 activation 尚未满足。
- 允许的下一步：finding owner 修复 F-001、更新必要测试与 Docs（若语义变化），重新完成 Phase 2 / task commit evidence，再由独立 reviewer 对新 HEAD 进行完整 diff review。
