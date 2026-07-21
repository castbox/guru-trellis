# #144 Branch Review Round 10 替代问题发现审查报告

## 审查元数据

- 审查身份：`/root/issue_144_round10_replacement_review`
- 逻辑角色：`问题发现审查代理`
- 调度类型：Round 9 被 platform interrupt 后的 replacement reviewer
- 前任终止事件：`evt-0199-f9642805a3`
- 审查 HEAD：`1338505df40aeb746af3a5f36c114a0877f85c2d`
- 基线与 merge-base：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 完整范围：`origin/main...HEAD`
- Diff 规模：99 个文件，21984 行新增、256 行删除，6 个 task work commits
- 问题计数：P0=0、P1=0、P2=0、P3=1，`findings_count=1`
- 审查方式：全程只读；未编辑文件，未调用 Guru recorder、review gate、finish、push 或 PR 命令。

## 审查范围

本轮重新读取了 live Issue #144、#145、#146，approved `prd.md`、`design.md`、
`implement.md`、Docs SSOT Plan、`implementation-handoff.md`、最终
`phase2-check.json`、`issue-scope-ledger.json`、commit plan 006，以及 Round 1-8
全部原始报告和 finding 生命周期。

代码审查覆盖 interface 1.2/1.3、registry 1.1、extension public API、closed schema
grammar 与实例校验、consumer ownership、projection totality、public/private 分层、
representative fixtures、discovery/invocation、canonical/dogfood runtime、preset
installer、selected-platform 分发、throwaway/update/reapply 合同和完整六个提交。

同时重新读取 Trellis 官方 workflow 与 spec marketplace 文档。当前实现仍使用官方
Markdown workflow、marketplace、preset 与项目本地扩展面，没有修改 Trellis upstream、
全局 npm 包、`node_modules` 或用 hook/script 承担 semantic judgment。

## 问题

### [P3] F-BR-P3-011：`pattern` 使用 Python 正则语义，错误接受 Draft/ECMA consumer 拒绝的字符串

- 主路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15900`
- Grammar 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15652`
- Dogfood 副本：`.trellis/guru-team/scripts/python/guru_team_trellis.py`
- 测试缺口：`trellis/skills/guru-team/tests/test_skill_packages.py:831`

Closed subset 将 `pattern` 列为 accepted Draft 2020-12 constraint。Schema grammar
使用 Python `re.compile()` 判定 pattern 合法性，实例校验使用 Python `re.search()`。
这既没有验证 ECMA-262 pattern dialect，也继承了 Python 与 JSON Schema consumer
不同的 anchor、字符类和正则语法语义。

最小正常路径复现：

```text
schema  = {"type":"string","pattern":"^[a-z]+$"}
instance = "a\n"

skill_json_schema_subset_errors(...)     -> []
skill_json_schema_validation_errors(...) -> []
Node new RegExp("^[a-z]+$").test("a\n")  -> false
Ajv 6.12.6 validate("a\n")               -> false, keyword=pattern
```

这里的换行通过标准 JSON 字符串转义进入普通 schema example、public input/output 或
invocation stdout，不需要手工篡改 artifact、恶意输入、竞态、TOCTOU 或 fault injection。
Python `$` 会在最终换行前匹配，而无 multiline flag 的 ECMA `$` 不会。

当前负例只证明 Python 自身拒绝未闭合 `"("`，没有覆盖 Python-only pattern、
ECMA-valid pattern、最终换行、`\d`/`\w` 字符域或其它跨 dialect 边界。因此完整 122 项
Skill suite 和 source/installed validator 均会绿色通过该反例。

影响是 1.3 source/installed validator 可以接受一个 public DTO/example，而按声明合同
运行的 workflow、Skill 或 stop consumer 使用标准 JSON Schema/ECMA validator 时会拒绝
同一值。这样会破坏 #144 对 Draft-compatible accepted constraints、example 可验证性、
thin projection 和跨 consumer 可移植性的承诺。Canonical 与 dogfood runtime 字节一致，
所以缺陷会原样进入 clean preset installation。

该问题属于 #144 current scope。#145/#146 只负责 production Skill payload migration，
不能承担 #144 validator 基础设施的 correctness 缺口。严重度为 P3，但在当前 issue
验收中阻塞 Branch Review Gate。

修复建议：

- 不要继续把任意 Python `re` pattern 当作 Draft-compatible pattern。
- 使用兼容 ECMA-262 的验证/匹配实现，或定义并机器拒绝一个经证明跨 Python/ECMA
  语义一致的更窄 pattern 子集。
- 若采用窄子集，应在 durable SSOT 明确 exact grammar；不能静默保留
  “Draft 2020-12-compatible”而执行 Python 方言。
- 增加至少以下回归：`^[a-z]+$` 对 `"a\n"` 必须拒绝、Python-only pattern 必须在
  grammar gate 拒绝、合法 accepted pattern 的 runtime 结果须与独立 ECMA validator 一致。
