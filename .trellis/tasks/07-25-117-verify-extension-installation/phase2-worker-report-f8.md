# Issue #117 BR-117-F8 Fresh Phase 2 检查报告

## 检查完成

### 检查身份与边界

- 角色：独立 `trellis-check` 阶段二检查代理
  `/root/issue117_phase2_check_f8`。
- Task：
  `.trellis/tasks/07-25-117-verify-extension-installation`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`。
- Branch：`feat/117-verify-extension-installation`。
- 当前 committed HEAD：
  `3bfbd100c8d75a619da19627e7da276a3f2e367b`。
- Base：`origin/main`，merge base
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`。
- 检查范围：`origin/main` 到当前 committed+dirty working tree 的完整 #117 范围，
  不是只检查 F8 单行差异，也没有复用旧 `phase2-check.json` 的语义结论。
- 唯一报告写入：
  `.trellis/tasks/07-25-117-verify-extension-installation/phase2-worker-report-f8.md`。
  本代理未修改 implementation、`phase2-check.json`、`review-gate.json`、
  `agent-assignment.json`、task commit plan、代码、测试或 durable docs。

Workspace boundary fresh checker 通过：

- `expected_workspace` 与 `actual_repo_root` 都是当前 Issue #117 worktree；
- source checkout status 为空；
- suspicious source artifacts 为空；
- task worktree 变更均为既有 F7/F8 lifecycle、review 和 commit metadata 路径。

Planning approval fresh checker 返回 `approved`。审批绑定三份 planning 文档内容，
当前 HEAD/dirty drift 没有改变 PRD、design 或 implement 的已批准语义。

### 已检查文件

- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`。
- `implementation-handoff.md`、`review.md`、`review-gate.json`、
  `phase2-check.json`、`agent-assignment.json`。
- `reviews/001-final.md`、`reviews/002-closure.md`、
  `reviews/003-final.md`、`reviews/004-f7-closure.md`。
- `task-commit-plans/001.json`、`002.json`、`003.json`、
  `issue-scope-ledger.json`、`task-start-context.json`、`task.json`。
- Canonical 与 installed
  `guru-verify-extension-installation` Skill package、Interface、schemas、
  examples、wrappers、eval corpus、contract tests。
- Canonical 与 installed shared runtime、registry、extension manifest、
  workflow marker、consumer/target schema、preset installer 与 ownership inventory。
- `.agents`、`.codex`、`.claude`、`.cursor` 四个平台分发副本。
- `.trellis/spec/workflow/{index,quality-guidelines,skill-package-contract,
  companion-scripts,workflow-contract}.md`。
- `.trellis/spec/preset/installer.md` 与 `.trellis/spec/docs/public-docs.md`。
- `README.md`、workflow/preset README、`docs/requirements/**` durable owners。
- 完整 `origin/main` 到 working tree diff 的 runtime、package、preset、ownership、
  validators、production eval、throwaway install/update/reapply 和 whitespace 结果。

### 已修复问题

本代理没有执行自修复。实现代理提交的 F8 candidate 已验证：

- `reviews/002-closure.md` 相对 HEAD 只删除一个 EOF 多余空行；
- 文件内容 SHA-256 为
  `67ea4c3edefd5ea9195ea19ca4f4f625cb14aaaa857101b573701dc06b9a204d`，
  size 为 `10156` bytes；
- Round 3 `review_rounds[]` 已绑定同一 SHA-256 与 size；
- `check-agent-assignment` fresh 通过，没有其它 stale report digest；
- `review.md` 如实把 F1/F2/F7 记为已关闭，把 F8 implementation candidate 记为
  `resolved_pending_closure`，没有提前声明 reviewer-owned finding closed；
- `implementation-handoff.md` 如实说明当前 HEAD 尚未包含 F8、需要 fresh Phase 2、
  task commit、独立 closure 和 fresh final review。

`BR-117-F8` 的 implementation candidate 因此满足当前 Phase 2。正式 finding closure
仍属于下一次 task commit 后的独立 Branch Review，不由本报告越权完成。

### 未修复问题

没有发现需要返回实现的 current-scope Phase 2 finding。

以下是明确的后续门禁，不是本地 implementation finding：

- `git diff --check origin/main...HEAD` 当前仍读取修复前的
  `3bfbd100...`，因此 exit 2，并精确报告旧 committed
  `reviews/002-closure.md:189`。只有 F8 task work commit 后才能执行并通过这条
  committed-range validation。
- Exact pushed feature-ref clean installation 必须在授权 push 后绑定 exact remote
  ref/HEAD 独立执行。当前 full local-source throwaway 不能冒充这份 publication
  evidence。
- 本报告不授权 commit、push、PR、Issue #117 closure、finish-work 或 release tag。
- Cursor native eval 在当前环境按 adapter 合同返回 `unsupported`，未进入交互会话；
  package/corpus 与 Cursor 分发 bytes 已由 source/installed validator、六处分发 diff
  和 throwaway 验证。

Claude installed native eval 有两次可观察瞬态：

- 第一次完整运行：命令 exit 0，但 run evidence 为 6/7，
  `workflow-stale-plan-reentry-verified` 的 native CLI return code 为 0，却没有生成
  required receipt/native trace，因此 runner 正确标记 `execution_error`。
- 第二次完整运行：命令 exit 0，但 run evidence 为 6/7，另一个
  `workflow-required-verified` case 同类缺 receipt/trace。
- 在其它 native eval 结束后，第三次以相同 clean-auth 条件完整重跑，得到 7/7
  `passed`。Source Claude 同样为 7/7。

失败 case 不固定，未表现为 source/installed bytes、DTO、schema、route 或 credential
配置差异。最终 fresh full rerun 已通过；前两次结果仍保留在本报告中，不伪装成首轮成功。

## 验证结果

### Semantic adequacy

| 维度 | 结论 | Fresh evidence |
| --- | --- | --- |
| Scope qualification | 通过 | F8 是 `normal_required_behavior` P3；candidate 只删除历史 raw report 的一个 EOF 空行 |
| Requirements/design | 通过 | 承接 `implement.md` full-range lint 与 durable quality guideline；未扩大 #117 |
| Runtime correctness | 通过 | 592 passed，13 skipped；F1/F2/F7 normal-path regressions 均在完整 suite 内 |
| Public Skill contract | 通过 | 175 passed；canonical/installed package contract 各 8 passed |
| Registry/graph/schema | 通过 | source/installed 均为 12 active Skills、46 exits、12 invokes、27 targets、0 legacy |
| Preset/ownership | 通过 | preset 45 passed；ownership 9 passed；43/43 frozen inventory，无 errors |
| Distribution | 通过 | canonical、installed、Shared、Codex、Claude、Cursor 六处 package tree byte-identical |
| Production eval | 通过 | Shared/Codex/Claude final source+installed 均 7/7；Cursor 受支持地返回 unsupported |
| Install/update/reapply | 通过 | full local-source throwaway exit 0；覆盖 discovery、init、preview/switch、update/reapply、ownership、sidecar 与 eval |
| Docs SSOT | 通过 | `ssot_first` owners 与 code/tests/manifest/README 一致；F8 无新增 durable delta |
| Redaction/security | 通过 | credential-safe tests、generic error/trace boundary 与 clean-auth Claude eval 通过；未持久化 credential/URL |
| Deployment/compatibility | 通过 | 无 CI/CD、容器、K8s、DB migration、Makefile、dependency 或生产数据面变化 |

Lint：通过。

- `bash -n` 通过。
- `python3 -m json.tool trellis/index.json` 通过。
- `git diff --check origin/main` 与 `git diff --check` 通过。
- `origin/main...HEAD` 的预期旧 committed failure 单独记录，不能用于声明 F8 已提交。

TypeCheck：不适用。

- 仓库没有配置 `mypy`、`pyright` 或 `ruff` type-check contract。
- 两个生产 Python 入口的 `py_compile` 通过。

Tests：通过。

- Runtime：592 passed，13 skipped。
- Skill packages：175 passed。
- Preset：45 passed。
- Ownership unit：9 passed。
- Canonical/installed package contract：各 8 passed。
- Full throwaway 尾部回归：20 passed、4 passed、20 passed。

### 完整命令证据

下表的 `out` / `err` 格式是
`sha256:size_bytes`。空输出统一是
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:0`。
`argv` 是实际目标命令，不包含 shell 日志重定向；没有记录 credential、remote URL
或 raw native transcript。

| argv | Exit | out | err | result_summary |
| --- | ---: | --- | --- | --- |
| `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 0 | `0828b6c2bc16ee117ca70768993f3963f9a3e2985186d07537c918f8eaa966ff:2548` | `62421cf6ca279f77d1c76a1ece733027655b4a41d8549e87f02ec43876be6edc:3889` | 592 passed，13 skipped |
| `python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py` | 0 | empty | `a7e3b1f5124f8a853c91da2b2fc9921d8d6def516fcf029ec9a8c62821a291a1:4064` | 175 passed |
| `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 0 | empty | `e28af043b2f9c21edf6053fa5844e791b1ed3141e74171e10fe5f18accc9f40f:809` | 45 passed |
| `python3 -m unittest trellis/presets/guru-team/scripts/python/test_upstream_ownership.py` | 0 | empty | `a61d330b9216fe766040074ec4bc7b99fb98b6213ad6221ce02b19832fae9d58:107` | 9 passed |
| `python3 trellis/skills/guru-team/packages/guru-verify-extension-installation/tests/test_contract.py` | 0 | empty | `60bb849356ffbc091f601e17fc6ae0b2eb5e26d734d433da020c6e775efbf97f:106` | canonical 8 passed |
| `python3 .trellis/guru-team/skills/packages/guru-verify-extension-installation/tests/test_contract.py` | 0 | empty | `60bb849356ffbc091f601e17fc6ae0b2eb5e26d734d433da020c6e775efbf97f:106` | installed 8 passed |
| `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source` | 0 | `c26bbae76ccab153d845b81cb4e8261025cb5fdc669a3caa1d387e69e4c27338:1322` | empty | passed；12/46/12/27，0 legacy |
| `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed` | 0 | `ff1f196406a78ef3b0788ffeb7c999412fcf7525cc564b40fde7606278e28739:1511` | empty | passed；12/46/12/27，0 legacy |
| `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | 0 | `a4d1fc6245408be090a084662c1f1c1da93723e968fea8d4b8bca28f641cdf9e:1790` | empty | dogfood overlays match canonical |
| `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json` | 0 | `7f2ed5369d0d9507da23cc5007a7baebfe33c17e1b60a3de80690a43abef05e1:1731` | empty | 43 frozen/active，13 claims，54 managed assets，0 errors |
| `.trellis/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode source --skill guru-verify-extension-installation --json` | 0 | `f3659a621bb577a9ee672dfbf85f0e659291b04d4c62e7f9fe9b91750a59a321:3115` | empty | 7 cases，4 adapters |
| `.trellis/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --json` | 0 | `f3659a621bb577a9ee672dfbf85f0e659291b04d4c62e7f9fe9b91750a59a321:3115` | empty | source/installed corpus identity 相同 |
| `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-verify-extension-installation --adapter shared --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-source-shared --json` | 0 | `6a8150e7a9a09e4f7fe47b632fc3053961123b326a647047cd5b98e69f448fb2:7046` | empty | passed 7/7 |
| `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --adapter shared --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-installed-shared --json` | 0 | `8badd2b94deb14cfce4a83722c5ac5babe21dd6be6a029382152ba24327aecbb:7070` | empty | passed 7/7 |
| `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-verify-extension-installation --adapter codex --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-source-codex --json` | 0 | `a44cba8edfd985689951bca0c6b9959bd85ba73d26e1ebce10e42312bdef1c75:7042` | empty | passed 7/7 |
| `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --adapter codex --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-installed-codex --json` | 0 | `3842b9354f162d3c72b65297882e1d03002df8545c07c838e4a6cafa6f23f200:7066` | empty | passed 7/7 |
| `env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL .trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-verify-extension-installation --adapter claude --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-source-claude --json` | 0 | `26048904c383ad309e879e64ad4c4e17ac9b8f1ed3948bb7cd7e6e91ae84a7b0:7053` | empty | passed 7/7 |
| `env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL .trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --adapter claude --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-installed-claude --json` | 0 | `8888ff4f4cb825e04bf6bee6af29f80e48d79d2573a4ae29f8f8e79abcf7ef36:6646` | empty | run evidence 6/7，one missing receipt/trace |
| `env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL .trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --adapter claude --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-installed-claude-rerun --json` | 0 | `59c144eeeec2eef23248c88d41139900bc46df000255251b68e1d39b1b5d0dda:6224` | empty | run evidence 6/7，different missing receipt/trace |
| `env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL .trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --adapter claude --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-installed-claude-rerun2 --json` | 0 | `52138f41e894920e999a4640aa290de14be99fd1d2ed16359e24dafb6266e1a2:7133` | empty | final full rerun passed 7/7 |
| `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-verify-extension-installation --adapter cursor --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-source-cursor --json` | 0 | `3081b017c1decd38356ed99c59aaa8ca190a32a63e9c83b0a8c03bb11045fd82:3439` | empty | 7/7 unsupported，未进入交互 |
| `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-verify-extension-installation --adapter cursor --run-root /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.H2DCmhggib/run-installed-cursor --json` | 0 | `10912fff0fc960f5d6c6095f4b215350102eea8ab2bce76c7b1101c74ce4d6ae:3463` | empty | 7/7 unsupported，未进入交互 |
| `env TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh /var/folders/rd/kbzpxp956nb3p_h04vnfg3l80000gn/T/tmp.q20sv59EOb` | 0 | `d8c87b583fef65d55912c8aa356b21c38e7e8e3954ebfba211a35bba2c0abafe:3646930` | `d3d05b7327306f2cbd87b2893dafafbb64ab058838b55ff276a374491dc73ea7:930` | public discovery + local unpublished workflow sample；full update/reapply passed |

六处分发的五条 canonical-to-destination 命令均 exit 0，stdout/stderr 均为 empty：

```text
diff -qr --exclude=__pycache__ '--exclude=*.pyc' trellis/skills/guru-team/packages/guru-verify-extension-installation .trellis/guru-team/skills/packages/guru-verify-extension-installation
diff -qr --exclude=__pycache__ '--exclude=*.pyc' trellis/skills/guru-team/packages/guru-verify-extension-installation .agents/skills/guru-verify-extension-installation
diff -qr --exclude=__pycache__ '--exclude=*.pyc' trellis/skills/guru-team/packages/guru-verify-extension-installation .codex/skills/guru-verify-extension-installation
diff -qr --exclude=__pycache__ '--exclude=*.pyc' trellis/skills/guru-team/packages/guru-verify-extension-installation .claude/skills/guru-verify-extension-installation
diff -qr --exclude=__pycache__ '--exclude=*.pyc' trellis/skills/guru-team/packages/guru-verify-extension-installation .cursor/skills/guru-verify-extension-installation
```

其余确定性门禁：

| argv | Exit | out | err | result_summary |
| --- | ---: | --- | --- | --- |
| `python3 -m json.tool trellis/index.json` | 0 | `101d90da22a6d19aaeec41f08da41b7176c041de4e2c0ab9058624e1d496d51c:773` | empty | marketplace index JSON valid |
| `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` | 0 | empty | empty | Bash syntax passed |
| `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` | 0 | empty | empty | Python syntax passed |
| `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-25-117-verify-extension-installation` | 0 | `edb6d263c4dec752d4a567d1225a598f69b87b3bdb83984e146620b12d07ba72:333` | empty | task valid |
| `./.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-25-117-verify-extension-installation` | 0 | `092318698f4ebb482b9d05f36cbcf4fdfec73b86ee33a6e75c6cb9728cd23440:1316` | empty | workspace boundary ok |
| `./.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task .trellis/tasks/07-25-117-verify-extension-installation` | 0 | `d20fbd7702c9ab8ae4f1a646ae969ea9e6edd494def9449c3425583a0a9851bd:782` | empty | approved |
| `./.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json --task .trellis/tasks/07-25-117-verify-extension-installation` | 0 | `3c54388731c33009ebbe7842f53e7d3e2a4ebd85b05658e5482b4610173368de:1409` | empty | 18 agents，5 review rounds，Round 3 digest current |
| `trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh --json --task .trellis/tasks/07-25-117-verify-extension-installation` | 0 | `741444a351d5e826affa25f8d41913c5a61beb1937e0e5b440fe120cc2bc8574:768` | empty | 3 work commits valid |
| `git diff --check origin/main` | 0 | empty | empty | base-to-working-tree F8 candidate passed |
| `git diff --check` | 0 | empty | empty | dirty diff passed |
| `git diff --check origin/main...HEAD` | 2 | `bbc795f1b3997576b60cdced9c59663933d7835ca1b3a5bf6010167da5676360:106` | empty | expected pre-commit old EOF finding；post-commit validation required |

一次 exploratory invocation 把已执行的 `task-commit-plans/003.json` 误作为新的
unexecuted candidate 交给 candidate checker，checker 按设计返回 `blocked`：
sequence 已使用、plan 已 committed、current Phase 2 尚未重录。它不是当前 commit
message 或历史 commit result 的失败证据；正确的 task-mode commit checker随后对三个
已提交 work commits 返回 `ok`。本报告不使用该 exploratory result 支撑通过结论。

## 证据交接

### 阶段二

Fresh Phase 2 覆盖 approved PRD/design/implement、完整 committed+dirty diff、prior
F1/F2/F7 closure、F8 candidate、current assignment/review/commit metadata、runtime、
public contract、schema/manifest、preset/ownership、六处分发、native eval、Docs SSOT
与 full throwaway。

Scope-first qualification 结论：

- F1/F2 已由 Round 3 independent closure 关闭，fresh runtime/package/security/task
  boundary regressions通过；
- F7 已由 Round 5 independent closure 关闭，fresh schema-before-access、
  controlled `WorkflowError`、exact-prior supersession 与 complete runtime tests通过；
- F8 working-tree candidate 只删除一个 EOF 空行，base-to-working-tree lint通过；
- 没有新的 `normal_required_behavior`、`existing_supported_behavior` 或
  `newly_accepted_scope` finding。

本报告可支撑主会话为当前 candidate 重新记录 `phase2-check.json` 的 semantic
`passed`。它不直接写 recorder artifact，也不替代 recorder/checker。

### Docs SSOT

- Plan strategy：`ssot_first`。
- 前序 #117 task delta 已合并到 canonical package contract、workflow/spec、
  requirements、README、registry/manifest、installer/runtime/tests。
- F8 只修改 task-local historical raw review report 的格式，不新增 public API、
  schema、workflow route、runtime、installer、ownership、deployment 或 security
  语义，因此 `durable docs update: no` 的理由成立。
- `review.md` 与 `implementation-handoff.md` 仅记录 current task lifecycle 和
  validation provenance，保持 task-history-only。
- Exact pushed-ref verification 仍是后续 publication gate，未被写入 durable docs
  success 声明。

### Branch Review handoff

- 当前 Phase 2 candidate：`passed`。
- 当前 committed HEAD 仍是 F8 修复前的 `3bfbd100...`。
- 下一步必须由主会话记录 fresh Phase 2、创建下一 unused task commit plan、提交
  F8 candidate 和 current task evidence。
- Task commit 后，独立 finding closure reviewer 必须重新执行
  `git diff --check origin/main...HEAD` 并关闭 `BR-117-F8`。
- 随后必须由未参与 closure 的 fresh final reviewer 覆盖最终完整
  `origin/main...HEAD`；本报告不是 Branch Review final pass。
- 未 push、未创建 PR、未关闭 Issue #117、未执行 finish-work。

### Deployment 与 security

F8 本身没有 runtime、API、config、schema、script、container、K8s、database、
Makefile、dependency 或 production data plane 影响。完整 #117 仍是 repository-local
Trellis extension 安装/验证控制面变更。

Claude 命令显式移除 `ANTHROPIC_AUTH_TOKEN` 与 `ANTHROPIC_BASE_URL` 后执行；报告仅记录
变量名、命令 argv、digest/size 和状态，没有记录 credential、endpoint、remote URL、
native raw stdout/stderr 或 transcript body。

## 结论

Phase 2 semantic conclusion：`passed`。

`BR-117-F8` 的 working-tree implementation candidate 已充分实现，current-scope
adequacy dimensions 全部通过，没有开放 Phase 2 finding。主会话可以消费本报告，
重新记录 fresh `phase2-check.json` 并进入下一 task commit。

不得从本结论推导 committed Branch Review pass、remote publication verification、
push、PR、Issue closure 或 finish-work。F8 的正式关闭仍需 task commit 后的独立
closure 与 fresh final review；exact pushed feature-ref clean install 仍需授权 push
后的独立 publication evidence。
