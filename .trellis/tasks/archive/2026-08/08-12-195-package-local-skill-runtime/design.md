# #195 技术设计：Package-local Skill Runtime

## 1. 设计目标

把当前共享 dispatcher 单体中的确定性实现拆回 15 个 Skill package，使 package 成为 command、runtime、error 与 package test 的唯一 owner；保留一个无 Skill 分支的最小 shared kernel；保持 Markdown Skill 的 AI judgment ownership 和现有 public I/O/typed exits。

## 2. 当前架构

```text
package scripts/invoke.sh and validators
                  |
                  v
.trellis/guru-team/scripts/bash/run-skill-command.sh
                  |
                  v
scripts/python/guru_team_trellis.py (38,333 lines)
                  |
                  +--> all record/check/execute/dispatch behavior
                  +--> package validation and eval support

test_guru_team_trellis.py (24,023 lines) tests the aggregate runtime
```

问题根因不是 Python 文件长度本身，而是 command ownership、错误语义和测试责任无法从 package public contract 直接定位；installed 与 platform projection 因此依赖共享 private implementation。

## 3. 目标目录与所有权

```text
trellis/skills/guru-team/
  registry.json
  runtime/                         # minimal shared kernel only
    command.py
    json_io.py
    schema.py
    paths.py
    git.py                         # only primitives with 2+ identical consumers
    tests/
  packages/<skill-id>/
    SKILL.md
    interface.json
    commands.json                  # complete package command index
    errors/catalog.json            # complete stable error catalog
    runtime/
      record.py                    # only when the Skill records
      check.py                     # only when the Skill validates
      execute.py                   # only when the Skill executes side effects
    scripts/*.sh                   # thin launchers only
    schemas/ examples/ evals/ references/
    tests/                         # package behavior, CLI, errors, exits
```

`record.py`、`check.py` 与 `execute.py` 是职责边界，不是强制三件套。一个 command 的 implementation 只能位于其 `commands.json.owner` 对应 package；跨 package 复用必须通过 public command/DTO，不能 import 另一 package 的 private runtime。

## 4. Command discovery

### 4.1 `commands.json`

每个 active package 提供闭合 command 数组。每项包含：

- stable command `id` 与 package `owner`；
- thin wrapper 与 Python `entrypoint`；
- ordered arguments，包括 required、repeatability、conflict set 与 allowed values；
- stdin mode/schema 与 stdout mode/schema；
- error catalog references 与 exit statuses；
- side-effect class：`none`、`repo_write`、`git_write`、`github_write`；
- runtime role：`record`、`check`、`execute`、`invoke`、`preview` 或 `sync`。

Source validator 聚合 15 个文件并构造全局 `command_id -> owner` map。重复 id、owner mismatch、缺失 wrapper/entrypoint、未声明 interface validator、声明但未引用 command 均阻塞。Installed validator 在 installed tree 重建相同 map，不信任 source-only 结果。

### 4.2 Dispatcher

新的 `.trellis/guru-team/scripts/bash/run-skill-command.sh` 是薄公共入口：定位 installed manifest 与 registry，把 `<skill-id> <command-id> argv...` 交给 shared kernel command loader。Loader 只做 schema/path 校验、owner lookup 与 entrypoint loading；它不识别具体 Skill/profile/exit，也不决定 semantic route。

Package 自有 wrapper 直接绑定其 package/command identity，不能由调用者覆盖 owner。`invoke.sh` 仍负责在 AI owner 已完成语义 gate 后调用确定性 checker 并投影 typed output。

## 5. Error catalog 与 CLI closure

`errors/catalog.json` 是稳定 deterministic failure SSOT。Catalog entry 包含 `code`、`when`、`exit_status`、定位字段规则、`remediation` 与引用 command ids。Public invocation error schema 继续约束 JSON envelope；catalog 不替代 schema。

Shared CLI renderer 从 `commands.json` 与 error catalog 生成 `--help`，runtime parser 读取同一 command definition。Contract test 比较 discovery、help、parser、wrapper 和 negative cases，阻止五份描述漂移。

JSON mode 使用单一 stdout writer：成功或失败只写一个 JSON object，diagnostics 写 stderr，未捕获异常转换为 package 声明的 internal error，不打印 traceback。Help path 在 repository discovery 与 side-effect handler 之前终止。

## 6. Shared kernel admission rule

一个 primitive 进入 shared kernel 必须同时满足：

1. inventory 中存在两个或更多真实 consumers；
2. consumers 对输入、输出、错误和 side effect 使用完全相同语义；
3. API 不接收 Skill id、profile、typed exit 或 route 作为行为分支；
4. kernel unit tests 与 consumer tests 覆盖相同 contract；
5. 删除任一 consumer 后仍不会把其 Skill-specific 行为留在 kernel。

不满足任一条件的逻辑留在 package。Finalizer transaction、merge expected-head、Publication payload、Verification capability 和 semantic result 结构均为 package-local。

## 7. Canonical、installed 与 platform projection

### 7.1 Canonical 到 installed

