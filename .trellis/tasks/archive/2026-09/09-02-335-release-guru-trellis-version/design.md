# 技术设计

## Ownership And Identity

`release-guru-trellis-version` 是 `castbox/guru-trellis` 的 project-local semantic orchestration Skill。共享定义位于 `.agents/skills/release-guru-trellis-version/`，并向 `.codex/skills/`、`.claude/skills/`、`.cursor/skills/` 同步 Agent 可读文件。它不声明公共 `interface.json`、schema、package runtime 或公共 typed exit，也不写入 `trellis/skills/guru-team/`、`trellis/guru-team-extension.json`、preset overlay、ownership inventory 或 `.trellis/.template-hashes.json`。

Skill 使用 Markdown 描述 release-specific 判断和路由；Git/GitHub mutation 继续由现有 owner 和工具执行。Skill 不新增持久化状态机或 companion script 来替代 AI 判断。

## Minimal Input And Fresh Preflight

每次 invocation 都从当前请求解析六项最小 identity：repository、current release Issue、target repo tag、target extension revision、official Trellis CLI version、predecessor tag。开始阶段前 fresh 读取 Issue 正文/评论/状态、`origin/main`、tags/Releases、version surfaces、工作区，以及本设计点名的 lifecycle owner 合同。

缺失、歧义、multiple mapping、candidate cross-SHA、live mismatch、unsupported exit、FAIL 或 SKIP 均停止。恢复只重新读取 live Git/GitHub facts 与仍有效的 owner-private checkpoint，不通过 tracked metadata 补写阶段状态。

## Two-Stage Lifecycle

### Preparation Task And PR

Skill 将 preparation 路由到现有 standard intake，并复用以下 owners：

1. Planning 只建立稳定 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
2. Phase 2 修改实际交付字节、确需更新的 durable docs、repo-private Skill 和 tests。
3. `guru-create-task-commit` 独占每次 task commit 的展示、确认和 side effect。
4. 最终内容 commit 后，`guru-review-branch` 对完整 `origin/<base>...HEAD` 执行一次独立 Branch Review。
5. `guru-review-task-publication` 即时生成并审查中文 PR title/body，只通过其现有最小 DTO 交给 `guru-finalize-task`。
6. `guru-finalize-task` 独占 push、PR create、archive 和 Ready transaction；`guru-merge-task-pr` 独占 expected-head merge 与 closure verification。

Skill 不复制上述 owner 的内部步骤，也不把 Review、Publication 或 Finalizer 结论写回 tracked task。Finalizer 现行 reviewed-content identity 合同明确排除的 provenance/archive metadata tail 不构成 delivery content 变化，不触发第二次完整 Branch Review。

若 fresh base 在 Finalizer 前正常前进，现有 `base_reconciliation_required` exit 必须在无 closeout plan 的路径上按自身 exact base facts 完成 preview、recorder、checker 与 public projection。该路径若被通用 plan-based identity 校验错误阻断，实施可窄修 Finalizer canonical runtime 及其 current-checkout dogfood 投影；修复不得改变 public schema、typed exit、consumer 或 transaction 行为。

### Post-Merge Exact Candidate

preparation PR 合并后，Skill 丢弃 preparation branch HEAD、旧 Branch Review、Publication 和 release evidence，fresh fetch `origin/main` 并冻结 candidate commit/tree。candidate 必须能由 live merge/base facts证明来源，且所有 release checks 绑定同一 candidate。

在任何 tag side effect 前，执行 Issue 要求的 release-specific minimum gate：predecessor-to-candidate 完整 diff、版本轴映射、source 与 installed validators、Shared/Codex/Claude/Cursor parity、install/update/reapply、secret scan、residue check 和独立语义 review。完整累计多平台 throwaway 矩阵仍由专门 Release Gate Issue 拥有；缺少当前 scope 必需证据或出现 SKIP 均不得继续。

之后按严格分离的动作边界处理 annotated tag、tag-pinned smoke、GitHub Release、Issue closure 和 cleanup。每个动作都 fresh 展示目标、refs、命令、预期结果并取得仅适用于该动作的确认。Release title/body 在 Release 动作前由 live Issue、candidate diff、验证证据与 exact identity 即时生成和语义审查，不落 task-local 文件。

## Stable Planning And Forbidden Persistence

`implement.md` 只描述稳定步骤和验证策略，不使用 Markdown checkbox，不因执行进度更新。task 目录不得出现 `release-notes*.md`、PR/Release body handoff、release-status、review-status 或 candidate-status 文件。

tracked task 和 durable docs 不保存 HEAD、时间戳、阶段进度、Gate 结果、finding closure、tag/smoke/Release 状态或用户授权。只有长期产品合同、repo-private Skill 定义、必要 README/SSOT contribution 和测试进入 delivery content。

## Freshness Model

现有 `guru-reviewed-content-1.0` 和各 owner gate 继续拥有 freshness。Skill 只声明 route：

- Skill、README、RDT/Architecture durable contribution、source、test、schema、config 或 script bytes 变化，使受影响的 Phase 2、Branch Review、Publication、Finalizer 或 exact-candidate gate stale。
- ignored owner-private checkpoint 的正常创建、替换或退休，以及既有 Finalizer lifecycle-only metadata，不改变 reviewed delivery identity。
- 任何不满足现有 owner metadata-tail allowlist 的 tracked 变化，均按 content drift 返回 task work。

## Docs SSOT Plan

- `ssot_first`：repo-private release orchestration 的 durable owner 是 `.agents/skills/release-guru-trellis-version/`；三个平台目录保存与共享定义字节一致的发现投影。
- 根 `README.md` 增加仓库维护者入口，明确 Skill 的私有范围、最小输入、两阶段模型和不随 preset 安装的边界。
- RDT owner 通过 `docs/requirements-design-test-contributions/335-release-guru-trellis-version/` 承接 requirement/design/test/traceability；是否 promotion 到 current SSOT 由 `guru-maintain-requirements-design-test-ssot` 决定。
- Architecture owner 通过 `docs/architecture/contributions/335-release-guru-trellis-version.md` 承接 repository release ownership 与 existing-owner composition；是否 promotion 由 `guru-maintain-architecture-baseline` 决定。
- `.trellis/spec/workflow/skill-package-contract.md` 仅作为公共 Skill 隔离 authority；除非实现发现长期公共合同存在真实缺口，否则不修改公共 workflow/package/preset SSOT。

## Test Design

repo-private contract tests 校验四投影字节一致、public inventories 零泄漏、forbidden tracked artifacts 为零、独立 confirmation boundaries 和 fail-closed wording。honest-path integration fixture 使用临时 Git 仓库与现有 reviewed-content helper，证明：稳定计划 -> 最终内容 commit -> 一次完整 Branch Review -> Publication -> Finalizer；Finalizer package 回归另以正常 base 前进证明 planless `base_reconciliation_required` 可通过 preview、recorder、checker 与 public wrapper。lifecycle metadata 不改变 identity，而 delivery/durable/config/script/test 变化改变 identity 并要求 re-review。

测试不伪造恶意状态，不依赖 Issue #332 资源，不创建真实 tag、Release、PR 或业务仓库安装。
