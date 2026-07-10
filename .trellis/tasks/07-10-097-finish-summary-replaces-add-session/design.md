# Issue #97 技术设计

## 1. 设计原则

1. Markdown skill/workflow 负责 AI 判断；Python 只做 recorder、validator 和 executor。
2. 完成摘要归属当前 task，不写 repo 级固定 journal/index。
3. 正常 finish 和 #100 backfill 共用一个 schema 与 validator。
4. PR URL 回写是单 task metadata tail，不改变已审查业务内容。
5. 官方 Trellis archive 与 add-session 文件保持不变，Guru Team 只改变自身调用路径。
6. Guru Team context 通过 canonical workflow/skill/overlay 的 no-workspace 路径收集；读取后过滤不满足 non-read 合同。
7. Recovery 只消费已审阅、已提交并与 review gate 绑定的发布输入快照，不重新解析可变 title/body/draft 来源。

## 2. 组件边界

| 组件 | 职责 | 禁止行为 |
| --- | --- | --- |
| `trellis-finish-work` skill/prompt | 生成并审查 `finish-summary-index.json`，展示 dry-run，触发正式 finish | 不伪造 Git、issue、PR、path 事实 |
| `guru_team_trellis.py` recorder | 读取 AI index 输入，收集确定性事实，生成/校验 final summary | 不从自然语言 artifact 推断问题、结果、行为或合同变化 |
| `finish-summary.schema.json` | 固定正常 finish 与 backfill 的结构条件 | 不承载 workflow 判断 |
| `task.py archive` | 执行官方 task 状态更新和目录移动 | 不修改官方实现 |
| `publish-pr` | push、远端验证、创建或恢复 PR、回写 PR URL | 不写 workspace/runtime 固定索引 |
| `pr-readiness.json` | 保存 AI 审阅结论与不可变 `publish_inputs` 快照 | 禁止 recovery 从当前 task/config 重算 title/body/draft |
| shared `trellis-start` 与 Codex/Cursor overlays | 注入 phase、packages、task、spec 与 Git facts | 不打开、枚举或输出 workspace journal/path/line count |
| preset installer | 安装 schema/script/overlay，写配置与 ignore 策略 | 不改 upstream/global npm/node_modules |

## 3. AI index 输入合同

task-local 文件名固定为 `finish-summary-index.json`：

```json
{
  "schema_version": 1,
  "index": {
    "problem": "触发场景与旧行为",
    "outcome": "新行为与非目标边界",
    "changed_behavior": ["行为变化"],
    "affected_surfaces": [
      {"kind": "workflow", "name": "Guru Team finish-work", "paths": ["trellis/workflows/guru-team/workflow.md"], "change": "具体变化"}
    ],
    "contract_changes": [
      {"contract": "finish session recording", "before": "旧合同", "after": "新合同", "source_artifact": "design.md"}
    ],
    "search_terms": {
      "commands": ["add_session.py"],
      "config_keys": ["session_auto_commit"],
      "schema_fields": ["finish-summary.json:index.search_terms"],
      "symbols": ["cmd_finish_work"],
      "phrases": ["workspace journal 冲突", "task-local finish-summary", "完成摘要归档"]
    }
  }
}
```

recorder 生成 `issue_refs`、`pr_refs`、`branches`、`paths` 和 `retrieval_text`。AI input 不接收这些事实字段，防止 branch/diff/issue scope 漂移。

输入文件随 task 归档，作为 AI 判断来源。最终 `finish-summary.json` 是 #98 的唯一搜索输入。

## 4. Final summary 构建

### 4.1 事实来源

| Final 字段 | 来源 |
| --- | --- |
| `task.*` | `task.json`、`task-start-context.json`、实际 archive 路径 |
| `git.base_branch` / `branch` | task context、当前 branch |
| `git.commits` | `base_ref..reviewed_head` 的 commit SHA 序列 |
| raw changed paths | 成功执行 `git diff --name-only <base>...HEAD`，以及 initial 阶段成功执行 `git ls-files --others` 后的排序去重结果 |
| `git.changed_paths` | raw changed paths 过滤 `.trellis/workspace/**` 与 `.trellis/.runtime/**` 后的安全路径集合 |
| path snapshot unavailable | 任一必需 Git path snapshot 命令返回非零；只决定两个 path 数组清空和固定 unavailable fact |
| protected filtering fact | 被过滤集合是否为空；只决定是否追加固定 `contract_changes[]` 事实记录 |
| GitHub issue arrays | `issue-scope-ledger.json` |
| `github.pr_url` | 初始空字符串；创建或恢复 open PR 后写实际 URL |
| `artifacts` | archived task 内白名单文件存在性 |
| `index` 判断字段 | `finish-summary-index.json` |
| `index.search_terms` 事实字段 | issue arrays、branch、changed paths、PR URL |
| `generated_at` | UTC 秒精度 RFC3339 |

