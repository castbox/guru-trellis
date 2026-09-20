# #443 Task Identity Session Binding Test contribution

状态：`reviewed_promoted`。`T443-01..20` 是稳定验收矩阵；自动化测试与 semantic review 分层记录，脚本结果不替代 Architecture/RDT owner 判断。

| Test | 场景与通过条件 |
| --- | --- |
| `T443-01..04` | 五个 profile/route discriminator 正例与所有非法组合拒绝；五个成功出口加一个 blocked exit 的 schema/example/consumer closure |
| `T443-05..08` | same-task resume、missing-binding rebind、跨 session continue 与幂等 retry；不创建第二 task/branch/worktree/mapping |
| `T443-09..11` | A→B→A switch 每次 fresh 验证 source/target；错误 active task、未知 branch、缺失 session context zero-write |
| `T443-12..15` | Reactivate generation invalidation、旧 Cleanup receipt拒绝、base advance与缺失 provenance阻塞、metadata base-branch fallback |
| `T443-16..18` | manual recovery重建最小 mappings/binding、冲突零写入、post-write validator拒绝错误 active task |
| `T443-19..20` | canonical/installed/platform parity、registry 32/142/102、production workflow 22/98、ownership/reapply/drift与diff hygiene |

## 已执行证据与边界

- #443 integrated committed range 为 `a74d729ed84449ce603d112e277fa567e87a7bf3..4dd9f7b7d4df2167819745565225001355adb5ee`；Issue #443 于 `2026-09-19T13:42:34Z` closed，range 后续已进入 main history。
- 当前 canonical package 的 contract/runtime suite fresh 执行 26 tests，覆盖 profile闭集、A→B→A、跨 session、mapping locator、base provenance、manual recovery、generation/receipt invalidation与zero-write，结果 PASS。
- live registry/interface/commands 聚合为 32 active packages / 142 external exits / 102 commands；canonical production workflow 为 22 mandatory invokes / 98 exits。installed package 与 canonical interface/runtime bytes一致；package-private tests按当前安装合同不分发。
- 完整 source/installed/platform、preset reapply、ownership、dogfood drift与 #452 平台扩展验证必须在 promotion-created combined diff 上重新执行；这些后续结果不倒填为 #443 pre-promotion evidence。

未执行完整多平台 Release/upgrade matrix，也不证明 #434 production graph activation、真实生产 binding、push、PR、远端 merge、tag、Release 或 Issue closure mutation。
