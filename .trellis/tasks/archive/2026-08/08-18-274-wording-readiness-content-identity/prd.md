# #274 修复 wording_current 与 readiness 的目标内容摘要不一致

## 目标

修复 `guru-review-contract-wording:change_request` 的 public transition，使其对同一标题和正文生成与 `guru-review-change-request::normalize_target()` 完全一致的 canonical 内容身份。未漂移的 `clarity_current -> wording_current -> readiness_current` 链路必须直接通过，不再依赖调用方手工替换摘要。

## 已确认事实

- Issue #274 是本 task 的唯一 delivery authority；`issue-scope-ledger.json` 仅包含 `primary=#274`、`close=[#274]`，`related` 与 `followup` 均为空。
- `trellis/skills/guru-team/packages/guru-review-contract-wording/runtime/invoke.py:18-21` 当前选取第一个 `body` scope item，并把正文 SHA-256 同时写入 transition 顶层与内嵌 `wording.target_content_sha256`。
- `trellis/skills/guru-team/packages/guru-review-change-request/runtime/common.py:80-86` 将内容身份定义为 `digest({"title_sha256": <title sha>, "body_sha256": <body sha>})`。
- 当前 Issue #274 正文摘要为 `c84c31a1126817adaca8a9c6c075afb956ebb5d8e07a378b185a49ef52148f8f`，标题与正文的 canonical 组合摘要为 `f7be6c7e4f8791253c5f7644901874228e1b952e3fd4f2776759a2d74361bdf4`；production readiness recorder 已复现 `stale_identity / prerequisite_payloads`。
- `trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py:1400-1434` 当前再次读取 wording owner scope 并手工重算组合摘要，导致 installed transcript 绕过了真实 public producer 缺陷。
- #114 固定 `change_request` scope 必须包含 title 与 body；#101 保留 readiness canonical target ownership；#195 固定 package-local runtime 与 canonical、installed、平台投影分发边界。

## 需求

### R1 Canonical 内容身份

`change_request:pass` public invoke 必须从已检查 owner scope 中精确取得一个 `title` item 和一个 `body` item，并使用现有 canonical JSON digest 规则计算：

```text
digest({"title_sha256": title_item.content_sha256,
        "body_sha256": body_item.content_sha256})
```

transition 顶层 `target_content_sha256` 与内嵌 `wording.target_content_sha256` 必须写入同一个结果。`transition_id` 继续由完整 `wording` projection 派生。

### R2 固定 scope fail closed

title 或 body 缺失、重复，或 scope 无法形成唯一二元组时，public invoke 必须在输出 transition 前以稳定 `stale_identity` 失败，field path 固定为 `owner_result.scope`。禁止选择第一个匹配项或补空值。

### R3 Consumer ownership 不变

`guru-review-change-request::normalize_target()` 的 title+body canonical 规则保持不变。生产 runtime 禁止导入另一个 package 的 private runtime，也不新增 public 字段、schema id、schema version 或兼容分支。

### R4 真实跨 package 回归

installed Phase 0 transcript 必须直接消费 wording public output 中的 `target_content_sha256` 构造 readiness prerequisites，并真实调用 production `record-change-request-review` 与 `check-change-request-review`。测试禁止在 caller 中再次从 owner scope 重算目标内容身份。

### R5 漂移与结构负例

回归必须分别覆盖 title-only 漂移、body-only 漂移、缺失 title、缺失 body、重复 title 和重复 body。内容漂移必须由 readiness 的现有 identity linkage 拒绝；结构异常必须由 wording invoke 在 projection 前拒绝。

### R6 分发与文档

Canonical package 是实现来源；preset apply 负责同步 installed dogfood、Shared、Codex、Claude 与 Cursor public projection。平台 public projection 禁止出现 private runtime、tests 或 errors。Package contract 与 Phase 0 data contract 必须明确 title+body canonical 内容身份及唯一 scope 条件。

## 验收标准

1. 非空 title/body 的 wording public output 两处内容摘要均为 canonical 组合摘要，且与单独正文摘要不同。
2. 原样 wording transition 通过 production readiness recorder/checker，并到达 `ready`。
3. title-only 与 body-only 漂移均返回现有 stale route，不产生 readiness success。
4. 缺失或重复 title/body 的六类结构负例均在 wording public invoke fail closed。
5. Focused package tests、真实 installed Phase 0 transcript、source/installed package validation、platform projection privacy 和 dogfood drift 全部通过。
6. Public schemas、typed exits、consumer mapping 与 readiness canonical owner 无变化。
7. PR 明确区分本 task 的 focused 验证与未执行的累计 release、完整 throwaway、tag、业务仓升级边界。

## 非目标

- 不改变 clarification、readiness 或 workspace owner 的语义职责。
- 不修复其它 Phase 0 handoff、base evidence 或历史兼容问题。
- 不发布 tag、GitHub Release，不执行累计 release gate，不升级业务仓，不恢复 playable-ads-guru Issue #15。
- 不增加恶意伪造、并发、锁、TOCTOU、fault injection、跨 OS 或故障恢复机制。

## 未验证边界

Phase 1 只形成可审核计划，不证明实现或回归通过。累计 release 和完整 clean throwaway install/update/reapply 矩阵属于后续 release authority，不是 #274 的完成条件。
