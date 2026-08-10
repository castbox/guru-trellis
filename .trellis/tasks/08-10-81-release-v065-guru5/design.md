# #81 v0.6.5-guru.5 发布设计

## 1. 生命周期边界

本 Issue 分为两个连续但 authority 不同的阶段：

1. **Preparation task lifecycle**：在专用 branch/worktree 中修改 release-owned bytes，经 Guru Team Phase 2/3 发布并合并一个只 `Refs #81` 的 PR。
2. **Post-merge release lifecycle**：从 fresh remote `main` 冻结 candidate，完成 pre-tag validation、tag、tag-pinned validation、Release、evidence comment 和 Issue closure。

Preparation task archive/PR merge 只表示代码准备完成，不改变 #81 的 release gate authority；#81 只有在最终 evidence comment 后才关闭。

## 2. 版本与身份模型

```text
repo release tag       v0.6.5-guru.5
annotated tag object   tag push 后由 remote Git 事实确定
peeled source commit   preparation PR merge 后冻结的 exact remote main candidate
extension revision     0.6.5-guru.26
official Trellis CLI   0.6.5
marketplace source     gh:castbox/guru-trellis/trellis#v0.6.5-guru.5
```

Repo tag、extension revision、official CLI 是独立轴。Candidate bytes 相对 `.4` 已变化，因此 extension revision 必须递增。README 不硬编码尚未产生的 future merge SHA，避免“为了写 candidate SHA 又改变 candidate bytes”的循环；最终 OID 映射由 immutable Git refs、Release notes 和 evidence comment 精确承接。

## 3. Canonical 与 installed 边界

- Canonical manifest：`trellis/guru-team-extension.json`。
- Canonical workflow docs：`trellis/workflows/guru-team/README.md`。
- Canonical preset docs/commands：`trellis/presets/guru-team/README.md`。
- Release/source identity examples 与直接测试：仅修改当前 stable 含义的实例；纯 fictional compatibility fixtures 保持去耦。
- Dogfood installed manifest/copies：通过 canonical preset `apply.sh --repo .` 同步，不把 installed copy 当 source of truth。
- 同步后运行 source/installed package、ownership、overlay drift、recursive sidecar 和 exact managed inventory 检查。

## 4. Candidate 验证数据流

```text
preparation PR merge
  -> sync fresh origin/main
  -> freeze candidate OID/ref
  -> clone/fetch exact candidate into clean source checkout
  -> create clean throwaway target(s)
  -> official Trellis CLI 0.6.5 init/workflow/update
  -> Guru preset apply/reapply/upgrade
  -> source + installed + platform + sidecar + closed-loop gates
  -> pre-tag PASS
  -> confirmed annotated tag push
  -> repeat using #v0.6.5-guru.5
  -> tag-pinned PASS
  -> confirmed GitHub Release
  -> confirmed evidence comment + explicit close
```

验证器必须同时记录 source repo/ref 与 target checkout，不允许把 target HEAD 当 extension source commit。Pre-tag 与 tag-pinned 是两个独立 gate，后者不能复用前者的 semantic pass。

## 5. Upgrade/update 覆盖

- Fresh install：官方 CLI 0.6.5 + `.5` workflow marketplace + preset initial apply。
- Existing workflow：preview 后 switch 到 `.5`。
- Official update：`trellis update` 后重新选择 workflow/reapply preset，再检查 `.new/.bak`、ownership 和 managed inventory。
- Upgrade：从 public `.4` 安装态升级到 candidate，再在 tag push 后从 `.4` 升级到 `.5`。
- Dogfood：canonical apply 同步后验证工作仓库无 overlay drift；candidate/tag source 验证在 clean throwaway 中完成。

## 6. PR 与 Issue closure 语义

- Preparation PR body 只能 `Refs #81`。
- `issue-scope-ledger.json.close_issues=[]`；#81 不由 PR merge 自动关闭。
- #180 仅 related，#195 仅 followup。
- Final evidence comment 与 explicit close 是发布末端独立 GitHub 副作用，必须以 release/tag-pinned live facts为前置。

## 7. 失败与恢复

- Candidate/main/release-owned bytes 漂移：丢弃旧 evidence，重新冻结并完整重跑 pre-tag gate。
- Tag 已存在：若 object/peeled candidate 不完全匹配则 fail closed，禁止移动或覆盖；完全匹配只进入只读 recovery。
- Tag-pinned 验证失败：保留 tag 事实但禁止 Release/comment/close，修复必须通过新明确范围处理；不得改写已 push tag。
- Release 已存在：只允许 exact tag/title/body recovery；不覆盖不匹配 release。
- Comment 成功但 close 失败：live reread comment 后只重试精确 close，不重复 comment。

## 8. 安全与部署影响

不涉及 secret、数据库、容器、Kubernetes、CI/CD、基础设施或业务数据。GitHub 只使用已认证 repo-bound `gh/gh api`；Git transport 只使用 `git`。命令/evidence 输出必须去敏，不记录 token、环境 secret、签名 URL 或本机私有配置。

## 9. Docs SSOT Plan

- Strategy：`ssot_first`。
- Durable owners：canonical manifest、workflow README、preset README 及直接 release identity tests/examples。
- Generated/installed copies：只通过 preset installer 同步并以 drift validators 检查。
- Task planning：本目录 `prd.md`、`design.md`、`implement.md` 仅为任务历史，不作为发布后 runtime authority。
- Release evidence：GitHub Release notes 与 #81 comment 是远端发布事实的 consumer，不新增 tracked handoff/review artifact。
