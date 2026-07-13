# #120 实现交接与 Docs SSOT Reconciliation

## 1. 交接身份与状态

- 实现 owner：`trellis-implement`（本轮 Branch Review finding 修复 owner）。
- Docs SSOT strategy：`ssot_first`。
- 当前结论：实现与本地验证已完成，可交给 `trellis-check` 逐项复核；本文不是
  `phase2-check.json`，也不声明 Branch Review pass。
- 当前生产边界：production registry 仍只有 `guru-create-work-commit` 的
  `reserved` entry，没有 active production skill。

## 2. Primary Implementation Inputs

Durable docs 是本次实现的 primary input。实现前先读取并按以下长期合同工作：

- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `.trellis/spec/workflow/index.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/docs/public-docs.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

这些 durable sources 定义 canonical owner、registry lifecycle、closed-loop
顺序、workflow marker、typed exit、script/AI 边界、managed hash、platform
distribution、upgrade/update 和公共 API。代码实现没有另建第二套 Markdown
流程定义。

Task delta 只作为已经人工确认的 temporary evidence，具体来源为：

- `prd.md` 的 R1-R8、AC1-AC12 与明确范围外边界；
- `design.md` 第 2-12 节的 SSOT、interface、marker、distribution、hash、validator、
  tests、Docs SSOT、兼容性与安全设计；
- `implement.md` 第 2-10 节的 docs-first 顺序、schema/validator/installer/test 与
  throwaway 验证计划；
- `research/architecture-evidence.md` 的官方 Trellis 扩展面和仓库现状证据；
- `reviews/round-001-final-release.md` 的 P1 frontmatter/test evidence finding 与
  P2 handoff evidence finding。

Temporary evidence 只用于确认 durable contract 的当前任务增量，不取代上述
durable docs。

## 3. Durable Docs Sync Result

原始实现已经把以下 task delta 合并到 durable docs：

- canonical root `trellis/skills/guru-team/` 与 generated/installed copy 边界；
- `reserved` / `active` registry lifecycle；
- workflow/standalone mode、entry/freshness/re-entry、固定 closed-loop stages；
- `guru-skill-invoke` / `guru-skill-exit` marker 与唯一 consumer/stop；
- preset platform distribution、previous managed hash、`.new/.bak`、manifest
  inventory 与 `trellis update` reapply；
- `check-skill-packages --mode source|installed` 的 deterministic scope 和 AI
  semantic review 边界；
- stable id/schema/command/lifecycle 的公共 API 与迁移要求。

Branch Review round 1 后又把以下缺口先合并到 durable docs，再修改代码：

- active `SKILL.md` 只有一段闭合 `---` frontmatter；只允许 `name`、
  `description`；name 等于 stable id/registry/interface，description 非空且与
  interface 一致；
- `tests[]` 是 unique package-relative `tests/<file>`，必须为真实 regular file，
  逐组件无 symlink，不能是标签、虚构路径或 tests root 外路径；
- test evidence 属于 package tree，随 installed/platform inventory 分发和校验。

本轮实际同步了：

- `.trellis/spec/workflow/skill-package-contract.md`
- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

其余 durable docs 已逐项复核，现有 owner/流程语义未因本轮 finding 改变，因此
没有机械重复新增同一规则。Sync result 为：durable requirement、spec、public
README、schema、runtime 和 tests 对 frontmatter/test evidence 使用同一合同。

## 4. Code, Schema, Tests And Installer Carryover

- Schema：`skill-registry.schema.json` 将 active `name` 收紧为 public skill id；
  `skill-interface.schema.json` 收紧 `name` pattern，并把 `tests[]` 定义为 unique
  `tests/<file>` 路径，且从字符串起点拒绝任意 `..` 路径段，包括
  `tests/../outside.py`。Canonical、fixture 与 dogfood installed schema bytes 一致，
  最终 interface schema SHA-256 为
  `e3377ced5638ea486335f174fe9604111aedec57dff196d89d76c99b2042036c`。
- Validator：canonical `guru_team_trellis.py` 解析 strict frontmatter，绑定
  registry/interface/SKILL identity 和 description，并对 test evidence 执行
  safe-relative、allowed root、duplicate、existence、regular-file 与逐组件
  `lstat` 校验；malformed input 仍返回 structured `failed/errors`。
- Fixture：`guru-example-action` 仍为 fixture-only active package；registry、
  interface 与 SKILL name 统一为 stable id，description 对齐；新增 package-local
  `tests/test_contract.py`，interface 指向该真实证据。
- Installer：现有 package tree inventory 会复制 package-local tests，无需增加
  语义判断分支；distribution tests 明确断言 shared/Codex copy 和 manifest
  `files[]` 包含 test evidence。
- Regression：覆盖空 SKILL、缺/未闭合/重复/额外 identity frontmatter、name/
  description drift、空 description，以及 tests missing/outside/symlink/wrong
  type/duplicate/parent traversal；reviewer 的空 SKILL 与虚构 tests 是两个独立
  测试场景，`tests/../outside.py` 也有独立 schema 回归。
- Dogfood：preset apply 已同步 canonical runtime 和两份 schema 到
  `.trellis/guru-team/`；known upgrade backup 经 hash/路径核对后处理，第二次 apply
  为幂等且 installed validator 通过。

## 5. Task-History-Only Content

以下内容只保留在 task history，不合并为公共 package 或 durable contract：

- issue/PR 历史检索过程、方案比较和本机执行时间；
- `planning-approval.json`、`agent-assignment.json`、`implement.jsonl`、
  `check.jsonl` 的本次运行状态；
- `reviews/round-001-final-release.md` 与 `review.md` 的 round 1 blocked 事实；
- 本地 throwaway 临时目录、模拟 issue/PR 编号、临时 Git HEAD/digest；
- 本实现交接中的一次性 suite 计数与当前分支验证状态。

这些证据可供 checker 复核，但不得进入公共 skill package、marketplace 或 preset
runtime。

## 6. Verification Evidence

- `python3 -m unittest` skill/package targeted suite：`54/54` passed。
- preset installer suite：`36/36` passed。
- preset + companion + skill/package full suite：`474/474` passed。
- canonical/dogfood `check-skill-packages --mode source`：passed；production
  `reserved_ids=[guru-create-work-commit]`，`active_ids=[]`。
- dogfood `--mode installed`：passed；selected platforms 为 Claude/Codex/Cursor，
  conflict/sidecar 均为 0。
- canonical preset apply：known schema/runtime upgrade sidecar 经核对解决；第二次
  apply 无 installed/updated/backup/conflict，dogfood drift passed。
- clean throwaway：workflow init、preview/switch、preset apply、
  `trellis update --force`、workflow/preset reapply、installed validation、两轮
  installed finish-work 和最终零 `.new/.bak` 全部通过。
- `py_compile`、相关 `bash -n`、changed JSON parse、task validate、planning gate、
  workspace boundary、canonical/dogfood byte comparison、`git diff --check` 通过。

## 7. Follow-Up And Current PR Limitations

- 本 PR 不实现或激活 `guru-create-work-commit`，也不实现 #98、#115 或其它
  business workflow skill。
- 当前修复尚未 commit/push；exact feature-ref marketplace verification 必须等
  reviewed content push 后绑定 remote branch/ref 与 HEAD 执行。本地 throwaway
  明确采样公开 `main`，不能替代该远端 gate。
- 本机官方 Trellis CLI/项目基线仍为 `0.6.5`；npm latest 已观察到 `0.6.6`，本 PR
  没有未经评审升级兼容基线。
- Round 1 `review.md` 继续保持 blocked 历史；实现 owner 不改写 review 结论。
  Checker 必须读取本文和当前 diff，重新执行 Phase 2 语义复核并产生 fresh evidence；
  recorder/validator 不能代替该判断。
- 无 Docker、K8s、DB migration、Makefile 或服务部署影响；存在 public schema、
  validator、preset installed asset 与 platform package inventory 影响。

## 8. Remaining Risk

- exact remote feature-ref install/update 仍待 publish 前 verifier；在该证据产生前
  不得宣称远端开箱验证完成。
- Frontmatter 是刻意收紧的 plain two-field contract，不是通用 YAML；未来若要允许
  多行 YAML、其它 metadata 或 Markdown `---` 分隔线，必须升级公共合同、schema/
  parser/tests 和迁移说明，不能静默放宽。
