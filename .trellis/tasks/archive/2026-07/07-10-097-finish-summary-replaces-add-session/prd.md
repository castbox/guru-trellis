# Issue #97：用 task-local finish-summary 替代 workspace journal/add_session

## 1. 来源与目标

- Source issue：<https://github.com/castbox/guru-trellis/issues/97>
- 前置 issue：#96 已合并到 `main`，当前基线为 `ff8c03abb259c2a048626ea72e0bf57138db2c14`。
- 目标：Guru Team finish/publish 不再调用官方 `add_session.py`，不再读写 `.trellis/workspace/**`，改用当前 task 内的 `finish-summary.json` 保存完成摘要和历史检索信号。
- 后续消费者：#100 复用本任务定义的 schema 做 archived task 回填，#98 只扫描 archived task 内的 `finish-summary.json`。
- GitHub issue #97 body 已包含方案 A 的安全过滤、Git path snapshot 失败降级、固定事实记录与 PR create failure 后 publish retry 合同。此前 P1 Planning Blocker 已通过 0/1/>1 recovery 规划修订闭环；commit 后独立 Branch Review 又发现 5 个 current-scope finding。本轮规划必须同时承接启动上下文不读 workspace、不可变 recovery 输入、Git path snapshot 失败降级、durable requirements 收敛和 throwaway sidecar 清理；新的 post-planning approval 完成前不得恢复 Phase 2。

## 2. 当前问题

Guru Team `finish-work` 当前在 `task.py archive` 后调用 `add_session.py`。该命令写入 `.trellis/workspace/<developer>/journal-*.md` 和 `index.md`。同一开发员在多个 worktree 中并行完成 task 时，这组固定 tracked 路径会进入多个 PR，形成结构性冲突。

`session_auto_commit: false` 只阻止官方脚本自动 stage/commit，不能阻止 `add_session.py` 写文件。Guru Team 必须停止调用该脚本，并把完成摘要收敛到当前 task 的归档目录。

## 3. 功能需求

### R1. finish-summary 合同

- 新增 canonical JSON Schema：`trellis/workflows/guru-team/schemas/finish-summary.schema.json`。
- schema 版本固定为整数 `1`，正常完成的 `generator` 固定为 `guru-team.finish-work`。
- schema 同时承载 #100 已定义的 `guru-team.finish-summary-backfill` 分支和 `backfill` 条件字段；正常完成产物不得含 `backfill`。
- companion validator 必须检查字段集合、类型、长度、枚举、SHA、issue number、路径净化、数组数量、去重、禁止填充、`retrieval_text` 派生值和正常/backfill 条件分支。
- 最终文件路径固定为 `.trellis/tasks/archive/<YYYY-MM>/<task-slug>/finish-summary.json`。

### R2. AI 判断与脚本事实分层

- finish entry 在 dry-run 前生成 task-local `finish-summary-index.json`，只承载 AI 已审查的 `problem`、`outcome`、`changed_behavior`、`affected_surfaces`、`contract_changes` 与非事实型 search terms。
- `finish-work` 通过 `--finish-summary-index-file` 读取该文件。
- companion script 只注入 task、Git、issue scope、artifact、UTC 时间、branch/path/ref 和 `retrieval_text` 事实，并校验 AI 输入；脚本不得从 PRD、review 或 PR body 推断行为变化和合同变化。
- `finish-summary-index.json` 保留在 task archive 中作为 recorder 输入证据；#98 只读取 `finish-summary.json`。

### R3. finish-work 写入时序

