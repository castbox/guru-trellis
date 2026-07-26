# Issue #117 BR-117-F10 Fresh Phase 2 检查报告

## 检查完成

### 检查身份与边界

- 角色：独立 `trellis-check` 阶段二检查代理
  `/root/issue117_phase2_check_f10`。
- Task：`.trellis/tasks/07-25-117-verify-extension-installation`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/117-verify-extension-installation`。
- Branch：`feat/117-verify-extension-installation`。
- 检查时 committed HEAD：
  `a47e1fbd7bedb001649814969096076bb70157db`。
- Base 与 merge base：`origin/main`，
  `0cd2498f821b38ce91bd82fa9e232b1528241e5d`。
- 检查范围：完整 `origin/main...HEAD` committed range、当前 BR-117-F10
  working-tree implementation、task lifecycle metadata、durable docs 与安装后资产；
  `git diff origin/main` 终态为 336 files changed、57,461 insertions、3,431
  deletions。本轮没有只审查最新 runtime hunk，也没有复用旧
  `phase2-check.json` 的语义结论。
- 本代理唯一写入本报告。未修改 implementation、tests、contracts、
  `phase2-check.json`、`agent-assignment.json`、review gate、task commit plan 或
  publication artifact。
- 未执行 commit、push、PR、Issue closure、finish-work、release 或 production
  publication。

Fresh startup gate：

- workspace boundary 通过；expected workspace 与 actual repo root 均为当前
  Issue #117 worktree，source checkout clean，suspicious source artifacts 为 0；
- planning approval 为 schema `2.0`、`typed_exit=approved`、
  `explicit-post-planning-review` provenance，包含 passed ambiguity review、
  fixed-scope scanner evidence，且三份 planning document digest 仍匹配；
- `check.jsonl` 无 curated file row，因此按 fallback 读取 task artifacts，并通过
  `get_context.py --mode packages` 展开适用 workflow、preset、Docs SSOT、quality
  与 public Skill contracts；
- 当前角色为 Phase 2 check，不是 Branch Review；旧 review artifacts 保持原样。

### 已检查文件

- Task planning 与 scope：`prd.md`、`design.md`、`implement.md`、
  `planning-approval.json`、`issue-scope-ledger.json`。
- Implementation/check handoff：`implementation-handoff.md`、旧
  `phase2-check.json`、`agent-assignment.json`、task commit plans 与 review
  lineage。
- Canonical 与 installed runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py` 及 runtime tests。
- Canonical 与 installed native eval adapter：
  `trellis/skills/guru-team/adapters/eval/native_adapter.py` 与 installed copy。
- Canonical、installed、Agents、Codex、Claude、Cursor 六处
  `guru-verify-extension-installation` package，重点检查 `interface.json`、
  `references/contract.md`、private schemas、examples、wrappers、eval corpus 与
  package contract tests。
- Canonical/installed registry、consumer/target graph、extension manifest、preset
  installer、overlay ownership inventory 与 platform distribution。
- `.trellis/spec/workflow/{index,quality-guidelines,skill-package-contract,
  companion-scripts,workflow-contract}.md`。
- `.trellis/spec/preset/{installer,upstream-ownership,
  overlay-guidelines}.md`、`.trellis/spec/docs/public-docs.md` 及 cross-layer / code
  reuse guides。
- `README.md`、workflow/preset README 与 `docs/requirements/**` durable owners。
- Retained throwaway target：
  `/tmp/issue117-f10-check-throwaway-local.TYnIdX/project`。

### Scope-first finding qualification

| 候选 | 受支持正常路径资格 | 结论 |
| --- | --- | --- |
| F10 installed evidence 只证明命令退出，未证明已安装资产完整性 | 原 finding 可在正常 executor/throwaway 路径复现，不依赖 artifact 篡改或恶意输入；属于 approved BR-117-F10 current scope | 当前实现已建立 canonical expectation、installed digest、manifest relation、category/platform 与 capability evidence 闭环；不再构成 finding |
| Collector 自身没有枚举任意额外文件 | Collector 的 `asset_digests` 按 canonical expectations 遍历；完整 `verified` 路径同时强制 installed package validator，后者对 managed/package/platform unexpected、sidecar、conflict、removal fail closed | 记录为分层观察，不是 qualified finding；不得声称 collector 单独完成全目录 arbitrary-extra scan |
| Exact pushed feature-ref 尚未安装验证 | 当前没有 commit/push 授权，不能形成 exact remote branch-ref evidence | publication 后置证据，不是本地 implementation finding |

