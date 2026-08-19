# 当前测试计划与证据

## #266 inherited validation

| Check | 计划 | 状态 |
| --- | --- | --- |
| Markdown/path/link/template-residue/heading | 扫描 `docs/**` 与最小 spec projection | PASS：Markdown links/headings 结构检查 |
| RDT/Architecture structure | 校验唯一 current locator、version/status、traceability | PASS：required locator 与 YAML parse |
| dogfood context | `get_context.py --mode packages/phase` | PASS：发现 `architecture, docs, preset, workflow` |
| inventory closure read | registry/interface/manifest/workflow locator 对照 | PASS：21/21 Skill exit 顺序一致 |
| Architecture semantic wrapper | `bootstrap_foundation` current owner result | PASS：`baseline_current` |
| RDT semantic wrapper | `bootstrap_foundation` current owner result | PASS：`ssot_current`；一次错误 digest 被 runtime fail closed 后按 canonical serialization 重试通过 |
| Repository Bootstrap wrapper | `existing_repository` aggregate owner result | PASS：`completed` |
| scope | `git diff --check` 与 changed-path allowlist | PASS：无 whitespace error；只含 task/docs/spec 允许路径 |
| independent full diff review | 完整 docs/spec diff，无 blocking finding | Phase 3 owner |

上述 PASS 是 #266 当前 worktree 的 focused docs/spec evidence；commit 后仍需 Phase 2 与完整 Branch Review 重新绑定 current diff。

## Fresh-read historical focused evidence

| Package | Live source identity | Historical evidence statement | 本次判定 |
| --- | --- | --- | --- |
| #262 Finalizer regression investigation | Issue CLOSED / `not planned`；关闭评论绑定当时的 current main、`origin/main` 与 `v0.6.5-guru.9^{}` commit `56b5f411e533b200e4d8685ca7a2ffb0c778a7f5` | clean canonical source targeted test PASS，连续 10 次 10/10 PASS，`guru-finalize-task/tests/test_contract.py` 44/44 PASS | `source_confirmed` 的历史关闭结论；当前无法复现且证据不足，没有 code fix；#266 未重跑这些 runtime tests，也不将其外推为 current main 或 release-candidate proof |
| #263 RDT | PR #279 MERGED；reviewed head `d53335a721c38b2687b1895fd903751747f53e1c`，tree `82ac9e84ac84df091426b473161e2f1520ef0b25`；archive head `eaf955e058a472e633a9d954002117fea8076d3d`；merge `891c21473541d8e10317adfab7bf3d0a9106aaa0`，二者 tree 均为 `63ebb5c266cf43dc5fc8f1174528046d62fd1613`；Issue CLOSED | PR body/归档证据声明 canonical/installed 9/9、eval 6/6、integration 14/14、preset 75/75，一个代表性 Codex clean throwaway；完整矩阵 deferred | `source_confirmed` locator；结果为 fresh 回读的 historical focused claim，未在 #266 rerun，也不是 GitHub CI proof |
| #264 Architecture | PR #268 MERGED；reviewed head `1cb2506bfe44813fd4e08adf948645908d055b28` 与 functional merge `37fdfe63171296921554625aae39640b88eb9dc7` tree 均为 `51137d2bd543292850bb8e91ad43999889097852`；archive metadata head `991080b6000c91011bbd0f4c5f2f15d70fb531ae` 与 PR #272 merge `3b0f78c1a528ee6aee2d317db206e2f5acb8074b` tree 均为 `dc501709797c499d9dd746f2fd5cadddc8110da9`；Issue CLOSED | PR body/commit 声明 19 packages / 66 commands、contract/runtime/shared eval、全平台 reapply/drift、零 `.new/.bak` 与 executable mode 通过；clean marketplace sample 未验证 | `source_confirmed` locator；历史结果未 rerun且不是 GitHub CI proof；archive 无 `finish-summary.json`，current main 仍保留 active-path `status=in_progress` 副本，clean boundary 保持 `unverified` |
| #265 Bootstrap | PR #280 MERGED；reviewed head `f2c670984a8c11928b085081e0085bdefa2f4604`，tree `02b50f6b2efb6d6b9e091343ba8737af50756359`；archive head `de1c6e2692c3717777d9b432b68af3e6f9ae6f29`；merge `3c0d4a2ffe4799eb67f4c5b1c33d8f8a36f61875`，二者 tree 均为 `45e8b402998477ad53964335a888e601eca76e3f`；Issue CLOSED | PR body/归档证据声明 53 项 package/runtime、projection/reapply/drift 与代表性 Trellis 0.6.5 clean throwaway 通过；#260/#267 deferred | `source_confirmed` locator；结果为 fresh 回读的 historical focused claim，未在 #266 rerun，也不是 GitHub CI proof |

## 明确保留的未验证边界

- #260/#267：完整多平台 Throwaway、Trellis `0.6.15` upgrade/update 与 exact release-candidate matrix。
- #275 local-current representative Throwaway 已通过；exact committed/remote candidate cumulative Release Gate、annotated tag、tag-pinned fresh smoke、GitHub Release 与 `castbox/k8s-infra#28` live consumer gate仍待后续阶段执行。
- candidate manifest `0.6.5-guru.36` / tag `v0.6.5-guru.10` 尚非已发布 stable Release。
- current-version business repository A/B parallel task/Finish/cleanup matrix 与 live provider partial
  recovery variants 未由 #266 重跑，保持 `unverified`；upgrade 后的完整矩阵由 #260 消费，
  exact release candidate 由 #267/#275 各自门禁消费。
- #263/#264/#265 的相关 PR 没有 GitHub review record、check run 或 commit status；本计划只引用
  PR body、commit 与 task archive 的 focused evidence，不将其改写为 GitHub CI 证明。

这些边界不是 #266 failure，也不能被 #266 docs/spec validation 宣称已覆盖。

## #275 focused evidence

| Check | 当前结果 | 证明边界 |
| --- | --- | --- |
| exact `v0.6.5-guru.9` regression | `finalization_stale` 可复现 | immutable affected release identity 与原始故障 |
| Finalizer source / installed | 51/51 PASS | exact archive commit、metadata-tail fail-closed 与 terminal projection/stale negative coverage |
| Finish-family source/installed | 6/6 PASS | Finalizer/Publication/Merge closeout integration |
| routing / upgrade contract | 44/44、7/7 PASS | managed Python caller graph与 registry-derived inventory contract |
| local-current representative Throwaway | PASS | clean install、0.6.5 -> 0.6.15 update/reapply、closeout initial/after-update、no-developer sample；不是 exact committed release proof |

Release candidate metadata更新后必须重新执行 focused suites、projection/drift/mode/sidecar检查；commit 后再执行 exact candidate cumulative gate。