- dry-run 必须校验 index 输入并输出 finish-summary 计划，不执行 archive、journal、commit、push、PR 或文件写入。
- 正式 finish 在 archive 流程中写入 archived task 的 `finish-summary.json`，初始值必须满足 `github.pr_url=""` 和 `index.search_terms.pr_refs=[]`。
- `git.commits` 记录 base 到 Branch Review Gate HEAD 的 task work commits。
- recorder 必须先对 `git diff --name-only <base>...HEAD` 的原始输出排序去重，再过滤 `.trellis/workspace/**` 与 `.trellis/.runtime/**`，把过滤结果写入 `git.changed_paths` 和 `index.search_terms.paths`；两个字段必须完全一致。
- initial `git diff`、initial `git ls-files --others` 或 final/recovery `git diff` 任一命令失败时，recorder 不得写入任何路径或命令错误文本，必须把 `git.changed_paths` 和 `index.search_terms.paths` 同时写为 `[]`，只追加一次固定且不披露路径、basename、数量、stderr 或 ref 的 `finish-summary git path snapshot unavailable` contract fact，并重新派生 `retrieval_text`。
- Git path snapshot 失败分支不得追加 `finish-summary protected path filtering` fact；schema 与 path validator 在该分支仍须 fail closed，不得因降级而接受非法 path。
- schema 与 validator 必须继续拒绝 final summary 任一 path 字段中的 `.trellis/workspace/**` 与 `.trellis/.runtime/**` 路径，不设置删除态或其它例外。
- 当过滤集合非空时，recorder 必须向 `index.contract_changes[]` 追加一条固定事实记录：`contract="finish-summary protected path filtering"`、`before="原始 Git 变更集合包含受保护运行态路径。"`、`after="完成摘要已过滤受保护运行态路径，过滤项未写入 path 字段。"`、`source_artifact=""`。该记录不得包含被过滤路径本身；过滤集合为空时不得追加该记录。
- finish-work 不调用 `.trellis/scripts/add_session.py`，不提供 `--skip-journal`、`--journal-title`、`--journal-summary` 或 add-session commit 参数。

### R4. PR URL 两阶段回写

- `publish-pr` 创建 PR 并获得 URL 后，更新同一 archived task 的 `finish-summary.json`。
- 回写只改变当前 archived task 的 `finish-summary.json` 和脚本明确写入的同 task publish metadata。
- 回写提交必须通过 schema validator 和精确 metadata path allowlist；代码、配置、schema、workflow、preset、docs、test、CI/CD、部署与 Makefile 路径必须触发失败。
- 回写 commit 推送到同一 PR branch，不重新执行 Branch Review Gate。
- recovery 同时承接两类中断：`gh pr create` 客户端返回失败，以及已获得 PR URL 后 summary write/validation/commit/push 失败。任何中断都必须返回可直接执行的 recovery 命令，并指向同一个 task-local `pr-readiness.json` 发布输入快照。
- `pr-readiness.json` 必须成为发布输入 SSOT，固定 repo、base branch、head branch、reviewed HEAD SHA、exact title、task-local body source、body SHA-256、draft、reviewed source 和 canonical snapshot SHA-256。该 artifact 与 body 必须在首次 `gh pr create` 前已提交；recovery 必须验证当前 bytes 与绑定 Git blob、snapshot digest、review gate reviewed HEAD 和 body digest 完全一致。
- recovery command 只能引用 archived task 的 `pr-readiness.json` 和固定 task/repo/remote 定位参数，不得重新接受可改变 title、body 或 draft 的命令行覆盖。artifact/body dirty、staged、未提交、被另一个 metadata commit 改写或摘要不匹配时，必须在 PR query/create 前 fail closed。
- recovery 在查询或创建 PR 前必须重新验证当前 branch 与 base identity、AI-reviewed body/readiness、Branch Review Gate、当前 HEAD 与 remote branch HEAD。marketplace verification 为 required 时，recovery 只能严格校验并复用既有 passed verifier artifact、ledger evidence、verified/remote HEAD 与 gate，不得重跑 verifier。
- 前置复核通过后，recovery 必须查询同一 repo 与当前 head branch 的 open PR：恰好 1 个时复用其 URL；0 个时使用同一 repo/base/head/title/body/draft 安全重试 `gh pr create` 一次；多于 1 个时 fail closed，不选择、不创建 PR。
- `gh pr create` 客户端返回失败但服务端实际已创建 PR 时，上述查询必须先发现并复用恰好 1 个 open PR，禁止再次创建重复 PR。
- 0 个 open PR 分支的单次 create 重试仍失败时，初始 summary 必须保持 `github.pr_url=""` 与 `pr_refs=[]`，命令返回非零并输出同一可执行 recovery；同一次 recovery 调用不得执行第二次 create 重试。
- recovery 取得或复用 canonical PR URL 后，必须继续执行同一 summary rewrite/validation、精确 metadata commit、push 与 remote SHA 校验；重复 recovery 不得生成第二个 PR 或扩大 metadata allowlist。

