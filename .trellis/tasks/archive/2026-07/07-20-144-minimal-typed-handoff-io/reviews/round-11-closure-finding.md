# #144 Branch Review Round 11 问题闭环审查报告

## 审查元数据

- 审查身份：`/root/issue_144_round10_replacement_review`
- 逻辑角色：`问题闭环审查代理`
- 复用决定：`reuse-for-closure`
- 审查 HEAD：`7f5a325896c2819b4353b2da2e1c5635182ec930`
- 基线与 merge-base：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 完整范围：`origin/main...HEAD`
- Diff 规模：100 个文件，23291 行新增、352 行删除，7 个 task work commits
- 当前提交：`fix(trellis): #144 对齐可移植 pattern 语义`
- 问题计数：P0=0、P1=0、P2=0、P3=1，`findings_count=1`
- 建议原始报告路径：`.trellis/tasks/07-20-144-minimal-typed-handoff-io/reviews/round-11-closure-finding.md`
- 审查方式：全程只读；未编辑文件，未调用 Guru recorder、validator、review gate、commit、push、PR 或 finish-work。

## 审查范围

本轮以 Round 10 原始报告中的 `F-BR-P3-011` 为闭环对象，重新审查了 approved
`prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、
`implementation-handoff.md` 第 17-18 节、最新 `phase2-check.json`、
commit plan 007、issue scope ledger、canonical/dogfood runtime、portable pattern
合同、固定测试矩阵及完整 `origin/main...HEAD` diff。

同时复核了 Issue #144、#145、#146 的 live 状态与范围关系。三者均为 OPEN；
ledger 只将 #144 列入 `close_issues`，#145/#146 保持 `followup_issues`，分类正确。

## 问题

### [P3] F-BR-P3-011：portable compiler 仍未实现其声明的 Node `u` 搜索位置语义

- 编译器：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15504`
- `$` 转换：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15664`
- 实例匹配：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:16126`
- 固定测试矩阵：
  `trellis/skills/guru-team/tests/test_skill_packages.py:848`
- Node 对照测试：
  `trellis/skills/guru-team/tests/test_skill_packages.py:935`
- 合同语义：
  `.trellis/spec/workflow/skill-package-contract.md:347`
- 完整矩阵要求：
  `.trellis/spec/workflow/quality-guidelines.md:106`

Round 11 已正确关闭原始 trailing-newline 复现：

```text
schema   = {"type":"string","pattern":"^[a-z]+$"}
instance = "a\n"

当前 runtime -> pattern violation
Node/Ajv        -> false
```

但 accepted grammar 仍存在正常路径差异。最小复现为：

```text
pattern  = "(?!^|$)"
instance = "😀"
```

当前 canonical runtime：

```text
skill_json_schema_subset_errors(...)     -> []
compiled Python pattern                  -> "(?!^|\Z)"
skill_json_schema_validation_errors(...) -> ["probe violates pattern at $"]
```

Node 20-compatible `RegExp`：

```text
new RegExp("(?!^|$)", "u").exec("😀") -> [""], index=1
new RegExp("(?!^|$)", "u").test("😀") -> true
```

Ajv 6.12.6：

```text
valid=true
errors=null
```

JavaScript 字符串按 UTF-16 code unit 编址。Node 的 unanchored search 可以在 astral
字符 surrogate pair 内部的 UTF-16 index 1 找到零宽匹配。Python Unicode 字符串将
`"😀"` 视为一个 code point，只存在开始和结束两个搜索位置；转换后的
`(?!^|\Z)` 在这两个位置均失败。

因此，虽然语法翻译修复了 `$`、dot、whitespace 等已知差异，使用 Python `re.search()`
执行翻译结果仍不能完整实现 durable SSOT 声明的
`new RegExp(pattern, "u").test(instance)` 语义。

## 合同与测试缺口

`skill-package-contract.md` 的 exact EBNF 明确接受 negative lookahead，并明确规定
matching 等价于 Node Unicode RegExp。该复现完全落在已声明的合法 grammar 内，不涉及
Python-only syntax、恶意篡改、竞态、TOCTOU 或 fault injection。

现有固定矩阵分别覆盖了普通 negative lookahead 和 astral dot，却没有覆盖
“零宽 assertion + astral input + unanchored search”的组合。Node 对照测试只遍历该固定
矩阵，所以即使测试绿色也无法发现此差异。

初步生成对照曾覆盖 870 个 accepted patterns × 100 个 values，共 87000 次 Node `u`
比较且无 mismatch；扩大到嵌套 assertion 后才发现本例。这说明当前 Phase 2 所称
202500 次 differential 仍未覆盖完整 legal semantic class，不能据此证明
`F-BR-P3-011` 已关闭。

## 影响与范围判断

该差异会使 interface 1.3 source/installed validator 拒绝一个由标准 Node/Ajv consumer
按公开合同接受的 DTO 值，破坏 #144 对 accepted constraint、example validation 和
跨 consumer 可移植性的承诺。

缺陷位于 #144 新增的 validator 基础设施内。#145/#146 只负责九个 production Skill
payload migration，不能承接该 correctness 缺口。因此本项继续作为原
`F-BR-P3-011` 的 current-scope P3，不另建 unrelated finding，也不得降级为 observation
或 follow-up。

最新 `phase2-check.json` 将该 finding 标记为 resolved 并返回 `typed_exit=passed`，
但该结论已被上述独立正常路径复现反驳，不能支持 passing Branch Review Gate。

## 修复要求

可选择以下一种有明确证明的方向：

- 收窄 portable grammar，机器拒绝会暴露 UTF-16 interior zero-width 搜索语义且无法由
  Python code-point matcher 等价执行的 pattern。
