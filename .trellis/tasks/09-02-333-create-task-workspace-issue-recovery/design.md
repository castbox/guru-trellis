# #333 Technical Design

## 1. Problem Restatement

Reviewed-draft Issue transaction 需要一个与真实 `gh` output contract 一致的 create path，并需要一个
在 create 前运行的 exact live recovery path。当前实现把 create/read 混入同一个 JSON adapter，导致
remote mutation 成功后本地返回 `invalid_json`，retry 又缺少 recovery lookup。

## 2. Design Invariants

- Semantic owner 仍是 `guru-create-task-workspace`。
- Script 只执行 deterministic GitHub calls、parse、exact comparison、binding 和 route validation。
- GitHub read 保持 strict JSON。
- GitHub create 使用 strict canonical plain-text URL。
- 0/1/>1 是 closed branch；禁止 heuristic candidate selection。
- Create 与 recover 共用 live binding path。
- Public Skill/API/typed exits/schema identity 不变。
- Owner-private cross-invocation cache count=0。
- Remote create 后 retry 通过 live authority恢复，不通过旧 conversation 或旧 private result恢复。

## 3. Runtime Structure

### 3.1 Command runner and decoders

在 `runtime/execute.py` 内收敛一个 package-private command runner：

```text
run_gh(repo, argv)
  -> return stdout on exit=0
  -> raise current provider/stale error on exit!=0
```

Runner 不决定 output format。两个 decoder 独立消费 stdout：

```text
github_json(repo, argv)
  -> json.loads
  -> accept declared JSON shape
  -> invalid_json on parse/shape failure

github_created_issue_url(repo, argv)
  -> remove one terminal line ending
  -> require one non-empty line
  -> require canonical Issue URL shape
  -> reject extra text or extra lines
```

`mutation_boundary_current()`、candidate lookup、live reread 仅调用 `github_json()`。
`gh issue create` 仅调用 `github_created_issue_url()`。

### 3.2 Canonical URL validation

Create stdout validation必须绑定 target repository：

```text
scheme=https
host=current GitHub host
path=/<owner>/<repo>/issues/<positive integer>
query=""
fragment=""
```

Parsed URL 不是 final authority。Runtime 立即执行 `gh issue view <url> --json ...`，并要求 returned
`url` 与 parsed URL 完全相同。该 live read 负责 number、state、content 和 labels authority。

### 3.3 Exact recovery lookup

新增 package-private `find_reviewed_draft_issues(plan)`：

1. 从 `plan.freshness.captured_at` 取 UTC calendar date `YYYY-MM-DD`。
2. 执行 repo-bound `gh issue list --state open --search created:>=YYYY-MM-DD --limit 1000
   --json number,url,state,title,body,createdAt,updatedAt,labels`。
3. JSON root 必须是 array；每个 examined row 必须含完整字段。
4. Returned row count=1000 时 runtime 必须以 `stale_identity` 阻断，因为 query exhaustion 未被证明。
5. Returned row count<1000 时，解析 capture timestamp 与 candidate `createdAt` 为 UTC instant。
6. 逐项 compare：title string 与 body string 保持 byte-exact；label names 通过 Unicode `casefold()` 后
   deduplicate/sort，以匹配 GitHub 大小写无关解析并接受 live canonical casing；state 和 capture threshold
   继续 exact compare。
7. 以 Issue number排序，返回 0、1 或 >1 rows。
8. 字段缺失、timestamp invalid 或 repository binding 不可证明时 fail closed。

Search 仅用于 normal retry recovery。它不扫描 closed Issues，不读取 PR，不引入 duplicate semantic judgment，
也不修改 Intake 的 duplicate-disposition owner。

### 3.4 Closed execution flow

```text
validate plan + mutation boundary
  -> find exact post-plan open Issues
  -> count=0:
       gh issue create -> strict text URL parse -> live view
  -> count=1:
       skip create -> live view by candidate number
  -> count>1:
       fail closed before create
  -> build exact created_issue binding
  -> existing result schema 2.0
  -> existing refresh_review consumer
```

### 3.5 Shared binding helper

`bind_reviewed_issue(plan, locator)` 统一执行：

- strict JSON `issue view`；
- number 与 canonical URL验证；
- `state=open`；
- title/body SHA-256；
- case-folded、deduplicated、sorted label identity；
- reviewed draft id/digest projection；
- `facts_sha256` derivation。

Helper 同时服务 create 和 recover。Result 不新增 `created_by` 或 recovery history 字段，因为 typed consumer
只需要 current live binding；create/recover 来源能从当前 invocation operation counter推导，public consumer
不消费该来源。

## 4. Failure And Retry Semantics

### 4.1 Failure before remote create

Candidate lookup、base recheck 或 create command precondition failure时，remote create count=0。

### 4.2 Failure after remote create

以下 failure 均可能发生在 remote Issue 已存在后：

- create stdout malformed；
- create stdout canonical URL parse failure；
- immediate `issue view` provider failure；
- immediate live binding mismatch；
- result/checker delivery interruption。

当前 invocation fail closed。后续同-plan retry再次运行 candidate lookup；唯一 exact match 被收养，create
不再执行。该机制满足 idempotent recovery，但不声明 cross-process atomicity。

### 4.3 Ambiguity

>1 exact candidates 表示 live authority不能唯一绑定 reviewed plan。Runtime 在 create 前阻断。它不选择
latest、lowest number 或 first row，也不要求用户在本 Skill 内重新判断 duplicate semantics。

