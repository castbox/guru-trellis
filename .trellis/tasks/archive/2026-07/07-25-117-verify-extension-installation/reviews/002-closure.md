# Branch Review Finding Closure 原始报告

## 审查身份与范围

- 审查意图：`finding_fix_review`
- 角色：问题闭环审查代理
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Issue：`castbox/guru-trellis#117`，live state 为 `OPEN`
- Branch：`feat/117-verify-extension-installation`
- Base：`origin/main`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：`538def79408d417107c3adae61c4466116395d96`
- 完整范围：`origin/main...HEAD`，325 files，44401 additions，2883 deletions
- Finding-fix 范围：`5ffa1077167d067130e72e3768c9e9097052f8a6..538def79408d417107c3adae61c4466116395d96`，21 files
- 行为边界：只读审查实现与证据；除本 raw report 外未修改实现、stage、commit、push、创建 PR 或关闭 Issue；未调用 review recorder/checker/public wrapper

Workspace boundary 通过：

- Expected workspace 与 actual repo root 均为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`
- Source checkout 为
  `/Users/wumengye/Documents/GoProjects/guru-trellis`，无 source checkout 改动
- 审查开始时 task worktree 只有允许的
  `agent-assignment.json` 与 `task-commit-plans/002.json` recorder/liveness 改动
- Suspicious source artifacts：无

## 上游证据复核

- Live Issue #117 正文与 `issuecomment-5045035361` 均已读取；本轮两个 finding 都属于正文明确要求的正常 correctness/security-redaction 路径，不依赖恶意篡改、对抗输入或非常规并发场景。
- Planning approval 为 schema `2.0`、`typed_exit=approved`；`ambiguity_review.status=passed`，fixed normative scan 无 hit、无 unchecked hit；用户确认记录明确为 `source=explicit-post-planning-review`。
- 当前 `prd.md`、`design.md`、`implement.md` SHA-256 分别为
  `e8f4402d...`、`24437f24...`、`7922efb0...`，与 approved planning 完全一致。
- Current Phase 2 为 `guru-check-task:passed`。其 snapshot 绑定 parent HEAD
  `5ffa1077...` 加 finding-fix dirty scope；`task-commit-plans/002.json` 随后记录 commit
  `538def79...`、parent `5ffa1077...`，且 expected/actual tree
  `492f6ba19fb12d59ec4d2d5a4e9642348e980b05` 完全匹配。
- 既有 `review.md`、`review-gate.json` 与 `reviews/001-final.md` 正确保留旧 HEAD
  `5ffa1077...` 上的两个 open P1；它们不是当前 HEAD 的 pass 证据，本轮未改写。

## Finding Closure

### BR-117-F1：Closed

原 finding：HTTP(S) credential URL userinfo 漏检，可能使 secret URL 进入
`marketplace-verification.json` 或公开错误/trace。

Qualification 复核：

- Scenario class：`normal_required_behavior`
- Requirement refs：Issue #117 Redaction、`prd.md` 3.7 与验收标准、canonical package
  `references/contract.md` 的 Private evidence
- 无需恶意行为即可由正常 semantic evidence 或 command evidence 触发，原 P1 qualification
  仍成立。

关闭证据：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18205`
  使用 case-insensitive authority-userinfo 扫描
  `https?://[^/\s@]*@`。它覆盖 empty、username-only、username/password、
  percent-encoded 与 multiple-`@`，并让空白或 `/` 终止 authority candidate。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18431`
  在 private payload validation 中统一产生 generic
  `private evidence contains unredacted sensitive material.`。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:25472`
  在 `write_json()` 前运行完整 payload validation；有 redaction error 时直接抛出，
  `marketplace-verification.json` 不会写入。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:15225`
  覆盖五类 URL 形状及 whitespace/path non-credential controls。
- 同文件 `:15247` 覆盖 artifact absence、generic public error 与 CLI stdout/stderr
  不反射 credential URL。
- Fresh independent probe 对五类形状逐一执行 recorder path：5/5 fail closed，
  5/5 artifact absent，5/5 public error generic 且不含输入。
- Fresh Shared source production eval：7/7 passed；新 run root 的 retained files 扫描
  对 credential URL、`github_pat_`、`ghp_`、`x-access-token:` 为 0 hits。
- Canonical 与 installed runtime SHA-256 均为
  `5bb3a7c7d543b6d27aa455664562eae08ed0f696b81b500a681aa81e1a5c1572`；
  Shared/installed adapter SHA-256 均为
  `21ddaa1f7d316a2ec9e60d1d089dce1a2d14aaf4405a57685e1824196244e8e9`。

结论：原泄漏路径在 artifact write 前关闭，公开错误不反射 secret，eval retained
surface 保持 generic error/digest 边界。`BR-117-F1` 可标记 `closed`。

### BR-117-F2：Closed

原 finding：task-bearing execute/record/check 未重建 active task 与 repository/worktree
identity，可接受 wrong、archived 或 wrong-worktree task 并污染 artifact/route。

Qualification 复核：

- Scenario class：`normal_required_behavior`
- Requirement refs：`prd.md` 3.3、package Interface `repository_identity`、canonical package
  `references/contract.md` Entry
- 普通 stale/misrouted `task_ref` 是支持流程中的常见错误，不依赖伪造或 hostile input，
  原 P1 qualification 仍成立。

关闭证据：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:25238`
  新增单一 `extension_verification_task_identity()`：
  - 只接受 `.trellis/tasks` 下 direct active task；
  - 必须加载 `task-start-context.json`；
  - 校验 `task_ref`、task slug、active status；
  - 校验 live branch、`task.json`、portable context branch；
  - 校验 public `repo_ref` 与 context source repo；
  - 校验 current active-task pointer；
  - 最后调用共享 `assert_workspace_boundary()`。
