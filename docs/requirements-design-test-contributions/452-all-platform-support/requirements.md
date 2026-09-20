# #452 All Platform Support Requirements contribution

状态：`reviewed_promoted`。本文件已由受控 RDT promotion 提升到
`current-main-0.6.17-guru.58`；`.57` 为 immutable predecessor，
Architecture shared current 仍为 `.57/active`。实现与验证尚未完成。

- `R452-01`：平台 authority 只能包含两层：由固定 Trellis source identity 绑定的 upstream `AI_TOOLS` 完整平台集合，以及目标业务仓库 installed manifest/provenance 记录的 exact selected platform set。不得新增 Guru-supported、dogfood-supported、deferred 或 unsupported 中间集合。
- `R452-02`：upstream inventory 的 canonical `AITool` id、唯一 public `cliFlag`、template/root、native destination 与 entry form 必须来自 pinned `AI_TOOLS` registry 或其显式映射。当前 inventory cardinality 为 22；实现不得通过目录名、统一 overlay 数量或 ambient upstream checkout 猜测平台集合，也不得把 `claude-code` 与 `claude` 混为同一字段。
- `R452-03`：公开 installer 必须完整删除 `--all-platforms` 选项及其选择分支、manifest 状态、upgrade/throwaway 入口和专项测试；旧参数作为未知参数在目标仓库写入前失败，不得保留隐藏的全集安装语义。
- `R452-04`：重复 `--platform <cli-flag>` 必须接受一个或多个合法 registry `cliFlag`，并形成去重、稳定且非空的 exact subset；installed `selected_platforms` 使用相同表示，每个值唯一映射回一个 canonical `AITool` id。unknown platform、缺少 projection descriptor、重复映射或 selection 与 inventory 不一致时必须在目标仓库写入前 fail closed。
- `R452-05`：未提供 `--platform` 时默认 selected set 恰为 Claude、Codex、Cursor；提供一个或多个 `--platform` 时只使用显式 exact subset，不与默认集合合并。
- `R452-06`：三平台默认值只属于无参数新安装策略，不构成第三层平台 authority，也不得覆盖显式 selection 或 upgrade selection。
- `R452-07`：业务仓库升级必须先读取并验证 current installed manifest/provenance 中以 registry `cliFlag` 表示的 exact selected set，再以重复 `--platform <cli-flag>` 原样 reapply。单平台、任意 subset、三平台和完整 22 平台 selection 都不得被默认值、source checkout dogfood 或新 upstream inventory 自动扩张或收缩。
- `R452-08`：`guru-trellis` dogfood 是普通业务仓库安装状态的特例，其 exact selected set 固定为 Claude、Codex、Cursor。dogfood reapply 与 drift 只消费该 selection；canonical 拥有全平台 projection 不要求当前 checkout 安装其它平台。
- `R452-09`：OpenCode 是 upstream 22 平台的普通成员，必须支持显式安装、ownership、manifest/provenance、reapply/update、throwaway 与 native actual-load；它不因 canonical support 自动进入 `guru-trellis` dogfood。
- `R452-10`：全部 selected platform projection 必须保持 canonical/installed/native-surface parity、executable mode、managed ownership、sidecar/removal provenance 与 package-private `tests/` 排除。#434 production graph activation、正式 release/tag/GitHub Release 和业务仓库生产验证均不在本 contribution 的授权范围内。

本 contribution 只固定 Issue #452 的平台合同。RDT promotion 不证明实现完成、测试通过、
commit、push、PR、merge、tag、Release 或 Issue closure 都需要后续独立门禁与明确证据。
