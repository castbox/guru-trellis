# #333 修复 Issue 创建输出与精确恢复

## Goal

修复 `guru-create-task-workspace` 的 reviewed-draft Issue transaction，使真实
`gh issue create` 输出能被正确消费，并使远端 Issue 已创建、当前 invocation 未取得完整结果时的
后续 retry 只收养同一个 live Issue，不执行第二次 create。

该修复保持 GitHub read 的严格 JSON 校验、现有 public Skill/API/typed exits、完整 Intake refresh、
workspace/task transaction 和发布边界不变。

## Background And Confirmed Facts

- Live authority 是 GitHub Issue #333；该 Issue 无 comment 修订，状态为 Open。
- 当前 base 是 `main@c3003568dae6773378f0eca3cdb6c69fcc5cb232`。
- 当前 task branch 是 `fix/333-create-task-workspace-issue-recovery`，task 状态是 `planning`。
- `gh` 版本是 `2.98.0`。`gh issue create --help` 不含 `--json`，成功 stdout 是 canonical Issue URL 文本。
- `gh issue view` 与 `gh issue list` 通过显式 `--json` 输出 JSON。
- `runtime/execute.py:6-10` 的 `github()` 对全部命令 stdout 执行 `json.loads`。
- `runtime/execute.py:26-35` 的 `create_issue()` 把 create 结果当作含 `url` 的 JSON object。
- `references/contract.md:94-101` 已声明 reviewed title/body/labels、capture time、0/1/>1 exact recovery、
  live reread 和零重复 create。
- `tests/test_contract.py:130-136` 通过 mock 返回 `{"url": ...}`，未覆盖 CLI 文本输出，
  未覆盖 0/1/>1 recovery，也未覆盖 remote-create 后 retry。
- Current Requirements 的 `REQ-012` 与 `BEH-006` 已拥有 provider partial recovery 与唯一 owner route。
- Current Test authority 的 `TST-011` 与 `SCN-008` 已拥有 partial recovery 和零重复副作用。
- #249 是 future inactive workspace-preparation cutover authority；本 task 不实现、不修改、不关闭 #249。

## Requirements

### R1. Split GitHub output contracts

1. JSON read path 仅接受一个 JSON object 或 JSON array，parse failure 保持 `invalid_json`。
2. Issue create path 仅接受一个 canonical plain-text Issue URL；接受 CLI 结尾换行，禁止额外非空行。
3. Create path 禁止把文本解析放宽到任意字符串、任意 URL 或 silent fallback。
4. Reviewed title 和 body bytes 原样传给 `gh issue create`；禁止 trim、newline injection 或内容重写。

### R2. Exact post-plan recovery before create

1. 每次 reviewed-draft transaction 在 create 前读取 current open Issue candidate set。
2. Candidate 必须同时满足：repository 相同、state=open、title bytes 相同、body bytes 相同、
   label name set 按 GitHub 大小写无关语义相同、`createdAt >= plan.freshness.captured_at`。
3. Lookup 使用 `created:>=<UTC capture date>`、`--state open`、`--limit 1000` 和声明的 JSON fields。
   Returned row count=1000 时 completeness 未被证明，transaction 必须在 create 前阻断。
4. Runtime 仅从当前 plan 取得 title/body/labels/capture identity，不读取旧 result、Discovery private state
   或跨 invocation cache。
5. Search 返回 malformed JSON、缺必需字段或无法证明 current completeness 时 fail closed。

### R3. Deterministic 0/1/>1 route

1. Exact match count=0：执行一次 `gh issue create`。
2. Exact match count=1：跳过 create，收养该 Issue。
3. Exact match count>1：阻断 transaction，create count 保持 0。
4. Create 与 recover 均进入同一个 live reread/binding helper。
5. Create 与 recover 均产生现有 `created_issue` result variant，并返回现有 `refresh_review` typed exit。

### R4. Immediate live binding

