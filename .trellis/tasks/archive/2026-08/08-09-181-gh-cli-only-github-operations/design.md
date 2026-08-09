# Design: GitHub CLI-only platform operations

## 1. Architecture

采用一个 durable policy owner、一个 shared deterministic adapter layer、多个薄 consumer 的结构：

```text
workflow/spec GitHub I/O SSOT
  -> guru-* Skill contracts and platform entries reference the SSOT
  -> shared companion runtime executes repo-bound gh/gh api
  -> schemas/typed errors expose deterministic failure facts
  -> semantic Skill owners decide readiness, scope, findings and routes
```

不新增公共 wrapper Skill；已有 package 继续拥有其 closed-loop 行为，只删除 fallback 选择并引用统一合同。

## 2. Durable SSOT

`.trellis/spec/workflow/workflow-contract.md` 拥有跨 Skill 的 GitHub platform I/O policy，至少定义：

- authenticated `gh`/`gh api` only 与 forbidden channels；
- high-level command 优先、`gh api` 作为 CLI 内部能力 fallback；
- explicit repo/issue/PR/base/head/expected-SHA binding；
- CLI/auth/repo-access/permission/API/response failure taxonomy；
- CLI facts 与 AI semantic judgment 分层；
- `git` local/transport boundary；
- secret redaction 与 no-authorization-persistence。

`companion-scripts.md` 承接 deterministic adapter/error mapping；`quality-guidelines.md` 承接 regression、distribution 与 throwaway/update gates；public docs 只描述用户可执行合同，不复制 Skill 内部步骤。

## 3. Runtime Boundary

在 shared Python runtime 收敛 GitHub CLI 调用入口，复用统一 repository normalization、CLI availability/auth/access preflight、JSON decoding、required-field checking 与 portable error classification。调用方传入完整 repo identity 和业务 identity，不从当前目录、connector state 或平台隐式 context 推断。

稳定 failure categories 至少覆盖：

| Category | Meaning | Recovery owner |
| --- | --- | --- |
| `github_cli_missing` | `gh` executable unavailable | install CLI, retry same owner |
| `github_auth_failed` | `gh auth status` invalid | repair CLI auth, retry |
| `github_repo_access_denied` | target repo cannot be read | repair repo permission/identity |
| `github_permission_denied` | authenticated actor lacks mutation/read scope | repair permission or authority |
| `github_api_unavailable` | API/network/server unavailable | mapped retry with same identity |
| `github_response_incomplete` | required JSON/API field absent or invalid | fail closed; adapter/contract repair |

Error facts不得自动决定 semantic route。各 owner 根据其 declared exits 消费精确事实；`verification_required` 仍只用于真正缺失/过期的 extension installation evidence。

## 4. Command Binding

- `gh issue|pr|run ... --repo castbox/guru-trellis` 或 runtime-provided normalized repo。
- `gh api repos/<owner>/<repo>/...`，禁止省略 repo segment。
- PR mutation/read 同时绑定 number、base/head repository identity；适用 mutation 使用 expected head SHA 或 API equivalent precondition。
- `git fetch/push/ls-remote/rev-parse/worktree` 保持现状。

## 5. Distribution

先修改 canonical `trellis/workflows/guru-team/`、`trellis/skills/guru-team/`、`trellis/presets/guru-team/overlays/` 与 specs/tests，再运行 preset apply 同步 `.trellis/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/`。不得把 dogfood copy 当唯一源头。

## 6. Compatibility And Migration

公共 Skill ids、Interface 1.3 profiles、typed exits 与 schema ids 默认保持兼容。若现有泛化错误字段无法表达精确 categories，采用 additive schema migration 或新 schema version，并同步 consumer projection；不静默改变已有 public exit 语义。

历史 archive/review 文档不是安装 surface，不做大范围回写；静态 guard 只扫描 current canonical/installed/platform/public surfaces，避免把历史证据误判为运行时 fallback。

## 7. Docs SSOT Plan

策略：`ssot_first`。

1. 先更新 workflow/companion/quality durable specs，作为实现与审核 authority。
2. 实现 runtime、Skill references、platform/preset 与 tests。
3. 更新 top-level、workflow、preset README，仅保留安装/使用和 CLI-only 用户合同。
4. preset apply 后验证 canonical/dogfood 字节、ownership、drift 与 `.new/.bak` 为零。

## 8. Risk And Rollback

- 最大风险是过宽 static grep 误伤历史 archive 或把 `gh api` 错当外部 adapter；guard 使用 allowlisted current surfaces 与结构化 command assertions。
- failure taxonomy migration 可能影响多个 owner；先锁定 shared adapter tests，再逐 consumer 回归。
- 任何 current package/manifest/schema mismatch 立即 fail closed；回滚以 task branch commit 为单位，不修改 main、remote 或 #180。
