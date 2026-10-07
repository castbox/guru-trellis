# 旧业务仓原地升级（#495 后继候选）

目标开发候选为 Guru `0.7.0-guru.3` / Fork `0.7.0-castbox.3`，尚未发布 Guru 或完成其正式同源验收。Fork PR28 已合并；唯一 source lock 为 `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c`、成功 main CI `37647767799`，该精确源码本地构建通过。正式 Guru source_locked 升级还要求包含当前实现的固定、远端可寻址 Guru commit。已发布 `v0.7.0-guru.1` 本身不含迁移器，但属于新迁移器的合法来源。

## 支持合同与来源分组

全部 `v0.6.x-guru.*` 和 `v0.7.0-guru.*` 正常安装均进入同一 public 入口，不能按代表 revision 排除。release tag、extension revision 和实际 core 分别核对；目标必须是来源后继，同目标只报告 reapply。selector 从旧固定 `.41` 参数迁移为 `guru0.6-family` / `guru0.7.0-family`，它只选择族，不能替代实际安装与来源核验。旧 published 包 immutable，不新增旧参数 alias。

| 组 | 正式 tag 归属（2026-10-07 远端盘点） | 迁移差异与代表 |
| --- | --- | --- |
| G1 | `v0.6.5-guru.1/.2` | schema1 无 package/overlay receipts 与 expanded hashes，早期混合 upstream claims；代表 `.1` |
| G2 | `v0.6.5-guru.3` | schema1 有 receipts、actual extension `.25`；代表 `.3` |
| G3 | `v0.6.5-guru.4/.5` | schema2 无 expanded hashes、extension `.25/.27`；代表 `.4` |
| G4 | `v0.6.5-guru.7/.8/.9/.10` | schema2 完整 hashes、extension `.31/.33/.34/.36`；代表 `.7` |
| G5 | `v0.6.15-guru.1..6` | core .6.15；tag `.1` extension 是 `.6.5-guru.37`，其余 `.38/.39/.40`；代表 `.1` |
| G6 | `v0.6.16-guru.1` | extension `.41`，core .6.16；同 extension 后续 source 的 core .6.17 补映射验证 |
| G7 | `v0.6.17-guru.1/.2` | extension `.42/.43`、core .6.17；代表 `.2`，`.1` 的 all_platforms 配置差异定向验证 |
| G8 | `v0.7.0-guru.1` | core .7.0-castbox.1，current task/control 保留；已有未发布 `.2` source 安装单列 core/current-control 差异 |

全部 19 个正式 tag 有覆盖归属。每个 tag 核验真实 receipt、source/core 映射和 managed footprint；每种不同迁移路径运行代表性升级/恢复/回退，同组等价不逐版本重复。task 格式和状态独立于版本，横向验证 known legacy/current/deferred 与 planning/in_progress。真实差异推翻同组等价时，只增加该差异验收。

正式 tag 使用该 tag 的真实 installer 在干净隔离样本生成 before，不复制历史 dogfood manifest 冒充正式安装。旧 installer 可记录 preparation predecessor、mutable ref 或 dirty source；按正式 source 和实际 receipt/资产字节核对，不把旧 receipt 状态当作排除整个版本族的理由。缺来源对象先读取正式 source；未知本地文件保留并具体诊断，不能用目标 hash 补旧事实。未来不存在的版本不宣称已验收。

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
INSTALLED_CORE="$(cat .trellis/.version)"
node "$FORK_SOURCE/packages/cli/bin/trellis.js" migrate \
  --from "$INSTALLED_CORE" --plan "$CORE_PLAN" --dry-run
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
一致且已审查的路径。缺 hash 的旧资产从核验过的对应旧 canonical source/installer 映射读取；已有 receipt hash 优先绑定旧字节。source.commit 的旧记录语义须与正式 tag/source 一起核对，不能机械要求 predecessor 等于最终 tag。旧清单中的 upstream-owned entries 交还 Fork，不由 Guru 批量删除。

配置、业务 spec、平台用户区域和无关工作保持；`.developer`、journal、traces、
archive 原字节保留，不重新成为 current authority。所有 `.new/.bak` 逐项解决后，
再执行 source/installed/platform、managed inventory/runtime、reapply/drift 和
recursive zero-sidecar 验证。拒绝、重试和单个 version 文件不构成升级成功。

## 任务接续

已满足 current schema 的 task 原 bytes/modes、TaskId、generation、source、状态、关系、业务字段与有效 control/session 保留，不套旧转换或重建有效绑定。known legacy task 保留合法非 UUID id，缺 generation 初始化 0，source 由 AI
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
不删除远端 PR。有效回退需恢复实际 before core/Guru、旧 bytes/modes/control、无关状态并运行对应旧 runtime smoke；输出真实恢复版本，不固定 `.41`。
core/task 已写而 Guru 因普通冲突暂停时产生的新业务工作也受保护：resume 保留
这些工作并继续剩余安装，固定 rollback 基线不得随 resume 吸收新增事实。

## 验证边界

本 Issue 拥有代表性旧来源到后继的 public 迁移、两个最低任务接续、普通部分失败
恢复和真正 post-write rollback；完整累计多平台矩阵有独立 owner。
真实业务仓升级、远端 marketplace、版本发布均须另行确认。当前实现结果参见
task-owned [系列验证贡献](../../../docs/requirements-design-test-contributions/495-upgrade-version-families/test.md)。历史 `.41` 验收只复用未变化且来源匹配的部分，不能代替本轮分组和同源远端验收。


## 已审查定制 companion

升级计划显式 preserve 的 companion 保留原 bytes/modes，目标差异在 preview 审查，不把本地定制写成 canonical ownership。普通 preset reapply 再遇该文件时保留它并生成 `.new` 提示处置，不能无条件覆盖或修改其权限。current Skill/overlay 的接口必须满足当前合同，不能保留不兼容旧接口后声称 current pass；需要合并的定制通过原 resume 入口接续。`config.yml` 是用户配置，即使旧清单曾误列为受管也不清退。
