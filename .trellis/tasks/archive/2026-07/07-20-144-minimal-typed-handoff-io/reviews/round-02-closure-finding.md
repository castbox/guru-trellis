# #144 Branch Review Round 2 问题闭环审查原始报告

## 审查元数据

- 审查轮次：Round 2
- `logical_role`：`问题闭环审查代理`
- 技术 `agent_id`：`/root/issue_144_closure_review`
- `reuse_decision`：`new-agent`
- Reviewed HEAD：`535536dbd55427241d7ce88cc14629d47fb6d26c`
- Base：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 完整 diff：`origin/main...HEAD`，95 files
- Issue：`castbox/guru-trellis#144`，live state=`OPEN`
- 问题计数：P0=0，P1=0，P2=2，P3=0
- `findings_count=2`
- 审查边界：全程只读，未编辑文件，未运行任何 recorder、review gate、finish、push 或 PR 命令。

## 问题

### [P2] F-BR-P2-001：Skill consumer 仍未绑定 registry 拥有的目标接口

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:16148`
- 当前实现直接接受 producer 声明的任意安全 `interface_path`，随后只检查被读 JSON 的 `id == consumer.id`。它没有根据 registry 中该 target Skill 的 active entry 解析并要求 exact interface path。
- 正常路径复现：在 representative fixture 临时副本的 producer package 中保留一份复制或重构遗留的 `fake-sync-interface.json`，内容沿用 `guru-example-sync` id，再把 `sync_input.contract.interface_path` 指向该副本。完整 `validate_skill_source()` 返回 `status=passed, errors=[]`。
- 此场景不依赖伪造 gate/hash 或攻击者模型，只需正常 package copy/refactor 留下同 id 的 stale contract。
- 影响：producer-owned 或 stale 第三方文件仍可代替 registry 登记的 target-owned input，目标 Skill 后续演进时 handoff 可与真实 consumer contract 脱节。
- 触发依据：Issue #144 consumer ownership、PRD R6、design 4.4，以及 durable contract 的 target-owned input 要求。
- Closure：`reopened`。新增 `skill_input` 和 id 检查是部分修复，但未关闭原 finding 的 ownership 语义。

### [P2] F-BR-P2-005：direct 到 scalar CLI 只验证 example，未证明全域兼容

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:16268`，并见 `16328`。
- 静态 required/source/schema 兼容证明只在 `operation != "direct"` 时执行。Structured direct 有 exact schema equality，但 scalar CLI direct 仅把 declared example 投影后调用 `skill_scalar_value_matches()`。
- 正常路径复现：把 forwarded output 改为 `{exit_id,item}` direct 到 `guru-example-sync` scalar input；`item` schema 允许空字符串，example 保持 `"alpha"`。完整 source validator 返回 `status=passed, errors=[]`，但合法 producer output `{"exit_id":"forwarded","item":""}` 不满足 target scalar `string` 的非空约束。
- 影响：已激活的 1.3 package 可以声明不能覆盖全部合法 producer outputs 的 direct handoff，正常运行时会在唯一 consumer 边界失败。
- 触发依据：Issue #144 direct pass-through、PRD R6、design 4.5，以及 durable contract“direct output 已精确满足 consumer input”。
- Closure：新 current-scope P2；应对 scalar direct 做逐字段全域证明，或禁止 scalar consumer 使用 direct。

## Round 1 Closure

- `F-BR-P2-001`：未关闭，状态=`reopened`，原因见上。
- `F-BR-P2-002`：已关闭。非 direct projection 强制 required source，并对有限值、exact schema、非空字符串、正整数和 ASCII trim 做保守全域证明。
- `F-BR-P2-003`：已关闭。Public/private schema ids 与 paths 分别求交并独立拒绝。
- `F-BR-P2-004`：已关闭。Wrapper 必须绑定唯一 validator 并完整匹配 dispatcher-only bytes；注释、死代码和本地输出均被负例拒绝。
- 六类 package root：已关闭。Canonical、installed、`.agents`、`.codex`、`.cursor`、`.claude` 均由默认环境执行回归覆盖。

## 验证证据

- Skill tests：100/100 passed。
- Preset installer tests：39/39 passed。
- Ownership tests：6/6 passed。
- Source/installed validation：passed，9 legacy、0 production minimal；installed 为 384 managed、0 sidecar/conflict/removal。
- Dogfood drift：passed；43 frozen overlays identity 与 13 managed claims 均通过。
- Clean public-sample throwaway：exit 0，覆盖 init、workflow preview/switch、preset install、`trellis update`、reapply、20/20 tests 和最终零 sidecar。
- Post-commit Phase 2 ancestor audit：`allow_committed_head=true` 时 `typed_exit=passed, errors=[]`。
- 1.2 schema SHA-256 仍为 `33e5daf1...841e`；production package/platform payload 无 diff。
- Python compile、Bash syntax、JSON parse、task validation、workspace boundary、`git diff --check`：通过。
- 两项上述正常 authoring 反例均被当前 validator 错误接受，因此绿色测试不能替代语义 finding。

## Docs SSOT 与范围

- Docs SSOT Plan 为 `complete_docs + ssot_first`；spec、requirements 与三份 README 已同步 Round 1 四项修复。
- 当前代码在 target-owned exact locator 和 scalar direct 全域兼容两处仍未承接 durable contract，存在 Docs SSOT 不一致。
- 九个 production Skills 保持 interface 1.2 + `legacy`；1.3 representative fixture 未进入 production registry、manifest、安装 inventory 或 mandatory workflow。
- Live #145、#146 均为 `OPEN` follow-up；#144 只可关闭自身，related/umbrella issues 不得关闭。

## 观察项与后续候选

- Exact feature-ref marketplace verifier 仍按设计 exit 2，因为分支尚未 push；public marketplace sample 不能冒充 immutable feature-ref evidence。
- Trellis CLI 验证基线为 0.6.5；npm latest 0.6.7 不属于 #144 当前范围。
- 两项 P2 都属于 #144 current scope，不建议拆成新 follow-up issue；#145/#146 边界保持不变。

## 部署与安全

- CI/CD、container、K8s/Kustomize、DB migration 与 Makefile 无 diff，无部署或数据库迁移影响。
- 未发现 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录泄漏。
- Findings 均由受支持的正常 package authoring 路径复现，不依赖 hostile input、竞态、TOCTOU、锁或 fault injection。

## 结论

Branch Review Round 2 阻塞：P0=0、P1=0、P2=2、P3=0，`findings_count=2`。当前 HEAD 不得进入最终放行或 `trellis-finish-work`；应返回实现，修复后重新执行完整 Phase 2，并由新的问题闭环审查代理复核。
