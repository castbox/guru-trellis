# Issue #105 Branch Review Round 18 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round18`
- 独立性：未参与实现、Phase 2 或 Round 1-17
- reviewed_head：`d8bde831632c7e0e3141ae005fcea973092d8702`
- diff_range：`origin/main...HEAD`
- reuse_decision：`new-agent`
- findings_count：`6`
- 结论：`fail`

## 审查范围

只读审查了 live Issue #105、规划三件套及 approval、Phase 2、ledger、assignment、Round 1-17、完整 60 文件 diff、12 个 commit objects、canonical/dogfood/preset/overlays、平台入口、schema、测试与 durable docs。

重点覆盖 closeout 顺序、remote/raw identity、PR body/title/head/base/fork、summary URL/ref、archive path/tree/blob/lineage、exact/incomplete recovery、resolver/locator、history rewrite、安装/update/reapply、Docs SSOT、安全及部署。未修改文件，未运行 Guru Team recorder/gate，未 commit、push 或创建 PR。

## 发现项

### P1-1：history rewrite 后的审查 ledger 依赖不可移植的悬空 commit

证据：

- `agent-assignment.json` 的 Round 1-16 `reviewed_head`、reuse/status/assigned head 仍大量引用 rewrite 前 SHA。
- 除 base 与 `d8bde83` 外，这些 SHA 无任何 ref，仅因本机 branch reflog 尚未过期而可解析；`refs/original` 为空。
- 每个旧 tree 均能唯一映射到 rewrite 后链，例如 `b900a3c -> f1d47844`、`fda16dd -> 15343508`、`94d44d7 -> c48634c0`。
- `validate_agent_assignment_payload()` 要求每个历史 head 都能由 `git rev-parse <sha>^{commit}` 解析；review gate 会重跑完整 assignment 校验。

影响：当前机器暂时可通过，但 push 后 fresh clone、reflog 过期或 GC 后旧对象不会存在，`check-agent-assignment`、review gate 和 active closeout recovery 会失败。当前 gate evidence 不是可移植、长期可审计的证据。

修复要求：把所有生命周期 head 重锚到 rewrite 后等价 commit，并同步 raw report/assignment digest；或引入可移植的 old/new rewrite mapping 与不依赖悬空对象的 validator 合同。

### P1-2：普通 archived recovery 仍读取工作树中的 plan

证据：

- `cmd_finish_work` 只在缺少 task context 时进入 commit-blob plan-only boundary。
- 普通 archived task 保留 `task-start-context.json` 时，会直接读取并校验 archived working-tree `closeout-plan.json`，之后才识别 exact committed archive。
- 生产损坏测试的 `delete` 删除 context 后走 plan-only 路径；`tamper` 只破坏 body/summary；没有覆盖 exact commit + keep-context + plan 缺失/篡改。

影响：精确 archive commit 已存在时，本地 plan 缺失或篡改仍会在 remote PR binding/ready 前阻塞，违反“commit tree/blob 为权威、archive 后不再 artifact read/validate”。

修复要求：所有 archived exact recovery 都从当前 commit blob 读取 plan 并验证 dedicated boundary，不以 task context 是否存在决定 plan authority。

### P1-3：canonical workflow 的正式命令缺少必填 digest

证据：

- `trellis/workflows/guru-team/workflow.md` 前部主 helper 示例的正式命令没有 `--expected-plan-digest`；dogfood 副本逐字相同。
- 同一 workflow 后部和全部 finish entries 使用正确参数。
- 实现要求 formal digest 逐字匹配。

影响：AI 按 runtime workflow 前部明确命令执行时，formal finish 固定失败。Docs SSOT 内部存在两套不可等价入口。

修复要求：修正 canonical/dogfood 示例，并增加扫描所有正式 finish 命令均携带 digest 的回归测试。

### P1-4：tracked artifact 内容漂移只在 official move 后发现

证据：

- active projection 只比较文件名集合并校验 summary/marketplace，没有把所有 active tracked bytes、mode 与 evidence commit blob 比较。
- evidence commit 后若 `review.md` 等 tracked artifact 被改写，或某 tracked artifact 是 symlink，仍可进入 official archive。
- blob continuity 首次完整比较发生在 official move 之后；symlink 分支还会把 Git symlink blob 与跟随链接后的 `read_bytes()` 比较。

影响：本地可检测的内容/mode 漂移会重新形成 archived-but-draft，直接违反 PRD 的 pre-archive failure boundary。

修复要求：调用 `task.py archive` 前校验全部 tracked path 的 mode、regular-file 约束和 blob continuity，并校验 pre-move dirty set 只包含计划中的 final untracked output。

### P1-5：immutable archive month 与官方 archive 的实时月份可能分叉

证据：

