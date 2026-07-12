# Issue #105 最终放行审查原始报告 Round 6

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round6`
- 独立性：未参与实现、Phase 2 或 Round 1-5
- reviewed HEAD：`533d9e54fb912a29e5a422219163afa9e2c3ec32`
- diff range：`origin/main...HEAD`
- findings_count：`3`
- 结论：`fail`

## 审查范围

独立读取了 live issue #105、规划三件套、planning approval、Phase 2、ledger、assignment、Round 1-5 原始报告和完整 47 文件 diff。

重点覆盖 immutable plan/digest、dry-run/formal、raw PR identity、Git raw/effective remote、marketplace evidence、final summary、archive blob continuity、恢复状态机、生产 Git failure matrix、三方 HEAD、#97/#98 合同、durable specs、canonical/dogfood、preset/overlay、五平台入口、throwaway/update、安全和部署影响。

## 发现项

### P1-1：dogfood 安装 provenance 被错误降级，Claude 资产失去 managed ownership

证据：

- `.trellis/guru-team/extension.json:86-103` 将 `selected_platforms` 从 `claude/codex/cursor` 改为仅 `codex/cursor`，并把 `all_platforms` 从 `true` 改为 `false`。
- 同文件当前 `managed_assets` 不再包含五个 `.claude/**` 资产，但这些文件仍实际存在且本分支修改了 `.claude/commands/trellis/finish-work.md`。
- `implement.md:58-65` 明确要求用 `apply.sh --repo . --all-platforms` 同步 dogfood。
- 当前 manifest 为 66 个 managed assets；基线为 70 个，并包含五个 Claude 条目。

影响：

后续 update/reapply/rollback 无法把 Claude 入口识别为当前 preset 管理资产，dogfood provenance 与真实安装状态分裂，违反 all-platform 同步及 upgrade/update 抗漂移门禁。

建议：

重新以 `--all-platforms` 应用 canonical preset，确认 manifest 恢复三个平台、`all_platforms=true`、Claude managed assets 完整；再检查 sidecar、overlay drift 和 installed manifest diff。

### P1-2：被 AI 审阅的 body source 仍按 `strip()` 等价，未绑定 task-local 原始 bytes

证据：

- `guru_team_trellis.py:8163-8175` 的 `read_pr_body_file()` 对任意路径内容执行 `.strip()` 并补一个换行。
- `prepare_closeout():11142-11162` 允许 `--body-file` 或 `--body-artifact` 指向其他来源，最后只比较 `resolved_body.strip() == body.strip()`。
- 因此另一个 body source 与 task-local `pr-body.md` 只要去除首尾空白后相同即可通过；计划和最终 PR 实际绑定的是未被逐字确认的 task-local bytes。
- durable contract `companion-scripts.md:134-139` 声明 task-local raw UTF-8 是唯一 identity，不允许 trim 或 newline normalization。
- 当前 raw-body 测试只覆盖 plan/readiness/PR 后继阶段篡改，没有覆盖 prepare 的替代 source 路径。

影响：

AI 审阅证据和实际发布 body 可在首尾空白、最终换行及 Markdown 敏感空格上不同，破坏 immutable reviewed body 合同。

建议：

finish-work 必须要求 reviewed source 解析到当前 task 的 `pr-body.md`，并按原始 bytes或原始 UTF-8 文本逐字比较；不要复用 legacy trim resolver。补外部 body-file、body-artifact、首尾空白和最终换行负向测试。

### P1-3：clean throwaway 安装后的完整 closeout smoke 没有执行

证据：

- `prd.md:114-116` 和 `implement.md:92-96` 要求 clean throwaway 在安装 workflow/preset 后完成 dry-run digest、formal draft、archive metadata 和 ready。
- `verify-throwaway-install.sh:169-178` 只检查 schema、函数名和入口文案。
- 同脚本 `:297-317` 只验证无 intent 的 direct finish/publish 会失败，之后验证 preview/switch/update/reapply；没有创建可 closeout task，也没有运行正式 finish。
- 生产 fixture `test_guru_team_trellis.py:10348-10372` 手工复制 `.trellis/scripts`、schemas 和 workflow，未通过 workflow marketplace/preset 安装，所以不能证明 installed artifact 可完成同一路径。
- Phase 2 仅记录 install/update throwaway 与独立 production fixture，缺少两者组合证据。

影响：

开箱即用门禁仍未证明。managed asset、wrapper、配置、权限或安装路径问题可能只在真实安装后的 formal closeout 暴露。

建议：

让 throwaway 安装产物创建完整 task/gate/ledger/body/index，使用真实 Git/bare remote和受控 GitHub adapter执行 installed `finish-work.sh` dry-run/formal/archive/ready，并在 update/reapply 后重跑或验证等价恢复路径。

## 问题生命周期

Round 1 四项 P1、Round 3 head repository P1、Round 4 本地 transport P1，以及 Phase 2 的 raw/effective URL normalization 子问题均有实现和测试证据，未发现回退。

Phase 2 `head=dbe3d4c`；其九个 `dirty_paths` 与 `dbe3d4c..533d9e5` 九个非 metadata 文件精确相等，三个变更 spec 哈希与当前文件一致。Round 1-5 报告哈希、reviewer reuse/freshness 和 interrupted-agent lineage均一致。

本轮三项 P1 是此前未闭环的当前 scope 缺口。

## 验证证据

独立复跑：

- canonical tests：`373/373 pass`
- preset tests：`36/36 pass`
- `git diff --check origin/main...HEAD`：pass
- canonical/dogfood Python、workflow、五平台 entry byte equality：pass
- 无 `.new` / `.bak`
- 当前仅 task metadata/review tail dirty

测试通过不覆盖上述三项缺口。

## Docs、部署与安全

核心 closeout 顺序、strict remote、archive continuity 和恢复语义在 durable docs/canonical workflow/dogfood workflow中一致；但 raw reviewed-body 声明强于实现，且安装 provenance/throwaway 验收未闭环，因此 Docs/交付门禁整体为 `fail`。

未变更 CI/CD、容器、K8s/Kustomize、DB migration、Makefile 或部署资产。未发现 secret、token、私钥、`.env`、客户数据或签名 URL 泄露；remote 错误脱敏未见回退。

## 观察项

- 当前分支尚未推送，current-branch remote marketplace verifier 与真实 GitHub closeout E2E 仍待 publish-time 执行。
- 远端仍不存在 `v0.6.5-guru.3`，不得声称稳定 tag 路径已验证。
- ledger scope 正确：只关闭 #105；#53/#96/#97/#100 为 related；#98/#99/#101 为 follow-up。

## 后续候选

0。三项 finding 均属于 #105 当前范围。

## 结论

Round 6 最终放行不通过。必须闭环以上三项 P1，重新执行 Phase 2、finding owner closure，并派发新的 fresh 最终放行审查代理后，才能记录通过的 Branch Review Gate 或进入 finish-work。
