# #412 技术设计

## 设计边界

本修复包含两个互不混淆但由同一 Phase 2 blocker 约束的窄修复面：

1. caller inventory 采用 canonical-data-only 方案。`verify_throwaway_python_routing.py` 的当前正常 discovery 是事实生产者，`throwaway-python-callers.json` 是 expected inventory authority。实现不改变 discovery、路由或安装器行为，只校正一个已过期 object 的 identity 与 canonical 顺序位置。
2. Architecture/RDT 采用 authority-first repair + projection synchronization。RDT owner 先在 Issue #412 限定的 #410 contribution、`.52` Design/Test/traceability 与 manifest 中收敛唯一 authority；checker 通过后，六个 stale projection/README 导航再同步 current identity、source binding 和 active/superseded 状态。流程不创建 `.53`，不改写 `.51` history，也不改变 #410 release lifecycle。

## 数据流与修改算法

```text
current source files
  -> verify_throwaway_python_routing.py discovery
  -> current row identity and full anchor_sha256
  -> unique stale inventory preimage match
  -> replace id + anchor_sha256
  -> move the same object to the discovery-produced index
  -> source inventory validation
  -> preset install/reapply
  -> installed inventory and platform projection validation
```

修改前必须重新运行 discovery，并验证：

1. missing 集合仅包含 `helper-python_subprocess_second_hop-559881091ab0`。
2. stale 集合仅包含 `helper-python_subprocess_second_hop-c2f9a2db85f3`。
3. 旧 object 通过旧 `id` 与完整旧 hash 唯一命中。
4. 当前 discovery 返回的新完整 `anchor_sha256` 前 12 位为 `559881091ab0`。
5. owner、kind、classification、expected launcher、ordinal 与 stale object 完全一致。
6. discovery 与 registered 列表长度和 identity 集合一致，且唯一剩余差异是目标 object 从 registered index 9 移到 discovered index 7。

任一条件不成立即停止并回到需求/实现发现，不扩大修改范围。

## `.52` authority reconciliation

RDT owner 按以下顺序完成 authority repair：

1. 以 reviewed #410 contribution、`.52` Requirements/Test 正文、Architecture `.52/active` 和 release contract 为当前证据，不从 stale projection 反推 authority。
2. 对 contribution Requirements/Design/Test、versioned Design/Test 与三层 traceability 中的 R410/D410/T410 identifier 逐项建立语义映射，决定唯一正确集合；不得预设较短或较长编号集合天然正确。
3. 统一 contribution manifest 的 top-level/nested promotion state，只保留一个与 reviewed promotion 事实一致的状态。
4. 在 Requirements、Design、Test 三层 `.52/traceability.md` 补齐 #410 的双向闭合，并把 Architecture inheritance 统一为 `.52/active`；移除把 `.51/current` 当作当前 source 的残留文字，同时保留 `.51` immutable predecessor 关系。
5. 运行 RDT repair checker；只有 authority 内部无冲突后，六处 current projection 才能同步该结果。

允许修改的 authority 文件仅为 contribution 的 `requirements.md`、`design.md`、`test.md`、`traceability.md`、`manifest.yaml`，`.52` Design `design-main.md`，以及 Requirements、Design、Test 三层 `.52/traceability.md`。若语义收敛需要 `.53`、新的产品决策、公共 API/runtime 变化或 release lifecycle 变化，立即停止并回到 live Issue authority。

## Canonical 与 installed/dogfood projection

inventory JSON 保持唯一手工修改点。安装副本只能由当前 preset installer 产生；如果 `apply.sh --repo .` 对 tracked dogfood surface 没有合法变化，则保持零 projection diff。若产生变化，只接受当前 canonical overlay 声明拥有的路径，并通过 `check-dogfood-overlay-drift.sh`、ownership 和四平台 parity 证明来源，不手工修补 installed copy。

## Docs SSOT Plan

- strategy：`authority_repair_then_controlled_projection_repair`
- durable authority evidence：Issue #412、`docs/architecture/README.md`、`docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`、各 `.52` manifest、#410 contribution 与 PR #411 merge facts
- task artifacts：本 task 的 `prd.md`、`design.md`、`implement.md`
- durable authority changes：仅修复 #410 contribution 的 `requirements.md`、`design.md`、`test.md`、`traceability.md`、`manifest.yaml`，`.52` Design `design-main.md` 和 Requirements、Design、Test 三层 `.52/traceability.md`；不创建新 authority version。
- durable projection changes：authority checker 通过后，只修复 `.trellis/spec/architecture/baseline-usage.md`、`.trellis/spec/docs/requirements-design-test-ssot.md`、`.trellis/spec/docs/public-docs.md`、`docs/requirements/README.md`、`docs/design/README.md` 和 `docs/test/README.md` 的 current projection/导航；不修改历史 `.51` authority。
- source-binding projection：`.52` 继续绑定 reviewed #410 contribution + inherited immutable `.51` authority；current graph 23 Skills / 97 exits / 78 commands、Fork source、CLI/core `0.6.17`、`pnpm@10.32.1`、extension `0.6.17-guru.42` 和 target repository tag `v0.6.17-guru.1` 保持四轴独立。
- reconciliation checkpoint：先由 RDT owner 证明 authority 内部一致，再由 Architecture/RDT `repair` owners 审查 projection 充分性，最后重新运行 Planning、Phase 2 和 Branch Review，确认没有历史重写或超出授权文件集的 durable Docs 扩张。

## 兼容性与迁移

该行 identity 由 source anchor 内容派生，不是人工稳定 API。更新 inventory expectation 与顺序不改变 launcher、调用方式或运行时输出。不存在双读、fallback、旧 identity 兼容或迁移层；保留旧 identity 或旧顺序都会继续制造 inventory drift，因此直接替换 identity 并恢复 discovery 顺序是唯一当前方案。

## 架构影响

runtime 与产品架构仍为 `no_architecture_impact`：不改变 owner、数据流、公共合同、运行时边界、并发/恢复语义或跨仓职责。但 `.52` RDT authority 与 Architecture/RDT public projection 均已 stale，因此必须先通过 RDT authority repair 收敛 source，再通过 `guru-maintain-architecture-baseline:repair` 和 `guru-maintain-requirements-design-test-ssot:repair` 恢复 current projection，之后重新调用双方 `task_impact_sync(stage=planning)`。任何 owner typed route 优先于本计划预期。

## 风险与停止条件

- source 在实施前变化导致 discovery identity 再次变化。
- stale/missing 集合不再是严格的一进一出。
- preset reapply 产生无法由 canonical ownership 解释的 tracked 或 sidecar 变化。
- focused throwaway 依赖 mutable/global runtime，或任一 required check 只能以 `SKIP` 结束。
- authority repair 需要创建 `.53`、修改 `.51` 或更早版本化正文、扩展到 Issue #412 明确授权的 authority 文件之外、改变 #410 release lifecycle authority，或引入新的产品/API/runtime 行为。
- projection repair 在 authority checker 通过前执行，或需要扩展到六个声明文件之外。

发生上述任一情况时保留事实并停止，不追加兼容路径或扩大任务。