- 实现真实的 ECMA Unicode search-position 行为，使 accepted grammar 在 UTF-16 搜索位置、
  code-point consuming 与零宽 assertion 上均与 Node 一致。

不得仅为本例增加特殊判断，也不得继续用固定 expected-value 表替代独立 consumer 对照。

至少增加以下回归：

- `pattern="(?!^|$)"`、`instance="😀"` 必须与 Node `u` 一致。
- 覆盖 astral 字符前、中、后的零宽匹配位置。
- 覆盖 negative lookahead、anchors、alternation、empty alternative 和量词产生的零宽路径。
- 对生成的全部 accepted patterns 加入 astral、BMP、line terminator 与混合字符串矩阵。
- grammar gate 与 runtime matcher 继续共用同一 accepted subset，且 canonical/dogfood/
  installed bytes 保持一致。

修复后必须重新执行完整 Phase 2、installer、throwaway/update/reapply 和 Branch Review，
不能复用本轮 `phase2-check.json`。

## 既有问题生命周期

- Round 1：4 个 P2。
- Round 2：2 个 P2。
- Round 3：前序问题闭环，零 finding。
- Round 4：新增 2 个 P2。
- Round 5：Round 4 与 Phase 2 findings 闭环，零 finding。
- Round 6：新增 `F-BR-P2-008` 与 `F-BR-P3-009`。
- Round 7：前述问题关闭，但新增 `F-BR-P3-010`。
- Round 8：`F-BR-P3-010` 闭环，零 finding。
- Round 9：平台中断，partial output 不具备 gate 效力。
- Round 10：确认 `F-BR-P3-011` 为 open current-scope P3。
- Round 11：原 trailing-newline reproduction 已修复，但扩大 accepted-grammar 对照后仍发现
  同一 ECMA portability finding 的零宽 UTF-16 变体；`F-BR-P3-011` 保持 open。

Strict JSON/finite number、RFC 3339、year 0000、IPvFuture `V/v`、RFC 3986 URI 与
IPv6 zone-ID 修复均保持关闭，未发现回归。

## Docs SSOT

Docs 策略继续为 `complete_docs + ssot_first`。Exact portable pattern EBNF 仅由
`.trellis/spec/workflow/skill-package-contract.md` 拥有，其他 durable docs 与公开
README 只引用该合同或规定验证矩阵，未发现新的重复 SSOT。

当前问题是 runtime/test evidence 未满足既有 SSOT，不是需求范围变化。若修复选择收窄
grammar，必须同步 exact EBNF、quality matrix、companion contract 和公开 README；
若保持现有 grammar，则 runtime 与测试必须实现并证明完整 Node `u` 等价性。

## 新鲜验证证据

本轮确认通过：

- Portable pattern 原始 trailing-newline reproduction：已修复。
- 完整 Skill package suite：125/125 passed。
- Shared runtime：548 passed，13 skipped。
- Preset installer：39/39 passed。
- Upstream ownership：6/6 passed。
- Canonical/dogfood runtime byte comparison：passed。
- Canonical/installed/fixture interface 1.3 schema byte comparison：passed。
- Source validator：9 active、9 legacy、0 production minimal、35 exits。
- Installed inventory：384 managed files，0 removal/conflict/sidecar。
- `git diff --check origin/main...HEAD`：passed。
- Source checkout：clean，`main@cbd0396a`。
- Added-line secret pattern scan：0。
- Deployment-path scan：0。

本轮独立 Python/Node/Ajv 探针稳定复现 `F-BR-P3-011` 的剩余差异。上述绿色 suite
没有覆盖该 semantic class，因此不能推翻 finding。

测试完成后 task worktree HEAD 与 merge-base 未变化。工作树仅包含预期的 Branch Review
及 task commit plan metadata，没有新的 non-metadata drift。

## 开箱即用与 Upgrade/Update

现有 evidence 覆盖 clean init、workflow preview/switch、preset 初装、
`trellis update`、preset reapply、三平台分发、source/installed validator、ownership
检查与最终零 sidecar。未发现新的 installer、overlay drift 或 upgrade/update 分发缺陷。

Canonical 与 installed runtime 字节一致也意味着该 finding 会原样进入 clean preset
installation；分发一致性不能证明 matcher semantics 正确。

Feature branch 尚未 push，immutable exact remote feature-ref marketplace verification
继续按批准边界 deferred 到 post-push/pre-PR。该项不计作 finding。

## 兼容性、部署与安全

九个 production Skills 仍全部为 interface 1.2 + `legacy`，production
`minimal_handoff=0`；#145/#146 migration 边界与现有 typed exits 未被提前改变。

完整 diff 不涉及 CI/CD、Docker/Compose、Kubernetes/Kustomize、数据库 migration、
Makefile、service、API、worker 或部署配置，无服务部署、数据迁移或配置迁移影响。

未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始
记录泄漏。复现使用普通 accepted schema 与 Unicode 字符串，属于
honest-but-fallible 正常运行路径。

## 观察项与后续候选

- 观察项：exact remote feature-ref marketplace verification 保持 post-push/pre-PR，
  不阻塞当前本地实现审查。
- 后续候选：无。`F-BR-P3-011` 属于 current scope，不能移交 #145/#146。

## 结论

Round 11 问题闭环审查不通过：

- P0=0
- P1=0
- P2=0
- P3=1
- `findings_count=1`

`F-BR-P3-011` 尚未关闭。不得记录 passing Branch Review Gate，不得进入
`trellis-finish-work`、push、PR 或关闭 #144。

应返回实现并重新执行完整 Phase 2。由于本 closure round 仍发现问题，本审查身份成为该
finding 的当前 owner；后续必须先完成新的 closure review，确认零 finding 后，才能调度
从未参与此前轮次的新 `最终放行审查代理`。