### 4.2 retrieval_text

recorder 按固定顺序收集以下字符串，并用单个换行符拼接：

1. `task.title`
2. `index.problem`
3. `index.outcome`
4. `index.changed_behavior[]`
5. `index.affected_surfaces[].change`
6. `index.contract_changes[].before`
7. `index.contract_changes[].after`
8. `index.search_terms.phrases[]`

validator 重新生成该值并做全值比对。总长度超过 3000 时失败，不截断、不补字。

### 4.3 去重与禁止填充

- 字符串先 trim，再以 Unicode 大小写折叠、空白折叠、标点移除后的值做重复比较。
- 同一数组出现规范化重复值时失败。
- 单个字符串中相邻分句规范化后相同时失败。
- `changed_behavior`、`affected_surfaces`、`phrases` 的数量和文本长度按 issue #97 固定上限校验。

### 4.4 路径校验

- final summary 中的 path 必须是 repo-relative 或 task-relative。
- 绝对路径、`..` segment、`.trellis/workspace/**` 与 `.trellis/.runtime/**` 在任一 path 字段中触发失败，不存在删除态例外。
- recorder 必须按固定顺序执行：收集 raw `git diff --name-only <base>...HEAD`、排序去重、分离受保护前缀路径、把其余安全路径写入 `git.changed_paths`、把同一数组写入 `index.search_terms.paths`。
- raw diff 全部命中受保护前缀时，`git.changed_paths=[]` 且 `index.search_terms.paths=[]`；raw diff 同时含受保护路径和普通路径时只保留普通路径；raw diff 不含受保护路径时保留完整排序去重结果。
- initial `git diff`、initial `git ls-files --others`、final/recovery `git diff` 任一失败时，整个 snapshot 视为 unavailable，不保留其它命令产生的任何路径；两个 path 数组必须同时为 `[]`。
- snapshot unavailable 时必须追加且只追加以下固定事实；不得包含命令名、ref、路径、basename、数量、stderr 或环境详情，也不得同时追加 protected filtering fact：

```json
{
  "contract": "finish-summary git path snapshot unavailable",
  "before": "Git 变更路径快照未成功完成。",
  "after": "完成摘要已使用空路径集合，未写入未验证路径。",
  "source_artifact": ""
}
```

- unavailable fact 加入后必须重新派生并全值校验 `retrieval_text`；schema 与 path validator 继续 fail closed。
- 被过滤集合非空时，recorder 必须追加且只追加以下固定事实记录，不得写入被过滤路径、路径 basename 或数量：

```json
{
  "contract": "finish-summary protected path filtering",
  "before": "原始 Git 变更集合包含受保护运行态路径。",
  "after": "完成摘要已过滤受保护运行态路径，过滤项未写入 path 字段。",
  "source_artifact": ""
}
```

- 被过滤集合为空时不得追加该固定事实记录。该记录来自 Git 过滤事实，不从 PRD、review 或 PR body 推断。
- schema 与 Python validator 都必须拒绝 final summary 任一 path 字段中的受保护前缀；固定事实记录只解释过滤发生，不放宽 path validator。
- `artifacts.*` 必须指向当前 archived task 内实际存在的文件。
- `contract_changes[].source_artifact` 必须为空字符串，或命中 `artifacts` 中的 task-relative value。

## 5. Finish/publish 时序

```text
AI 审查 index input
  -> AI 审查 pr-readiness publish_inputs 快照
  -> finish-work --dry-run（只校验与预览）
  -> task.py archive（session_auto_commit=false）
  -> recorder 写 archived finish-summary，pr_url=""
  -> archive/review metadata commit
  -> push + remote marketplace verification
  -> normal gh pr create
     -> 成功：取得 canonical PR URL
     -> 客户端失败：进入 recovery
  -> recovery 只加载 archived pr-readiness 快照
     -> 验证 snapshot digest、committed Git blob、body digest、review gate reviewed HEAD
     -> 重验 repo/branch/base、HEAD/remote HEAD；禁止 title/body/draft override
     -> marketplace required：只复用并严格校验既有 passed verifier evidence
     -> 查询当前 head branch open PR
        -> 1 个：复用 URL
        -> 0 个：同一 repo/base/head/title/body/draft 只重试 gh pr create 一次
        -> 多于 1 个：fail closed
  -> 最终 Git path snapshot 成功时排序去重并过滤受保护前缀
     -> snapshot 失败时两个 path 数组清空并追加固定 unavailable fact
  -> 若过滤集合非空则追加固定 contract change 事实
  -> 回写 pr_url / pr_refs / safe changed_paths
  -> final summary schema validation
  -> 精确单 task metadata commit
  -> push 同一 branch
```

