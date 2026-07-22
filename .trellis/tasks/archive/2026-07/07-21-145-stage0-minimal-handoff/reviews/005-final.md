# #145 Branch Review Round 5：最终放行审查

## 审查身份与范围

- Technical agent id：`/root/issue145_final_release_r2`。
- 角色：新的独立 `最终放行审查代理`；未参与 Round 1-4 的 finding 发现、实现或闭环，也未运行任何 Branch Review recorder / gate script。
- Base：`origin/main@096d1889a511969d5ff09ef4d198ac2825110148`；merge-base 与该 base HEAD 一致。
- Reviewed HEAD：`9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`。
- 完整审查范围：`origin/main...9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`，1258 paths，108750 additions，2025 deletions。
- 本轮重新读取 live GitHub authority、三份规划、issue ledger、完整三提交 diff、四轮原始报告、fresh Phase 2、commit plans、Docs SSOT、canonical/installed/platform copies、installer、runtime、eval adapter 与测试；未把既有 `pass` 或脚本返回值替代为本轮语义结论。
- 本轮唯一写入为本报告；未修改实现、Docs、其它 task artifact，未提交、push、创建 PR、关闭 issue 或调用 `finish-work`。

## Issue、Authority 与关闭范围

- Live GitHub 状态：#145 为 open，且仍是唯一 `close_issue`；#144、#147 为 closed authority refs；#146 为 open follow-up。
- #145 authority comment `5037168364` 与 task ledger 一致：proposal
  `b0f134e6b53061ca4390e45a6dcf79edf020ef43e2fef57e0ed03f08278eb5be`
  和 `a2c902d92d3650c6431088b3f7e660b5bfb4a6f0123e7af7abcfaf40c5a1504a`
  均为 `accepted_current`；action digest 为
  `daa17d1458eab48e170fbc9c48b6167152d73018c57d929544690a54b4b6dd2e`。
- #144 只提供 Interface 1.3 optional scalar compatibility authority；#147 只提供 production semantic eval runner/adapter closure authority。两者不 reopen、不再次关闭。
- #146 继续独占 `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 三包迁移；三包在当前 registry 中仍精确为 `guru-team-skill-interface-1.2 + legacy`。
- #98、#127、#132 仅为 related issues。任何 PR readiness 只能使用 `Closes #145`，不得关闭 #98/#127/#132/#144/#146/#147。
- 明确排除恶意伪造/篡改、锁、并发压力、TOCTOU、额外 fault injection、crash consistency 与跨 OS 原子性；本轮没有以这些已排除场景制造 finding。

## 三个 Commit 与 Phase 2 证据

- `72326953e4df36a91201f10f581361b045e8c6f0`：完成 Stage 0 六包最小 handoff、manifest、runtime/eval、distribution 与 Docs 主迁移。
- `ded63e71e5bab787c5d795a300e3507142b18521`：修复 Round 1 preset transaction finding，并排除 `.trellis/.developer`、runtime/workspace、Git 与 Python cache 的 staging/activation。
- `9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`：修复 Round 3 non-main fallback finding，使 sync-directed projection 省略 optional base，由 formal resolver 独占 fallback。
- 三个 commit 的 parent 链精确为 `096d1889 -> 7232695 -> ded63e7 -> 9f94108`；task commit plans 分别绑定对应 committed paths/tree/blob/mode。Commit 003 的 exact stage paths 与实际 paths 均为 92，expected/actual tree 均为 `ed8c7f4325113fc83911a264d8be8fcf4d4a73ae`。
- Fresh Phase 2 artifact SHA-256 为
  `dbf5ab3535c5fd5ab2829e1bb610a8d9caa1869d60368015ad222012bfc790e3`，
  `facts_sha256=73334880433f8384f50537d7ec645dd1acd02d49387d3a1f8dfa6e570f6c9eec`；
  `typed_exit=passed`、AI Gate passed、`full_rerun=true`、findings=0。
- Phase 2 在 pre-commit HEAD `ded63e71` 上绑定完整 committed scope 与 92 个 finding-fix dirty bytes；Commit 003 证明这些 bytes/modes 被原样提交。按 post-commit ancestor audit 合同，不应仅为匹配新 HEAD 重录 Phase 2；最终 `review-branch.sh` 应执行正式 post-commit audit。本审查没有运行该 gate script。

## 审查轮次与问题生命周期

