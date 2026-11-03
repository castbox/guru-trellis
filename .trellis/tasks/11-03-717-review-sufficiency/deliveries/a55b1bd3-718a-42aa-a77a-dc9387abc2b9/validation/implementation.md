# 实现与安装验证观察

观察对象：Task `717-review-sufficiency` 的 D1 完整工作树候选；固定 B 为 `404c841e9ca917b4680831aa0becd2e26d72fa0c`。这份结果供本批 Check、Review 与 Completion 使用，不替代它们的语义判断。真实 Agent 行为单独见 [review-sufficiency.md](review-sufficiency.md)。

## 机械与分发结果

- 独立审核 runtime 14 项、Check contract 13 项、Branch contract 6 项通过。命中原公开合同和运行行为，没有修改公共 I/O/schema/出口。
- `test_review_sufficiency_distribution.py` 通过真实 preset writer 初装/reapply，核 shared/Claude/Codex/Cursor 的十二个入口、共同源及依赖解析、provenance、用户内容保留、零遗留 sidecar。另核未知本地 spec 修改保留并生成 `.new`，manifest 不被该冲突覆盖。稳定执行 1 项通过，61.535 秒。
- source package validator 通过，实际 inventory 为 43 个 packages / 128 个 commands。370 个源 Python 文件内存语法、JSON、Bash、Task context 与 diff hygiene 检查通过；eval collector 自有 3 项机械测试通过。E 测试断言和 A 合法入口文本修订后，又核全部命中 eval Python 的内存语法、源/安装字节、实际 tools 同步及最终 drift，均通过。这些只证明相应机械边界。

规则实施者的原始命令/结果由本会话的原生工具轨迹承接；真实 writer 首次缺少显式匹配 Core scripts，随后一次执行遇到进行中的源修改，均保留原失败。固定源稳定后的执行通过；错误测试 class selector 的命令不计作通过。

## 实际 dogfood tools 同步

通过完整源 `guru-upgrade-tools` 的 preview、prepare、invoke 同步本任务 checkout。执行 public maintenance API 1.0，匹配 CLI/Core `0.7.0-castbox.6`，选择 `local_candidate`；原 writer 返回 `tools_upgraded`，安装版本 `0.7.0-guru.7`。已有 `.trellis/config.yaml` 保留，AGENTS 由原纯 renderer 组合，项目原有内容不丢失。

实际 installed package validator 返回 `passed`；`check-dogfood-overlay-drift.sh` 返回 `ok`，shared/Claude/Codex/Cursor、workflow 与 managed-spec 副本匹配 canonical。目标自身 Python resolver、native continuation 与公开内存 operation probe 通过；回读当前 Task/Delivery 仍为原身份、generation 0、implementing，Planning 仍 applicable。受管 manifest 的 new_copies/managed_backups 均为空；安装仅更新本 checkout 工具，不迁移历史 Task。

准备时曾将 Core 的 `claude-code` 平台名直接传给 Guru，原 prepare 在写入前拒绝；随后按实际 Guru manifest 的 `claude/codex/cursor` 名称重新准备，使用成功返回的唯一计划执行。没有复用失败计划或改写原 writer。

## 证明边界

完整多平台 clean/existing/update/workflow-switch/Release 矩阵未执行；其它业务项目未更新。`formal_fork_source_lock` 是原 tools 结果明确保留的未验证项。本批证明本地候选的受管分发与 tools 采用，不能推出正式发布、所有平台原生模型行为或外部专业 Skill 接入。完整 Agent 逐例正确性仍须读取实际观察；安装和命令通过不证明审核充分性。