未发现新的 `normal_required_behavior`、`existing_supported_behavior` 或
`newly_accepted_scope` candidate；qualified finding、scope proposal 与 blocker 均为
0。

### 已修复问题

本检查代理没有执行自修复。实现候选已满足 BR-117-F10：

- Throwaway verifier 接受显式 work root，installed bytes 只从 retained
  `<work>/project` 读取；
- expectation set 绑定 canonical source path、installed path、relation、category、
  platform 与 expected SHA-256；
- 资产类别为 workflow 1、preset 6、schema 4、Skill 44、platform 176，共 231；
- relation 为 canonical workflow 1、managed manifest 10、Skill manifest 44、
  platform manifest 176；
- missing、duplicate、digest mismatch、manifest relation error、platform selection
  error、unknown command/asset reference 与 capability 空 evidence 均 fail closed；
- 每个 selected capability 都必须同时持有 stable `command_refs` 与
  `asset_paths`；
- semantic applicability、finding、retry/re-entry 与最终 route 仍由 AI owner
  判断；runtime 只执行、记录、校验并投影最小 public DTO；
- workflow/standalone 输入、四个 typed exits、public output schema 与 consumer
  mapping 未扩张。

### 未修复问题

没有需要返回实现的 current-scope Phase 2 finding。

以下为授权或环境边界，不是实现缺陷：

- Exact pushed feature-ref clean install 必须在后续获准 push 后绑定实际 remote
  ref/HEAD 执行。本轮 local unpublished workflow sample 不能冒充该证据。
- Cursor native command 在当前 adapter capability contract 下返回 7/7
  `unsupported`，没有伪造 passed；Cursor package bytes、manifest relation 与安装
  资产已由 distribution、installed validator 和 throwaway 验证。
- 当前 extension manifest 如实记录 dirty source provenance；后续 commit/apply
  应重新绑定最终 commit。
- 本报告不授权 `phase2-check.json` recorder、task commit、push、PR、Issue #117
  closure、finish-work 或 release。

## 验证结果

### Semantic adequacy

| 维度 | 结论 | Fresh evidence |
| --- | --- | --- |
| Requirements/design | 通过 | F10 收敛 installed completeness 与 capability evidence，不扩大 Issue #117 public 行为 |
| Runtime correctness | 通过 | full runtime 600 passed、13 skipped；完整 success/partial/missing/duplicate/mismatch/relation/capability 负例覆盖 |
| Public Skill contract | 通过 | public DTO、四 exits 与 consumer mapping 未扩张；六处分发 package 相同 |
| Installed inventory | 通过 | expected/observed/matched 231；1/6/4/44/176 五类完整；所有 error arrays 为空 |
| Registry/graph/schema | 通过 | source/installed 均 12 active Skills、46 exits、27 targets、0 legacy |
| Preset/ownership | 通过 | 54/54 tests；43 frozen/active、13 claims、54 managed assets、0 errors |
| Distribution | 通过 | canonical/installed/shared/Codex/Claude/Cursor package byte-identical；runtime 与 native adapter canonical/installed 相同 |
| Production eval | 通过 | Shared/Codex/Claude source+installed 各 7/7 passed；Cursor source+installed 各 7/7 unsupported |
| Install/update/reapply | 通过 | full local-source throwaway exit 0；覆盖 discovery、init、preview/switch、update、reselect、reapply、recovery、no-developer 与 final checks |
| Docs SSOT | 通过 | `ssot_first`：package Interface/contract/private schema/examples 已承接 F10，installed/platform copies 与 runtime/tests/manifest 一致 |
| Security/redaction | 通过 | 高风险 token pattern 只命中 detector literal、合成负例与旧去敏 evidence 说明，未发现真实 secret/credential |
| Deploy/compatibility | 通过 | 无 dependency、CI/CD、container、Compose、K8s/Helm/Kustomize、DB migration、Makefile 或 production config 变化 |

