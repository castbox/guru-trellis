# Issue #105 最终放行审查原始报告 Round 9

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round9`
- 独立性：未参与本任务实现、Phase 2 或 Round 1-8
- reviewed_head：`4f634a73d887016f9b25dc07a98de8a94d171aa4`
- diff_range：`origin/main...HEAD`
- reuse_decision：`new-agent`
- findings_count：`1`
- 结论：`fail`

## 审查范围

独立读取了 live Issue #105、`prd.md`、`design.md`、`implement.md`、planning approval、Docs SSOT Plan、五份 durable specs、canonical/dogfood workflow、README、平台入口、schema、companion、preset/overlay、完整 50 文件 diff、Phase 2、ledger、assignment 和 Round 1-8 原始报告。

重点检查 immutable plan/digest、draft PR identity、final projection、archive transaction、active/archive recovery、blob continuity、raw UTF-8 body、symlink/Darwin `/var` 边界、raw/effective remote transport、head repository、all-platform provenance、installed closeout、issue scope、安全与部署影响。

## 完整 Diff 结论

完整 diff 当前存在 1 项 P1，不能记录最终 Branch Review Gate pass。

### P1：archive move 后仍重新执行本地 artifact/body/summary validator

路径与证据：

- `.trellis/tasks/07-11-105-finish-work-closeout-transaction/prd.md:71` 要求 archive transaction 完成后不得再构建、校验或改写 repo artifact。
- `design.md:139` 明确规定 archive move 后不得调用 schema builder、ledger validator、body validator、summary rewrite 或 verifier；`design.md:143` 要求 ready 重试只执行 PR identity/HEAD 和 ready 切换。
- `guru_team_trellis.py:12052` 在官方 `task.py archive --no-commit` 已移动 task 后调用 `validate_closeout_archive_layout()`。
- `guru_team_trellis.py:11958-11961` 随后重新执行 final-summary schema/template、finish-summary、ledger 和 marketplace artifact/digest 校验。
- `guru_team_trellis.py:12087-12095` 在 archive commit push 后的 ready 阶段再次调用完整 PR identity validator。
- 该 validator 在 `guru_team_trellis.py:11701-11718` 重新读取 archived `pr-body.md`，校验 bytes、SHA-256、UTF-8，并重新执行 summary schema/template 校验；ready confirmation 在 `12115-12123` 再执行一次。
- archived recovery 在 `12183-12204` 也先重复 plan、body、summary 和 archive layout validator，再进入 HEAD/ready 恢复。

影响：

task 已经从 active locator 移走后，任何 archived body/summary/marketplace 文件读取或 schema/digest 错误，都可能使流程停在 archived-but-draft，重新引入 #105 要消除的 archive 后可预见本地失败。archive commit 已 push 后也可能因本地 artifact validator 失败而无法转 ready；同一入口重试会再次执行相同 validator，而不是仅恢复 remote identity/HEAD 和 draft-to-ready。

Docs SSOT 也未收敛：`workflow-contract.md:474-476` 与 planning 合同规定 exact archive commit 后只允许 push、HEAD、ready；但 `companion-scripts.md:137-142` 和 `data-contracts.md:128-133` 又要求 archived recovery/ready 重新校验 task-local body/summary identity。

修复建议：

- 所有 body、summary schema/template、ledger、marketplace 校验保留在 active final projection。
- archive move 后只校验 exact path set、tracked blob continuity、官方 `task.json` 差异、commit lineage、push 和三方 HEAD。
- ready/recovery 使用已绑定的 immutable PR facts和摘要，不再重新进入通用 artifact validator。
- 增加 spy/failure-injection，明确断言 archive move 后 summary、ledger、body validator 均不会再调用。

## 问题生命周期

- Round 1 的 4 项 P1：Round 2 closed。
- Round 3/4 的 head repository、local transport、raw/effective remote identity 链：Round 5 closed。
- Round 6 的 all-platform provenance、raw task-local body、installed closeout 3 项 P1：主体在 Round 7 closed。
- Round 7 ledger 缺 targeted `50/50`：Round 8 closed。
- Round 9 使用此前未出现的新 agent，freshness 规则满足；本轮新增上述 P1，当前保持 open。

## Phase 2 与测试证据

- `phase2-check.json.head` 等于 reviewed HEAD。
- Phase 2 记录 19 项 P1，均为 `resolved`；checked artifacts 覆盖规划三件套、ledger 与 Round 1-7，Round 8 为后续 closure metadata tail。
- 独立复跑 canonical：`384/384 pass`。
- 独立复跑 targeted closeout：`50/50 pass`。
- 独立复跑 preset：`36/36 pass`。
- `py_compile`、changed Bash syntax、JSON/JSONL parse、overlay drift、canonical/dogfood 与五平台入口 equality、`git diff --check` 均通过。
- 测试没有断言 archive move 后禁止再次调用本地 artifact validator，因此绿灯不覆盖本轮 finding。

## Issue Ledger

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`
- primary 与 close acceptance evidence 逐字一致。
- `384/384`、`50/50`、`36/36`、71 assets、initial #105、after-update #106 各唯一且完整。

## 开箱即用与 Upgrade/Update

- dogfood provenance：`claude/codex/cursor`、`all_platforms=true`、71 个存在且排序去重的 managed assets。
- `managed_backups=[]`、`new_copies=[]`，无 `.new/.bak`，overlay drift 为零。
- 本轮 throwaway 重跑 initial #105 完成 digest、formal、archive、ready、clean tree 和三方 HEAD。
- 后续 public marketplace preview 因 registry timeout 中断；Phase 2 已记录此前 initial #105 与 update/reapply #106 两轮完整通过。
- current-branch remote marketplace 和真实 GitHub E2E 仍应由 publish-time fail-closed verifier 承接。
- 远端不存在 `v0.6.5-guru.3`，不得声明该稳定 tag 路径已验证。

## 部署与安全

未修改 CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration 或 Makefile。配置变化仅涉及 Guru Team closeout publish 默认 draft 合同。

未发现真实 token、secret、private key、`.env`、客户数据或签名 URL。diff 中 credential/token 字符串均为 strict remote parser 的负向测试 fixture。

## 观察项

- 当前分支尚未 push、未建 PR。
- 本轮 throwaway update/reapply 尾段受外部 registry timeout 影响；不改变已确认的代码 finding。
- 官方 Trellis 文档确认流程判断应由 workflow Markdown 定义，脚本只执行确定性动作；当前 validator 的能力本身符合脚本边界，但执行时点违反 #105 的 archive 边界。

## 后续候选

0。唯一 finding 属于 #105 核心目标，不能拆为 follow-up。

## 结论

Round 9 最终放行失败。`findings_count: 1`，`reuse_decision: new-agent`。必须先移除 archive move 后的 body/summary/ledger/artifact validator，统一 durable Docs SSOT，并重新执行 Phase 2、finding closure 和 fresh 最终放行审查。
