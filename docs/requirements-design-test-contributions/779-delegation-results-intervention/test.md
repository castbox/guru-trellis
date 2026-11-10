# #779 验证策略与实际边界

T779-01/02 的完整预期位于 `proposed/docs/test/current/task-delivery-lifecycle.md`。要求→职责→验证见 traceability.md。候选形成时已完成 Planning Author、Wording、独立 candidate/final Architecture 与 Approval，D1 已由原 Activation 进入实施；这些结果不证明实现、安装同步、Check 或实际 Agent 效果通过。

## 实施后、候选 Check 前的观察

- `git diff --check`、Task `validate`、marketplace JSON 与 Bash 语法检查通过；官方 JSONL 均有效。context validator 提醒大型 spec 注入会截断，实际执行者按原加载合同自行读取完整必要正文。
- 依项目声明范围在内存编译 390 个 Guru Python 文件通过；没有改 Python/runtime，不把语法结果当作方法效果证明。installed `guru-sync-base` contract discovery 返回有效 current 合同。
- 原 source-owned `guru-upgrade-tools` 用固定同一 public/Guru plan 执行。调用等待通道超时后，已核原进程仍运行，未发起第二次安装；原进程正常达到 `complete`，再经同操作 `resume` 正式返回 `tools_upgraded`。实际 installed version 为 `0.7.0-guru.8`，模式为 `local_candidate`，`formal_fork_source_lock` 仍未验证。
- 原 tools owner 实际执行目标 installed/native/public-operation 验证及 peer preservation 后才返回成功。当前 Task/Delivery 的 key、scope、planning_root 和 `implementing` 保持，Planning 结果仍 applicable。`AGENTS.md`、`.trellis/config.yaml` 与冻结 preimage 的内容一致。
- `check-dogfood-overlay-drift.sh --repo .` 通过；Claude/Codex/Cursor 所选投影、shared Skill root、workflow 和 managed specs 一致。受影响安装根递归 sidecar 检查结果为空。实际 Python 选择写在 checkout-local `.trellis/.runtime/guru-team/python/selection-v3.json`，schema 为 `3.0`；没有新建旧 `active.json`。目标 resolver 实际选择用户缓存 managed Python，common/peer pointer 由原 owner 保留。
- 同步后的 installed `get_context.py --mode phase --step 2.1` 正常返回新增方法加载引用，证明实际入口能读取该投影；它不证明 Agent 后续行为或节省效果。

后续仍待：完整候选 Architecture/Check、原 RDT final integration/readback、实际 after 重绑及最终 Check/committed Review/readiness。本文的观察截止不预填这些结果。设备、事故重放、消息计数、完整多平台/Release 矩阵、业务采用和成本节省效果未验证且不作为本项新增验收。
