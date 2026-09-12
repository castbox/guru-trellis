# #329 技术设计

## 1. 版本与来源身份

唯一 framework source：

```text
repository: https://github.com/castbox/Trellis.git
commit: a2003296b4c4ce46c50d72ead3b2ec9c317f69fc
cli_version: 0.6.17
package_manager: pnpm@10.32.1
```

`trellis/presets/guru-team/source/trellis-source.json` 是 canonical lock；构建、安装、update、
source validation 和 installed projection 只消费这一份 authority。固定 checkout 自身安装依赖并
build 后直接运行 `packages/cli/bin/trellis.js`，继续使用现有 `.guru-source-commit` 证明 dist 与
实际 HEAD 对应。任何 prepare/fetch/build/version/marker 失败均停止，不回退全局或 npm CLI。

本 task 更新 framework/CLI 轴，不顺带发布新 Guru repository tag。当前 Guru extension revision
`0.6.16-guru.41` 在未进入独立 release preparation 前保持独立；公开文档区分“latest released
Guru tag”与“main/source checkout 当前固定 framework”。

## 2. Ownership 与更新顺序

### 2.1 Trellis-owned managed files

`.trellis/scripts/**`、`.trellis/config.yaml`、`.trellis/workflow.md` 中由官方 template hash 管理的 stock
platform hooks/skills/commands、template hash 和其它 framework-generated assets 由固定
`0.6.17` CLI 的正式 `update --migrate` / generation 结果拥有。实现不得手工重造或长期 patch
这些文件。

上游 `init_developer.py`、`get_developer.py`、`add_session.py` 在 `0.6.17` 仍可作为 retired
command stub 存在；Guru 只验证其明确拒绝/迁移提示，不调用、包装或恢复旧功能。

### 2.2 Guru-owned canonical files

Guru source lock、preset installer、ownership inventory、workflow/Skill contracts、package runtime、
fixtures、README 和平台 overlays 在 canonical `trellis/**` 下直接演进。之后运行 preset reapply
同步 `.trellis/guru-team/**`、`.agents/.codex/.claude/.cursor` 的 Guru-owned installed copies，
再执行 drift 和 sidecar 校验。

任何 active Guru consumer 一旦失去旧机制职责，同步删除其配置、schema 字段、fixture、测试和
current docs；不增加 compatibility wrapper。历史 archive、superseded RDT/Architecture、release
记录和 Git history 保持不变。

## 3. Identity-free task lifecycle

### 3.1 Current task resolution

current task 由以下 facts 闭合：

1. 当前 checkout 的 Git common-dir、branch 与 live worktree path；
2. active `task.json` 的 id、branch、base branch 与 `worktree_path`；
3. ignored Guru workspace/task mappings；
4. task-local issue scope ledger；
5. entry contract 明确要求且 caller 已提供的显式 task selector。

`.trellis/.developer`、`TRELLIS_DEVELOPER`、journal 或“唯一 assignee/task”均不参与选择。
`source_checkout` 只表示 mapping provenance，不单独绑定 task。缺失或冲突继续返回
`invalid_task_state`，不通过旧 identity 猜测或修复。

### 3.2 Creator、assignee、owner、actor

- 新 task：owner executor 必须把已审阅 assignee 同时作为显式 creator/assignee 传给
  `0.6.17` official task store；移除 call-scoped `get_developer` monkeypatch。
- 无 Issue assignee：repo access preflight 通过时，owner executor 使用当前 authenticated GitHub login；
  preflight 未通过或 login 为空时，在写入前返回显式 owner 输入要求。这是明确 caller authority，不是
  隐藏全局 fallback。
- CLI/filter：受控调用改为 `--assignee <name>`；不继续使用 `--mine`。
- 已有 task：读取 metadata 即可，不要求重新提供 person identity。
- 无法解析的新写入：在 mutation 前返回明确输入要求。

### 3.3 Guru task workspace 命名边界

Guru package 中的 `workspace_slug` / workspace mapping 表示“task 的隔离 checkout/worktree”，
不是旧 `.trellis/workspace/<developer>/journal-*`。现有稳定 public Skill id 与 typed exit 不变；
contract、schema description 和 README 必须显式区分两者。

owner result 中只为证明“未创建 legacy identity/journal”而存在、且没有下游 consumer 的
`source_developer_identity_created`、`target_developer_identity_created`、
`workspace_journal_created` 字段退出 current schema/runtime。若 schema id 需要变化，使用显式新版本并
同步所有受控 consumers；不维持双 runtime path，也不静默改变旧 schema 语义。

## 4. Legacy 数据保留

