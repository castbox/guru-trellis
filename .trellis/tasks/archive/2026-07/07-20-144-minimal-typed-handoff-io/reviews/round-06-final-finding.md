# #144 Branch Review Round 6 最终放行审查原始报告

## 审查元数据

- 审查身份：`/root/issue_144_round6_final_release`
- 逻辑角色：`最终放行审查代理`
- 复用决策：`new-agent`，未参与 Round 1-5
- 审查 HEAD：`61a78a90909db38bf18d59d32cf03dd712a21e1c`
- 基线：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 范围：完整 `origin/main...HEAD`
- 规模：97 个文件，19824 行新增、193 行删除，4 个 task work commits
- 提交：`66ddb160`、`535536db`、`b7588935`、`61a78a90`
- 问题计数：P0=0，P1=0，P2=1，P3=1，`findings_count=2`
- 审查方式：只读；未修改任何文件，未运行 Guru Team recorder、validator、review gate、finish、push 或 PR 命令。

## 审查范围

已从零审查 live #144、#145、#146，任务 `prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、`implementation-handoff.md`、`phase2-check.json`、`issue-scope-ledger.json`、`task-commit-plans/004.json`，以及 Round 1-5 原始报告和问题生命周期。

代码审查覆盖 interface 1.3 schema、registry 1.1、extension public API、canonical/dogfood runtime、representative fixture、projection、consumer owner locator、discovery、installer、managed inventory、selected-platform 分发、throwaway/update/reapply 边界和四个完整提交。

## 问题

### [P2] F-BR-P2-008：默认 JSON 解码允许非有限数绕过 public contract 验证

- 主路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15197`
- 相关路径：同文件 `15418`、`15546`、`15672`、`16767`
- Dogfood 安装副本存在相同行为。

`skill_read_json()` 使用 Python 默认 `json.loads()`。该解码器接受标准 JSON 不允许的 `NaN`、`Infinity` 和 `-Infinity`。随后 closed-subset grammar 只按 Python `int|float` 判断 numeric keyword，实例校验也把非有限 float 当作 `number`；对 `NaN` 的 minimum/maximum 比较均为 false。代表 invocation stdout 同样使用默认 `json.loads()`。

只读内存探针结果：

```text
{"x":NaN}      custom validation errors=[]
{"x":Infinity} custom validation errors=[]
```

正常复现不需要伪造 artifact 或攻击输入：1.3 Skill 作者可因浮点计算或 Python 默认序列化，在 output example 或 invocation stdout 中得到 `NaN`；若字段 schema 为 `type=number, minimum=0`，当前验证链会通过。`json.dumps()` 又会默认重新输出 `NaN`，其他严格 JSON consumer 无法解析。

这破坏 live #144 对 schema/example 可解析性、稳定 discovery、单一 typed-exit DTO 和 Draft 2020-12-compatible closed contract 的承诺。相同缺口会随 preset 安装到新仓库，绿色 source/installed 检查不能证明该合同可移植。

修复方向：

- 为 contract asset、interface、example 和 invocation stdout 使用拒绝非标准 constants 的严格 JSON loader。
- 对内存中的 schema/instance 数字执行显式 finite 检查，或采用不会把合法大指数静默转换为 infinity 的精确数字解析策略。
- Public DTO 序列化使用 `allow_nan=false` 等等价 fail-closed 行为。
- 增加 schema keyword、static example、invocation stdout 和 installed validation 回归测试。

### [P3] F-BR-P3-009：声明支持的 `date-time` / `uri` format 未实现兼容语义

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15550`
- 测试缺口：`trellis/skills/guru-team/tests/test_skill_packages.py:793`

Closed subset 把 `date-time` 和 `uri` 列为支持的 format，但 `format_matches()` 使用自定义正则、`datetime.fromisoformat()` 和宽松 `urlsplit()`，与声明的标准语义不一致。

正常探针结果：

```text
2020-01-01t00:00:00z       标准 date-time 有效，custom 拒绝
1990-12-31T23:59:60Z       RFC 3339 leap second 有效，custom 拒绝
foo: bar                   含裸空格的 URI 无效，custom 接受
https://exa mple.com       含裸空格的 URI 无效，custom 接受
```

现有测试只覆盖非字符串 format 和 unsupported format，没有验证两个已支持 format 的合法/非法实例域。这会让正常 package authoring 出现错误拒绝或错误通过，与 Round 4 后 durable Docs 所称“每个 accepted constraint 均被执行”的合同不一致。

修复应选择其一：完整实现并测试相应标准语义，或在实现完整前从 closed supported format 集合中移除并稳定拒绝，不能继续宣称支持但执行不同语义。