- closeout plan 固定 prepare 时的当前 `YYYY-MM`。
- 官方 task archive 在真正 move 时重新读取当前月份。
- 月末跨零点或跨月中断恢复后，official move 会进入新月份，而 executor 在计划的旧月份查找 archive 并于 move 后失败。

影响：已提交 immutable plan 的 active task 可能没有合法恢复动作，且 task 已移动到非计划位置。

修复要求：在设计层统一 archive destination 的单一权威，补跨月 production recovery；不得让 plan 与 official executor 分别读取时钟决定路径。

### P1-6：官方 `after_archive` hook 未纳入 preflight 或事务合同

证据：

- companion 调用未修改的官方 archive。
- 官方 archive 在目录 move 后执行 `after_archive` hooks。
- plan 未绑定 `.trellis/config.yaml` 的 hook 配置，也未在 archive 前拒绝或约束该 mutation surface。

影响：现有项目若配置 repo-mutating `after_archive` hook，hook 产生的额外路径会在 move 后触发 layout/dirty allowlist 失败，再次留下 archived-but-draft。

修复要求：在 archive 前显式处理 hook 合同：禁止不受支持的 `after_archive` hook，或提供确定性、预验证且纳入 transaction allowlist 的执行模型，并补 installed/recovery 测试。

## 问题生命周期

Round 1-15 的既有 closeout、remote、installed、post-archive、locator/resolver findings，以及 Round 16 两项 P1，在其对应 closure 轮次均有证据关闭。独立复核确认：

- 12 个当前 commits 均有实质 `背景/变更/边界/验证` 和 `Refs #105`，结构检查 `errors=[]`。
- rewrite 前后均为 12 trees，顺序 digest 都是 `49ffd792ddb48d41fd99e28e4a4ebcef01355d8a31f3351b3affac665aebc78d`，最终 tree 相同。
- 五组 canonical/dogfood continue surfaces 逐字相等，Round 16 的旧 continue 语义已消除。

本轮六项是对当前最终 HEAD、恢复可移植性及 archive transaction 的新发现，不是旧 finding 降级或 follow-up。

## 验证证据

Phase 2 记录：canonical `404/404`、targeted `55/55`、locator `21/21`、preset `36/36`、installed initial #105/update #106、compile/Bash/schema/artifact/equality/overlay/sidecar 全部通过。

本轮独立只读核对：

- `git diff --check origin/main...HEAD`：pass。
- 60 files、12 commits；tree rewrite digest 与 commit body 合同如上。
- canonical/dogfood Python、workflow、三份 schema及十个 continue surfaces 一致。
- manifest 为 Claude/Codex/Cursor、`all_platforms=true`、71 项排序唯一且存在；无 `.new/.bak`。
- 当前未提交项仅 task metadata/reviews tail。

现有绿灯未覆盖本轮六项：悬空 SHA 的 fresh-clone validator、keep-context plan 损坏、workflow 前部命令、pre-move tracked blob/mode、跨月 archive、`after_archive` hook。

## Docs SSOT

官方 Trellis 文档确认 workflow 行为应由 `.trellis/workflow.md` Markdown 定义，marketplace/preset 是正确扩展面；本分支未修改 upstream/npm/node_modules。

但 P1-2 与 durable “commit blob authority”冲突，P1-3 是 workflow 内部命令冲突，P1-4 至 P1-6 使“archive 前消除本地可预见失败”不成立。Docs SSOT：`fail`。

## Ledger 与范围

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`
- primary/close acceptance evidence 一致，分类正确。
- “exact commit 不依赖本地 archived artifact”和“全部本地错误在 archive 前失败”的验收声明被本轮 findings 反证，当前不得关闭 #105。

## 部署与安全

无 CI/CD、Docker、Compose、K8s/Kustomize、Helm、migration 或 Makefile 变更。未发现真实 token、secret、private key、`.env`、客户数据或签名 URL；credential URL 仅为拒绝测试 fixture。

本轮问题属于 closeout 完整性和恢复可移植性，不构成新的 secret 泄漏，但会阻塞可靠发布。

## 观察项

- 远端尚无 `fix/105-finish-work-closeout-transaction` branch。
- 远端不存在 `v0.6.5-guru.3`；不得声明 stable-tag 安装已验证。
- current-branch remote marketplace 与真实 GitHub E2E 仍只能由 publish-time fail-closed verifier 承担。
- dogfood manifest 的 `source.commit=94d44d7`、`tree_state=dirty` 是 apply 时观测，不是本轮 finding。

## 后续候选

0。六项均属于 #105 核心事务、恢复或发布门禁范围，不得降级为观察项。

## 结论

Round 18 最终放行不通过。

- P0：`0`
- P1：`6`
- P2：`0`
- P3：`0`
- findings_count：`6`
- reuse_decision：`new-agent`

必须修复以上问题、重新执行完整 Phase 2，并由本 agent 仅以问题闭环审查代理复核；闭环后还需派发新的 fresh 最终放行审查代理。
