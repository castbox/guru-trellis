# #815 工程验证观察

## 对象与证明边界

观察日期：2026-11-13。正式 Task checkout 的开发基线和未变 HEAD 为 `cb8b4ce349b54cd832ff5b8f72602c5a721ce875`；本页描述未提交工程候选，不声明正式 Check/full_review 或交付。Fork source/build marker 均为 `e3793251fad8bd261d0c370d408c7675b9f6a140`，CLI/Core 实际 package 为 `0.7.0-castbox.6`，public maintenance API1.0 及 AGENTS custom capability 可用。所有工具同步使用 local_candidate，`formal_fork_source_lock` 保持未验证。

## 已执行结果

| 入口/对象 | 实际结果 | 覆盖与限制 |
| --- | --- | --- |
| 原 source `check-skill-packages.sh --json --mode source` | passed；43 active packages、126 commands、161 source-private test assets | 包合同、图与源码资产验证；161不是已执行测试数 |
| 原 managed resolver 下 unittest：Reconcile test_contract.py / test_runtime.py | 8/8、52/52 passed | 固定 Fork fixture、resolved、metadata/恢复及现有 runtime 回归 |
| 原 managed resolver 下 unittest：tools test_contract.py | 9/9 passed | 原 public profiles/consumer/schema 合同；本次I/O无差额，不新增正文自比较测试 |
| 原 managed resolver 下 unittest：Publication test_*.py | 47/47 passed，无 skip | 原事务、正常未完成/完成动作、迁移及恢复；provider替身不证明live GitHub |
| 新 managed_manifest_conflict_flow.py 的真实两分支 fixture | 正常 canonical 及两次原 installer 输出形成 extension.json Git 冲突 | 原 Task/Planning 为明确的 pre-boundary fixture，不证明真实 Planning/Review |
| 当前执行 Agent 完整读修订后的 Reconcile/tools SKILL及contract，实际原preview/prepare/invoke | 固定完整 H blob 原字节与provenance/hash保持，4个真实组合投影逐路径replace；原installer生成最终manifest，tools_upgraded | AI实际接续与自动driver检查分开；未拼JSON、改hash或代填判断 |
| fixture 目标自身 resolver、installed validator、native runtime-contract/continuation、dogfood drift | 全部退出0，三平台一致，conflict/sidecar均0 | Claude/Codex/Cursor投影，不证明其它native host或完整矩阵 |
| 原execute-base-candidate → execute-resolved-base-reconciliation → 同请求恢复 | candidate ok；committed/recovered均为 `7bd39e4dd3dcd3910b6e18ea1b0ca9393dc0706d` | 最终tree=`044e61d55671e38356e5f3d562cd5ac02a307085`；父序为prior H `b20d27831b329e7bf8c19ff07976c9eebebc7dc2`、new base `5e9bbbdcb7300c975fc7e1e2d6fa1be31aee4b21` |
| driver --verify；原tools一次fresh reapply及后续resolver/installed/drift/verify | 全部退出0；reapply tools_upgraded | 零unmerged、组合4类投影、peer及自然dirty当前Task metadata保持；临时旧manifest未进入resolved候选 |
| 原joint_resolved_flow.py | passed，8次公开操作，同Delivery/PR9事实保留 | 真实本地Git/公开wrapper，provider与semantic输入为fixture；不证明正式独立语义审核或live PR |
| 原tools同步本Task checkout | tools_upgraded；目标resolver/installed/drift/native/current均退出0 | 同D1 implementing，Planning applicable；Task/session/peer由原owner前后核验保留；仅20份正文投影与manifest有tracked差额 |
| 内存compile、shell语法、变更链接/anchor、git diff --check、Task context validate | 394个Guru Python文件通过；shell语法通过；11个新增canonical链接/anchor通过；context各10条合法 | 三份大spec的注入截断警告保留，实际必需正文另行完整读取；无独立TypeCheck配置 |

116项定向unittest、真实manifest组合、Agent接续、安装、Git整合与源码分发分别建立上述层次的事实，不互相代替。原20份受管投影由tools/installer同步，未手抄。

## 首次失败与正常纠正

- 首次Reconcile测试未提供其fixture helper要求的 `TRELLIS_FIXED_FORK_SOURCE`，在setup拒绝；补实际固定Fork后52项通过。该装配失败不作为产品缺陷或因果red证据。
- 一次source resolver曾报 `runtime_dependency_missing`；原manage --check确认当前cache有效，原入口后续执行成功。未更改runtime、锁或依赖；该短暂设施现象原因未确定。
- tools首次prepare将上游platform id `claude-code`误作Guru installer flag，普通输入被拒绝。改为原声明flags `claude/codex/cursor` 后冻结有效plan并沿同plan执行；首次失败未进入目标写入。
- fixture首轮缺branch binding，原task start拒绝；第二轮candidate误传目录，原API拒绝。仅纠正pre-boundary装配并沿既有scratch事实继续，保留原失败输出，不改业务断言或待测输出。

原完整运行材料保留于本次外部临时运行目录 `guru-815-manifest-qxcn2adm` 的 attempt2/reapply/joint-proof 和 `guru-815-task-tools-fty4fyeh`；不写Task gate、授权记录或原始扫描账本。

## 整合与未完成责任

RDT三份完整proposed保留全部原正文，原owner在本Task分支/上述HEAD核实际target后写入并readback；结果为 integrated_pending_review。current单元只承接R815/D815/T815及必要关系，不改全局root/index/version或历史。后续质量事实由原正式结果承接，本页不追写自己的最终pass。

本地TaskCommit、I815-08 clean H的正式source_locked采用、完整committed独立Review、readiness、push/PR/merge、Completion/Closure/Finish均尚未执行。完整多平台安装/升级/Release矩阵、其它native host及live远端效果未验证；不是本次工程验证的通过声明。
