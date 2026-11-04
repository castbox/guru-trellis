# #731 定向验证结果

本记录供本Delivery的Check、Review与整体Completion消费。观察对象为固定main基线1d32c9c8044ed12fce54ab991545ab0cfde0993c及本次canonical候选。历史现场事实见同目录historical-observations.md；两者不能互相替代。

## 真实Agent隔离行为

入口为两个公开SKILL；载体位于canonical DAG tests/run_native_orchestration.py，host-only方法在native-orchestration.md。协调Agent与每个child turn均实际执行Codex CLI0.162.1。首组V1–V4配置gpt-6.1-sol/high；补充completion-drift组按当时当前配置使用同模型/medium，修改前与候选设置相同。模型只读同provider合同，预期和完整运行输出在模型目录之外；工具按显式operation执行合成动作，无自然语言关键词决策器或自动semantic pass。

- V1：最初baseline因工具审批配置拒绝inspect，未进入场景，保留环境失败；修正载体配置后使用同provider基线重跑。baseline2 DAG已完整dag_completed，原输入失败经合法后续解决、外部等待复查、独立/依赖推进及收口均完成，未复现历史失当。Sequence按同一最终分段fixture另做baseline3，亦完整chain_completed、无unfinished child，未复现失当。该基线还主动要求原owner清理其合成Completion说明中的歧义措辞；不能倒说成候选改进效果。故本轮不宣称红转绿或历史生产根因已修复。
- V2：candidate DAG真实初始child执行失败后停妥。协调器核实际输入并续接原owner；未知发送结果后读取实际对话/原operation，未重复发送。外部build两次running且child无新文字，第三次failed后协调器废止旧wait并安排原owner修正。101先merge仍open时继续Completion/Closure/Finish，完整closed/archive后才释放103。103因不可读兄弟事实而停下时，协调器刷新前驱结果并向原owner承接必要事实，实际执行后核所有节点closed/completed/archive、inactive、无pending，stop/readback心跳，至dag_completed。
- V3：candidate2 Sequence保留old-201已知不可恢复首失败，同Task/Delivery通过修正输入执行新op-201-2。真实child仅完成implementation/verify后结束，Check/fullrangeReview/readiness仍缺；协调器另发原owner质量段，实际补齐后单独merge并追Completion/Finish。201完整结果与inactive后才创建202；202也补质量段后完成。最后两节点closed/archive、inactive、无unresolved，心跳停止回读，至chain_completed。
- V4：candidate blocked真实execute返回mandatory_producer_output_missing。协调器要求原owner核输入、producer能力、原失败、修正及等价入口；真实child核certificate-v1 unavailable、无支持修正/等价且不能直接替代，保留失败后hold。协调器回读inactive/无unresolved与心跳stop/readback，给external-release-team最小certificate条件及同run恢复条件，至chain_blocked。

V3补充completion-drift：真实原child在scope revision 1完成实现、验证、合并并报告whole-Task Completion，随后host正常更新current authority为revision 2，增加checksum义务，保留旧声明/门禁。候选协调器读取live事实后明确指出旧Completion不覆盖新义务，交原owner实际执行checksum、刷新受影响Check/Review/readiness/Completion并Finish；原项全部完成且inactive后才推进第二项。最终chain_completed，两个Issue closed/completed、Task archived、无unfinished或unresolved，心跳stop/readback。相同fixture修改前补充对照也完整chain_completed，故此分支仍未复现历史失当。首次补充run因会话中断停止，已核进程消失，保留未完成trace，不计为通过；两组等价重跑到终点。

独立审核对照完整carrier和native tool结果，核V2/V3/V4上述多轮链；结论基于实际动作和证据，不是出口名称或计数。原始输出分别位于外部隔离运行candidate-dag、candidate2-sequence、candidate-blocked、baseline2-dag、baseline3-sequence、candidate2-completion-drift、baseline2-completion-drift的20261104输出目录，不进入公共包或安装投影。可用上述runner的--source-ref指定固定基线、--scene指定dag/sequence/blocked、--output指定新外部目录重现；省略source-ref读取当前工作树。

隔离heartbeat为事实载体的模拟时钟；真实Agent进程和消息处置不是模拟。此证据不证明实际App scheduler/chat续接、真实GitHub/生产业务、所有客户端或完整单Issue门禁集成。历史SSM仅收敛认证缺口，不表示业务完成。

## 源码与实际投影

- source package validator：43包，其中2个instruction-only，通过。
- python3 -m unittest trellis/skills/guru-team/tests/test_instruction_only_packages.py：4 tests通过；覆盖两包发现、显式元数据、Codex-only投影、私有tests排除、reapply与平台选择/冲突。
- runner内存compile及git diff --check通过；私有载体未进入installed公共包。
- 原guru-upgrade-tools以匹配CLI/Core0.7.0-castbox.6、local_candidate执行目标worktree同步，再对同候选实际reapply；两次tools_upgraded。实际选择claude/codex/cursor，Task task.json字节保持，用户配置保留；target原生get_context可读Task2与当前implementing。shell无session context时不将currentTask=null伪装绑定。
- reapply后dogfood overlay/workflow/spec及选定平台投影drift通过，无.new/.bak，模式沿原installer。仍保留formal_fork_source_lock未验证边界；本项未执行完整Release/Upgrade多平台矩阵、发布或生产操作。
