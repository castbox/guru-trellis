# Design

## 1. Target Architecture

全局业务 task graph 从十五个 mandatory Skills 收敛为十四个。`guru-verify-extension-installation` 保持 stable Skill id，但成为 extension source repository 的 standalone-only package，不再拥有 global workflow marker 或 Finalizer consumer edge。

```text
business repository
  Publication ready
    -> guru-finalize-task
    -> push content -> Draft PR -> archive -> Ready
    -> guru-merge-task-pr

castbox/guru-trellis source checkout
  explicit verify-extension-installation intent
    -> source identity preflight
    -> clean throwaway target
    -> capability execution + semantic adequacy review
    -> verified | blocked
```

Markdown workflow 只拥有十四个业务步骤的 phase/routing/typed-exit graph。Verifier package 拥有 source-only entry、semantic gate、deterministic executor/checker 与两个 standalone exits。Runtime 不从 changed path 决定调用 verifier。

## 2. Finalizer Contract Migration

Finalizer current interface 进行一次显式 breaking migration：

- aggregate input 从 5.0 升级到 6.0；删除 `verification_verified` 与 `standalone_verification_not_required` profiles；
- gate schema 从 3.0 升级到 4.0；route enum 删除 `verification_required`；
- transaction schema 从 1.0 升级到 2.0；state machine 删除 `verify`、verification ref 与 verifier checkpoint binding；
- external exits 从六个收敛为五个：`publication_review_stale`、`resume_finalization`、`reprepare_required`、`ready_for_merge`、`blocked`；
- 删除 `project_verification_required`、verification consumer input、authoring seed、output schema/example 与 Finalizer 内部 verification re-entry helpers。

`publication_ready` 仍由 Publication 唯一投影给 Finalizer。Finalizer preview 不再生成 marketplace candidate surfaces；content push 完成后直接继续 draft/archive transaction。现有 repo/ref/HEAD、scope ledger、PR identity、archive、confirmation 和 recovery 门禁保持原义。

旧 5.0 aggregate、verification re-entry input、`verification_required` output 与 gate/transaction schema 保留为 legacy 文件，current interface 不列入 active profiles、outputs、examples 或 schemas。Runtime 对旧输入返回 `retired_task_bearing_extension_verification`，remediation 指向从 current Publication evidence 完整重建 Finalizer 调用。

## 3. Verifier Contract Migration

Verifier current interface 进行 source-only migration：

- aggregate input 从 3.0 升级到 4.0；只保留 `source_repository_verification` standalone profile；
- input 不含 `task_ref`、`plan_ref`、business repo、branch review 或 publication identity；
- outputs 只保留 `verified` 与 `blocked`，consumer 均为 direct standalone caller；
- 删除 workflow `verification_required` profile、`not_required`、`return_to_task_work`、Finalizer projections 与 task finding route；
- private result 从 schema 3.0 升级到 4.0，persistence 固定为 ignored session runtime，不存在 task-local variant；
- package `judgment_mode=semantic` 保持不变，AI 仍负责 capability selection、adequacy、finding 与 final route。

明确调用已表达验证意图，因此 current profile 不需要 `not_required`。无 capability、非 source owner或 identity mismatch 均为 closed input error 或 `blocked`，不是一次空验证成功。

## 4. Source Identity Preflight

preflight 在创建临时目录、执行 `git clone`、运行 installer 或写 owner result 前完成：

1. 当前 root 必须含 canonical `trellis/guru-team-extension.json`、workflow marketplace 与 preset source assets；
2. `origin` 必须规范化为 `castbox/guru-trellis`；
3. public input `repo_ref` 必须为 `castbox/guru-trellis`；
4. requested ref 解析到一个 commit，resolved commit 必须与当前 checkout HEAD 一致；
5. checkout 必须处于 clean source state，task planning/implementation 的已知工作树变更在调用前完成提交；
6. input 不得携带 task-bearing 字段或 credential-bearing locator。

校验失败返回稳定 invocation error，且 execution trace 证明 clone/install/artifact-write command count 为零。校验通过后，executor 从 source ref 创建 isolated source checkout，并由该 checkout 创建 clean throwaway target。所有 target paths 位于临时目录并在结束时清理。