Preset installer 从 canonical registry 枚举 active packages，把完整 package 安装到 `.trellis/guru-team/skills/packages/<skill-id>/`，把 shared kernel 安装到 `.trellis/guru-team/runtime/`。Manifest 记录每个 managed file 的 source、hash 与 executable mode，并记录旧单体的 managed removal。

### 7.2 Platform projection

Installer 为 shared、Codex、Cursor、Claude 构造 allowlist projection。Projection 只包含 Agent 可读的 `SKILL.md`、interface、public schemas/examples/evals/references 和薄 public wrapper。以下路径必须被 denylist 与 recursive validator 同时拒绝：

- `runtime/**`；
- `tests/**`；
- `errors/**` 的 implementation catalog；
- package-private checkpoint、fixture 与 owner result。

平台入口引用 installed public wrapper，不复制实现。Public-only eval 从 projection root 启动，并用 denied read assertion 证明 private paths 不可读。

### 7.3 Dogfood 与 official update

Canonical 变更通过 preset `apply.sh --repo .` 同步 dogfood；drift checker 比较 canonical、installed 和 overlay。Official `trellis update` 后重新 apply preset，managed unchanged 文件更新，用户修改产生 `.new`/`.bak` 并阻塞验证，直到人工处理。不得 patch upstream-managed template 来维持 runtime。

## 8. 迁移数据流

```text
AI reads SKILL/public contracts
          |
          v
AI completes semantic gate (semantic Skills only)
          |
          v
package thin wrapper -> command discovery -> package runtime role
          |                                      |
          |                                      +--> owner-private checkpoint when required
          v
package checker -> typed public output -> unique workflow consumer
```

Deterministic `guru-sync-base` 跳过 AI semantic gate，但仍通过 package executor/checker 和 typed exit。所有 semantic Skills 保持 `forward -> AI gate -> conditional confirmation -> recorder/validator -> typed exit`。

## 9. Test ownership

- Kernel tests：只验证无 Skill 语义的 primitive、command discovery、JSON I/O、schema/path/Git primitive。
- Package tests：验证 package commands、help/JSON、errors、record/check/execute、profiles、exits、re-entry 和 semantic-result objective validation。
- Integration tests：验证 registry graph、workflow routing、installer/manifest、platform projection、upgrade/update、public-only eval 与完整 lifecycle。
- Negative architecture tests：扫描 kernel 的 Skill/profile/exit branches，扫描 package cross-private imports，扫描平台 private files，扫描 monolith/compat references。

测试不得导入其他 package private runtime，不得预制 checker-passed owner result 来代替真实 invocation，不得把 deterministic validation pass 当作 semantic approval。

## 10. Migration sequence 与 rollback

Checkpoint A 先冻结 inventory/schema/kernel/installer，再用 deterministic 与 semantic pilots 验证架构。B-E 只迁移各自 package owner；shared API 变更必须回到 A 的 schema/kernel review。每个 checkpoint 在 source tree 与 staged installed tree 运行 targeted validation，失败即回退当前 checkpoint 的 package 改动，不影响已通过 package 的 public contract。

Checkpoint F 只执行零引用证明、删除、全量集成与文档收敛。若发现 owner 遗漏，返回遗漏 Skill 所属 checkpoint；F 不新增 runtime pattern。删除前不建立 feature flag；外部行为回滚依赖固定 `.5` tag，开发期回滚依赖 checkpoint 可审 diff 和 tests。

## 11. Extension Verification 特殊边界

`guru-verify-extension-installation` 迁移 #205 合并后的 `standalone_only` source-repository owner。其 execute/record/check 和 clean throwaway capability tests 留在该 package。业务仓库 workflow、Publication、Finalizer、finish-work 无 verifier consumer，不产生 `verification_required`/`not_required` 轮次，不读取或写入 marketplace verification artifact。

## 12. 删除门禁

删除两个单体前必须同时获得：

- live registry 15/15 package command owner coverage；
- source 与 installed invocation trace 的 monolith call count 为 0；
- import/subprocess/path/dynamic fallback/docs/eval/test reference count 为 0；
- package、kernel、integration、public-only eval 与 installed validator 全部通过；
- `.5` upgrade staging 证明 managed old files 被删除且用户修改走 sidecar；
- business smoke 证明 verifier 不可达。

删除后重复相同扫描和完整验证，防止删除动作暴露隐式依赖。

## 13. Trade-offs

- 选择 package-local duplication 而非过早抽 shared helper：增加少量重复代码，换取清晰 owner 与独立删除能力；只有 admission rule 成立时才抽 kernel。
- 选择 generated help from command metadata：增加 schema/validator 工作，换取 discovery/parser/help/test 的单一事实来源。
- 选择一次 PR 的内部 checkpoints：符合 issue 单一完成定义，但扩大 review diff；通过 owner inventory、逐 checkpoint tests 和最终全 diff independent review控制风险。
- 不保留双 runtime：减少迁移后复杂度；回滚依赖 `.5` 固定版本与 managed installer provenance。