Lint：通过。

- `bash -n`、changed JSON parse、Python compile 均通过。
- `git diff --check origin/main` 与 `git diff --check` 均通过。
- 递归 non-fixture `.new` / `.bak` 扫描为 0。
- dogfood overlay drift 通过。

TypeCheck：不适用。

- 仓库没有为该 Python runtime 配置独立 `mypy`、`pyright` 或等价 owner。
- 生产 Python 入口由 `py_compile`、full unittest、schema/package validator 覆盖。

Tests：通过。

- Runtime：600 passed，13 skipped。
- Preset 与 ownership：54/54 passed。
- Skill integration：175/175 passed。
- 12 个 canonical package contract：114/114 passed。
- Verifier package contract：canonical 9/9、installed 9/9 passed。
- Full local-source throwaway：exit 0。

### Production eval matrix

Corpus SHA-256：
`0f4967559f92793964a3859d0158268d179fffcebb973b1715f356e0bde9535d`，
共 7 cases。

| Distribution | Adapter | 结果 | 备注 |
| --- | --- | --- | --- |
| source | shared | 7/7 passed | public invocation 与四 exits 匹配 |
| installed | shared | 7/7 passed | installed corpus/package path |
| source | codex | 7/7 passed | 无 auth、transient 或 execution error |
| installed | codex | 7/7 passed | 无 auth、transient 或 execution error |
| source | claude | 7/7 passed | outer runner 移除 inherited `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_BASE_URL` |
| installed | claude | 7/7 passed | clean-env，无 auth、transient 或 execution error |
| source | cursor | 7/7 unsupported | 符合当前 native adapter capability contract |
| installed | cursor | 7/7 unsupported | 未进入交互，不记作 passed |

Codex/Claude 四组 actual exits 均依次为：

1. `workflow-required-verified` -> `verified`
2. `workflow-applicability-conflict-blocked` -> `blocked`
3. `standalone-not-required` -> `not_required`
4. `task-install-finding-return` -> `return_to_task_work`
5. `standalone-remote-unavailable` -> `blocked`
6. `workflow-transient-retry-verified` -> `verified`
7. `workflow-stale-plan-reentry-verified` -> `verified`

首 case 的 `public_invocation_only`、`evals_not_loaded_by_skill`、
`private_runtime_not_read_by_agent` 三个 trace invariants 在 Codex/Claude
source/installed 四组均通过。

### Throwaway 与资产盘点

执行：

```bash
TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 \
  trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh \
  /tmp/issue117-f10-check-throwaway-local.TYnIdX
```

结果 exit 0，终态明确为：

```text
Verified public marketplace discovery plus local unpublished workflow sample at /tmp/issue117-f10-check-throwaway-local.TYnIdX/project
```

覆盖：

- public marketplace discovery 与 current-worktree local workflow sample；
- clean init、initial preset apply、existing project preview/switch；
- `trellis update --force`、workflow reselect、preset reapply；
- initial/post-update closeout recovery 与 task workspace probes；
- no-developer preservation 与 pre-146 recovery；
- source/installed package、ownership、publication wrapper smoke、eval 与 final
  zero-sidecar checks。

默认不带 allow flag 的 fresh probe 先按合同 fail closed，因为 dirty feature branch
若直接使用 `gh:castbox/guru-trellis/trellis#main` 会采样错误版本；该 probe 未触碰
仓库。受支持的 allow 模式只把远端用于 public discovery，并用当前 worktree bytes
覆盖实际 workflow sample。

Retained target 的 F10 collector fresh 结果：

| Category | Expected | Observed | Matched | Complete |
| --- | ---: | ---: | ---: | --- |
| workflow | 1 | 1 | 1 | true |
| preset | 6 | 6 | 6 | true |
| schema | 4 | 4 | 4 | true |
| skill | 44 | 44 | 44 | true |
| platform | 176 | 176 | 176 | true |
| Total | 231 | 231 | 231 | true |

