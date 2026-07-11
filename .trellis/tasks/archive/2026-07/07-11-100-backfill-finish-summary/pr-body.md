## 变更摘要

- 新增一次性 `backfill-finish-summary.sh` 迁移命令，为既有 archived tasks 生成符合 #97 schema 的 task-local `finish-summary.json`。
- 按固定白名单和字段优先级读取历史 task artifact，记录 `source_artifacts`、`missing_fields` 与 `confidence`，并对单 task 错误进行隔离。
- 对 archived task root、路径逃逸、surface 聚合、检索短语和 backfill-only retrieval 边界实施严格校验；不放宽正常 finish-work。
- 使用最终 builder 重建 44 份历史完成摘要，保留 #97 正常 summary 的原始字节。

## 影响范围

- Canonical workflow：新增 backfill Python 子命令、bash wrapper 和完整回归测试。
- Guru Team preset：安装新增公共 companion script，并同步 extension manifest、README、throwaway 安装与 update 验证。
- Dogfood 安装副本：同步 canonical Python、wrapper 与 workflow，overlay drift 保持为零。
- 历史 task artifact：新增或重建 44 份 archived `finish-summary.json`；不创建 repo 级全局 index。
- #97 的 `finish-summary` schema、`finish_summary_retrieval_text()` 和正常 finish/publish 路径保持不变。

## 验证结果

- Canonical unittest：334 项通过。
- Preset unittest：使用真实 `test_apply_guru_team_trellis_preset.py` 命令，36 项通过。
- Python validator 与 Draft 2020-12 schema：45/45 通过。
- 44/44 backfill 确定性重建与 surface path 守恒通过；写后 dry-run 为 45 skipped、0 errors。
- #97 正常 summary SHA-256 保持 `f18370b72df53c720f33e170b2113a6a7958311913f787a4c64279e7d025fd80`。
- Fresh throwaway repo 的 preset 安装、wrapper dry-run、workflow preview/switch、`trellis update --force`、workflow 重选和 preset reapply 通过。
- 远端分支 marketplace verification 由 publish gate 在 push 后执行，pending evidence 不会直接满足发布。

## Review Gate

- Branch Review Gate 已在 HEAD `ec5ac3e0f7752286ca5b17428b713711c1a07758` 通过。
- 审查范围为 `origin/main...HEAD` 的完整 73 文件 diff。
- 五轮独立审查发现并关闭 F-001 至 F-004；最终 fresh reviewer `/root/branch_review_100_release_round5` 的 `findings_count=0`。
- 审查覆盖需求、设计、代码、测试、Docs SSOT、历史数据、安装升级、安全边界、部署影响和提交消息合同。

## Docs SSOT

- 策略：`ssot_first`。
- Durable docs 已更新：`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/preset/installer.md`、canonical/dogfood workflow、workflow README 和 preset README。
- 已合并 task delta：task-root marker/ancestor、preview parity、固定 fallback、completion fallback、两个窄 retrieval 例外、commit 来源优先级、confidence 和 surface path 守恒。
- 仅保留为 task history：44 份仓库迁移结果、Phase 2/Branch Review 执行证据和 finding 生命周期。
- 当前限制与后续：远端 marketplace verification 在 push 后完成；#98 消费本任务生成的历史 summary，实现历史上下文分级发现。

## Issue 关闭范围

Closes #100

### 仅引用或相关

- Refs #53
- Refs #96
- Refs #97
- Refs #99

### 后续范围

- Follow-up #98

## 安全说明

- Backfill 只读取 archived task 目录中的固定白名单 artifact，不读取 active task、`.trellis/workspace/**` 或 `.trellis/.runtime/**`。
- 命令不访问 GitHub，不调用 `trellis mem`，不写入全局 committed index。
- 路径必须为 repo-relative archived task root；绝对路径、parent segment、symlink escape、分组目录和 task 子目录均 fail closed。
- 输出和错误信息不包含 token、secret、私钥、签名 URL、`.env`、数据库 URL、客户数据或本机绝对路径。
- 本次不修改 CI/CD、容器、Docker Compose、Kubernetes/Kustomize/Helm、数据库 migration 或 Makefile，无部署拓扑和运行时配置变更。
