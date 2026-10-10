# #453 Design contribution

候选，未晋升。继承 Design `.81/active` 与 public Architecture Baseline `.81/active`。设计责任定位如下；完整 reusable transport 合同只有 [companion spec](../../../trellis/presets/guru-team/spec/workflow/companion-scripts.md#intermediate-command-stdout-10) 一处。

| Identity | Owner / contract locator |
| --- | --- |
| D453-01 | `runtime/command.py`、`runtime/validate.py`；commands 1.1 与 intermediate receipt 1.0 schema |
| D453-02 | 原 package public invocation、owner schema、checkpoint 与 atomic/recovery owner；正式输出不变 |
| D453-03 | `runtime/io.py` 的固定 projection；当前 CLI/eval/integration caller；[MIGRATION-453](../../../trellis/presets/guru-team/MIGRATION-453.md) |
| D453-04 | preset installer、canonical packages 和所选平台 discovery projection |
| D453-05 | `adapters/eval/formal_exit_boundary.py` 的 native CLI replay；当前 AI 审查真实完整 transcript |

脚本只执行/校验/序列化事实，不生成 semantic judgment、grading 或授权记录。共享 dispatcher 不接管原 Skill route；native harness 不输出 pass/fail 语义结论。当前 command inventory 是 36 packages（34 semantic、2 deterministic）/109 commands；formal classification 依据 interface 的公共 wrapper 与该 wrapper 实际固定 runtime command 的共同绑定，不能只按文件名、role 或 wrapper-path equality 猜测。

[Architecture 候选](../../../.trellis/tasks/10-10-453-formal-skill-exit-boundary/architecture-contribution.md) 独立承接责任边界、兼容退出与 promotion；当前候选不创建新 ADR。