| Round | Agent | Reviewed HEAD | 结果 | 生命周期结论 |
| --- | --- | --- | --- | --- |
| 1 | `/root/issue145_final_review` | `7232695` | P1=1 | F-001：preset conflict 会留下 mixed graph，open/blocking |
| 2 | 同一 finding owner | `ded63e7` | findings=0 | F-001 通过 staging transaction、失败保留旧 graph 与 recovery tests 关闭 |
| 3 | `/root/issue145_final_release` | `ded63e7` | P1=1 | F-001：semantic re-entry 把 non-main fallback 改写为显式 `main`，open/blocking |
| 4 | 同一 finding owner | `9f94108` | findings=0 | F-001 通过 optional projection omission 与 formal resolver 端到端回归关闭 |
| 5 | `/root/issue145_final_release_r2` | `9f94108` | findings=0 | fresh final review；两个既有 finding 均保持 closed，未发现新 finding |

- Round 1-4 报告 SHA-256 与 assignment ledger 精确匹配：
  `2b2b08d3...`、`c838ceb4...`、`8f98923d...`、`89a4cad2...`。
- 两个 finding 均有正常路径 reproduction、对应 fix commit、原 finding owner closure 和后续 fresh final review；没有跳过 finding-fix full rerun，也没有让 finding owner 直接完成最终放行。

## 实现与公共合同

- Migration manifest 精确包含 6 Skills / 24 exits；registry 共 9 个 active packages，其中六包为 Interface 1.3 + `minimal_handoff`，#146 三包为 Interface 1.2 + `legacy`。
- 六包分别拥有 caller-owned input profile/scalar signature、per-exit closed output schema/example、唯一 consumer contract、declarative projection、private artifact declaration 与 canonical eval corpus；24 exits 与 profile/case bindings 双向闭合。
- `guru-sync-base.base_branch` 的 `required:false` 是显式 boolean。携带 base 保留 explicit 优先级；省略 base 时 formal resolver 继续使用 configured scalar -> ordered candidates -> remote default，semantic producer 不再硬编码 `main`。
- `guru-clarify-requirements` 三条相关输出与 `guru-review-change-request` 两条相关输出已删除 unresolved `handoff_base_branch`；三条 sync-directed projection 可合法省略 optional scalar，`needs_context` / `ready` 的 consumer schema 也允许 omission。
- Semantic public wrapper 只从 repo-local、checker-passed owner result 获取 actual typed exit；actual exit 先选择 output schema，`expected_exit` 只在 wrapper 返回后进行 expected-vs-actual assertion，未进入 adapter request、wrapper argv、owner recipe selector或 schema selector。
- 正常 Agent-facing projection 不含 eval corpus或 private runtime，trace 要求一次 Skill contract read + 一次 public wrapper invocation，并拒绝 undeclared read；owner staging 位于 Agent invocation boundary 之前，不把 private artifact/runtime 暴露为 public authoring input。
- Runtime/script 仍只执行 parsing、projection、checker、executor、validator 与 recorder 事实；Stage 0 semantic owner、human confirmation、route intent 与 issue scope 未迁移到脚本判断。

## Docs SSOT

- Docs strategy 为 `ssot_first`；fresh Phase 2 绑定 15 个 durable paths：workflow/preset/docs specs、三份 requirements docs 与 root/workflow/preset 三份公开 README。
- Durable docs 与代码一致声明：六包/24 exits 的 Interface 1.3 production activation、三包 #146 legacy boundary、optional base 的 formal resolver ownership、actual-exit schema selection、同 corpus 跨平台 eval、一次 preset staging transaction、pre-#145 upgrade、update/reapply 与 `.new/.bak` fail-closed/recovery 规则。
- Round 3 修复只删除 premature fallback 并使 consumer optionality 对齐既有 durable contract，没有改变 stable Skill/exit/schema ids、resolver precedence、semantic ownership或版本策略；fresh Phase 2 的 no-update reason 成立。
- Task-local PRD/design/implement、authority、liveness、finding reproduction 与 closure narrative 继续是历史/审查证据，没有变成与 durable docs 竞争的长期 SSOT。
- 官方 Trellis 当前文档继续确认 workflow 行为位于 `.trellis/workflow.md`，marketplace workflow 不要求修改上游源码；spec template marketplace 只承载可复用规范，不承载 active task、平台 prompt 或私有 runtime。本分支遵守这些扩展边界。

## 安装、Upgrade 与 Update

- Source validator 与 installed validator 均通过；installed facts 为 1284 managed files、0 conflict、0 removal、0 sidecar。
- Canonical 到 installed/shared/Codex/Claude/Cursor 六包 bytes/modes parity 为 30/30；registry、migration manifest 与 manifest schema source/installed parity 通过；dogfood overlay drift 与 upstream ownership 均通过。
- 独立完整 throwaway 验证通过：workflow marketplace discovery、local unpublished current-source workflow sample、clean preset install、Stage 0 normal/refresh/stop/mutation/recovery smoke、pre-#145 upgrade、Trellis workflow preview/switch、`trellis update`、preset reapply、source/installed validation、selected-platform parity 与最终零 `.new/.bak`。
- Preset transaction tests 45/45 通过，继续覆盖 unknown local edit 保留旧完整 graph、known managed backup graph、backup acknowledgement/reapply、forced installed-validation failure 与 developer identity 不被 staging/activation 覆盖。
- 未发布 feature branch 的 default throwaway guard 按合同返回 exit 2，明确拒绝把 public `main` marketplace sample 冒充当前 branch proof。Exact remote feature-branch marketplace install 必须在 branch 可远程解析后的 publish gate 补充；这是发布时序限制，不是当前实现 finding。

