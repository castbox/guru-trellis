# #637 测试策略与本轮实际结果

状态：实施中。以下Test对应Task design V637-01..08；策略不是通过声明。

| ID | 实际入口/输入 | 必须观察 |
| --- | --- | --- |
| T637-01 | 原公共Task/Delivery及七owner wrappers首次链 | 首次完整独立；当前Check/Review/readiness/predecessor真实绑定 |
| T637-02 | matching installed实际Agent，文档冲突/finding修订及未改consumer | 审双方/组合/依赖，当前完整覆盖，闭合不无因换新全量 |
| T637-03 | 共享Runtime/事务正常实现错误，原命令缺失/环境变化 | 扩审未改consumer并检错，缺项补跑，无关事实保留 |
| T637-04 | 同树提交/无关target前进/公开结果恢复/退休checkpoint | 固定B与同Delivery，旧gate不冒充当前，缺覆盖补审，无私有跨读 |
| T637-05 | 同构旧新实际Agent样本 | 充分性/检错成立，语义/命令/正式记录/远端等待分别实测，不预设收益 |
| T637-06 | #636实际installed早期入口及本Task获准远端动作 | 同PR/key/HEAD接续，Draft不冒充full_review；#638未来接口未验证 |
| T637-07 | canonical/platform/installed、单clean、apply/reapply/drift/mode/sidecar/在途恢复 | 完整matching投影和真实installed行为；非完整Release矩阵 |

## 已执行工程事实

原test_candidate_reuse.py通过真实Git及公共Check/TaskCommit/BranchReview/Readiness wrappers执行2项，12.000s，exit0：原Review checkpoint退休后，实际文档候选变化保留原public覆盖但不适用旧gate，旧输入被拒，新Check/full_review绑定精确最终candidate和Check predecessor；实际同树amend后由当前Check和clean Commit reentry接续，不制造额外提交。fixture语义authoring不证明AI实际判断，文档修订测试也不冒充真实Git冲突。

| 命中检查 | 实际结果与边界 |
| --- | --- |
| TaskCommit `test_early_draft.py` | 2项，4.138s，exit0。原#636提交入口的fixture回归通过。 |
| Publication `test_early_draft.py` | 3项，14.003s，exit0。原#636发布入口的fixture回归通过，不证明真实远端PR。 |
| source package validator | `check-skill-packages.sh --root . --mode source --json`返回passed，40 active packages、124 commands、134 test assets；证明结构及分发机械条件，不证明Agent语义判断。 |
| diff、语法与平台格式 | `git diff --check`及新增测试AST解析通过；实现owner的JSON/TOML overlay解析通过。尚未据此声明installed投影或运行行为通过。 |
| Task上下文与checkout | 原`task.py validate`通过，且提示3份规范超过32768字节注入上限；Agent需显式完整读取，不以截断注入证明已读。当前registered checkout边界检查返回ok。 |

安装首次尝试：将固定B的完整source普通clone作为dogfood目标执行apply，因clone含历史legacy archives而返回`upstream_delivery_migration_required`。保留历史归档，不删除或迁移来绕过；该尝试不计成功。

随后在全新临时Git仓库，以Fixed Fork CLI的官方marketplace入口固定到B执行`init -y --codex --no-monorepo --workflow guru-team`，exit0；再从固定B完整source执行preset apply，status=ok，无skill/overlay conflicts。这只证明旧B clean安装准备成功。新候选尚未安装；旧新实际Agent样本尚未创建，apply/reapply/drift与在途迁移均待执行。原始命令日志保留在本轮临时验证位置，不提交原始日志或本机路径。

## 尚未验证

canonical实现已形成早期候选，尚待完整质量门禁。实际Agent差额/共享依赖检错、旧新分阶段耗时、matching新候选安装与#636远端组合、完整当前Check/独立committed Review均未完成。RDT/Architecture共享晋升尚未执行。#638未来接口、业务采用/生产效果、完整Release与多平台升级矩阵不由此证明。