- expected set SHA-256：
  `d46066d8ef62a06c7438bd311ce28c566b48899e481732956fe4e78b4c0d62eb`；
- `missing_paths=[]`、`duplicate_paths=[]`、`unexpected_paths=[]`、
  `mismatched_paths=[]`、`relation_errors=[]`；
- installed package validator：2322 managed files，0 sidecar、0 removal、0
  conflict。

### Final sanity

- workspace boundary：通过；source checkout clean，suspicious artifacts 为 0；
- planning approval：`typed_exit=approved`，current planning digests valid；
- task validation：通过；
- source/installed package validation：通过；
- canonical/installed/Agents/Codex/Claude/Cursor verifier package equality：通过；
- canonical/installed runtime 与 native adapter equality：通过；
- final non-fixture `.new` / `.bak` scan：0；
- final whitespace checks：通过；
- credential sanity 共命中 10 个已知测试/检测/evidence marker：runtime detector
  canonical/installed 各 1、runtime tests 6、旧 phase2/review evidence 各 1；未发现
  credential value、private key、signed URL 或 userinfo URL。

## 证据交接

### 阶段二

本报告覆盖 approved PRD/design/implement、完整 committed+dirty diff、F10
candidate、task/review lineage、runtime、public/private contract、schema/manifest、
preset/ownership、六处分发、production eval、Docs SSOT 与 full throwaway。

Scope-first 结论：F10 的 supported normal path 已由真实 retained install target 与
231 项双向 inventory 证明；capability 同时绑定命令与资产证据；失败路径 fail
closed；没有新的 current-scope finding、scope proposal 或 blocker。

本报告包含足够的 semantic coverage、命令结果、Docs SSOT reconciliation 与开放
边界，可支撑主会话后续记录 fresh `phase2-check.json`；本代理没有写该 artifact。

### Docs SSOT

- Plan strategy：`ssot_first`。
- Durable owners：canonical verifier `interface.json`、
  `references/contract.md`、private schemas/examples 已承接 F10 expectation、inventory、
  relation 与 capability evidence 语义。
- Distribution：installed、Agents、Codex、Claude、Cursor copies 与 canonical bytes
  相同；runtime、tests、manifest 与 durable contract 一致。
- Task artifact：`implementation-handoff.md` 已记录 task-specific delta、验证结果、
  exact pushed ref follow-up 与 no-update reason。
- Higher-level `.trellis/spec/` / README 无需更新：F10 未改变 stable Skill id、public
  I/O、typed exits、consumer route、安装命令或用户行为；其既有 ownership 与
  install/update 合同继续成立。
- Exact pushed feature-ref evidence 是 publication 后置验证，不是 durable docs 缺口。

### 部署与安全影响

- 部署：无 production deploy、release、service restart 或 data migration。
- 配置：更新 extension manifest 的真实 dirty-source provenance 与 package-private
  schema/examples；无新用户配置键、环境变量合同或 public API。
- CI/CD、container、Docker Compose、Kubernetes、Helm、Kustomize、DB migration、
  Makefile、dependency manifest：无变化。
- 安全：新增逻辑只处理 repo-local canonical/installed asset path 与 SHA-256；没有
  credential、客户数据、private replay 或 production write。SHA-256 用于正常版本
  绑定与 stale/mismatch 检测，不宣称 hostile-input authenticity boundary。

### Recommendation

`pass`。建议主会话以本报告为 semantic evidence 记录并校验 fresh
`phase2-check.json`，随后按现有 workflow 进入 task commit / independent Branch
Review；exact pushed feature-ref 验证须在获得 push 授权后单独完成。

## 结论

BR-117-F10 Phase 2 检查完成。Lint、适用的 compile/schema/validator、tests、native
eval、full local-source throwaway、231 项 installed asset inventory、Docs SSOT 与
final sanity 均通过；未发现需要返回实现的 current-scope 问题。