`add_session.py` 不在该序列中。

## 6. PR URL recovery 合同

1. recovery 触发源只有两类：normal `gh pr create` 客户端失败，或已取得 PR URL 后 summary write/validation/commit/push 失败。错误 payload 必须保存失败阶段、已知 PR URL（未知时为空）、`pr-readiness.json` snapshot digest 和 archived task recovery command。
2. `pr-readiness.json.publish_inputs` 固定以下字段：`repo`、`base_branch`、`head_branch`、`reviewed_head_sha`、`title`、`body_source`、`body_sha256`、`draft`、`reviewed_source`；`publish_inputs_sha256` 是上述 object 按 canonical JSON 编码后的 SHA-256。`body_source` 必须固定为同 task 的 `pr-body.md`，`reviewed_source` 必须固定为 `body-artifact:pr-readiness.json`，不接受 task 外路径或内嵌 body。
3. snapshot 与 body 必须在首次 `gh pr create` 前进入已 push 的 task metadata commit。Recovery command 只携带 archived `--body-artifact <pr-readiness.json>` 与固定 task/repo/remote 定位参数，不携带 `--title`、`--body-file`、`--draft` 或 `--no-draft` override。
4. recovery 在任何 PR query/create 前必须依次验证：artifact 与 body 无 dirty/staged 变化；当前 artifact bytes 与绑定 Git blob 完全一致；canonical snapshot digest 与 `publish_inputs_sha256` 一致；body bytes 与 `body_sha256` 一致；`reviewed_head_sha` 等于 Branch Review Gate reviewed HEAD 且是当前 metadata HEAD 的祖先；repo/head/base 与 task context 一致；current HEAD 与 remote branch HEAD 符合 verifier/finish-summary metadata tail allowlist。任一失配立即 fail closed。
5. marketplace verification 为 required 时，normal publish 负责运行 verifier。recovery 不运行 verifier，只调用既有 validator 严格核对 passed artifact、ledger evidence、verified content HEAD、remote HEAD、publish HEAD 与 gate；缺失、pending、tampered 或 stale 均阻塞。
6. 前置复核通过后，recovery 按 snapshot 的 repo + head branch + base branch 查询 open PR，并只执行一个确定分支：
   - 恰好 1 个：复用该 PR 的 canonical URL，不调用 `gh pr create`。
   - 0 个：使用 normal publish 保存的同一 repo/base/head/title/body/draft 调用 `gh pr create` 一次；本次 recovery 调用禁止第二次 create。
   - 多于 1 个：fail closed，报告匹配数量，不选择现有 PR，也不创建新 PR。
7. 查询必须先于 0 个分支的 create 重试，因此“服务端已经创建 PR、客户端却返回失败”的竞态会落入恰好 1 个分支并复用，不产生重复 PR。
8. 0 个分支的单次 create 重试失败时，summary 保持初始空 URL / 空 `pr_refs`，返回非零并再次输出同一 recovery command；后续独立 recovery 调用重新从快照复核与 open PR 查询开始。
9. 取得 PR URL 后，normal 与 recovery 共用同一后续：重算 final safe paths 或按 snapshot-unavailable 合同写空数组，执行 idempotent summary rewrite 和 schema validator，再提交并 push 精确 summary metadata tail。
10. 回写 commit 前读取 `git status`，只接受当前 archived task 的 `finish-summary.json` 和 helper 明确更新的 publish metadata；dirty 或 staged summary 必须能由 recovery 接续，任何额外路径触发失败。
11. commit 后检查 `previous_head..HEAD`，路径集合必须精确匹配 recorder 返回值；随后 push 并核对 remote branch SHA。若 HEAD 已是精确 summary tail，重复 recovery 只验证并 push，不生成重复 commit 或 PR。

## 7. Guru Team no-workspace context 合同

