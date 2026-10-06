# 旧业务仓原地升级（#495 后继候选）

当前 Guru `0.7.0-guru.2` 为未发布候选；已发布 `v0.7.0-guru.1` 不含迁移能力。
canonical source lock 已固定包含迁移 PR #27 的 Fork
`8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / `0.7.0-castbox.2`，
对应成功 main CI `37473087582`。该 CI 只证明精确 Fork 提交的检查结果；
实际 checkout/build、Guru 候选完整验收和发布仍需各自验证。
完整验收及发布完成前，不提供可发布固定版本升级声明。

## 支持合同与入口

最低且明确支持来源为 core `0.6.16` / Guru `0.6.16-guru.41`，还须核对
旧 manifest/provenance、core 模板 hashes、任务格式和实际 Git 状态。
`0.6.5/0.6.7/0.6.15` 等来源不借用此证明。目标 workflow 与 preset 必须来自
同一正式固定 Guru candidate，Fork 必须为已构建且固定 source 的迁移实现。

从目标完整 source 的
`trellis/skills/guru-team/packages/guru-upgrade-installation/SKILL.md`
加载 standalone semantic Skill。它可在旧 target 无法通过 current preflight 时使用；
source 的完整 dispatcher、managed Python 和 preset 依赖仍必须可用。
一个复制的 Skill 目录不构成独立安装器。

AI 提示词：

```text
请从已审查且固定的目标 Guru source 加载 guru-upgrade-installation。
先核对 Fork source lock、实际成功构建和 CLI migration 能力，再只读检查当前业务仓。
按该 Skill 合同审查并展示逐文件/逐任务计划、来源与本地编辑处置、实际命令和回退范围。
具体写入取得当前对话确认后执行；升级真实业务仓与版本发布分别确认。
保留合法 TaskId、业务代码/规划/配置/spec/定制和无关 dirty/untracked。
分别报告安装、当前任务 owner 接续、残余旧交付状态与未验证边界。
```

Fork 的正式动作入口为：

```bash
cd "$TARGET_REPO"
node "$FORK_SOURCE/packages/cli/bin/trellis.js" migrate \
  --from 0.6.16 --plan "$CORE_PLAN" --dry-run
```

`CORE_PLAN` 是 AI 已审查字段与文件动作的私有确定性投影，不含用户授权。
移除 `--dry-run` 只执行 core/活动任务转换；它不能单独证明完整 Guru 安装成功。
完整升级、preview、resume 与 rollback 参数以 package 的 current Interface、
schemas 和 wrapper help 为唯一执行合同，本文不复制其字段或私有恢复实现。

## 受管更新与保留

Core/template 由 Fork 更新；marketplace workflow 使用同一 provider 的
`--create-new` 预览、审查后 `--force` 应用；Guru 旧 provenance 由独立迁移
校验 exact managed bytes，备份并显式退役旧资产，再走当前 preset 正式安装。
普通 `update`、`apply` 和 current readers 不增加 legacy fallback。
未知编辑必须单列 AI 处置，不以 marker、目录或“看起来像生成文件”认领 ownership。
Core current actions 不替代旧 receipt inventory。AI 对照旧 template hashes 与目标
路径，逐项展示退役资产的 remove/preserve；删除只执行精确 receipt-owned、旧 bytes
一致且已审查的路径。Guru 旧 hash 未展开资产从 manifest 的 exact source.commit
读取；source checkout 缺该对象时，先从正式 remote 获取该精确 OID，再预览，
不能依赖未说明的本机完整历史。

配置、业务 spec、平台用户区域和无关工作保持；`.developer`、journal、traces、
archive 原字节保留，不重新成为 current authority。所有 `.new/.bak` 逐项解决后，
再执行 source/installed/platform、managed inventory/runtime、reapply/drift 和
recursive zero-sidecar 验证。拒绝、重试和单个 version 文件不构成升级成功。

## 任务接续

活动 task 保留合法非 UUID id，known missing generation 初始化 0，source 由 AI
根据需求与 live facts 明确，不从 URL 或目录猜 closing intent。完整/精简旧 task
转换按 Skill/Fork 的受支持合同执行；未知字段和非空关系逐项审查，不静默丢失。

迁移后沿 current identity → branch establishment → checkout resolution →
session binding → fresh Planning。Planning 保留原规划，unpublished in_progress
保留 commit 和未提交业务工作；fresh 当前规划审查后进入 dev/check。
schema pass 仅证明数据格式，不证明接续。无 session key 使用 explicit TaskId。
Planning 必须加载样本业务自己的 Architecture baseline，并实际执行 Architecture、
两类 qualification、wording 和语义 Planning gates。
仅 untracked、未出现在分支 HEAD 的旧 task 或真实 branch 歧义须给出具体处置。

无关 known-legacy active 只保留 TaskId/TaskRef 占用，不进入 current candidates。
逐项诊断后可在 private core plan 显式 deferred/preserve，原字节保留；未审查遗漏
仍阻塞，direct old/目标占用/身份碰撞/坏 current 仍拒绝。分别报告 converted、
deferred 原因和下一 owner，不把混合库存升级声称为所有任务已转换。

已有 PR、merge、旧 Finalizer/Finish 在途分别只读核对 live state，明确当前可用路径
或 pinned-old/manual disposition。旧 gate 不成为 current pass，不重复 commit/push/
PR/merge，不自动关闭任务或 Issue；残余每个 task 都要报告原因、影响与下一 owner。

## 恢复与回退

执行前保留实际写入/删除路径的私有备份及新增路径清单。普通部分写入按已完成
动作和当前 old/target bytes 恢复；core 已写而 Guru 本地冲突未解决时，不能声明
整仓成功。恢复只做剩余动作，不重复任务转换或外部副作用。

回退只适用于已真实更新 core/Guru/活动 task 后且尚无新版业务工作。
AI 必须先读取新任务、交付、业务和 control/session 状态，判断回退范围。
出现新版工作时停止覆盖式恢复并保留新增内容；不 reset Git、不 rewind commit、
不删除远端 PR。有效回退需恢复旧 bytes/modes、无关状态及旧 runtime smoke。
core/task 已写而 Guru 因普通冲突暂停时产生的新业务工作也受保护：resume 保留
这些工作并继续剩余安装，固定 rollback 基线不得随 resume 吸收新增事实。

## 验证边界

本 Issue 拥有代表性旧来源到后继的 public 迁移、两个最低任务接续、普通部分失败
恢复和真正 post-write rollback；完整累计多平台矩阵有独立 owner。
真实业务仓升级、远端 marketplace、版本发布均须另行确认。当前实现结果参见
task-owned [验证贡献](../../../docs/requirements-design-test-contributions/495-legacy-installation-upgrade/test.md)。
