# 统一 Guru Team GitHub 操作通道为 gh CLI 并禁止 App/MCP fallback

## Goal

将已认证的 GitHub CLI 固化为 Guru Team 所有 GitHub 平台 live read、semantic evidence、mutation 与 recovery 的唯一执行通道，消除 GitHub App、MCP、connector、浏览器 UI 与隐式平台上下文造成的权限、字段和恢复语义漂移，同时保留 AI semantic judgment 与确定性 CLI fact/execution 的职责边界。

## Confirmed Facts

- Issue #179 已由 PR #193 合并，Issue #191 已由 PR #192 合并；Issue #180 仍为 Open 并明确等待 #181。
- 当前主线基线为 `cd6a948671ef761f79c53db551e3d5120cc41559`，任务使用专用 branch/worktree，Issue #181 是唯一 close scope，Issue #180 仅为 related downstream。
- shared companion runtime 已直接调用 `gh auth status`、`gh issue`、`gh pr` 与 `gh api`，但 durable workflow/spec 尚未定义统一通道、repo binding 和精确 failure taxonomy。
- 当前 canonical/discovery copies 中仍有 `existing GitHub connector` 等 fallback wording；平台 overlay 与 README 需要同步治理。
- `git` 继续拥有本地 Git、fetch、push、ls-remote 与 Git transport；本需求不以 `gh` 替代它们。

## Requirements

1. 在 durable workflow spec 建立单一 GitHub I/O SSOT：Guru Team GitHub 平台操作只允许已认证 `gh`/`gh api`，禁止 App、MCP、connector 与 browser UI fallback；各 Skill 引用该合同，不复制局部政策。
2. 高层命令能够完整表达时使用 `gh issue`、`gh pr`、`gh run` 等；否则使用 `gh api`，且不得切换到其它平台 adapter。
3. 每次 GitHub live 操作显式绑定 repository：高层命令包含 `--repo owner/repo`，REST 调用使用完整 `repos/<owner>/<repo>/...` endpoint；mutation 继续绑定目标 number、base/head 与适用 expected SHA。
4. entry/preflight 同时校验 CLI availability、`gh auth status` 与目标 repo 实际访问能力；CLI missing、auth、permission、API unavailable、response incomplete 分别进入精确 failure/recovery，不 fallback、不误报成功、不泛化为 `verification_required`。
5. runtime 只把 exit code、stderr classification 与 JSON/API fields 作为确定性事实；readiness、scope、finding、close semantics 与 route 仍由相应 AI semantic Skill 拥有。
6. 覆盖 Issue/PR create/read/edit/comment/labels/state、checks/reviews/mergeability/base/head、Draft/Ready、merge、workflow run/check 与 post-merge status verification 的 CLI-only 正常路径。
7. 增加结构化/static guard 与 deterministic fixtures，阻止 canonical、installed、preset/platform surfaces 重新引入 forbidden adapter/fallback wording，并验证 repo binding、expected SHA、missing fields 与精确 failure taxonomy。
8. canonical workflow、公共 Skill packages、shared runtime、preset overlays、dogfood/discovery copies、schemas/tests 与 README 保持同步；安装与 upgrade/update 后继续成立。
9. 本任务自身的 GitHub read、publication 与后续 merge 也只使用 `gh`/`gh api`；secret/token 仅由 `gh` credential store 提供，不进入参数、日志、artifact 或回复。

## Acceptance Criteria

- [ ] AC1：`workflow-contract.md` 或同层 durable SSOT 明确 CLI-only、no-fallback、repo/identity binding、semantic/deterministic boundary 与 `git` transport boundary。
- [ ] AC2：canonical、dogfood、preset overlays、Codex/Claude/Cursor entries、公共 `guru-*` contracts 与 README 不再提供 App/MCP/connector/UI workflow fallback。
- [ ] AC3：Issue、PR、comment、label、checks、reviews、mergeability、Draft/Ready、merge、workflow run/check 与 post-merge verification 均有显式 repo-bound CLI path。
- [ ] AC4：所有适用高层 `gh` 调用含 `--repo`；所有 `gh api` 调用使用完整 repo endpoint；mutation fixture 证明 number/base/head/expected SHA binding。
- [ ] AC5：CLI missing、auth failure、repo access/permission、API unavailable 与 incomplete response 产生不同的稳定 error code/recovery，且没有 fallback 或虚假 `verification_required`。
- [ ] AC6：semantic review 证明 CLI facts/exit code 未替代 readiness、scope、finding、close semantics 或 route 判断。
- [ ] AC7：fetch/push/ls-remote 等本地/transport 操作仍由 `git` 执行，未被迁移到 `gh`。
- [ ] AC8：static/fixture tests 对 forbidden adapter 名称、fallback wording、implicit repo context 与 response-field 缺失 fail closed。
- [ ] AC9：canonical、dogfood、preset/overlay、schema、tests、spec 与 public docs 同步，ownership/drift/sidecar checks 通过。
- [ ] AC10：clean throwaway marketplace init、existing-project preview/switch、preset initial/reapply、official update/upgrade 与 Codex/Claude/Cursor entry consistency 验证通过。
- [ ] AC11：current-HEAD Phase 2 semantic check 与独立 branch review 均无开放 P0-P3 finding。
- [ ] AC12：PR body 只使用 `Closes #181`；#180 不被关闭或修改。

## Out Of Scope

- Issue #180 的 Finalizer transaction、确认预算、merge lifecycle 与 #174 replay。
- 使用 `gh` 替代本地 Git 或 Git transport。
- 新增只包装单条 `gh` 命令、没有独立闭环语义的公共 Skill。
- token 管理、迁移或持久化，以及恶意 actor、对抗输入、竞态、锁、TOCTOU、fault injection 与跨 OS crash consistency 加固。