- 同步 canonical/dogfood runtime，并重新执行完整 Phase 2、installer、throwaway 和
  Branch Review。

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
- Round 10：前序关闭结论不回退；新确认 `F-BR-P3-011` 为 open current-scope P3。

Strict JSON/finite number、RFC 3339、year 0000、IPvFuture `V/v`、RFC 3986 URI 与
IPv6 zone-ID 修复均保持关闭，未发现回归。

## Issue 与范围

Live #144、#145、#146 均为 OPEN。Ledger 只把 #144 放入 `close_issues`，#145/#146
保持 `followup_issues`，相关 umbrella 仅使用 related 语义，分类正确。

九个 production Skills 仍全部为 interface 1.2 + `legacy`，production
`minimal_handoff` 数量为 0，现有 typed exits、mandatory routes 与 runtime behavior
未被 #144 提前迁移。由于 `F-BR-P3-011` 未关闭，当前 HEAD 尚不满足关闭 #144 的条件。

## Docs SSOT

Docs 策略仍为 `complete_docs + ssot_first`。Durable
`.trellis/spec/workflow/skill-package-contract.md` 明确把 1.3 schema 定义为
“Draft 2020-12-compatible closed subset”，并声明 accepted `pattern` constraint 会被执行。

当前问题是 runtime 与该 SSOT 不一致，不是规划范围变化。若修复采用显式窄化 regex
grammar，需要同步 `skill-package-contract.md`、`quality-guidelines.md`、
`companion-scripts.md` 及公开 README；若实现 ECMA-compatible semantics，则补充
实现与测试证据即可。无需把任务退回 requirement clarification 或 #145/#146。

## 新鲜验证证据

本轮实际执行并通过：

- Skill package suite：122/122 passed。
- Shared runtime：548 passed，13 skipped。
- Preset installer：39/39 passed。
- Upstream ownership：6/6 passed。
- Source package validator：9 active、9 legacy、0 production minimal、35 exits。
- Installed validator：384 managed files，sidecar/removal/conflict 均为 0。
- Dogfood overlay drift：passed；43 active/frozen entries 与 13 managed claims 通过。
- External `Draft202012Validator.check_schema()`：3/3 passed。
- Canonical/dogfood runtime 与三份 interface 1.3 schema byte comparison：passed。
- Changed Bash `bash -n`、changed JSON `jq empty`、`git diff --check`：passed。
- Source checkout保持 clean，固定在 `main@cbd0396a`。
- Added-line secret/credential/private-key/database-URL/signed-URL scan：0。
- Deployment-path scan：0。

上述绿色结果不覆盖 `F-BR-P3-011` 的实例语义；最小 Python/Node/Ajv 对照探针稳定复现
该差异。

## 开箱即用与 Upgrade/Update

当前 HEAD 的 Phase 2 与 Round 8 evidence 已绑定 public-sample clean throwaway：
覆盖 clean init、workflow preview/switch、初装、`trellis update`、preset reapply、
initial/after-update/no-developer smoke、source/installed/ownership/platform checks 与
最终零 sidecar。本轮重新核对了对应脚本、final-byte hashes、source/installed inventory
和 dogfood drift，未发现 distribution 或 upgrade/update 的第二项缺陷。

但 installed runtime 与 canonical runtime 完全相同，因此 throwaway 绿色只证明分发一致，
不能证明 accepted `pattern` 的 Draft/consumer semantics 正确。

当前 feature branch 尚未 push，exact immutable remote feature-ref marketplace
verification 继续按已批准边界 deferred 到 push 后、PR 前。该项不计作本轮 finding，
也不能替代 `F-BR-P3-011` 的修复。

## 兼容性、部署与安全

现有 1.2 production packages 与 scalar compatibility timeline 未变化，#145/#146 migration
边界保持完整。Finding 影响的是 #144 新增的 1.3 validator contract 和后续迁移前置能力。

完整 diff 不涉及 CI/CD、Docker/Compose、Kubernetes/Kustomize、数据库 migration、
Makefile、service、API 或 worker，无服务部署、配置迁移或数据迁移影响。

未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始
记录泄漏。复现只使用普通 schema 与 JSON 字符串，符合 honest-but-fallible 正常运行范围。

## 结论

Round 10 replacement review 不通过：

- P0=0
- P1=0
- P2=0
- P3=1
- `findings_count=1`

不得记录 passing Branch Review Gate，不得进入 `trellis-finish-work`、push、PR 或关闭
#144。应把 `F-BR-P3-011` 返回实现，补充 Draft/ECMA-compatible pattern grammar 与实例
回归，重新执行完整 Phase 2、创建新的 finding-fix commit，并由 finding owner 完成闭环
审查；闭环后仍需新的最终放行审查。
