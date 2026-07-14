# #125 技术设计：Skill standalone runtime dependency

## 1. 设计结论

采用“package 声明依赖、extension 发布能力、shared dispatcher 校验并执行、preset 完整分发”的四层合同：

```text
workflow mandatory invoke / platform direct discovery
  -> package thin wrapper
  -> Guru Team shared runtime dispatcher
  -> interface dependency + installed extension manifest + managed inventory
  -> existing shared companion command / Python runtime
```

`standalone` 只移除 global workflow routing dependency，不移除 Guru Team extension runtime dependency。Package wrapper 不再直接寻找 `check-commit-messages.sh` 或 `create-task-commit.sh`。

## 2. SSOT 与所有权

| 层 | SSOT | 所有权 |
| --- | --- | --- |
| Mode 与 package contract | `.trellis/spec/workflow/skill-package-contract.md` | 定义 routing independence、runtime dependency、non-portable 边界 |
| Interface schema | `trellis/skills/guru-team/schemas/skill-interface.schema.json` | 定义机器字段与闭集约束 |
| Active interface | `trellis/skills/guru-team/packages/guru-create-task-commit/interface.json` | 声明当前 Skill 的 mode、dependency 与 runtime command |
| Package execution prose | `SKILL.md` 与 `references/contract.md` | 定义 direct discovery 入口、完整闭环与 fail-closed 行为 |
| Runtime capability | `trellis/guru-team-extension.json` | 发布 extension runtime API version 与 dispatcher id |
| Deterministic execution | `trellis/workflows/guru-team/scripts/` | 校验完整安装与兼容性，然后调用现有共享 command |
| Distribution | `trellis/presets/guru-team/` | 安装 runtime、schema、package、manifest 与平台副本 |
| Durable requirements | `docs/requirements/` | 记录产品级安装与调用合同 |
| Public docs | 三份 README | 说明用户安装、升级、standalone 边界与 installed files |

Generated copies 只能从 canonical source 生成。Dogfood `.trellis/guru-team/skills/` 与平台 roots 不拥有语义。

## 3. Interface schema 迁移

现有 interface schema `1.0` 没有 dependency 字段。新增 required 字段会改变兼容面，因此 schema identity 必须升级为 `1.1`，extension manifest 的 `interface_schema_id` 必须同步升级。Mode id 保持 `workflow` 与 `standalone`。

### 3.1 Mode metadata

每个 mode 增加闭集 `routing`：

```json
{
  "workflow": {
    "routing": "global_workflow",
    "entry_precondition_ids": ["..."]
  },
  "standalone": {
    "routing": "direct_discovery",
    "entry_precondition_ids": ["..."]
  }
}
```

Source validator 必须校验 exact mode set、exact routing value、entry precondition identity 与顺序一致。

### 3.2 Runtime dependency metadata

Interface 增加一个 closed object `runtime_dependency`：

```json
{
  "extension_id": "guru-team",
  "api_version": "1.0",
  "manifest_path": ".trellis/guru-team/extension.json",
  "dispatcher": "run-skill-command",
  "distribution": "guru-team-preset",
  "package_portability": "not-self-contained"
}
```

每个 validator 增加 `runtime_command`，值必须是 extension manifest `public_api.companion_scripts[]` 中的稳定 command id。`command` 继续指向 package thin wrapper，保持调用入口不变。

### 3.3 Extension capability metadata

`trellis/guru-team-extension.json.public_api.skill_runtime` 增加：

```json
{
  "api_version": "1.0",
  "dispatcher": "run-skill-command",
  "manifest_path": ".trellis/guru-team/extension.json"
}
```

Extension version 必须从 `0.6.5-guru.5` 升级到下一个 Guru revision，并同步 README version matrix、installer assertions 与 dogfood manifest。

## 4. Shared dispatcher

### 4.1 Public entry

新增 managed executable：

```text
.trellis/guru-team/scripts/bash/run-skill-command.sh
```

Canonical Bash wrapper 只转发到 `guru_team_trellis.py` 的新 subcommand。`run-skill-command` 作为 stable companion script id 写入 extension manifest 与 preset installed-file list。

### 4.2 输入

Dispatcher 接受：

- `--package-root <path>`
- `--validator <validator-id>`
- `--` 后的原始 command 参数

Package wrapper 只能传递自身 package root 与固定 validator id，不得传递任意 runtime path。

### 4.3 客观校验顺序

1. 从 dispatcher canonical location 推导 target repo root。
2. 以 component-wise `lstat` 校验 package root、interface、installed manifest 与 dispatcher 路径。
3. 加载 interface schema 1.1 并验证 active package interface。
4. 校验 `runtime_dependency.extension_id` 与 installed manifest extension id。
5. 校验 dependency API version 与 `public_api.skill_runtime.api_version`。
6. 校验 dispatcher id、manifest path、distribution id 与 package portability enum。
7. 调用 installed package validator，确认 canonical installed package 与当前 discovery copy 处于受管且无 drift 状态。
8. 解析固定 validator id，读取其 `runtime_command`，确认该 command 出现在 extension public API。
9. 映射到 `.trellis/guru-team/scripts/bash/<runtime-command>.sh`，完成路径和 executable 校验后 `exec`。

