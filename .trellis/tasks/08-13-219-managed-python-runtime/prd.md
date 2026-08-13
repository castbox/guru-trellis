# #219 受管 Python Runtime 需求

## 目标

Guru Team preset 必须自包含地安装、选择、校验和升级其 Python 运行时依赖，使 canonical source、dogfood 安装副本和业务仓库中的公开 Skill wrapper 不再依赖全局 site-packages、偶然激活的 virtualenv 或交互式 shell PATH。

## 需求权威与背景

- Live authority：`castbox/guru-trellis#219`，2026-08-13 读取时为 open、无评论、唯一 assignee 为 `wesleywu`。
- 当前 `main@3504ecad9ada04493b21f426ff8b8718ad83f969` 的 `trellis/skills/guru-team/runtime/launch.sh` 无条件执行 PATH `python3`；`runtime/schema.py` 在缺少 `jsonschema` 时返回 `runtime_dependency_missing`。
- 当前 preset 没有 Python dependency manifest/lock、受管解释器 bootstrap 或 runtime resolver。真实 PATH Python 3.14.6 无 `jsonschema`，公开 wrapper 因此无法运行。
- 本任务是固定顺序 `#219 -> #217 -> #218 -> #222` 的第一项。只实现并关闭 #219；#217、#218 不进入实现，#222 承接累计发布门禁。

## 功能需求

### R1 依赖锁与可审查来源

- 发布一个 canonical Python dependency manifest/lock，锁定 `jsonschema` 及完整传递依赖。
- 每个已锁定分发包必须固定版本和 hash，安装使用公开默认 Python package index，不注入私有 index、凭据或用户 site-packages。
- lock 是 preset managed asset；canonical、installed 和 manifest inventory 必须一致。

### R2 受管隔离环境

- preset apply 在 target repo 的 gitignored `.trellis/.runtime/guru-team/python/` 下创建隔离环境，不修改系统、Homebrew、global 或 `--user` site-packages。
- runtime identity 必须绑定 Guru Team runtime/interface version、dependency lock digest、Python implementation 与 major/minor version。
- 相同 identity 的 apply/reapply 幂等复用；lock 或 Python identity 改变时构建新候选环境，只有完整能力验证通过后才切换 active identity。
- 候选构建或验证失败时保留旧环境与 active identity，返回稳定错误和可执行 repair 命令。
- stale runtime 清理不属于普通 wrapper；不得递归删除 provenance 未知目录。

### R3 单一 resolver 与入口一致性

- `launch.sh`、`run-skill-command.sh`、package wrapper、discovery/eval/validation 等 Guru-owned Python 功能统一通过一个最小确定性 resolver。
- preset bootstrap 可使用明确选择的 PATH Python 创建 venv；激活后所有公开 runtime command（包括 `--help --json`、record/check/execute/invoke）必须在受管解释器内运行。
- wrapper 不要求手工 activate venv，不读取 active virtualenv，不 fallback 到其他 Python 或系统 site-packages。
- canonical source checkout 与 installed preset 使用同一 resolver 合同；dogfood 副本由 canonical preset apply 同步。

### R4 能力验证与错误合同

- 安装激活前验证 Python/venv/pip 可用、hash-locked 安装成功、依赖版本与 lock 一致，并真实执行 Draft 2020-12 schema 能力探针。
- 网络/索引不可用、Python 不兼容、venv/pip 缺失、wheel 不可用、hash/version 不匹配、active runtime 缺失或损坏时 fail closed。
- runtime 入口失败返回无 traceback 的稳定 `runtime_dependency_missing` JSON，包含具体 dependency、runtime identity（无法确定时为 `null`）和真实可执行的 preset repair 命令。

### R5 测试与快速发布边界

- package/runtime tests 不再把 `jsonschema` 缺失视为 optional skip。
- 覆盖 PATH Python 无 `jsonschema` 但受管 runtime 完整的正向路径，以及 PATH 改变、Python minor 改变、lock digest 改变、损坏 runtime、网络/安装失败、重复 apply 和失败恢复。
- 验证 Draft 2020-12 行为，而不只验证 import。
- 执行一次聚焦 clean runtime install：干净临时 repo 的 PATH Python 无 `jsonschema`，preset 安装后一个真实公开 wrapper 的 schema 路径成功。
- 完成 package/runtime tests、canonical/installed equality、targeted reapply、dogfood drift 与递归零未知 `.new`/`.bak` sidecar。

## 验收标准

- AC1：依赖 lock 包含 `jsonschema` 全部传递依赖的固定版本与 hash，installer 只以 require-hashes 模式安装。
- AC2：fresh apply 创建 repo-local gitignored runtime；相同 identity reapply 不重装，identity 变化创建并切换到新环境。
- AC3：候选安装/能力验证失败不切换 active identity；旧 runtime 仍可解析和运行。
- AC4：公开 wrapper 在 PATH Python 无 `jsonschema` 时通过受管解释器完成至少一次真实 Draft 2020-12 schema 校验。
- AC5：active runtime 缺失/损坏时 wrapper 返回稳定 `runtime_dependency_missing` JSON、无 traceback、无 PATH fallback，并给出 preset repair 命令。
- AC6：canonical runtime/lock/入口与 dogfood installed 副本 byte-equal；targeted reapply 与 drift checker 通过；仓库递归扫描无未知 `.new`/`.bak`。
- AC7：测试覆盖 Issue 声明的正常恢复矩阵，且必需依赖缺失不会 skip。
- AC8：文档不再把全局 `pip install jsonschema` 作为正式修复路径，并明确当前 PR 不是发布充分性证明。

## 非目标

- 不修改 Trellis upstream、全局 npm、系统 Python 或 Homebrew 环境。
- 不实现自制 JSON Schema validator，不 vendor 任意 Python 源码。
- 不修改 Skill semantic ownership、typed exits 或 #217/#218 的 correctness 行为。
- 不增加恶意 actor、手工篡改、锁、TOCTOU、并发压力、crash consistency 或跨 OS 原子性设计。
- 不运行完整 12-capability `guru-verify-extension-installation`，不重复完整 marketplace、official Trellis update、全平台 throwaway 或业务仓库 upgrade smoke。
- 不创建 tag/Release，不启动 #217/#218/#222，不声称当前 main 已可发布。

## Docs SSOT Plan

- `trellis/presets/guru-team/README.md`：安装、runtime identity、reapply 与故障修复的用户 SSOT。
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md`：bootstrap、resolver、wrapper 与确定性脚本边界的 canonical spec。
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`：受管 runtime 的 package、clean install、reapply、drift 与 sidecar 验证门禁；preset apply 同步对应 `.trellis/spec/workflow/**` dogfood 副本。
- runtime/lock 内的机器可读 manifest 是依赖与 identity 的执行 SSOT；README 只解释，不复制完整 lock 内容。
- 不修改 workflow phase、Skill semantic contract 或平台专属行为文档；所有入口只承接共享 resolver。
