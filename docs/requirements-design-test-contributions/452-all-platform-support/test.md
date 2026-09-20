# #452 All Platform Support Test contribution

状态：`reviewed_promoted`。`T452-01..12` 已成为 `.58` current acceptance authority。
2026-09-20 fresh implementation evidence 已使 `T452-01..11` 通过；`T452-12` 仍为
`in_progress`，等待 Task Commit 与完整 Branch Review。脚本结果不替代 Architecture/RDT
semantic gate。

| Test | 场景与计划通过条件 |
| --- | --- |
| `T452-01` | 锁定 upstream source identity，解析 `AI_TOOLS` 得到 exact 22-platform inventory；id、template/root、native entry 与 descriptor 可追溯，ambient checkout 或目录扫描不能改变结果。 |
| `T452-02` | 公开 parser、installer、manifest、upgrade、throwaway 和 JSON output 均不存在 `--all-platforms` / `all_platforms` 合同；旧参数作为未知参数写前失败。 |
| `T452-03` | repeated `--platform` 覆盖单平台、多平台、任意合法 subset、重复输入归一化与 unknown id 拒绝；最终 manifest/projection/ownership selection 精确一致。 |
| `T452-04` | 未提供 `--platform` 时 selection 恰为 Claude、Codex、Cursor；提供 repeated `--platform` 时只选择显式 subset，unknown 与旧 `--all-platforms` 都在写前拒绝。 |
| `T452-05` | 验证 default selection 只影响无参数新安装；显式 subset 与 upgrade selection 不被默认值扩张、收缩或重标为第三层 authority。 |
| `T452-06` | upgrade fixtures 覆盖单平台、任意 subset、三平台和完整 22 平台，从目标 manifest/provenance 读取 exact selection 并生成 repeated `--platform`；缺失、空、unknown 或跨 section 不一致时写前失败。 |
| `T452-07` | `guru-trellis` dogfood manifest、installed packages、native projections、reapply 参数和 drift selected set 恰为 Claude、Codex、Cursor；OpenCode 与其它平台不因 canonical support 出现在 dogfood checkout。 |
| `T452-08` | OpenCode explicit install 产生正确 `.opencode` discovery/command/skill projection，并覆盖 clean、existing、reapply、update、removal provenance 与 representative actual-load。 |
| `T452-09` | 对全部 22 个 descriptors 验证 canonical/installed/native-surface bytes、mode、manifest mapping、ownership cardinality 与 package-private `tests/` 排除；不假设平台目录或 overlay 数量同构。 |
| `T452-10` | reapply/update 覆盖 unchanged、matching managed backup、正常本地修改、removed platform 与 inventory drift；未知本地修改生成 `.new` 或保留 sidecar，不静默覆盖。 |
| `T452-11` | 代表性 clean throwaway 与 selected-subset integration 验证安装入口、manifest/provenance、reapply、drift 和最终 managed-file hygiene；不执行 22 平台 native matrix。 |
| `T452-12` | fresh Architecture/RDT、Phase 2、task check、Task Commit 和完整 Branch Review重新绑定最终 diff；确认 #434 graph 未激活，且 release/tag/GitHub Release 与业务生产验证没有被宣称通过。 |

## 当前证据状态

- 本文件创建和 promotion 时只完成 task planning 与 contribution authoring；当时
  `T452-01..12` 均为 `not_executed`。该状态是历史快照，不再代表当前执行结果。
- 当前 shared RDT authority 为 `current-main-0.6.17-guru.58/active`；`.57` 是 immutable predecessor，Architecture shared current 仍为 `.57/active`。
- `T452-01..11 = passed`：核心 inventory/installer/ownership/native/upgrade 测试
  `180 passed`；Finalizer provenance `20 passed`；workflow mode 与 extension verification
  `22 passed`；throwaway Python routing `44 passed`；ownership、dogfood drift、显式
  OpenCode 1.18.30 actual-load，以及单个 Codex focused clean/update/reapply 均通过。
- `T452-12 = in_progress`：fresh RDT 已重绑定当前候选；Task Commit、完整 committed-range
  Branch Review、Publication 与 Finalizer 尚未执行。#434 graph 未激活，release/tag/GitHub
  Release 与业务生产验证未宣称通过。

## 未验证边界

- 正式 release/tag/GitHub Release、发布后 tag-pinned smoke 与业务仓库生产升级不属于 Issue #452 本轮验证。
- #434 Delivery/Completion/Closure/Finish production graph activation 不属于本 contribution，不得由平台测试间接激活。
- 当前环境缺少某个平台 CLI 时，只能记录该 native actual-load 的环境边界；不能把静态目录存在或文件相等写成 actual-load PASS。