任一步失败都必须在目标 companion command 运行前退出。

### 4.4 Wrapper fallback

Package scripts 只定位两个合法 dispatcher layout：audited installed package layout 与平台 discovery layout。找不到 dispatcher 时必须输出固定 remediation：

- 当前 Skill 不是 self-contained/portable package；
- 安装或升级完整 Guru Team preset；
- 处理 `.new` / `.bak`，再运行 source/installed validation；
- 重试原命令。

Wrapper 不得回退到旧 runtime command 直连路径。

## 5. Validation ownership

- JSON Schema 负责字段存在、类型、enum、additionalProperties、路径 pattern。
- Source validator 负责 mode parity、dependency cross-field、validator command membership 与 source tree 事实。
- Installed validator 负责 manifest provenance、managed hashes、平台副本、executable mode、sidecar 与 drift。
- Shared dispatcher 负责本次 invocation 的 runtime/API/package freshness。
- AI 继续负责 scope、sufficiency、review findings、human confirmation 与 typed route 判断。

脚本不得把 runtime compatibility pass 当成 semantic pass。

## 6. 测试设计

### 6.1 Package contract tests

- 断言 `workflow.routing=global_workflow`。
- 断言 `standalone.routing=direct_discovery`。
- 断言两种 mode 的 precondition ids 完全一致。
- 断言 runtime dependency 与 extension capability 一致。
- 断言 contract 同时包含 routing independence、runtime dependency、non-portable 语义。
- 断言 wrapper 不包含 parser、task/gate 解析、Git staging 或 transaction 实现。

### 6.2 Negative fixtures

- 单独复制 package，执行两个 wrapper，必须 exit 2 并输出 preset install/upgrade remediation。
- 删除 installed manifest、删除 dispatcher、修改 API version、修改 dependency id、修改 runtime command、制造 discovery copy drift，必须在业务副作用前失败。
- Interface schema/source validator 必须拒绝缺字段、额外字段、坏 enum、错误 mode routing 与 workflow/standalone precondition 漂移。

### 6.3 Positive installation fixtures

- Preset 完整安装后，从 `.agents/skills/guru-create-task-commit/` 直接调用 wrapper，证明 direct discovery 不依赖 global workflow routing。
- 保留现有两轮 task commit smoke，证明 shared parser 与 exact executor 仍由 runtime 执行。
- `trellis update`、workflow switch、preset reapply 后再次执行 standalone runtime probe。
- Source/installed validation、managed inventory、platform selection、clean recursive sidecar scan 必须通过。

## 7. Docs SSOT Plan

- Docs state：`partial_docs`。
- Strategy：`ssot_first`。
- 原因：本任务修改公共 mode、interface、runtime、installer 与 upgrade 合同；task artifact 不得成为长期语义来源。
- 证据路径：`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/docs/public-docs.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、三份 public README。
- Durable docs 更新：先更新上述 spec 与 requirement files，再实现 schema/runtime/installer，最后同步 README 与 generated copies。
- Task delta 回写：mode 定义、runtime dependency 字段、fail-closed remediation、安装/升级验证矩阵必须全部写入 durable docs。
- Task history only：stacked base 决策、Phase 0 命令输出、sub-agent liveness、逐轮 findings、临时验证日志只保留在 task artifacts。
- Merge checkpoint：Phase 2 check 前，durable docs、canonical source、installed copies 与 tests 必须完成一致性核对。
- PR limitation：#125 PR 先以 `feat/122-guru-create-task-commit` 为 base；PR #124 合并后必须把 #125 PR retarget 到 `main`，并重新验证 base-to-HEAD diff。

## 8. Upgrade、rollback 与兼容

- Upgrade：运行 `trellis update` 后重新选择 Guru Team workflow、重新 apply preset、处理 sidecars、运行 source/installed/drift validation。
- Old runtime：新 wrapper 必须拒绝缺少 `run-skill-command` API 的旧安装，并输出升级提示。
- Rollback：回退 #125 的 task work commit，使用前一 Guru Team release ref 重新 apply workflow/preset，再验证 installed manifest 与 managed hashes。
- Mode compatibility：`workflow` / `standalone` id 和 typed exits 不变；schema identity 升级记录机器合同变化。

## 9. 安全与部署影响

- 安全：不得输出 token、secret、private key、签名 URL、`.env`、数据库 URL 或本机绝对路径。错误信息只能包含稳定 command、repo-relative path 与公开安装入口。
- 部署：不新增服务、CLI 业务入口、worker、schedule、queue、数据库 migration、容器或 Kubernetes 资源。
- CI/CD、Dockerfile、Docker Compose、Kustomize、Makefile：本任务不改变这些资产，也不改变应用部署形态。
