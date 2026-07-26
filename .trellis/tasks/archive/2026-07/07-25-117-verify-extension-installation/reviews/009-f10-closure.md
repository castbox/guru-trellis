# Issue #117 Branch Review Round 10 F10 问题闭环原始报告

## 检查完成

### 审查身份与范围

- 审查意图：`finding_fix_review`
- Package owner：`guru-review-branch`
- 角色：fresh 独立问题闭环审查代理
  `/root/issue117_f10_closure`
- 独立性：未参与 Round 9 `BR-117-F10` 发现、F10 实现或 F10 Phase 2；本轮也不是
  fresh final reviewer
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Issue：`castbox/guru-trellis#117`
- Branch：`feat/117-verify-extension-installation`
- Base：`origin/main`
- Base HEAD / merge base：
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：
  `a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- 完整 committed range：
  `origin/main...a28b38e5a8894e3d60b9e9694a92ed610f763f25`
- 完整范围规模：340 files，59,076 insertions，3,431 deletions；本轮审查了六个
  committed task commits 的完整范围，没有只审查最新 F10 commit
- F10 commit：`a28b38e5a8894e3d60b9e9694a92ed610f763f25`，parent
  `a47e1fbd7bedb001649814969096076bb70157db`，tree
  `86ab962b02448776e8ac91cfa6b6d45a62f6df4a`
- 写入边界：本代理只写本报告；没有修改 implementation、tests、durable docs、
  `review.md`、`review-gate.json`、`phase2-check.json`、
  `agent-assignment.json` 或 task commit plan
- 未执行 recorder、commit、push、PR、Issue mutation、publication、release 或
  `finish-work`

Workspace boundary 在开场与结束前均通过：expected workspace 与 actual repo root
都是当前 Issue #117 worktree；source checkout clean；suspicious source artifacts 为
0。报告写入前 worktree 只有主流程维护的 `agent-assignment.json` 与
`task-commit-plans/006.json` dirty metadata tail，本代理未触碰二者。

Planning approval 为 schema `2.0`、`typed_exit=approved`；
`ambiguity_review.status=passed`、`unchecked_normative_hits=[]`，确认来源是
`explicit-post-planning-review`。PRD、Design、Implement 当前 digest 分别为：

- `e8f4402d93bbd7bd141bd6fa0e493a452a5e4f71ec25f5fb82a8a5b48c25d714`
- `24437f24e32d194d8ac86759aa1f0af8fba0aeb03395df07c2a8dac7f66b9d9d`
- `7922efb0ec9d5995370f2868ea69a1eef46aef56d53007d6b39325b43cab9102`

三者与 approved artifact digest 相同。`check.jsonl` 只有 seed row，因此按 fallback
读取 task artifacts，并从 workflow、preset、Docs SSOT、quality 与 public Skill
contract durable specs 建立审查基线。

### 已检查文件

- Branch Review package：`.agents/skills/guru-review-branch/SKILL.md` 与
  `references/contract.md`
- Task planning/scope：`prd.md`、`design.md`、`implement.md`、
  `planning-approval.json`、`issue-scope-ledger.json`
- Implementation/check handoff：`implementation-handoff.md`、
  `phase2-worker-report-f10.md`、`phase2-check.json`、Plan 006 与当前 assignment
- Review lineage：`review.md`、`review-gate.json`、`reviews/001-final.md` 至
  `reviews/008-final.md`，重点复核 Round 9 `BR-117-F10` qualification 与 required
  closure
- 完整 `origin/main...HEAD` commit/file/hunk inventory、whitespace、redaction、
  deployment 与 public API surface
- Canonical/installed runtime 与 tests：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、installed copy、
  `test_guru_team_trellis.py`
- Canonical/installed eval adapter：
  `trellis/skills/guru-team/adapters/eval/native_adapter.py` 与 installed copy
- Canonical、installed、Shared、Codex、Claude、Cursor 六处
  `guru-verify-extension-installation` package，包含 Skill、Interface、contract、
  schemas、examples、wrappers、eval corpus 与 tests
- Registry、consumer/target graph、extension manifest、preset installer、ownership
  inventory、throwaway installer 与 platform distribution
- `.trellis/spec/workflow/{workflow-contract,skill-package-contract,
  companion-scripts,quality-guidelines,index}.md`
- `.trellis/spec/preset/{installer,upstream-ownership,overlay-guidelines}.md`、
  `.trellis/spec/docs/public-docs.md`
- `README.md`、workflow/preset README 与 `docs/requirements/**` durable owners
- Fresh retained installed target：
  `/tmp/issue117-f10-closure-throwaway/project`

### Candidate Qualification

| Candidate | 受影响正常路径与证据 | 合同绑定 / scenario class | Disposition |
| --- | --- | --- | --- |
| `BR-117-F10`：成功 executor 缺少 installed asset digests 与 capability asset evidence | exact ref checkout 后的正常 clean install success；Round 9 已证明旧实现只保留 source digests | Issue #117 artifact contract、PRD 3.2/3.3/3.4、Design 4.4/5.2；`normal_required_behavior` | 既有 `qualified_finding`，P2；本轮复核为 `closed`，不是新 finding |
| Collector 的 `unexpected_paths` 不枚举任意额外文件 | Collector 以 canonical expectation 枚举 digest；完整 throwaway 同时执行 installed package validator，后者校验 manifest、未知 package/platform copy、managed inventory 与 sidecar，任一异常使 monolithic command 非零且 executor 不能 `passed` | Required closure 2、installed package deterministic contract；`normal_required_behavior` | `rejected_candidate`：分层完整路径已 fail closed；不得把 collector 单层描述成任意目录扫描器 |
| F10 private inventory 可能扩张 public DTO 或把 machine pass 升格为 semantic pass | Interface、四个 output schemas、consumer mapping、recorder/checker shape 与 real-wrapper eval | PRD 3.2/3.4、Interface 1.3 minimal handoff、AGENTS 2/3/4；`normal_required_behavior` | `rejected_candidate`：inventory/digests 仍为 private state，AI 继续拥有 applicability/profile/adequacy/finding/route |
| Exact pushed feature-ref 尚无 clean-install evidence | 当前 HEAD 尚未按 publication 授权推送；fresh throwaway 明确使用 `local unpublished workflow sample` | PRD 3.5、Design 6/7、post-push publication contract；`out_of_scope` for local closure | 保持 post-push publication gate；不伪装为当前 local finding，也不以 local sample 冒充 |
| hostile/tamper/race/TOCTOU/locking/fault-injection/crash/cross-OS 扩展 | 只能通过恶意伪造、对抗性输入或非需求异常机制构造 | AGENTS 2.1 与 PRD 第 5 节；`out_of_scope` | 拒绝进入 finding、scope proposal 或 required follow-up |

Qualification counts：5 candidates；existing finding closed 1；new qualified finding
0；rejected candidate 2；out-of-scope / deferred observation 2；scope proposal 0；
blocker 0。

### BR-117-F10 Closure Evidence

#### 1. 真实 installed target 与 231 项 inventory

`extension_verification_execute_facts()` 现在把显式临时 work root 传给
`verify-throwaway-install.sh`，并只从该命令生成的 `<work>/project` 调用
`extension_verification_installed_asset_facts()`。它不从 source checkout、dogfood
worktree 或 synthetic empty directory 读取 installed bytes。

Fresh full local-source throwaway 的 `/tmp/issue117-f10-closure-throwaway/project`
重新计算结果：

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
- Relation counts：`canonical_workflow=1`、`managed_manifest=10`、
  `skill_manifest=44`、`platform_manifest=176`
- Platform counts：Shared/Codex/Claude/Cursor 各 44
- `missing_paths=[]`、`duplicate_paths=[]`、`unexpected_paths=[]`、
  `mismatched_paths=[]`、`relation_errors=[]`

Expectation 同时绑定 installed path、canonical source path、expected SHA-256、
category、optional platform 与 relation。Workflow、runtime/schema、shared Skill 与四个
platform package 均来自 checked-out canonical bytes；manifest path/source/hash、
selected platform 与 installed byte 任一不一致都会使 inventory incomplete。

#### 2. Per-capability stable evidence

12 个 closed capabilities 不再共享一个无语义的 `evidence_step`。每个 capability
事实使用 stable `command_refs` 与 category-derived `asset_paths`：

- command refs 只能引用当前 execution 中唯一 command id；unknown ref 被 recorder
  shape gate 拒绝；
- asset paths 只能引用当前 installed digest rows；missing ref 被拒绝；
- command、capability、expectation 与 digest path 重复均被拒绝；
- executor success 后若任一 capability 缺 command 或 asset evidence，会把 execution
  降为 `failed`；
- recorder 的 `verified` 路径再次要求 selected capability 顺序/集合一致、全部
  `status=passed` 且 command/asset refs 非空。

Monolithic throwaway command 可以支撑多个能力，但 mapping 由 closed capability-to-
command 与 capability-to-category catalog 确定，不再把最后一个 step index 无差别复制
为全部能力的充分证据。

#### 3. Fail-closed matrix

- Missing installed file：`missing_paths` 非空，`complete=false`
- Duplicate expectation、digest 或 manifest record：duplicate gate / relation error，
  `complete=false`
- Unexpected package/platform copy：完整 throwaway 的 installed validator 返回非零，
  executor 不能进入 `passed`
- Digest/category/platform mismatch：`mismatched_paths` 非空
- Manifest source/hash/count 或 selected platform mismatch：`relation_errors` 非空
- Unknown command/asset ref、重复 command/capability id：semantic shape error
- 空 category、count/digest/expected-set 不一致或任一 capability evidence 不完整：
  `verified` 被拒绝

Fresh 600-test runtime 覆盖 F10 正向 path、mismatch/missing/duplicate、executor real
target、capability refs、compatibility wrapper、F9 branch/lightweight/annotated tag
checkout identity 与既有 retry/stale/redaction/public projection paths。这里的
fail-closed 用于正常 version binding 和 correctness，不宣称 hostile-input authenticity
boundary。

#### 4. Public DTO、typed exits、consumer 与 AI boundary

- Workflow/standalone inputs 仍结构独立；
- `verified`、`not_required`、`return_to_task_work`、`blocked` 四个 output schema、
  `exit_id` discriminator 与唯一 consumer mapping 未改变；
- `asset_expectations`、`asset_digests`、`asset_inventory`、capability command/asset
  refs 只存在于 execution/private evidence schema，不进入 public outputs；
- `verified` 仍需 AI-authored applicability、closed profile、adequacy、findings、route
  与 redaction pass；executor exit 0、inventory complete 或 checker pass 都不能自行
  产生 semantic `verified`；
- #118 producer edge、#119 finish-family integration 与 #132 legacy cleanup 均未激活。

#### 5. 六处分发与 ownership

Canonical package 与 installed、Shared、Codex、Claude、Cursor 五个 destination 在排除
test bytecode 后 byte-identical；canonical/installed runtime 与 native adapter 也相同。
Source/installed validators fresh 通过，均为 12 active Skills、46 exits、12 invokes、
27 targets、0 legacy；installed manifest 为 2,322 managed files、0 sidecar、0 removal、
0 conflict。Fresh throwaway 的 frozen ownership 为 43 active/43 frozen、13 managed
claims、54 managed assets、0 errors。

#### 6. Closure 状态

`BR-117-F10` required closure 1-5 均有当前 committed implementation、schema/contract/
example、normal-path tests、真实 installed target 与六处分发证据。Finding 状态：
`closed`。

### 已修复问题

Branch Review 模式不修改 implementation。F10 修复由 implementation owner 完成；本轮
仅独立确认 closure，没有自修复。

### 未修复问题

没有 current-scope open finding、scope proposal 或 blocker。

Exact pushed feature-ref clean install 尚未执行，因为当前流程没有 push/publication
授权；这是预先声明的 post-push gate，不是本轮未修复 implementation 问题。

## 验证结果

### Fresh Commands

- Runtime：`python3 -m unittest .../test_guru_team_trellis.py` -> 600 passed，
  13 skipped
- Verifier contract：canonical 9/9、installed 9/9 passed
- Source/installed Skill validators：passed；12 active Skills、46 exits、12 invokes、
  27 targets、0 legacy；installed 2,322 files、0 sidecar/removal/conflict
- Retained target collector：231 expected / 231 observed / 231 matched，complete=true
- 六处分发、runtime、adapter equality：passed
- `git diff --check origin/main...a28b38e...` 与 working-tree `git diff --check`：passed
- Recursive non-fixture `.new` / `.bak`：0
- Full local-source throwaway：exit 0；终态为
  `Verified public marketplace discovery plus local unpublished workflow sample ...`
- Workspace boundary final probe：passed；source checkout clean、suspicious artifacts 0

### Production Eval

Fresh source 与 installed matrix：

| Adapter | Source | Installed | 结论 |
| --- | --- | --- | --- |
| Shared | 7/7 passed | 7/7 passed | real public wrapper 与四 exits 匹配 |
| Codex | 7/7 passed | 7/7 passed | trusted Git root path 通过 |
| Claude | 7/7 passed | 7/7 passed | outer runner 使用 `env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL` |
| Cursor | 7/7 unsupported | 7/7 unsupported | 符合 capability contract，未伪造 pass |

Shared/Codex/Claude 六组 actual exit 序列均为：

1. `verified`
2. `blocked`
3. `not_required`
4. `return_to_task_work`
5. `blocked`
6. `verified`
7. `verified`

### Lint / TypeCheck / Tests

- Lint：通过。Fresh diff check、JSON/schema/package validators、distribution equality
  与 non-fixture sidecar scan 均通过；Phase 2 的 Bash syntax、Python compile 与
  dogfood drift 证据由本轮代码/throwaway 路径再次覆盖且未出现回归。
- TypeCheck：不适用。仓库没有该 Python runtime 的独立 mypy/pyright owner；Python
  compile、600-test runtime、schema 与 package validators 承接当前检查。
- Tests：通过。除本轮 fresh 600 + 9 + 9 与八组 eval 外，current Phase 2 还记录
  Skill integration 175、preset/ownership 54、12 canonical package contracts 114，
  并与本轮完整 throwaway 结果一致。

## 证据交接

### Docs SSOT

- Plan strategy：`ssot_first`
- Canonical package Interface、contract、execution/private schemas 与 examples 已承接
  F10 的 explicit work root、真实 installed target、expected set、relation/category
  completeness、per-capability refs 与 fail-closed contract
- Installed/Shared/Codex/Claude/Cursor copies、runtime/tests/adapter 与 extension manifest
  同步；task delta 已合并到 durable package owners
- Higher-level `.trellis/spec/`、requirements 与 README 已拥有 public I/O、ownership、
  install/update/reapply、remote/eval independence 合同。F10 没有改变 stable Skill id、
  public DTO、typed exits、consumer route、安装命令或用户行为，因此 F10 commit 对这些
  higher-level owners 0 diff 的 no-update reason 成立
- Task-history-only 内容包括 F10 finding provenance、旧 command-only gap、Claude
  inherited env 诊断、temporary throwaway locator 与 review lineage；不应复制进 durable
  docs
- Exact pushed ref 是 post-push evidence，不是 Docs SSOT 缺口

### 安全、部署与兼容边界

- Fresh changed-file high-risk credential scan 未发现真实 token、private key、credential
  URL 或 signed URL；fixtures、detector literal 与历史去敏说明不作为 secret finding
- Private evidence只保留 safe repo-relative paths、SHA-256、sanitized argv、exit code、
  output digest/size；不保留 raw command output、native transcript body、绝对 temp path
  或 credential URL
- 完整 diff 没有 dependency manifest、CI/CD workflow、Docker/container、Compose、
  Kubernetes、Helm/Kustomize、DB migration、Makefile 或 production config 变更
- 无 deploy、service restart、production write、private replay 或 data migration
- 当前改动只影响 Guru extension workflow/runtime/package/schema/docs/tests 与
  installation evidence correctness；不要求额外部署资产同步

### Branch Review Gate

- 本报告可作为 Round 10 `BR-117-F10` closure raw evidence，证明该 finding 已关闭且
  当前完整范围没有新 finding、proposal 或 blocker
- 本报告不能单独支持 Branch Review `passed`：package contract 要求 closure 后由一个
  未执行本轮 closure 的不同 fresh final reviewer 再次覆盖完整当前
  `origin/main...HEAD`
- `review.md` / `review-gate.json` 的后续 lifecycle 记录属于主流程；本代理未修改
  recorder artifact

### Exact Pushed Ref Deferred

本轮 full throwaway 明确是 current committed worktree 的 local unpublished workflow
sample。它证明 local-source install/update/reapply correctness，但不能替代
`refs/heads/feat/117-verify-extension-installation` push 后由 `git ls-remote` 解析并绑定
`a28b38e5...` 的 exact remote-ref clean install。该项保持 publication gate，当前状态
`deferred_post_push`，不影响 F10 closure。

## 结论

- `BR-117-F10`：`closed`
- New qualified findings：0
- Scope proposals：0
- Blockers：0
- Closure recommendation：`closure_complete`
- Required next route：`fresh_final_review_required`

Round 10 是问题闭环轮，不是 fresh final pass。即使本轮零新 finding，也必须由未参与
本轮 closure 的不同 reviewer 对完整当前 range 执行最后一轮 fresh final review；在该轮
完成前不得把本报告记录为 Branch Review `passed`，也不授权 push、PR、Issue #117
closure、publication 或 `finish-work`。
