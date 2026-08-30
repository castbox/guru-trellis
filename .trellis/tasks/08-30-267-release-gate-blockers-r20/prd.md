# #267 r20 Release Gate blocker 修复需求

## 1. Authority And Current Facts

唯一 current requirement authority 是 live Issue #267 body `2026-08-30-r20`。
本任务从 `main@5650df47fe17fe89b7cb616be6c9551608164832` 开始；该 commit 的
tree 是 `463e78fee7906bca9f80c51aa78097c7ff01af0e`。它包含：

- Issue #311 fix commit `5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8`；
- PR #313 merge commit `21c7da14798683193b460a5e7c5bd24c7c517804`；
- PR #314 merge commit `3efcce72a0d47e38ec725aa8c0f8498992f3416f`。

该 SHA 的 fresh pre-tag 验证确认两个 blocker：

1. standalone `guru-verify-extension-installation` 在 `pre-matrix` 返回
   `blocked/pre_matrix_before_tag_unavailable`。exact-SHA shallow extension source checkout
   缺少 `v0.6.5-guru.10`，matrix 在首个 cell 前以 exit 128 终止。
2. #311 installed-business-repository Finalizer matrix 的首个 `claude-clean` cell 返回
   `provenance_tail_manifest_fields_outside_allowlist`。preset reapply 将
   `skill_packages.files[*].action` 与 `overlays.files[*].action` 从 `installed` 变为
   `unchanged`；当前 manifest diff 把两个 files 容器判定为 allowlist 外变化。其余五个
   matrix cells 尚未运行。

`5650df47...` 是本任务 base 与失败证据绑定的 historical candidate，不是可发布 candidate。
`v0.6.15-guru.3` tag 与 GitHub Release 均不存在。Issue #267 与 Issue #311 均保持 OPEN。

## 2. Goal

修复上述两个 normal-path Release Gate blocker，使修复合并后的 fresh `main` 能重新冻结为
新的 `.3` exact candidate，并从零执行 Issue #267 r20 的完整 pre-tag gates。

## 3. Requirements

### R1 Exact Before-Tag Availability

compatibility matrix runner 必须在任何 matrix cell 开始前完成以下确定性步骤：

1. 解析本地 `before_tag` 的 tag object 与 peeled commit；
2. 本地 tag 缺失时，从当前 source checkout 的 `origin` 精确 fetch 同名
   `refs/tags/<before_tag>`；
3. fetch 后重新解析 tag object 与 peeled commit；
4. 只有两项解析均成功时才进入第一个 matrix cell；
5. remote 缺少该 tag、fetch 失败、tag 仍不可解析或 ref 不是精确 tag 时，返回结构化
   `pre-matrix` failure，不执行任何 matrix cell。

该路径不得创建伪造 tag、不得切换到 mutable branch、不得使用未绑定 exact candidate 的另一个
source checkout、不得把失败转换为 PASS 或 SKIP。

### R2 Closed Provenance Action Transition

Finalizer 与 Publication 的 provenance-tail manifest validator 必须识别两个闭合集合：

- `skill_packages.files`；
- `overlays.files`。

每个集合只有同时满足以下条件时，才把 container diff 分类为合法 provenance transition：

1. before/after 都是 list，长度与顺序相同；
2. 每个位置都是 object；
3. 删除 `action` 后的 object byte-equivalent；
4. before `action` 的值必须是 `installed`；
5. after `action` 的值必须是 `unchanged`。

新增、删除、重排条目，修改 path/source/destination/hash/mode/platform，或使用其它 action
transition 时，validator 必须继续返回
`provenance_tail_manifest_fields_outside_allowlist`。既有 source binding、manifest-only dirty path、
reviewed-content parent、publication head、direct-parent lineage 与 clean checkout 检查保持不变。

### R3 Canonical And Installed Consistency

- canonical `guru-finalize-task` 与 `guru-review-task-publication` 分别拥有自己的 package-local
  validator；两份实现与 owning tests 必须表达同一 closed transition。
- canonical preset matrix runner 是 before-tag fetch 行为的唯一 source owner。
- `.trellis/guru-team/**` dogfood copies 只由 preset apply 生成，禁止手工建立第二实现。
- canonical、dogfood、Shared、Codex、Claude、Cursor projection 的 managed bytes 与 modes 必须通过
  current validators。

