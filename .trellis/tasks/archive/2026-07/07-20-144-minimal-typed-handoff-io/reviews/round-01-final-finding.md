# #144 Branch Review Gate 独立审查原始报告

## 审查元数据

- 审查轮次：Round 1
- 审查角色：最终放行审查代理
- 技术 `agent_id`：`/root/issue_144_final_review`
- Reviewed HEAD：`66ddb16081672fbf778a3c91cefc62e38945a9a9`
- Base：`origin/main@cbd0396a2ddb7dd0efa613be7b7d93790eb2e34d`
- 完整 diff：`origin/main...HEAD`，94 files
- Issue：`castbox/guru-trellis#144`，live state=`OPEN`
- 问题计数：P0=0，P1=0，P2=4，P3=0
- 审查边界：全程只读；未编辑文件，未运行 `review-branch.sh`、`check-review-gate.sh`、`record-*` 或 finish/publish 命令。

## 问题

### [P2] Skill consumer 可以绕过目标 Skill 自有 input contract

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15969`，并见 `15975-16010`。
- 问题：consumer identity 为 `kind=skill` 时，validator 仍接受任意 `contract.kind=json_schema`；即使使用 `skill_input`，也只读取 `interface_path`，没有验证目标 interface 的 `id` 等于 `consumer.id`。producer 因此可以把 Skill consumer 绑定到自身或任意 schema，而不是目标 Skill 独立拥有的 public input。
- 正常路径复现：在 representative fixture 临时副本中保持 `sync_input.consumer={kind:skill,id:guru-example-sync}`，将 contract 改为 producer 自身 forwarded-output `json_schema`，projection 改为 `direct`；`validate_skill_source()` 返回 `status=passed, errors=[]`。实际 `guru-example-sync` 仍要求 scalar `exit_id/item`，声明的 consumer handoff 已与目标 Skill 脱钩。
- 影响：错误 package 可被激活，并在运行时把不符合目标 Skill input 的 DTO 路由给它，违反 issue 的 Consumer contract 类型、PRD R6、AC5/P6 和 durable target-Skill-owned input 合同。

### [P2] 非 direct projection 只验证一个 example，不能保证所有合法 producer output 均可消费

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:16082` 至 `16103`；normalizer 位于 `15734`。
- 问题：validator 仅对 declared example 调用 projection 并校验 consumer schema，没有验证 producer schema 到 consumer schema 的全域兼容性，也没有证明 mapped target-required 字段在 producer 中必填。
- 当前 fixture 正常路径复现：`{"exit_id":"repeat","profile":"reentry","next_topic":" "}` 合法通过 `action-repeat-output.schema.json`；`trim_ascii_outer_whitespace` 后得到 `{"source_exit":"repeat","profile":"reentry","topic":""}`，不通过 `action-reentry-input.schema.json` 的 `topic minLength=1`。当前 canonical example 为 `" beta "`，所以 source validator 仍整体通过。
- 第二个正常 authoring 变体：从 forwarded producer schema 的 `required` 移除 `forwarded_item`，保留完整 example；validator 仍通过，但合法 producer instance 只含 `exit_id` 时，projection 无法生成 scalar consumer 必填 `item`。
- 影响：1.3 合同可宣称 projection 有效，但合法 typed output 在正常运行时无法进入唯一 consumer，违反 R6、AC5/AC9 和 durable thin deterministic projection 合同。

### [P2] Public/private 互斥只比较 `(schema_id,path)` 整对

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15919`、`15946`、`16116`、`16124-16125`。
- 问题：实现把 public/private ref 存为 `(schema_id,path)` tuple 后只检查 tuple 交集；合同要求 schema ids 与 paths 分别 disjoint。相同 schema id 配不同 path，或相同 path 配不同 id，不会命中。
- 正常路径复现：在 fixture 临时副本中让 sync private checkpoint 文件使用 public sync-output schema 内容，private ref 复用 public output schema id 但保留 checkpoint path，并同步 fixture extension private inventory；source validator 返回 `status=passed`。
- 影响：public DTO schema 可同时登记为 private checkpoint/gate artifact，破坏 #144 的 public/private 分类与 exact inventory，违反 PRD R7/R11、AC10 和 durable disjoint 合同。

### [P2] Package wrapper 只靠字符串包含判断 dispatcher 路由

- 路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:15879`。
- 问题：validator 只检查 wrapper 文本包含 `run-skill-command.sh`，不验证实际执行路径只路由 shared dispatcher。wrapper 可复制 parser/projection/business behavior，并把 dispatcher 名放进注释或死代码后通过。
- 正常路径复现：将 fixture wrapper 临时改为 executable shell：注释中写 `run-skill-command.sh`，随后直接 `printf` 合法 completed DTO；完整 source validator 返回 `passed`。
- 影响：新增或实质修改 Skill 可以形成第二套业务实现，违背 design 4.2 的 thin wrapper 合同和仓库“Markdown 定义流程，脚本执行事实”的扩展边界。

## 验证证据

以下命令均通过，但没有覆盖上述语义负例：

- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'`：95/95。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：39/39。
- `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`：6/6。
- source / installed `check-skill-packages`、dogfood drift、upstream ownership、legacy discovery：通过。
- Changed Python compile、Bash syntax、JSON parse、task validation、`git diff --check`：通过。
- Clean public-sample throwaway init/update/reapply：exit 0，最终无 `.new/.bak` sidecar。

## 观察项

- Remote feature branch 尚不存在，exact current-feature-ref marketplace install 仍无法执行；当前仅 public marketplace sample 与 local unpublished canonical bytes 通过。push 后必须补 immutable exact-ref marketplace evidence。
- Fixture `public_input_schema_ids` 未包含 aggregate `oneOf` schema id；“aggregate 只是 validator index”与“public input schema exact inventory”之间措辞仍有歧义，本轮未将歧义提升为 finding。
- Worktree 审查时仅 `agent-assignment.json`、`task-commit-plans/001.json` 因 post-commit liveness/metadata 更新而 dirty；不属于 reviewed implementation diff。

## Docs SSOT 与范围

- 九个 production Skill 继续保持 interface 1.2 + `legacy`，未发现 production typed-exit 语义迁移；#145/#146 仍为 `followup_issues`，不得由 #144 关闭。
- Docs SSOT 目标路径已同步，文字明确声明 target-owned consumer、projection 和 public/private disjoint 规则；实现未完全承接这些规则，因此当前为代码与 Docs SSOT 不一致，阻塞放行。
- 未发现 fixture 泄漏到 production registry 或 mandatory workflow；production workflow 内 `guru-example-action` 仅为 fenced syntax example。

## 部署与安全

- CI/CD、container、K8s、DB migration、Makefile 无 diff；无部署或数据库迁移影响。
- 未发现 token、secret、private key、签名 URL、客户数据或敏感原始记录泄漏。
- 四项问题均可由受支持的正常 package authoring/validation 路径复现，不依赖恶意篡改、攻击者模型、竞态或非常规 fault injection。

## 结论

P2 findings 未清零，Branch Review Gate 必须 fail closed。修复后需要新 commit、完整 Phase 2 验证和新的独立 Branch Review。
