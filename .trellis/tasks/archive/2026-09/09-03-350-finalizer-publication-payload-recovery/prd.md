# #350 修复 Finalizer 在 base evolution recovery 中收敛正常 Publication payload 演进

## Goal

在合法 base evolution 加单一 provenance metadata tail 的 existing-PR recovery 中，允许 fresh Publication title/body 正常演进，并复用既有 metadata convergence；保持 transaction schema、public I/O、PR #337 与 #333 transaction 不变。

## Requirements

- predecessor transaction 必须仍是未绑定的 `ordinary_publication/push_content`，task、repo、base/head branch、close-Issue scope 与 archive 状态精确一致。
- predecessor Publication HEAD 必须同时等于远端分支和唯一同仓库 Open PR HEAD；Git 拓扑必须通过 #344 exact base-evolution binary-delta 与 #347 single legal provenance-tail validator。
- current Publication 必须来自 fresh Publication Review，并绑定当前 Branch Review commit；只允许 title/body 相对 predecessor 正常演进，禁止业务内容、Issue disposition、scope、repo、branch、PR identity 或 HEAD 漂移。
- title/body 演进必须交由现有 `classify_existing_pr_recovery()` 产生 metadata comparison，并最多执行一次 metadata convergence；完全一致时不得 edit PR。
- preview 必须保持 side-effect-free，报告 `existing_pr_recovery`、`strict_ancestor`、`push_required=true`、精确 PR、逐字段 metadata comparison 和 Ready action。
- execute 必须在首个外部 mutation 前写入 current-plan-bound recovery transaction，恰好 push current Publication HEAD 一次、PR create 为零，且 same-plan retry 不重复已完成副作用。
- 保持现有 transaction schema、public Skill I/O、typed exits、#342/#344/#347/#338 行为兼容；不修改 PR #337、#333 transaction 或 #249。

## Acceptance Criteria

- [ ] 真实去敏 topology 可在无手工 transaction 修改下通过 Finalizer preview，并识别 PR #337 的正常 Publication body 演进。
- [ ] preview 报告 `existing_pr_recovery`、`strict_ancestor`、`push_required=true`、`metadata_update_required=true`，并保留 Ready/Draft 语义。
- [ ] Happy Path 在 mutation 前完成 transaction rebind，current Publication push 一次、PR create 零次、metadata edit 为 0 或 1，随后复用 archive/Ready recovery。
- [ ] title/body、close scope、task/repo/base/head branch、PR/remote HEAD 或 Git topology 任一不满足时，在首个 mutation 前 fail-closed。
- [ ] 非 provenance 文件、非法 manifest、多 tail、额外 business delta、stale Publication/Branch Review 与 transaction 冲突保持阻断。
- [ ] canonical、dogfood installed、Shared/Codex/Claude/Cursor projection 与 targeted source/installed、ownership、drift、task/package、sidecar-zero 验证通过。

## Scope Boundary

- 仅修复 Finalizer recovery contract；不实现或吸收 #333 业务改动。
- 不修改、关闭、重建或合并 PR #337，不修改 #333 owner-private transaction，不关闭 #249。
- 不扩展为任意 Publication rewrite、多 provenance tail、Release Gate、tag/Release、部署、生产 proof 或完整 Throwaway matrix。
- 不处理恶意伪造、攻击模型、锁、TOCTOU、压力竞态或额外 crash-consistency 加固。