1. canonical `.agents/skills/trellis-start/SKILL.md` 不再运行无 `--mode` 的 `get_context.py`；固定运行 `get_context.py --mode phase`、`get_context.py --mode packages`、`task.py current --source`、`task.py list --mine` 与 `git status --short --branch`，只组合 workflow、package、active task 与 Git facts。
2. Codex/Cursor canonical session-start overlays 必须从既有本地 context builder 中删除 journal helper import 和 journal path/line-count 分支，保留 task、Git、active-task count 与 spec-index facts。
3. shared skill 与 hooks 不得调用 `get_active_journal_file()`、`count_lines()` 或对 `.trellis/workspace/**` 执行 `exists`、glob、iterdir、open/read；输出不得包含 `JOURNAL FILE`、workspace journal path/basename/content/line count。
4. canonical source 必须位于 marketplace workflow/preset overlays，dogfood copy 由 preset apply 同步；官方 `.trellis/scripts/common/session_context.py` 保持不变。
5. 单元测试以 workspace path access guard 让任何 open/enumerate/read 立即失败；fresh throwaway sentinel 在 ignored workspace 放置 journal，再运行 shared start、Codex hook、Cursor hook，验证 guard 未触发且输出不含 sentinel 信号。

## 8. Marketplace verification 兼容

远端 marketplace verifier 只在 normal publish 的 PR 创建前运行，PR URL metadata commit 位于 verifier tail 之后。PR-exists 或 create-failure recovery 必须复用既有 passed evidence，不得因 dirty/staged summary 再运行 verifier。validator 必须接受 current HEAD 为精确 verifier tail 或 verifier + finish-summary tail，严格核对 remote HEAD、ledger 与 gate；其它 path 仍触发失败。`marketplace-verification.json` 增加 `finish_summary_schema_sha256` 与 workspace ignore/config 事实，保证安装产物包含新合同。

## 9. 配置与安装迁移

- preset installer 新增 `ensure_session_auto_commit_false()`，只写顶层 `session_auto_commit: false`，并报告旧值。
- preset installer 新增 workspace ignore recorder，写入 `.trellis/workspace/`，不删除本机 workspace 内容。
- preset installer 停止扫描 `.trellis/workspace/index.md` 与 `.trellis/workspace/*/index.md`。
- 本仓库通过 Git 删除 tracked workspace 文件；删除动作属于本 task work commit。
- finish-summary 不保存这些删除路径或文件内容；固定 contract change 事实只说明过滤发生，不披露路径名。
- `MANAGED_ASSET_PATHS` 加入 finish-summary schema，installed copy 由 preset apply 生成。
- throwaway preview 对预期 `.trellis/workflow.md.new` 做内容校验后必须删除；switch、update、preset reapply 结束后执行递归 `.new/.bak` 扫描，任何剩余 sidecar 使 verifier 失败并报告相对路径。

## 10. Docs SSOT Plan

策略：`ssot_first`。

| 层级 | 文件 | 写入内容 |
| --- | --- | --- |
| 流程 SSOT | `trellis/workflows/guru-team/workflow.md` | finish-summary input、dry-run、archive、publish/recovery 顺序 |
| 数据 SSOT | `finish-summary.schema.json`、`.trellis/spec/workflow/data-contracts.md` | schema、validator、metadata tail 合同 |
| 脚本边界 | `.trellis/spec/workflow/companion-scripts.md` | AI judgment 与 recorder/validator 分层 |
| 安装 SSOT | `.trellis/spec/preset/installer.md`、preset README | schema 安装、config、ignore、upgrade 行为 |
| 用户文档 | root/workflow README、`requirement-main.md`、`guru-team-trellis-flow.md` | Guru Team 不再使用 workspace journal，完整 finish/publish/recovery 时序 |
| 平台入口 | shared start 与 canonical overlays | Codex、Cursor 与 shared skill 使用 no-workspace context；各平台 finish 文案一致 |

task delta 在 Phase 2 合并回上述 durable docs；研究与 review 过程只留在 task archive。

## 11. 兼容与回滚

- 已归档且缺少 summary 的 task 不在本任务修改，交由 #100。
- 正常 finish 缺少 index input 时 fail closed，不回退到 journal。
- live #97 要求 PR create failure 后 publish retry、Git path snapshot 失败时空 paths 加原因，以及 Guru Team context 不读 workspace。此前 P1 已闭环；本设计本轮新增第 6 节不可变快照、第 7 节 no-workspace context、snapshot-unavailable 分支与 sidecar 收敛，必须取得新的 post-planning approval 后才能返回 Phase 2。
- 回滚本任务代码后，tracked workspace 历史不会自动恢复；恢复必须通过独立 Git 变更并重新评估并行冲突。
- 本任务不创建 extension release tag；`0.6.5-guru.3` 的最终 tag 在 merge 后 release 流程处理。
