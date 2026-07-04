# #33 Guru Team Extension v0.6.5 版本与发布 tag 对齐

## 背景

Issue #31 已经引入 Guru Team extension canonical manifest 和 installed provenance，
但当前 `trellis/guru-team-extension.json.version` 仍为 `0.1.0`。用户已经确认本
repo 是 Guru Team 专门维护的 Trellis 扩展仓库，发布 tag 应采用 repo 级
`vX.Y.Z`，本次目标版本为 `v0.6.5`，而不是长期使用 `guru-team/v0.6.5`。

已知事实：

- Trellis CLI `0.6.5` 已验证支持 workflow marketplace `#ref`。
- 旧 tag `guru-team/v0.6.5` 已存在并指向 `main` 上旧 manifest 的 commit。
- 新 tag `v0.6.5` 不能在 manifest/docs PR merge 前创建，否则 tag 与 manifest
  version 会再次不一致。

## 目标

把 Guru Team extension 的可观测版本、公开安装命令和 release tag 规范统一为：

- canonical manifest version 为 `0.6.5`；
- 稳定安装示例使用 `gh:castbox/guru-trellis/trellis#v0.6.5`；
- `main` / 不带 `#ref` 只表示 latest/canary 或需要即时跟随仓库 HEAD 的场景；
- repo release tag 使用 `vX.Y.Z`，并必须与 `trellis/guru-team-extension.json.version`
  一致；
- workflow template id 继续保持 `guru-team`，不把版本号编码进 template id。

## 需求

1. 更新 canonical manifest：
   - `trellis/guru-team-extension.json.version` 改为 `0.6.5`；
   - `tested.trellis_cli` 可记录已经验证过的 Trellis CLI `0.6.5`。
2. 更新 dogfood installed manifest：
   - 通过 preset installer 同步 `.trellis/guru-team/extension.json`；
   - 保留其 installed provenance 语义，不把它当 canonical source。
3. 更新公开文档：
   - `README.md` 的安装、升级 prompt、版本说明和 release order 要写清楚
     `#v0.6.5` / `#vX.Y.Z` 稳定安装形态；
   - `trellis/workflows/guru-team/README.md` 和 `trellis/presets/guru-team/README.md`
     与顶层 README 保持一致；
   - `docs/requirements/requirement-main.md` 记录长期 requirement / release tag
     contract。
4. 更新可复用 spec：
   - 在 `.trellis/spec/workflow/data-contracts.md` 或 `.trellis/spec/preset/installer.md`
     中沉淀 release tag 与 manifest version 的长期维护规则。
5. 保持版本概念分离：
   - 官方 Trellis CLI 版本：`trellis --version`；
   - 目标 repo Trellis project template 版本：`.trellis/.version`；
   - marketplace index schema version：`trellis/index.json.version`，当前仍为 `1`；
   - Guru Team extension version：`trellis/guru-team-extension.json.version`；
   - installed provenance：`.trellis/guru-team/extension.json`。

## 验收标准

- [ ] `trellis/guru-team-extension.json.version` 为 `0.6.5`，JSON 合法。
- [ ] `.trellis/guru-team/extension.json` 中 installed extension version 同步为
      `0.6.5`，并保持 provenance 字段。
- [ ] 文档中的稳定安装命令包含 `gh:castbox/guru-trellis/trellis#v0.6.5`。
- [ ] 文档说明 mutable `main` / 不带 `#ref` 适用于 latest/canary，稳定安装应 pin
      `#vX.Y.Z`。
- [ ] 文档说明 release 操作顺序：先 merge manifest/docs PR，再在 merge commit 上
      创建 annotated tag `v0.6.5`，验证后再退休旧 `guru-team/v0.6.5`。
- [ ] `trellis/index.json.version` 不被改成 extension version。
- [ ] `guru-team` workflow template id 不变。
- [ ] 运行 JSON、脚本语法、Python compile、installer tests、workflow helper tests、
      dogfood drift、task validate 和 docs diff check。
- [ ] 对 `#v0.6.5` 的远程 throwaway 安装验证在本 PR 阶段标记为 post-merge / post-tag
      待验证，不能提前宣称已经通过。

## 非目标

- 不修改 Trellis upstream source、global npm package、`node_modules`。
- 不修改 workflow template id `guru-team`。
- 不在 PR merge 前创建或推送 `v0.6.5`。
- 不在本任务中实现自动 release 流程或 GitHub Actions。
- 不把 active task 状态、workspace journal 或 PR runtime 状态放入 marketplace /
  preset / spec template。

## Docs SSOT

本 repo 有 durable docs：

- 顶层 `README.md` 是用户安装、升级、版本查看和 release tag 策略的主入口。
- `trellis/workflows/guru-team/README.md` 是 marketplace workflow 使用说明。
- `trellis/presets/guru-team/README.md` 是 preset installer 与开箱验证说明。
- `docs/requirements/requirement-main.md` 是本仓库已实现扩展能力和长期 requirement 的
  汇总。
- `.trellis/spec/` 是本仓库后续任务要遵循的可复用维护规则。

本任务必须更新这些 durable docs / spec，而不是只把决策留在 task artifact 中。

## 官方依据

- Trellis 官方 `Customizing the Workflow` 文档说明 workflow 行为由 `.trellis/workflow.md`
  Markdown 控制，运行时读取，不需要修改 Python/hook/Trellis upstream。
- Trellis 官方 `Custom Spec Template Marketplace` 文档说明 Git source 格式为
  `provider:user/repo[/subdir][#ref]`，并示例使用 `#v1` pin branch 或 tag。
