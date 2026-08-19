# #266 Bootstrap guru-trellis 当前双 SSOT 与架构基线

## 目标

在 `castbox/guru-trellis` 当前 `main` 上，真实执行
`guru-bootstrap-repository-ssot:existing_repository`，建立并激活唯一、按版本组织的：

- Requirements SSOT；
- Design SSOT；
- Test Strategy / Test Plan SSOT；
- Architecture Baseline SSOT；
- 面向 Trellis Agent 的最小 `.trellis/spec` locator/index/使用规则投影。

本 task 只交付仓库文档与 Spec 基线，不改变 runtime/product 行为，不改变任何公共
Skill、schema、typed exit、consumer 或命令身份。

## 实时基线与 provenance

- `source_confirmed`：2026-08-19 intake 时 `origin/main` 为
  `3c0d4a2ffe4799eb67f4c5b1c33d8f8a36f61875`，PR #280 已合并，Issue #265 已关闭。
- `source_confirmed`：最新稳定 GitHub Release/tag 为 `v0.6.5-guru.9`；其 peeled commit
  为 `56b5f411e533b200e4d8685ca7a2ffb0c778a7f5`。
- `source_confirmed`：current extension manifest 为 `0.6.5-guru.35`，目标/已测试
  Trellis CLI 仍为 `0.6.5`。
- `source_confirmed`：#263、#264、#265 均已 Closed；#265 merge commit 是当前 base。
- `code_recovered`：current source 已包含 Requirements/Design/Test、Architecture
  Baseline、Bootstrap 三个 active package 及其 workflow/spec projection contract。
- `unverified`：#263/#264/#265 的历史 focused evidence 必须从各自 merged source、归档
  task、finish-summary、PR 与命令结果 fresh 回读后才能写入 Test Plan；旧摘要不能自动记为 PASS。
- `unverified`：完整多平台 Throwaway、v0.6.15 upgrade/update 与 exact candidate release
  matrix 未由本 task 执行，分别保留给 #260/#267；#275 另行拥有 replacement-release gate。

## 必需范围

### Requirements

按 current version 建立目标、角色、适用 repository、非目标、官方 Trellis/Guru ownership、
完整 workflow lifecycle、task/history/naming/docs/base/provider recovery、安装与多平台入口、
业务并行约束、当前发布范围、兼容边界、known gaps、版本矩阵与 traceability。

### Design

建立 canonical/installed/dogfood/platform 分层、global workflow/step-local Skill 分层、
public I/O/private state、AI semantic/deterministic runtime 边界、task/workspace/runtime/history
数据 ownership、distribution/installer/overlay architecture、关键 sequence、capability owner map、
schema/API compatibility 与 Requirements -> Design -> Test 追踪。

### Test

建立 static/unit/integration/throwaway/live/external 证据分层，覆盖 package/runtime、
source/dogfood/installed/platform equality、workflow/registry/interface/schema/typed-exit closure、
历史 focused evidence、业务并行、task/history/archive/naming/docs/baseline、provider recovery、
upgrade/release gate 与 known skipped/unverified evidence。

### Architecture Baseline

建立并严格分离 FOUNDATION、CURRENT、TARGET、DOMAIN、INTEGRATION、GAP、GOVERNANCE、
PLAN、ADR 与 EVIDENCE。CURRENT 只包含 current code/config/test/release 已证明事实；
v0.6.15 与 Phase-owner 重构只能进入 TARGET/GAP/PLAN，不得冒充 CURRENT。

### Spec 投影

建立或更新逻辑等价的：

- `.trellis/spec/docs/index.md`
- `.trellis/spec/docs/requirements-design-test-ssot.md`
- `.trellis/spec/architecture/index.md`
- `.trellis/spec/architecture/baseline-usage.md`

投影只保留 authority locator、version/status/scope、读取顺序、traceability、task 更新规则、
typed route 和 freshness，不复制 docs 正文，不形成第三 authority。

## Docs SSOT Plan

- strategy：`bootstrap_or_repair_docs`。
- canonical authority：`docs/requirements/`、`docs/design/`、`docs/test/`、
  `docs/architecture/`。
- current version：以 current source as-built 版本建立 active current entry；released
  `v0.6.5-guru.9` 作为明确历史/released baseline，不与 current main 混同。
- migration：现有 `docs/requirements/{README.md,requirement-main.md,guru-team-trellis-flow.md}`
  内容被吸收、引用化或标记历史边界；不得保留第二套 current authority。
- projection：`.trellis/spec` 仅维护最小索引/使用规则。
- parallel rule：Bootstrap 后普通并行 task 不直接写 shared current docs/spec index，后续变更
  由 #263/#264 task-impact/contribution/promotion owner 处理。
- task history：本 task planning/check/finish artifact 只保留任务证据，不成为长期产品 authority。

## 约束与非目标

- 所有正文使用中文，稳定技术标识、命令、路径、API/GitHub keyword 可保留英文。
- 事实必须标记 `source_confirmed`、`code_recovered`、`inferred` 或 `unverified`。
- 不执行完整多平台 Throwaway 或 exact release-candidate matrix。
- 不升级 Trellis v0.6.15，不发布 tag/Release，不修改其它 Issue body，不创建 repair Issue。
- 不开始 #275/#260/#267，不实施 #247/#249/#250/#261/#248/#252。
- 不修改 upstream/global npm/node_modules，不引入锁、TOCTOU、攻击模型或 shared ledger。

## 验收标准

- [ ] 四套 canonical authority 均有唯一 README/current entry/version/status/history navigation。
- [ ] released `v0.6.5-guru.9`、current main as-built 与未来 TARGET 清晰分离。
- [ ] capability inventory 覆盖 current active Skills、typed exits、schemas、commands、platform routes
  与 managed assets，并由 live registry/interface/manifest 派生。
- [ ] Requirements -> Design -> Test traceability 完整且与 Architecture Baseline 不冲突。
- [ ] CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE 无语义串位。
- [ ] 初始恢复 provenance 诚实，未把代码、旧 Issue 或历史测试误写成 confirmed intent/PASS。
- [ ] 现有分散 docs 已吸收、引用化或历史化，不存在双 current authority。
- [ ] `.trellis/spec` 仅为最小 projection，路径、链接、读取顺序和 freshness 有效。
- [ ] 文档无 placeholder、空标题、断链、失效路径、过期命令或未标记历史内容。
- [ ] fresh focused evidence 精确绑定 #263/#264/#265 source/HEAD/命令/结果与未验证边界。
- [ ] Issue-owned docs/spec/link/structure/dogfood-context checks 全部通过。
- [ ] 独立 Branch Review 覆盖完整 `origin/main...HEAD` docs/spec diff 且无 blocking finding。
- [ ] task 可被 index/history query 发现，并在 merge 后按完整 Finish/archive/cleanup 门禁收口。
- [ ] diff 不含 runtime/product/public Skill/schema/exit identity 变更。