## 5. Compatibility

- `guru-create-task-workspace` id 不变。
- Interface 1.4 profile 不变。
- `guru-task-workspace-plan-1.0` 与 result schema 2.0 shape 不变。
- `created|refresh_review|blocked` exit set 不变。
- Existing issue path 继续 strict JSON reread。
- Workspace/task code path不改。
- Error catalog优先复用 `invalid_json` 与 `stale_identity`；只有 current catalog无法准确表达 closed
  failure时才新增 error code，且不得改变 public typed exits。

## 6. Test Design

### 6.1 Adapter contract

- JSON object read pass。
- JSON array list pass。
- malformed JSON read -> `invalid_json`。
- one canonical URL line pass。
- URL + terminal newline pass。
- empty output、extra line、non-URL、wrong repository、query/fragment -> fail closed。

### 6.2 0/1/>1 matrix

- 0 rows -> create call count=1 -> live view -> binding。
- 1 exact row -> create call count=0 -> live view -> same result variant。
- 2 exact rows -> create call count=0 -> blocked/error route。
- 1000 lookup rows -> completeness blocked -> create call count=0。
- Non-matching title/body/labels/state/capture timestamp rows不进入 exact count；仅 label canonical casing
  不同仍视为 exact candidate。

### 6.3 Stateful fake-`gh` recovery

测试创建临时 fake `gh` executable 与 state JSON：

1. `issue list` 初次返回 `[]`。
2. `issue create` 写入 Issue #112，create counter加一，并输出 canonical URL。
3. 首次 `issue view` 注入 provider failure。
4. 第二次 executor run 的 `issue list` 返回 Issue #112。
5. 第二次 run 跳过 create，`issue view` 返回完整 JSON。
6. Final assertions：Issue number=112、canonical URL一致、cumulative create counter=1、typed exit=
   `refresh_review`、workspace/task writes=0。
7. Fake provider 将 reviewed `BUG` canonicalize 为 live `bug`，证明 retry lookup、binding 和 checker 使用
   同一大小写无关 label identity，同时 create argv 仍保留 reviewed label 原字符串。

该 test 使用真实 subprocess/PATH dispatch，不再通过 `mock.patch(execute.github, ...)` 伪造 JSON create。

### 6.4 Regression

- Existing open Issue mutation-boundary test。
- `current` mode workspace/task tests。
- `worktree` mode create/reuse tests。
- Checker live reread drift tests。
- Installed package command/help/runtime tests。

## 7. Docs SSOT Plan

Strategy：`ssot_first`；Scope：`complete_docs`。

### 7.1 Current semantic owners

- Requirements owner：`REQ-012`、`BEH-006` 已覆盖 provider recovery 与零重复 task recovery。
- Test owner：`TST-011`、`SCN-008` 已覆盖 partial recovery 与零重复副作用。
- Architecture owner：current baseline、design constitution、change contract 已覆盖 package-local owner、
  deterministic runtime、minimum necessary complexity 和 current-conforming no-impact route。

这些 current owners 已拥有本修复语义，因此本 task 不创建 RDT contribution，不创建 Architecture
contribution，不修改 shared current version，也不创建 ADR。

### 7.2 Durable delta

- `trellis/skills/guru-team/packages/guru-create-task-workspace/references/contract.md`：明确 read JSON 与
  create text URL decoder、search completeness failure 和 shared binding helper。
- `.trellis/spec/workflow/workflow-contract.md`：仅当 current shared `gh` adapter prose 把全部 stdout
  写成 JSON时，先修正文为 command-declared output contract；若 current prose 已准确，保持不变。
- `.trellis/spec/workflow/companion-scripts.md`：仅当 recovery executor/fake-provider contract存在通用缺口
  时更新；若 current prose 已准确，保持不变。
- `.trellis/spec/workflow/quality-guidelines.md`：仅当 focused recovery validation ownership缺失时更新；
  若 `TST-011/SCN-008` 投影已充分，保持不变。
- Public README、workflow README、preset README：本修复不改变 user command 或 public route，保持不变。

### 7.3 Projection

Canonical 修改完成后运行 preset apply，生成 `.trellis/guru-team/**` 与 Shared/Codex/Claude/Cursor
copies。禁止手工把 generated copy作为 semantic source。

## 8. Architecture Impact

Planning judgment target：`no_architecture_impact`。

Reason：本 task 只把 active package executor 对齐已存在 contract、Requirements、Test authority 和
official CLI output；不改变 owner、boundary、public API、persistence、SDK、external provider、single-writer、
compatibility exit、GAP lifecycle 或 architecture decision。

命中的 constitution identities：

- `mature-practice-applicability`：使用 official `gh` command contract。
- `cohesion-change-isolation`：JSON/text decoder 与 semantic owner 分离。
- `minimum-necessary-complexity`：只实现 0/1/>1 normal recovery，不增加 lock 或 hostile model。
- `debt-one-way-convergence`：删除 test 对虚构 JSON create output 的依赖，不新增 fallback。

No-impact route 不创建 contribution、project-check burden 或 ADR。

## 9. Rollback

- Runtime、contract、tests 作为同一 task commit unit回滚。
- Preset generated copies随 canonical rollback重新 apply。
- Public schemas/exits未变，因此 rollback不需要 migration adapter。
- 若 exact recovery无法在 current `gh issue list` contract下证明 completeness，停止实现并回到 Planning；
  禁止切换 raw API 或弱化 exact match。