### R5. workspace 与配置策略

- 从 Git tracking 删除本仓库现有 `.trellis/workspace/index.md`、`.trellis/workspace/wumengye/index.md`、`.trellis/workspace/wumengye/journal-1.md`。
- 上述三个删除路径保留在 Git raw diff 中，但必须从 `git.changed_paths` 和 `index.search_terms.paths` 过滤；过滤事实只通过 R3 的固定 `contract_changes[]` 记录表达。
- `.gitignore` 与 preset installer 必须加入 `.trellis/workspace/` 规则；preset 不再扫描或改写 workspace index 文案。
- `.trellis/config.yaml` 和 preset materialization 必须写入 `session_auto_commit: false`。
- `METADATA_ONLY_PREFIXES` 不再包含 `.trellis/workspace/`。
- Guru Team shared `trellis-start`、Codex session-start 与 Cursor session-start 必须使用 canonical overlay 定义的 no-workspace context 路径，不得打开、枚举、读取或输出 `.trellis/workspace/**` journal、journal path、basename、内容或 line count。
- no-workspace context 只能通过 Guru Team workflow/skill/overlay 实现：shared start 只组合 phase、packages、active task 与 Git facts，Codex/Cursor overlay 删除 journal import/call；不得修改 Trellis upstream、全局 npm、`node_modules` 或把读取后过滤伪装成 non-read。
- 官方 `.trellis/scripts/add_session.py`、`task.py archive` 和 Trellis upstream 文件保持原样。

### R6. canonical、installed copy 与文档

- canonical workflow、companion、schema、preset installer、README、requirements、spec 和平台 overlay 必须表达同一 finish-summary 流程。
- `docs/requirements/guru-team-trellis-flow.md` 必须移除 archive+journal/add_session 旧链路，完整表达 AI index、initial summary、marketplace verifier、0/1/>1 recovery、PR URL metadata tail 与 no-workspace context 合同。
- 执行 all-platform preset apply 后，dogfood installed copy 与 canonical source 必须 byte-equal，overlay drift 必须为零。
- throwaway workflow preview 产生的预期 `.trellis/workflow.md.new` 必须在内容校验后显式删除；preview、switch、update、preset reapply 全部结束后必须递归检查 `.new` / `.bak`，存在任一 sidecar 时失败。
- extension manifest 的 public artifact contract 必须加入 `finish-summary.json`；`0.6.5-guru.3` 尚无 release tag，本任务不创建 tag。

## 4. 非目标

- 不实现 #100 的 archived task backfill 命令。
- 不实现 #98 的历史搜索命令和 `context-discovery.json`。
- 不处理 #99 的 developer identity 前置。
- 不修改官方 Trellis workflow、全局 npm 包或 `node_modules`。
- 不从 `.trellis/workspace/**` 迁移 journal 内容。

## 5. 验收标准