在 update/reapply/installer/transaction/verification 前对以下 root 建立 byte/mode/path snapshot：

- `.trellis/.developer`；
- `.trellis/workspace/**`；
- `.trellis/agent-traces/**`；
- 现有 `.gitattributes` 文件，以及位于上述 roots 内的用户文件。

这些 root 从 staging copy、scan、migration、removal、restore、index、context 和 owner resolution
全部排除。验证后比较文件集合、symlink identity、mode 与 bytes。absent fixture 保持 absent；
present-A/present-B 的不同内容不得改变同一 task/Git/caller authority 下的结果。

## 5. Installer 与迁移数据流

### Clean install

固定 source checkout build -> 固定 CLI `init`（显式 creator/assignee 仅在 init 创建 bootstrap
task 时提供）-> marketplace workflow -> Guru preset apply -> source/installed validation ->
platform session/task lifecycle probes -> recursive sidecar scan。

### Existing update

保存 legacy 与用户修改 snapshot -> 固定 CLI update preview/migration plan -> 审核 active managed
removals/conflicts -> 仅当 migration plan 声明 task ownership migration 时执行
`update --force --migrate --assignee <explicit> --skip-all` -> workflow preview/force
按同一 provider 应用 -> 同平台 Guru preset reapply -> installed validation -> legacy byte comparison ->
第二次 update/reapply 重复应用一致性验证。

Guru installer 删除“主动添加 `.trellis/workspace/` ignore”和 session-recording config 的 current
责任；不得删除用户已有 ignore/attributes/history。`task_auto_commit` 取代 active
`session_auto_commit` 语义，legacy 配置仅按 upstream archive compatibility 读取，不启用 recording。

## 6. 验证设计

### 6.1 Source 与静态门禁

- fixed commit/remote/version/package-manager/source-marker；
- upstream ownership、managed inventory、schema/interface/public graph；
- canonical/dogfood/installed/platform byte parity；
- retired API 调用扫描按 production/test/generated/current-doc/history 分类；
- Python/Bash/JSON/schema、task validation、`git diff --check`、3000-line touched source review。

### 6.2 三平台 lifecycle matrix

Codex、Claude、Cursor 各执行：clean install、existing update、reapply、linked worktree、new session、
resume、task creation、planning context、Phase 2 entry/check、commit/review/publication/finalization/archive
代表入口。真实 GitHub mutation 使用 fixture provider；本 task 不创建远端 PR/merge/tag/release。

每个平台固定覆盖 legacy absent 与一个 legacy present fixture；跨平台共享 deterministic matrix
补充 present-A / present-B 的结果一致性和 byte preservation。所有入口必须使用 target checkout
的 managed runtime，不以
source interpreter 或全局 CLI 替代。

### 6.3 结果分层

分别记录：upstream source build、Trellis-generated adoption、Guru unit/focused、installed matrix、
live remote facts、未验证 release/business smoke。任一层失败不能被另一层 PASS 覆盖。

## 7. Docs SSOT Plan

策略：`ssot_first`，但遵守 Architecture/RDT single-writer promotion。

1. 在首次 runtime 修改前形成 task-local RDT 与 Architecture contribution candidate，明确
   `R329/D329/T329`、source mapping、identity-free lifecycle、legacy preservation 和 task-worktree
   authority；不直接把 planning 文本写成 shared current。
2. 同步 durable Guru specs：workflow contract、data contracts、companion scripts、quality guidelines、
   skill package contract、preset installer/upstream ownership/public docs。
3. 同步 public README、workflow README、preset README 和 current-vs-released version说明；历史
   release/archive/superseded docs 不批量改写。
4. 实现与验证完成后由 RDT/Architecture owner 审核 contribution；需要 shared current 变化时走
   serialized promotion，promotion-created diff 重新进入 Phase 2、commit 与 full-diff Branch Review。

## 8. 架构影响

预期为 `architecture_contribution_required`，不是 `no_architecture_impact`：framework source binding、
task identity source、upstream/Guru ownership、distribution migration 和 lifecycle verification 均改变
CURRENT architecture。贡献不得改变既有 23 Skills / 97 exits 的业务图，除非 live implementation
证明某个 current schema/command inventory 必须显式迁移；任何 graph/API 变化必须单独列出
before/after 与 consumer migration。

## 9. 回退边界

回退只针对本 task candidate；不 reset 其它 worktree，不恢复旧 #329 patch/stash，不删除 legacy
数据。upstream update 或 preset activation 失败时保留旧 checkout/installed state 与 sidecar 证据，
修复原因后从固定 source 重新生成，不能手工拼接 mixed `0.6.16/0.6.17` runtime。
