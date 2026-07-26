# Issue #117 Fresh Final Branch Review

## 检查完成

### 审查身份与范围

- Review package：`guru-review-branch`
- Review profile：`fresh_final_review`
- Reviewer：`/root/issue117_f10_final`
- Closure reviewer：`/root/issue117_f10_closure`
- Base：`origin/main`
- Merge base：`0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：`a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- Full diff：`origin/main...a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- Diff size：340 files，59,076 insertions，3,431 deletions
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`

本轮是 package-owned fresh final review。审查覆盖完整 committed branch，而不是只看
F10 最后一笔提交。没有运行 Guru Team recorder/validator、Branch Review Gate、
commit、push、PR、Issue mutation、publication 或 finish-work。

### 已检查文件

- `AGENTS.md`
- `.agents/skills/guru-review-branch/SKILL.md`
- `.agents/skills/guru-review-branch/references/contract.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/prd.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/design.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/implement.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/planning-approval.json`
- `.trellis/tasks/07-25-117-verify-extension-installation/issue-scope-ledger.json`
- `.trellis/tasks/07-25-117-verify-extension-installation/implementation-handoff.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/phase2-check.json`
- `.trellis/tasks/07-25-117-verify-extension-installation/phase2-worker-report-f8.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/phase2-worker-report-f9.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/phase2-worker-report-f10.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/review.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/review-gate.json`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/001-final.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/002-closure.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/003-final.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/004-f7-closure.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/005-f8-closure.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/006-final.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/007-f9-closure.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/008-final.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/reviews/009-f10-closure.md`
- `.trellis/tasks/07-25-117-verify-extension-installation/task-commit-plans/006.json`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/skills/guru-team/adapters/eval/native_adapter.py`
- `trellis/skills/guru-team/registry.json`
- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `.trellis/spec/workflow/`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/docs/public-docs.md`
- `README.md`
- `docs/requirements/`
- canonical、installed、Agents、Codex、Claude、Cursor 六处分发副本

`check.jsonl` 只有 seed row；已按 fallback 读取 task 三份规划文档并运行
`get_context.py --mode packages`。Planning approval schema 2.0、`typed_exit=approved`、
`ambiguity_review=passed`、fixed-scope scanner evidence、空
`unchecked_normative_hits`、`explicit-post-planning-review` provenance 和三份文档
current digest 均已核验。

### Scope Qualification

| Candidate | 可支持的正常路径 | Authority | Qualification | 结论 |
| --- | --- | --- | --- | --- |
| Collector 的 `unexpected_paths` 本身不遍历任意额外文件 | Collector 枚举 closed canonical expectation；完整 throwaway 同时执行 installed package、manifest、platform、managed inventory 和 sidecar validator | F10 accepted current scope；`normal_required_behavior` | `rejected_candidate` | 当前 acceptance 是完整受管安装 surface，不是任意项目目录扫描。正常受支持路径中的 package/platform/managed extra 会使完整命令非零，executor 不能进入 `passed`。不得把 collector 单层夸称为任意目录扫描器 |
| Exact pushed feature-ref clean install 尚未执行 | 当前没有 push/publication 授权，本地 unpublished source 不能形成 remote ref evidence | PRD 3.5、Design 6/7、post-push publication contract | `out_of_scope` for local closure | 保留为 mandatory post-push gate；不是当前 implementation finding，也不得用 local throwaway 冒充 |
| hostile/tamper、race/TOCTOU/locking、fault injection、crash consistency、cross-OS atomicity | 需要恶意伪造、对抗性输入或非需求异常机制 | `AGENTS.md` 2.1、PRD exclusions | `out_of_scope` | 不进入 finding、scope proposal 或 required follow-up |

Qualification counts：

- qualification candidate：1
- rejected candidate：1
- qualified finding：0
- scope proposal：0
- blocker：0
- deferred post-push observation：1

### F1-F10 Closure Audit

| Finding | Current closure evidence | 结论 |
| --- | --- | --- |
| F1 remote unavailable 不得伪造 HEAD | `ls-remote` 非零或无 exact row 时 `remote_head=null`；只有 blocked execution 可保留 null；checker 重新解析 exact ref，后续恢复会使旧 blocker stale | resolved |
| F2 exact refs namespace | Workflow 使用 `refs/heads/<branch>`；standalone 只接受 exact `refs/heads/**` / `refs/tags/**`；remote command查询 direct 与 peeled 两个 exact refs | resolved |
| F3 task dirty/worktree freshness | Task-bearing evidence记录排除唯一 gate artifact后的 full worktree snapshot digest；checker重算并拒绝 content drift，同时校验 local HEAD | resolved |
| F4 native eval response readiness | Adapter 写完整 `public-invocation-response.pending.json` 后才 `replace()` 发布 final response；consumer只读取 final path；清理同时覆盖 draft/final | resolved |
| F5 credential URL redaction | Artifact write 前使用 `(?i)https?://[^/\s@]*@` 与固定 secret marker fail closed；username-only/password/percent-encoded/empty/multiple-`@` URL均被拒绝；public error只保留泛化文本或 digest | resolved |
| F6 task/worktree identity | execute/record/check 都绑定 direct active task、`task.json`、`task-start-context.json`、repo、branch、active pointer 与 shared workspace boundary；taskless standalone 不制造 task identity | resolved |
| F7 recorder schema 与 supersession | Recorder先加载并验证 execution/review schema再访问字段；existing prior 必须完整自校验；无 prior 不接受 supersedes；replacement 必须 exact match prior `verification_ref` | resolved |
| F8 committed raw report EOF | `reviews/002-closure.md` committed bytes 以正文后单个 LF 结束，没有额外空白行；current file与commit内容一致 | resolved |
| F9 annotated tag identity | exact `ls-remote` direct/peeled rows区分 tag object 与 commit；checkout使用 resolved commit；随后 `HEAD^{commit}` 必须与 resolved commit 相等 | resolved |
| F10 real installed target 与充分证据 | Executor显式传递 throwaway work root，只读取 `<work>/project`；231项 closed inventory绑定 canonical/manifest/platform relation、digest/category；capability绑定 stable `command_refs` 与 `asset_paths`；private inventory不进入 public DTO | resolved |

F1-F10 均已在 current HEAD 的实际代码路径、tests、package contract、durable docs 和
fresh validation 中闭合。没有依赖旧报告结论代替 current implementation 复核。

### 已修复问题

Branch Review 模式不修改 implementation。当前没有需要本 reviewer 修复的问题。

### 未修复问题

没有 current-scope 未修复问题。

Exact pushed feature-ref clean install 是明确的 post-push publication gate。当前禁止
push/publication，因此本轮保持 deferred，不构成 local implementation blocker。

### 验证结果

#### Full Test Suites

- Runtime：
  `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  -> Ran 600，OK，13 skipped
- Skill integration：
  `python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py`
  -> Ran 175，OK
- Preset/ownership：
  `python3 -m unittest test_apply_guru_team_trellis_preset.py test_upstream_ownership.py`
  -> Ran 54，OK
- Twelve canonical package contracts：Ran 114，OK
- Canonical verifier contract：9/9 passed
- Installed verifier contract：9/9 passed

Installed verifier 第一次使用
`python3 -m unittest .trellis/.../test_contract.py` 时因该 dotted module path
无效而由 unittest loader 返回 `KeyError: ''`。改为直接执行 installed test file 后
9/9 passed；这是 reviewer command invocation 格式错误，不是产品测试失败。

#### Validators And Static Checks

- Source Skill validator：passed；12 active Skills、46 exits、12 invokes、
  27 targets、0 legacy
- Installed Skill validator：passed；2,322 managed files，0 sidecar、0 removal、
  0 conflict
- Dogfood overlay drift：passed；43 active / 43 frozen ownership，
  13 classified managed claims
- `task.py validate`：passed
- Changed JSON parse：passed
- Changed Bash syntax：passed
- Canonical/installed Python compile：passed
- `git diff --check origin/main...HEAD`：passed
- Working-tree `git diff --check`：passed
- Recursive non-fixture `.new` / `.bak` scan：0
- Canonical/installed/shared/Codex/Claude/Cursor package equality：passed
- Canonical/installed runtime equality：passed
- Canonical/installed native adapter equality：passed

#### Production Eval

| Adapter | Source | Installed | Actual result |
| --- | --- | --- | --- |
| Shared | 7/7 passed | 7/7 passed | public wrapper与四 exits匹配 |
| Codex | 7/7 passed | 7/7 passed | trusted Git root path通过 |
| Claude | 7/7 passed | 7/7 passed | outer runner清除 `ANTHROPIC_AUTH_TOKEN` 与 `ANTHROPIC_BASE_URL` |
| Cursor | 7/7 unsupported | 7/7 unsupported | 符合 adapter capability contract，没有伪造 pass |

Shared/Codex/Claude 六组 actual exit 序列均为：

1. `verified`
2. `blocked`
3. `not_required`
4. `return_to_task_work`
5. `blocked`
6. `verified`
7. `verified`

#### Full Local-Source Throwaway

命令：

`env TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh /tmp/issue117-final-throwaway.8uqQFQ`

结果：exit 0。终态：

`Verified public marketplace discovery plus local unpublished workflow sample at /tmp/issue117-final-throwaway.8uqQFQ/project`

覆盖 public marketplace discovery、local unpublished workflow init、initial apply、
existing preview/switch、`trellis update --force`、workflow reselect、preset reapply、
no-developer preservation、pre-#146 recovery、ownership、installed eval 和 final
zero-sidecar。

Fresh retained target collector：

| Category | Expected | Observed | Matched | Complete |
| --- | ---: | ---: | ---: | --- |
| workflow | 1 | 1 | 1 | true |
| preset | 6 | 6 | 6 | true |
| schema | 4 | 4 | 4 | true |
| skill | 44 | 44 | 44 | true |
| platform | 176 | 176 | 176 | true |
| Total | 231 | 231 | 231 | true |

- Expected set SHA-256：
  `d46066d8ef62a06c7438bd311ce28c566b48899e481732956fe4e78b4c0d62eb`
- Relations：`canonical_workflow=1`、`managed_manifest=10`、
  `skill_manifest=44`、`platform_manifest=176`
- Platforms：Shared/Codex/Claude/Cursor 各 44
- `missing_paths=[]`
- `duplicate_paths=[]`
- `unexpected_paths=[]`
- `mismatched_paths=[]`
- `relation_errors=[]`

#### Lint / TypeCheck / Tests

- Lint：通过
- TypeCheck：不适用。仓库没有该 Python runtime 的独立 mypy/pyright owner；
  Python compile、full unittest、schema 与 package validators 承接
- Tests：通过

### 证据交接

#### Planning And Commit Binding

- Planning approval schema：2.0
- Planning typed exit：`approved`
- Approval provenance：`explicit-post-planning-review`
- Ambiguity review：passed
- Unchecked normative hits：0
- Plan 006：58 exact stage paths
- Plan 006 commit：
  `a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- Plan 006 parent：
  `a47e1fbd7bedb001649814969096076bb70157db`
- Expected/actual tree：
  `86ab962b02448776e8ac91cfa6b6d45a62f6df4a`
- Tree and all 58 blob/mode rows：matched

#### Docs SSOT

- Strategy：`ssot_first`
- F10 durable delta 已进入 canonical package `interface.json`、
  `references/contract.md`、execution/private schemas、examples、runtime、tests 与
  extension manifest，并同步 installed 与四平台副本
- Higher-level specs、requirements 与 README 已拥有 public I/O、ownership、
  install/update/reapply 和 remote/eval independence 合同
- F10 没有改变 stable Skill id、public DTO、typed exits、consumer route 或安装命令，
  因此 higher-level no-update reason 对 final diff 仍成立
- `review.md` / `review-gate.json` 的 committed 内容仍表示 Round 9 F10 open，是主流程
  尚未消费 closure/final raw reports 的预期 lifecycle；本 reviewer未自行修改 gate

#### Security And Deployment

- 未发现 secret、credential、private key、signed URL、`.env` 或敏感原始记录进入
  tracked artifact、public DTO、eval trace 或报告
- Raw command output不持久化，只记录 digest与size；remote clone argv使用 sanitized
  locator
- Credential authority userinfo在 artifact write前 fail closed
- 变更不涉及数据库、migration、容器、Kubernetes、CI/CD 或 production deployment
- Throwaway和eval只使用临时目录；没有 production write
- Public API变化是 additive active Skill package、两个 input profiles、四 typed exits、
  runtime command inventory和未来 target bootstrap；#118 producer、#119 integration、
  #132 cleanup均未激活

#### Branch Review Handoff

- Diff range：
  `origin/main...a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- Reviewed HEAD：
  `a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- New qualified findings：0
- Scope proposals：0
- Blockers：0
- Deferred：exact pushed feature-ref clean install，post-push only
- 本报告可作为 main session 更新 `review.md` 与 Branch Review Gate 的 fresh final
  semantic evidence；本 reviewer未执行 recorder或gate

### 结论

完整 branch diff、approved planning、Plan 006、F1-F10 lineage、Docs SSOT、public
I/O、consumer mapping、runtime、installer、ownership、六处分发、production eval 和
fresh throwaway/inventory 均通过 current review。

推荐 typed route：`passed`。
