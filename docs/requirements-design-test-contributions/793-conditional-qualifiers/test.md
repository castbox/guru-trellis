# #793 实际验证与边界

原 owner：guru-maintain-requirements-design-test-ssot；状态为已晋升来源；当前验证策略位于对应完整目标。
完整长期策略是 [qualifier-applicability](proposed/docs/test/current/qualifier-applicability.md)。
本文件只记录本轮实际观察，原正式 Gate 以实际公共结果为准，不复制第二完成账本。

结果仅覆盖下列实际验证层级，规划或阶段状态不作为实现通过证据。

| 策略 | 当前观察 |
| --- | --- |
| TST-793-01 确定性合同/原出口 | 原 managed Python 对三个包各自 tests/test_contract.py、tests/test_runtime.py 作独立进程 unittest discovery：normal 25、solution 25、root 9，全部 exit0/OK，含原真实 public wrapper。source package/consumer graph 通过（43 packages、128 commands）。这些结果验证事实/结构/出口，不证明caller语义触发。 |
| TST-793-02 普通未触发入口 | 完整 provider 的 v1-cheap 原生 Author 初始 profile 实际返回 requirements_ready。primary trace 只读取三个短 applicability，未读取 qualifier 全文或调用 wrapper；仍完成初始需求与候选判断。后续独立 Architecture/规划阶段在900秒超时，因此不记完整 Author run 通过。 |
| TST-793-03 root-only 与真实触发 | conditional-diagnosis 从真实 core.parse_csv_line 与同输入运行输出进入原 Author。normal/solution 未触发；root 实际 stdin wrapper 返回 classified / diagnosis_incomplete，Author 初始 profile 实际返回 requirements_ready。首次错误地给 stdin-only 参数传文件，收到 invalid_arguments，改用 stdin 后成功；原错误保留。primary 只额外读取 normal 的 file-set recipe，未执行 normal/solution 判断或 wrapper。后续 Architecture/规划仍超时，不记全链通过。TST-793-01 的原未变非通过投影覆盖继续适用。 |
| TST-793-04 采用、刷新与恢复 | 三个独立完整 provider 的有界原生 Author 候选观察均 exit0。unchanged 使用真实前序结论，未全文加载 qualifier 或重调 wrapper，同时核当前工作与剩余报告缺口；material 增加同样本实际 Python 行/return trace 后，原 owner 因因果证据变化重调 root；lost 不提供任何前序结论，原 owner 重新判断并调用 root。后两者实际 stdout 均为 classified / diagnosis_incomplete，wrapper exit0、stderr为空，均通过 Interface 选择的 shared router 2.0 schema。lost 的自然语言报告误将 package-local 历史1.0当当前consumer，后续按真实Interface纠正，原日志未改。这些结果仅证明候选采用/刷新/重判，不是完整 Author、Architecture 或 Check。 |
| TST-793-05 分发与迁移 | 原 guru-upgrade-tools 在同checkout实际返回 tools_upgraded / 0.7.0-guru.8，保留 formal_fork_source_lock 未验证边界。目标 resolver 返回原 immutable managed Python；installed package检查通过（43 packages、128 commands、零conflict/sidecar），dogfood workflow/shared/Codex/Claude/Cursor投影及spec drift通过；递归受管sidecar为零。真实 delivery current仍为同Task/gen/key/root、implementing及原planning-accepted结果，continuation可读；owner原检查确认peer/common pointers保持。 |

不声称目标业务安装采用、费用降低、业务事故修复、完整安装矩阵或 Release 通过。
本记录只承载上述实际验证。正式质量、Git 与远端结果读取各原公共结果及
Git/PR 事实；本页不预填后续阶段通过或整体完成。

本轮可丢弃原始观察位于仓库外 `/tmp/guru793-native.Adq7EO` 和
`/tmp/guru793-v4-w34qvyjz`。前者保留两个900秒超时及首次carrier错误；后者保留
原始工具事件、wrapper输入输出和上述路径误判。它们不作为公共包资产或阶段权威。

工具同步首次prepare混用了public platform id `claude-code`与Guru flag，实际准备
失败且未应用；按既有映射使用`claude`后才冻结计划。原操作的public native
context检查两次触发10秒超时。直接检查可成功，剖析定位为169个registered
workspace产生约509次Apple Git launcher子进程。命令PATH改为`xcrun --find git`
定位的同版本实际Git后，相同检查约5.2秒返回；沿原recovery ref完成，未改源码、
超时、身份、写集或校验。原失败和恢复输出保留于仓库外
`/tmp/guru793-tools.sGAclt`；这不形成新的安装恢复协议或全矩阵证明。