### R4 Release And Issue Boundaries

- 本任务不改变 `v0.6.15-guru.3` / extension `0.6.15-guru.39` / Trellis CLI `0.6.15`
  映射。
- 本任务不创建或移动 tag，不创建 GitHub Release，不发布 assets。
- 本任务不关闭 #267、#311、#312 或其它 Issue。
- 本任务不修改业务 repository。
- branch-level test pass 只证明修复实现；它不证明新 exact candidate Release Gate 已通过。
- 修复 PR 合并后，必须从 fresh live remote `main` 记录新的 SHA/tree 并重跑全部 release evidence。

## 4. Exact File Boundary

实现范围固定为：

- `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py`；
- `trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py`；
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/tests/test_contract.py`，仅补
  shallow exact-SHA source regression；
- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`；
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`；
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`；
- `trellis/skills/guru-team/packages/guru-review-task-publication/runtime/owner.py`；
- `trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py`；
- `trellis/skills/guru-team/packages/guru-review-task-publication/references/contract.md`；
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`；
- `trellis/presets/guru-team/spec/workflow/companion-scripts.md`；
- preset apply 生成的 `.trellis/guru-team/**`、`.trellis/spec/workflow/**` 与
  `.trellis/guru-team/extension.json` 对应 managed projection；
- `.trellis/tasks/08-30-267-release-gate-blockers-r20/` 下的本任务文件。

若实现需要修改 public Skill I/O、schema、typed exit、consumer、owner、single-writer、Release identity，
或产生上述边界外的 managed byte、`.new`、`.bak`、未知 sidecar，立即停止并重新进入 scope review。

## 5. Acceptance Criteria

1. 在只含 exact candidate commit、缺少本地 `v0.6.5-guru.10` 的 shallow source fixture 中，
   runner 从 `origin` 精确取得该 annotated tag，解析 tag object 与 peeled commit，并进入 matrix-cell
   stage。
2. local tag 已存在时不执行 fetch；remote tag 缺失或 fetch 后仍不可解析时返回结构化
   `pre-matrix` failure，matrix cell count 为 `0`。
3. Finalizer 与 Publication 均接受两个 files 容器中逐条 `installed -> unchanged`，且只接受
   action 字段变化。
4. Finalizer 与 Publication 均拒绝 `installed -> updated_managed`、`unchanged -> installed`、
   条目增删/重排及任一非-action 字段变化，error code 保持
   `provenance_tail_manifest_fields_outside_allowlist`。
5. provenance tail 仍只有 `.trellis/guru-team/extension.json` 一个 changed path；
   `reviewed_content_head` 不变，`publication_head` 是唯一 direct child。
6. canonical focused tests、installed focused tests、matrix/upgrade contract tests、standalone verifier
   focused tests、preset apply、dogfood drift、package validator、registry/consumer graph、mode、permission、
   managed-byte parity 与 recursive sidecar-zero 全部 PASS。
7. 修复合并后的 fresh exact candidate 上，standalone verifier 返回通过出口；六个 platform/scenario
   matrix cells 全部 PASS，其中 `claude-clean` 不再出现两个 r20 blocker code。
8. 新 candidate 仍包含 `5650df47...`、`5b3b7bef...`、`21c7da147...` 与
   `3efcce72...`；`.3` tag/Release 在独立发布确认前仍不存在。
9. predecessor `.2` 到新 candidate 的 full committed diff review 中，P0/P1/P2/P3 未关闭 finding
   数量全部为 `0`，随后才进入 tag 副作用确认。

## 6. Out Of Scope

- 修改 Trellis upstream、global npm、`node_modules` 或 GitHub provider contract。
- 改变 matrix cell 集合、平台集合、clean/existing 场景定义或 before-state identity。
- 放宽任意 manifest content、source binding、checkout cleanliness 或 publication lineage 检查。
- 引入 dual path、fallback pass、历史 tag fabrication 或 cross-SHA evidence reuse。
- commit、push、PR、merge、tag、Release、Issue closure 或 cleanup。

## 7. Blocking Open Questions

无。
