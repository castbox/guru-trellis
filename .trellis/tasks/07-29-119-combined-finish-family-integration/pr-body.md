## 变更摘要

- 将 Guru Team Finish-family 收尾链路收敛为薄 workflow 编排，通过 13 个 typed exits 路由 `guru-review-task-publication`、`guru-verify-extension-installation` 和 `guru-finalize-task` 的唯一 consumers。
- 新增 Guru namespace 的 Shared/Codex/Claude/Cursor finish 入口与兼容迁移，平台入口只负责加载和路由，不复制 Skill 内部合同。
- 补齐 public-only cross-skill evidence、#105 transaction/recovery 回归、clean install、`trellis update`、preset reapply 和四平台安装验收，并同步 durable Docs SSOT 与 ownership inventory。

## 影响范围

- Workflow marketplace：canonical 与 dogfood `.trellis/workflow.md` 的 Finish Phase 3.6/3.7 路由。
- Guru preset：三个 additive `guru-finish-work` 平台入口、ownership/manifest、installer 与 throwaway verifier。
- Public integration：Finish-family adapter/eval、per-exit output schema、consumer projection 与 private-runtime boundary。
- 未修改 `guru-review-task-publication`、`guru-verify-extension-installation`、`guru-finalize-task` 的内部行为，未移植 PR #160 task artifacts，也未提前实施 #132 upstream overlay cleanup。

## 验证结果

- Skill package：184/184。
- #105 transaction/recovery：640 passed，13 intentional skips。
- Preset installer：48/48；ownership：12/12；Finish entry contract：3/3。
- Source combined Shared/Codex/Claude/Cursor：4/4；initial/post-update installed 四平台两轮均为 4/4。
- Clean install、workflow init/preview/switch、`trellis update --force`、preset reapply、`.new`/`.bak` 与 dogfood overlay drift：通过。
- Exact pushed ref `8e08be3d716e6f81cde2961831beb14d4deb6801` 的 remote marketplace verification 由 finalizer 在 Draft PR 前执行；当前 ledger 以 machine-pending 状态 fail closed，不将本地 sample 冒充远端证据。

## Review Gate

- Reviewed HEAD：`8e08be3d716e6f81cde2961831beb14d4deb6801`。
- Branch Review：`review-gate:54bd28f48808c5d727acefbdd33a95f6dbcf3a37c78641615e0e8c6b2ccd8076`。
- Round 4 关闭 `BR-FINAL-F1`；Round 5 fresh final reviewer 覆盖完整 `origin/main...HEAD`，结论为 0 finding、0 scope proposal、`passed`。

## Docs SSOT

- 策略：`ssot_first`。
- durable docs：已同步 `docs/requirements/requirement-main.md`、README、canonical workflow/preset README 及 `.trellis/spec/workflow/**`、`.trellis/spec/preset/**` 的 Finish routing、platform entry、installation 与 ownership 合同。
- task delta merge：#119 acceptance、BR-FINAL-F1 的 43 = 25 + 18 ownership 口径和 combined validation 已回写长期 SSOT。
- task history：acceptance gap audit、agent assignment/recovery、命令 digest、raw review reports 与 finding lifecycle 仅保留为 task history。
- follow-up / limitation：#132 继续负责全仓 upstream overlay migration；本 PR 不提前实现或关闭 #132。Exact pushed-ref verification 必须在 PR 创建前由 finalizer 完成。

## Issue 关闭范围

- Closes #119
- Closes #115
- Related: #105、#116、#117、#118
- Follow-up: #132，保持 open

## 安全说明

- 未引入或输出 token、secret、private key、签名 URL、`.env`、数据库 URL 或客户数据。
- 变更限于 workflow marketplace、preset、平台入口、ownership/manifest、eval 与安装验证；无 CI/CD、容器、Kubernetes/Kustomize、数据库 migration 或 Makefile 变化。
- 按 Issue 正文保持 honest-but-fallible 正常运行边界，不扩展恶意 actor、伪造、竞态、锁、TOCTOU、额外 fault injection 或跨 OS crash consistency。
