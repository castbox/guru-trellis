# Phase C Migration And Retirement Ledger

## 1. Rule

Phase C只建立target-native substrate与package-ready contracts。Current production predecessor继续运行，直到
Phase D443、Phase D436完成package migration，随后Phase E434在一个activation transaction中切换并退役旧面。

`retain_until_phase_e`不表示兼容支持；它表示Phase C禁止半切production graph。新substrate对这些predecessor
保持零读取零写入。

## 2. Closed disposition

| Asset/capability | Phase C disposition | Phase D owner | Phase E exit condition |
| --- | --- | --- | --- |
| `guru-create-task-workspace` package/id/command | `retain_until_phase_e` | new `guru-create-task` package由Phase C完成 | selector切到new package后删除old id/command |
| `task-workspace-plan/result/recovery` schemas | `retain_until_phase_e` | none; new schemas不复用old ids | old consumer count=0后删除 |
| task/workspace mapping writers | `retain_until_phase_e` | Phase D443/D436移除各自writer依赖 | global writer count=0后删除 |
| task/workspace mapping readers/repair | `retain_until_phase_e` | Phase D443/D436移除各自reader依赖 | global reader count=0后删除 |
| path-bearing session payload | `replace_in_fork_then_d443` | Phase D443 Bind major | new Bind selector active且old schema consumer=0 |
| `task.json.worktree_path/meta.worktree_path` authority | `stop_reading_in_new_code` | Phase D443/D436 consumers | all production consumer count=0；tracked legacy bytes保留 |
| `task.json.branch/meta.branch` authority | `stop_reading_in_new_code` | Phase D443/D436 consumers | branch association active；legacy field只作non-authority history |
| `base_head/entry_head/source_checkout` authority | `stop_reading_in_new_code` | affected package owners | live operation DTO consumers complete，old reader count=0 |
| Bind Interface 1.4 inputs/outputs | `out_of_phase_c` | Phase D443 | new major selector/routers原子激活 |
| Reactivate/Completion/Closure/Finish/Cleanup majors | `out_of_phase_c` | Phase D436 | migrated interfaces与routers原子激活 |
| #434 workflow graph/targets/stops | `forbidden_in_phase_c` | none | Phase E434 fresh reconcile通过 |
| registry selectors | `forbidden_in_phase_c` | none | Phase E434 package-ready gate通过 |
| active extension manifest | `forbidden_in_phase_c` | none | Phase E434 complete inventory通过 |
| installed/platform projection bytes | `forbidden_in_phase_c` | package source prepared by C/D | Phase E434 atomic publication与parity通过 |

## 3. Compatibility contract

Phase C不支持以下中间态：

- old package读取new store；
- new package读取old mapping；
- session dual-read或dual-write；
- old/new public id alias；
- registry选择new package但workflow仍走old edge；
- installed/platform bytes先于active manifest/selector切换；
- Guru overlay修改Fork生成文件。

Phase C branch自身允许old predecessor与inactive new canonical bytes并存，原因只有一个：production selector仍唯一
指向old predecessor。Phase E activation完成后old predecessor必须删除，不转为长期deprecated compatibility。

## 4. Verification queries

实施时维护封闭query set：

- old mapping reader count；
- old mapping writer count；
- old public id consumer count；
- path-bearing session schema consumer count；
- removed task metadata authority reader count；
- active registry selector count；
- workflow producer/consumer count；
- installed/platform mixed-major count。

Phase C acceptance只要求“new code counts = 0”和“active selectors unchanged”。Phase E acceptance要求上述old/mixed
counts全部为0，并独立证明new graph完整。
