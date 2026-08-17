# v0.6.5-guru.8 发布说明

## 版本映射

- Guru Trellis repo tag：`v0.6.5-guru.8`。
- Guru Team extension revision：`0.6.5-guru.33`。
- 官方 `@mindfoldhq/trellis` CLI：`0.6.5`。
- exact candidate commit/tree：preparation PR 合并后从 fresh `origin/main` 冻结；本文件不在合并前预填。

repo tag 与 extension revision 是独立版本轴。workflow marketplace 与 preset 必须来自同一
immutable tag；tag 的 peeled commit 必须等于最终冻结 candidate。

## 累计变更

- #208 / PR #234：Finalizer 可在同一变更请求内受控接管既有 Ready PR，并保持 expected-head、
  publication payload 与恢复边界。
- #164 / PR #235：新增 AI 语义选择的 task-free/standard Intake 路由，以及限定编辑、检查与
  scope/risk 演化闭环。
- #236 / PR #238：throwaway verifier 的完整 caller graph 使用 source/installed managed
  Python，并在两个 PATH 判别环境核对实际 `sys.executable`、runtime identity 与 dependency lock。
- #237 / PR #241：新增十个 mandatory normal-scenario profiles、四个 typed exits、
  scope-first qualification，以及 deterministic/no-model/fake-production production 路径。
- #243 / PR #244：恢复 versioned `production-current-3.0.json` 的 immutable bytes，使
  canonical/installed SHA-256 回到
  `98f632f815351ae3f84af081613c1b4cde6eab7bc1341af00467755f2f4acacb`。

`c8c2409cbb79759dae8be8ce95ce03655d5cf518` 归档上一发布的 bootstrap task，PR #245
归档 #243 task metadata；两者都属于 `v0.6.5-guru.7..candidate` 字节范围，但不是本版本的
新功能声明或关闭对象。

## 安装与升级

新仓库使用 tag-pinned marketplace workflow 与同 tag preset：

```bash
npm install --global @mindfoldhq/trellis@0.6.5
trellis init -y --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.8
guru_trellis_source="$(mktemp -d)"
git clone --depth 1 --branch v0.6.5-guru.8 \
  https://github.com/castbox/guru-trellis.git "$guru_trellis_source"
"$guru_trellis_source/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo . --platform codex --platform cursor
```

已有仓库先运行 `trellis update --dry-run`；只在输出包含 `MIGRATION REQUIRED`
时执行 `trellis update --migrate --skip-all`，否则执行 `trellis update --skip-all`。完成唯一一次
preserve-mode update 后，再使用 `v0.6.5-guru.8` preview/switch workflow，随后从同一 tag
reapply preset。完成后必须处理全部 `.new` / `.bak`，并验证 source、installed、
Shared/Codex/Claude/Cursor、ownership、managed inventory、executable mode、受管 Python 与
dogfood drift 一致。

## 验证与模型证据边界

本发布要求 fresh 执行 package/integration/eval、clean initial install、existing-repo
preview/switch、official update、preset reapply、linked worktree/closeout、双 PATH managed
interpreter identity，以及 #237 的 deterministic/no-model/fake-production、sandbox、schema/route
和安装投影验证。

本发布未取得 live GPT-5.6 Sol production semantic evidence。deterministic/no-model 结果不能
证明 `160x5`、`160x1` pressure matrix、模型稳定性、未来模型行为或永不复发已经通过。

## Bytecode staging 边界

release/package/managed/snapshot identity 排除 `.pyc`、`.pyo` 与 `__pycache__`。production 与
throwaway snapshot staging 使用显式 exclude，并在首次执行前和 postflight 对 staged roots
执行精确路径扫描，结果必须为零。source checkout 中 ignored bytecode aggregate 不参与
identity、freshness 或 blocking evidence；staged snapshot 命中只报告 hygiene failure。

该临时门禁只属于 #242 本轮 release evidence，不启动或吸收 #239 的 canonical runtime、
多 consumer 或 Trellis 0.7 多 workflow 范围。

## 安全与部署影响

- 不包含数据库 migration、服务部署、容器/Kubernetes 变更或业务配置迁移。
- 不修改 Trellis upstream、系统 Python、global npm 配置或 user site-packages。
- 不包含 credential、secret、客户数据、数据库 URL、签名 URL或敏感原始日志。
- 业务仓库升级属于显式操作；执行前应保留本地修改，处理所有 sidecar，并完成上述验证。

## Issue 范围

- 本发布只关闭 #242。
- #222、#208、#164、#236、#237、#243 仅作为 related authority，不重复关闭。
- #240 是发布后的独立 follow-up。
- #127、#220、#223、#239 保持排除且不修改其资源。