- [ ] 正常 finish-work 和 dry-run 均不调用 `add_session.py`，输出中不存在 journal 计划。
- [ ] shared `trellis-start`、Codex session-start 与 Cursor session-start 的 fresh-install sentinel 测试证明 workspace journal 未被打开、枚举、读取或输出，且上下文不含 journal path、basename、内容或 line count。
- [ ] 正常 finish-work 在 archived task 根目录生成 schema-valid `finish-summary.json`。
- [ ] 正常产物满足 #97 全字段合同；backfill schema 分支满足 #100 缺失字段例外。
- [ ] validator 覆盖 index 必填、最大长度、枚举、路径净化、数量、去重、禁止填充、派生文本一致性和受保护路径全字段禁入。
- [ ] PR 创建成功后回写 `github.pr_url`、`pr_refs` 和安全过滤后的最终 changed paths，并以精确 task metadata commit 推送。
- [ ] PR 创建客户端失败与 PR 创建后 summary tail 失败均进入同一确定性 recovery：发布前置复核通过后，1 个 open PR 复用、0 个 open PR 同参数只重试 create 一次、多于 1 个 fail closed。
- [ ] recovery mutation tests 分别修改 `pr-body.md`、title、draft、repo/base/head、reviewed HEAD SHA、reviewed source、snapshot digest 与 committed readiness blob；每种变更都必须在 PR query/create 前 fail closed。
- [ ] 测试覆盖 normal create failure -> 0 open -> retry create success、客户端失败但已有 1 open -> 复用、多个 open -> fail closed、PR exists + dirty/staged summary recovery、stale/tampered verifier fail closed，以及单次 retry 再失败后保持 initial summary 和同一 recovery command。
- [ ] PR 最终 diff 不含 `.trellis/workspace/**` 内容，只含删除记录和 ignore 策略变更。
- [ ] 测试覆盖 raw diff 全部被过滤后两个 path 数组为空、受保护路径与普通路径混合时只保留普通路径、无过滤项时保留完整排序去重结果三类输入。
- [ ] 测试分别覆盖 initial `git diff`、initial `git ls-files --others`、final/recovery `git diff` 失败：两个 path 数组同时为空，固定 snapshot-unavailable fact 恰好一次，protected-filtering fact 不存在，`retrieval_text` 与最终 index 一致。
- [ ] 过滤集合非空时固定 `contract_changes[]` 记录恰好出现一次且不含被过滤路径；过滤集合为空时该记录不存在。
- [ ] `session_auto_commit: false` 在 dogfood 和新安装 repo 中生效。
- [ ] finish-summary 搜索质量 fixture 覆盖 issue、PR、branch、path、command、config key、schema field、symbol、中文问题短语、artifact/path basename 与完成后行为短语。
- [ ] canonical tests、preset tests、compile、shell syntax、JSON、task validation、overlay drift、canonical/dogfood equality 和 `git diff --check` 全部通过。
- [ ] 干净 throwaway repo 安装后能完成 initial summary 与 PR URL recovery smoke，且 sentinel `add_session.py` 未执行、workspace 未写入。
- [ ] throwaway repo 执行 workflow preview/switch、`trellis update --force` 和 preset reapply 后，finish-summary schema、workflow、`session_auto_commit: false` 与 workspace ignore 策略仍存在，预期 preview sidecar 已清理，最终递归 `.new/.bak` 扫描为空。
- [x] GitHub issue #97 body 已通过 GitHub MCP/API 同步安全过滤合同，并经 live reread 确认 line 162 要求 PR create failure 后 retry。
- [x] 主会话已通过 GitHub MCP/API 把本 R4 的精确 0/1/>1 open PR 状态机同步到 live #97 body，并再次 live reread 确认。
- [ ] 用户审阅本轮承接 5 个 Branch Review finding 的 `prd.md`、`design.md`、`implement.md` 并给出新的 post-planning approval；新 approval 完成前不得恢复 Phase 2。

## 6. Docs SSOT 状态

- 当前状态：`partial_docs`。多数 durable docs 已切换到 finish-summary，但 `docs/requirements/guru-team-trellis-flow.md` 仍描述 archive + journal 旧流程，且启动/context 实现仍与 no-workspace 声明冲突；两项必须在重新执行 Phase 2 check 前修订并验证。
- 主 SSOT：`trellis/workflows/guru-team/workflow.md` 定义 Guru Team 流程；`finish-summary.schema.json` 定义机器合同；issue #97 定义产品范围和跨 issue 边界。
- task 文档只记录本次设计和执行证据，不替代 durable SSOT。
