# #125 明确 Guru Team Skill standalone 模式的 runtime 依赖语义

## 1. 背景与基线

`guru-create-task-commit` 由 Issue #122 / PR #124 引入。Issue #125 指出，现有合同同时使用 `workflow` 与 `standalone`，却没有明确区分 workflow routing independence 与 runtime/package independence。

本任务采用用户已确认的 stacked 基线：

- Git base：`feat/122-guru-create-task-commit`
- Base HEAD：`49bf572e6a89bff9c63416bea64254cda0c20bf0`
- PR #124 当前状态：OPEN、MERGEABLE、CLEAN
- #125 必须保持独立 Trellis task 与独立 PR，不得修改 #122 已归档 task，也不得改变 #122 / PR #124 的 issue close/ref 语义。

## 2. 目标

建立一套可审计、可机器校验的 Guru Team public Skill runtime dependency 合同，使 direct discovery 不再被误解为单目录独立分发，并让缺失或不兼容 runtime 在任何业务副作用前失败。

## 3. 稳定语义

1. `workflow` 与 `standalone` 必须继续作为稳定 mode id。
2. `workflow` 表示 global workflow 通过 mandatory marker 加载并调用 Skill。
3. `standalone` 表示 Skill 能脱离 global workflow routing，被平台直接发现和调用。
4. 两种 mode 都必须依赖完整安装且兼容的 Guru Team extension runtime、共享脚本和组件。
5. `standalone` 不得表示 Skill 目录是 self-contained package，也不得承诺该目录脱离 Guru Team preset 独立分发。
6. 两种 mode 必须执行同一组 entry preconditions、AI Review Gate、human confirmation 条件、recorder/validator 与 typed exits。

## 4. 功能需求

### R1. 机器依赖合同

- Public Skill interface schema 必须声明 mode routing 语义与 Guru Team runtime dependency。
- Active package interface 必须声明 extension id、runtime API version、installed manifest 路径、shared dispatcher id、preset distribution id 与 non-portable package 语义。
- Source validator 必须拒绝缺失、类型错误、未知字段、错误 mode routing、错误 dependency identity、错误 dispatcher 或 workflow/standalone precondition 漂移。
- Extension manifest 必须发布与 interface dependency 对应的 runtime API 能力。

### R2. 共享 runtime 单一来源

- Package wrapper 只能负责定位 shared dispatcher、传递 Skill/validator identity 与转发参数。
- Shared dispatcher 必须校验 installed extension manifest、runtime API compatibility、active package inventory、interface dependency 与目标 companion command，再调用共享 runtime。
- `validate_commit_message()`、task/gate 解析、Git snapshot、exact staging、transaction、rollback 与 result validation 必须继续只存在于 Guru Team runtime。
- Package 与平台副本不得复制上述能力。

### R3. Fail-closed 与修复提示

- 单独复制 Skill package、缺失 extension manifest、缺失 dispatcher、runtime API 不匹配、installed package drift 或命令映射不匹配时，wrapper 必须在业务副作用前以非零状态退出。
- 失败信息必须明确说明：该 Skill 不是 portable/self-contained package，调用方必须安装或升级完整 Guru Team preset，然后重试。
- 失败路径不得回退到旧 companion command，也不得猜测兼容性。

### R4. Canonical 与分发一致性

- Canonical source 必须位于 `trellis/skills/guru-team/`、`trellis/workflows/guru-team/` 与 `trellis/guru-team-extension.json`。
- Preset installer 必须安装 runtime dispatcher、interface schema、active package 与 extension manifest，并把 active package 分发到 shared、Codex、Cursor、Claude 已选 roots。
- `.trellis/guru-team/skills/`、`.agents/skills/`、`.codex/skills/`、`.cursor/skills/`、`.claude/skills/` 的受管副本必须由 preset apply 生成，不得手工形成另一份语义来源。
- Source、installed、dogfood drift 与 recursive sidecar 检查必须全部通过。

### R5. Durable 与公开文档

- `.trellis/spec/workflow/skill-package-contract.md` 必须成为 mode/runtime 语义 SSOT。
- Companion runtime、preset installer 与 public docs spec 必须承接各自边界。
- `docs/requirements/`、`README.md`、workflow README、preset README、canonical package contract 与 `SKILL.md` 必须使用同一语义。
- 安装清单必须包含新增的 shared dispatcher。

## 5. 验收标准

- [ ] `workflow` 与 `standalone` mode id 保持不变，机器 metadata 明确标识两者的 routing 差异。
- [ ] Interface schema 与 source validator 拒绝缺失或不兼容 runtime dependency。
- [ ] Canonical package contract 明确 `standalone` 只代表 routing independence。
- [ ] 单目录 wrapper fixture 以非零状态失败，stderr 同时包含完整 preset 安装/升级提示与 non-portable 说明。
- [ ] 完整 preset 安装后的 shared discovery wrapper 能以 standalone 入口调用 shared dispatcher。
- [ ] Clean throwaway 在初次安装以及 `trellis update` + workflow/preset reapply 后验证 standalone 入口。
- [ ] Package test 证明 wrapper 不含共享 parser、task/gate 解析或 Git transaction 实现。
- [ ] `check-skill-packages --mode source` 与 `--mode installed` 通过。
- [ ] Canonical package、installed package、已选平台副本、extension manifest 与安装清单无漂移。
- [ ] Dogfood apply 后无未处理 `.new` / `.bak`。
- [ ] Durable requirements、spec 与三份 public README 描述一致。

## 6. 范围外

- 不把共享 runtime 复制进 Skill package。
- 不提供 Skill 单目录 self-contained/portable 分发。
- 不新增 `standalone_within_guru_team_install` mode id。
- 不重新打开或修改 #122 已归档 Trellis task。
- 不改变 PR #124 的 title/body/close/ref 语义。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。

## 7. 文档状态与影响

- Docs state：`partial_docs`。
- 证据：`.trellis/spec/workflow/skill-package-contract.md` 已定义两种 mode 与 package 分发，但没有定义 routing independence、runtime API dependency、non-portable 边界或 runtime incompatibility 提示。
- 本任务改变公共 extension、interface schema、installer 与调用失败合同，必须更新 durable specs、durable requirements 与 public README。
- 详细 Docs SSOT Plan 由 `design.md` 单点定义。

## 8. 中台知识门禁

本任务不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 或其它业务中台框架。Middle-platform Knowledge Gate 结论为不适用。
