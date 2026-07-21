## 变更摘要

- 建立 Guru Team Skill interface 1.3 的最小 typed handoff I/O 基础设施，定义精简 public input、逐 typed exit output、consumer input、薄 projection 与 private artifact 边界。
- 扩展 registry、schema、discovery 与 shared validator，使 package 能声明 compatible interface variant、迁移状态和 public/private inventory，并由 consumer 约束驱动确定性校验。
- 新增 representative active fixture，覆盖 action、sync、legacy 三类 package、dispatcher wrapper、consumer contracts、projection、schema 与 invocation evidence。
- 补齐 Draft 2020-12 closed subset、strict JSON、finite number、format、URI 与 portable ECMA Unicode pattern 的正常路径兼容性校验。
- 同步 canonical workflow、preset installer、dogfood installed copy、三平台 overlay、durable Docs SSOT 与开箱即用/upgrade-update 验证。

## 影响范围

- 新能力仅为 interface 1.3 基础设施和 representative fixture；九个 production Skills 继续使用 interface 1.2 + `legacy`，production `minimal_handoff=0`。
- 不迁移现有 production payload，不改变 mandatory workflow route、typed exit id 或现有 consumer 行为。Stage 0 与其余 active package migration 继续由 #145、#146 承接。
- 变更涉及 workflow/preset companion scripts、registry/schema、fixtures、tests、Docs SSOT 和 task evidence。
- 不涉及 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration、Terraform、Makefile、依赖锁文件或业务服务部署配置，无服务部署、配置迁移或数据迁移要求。

## 验证结果

- Portable pattern focused suite：Node 20 与 Node 26 各 4/4 passed。
- Generated differential：Node 20 raw 与 Node 26 spec-equivalent wrapped oracle 各 4,081 patterns × 33 values = 134,673 comparisons，均为 0 mismatch。
- Finding owner closure 独立对照：Node 20.20.2 与 Node 21.7.1 各 90,080 comparisons，均为 0 mismatch。
- 最终放行独立对照：Node 26.4.0 raw oracle 覆盖 40 个 UTF-16 pair/isolated/zero-width/nullable/backtracking 定向场景，0 mismatch。
- Skill package suite：126/126 passed。
- Shared runtime：548 passed，13 skipped。
- Preset installer：39/39 passed；upstream ownership：6/6 passed。
- Source/installed validators、384-file Claude/Codex/Cursor inventory、dogfood drift、43 个 ownership entries、13 个 managed claims、canonical/installed bytes 均通过。
- Clean throwaway 已覆盖 marketplace sample、init、workflow preview/switch、preset install、installed smoke、`trellis update`、reapply、三平台 copies 与最终零 `.new`/`.bak`/sidecar/conflict/removal。
- `git diff --check`、changed Bash syntax、changed Python compile、58 个 changed JSON parse、secret/deployment/sidecar scans 均通过。

## Review Gate

- Branch Review 覆盖完整 `origin/main...HEAD` 的 101 files、8 commits，以及 planning、implementation handoff、Phase 2、Docs SSOT、issue scope、commit plan 和 review lifecycle。
- Round 14 由原 finding owner 关闭 `F-BR-P3-011`，P0=0、P1=0、P2=0、P3=0。
- Round 15 使用从未参与前序 review round 的全新最终放行代理独立审查，P0=0、P1=0、P2=0、P3=0。
- Review Gate 已绑定当前 reviewed HEAD，blocking findings 为 0。

## Issue 关闭范围

Closes #144

- #145：Stage 0 Skills payload migration，保持 follow-up，不由本 PR 关闭。
- #146：planning、Phase 2 与 task commit Skills payload migration，保持 follow-up，不由本 PR 关闭。
- #98、#109、#115、#127、#131、#132 仅为相关背景，不由本 PR 关闭。

## 安全说明

- 未引入或暴露 token、credential、private key、signed URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- Validator 与测试处理的是标准 JSON、schema 和 escaped Unicode 正常路径；未扩展到恶意篡改、hostile input、非常规竞态、TOCTOU 或 fault injection。
- Production runtime 仍只依赖 Python standard library；Node 仅作为测试 oracle，不存在 production Node/version branch。

## Docs SSOT / 文档同步

- Docs state 为 `complete_docs`，执行策略为 `ssot_first`，task delta 已合并到 durable docs。
- `.trellis/spec/workflow/skill-package-contract.md` 单一拥有 interface 1.3、public/private I/O、projection、consumer contract 与 portable pattern 的 exact contract。
- `data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md` 分别承接数据边界、确定性实现边界和测试义务；README/requirements 只保留公开摘要与导航，不复制 exact EBNF。
- 具体复现值、逐轮 finding 生命周期、命令输出、hash、Node 版本与 sidecar recovery 保留为 task history，不扩散到 durable SSOT。
- Follow-up / 当前 PR 限制：当前分支尚未发布时无法验证 exact immutable remote feature ref；该项由 push 后、PR 前的 Remote Marketplace Verification Gate 补证，现有 public-sample throwaway 未冒充完成。
