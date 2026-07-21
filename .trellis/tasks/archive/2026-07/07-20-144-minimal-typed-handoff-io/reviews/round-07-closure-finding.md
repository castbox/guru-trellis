# Round 7 问题闭环审查报告

## 审查元数据

- 逻辑角色：`问题闭环审查代理`
- 技术身份：`/root/issue_144_round6_final_release`
- 复用决定：`reuse-for-closure`
- Reviewed HEAD：`ced2c724d7fc69e2ccddf2a9cbdaf7d8a6cf0866`
- Base：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- Diff：98 files，21360 insertions，256 deletions，5 commits
- 审查方式：只读完整 diff 与独立标准边界复核
- 问题计数：P0=0、P1=0、P2=0、P3=1，`findings_count=1`

## 问题

### F-BR-P3-010：RFC 3986 URI 校验错误接受 IPv6 zone ID

- 严重度：P3
- 状态：open
- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15409`
- 同步副本：`.trellis/guru-team/scripts/python/guru_team_trellis.py`
- 当前实现把未匹配 IPvFuture 的 IP-literal 直接交给 `ipaddress.IPv6Address(literal)`。Python 3.12 的该 API 接受 scope/zone ID，但 RFC 3986 §3.2.2 的 `IPv6address` 与 `IPvFuture` grammar 不包含 `%` zone ID。
- 正常 authoring 路径复现：`skill_json_schema_validation_errors(value, {"type":"string","format":"uri"}, ...)` 对 `http://[fe80::1%eth0]/`、`http://[fe80::1%25eth0]/`、`http://[fe80::1%1]/` 均返回 `[]`。
- 独立证据：RFC 3986 ABNF 不允许上述 literal；Ruby `URI::RFC3986_Parser` 对三个值均返回 `URI::InvalidURIError`。
- 现有 URI 测试覆盖普通 IPv6、IPvFuture、坏 authority、端口和 percent encoding，但没有覆盖 zone ID，因此全量绿色测试未捕获该问题。
- 影响：1.3 contract validator 可接受不满足 durable SSOT 所声明 RFC 3986 generic syntax 的 `uri` 实例，构成当前范围 Docs SSOT 不一致。
- 修复要求：在调用 `IPv6Address` 前拒绝 scope/zone ID，或用严格 RFC 3986 IPv6 grammar 包装该调用；为 raw `%`、`%25` 和数字 scope 增加负例，并同步 canonical/dogfood runtime。

## 问题生命周期

- `F-BR-P2-008`：strict JSON loader、finite guard、`allow_nan=False` 已覆盖 schema/example/interface/registry/ref/marker/stdout/in-memory/public DTO；状态=`closed-by-round-7`。
- `F-BR-P3-009`：lowercase `t/z`、calendar、offset、leap-second position、URI whitespace/percent/authority 等原始问题已关闭；状态=`closed-by-round-7`。
- `F-P2-R7-P3-001`：year `0000` 与 proleptic Gregorian calendar 已关闭；状态=`closed-by-round-7`。
- `F-P2-R7-P3-002`：大小写 IPvFuture `V/v` 已关闭；状态=`closed-by-round-7`。
- `F-BR-P3-010`：IPv6 zone ID 被错误接受；状态=`open`；finding owner=`/root/issue_144_round6_final_release`。

## 需求与 Issue 范围

- GitHub #144、#145、#146 均为 OPEN。
- `issue-scope-ledger.json` 仅把 #144 列入 `close_issues`，#145/#146 保持 `followup_issues`；当前分类正确。
- `F-BR-P3-010` 直接影响 #144 所拥有的 interface 1.3 public contract validator 与 RFC 3986 format semantics，属于 current scope，不能转移给 #145/#146。

## Docs SSOT

- Durable specs 已声明 supported `uri` format 必须执行 RFC 3986 generic syntax。
- 当前 runtime 对 IPv6 zone ID 的接受行为与该 SSOT 不一致，因此是阻塞 finding，不是观察项或后续候选。
- 九个 production Skills 仍保持 interface 1.2 + `legacy`，#145/#146 的 payload migration 边界未改变。

## 验证证据

- Targeted strict JSON/RFC tests：9/9 passed。
- Skill package suite：122/122 passed。
- Shared runtime：548 passed，13 skipped。
- Preset installer：39/39 passed。
- Upstream ownership：6/6 passed。
- Canonical/dogfood runtime SHA-256 均为 `de1f5a6d9fe96be3a4c1fabfd1868333e8b77e7159b6e1846e85079fffc0cd1d`。
- Installed manifest：384 files 全部 hash/source identity 匹配；sidecars=0、removals=0、conflicts=0。
- `git diff --check origin/main...HEAD` 通过。
- Source checkout clean；task worktree 仅有父流程维护的 review/commit-plan metadata。

## Upgrade / Update 与开箱即用

- Canonical 与 dogfood runtime 同步，installer inventory 与 sidecar 门禁通过；因此该 finding 会一致进入新安装仓库，不能用副本一致性冒充 RFC 3986 语义正确。
- 当前 feature branch 尚未 push，exact remote feature-ref marketplace verification 无法执行，必须保留为 push 后、PR 前的发布门禁。

## 部署与安全

- Secret scan 无命中。
- 完整 diff 不涉及 CI/CD、container、K8s、migration 或 Makefile，无服务部署、配置迁移或数据迁移影响。
- Finding 可在正常 package authoring 路径复现，不依赖恶意篡改、攻击模型、竞态或 fault injection。

## 观察项

- Exact current-feature-ref marketplace verification 尚待 reviewed branch push 后执行；这不是当前 Phase 2/Branch Review finding 的替代证据。

## 后续候选

- Issue #145 与 #146 继续负责九个 production Skill payload migration；不得由 #144 当前 PR 关闭。
- 本轮未新增独立 follow-up issue；`F-BR-P3-010` 属于 #144 current scope，必须在当前 task 内关闭。

## 结论

Round 7 为 closure finding，不是 closure pass，更不是最终放行。当前 P0=0、P1=0、P2=0、P3=1，Branch Review Gate 必须继续阻塞。

应返回实现与完整 Phase 2，提交新的 finding-fix commit，再由本 technical finding owner 完成零 finding 闭环；之后仍必须派发从未参与前序轮次的全新 `最终放行审查代理` 审查最新完整 HEAD。