- Execute 在同文件 `:18018`、record 在 `:25355`、check 在 `:25513` 均调用该统一
  identity gate；wrong identity 在 command execution、artifact mutation 或 DTO projection
  前 fail closed。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:15310`
  覆盖 record wrong active task 且错误 task 无 artifact。
- 同文件 `:15344` 覆盖 check archived/completed task。
- 同文件 `:15372` 覆盖 execute wrong worktree mapping。
- Fresh independent probes 额外覆盖 missing `task-start-context.json`、inactive status、
  wrong repository 与 wrong branch：4/4 fail closed。
- 同文件 `:15110` 与 fresh independent inventory probe 证明 taskless standalone：
  - 不制造 task identity；
  - consumer 为 session `direct-caller`；
  - record 前后 Git status inventory 不变；
  - `marketplace-verification.json` 数量为 0。
- Fresh `ExtensionVerificationRuntimeTest`：15/15 passed，覆盖 execute/record/check、
  taskless session-only、remote unavailable、retry/stale 与 redaction 的相关交互。

结论：task-bearing 三入口已统一绑定 direct active task、context、status、repo、branch、
active pointer 与 workspace；wrong/archived/wrong-worktree fail closed，taskless standalone
仍 repository-write-free。`BR-117-F2` 可标记 `closed`。

## 新候选资格审查

- 新 candidate：无
- 新 qualified finding：无
- Scope proposal：无
- Rejected candidate：无
- Observation：真实 pushed feature ref 当前仍不存在；exact feature-ref clean installation
  是已批准、已记录的 post-push publication gate，不是本轮 closure finding，也未被 local
  throwaway 冒充。

## Docs SSOT 与分发

- Strategy：`ssot_first`
- Canonical package contract 与 `.trellis/spec/workflow/companion-scripts.md` 已合并
  F1 authority-userinfo redaction 与 F2 task-bearing identity 合同。
- Canonical、installed、Agents、Codex、Claude、Cursor 六份 package contract SHA-256
  相同：`2d7309758901fae30447ab5f3d00b689142cb706defe84d11c9bd996f183f57c`。
- Source/installed package validators 均通过：12 active Skills、46 exits、27 targets。
- Installed state：2322 managed files，0 sidecar，0 removal，0 conflict。
- Dogfood overlay drift 通过；frozen ownership 43/43，未扩大
  `transitional_legacy`。
- 本 finding-fix 未改变 public typed exits、未激活 #118/#119 producer/integration edge。

## 验证结果

- Lint：`git diff --check origin/main...HEAD` 通过
- TypeCheck：不适用；相关 canonical/installed Python runtime 与 adapter
  `compileall` 通过
- Focused tests：`ExtensionVerificationRuntimeTest` 15/15 passed
- Independent F1 probes：5/5 credential URL shapes fail closed，artifact absent，generic
  error 无输入反射
- Independent F2 probes：missing context、inactive status、wrong repo、wrong branch
  4/4 fail closed
- Taskless probe：status inventory unchanged，0 verification artifact
- Shared source production eval：7/7 passed，retained secret-pattern scan 0 hits
- Source/installed validators：通过
- Dogfood/ownership drift：通过

未在本 closure round 重跑 repository-wide 588-test、175-test 与完整 throwaway 长矩阵；
current Phase 2 已记录这些 fresh 全量结果。本轮通过独立代码审查、15-test focused suite、
额外正常路径 probes、production eval、validators 与 drift 检查形成不依赖 Phase 2
结论本身的 closure 证据。

## 部署与安全影响

- F1 secret persistence 风险在 current HEAD 关闭。
- F2 cross-task artifact/route 污染风险在 current HEAD 关闭。
- 完整 diff 未修改 CI/CD、容器、Compose、K8s/Kustomize、DB migration、Makefile、
  dependency manifest 或生产数据面；无需同步部署资产。
- Exact pushed feature-ref clean install 仍需在后续授权 push 后执行，在此之前不得声称
  remote publication verification 完成。

## 结论

- `BR-117-F1`：`closed`
- `BR-117-F2`：`closed`
- 当前 HEAD 新 finding：0
- Closure recommendation：主会话可记录本轮 finding closure；随后必须分派一个未参与
  本轮 closure 的 fresh final reviewer，重新覆盖完整
  `origin/main...538def79408d417107c3adae61c4466116395d96`。本报告不等于 final
  Branch Review pass，也不能单独支持 `review.md`/`review-gate.json` 的 `passed`。