## 5. Runtime Removal And Retention

删除：

- `MARKETPLACE_VERIFICATION_PREFIXES`、`marketplace_verification_required` 和 `closeout_reviewed_change_facts` 中 marketplace surface 分支；
- Finalizer plan 的 `marketplace.required`、candidate surfaces、verification transition 与 task-local verification lookup；
- verifier task identity、task-local artifact path、workflow owner state、Finalizer checker bridge 与 archived verification handling；
- finish integration、eval adapter、installed closeout 中 task-bearing verifier staging。

保留并重构：

- clean install、preset initial apply/reapply、Trellis update/reapply、sidecar、Skill discovery、platform equality、ownership inventory、README command 与 redaction capability executors；
- source ref resolution、credential redaction、asset inventory、command evidence 与 semantic result validation；
- Finalizer 的 Publication freshness、immutable push、Draft/Ready PR、archive transaction 与 Merge handoff。

## 6. Artifact And Recovery Migration

- current verifier 不创建或读取 `.trellis/tasks/**/marketplace-verification.json`。
- current Finalizer archive allowlist 删除 verification artifact，finish summary 不声明 verification ref。
- 旧 ignored verifier owner state、execution checkpoint 与 Finalizer `next_transition=verify` transaction 不参与 current recovery；current wrapper 返回 stable reprepare error。
- 已跟踪的 legacy task artifact 不由 installer 静默删除。Finalizer 将其报告为 legacy task residue，并要求在 task work 中显式移除后重新通过 Check/Commit/Review，避免 archive 偷渡旧证据。
- legacy schema/example 只服务迁移说明和拒绝测试，不进入 manifest current inventory、active interface 或 installed current runtime。

## 7. Docs SSOT Plan

| SSOT | Planned change | Derived consumers |
| --- | --- | --- |
| `trellis/workflows/guru-team/workflow.md` | 删除 verifier mandatory marker 与 Finalizer verifier edge，更新 graph counts | `.trellis/workflow.md`、三平台 finish entries |
| `trellis/skills/guru-team/packages/guru-finalize-task/` | Finalizer 6.0/4.0/2.0 migration 与五 exits | installed/shared/platform package copies |
| `trellis/skills/guru-team/packages/guru-verify-extension-installation/` | standalone-only 4.0 source-owner contract | installed/shared/platform discovery copies |
| `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | 删除业务 applicability、task artifact 与 bridge，增加 source preflight | `.trellis/guru-team/scripts/python/` |
| registry、production contract、extension manifest | 十四 workflow Skills加一个 standalone Skill的 current inventory | discovery、validator、eval、installer |
| workflow/preset/docs specs 与 README | 记录 ownership、migration、安装及验证入口 | 用户安装和维护说明 |

Canonical 修改完成后运行 preset apply，同步 dogfood 和 platform copies，再运行 drift checker。Generated copy 只用于一致性验证。

## 8. Test Architecture

- package contract：current profiles/exits/projections、legacy rejection、source identity preflight、zero task artifact。
- runtime unit：Finalizer 无 path applicability、直接 continuation、recovery migration、非 source zero-side-effect rejection。
- graph integration：十四 mandatory workflow invokes、Finalizer 五 exits、verifier standalone direct consumer、无 orphan edge。
- representative business fixture：覆盖业务 docs、code、config、`.trellis/**` 与 installed manifest，完整 closeout trace 断言 verifier invocation count 为零。
- source fixture：local canonical checkout配 remote candidate ref，clean throwaway initial install、existing repo update、official Trellis update/reapply、platform equality、ownership、redaction 与 zero-sidecar。
- distribution：canonical/installed/shared/Codex/Claude/Cursor bytes、manifest inventory、README command 与 executable mode。

## 9. Risk And Rollback

- 主要风险是删除 verifier bridge 时破坏 Finalizer push/archive recovery；实施按 transaction state 逐条替换测试，不合并半迁移 schema/runtime。
- 次要风险是 standalone-only package 被 registry validator误判为 orphan；registry/interface/validator/manifest 必须在同一版本单元切换。
- 回滚以完整版本单元执行：workflow graph、两个 package interfaces、runtime、registry、manifest 与 generated copies保持同一 commit，不保留 dual-route feature flag。