## 部署与安全影响

- 完整 diff 未修改 GitHub Actions、container/Docker、K8s/Kustomize、Helm、DB migration、Makefile 或 dependency lock/config paths；无数据库、生产配置、镜像、集群或部署动作。
- 变更影响 repo-local Trellis workflow package/runtime、preset distribution、平台 adapter/copies 与文档；升级时需按既有 `.new/.bak` 人工处理合同完成 reapply，不需要服务停机或数据迁移。
- Secret-shaped diff scan为 0；未发现 private key、GitHub token、AWS access key、`.env`、签名 URL、客户数据或原始 provider payload进入 diff、task evidence或报告。
- 本轮没有扩大权限、credential处理或生产副作用。GitHub issue/worktree/task mutation仍由 `guru-create-task-workspace` 独占，并受既有 semantic gate 与 confirmation 约束。

## 验证

- Skill package tests：`161/161`，通过。
- Workflow runtime tests：`548/548`，通过；13 个 capability-dependent tests skipped。
- Preset tests：`45/45`，通过。
- Upstream ownership tests：`6/6`，通过。
- Shared production eval：fresh Phase 2 记录六包 `24/24`；本轮完整 Skill suite 重新覆盖 actual-exit/expected-exit、profile/exit binding 与 non-main producer -> projection -> consumer 路径。
- Source / installed package validators：通过；activation set=`6/24`，active=`9`，minimal=`6`，legacy=`3`。
- Canonical/installed/shared/Codex/Claude/Cursor package parity：`30/30`。
- Dogfood overlay drift、upstream ownership、changed JSON、Python/shell syntax、task validation、`git diff --check`、recursive sidecar scan：通过或由 fresh Phase 2 完整记录并由本轮关键门禁复核。
- Full throwaway install/upgrade/update/reapply：通过；default unpublished marketplace guard：按预期 exit 2。
- 完整 diff 的 CI/CD/container/K8s/Helm/DB/Make/dependency path scan与 secret-shaped material scan：均 0。

## 发现项（P0-P3）

- P0：0。
- P1：0。
- P2：0。
- P3：0。
- `findings_count: 0`。
- 未发现可在已批准、honest-but-fallible 正常路径中复现的 current-scope correctness、compatibility、distribution、Docs、deployment或安全缺陷。

## 观察项

- Exact remote feature-branch marketplace install 尚未执行；分支未发布时无法提供该 remote proof。Local current-source 与 public marketplace discovery 均已验证，default guard 已防止错误宣称。
- Authenticated Claude native live probe 本地未完成；repository tests 已覆盖 Claude stdin/safe-mode 协议、fake-native trace 与 declared unsupported，且四平台 package bytes parity 通过。此项保留为外部 capability 限制，不阻断当前交付。
- 当前 worktree 的 dirty/untracked 内容仅为 Branch Review/commit-plan/assignment task metadata 与本报告；未发现未受审实现或 durable Docs 路径。正式 gate 仍应以 workspace boundary 与 post-commit Phase 2 audit 重新验证该事实。

## 后续候选

- #146 继续迁移 planning / Phase 2 / task commit 三包；不得并入 #145 的最终通过语义。
- Publish gate 在 branch 可远程解析后补 exact remote marketplace source proof，并在 PR readiness 中明确 `Closes #145`、部署无影响与上述 capability/时序限制。
- 不新增恶意 actor、锁、并发压力、TOCTOU、crash consistency、跨 OS 原子性或额外 fault injection follow-up；这些场景未被当前 requirement 触发。

## 结论

- `reviewed_head: 9f941087994eb4ea1e4fa9e0c407f8ba3ffd84f8`。
- `reuse_decision: new-agent`。
- `findings_count: 0`。
- Final Branch Review semantic result：**passed**。
- #145 的 Stage 0 六包最小 typed handoff、optional base fallback、production eval closure、atomic preset activation、distribution、Docs SSOT 与 upgrade/update contract 已获得完整实现与验证证据；Round 1/3 两个 P1 生命周期均已闭环。
- 本报告支持主会话继续执行正式 workspace boundary、post-commit Branch Review gate recorder/validator 与 human-artifact resolution；本报告自身不授权 push、PR、issue closure 或 `finish-work`。