## 问题生命周期

- Round 1：4 个 P2。
- Round 2：关闭 3 项，重新打开 `F-BR-P2-001`，新增 `F-BR-P2-005`。
- Round 3：上述问题及 fresh Phase 2 三项全部关闭。
- Round 4：新增 consumer-owned root 与 Draft closed-subset 两个 P2。
- 最终 Phase 2：又识别 recursive refs、canonical locator、root-only `$id`、integer、format 类型和 `additionalProperties` 六项。
- Round 5：确认 Round 4 两项及 Phase 2 六项均关闭。
- Round 6：前述关闭结论不回退；新发现 `F-BR-P2-008` 和 `F-BR-P3-009`，当前仍 open。

## 需求与 Issue 范围

Live #144、#145、#146 均为 OPEN。#144 明确拥有 public I/O 基础设施、schema/example 验证和 closed negative matrix，因此本轮两项都属于 current scope，不能降级给 #145/#146。

九个 production Skills 仍精确保持 interface 1.2 + `legacy`，typed exits 和 runtime route 未迁移；representative 1.3 fixture 未进入 production registry、mandatory workflow 或平台安装根。#145、#146 的 migration 职责保持不变。

`issue-scope-ledger.json` 仅把 #144 列入 `close_issues`，#145/#146 为 follow-up，related issues 不使用关闭语义；分类正确。但本轮 finding 未清零，当前 HEAD 不具备关闭 #144 的验收条件。

## Docs SSOT

Docs SSOT Plan 为 `complete_docs + ssot_first`。`skill-package-contract.md`、`companion-scripts.md`、`data-contracts.md` 和 `quality-guidelines.md` 已正确声明 consumer ownership、recursive closed subset、malformed input fail closed、1.2/1.3 边界和 #145/#146 migration。

当前差距是 runtime 未完整承接“严格 JSON + supported format semantics”，不是任务文档缺失。若修复选择缩减支持的 format 集合，需同步上述 durable SSOT；否则补代码与测试即可。

## 验证证据

本轮实际执行：

- Skill tests：113/113 passed。
- Shared runtime：548 passed，13 skipped。
- Installer：39/39 passed。
- Ownership：6/6 passed。
- `git diff --check origin/main...HEAD`：通过。
- Canonical/dogfood runtime、registry、1.3 schema：逐字节一致。
- Installed manifest：384 个 managed files 全部存在且 SHA-256 匹配；0 missing、mismatch、conflict、removal、sidecar。
- Secret scan：private key、GitHub/OpenAI/AWS token、数据库 URL、签名 URL 均为 0。
- Deployment path scan：CI/CD、container、Compose、K8s/Kustomize、migration、Makefile 均无命中。
- Source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis`：clean。

因角色限制，本轮未直接调用 `check-skill-packages` 等 Guru Team validator；113 项 Skill tests 已覆盖其 source/installed 代码路径，Round 5/Phase 2 的既有 validator evidence 也已逐项审阅。绿色回归未覆盖本报告的非有限 JSON 和 format 语义反例。

## Upgrade / Update / 开箱即用

Installer 已包含 interface 1.3 schema、discovery wrapper、consumer-owned roots、registry 1.1 和 managed provenance；现有 public-sample throwaway evidence 为 exit 0，覆盖 init、preview/switch、update、reapply 和零 sidecar。

但 installed runtime 与 canonical runtime 字节相同，因此两个 finding 会原样进入干净安装仓库，当前不能宣称 #144 的 public contract 开箱即用验收通过。

当前 feature branch 尚未 push；exact feature-ref marketplace verification 仍未执行。默认 verifier 以 exit 2 fail closed，符合设计。该项只能在 reviewed branch push 后由 Remote Marketplace Verification Gate 补证，不得冒充已验证。

## 部署与安全

完整 diff 不涉及 CI/CD、Docker/container、Compose、Kubernetes/Kustomize、数据库 migration 或 Makefile，无服务部署、配置迁移或数据迁移影响。

未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录泄漏。两个 finding 都可在正常 honest-but-fallible package authoring 路径复现，不依赖恶意篡改、攻击模型、竞态、TOCTOU 或 fault injection。

## 结论

Round 6 最终放行审查不通过：P0=0、P1=0、P2=1、P3=1，`findings_count=2`。

不得记录 passing Branch Review Gate，不得进入 `trellis-finish-work`、push、PR 或关闭 #144。应返回实现修复两项问题，补 targeted/full regression，重新执行完整 Phase 2，创建 finding-fix commit，并完成新的问题闭环和最终放行审查。
