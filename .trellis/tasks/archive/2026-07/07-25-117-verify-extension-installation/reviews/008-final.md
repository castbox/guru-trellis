# Issue #117 Branch Review Round 9 最终原始报告

## 检查完成

### 审查身份与范围

- 审查意图：`fresh_final_review`
- 角色：最终放行审查代理 `/root/issue117_final_after_f9`
- 独立性：未参与 Issue #117 implementation，也未参与
  `BR-117-F1`、`BR-117-F2`、`BR-117-F7`、`BR-117-F8` 或
  `BR-117-F9` closure
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`
- Issue：`castbox/guru-trellis#117`
- Branch：`feat/117-verify-extension-installation`
- Base：`origin/main`
- Base HEAD / merge base：
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`
- Reviewed HEAD：
  `a47e1fbd7bedb001649814969096076bb70157db`
- 完整 committed range：
  `origin/main...a47e1fbd7bedb001649814969096076bb70157db`
- 完整范围规模：336 files，54,535 insertions，5,689 deletions
- 行为边界：只读审查完整 committed diff、task evidence 与 durable Docs SSOT；
  除本 raw report 外未修改 implementation、tests、durable docs、
  `review.md`、`review-gate.json`、`phase2-check.json`、
  `agent-assignment.json` 或 task commit plan，未 commit、push、创建 PR、
  关闭 Issue 或调用 finish-work

Workspace boundary fresh 通过：

- Expected workspace 与 actual repo root 均为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`。
- Source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`，状态
  clean。
- 写报告前 task worktree 只有主会话维护的 `agent-assignment.json`、
  `task-commit-plans/005.json` 与 `reviews/007-f9-closure.md` lifecycle 改动。
- Suspicious source artifacts 与未处理 `.new` / `.bak`：无。

### 已检查文件

- Branch Review 合同：`.agents/skills/guru-review-branch/SKILL.md` 与
  `references/contract.md`
- Live Issue #117、accepted-current scope、Trellis 官方 workflow / marketplace
  文档
- `prd.md`、`design.md`、`implement.md`、planning approval、issue scope
  ledger、implementation handoff 与 Phase 2 evidence
- `task-commit-plans/005.json`、`review.md`、`review-gate.json`、
  `reviews/001-final.md` 至 `reviews/007-f9-closure.md`
- 完整 `origin/main...HEAD` file/function/hunk inventory、commit tree、
  whitespace 与 deployment/security surfaces
- Canonical runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- Runtime tests：
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- Canonical `guru-verify-extension-installation` Skill、Interface、contract、
  schemas、examples、evals、tests 与 wrappers
- Installed、Agents、Codex、Claude、Cursor package copies，以及
  canonical/installed runtime
- Source/installed registry、extension manifest、consumer schema、workflow
  markers、preset installer、ownership inventory、throwaway installer 与 eval
  adapter
- `.trellis/spec/workflow/{workflow-contract,skill-package-contract,
  companion-scripts,quality-guidelines,data-contracts}.md`
- `.trellis/spec/preset/{installer,overlay-guidelines,
  upstream-ownership}.md` 与 `.trellis/spec/docs/public-docs.md`
- `README.md`、workflow/preset README 与
  `docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md`

Planning evidence 为 schema `2.0`、`typed_exit=approved`；
`ambiguity_review.status=passed`、`unchecked_normative_hits=[]`，用户确认来源为
`explicit-post-planning-review`。三份 planning artifact 当前 SHA-256 分别为：

- PRD：`e8f4402d93bbd7bd141bd6fa0e493a452a5e4f71ec25f5fb82a8a5b48c25d714`
- Design：`24437f24e32d194d8ac86759aa1f0af8fba0aeb03395df07c2a8dac7f66b9d9d`
- Implement：`7922efb0ec9d5995370f2868ea69a1eef46aef56d53007d6b39325b43cab9102`

三者与 planning approval 的 reviewed content digest 一致。

### 既有 Finding Closure 链复核

1. `BR-117-F1`：credential URL redaction 缺口已由 Round 2 closure，状态
   `closed`。
2. `BR-117-F2`：task/worktree identity 缺口已由 Round 2 closure，状态
   `closed`。
3. `BR-117-F7`：recorder schema 与 supersession lineage 缺口已由 Round 4
   closure，状态 `closed`。
4. `BR-117-F8`：committed raw report EOF whitespace 缺口已由 Round 6
   closure，状态 `closed`。
5. `BR-117-F9`：annotated tag direct object 与 resolved checkout commit
   identity 缺口已由 Round 8 closure，状态 `closed`。Current runtime 使用 exact
   direct/peeled `ls-remote`、冻结 resolved commit、checkout 后
   `HEAD^{commit}` 比较，并让 checker/public projection 使用 actual checkout
   commit；branch、lightweight tag、annotated tag 与 mismatch regressions 均存在。

Round 8 明确不是 final pass。本轮由未参与 F9 closure 的 fresh reviewer 重新覆盖
完整 `origin/main...HEAD`，没有把 closure report 当作零 finding 放行结论。

### 已修复问题

无。Branch Review 模式不继续实现或自修复 current-scope finding；
`BR-117-F10` 留给 implementation owner，经完整 Phase 2、fresh task commit、
closure 与新一轮独立 final review 后再判断。

### 未修复问题

#### P2 `BR-117-F10`：成功 executor 未保留 installed asset digests，无法支撑 AI adequacy review

文件：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18188`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18217`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18229`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:15892`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py:16081`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/schemas/execution-facts.schema.json:17`

Qualification：

- Disposition：`qualified_finding`
- Scenario class：`normal_required_behavior`
- Severity：P2
- Status：`open`
- Scope proposal：无
- Requirement refs：
  - Live Issue #117 正向行为第 5 项与 Artifact 合同：Recorder 必须记录
    `installed asset digests`，并覆盖 installed
    workflow/preset/schema/skill/platform digests
  - `prd.md:47`：AI 在 executor 后审查命令事实与安装资产
  - `prd.md:61-63`：Recorder 将 digests、asset inventory 与 command facts
    写入唯一 private artifact
  - `prd.md:73-75`：installed asset digests 必须保留在 owner-private evidence
  - `design.md:231-239`：每个 required capability 都必须有执行事实和资产证据，
    platform corpus 与 installed package bytes 必须一致
  - `design.md:261-269`：private schema 固定包含 installed
    workflow/preset/schema/skill/platform asset digests
- Scope basis：这是 Issue #117 明确要求的 pushed-ref clean install 成功路径及
  private evidence 合同。任何正常 executor success 都进入当前代码段；finding
  不依赖恶意 actor、手工伪造 artifact/hash/state、hostile input、并发竞态、
  TOCTOU、锁、fault injection 或其它排除场景。

当前实现：

1. Throwaway installer 成功后，`tracked_assets` 只列出 remote source checkout
   中的 9 个 `trellis/**` canonical source 文件；随后从
   `source_checkout / relative` 读取 SHA-256。
2. 该 inventory 没有任何 clean throwaway target 中的 installed workflow、preset、
   schema、Skill 或 platform entry path，也没有 installed/canonical pair identity。
3. `status=passed` 只要求这 9 个 source digest 数量完整、throwaway command exit 0、
   ownership count 与 sidecar 结果满足条件；不要求 required installed digest
   inventory 存在或完整。
4. 所有 selected capabilities 都被赋予同一个总体 `status` 和最后一个
   `evidence_step`。该最后一步只保留 throwaway command 的 sanitized argv、exit code、
   stdout/stderr digest 与 size，不能向 AI Gate 提供各 capability 的 installed
   asset bytes/digests。
5. `execution-facts.schema.json` 只约束 `asset_digests` item 具有 path/sha256，
   没有表达或验证 installed categories/completeness；example 也只展示
   `trellis/index.json` source digest。
6. 当前 normal-path tests 验证 remote ref resolution、checkout binding 与 throwaway
   source pinning，但没有断言成功 facts 包含 installed digest categories，也没有
   missing/mismatch installed digest 的 fail-closed regression。

Normal-path control-flow proof：

```text
successful_throwaway -> digest exactly 9 source_checkout/trellis/** files
successful_throwaway -> require len(asset_digests) == 9
successful_throwaway -> map final command status/evidence_step to every capability
installed workflow/preset/schema/skill/platform digest facts -> absent
```

该结论由成功分支本身决定，不需要构造虚假输入。Full local throwaway、production eval、
source/installed package validator 与全部 unit tests 全绿，只能证明安装/分发检查执行成功；
它们不能补写或替代 owner-private evidence 中缺失的 installed asset digests。

影响：

- AI adequacy Gate 收到的 machine facts 无法按 approved design 审查 installed
  workflow/preset/schema/skill/platform bytes，也无法从 retained private evidence
  证明每个 required capability 的安装资产覆盖。
- `exit code 0` 与 throwaway 总体 pass 因而在事实层面替代了本应由 AI 消费的资产证据，
  与 PRD 明确禁止“executor exit code 冒充 semantic verified”的边界冲突。
- Recorder/checker 可以生成 schema-valid、current、`typed_exit=verified` 的 artifact，
  但该 artifact 缺少 current acceptance 明确要求的 installed digest inventory。
- 这是 publication 前验证证据的 correctness 缺口；不改变实际已安装 bytes，却使后续
  `guru-finalize-task` 可能消费没有充分 installed-asset evidence 支撑的 opaque
  `verification_ref`。

Required closure：

1. Executor 必须从真实 clean throwaway 安装结果收集 owner-private installed
   workflow/preset/schema/skill/platform asset digests；不能用 remote source checkout
   digest 或 command exit code替代。
2. Digest inventory 必须有确定的 expected set/category/completeness binding，并与
   canonical/manifest/platform corpus 建立可审查关系；缺失、重复或 mismatch 必须在
   `verified` 前 fail closed。
3. 每个 selected required capability 必须能引用对应 command fact 与 installed asset
   evidence；不能把同一个最后 command step 无差别映射为全部 capability 的充分证据。
4. 同步 package-owned schema、example、contract/runtime 表示及 canonical/installed/
   platform distribution；保持 public DTO、typed exits 与 consumer mapping 不扩张。
5. 增加正常成功路径的 installed digest inventory、category completeness、digest
   mismatch、missing asset 与 capability evidence regression。
6. 修复后重新执行完整 `guru-check-task`、fresh task commit、F10 closure 与独立
   fresh final review；pushed feature ref 可用后还需执行 exact remote-ref gate。

### 其它 Candidate 与 Observation

- `BR-117-F9` closure 后未发现其 direct/peeled parser、checkout comparison、
  checker freshness 或 public `resolved_head` projection 回归。
- Cursor source/installed eval 按 package contract 返回 `unsupported`，没有伪造
  native pass；不构成 finding 或 scope proposal。
- 既有 Claude auth transient 已被 current clean-auth 结果 supersede；没有稳定
  source/schema/route mismatch。
- Exact pushed feature-ref clean installation 尚未执行，因为当前 feature ref 尚未获
  push 授权。Local-source throwaway 不能冒充 remote publication evidence；该 gate
  保持 post-push boundary，不是 F10 的替代验证。

除 `BR-117-F10` 外，本轮没有其它新 qualified finding、scope proposal、
current-scope follow-up 或 ledger 变更建议。

### 验证结果

- Lint：通过
  - `git diff --check origin/main...HEAD`
  - `git diff --check origin/main`
  - `git diff --check`
  - 完整 changed JSON parse、changed Bash `bash -n`、changed Python
    `py_compile` 均通过
  - Canonical/installed/platform package equality 与 runtime equality 通过
- TypeCheck：不适用
  - 仓库未配置 `mypy`、`pyright` 或等价独立 type-check contract
  - 生产 Python 入口由 schema validators、`py_compile` 与 full unit tests 承接
- Tests：通过
  - Runtime：596 tests passed，13 skipped
  - Skill package：175 tests passed
  - Preset + ownership：54 tests passed
  - Canonical package contract：8/8 passed
  - Installed package contract：8/8 passed
- Fresh validators：通过
  - Source/installed graph：各 12 active Skills、46 exits、12 invokes、
    27 targets、0 legacy
  - Installed manifest：2,322 managed files，0 sidecar，0 removal，0 conflict
  - Dogfood overlay drift：passed
  - Upstream ownership：43 frozen/active legacy entries、13 managed claims、
    54 managed assets，0 errors
  - Canonical、installed、Agents、Codex、Claude、Cursor package `diff -qr`
    均相同；canonical/installed runtime `cmp` 相同
  - Non-fixture `.new` / `.bak` recursive scan：0

本轮未重复运行 3.6 MB full local-source throwaway transcript。F9 Phase 2 已对与
current commit tree 精确一致的 candidate 执行该矩阵，exit 0，覆盖 new repo、
marketplace discovery、init、preview/switch、preset apply/reapply、
`trellis update`、ownership、sidecar、contract 与 eval；task commit plan 005 的
expected/actual tree、26 个 path blob/mode 与 `a47e1fbd...` 完全匹配。本轮已 fresh
重跑 full runtime/package/preset/ownership tests、contracts、validators、drift、
distribution、syntax 与 whitespace gates。上述 pass 不覆盖 F10 的 retained installed
digest assertion。

### 证据交接

#### Branch Review

- Diff 范围：完整
  `origin/main...a47e1fbd7bedb001649814969096076bb70157db`
- Reviewed HEAD：`a47e1fbd7bedb001649814969096076bb70157db`
- 既有 findings：F1/F2/F7/F8/F9 均 `closed`
- 新 finding：`BR-117-F10`，P2，`normal_required_behavior`，`open`
- Scope proposal：0
- Verdict / typed route：`implementation_required`
- 本报告可作为 Branch Review Gate 的 Round 9 raw evidence，但不能产生
  `passed`，不能直接改写或冒充 `review.md` / `review-gate.json`

#### Docs SSOT

- Plan strategy：`ssot_first`
- Durable primary owners 已明确要求 installed asset digest inventory、逐 capability
  asset evidence 与 AI adequacy review；F10 是 runtime/schema/example/tests 未完整
  承接既有 approved Docs SSOT，不应通过弱化文档关闭。
- Implementation handoff 已记录 durable docs、task delta merge、task-history-only
  内容与 post-push limitation；F9 的 tag identity delta 已正确合并。
- Current canonical/installed/platform distribution bytes 一致，但该事实没有被成功
  executor 保留为 required installed digest evidence。因此 durable docs、task
  planning 与 runtime 的 current-scope Docs SSOT 不一致，构成 Branch Review blocker。
- F10 closure 应同步必要 schema/example/contract/runtime/tests 与分发副本；若字段形状
  不变，现有 durable requirement 无需重写。最终仍须重新复核 task delta merge 与
  `ssot_first` outcome。

#### Deployment、Upgrade / Update 与 Security

- 完整 336-file range 未修改 CI/CD、Docker/Compose、Kubernetes/Helm/
  Kustomize、DB migration、Makefile、dependency manifest 或 production data
  plane；F10 不需要部署资产或数据迁移。
- Source/installed validators、ownership freeze、zero-sidecar、distribution
  equality 与 prior full update/reapply throwaway 均通过。
- F10 修复涉及 clean-install evidence collection，必须重新执行 new install、
  preview/switch、`trellis update`、preset reapply、ownership 与 sidecar 门禁，
  证明 upgrade/update 后 installed digest inventory 仍 current。
- F10 不扩大 hostile-input/security scope，也不新增 secret、credential、权限或
  authenticity boundary。收集 installed digests 时仍只能持久化去敏 path/digest
  facts，不能保留 credential URL、secret、raw command output、临时绝对路径或
  native transcript body。
- 本报告未记录 token、secret、credential URL、endpoint、signed URL、raw provider
  response 或敏感原始日志。

### 结论

- Qualified finding：1（`BR-117-F10`，P2，open）
- Scope proposal：0
- Final verdict：`implementation_required`
- Typed route：`implementation_required`

当前分支不能通过 Branch Review Gate。Implementation owner 必须修复 F10，重新完成
完整 `guru-check-task`、fresh task commit、finding closure 与独立 fresh final
review。Exact pushed feature-ref clean installation 仍是授权 push 后的 publication
evidence，不能由本地验证冒充。

本报告仅是 fresh final review 的 raw evidence，不授权 publication、push、PR、
Issue #117 closure 或 finish-work。