1. Runtime 使用 candidate number 或 parsed canonical URL 立即执行 strict JSON `gh issue view`。
2. Live binding 必须验证 number、canonical URL、state=open、title SHA-256、body SHA-256、按 GitHub
   大小写无关语义归一化的 label set、reviewed draft id 和 reviewed draft SHA-256。
3. Binding mismatch 或 live read failure 阻断当前 invocation。
4. Checker 保持第二次 current live read，确认 executor result 与 live Issue 未漂移。

### R5. Partial-success retry

1. 首次 invocation 在 remote create 后遇到 response parse failure、立即 reread failure 或 result delivery
   failure时，不写 branch、worktree、task、ledger 或 runtime mapping。
2. 下一次同 plan invocation 必须先执行 exact recovery lookup。
3. 唯一 match 被收养后，create operation count 必须仍为 1。
4. Retry 返回的 binding 必须指向首次创建的 Issue number 与 canonical URL。

### R6. Compatibility and unchanged routes

1. 保持 Skill id、Interface 1.4、public input/output schemas、result schema、typed exits 和 consumers 不变。
2. Existing open-Issue workspace/task route保持现有行为。
3. Reviewed-draft zero-match create route保持 `refresh_review` stop boundary。
4. `current` 与 `worktree` workspace mode 不受本修复影响。
5. GitHub access 继续只经 authenticated repo-bound `gh` CLI；禁止 MCP、App、browser、raw HTTP 或 PATH hack。

### R7. Distribution

1. Canonical package 是 `trellis/skills/guru-team/packages/guru-create-task-workspace/**`。
2. Preset apply 生成 `.trellis/guru-team/**` 与 Shared/Codex/Claude/Cursor projections。
3. Affected canonical/installed/platform bytes 与 executable modes 必须通过 existing ownership/parity gate。
4. 未处理 `.new` 或 `.bak` count 必须是 0。

## Acceptance Criteria

- `AC-01`：真实 CLI-shape test 证明 create stdout 是单行 canonical URL 文本，read stdout 仍走 strict JSON。
- `AC-02`：0 exact match 执行一次 create，随后 live reread 产生 valid binding 和 `refresh_review`。
- `AC-03`：1 exact match 执行零次 create，随后 live reread 产生同一 result variant 和 typed exit。
- `AC-04`：2 exact matches 阻断，create operation count=0。
- `AC-05`：fake-`gh` stateful scenario 首次 create 后故意让 response/reread 失败；第二次调用收养首次 Issue，
  cumulative create operation count=1。
- `AC-06`：title、body、labels、state、capture time 或 canonical URL 任一真实 mismatch 不得形成 valid
  binding；仅 label canonical casing 不同必须形成同一 identity。
- `AC-07`：malformed JSON read 继续返回 `invalid_json`；plain-text create 不触发 JSON parse。
- `AC-08`：recovery lookup 返回 1000 rows 时阻断且 create operation count=0。
- `AC-09`：existing issue-only 和 workspace/task-only focused regressions通过。
- `AC-10`：canonical source test、installed package test、preset apply、dogfood drift、ownership/parity、
  recursive sidecar scan 与 `git diff --check` 通过。
- `AC-11`：public interfaces、schemas、commands、typed exits 与 consumer mapping保持 byte/semantic compatibility。
- `AC-12`：完整多平台 release matrix、tag、GitHub Release 和 tag-pinned smoke保持 `unverified`，归 #267。

## Out Of Scope

- 不实现 #249 staged replacement 或 #247 cutover。
- 不创建 downstream playable-ads authority-promotion Issue。
- 不修改 business repository scope。
- 不重构 GitHub authentication。
- 不引入 GitHub App、MCP、browser、raw API 或 PATH workaround。
- 不新增 public Skill、schema version、typed exit 或 transaction artifact。
- 不引入 hostile tampering model、TOCTOU protocol、lock、concurrency stress、fault injection 或 crash-consistency framework。
- 不执行 release-wide matrix、tag、GitHub Release、deployment 或 production experiment。

## Open Questions

无。Current Issue、contract、CLI evidence、RDT authority 与 test authority 已闭合目标、边界和验收。
