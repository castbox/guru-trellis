# #464 Test Contribution

`TEST-464-LOCAL` 承接 [traceability.md](./traceability.md) 的 SC-464-*。测试只观察正常行为；不将脚本 schema pass 当语义充分性，不将 mock 外部依赖当真实 GitHub 实效。

## 当前实际结果

SC-464-DELTA：当前 AI 读原 Check 合同与 fact-only
`trellis/skills/guru-team/packages/guru-check-task/evals/files/local-revision-facts.py`，
逐轮自行选择执行/复用，再调用原 recorder → checker → invoke。实际累计次数：

| 正常动作 | A | B | C |
| --- | ---: | ---: | ---: |
| initial | 1 | 1 | 0 |
| A-only | 2 | 1 | 0 |
| B dependency | 2 | 2 | 0 |
| B check definition/version | 2 | 3 | 0 |
| Python 3.14.7 → 3.12.8 | 2 | 4 | 0 |
| B decimals 2 → 3 | 2 | 5 | 0 |
| 新增 C | 2 | 5 | 1 |
| 当前 AI 不再持有 B fact，局部重跑 | 2 | 6 | 1 |
| task.notes 修订 | 2 | 6 | 1 |

checker 每轮 `ok`；A/dependency/check-definition/C/metadata 的内容修订产生当前绑定，
toolchain/environment/结果更新保持同一内容 identity，旧 initial record 未被改写。
该局部 fixture 未执行完整 Architecture/qualification 上游，public 输出诚实为 `blocked`，
不是完整 Phase2 pass。不可用分支只证明当前 AI invocation-local 放弃事实后的局部重跑，
不证明 native context-loss。合法配置可用性通过实际 Python 计算入口执行，未设旧值白名单。

SC-464-CONTINUE：当前 AI 在临时真实 Git 算术 fixture 读 accepted A/B 两个独立 slice、
实际代码及执行结果，自行作者 Completion 结论并调用安装的原 `scripts/invoke.sh`：
A 已交付/B 缺失返回 `additional_delivery_required`（consumer `task-delivery-planning-router`）；
B 内容已完成但未执行 check 返回 `evidence_pending`；实际执行 B check 后，以前一出口
投影形成 `evidence_refresh`，同一 committed HEAD 返回 `completed`，没有新增 mutation。
该回放从 Completion 的 module input boundary mock 外部 merge facts；没有声称已执行
Planning→Publish→真实 Merge 全链，也没有修改本 task 的 Completion/Closure/Finish 状态。

SC-464-RECOVERY/REVISION 的确定性模块证据：
`guru-review-task-delivery/tests/test_runtime.py` 11/11 PASS，含正常 ready 后 checkpoint
退休、same HEAD fresh re-entry，以及普通新 HEAD 拒绝旧 anchor；
`guru-reconcile-task-base/tests/test_runtime.py` 37/37 PASS，含 unchanged 零写、new/evolved
pair、bounded routes 与原恢复；`guru-check-task/tests/` 29/29 PASS；
`guru-create-task-commit/tests/test_runtime.py` 15/15 PASS，保留当前内容/精确 tree 与
同次 mutation 恢复。Workflow lifecycle prose 18/18 PASS 只作为 routing 一致性补充。
以上模块证据不单独证明 AI 的 anchor/authority/promotion 选择。

SC-464-DISTRIBUTION：canonical apply 后重新 apply 返回 `ok`，source/installed/activation
验证通过，Claude/Codex/Cursor/shared 原 owner 投影与3个 spec 同步。首次 apply 的23个
`.bak` 由随后标准 reapply 正常处理，最终无 `.new/.bak`；workflow 经确认目标无本地修改
后同步 canonical local sample。dogfood drift PASS。无 upstream/node_modules 修改。

SC-464-AUTHORITY/metadata 的新增当前 AI installed-wrapper 证据：在共同合法临时
task/branch/算术/Docs fixture 中，实际执行 Architecture no-impact、两个 Phase2
qualifier `classified` 与完整九维 Check，原正式出口为 `passed`。正常将计算误改为
`value + 2` 后实际 AssertionError，旧 checker stale，fresh qualification 为
`qualified_current`，Check 返回 `implementation_required` 且非 passed checkpoint
正常退休；修为 `1 + value` 后重新完整当前语义审查返回 `passed`。随后只更新
task.notes，旧内容绑定再次 stale；当前 AI 逐依赖复核后复用实际 fix check 事实，
没有新增计算执行，fresh upstream 与九维 Check 返回新的 `passed` 绑定；旧记录未改。
此处成功来自实际当前 AI 判断及 target-installed 原入口，未复制示例 pass。

SC-464-REVISION/RECOVERY 的共同 fixture 随后实际消费 Check `passed`：TaskCommit
第一次因普通 exclude 配置错误拒绝且 HEAD 不变，修正后用同 prepared candidate 成功；
同 locator 两次 stdout-loss recovery 均返回同一 commit，新增 commit 仅1个。
早期该轮虽然有真实 Branch/Delivery wrapper 输出，但遗漏 mandatory mechanism
qualification，只记为局部行为证据。下面 post-promotion 当前轮已补齐完整 mandatory 调用。

SC-464-REVISION 的真实 RDT promotion：作者建立 v1 与 isolated v2 contribution，
原 bootstrap 返回 `ssot_current`、task impact 返回 `sync_required`；另一位 AI
独立读取 contribution 和 current v1 后，实际写 shared current v2，并保留 v1
历史，原 promotion 返回 `ssot_current`。随后 fresh RDT/Architecture、两项资格和
完整九维 Check 返回 `passed`；只复用依赖未变且仍可读取的实际算术执行，不重跑计算。
原 TaskCommit 创建新的 promotion commit `3922540`，不同 reviewer 实际读取完整
`239b450...3922540` 后，fresh Branch Architecture/RDT、两资格及原
record/check/invoke 返回 `passed`，fresh publication Architecture、两资格与
十维 Delivery 返回 `ready`。此轮不消费 pre-promotion Branch pass。

在该 post-promotion candidate 上重做两支完整 recovery：

| 当前上下文 | Branch | Delivery | Architecture | normal / mechanism qualification | Check / Commit / Planning |
| --- | ---: | ---: | ---: | ---: | ---: |
| checked Branch DTO 仍可用 | 0 | 1 | 1 | 各1 | 各0 |
| Branch DTO 不可用且 checkpoint 已退休 | 1 | 1 | 2 | 各2 | 各0 |

第二支由同一独立 reviewer 重新读完整当前 range、live authority 和当前源码作新
语义 round。两支正式 Branch/Delivery 输出为 `passed` / `ready`，HEAD/base/tree/
current v2 均未改变，producer checkpoints 正常退休。promotion 只改变 RDT 知识
引用，没有 Architecture impact；未为回放虚构 Architecture contribution/ADR。

SC-464-AUTHORITY 的实际 Architecture owner 回放：共享 authority v2 与
`value + 1` → `1 + value` 为等价适用合同，原 installed invocation 返回
`baseline_current/no_architecture_impact/no_change`；authority v3 要求新增
持久化 calls.json，与原 pure/no-persistence 合同实质冲突，当前 owner 返回
`architecture_conflict/return_route=planning`，未消费旧 pass。这是 module
边界的当前 AI 判断；不是 Architecture promotion、远端或 native CLI 全链证明。

原 identity owner `guru-bind-task-session/tests/test_runtime.py` 的
`test_rebind_resume_and_manual_recovery_are_pointer_only` 与
`test_dirty_checkout_can_resume_but_branch_drift_blocks_without_write` 均 PASS；
不重建 #454 substrate。Publish 原 transaction 的同 HEAD existing-PR bind recovery
与 ready stdout-loss rematerialization 两个定向测试 PASS，观测没有新增 mutation；
前序 metadata postimage output-loss 与 missing-transaction return-to-review 证据保留。

当前 task 的 fresh Phase2 Architecture 原 wrapper 返回 `baseline_current` /
`no_architecture_impact`，normal/mechanism qualification 各返回 `classified`；这些只证明
各自独立 owner 的已审查结果，不代替完整 Check 充分性。

必需源检查：marketplace index JSON、canonical shell 语法、219个 Python 源文件
编译与 `git diff --check` 通过。正式 Trellis task validate 起初拒绝空
implement/check context；通过原 add-context 入口补入本次已使用的规范、规划和
Test locators 后通过。大 spec 的自动注入截断提示保留，当前 owner 已直接读取
完整相关合同，不以自动注入替代读取。

SC-464-REVISION 的提交后 finding-fix 回放：普通本地 Git setup 创建错误
`add_one(value)=value+2` 的 committed candidate；初始 TaskCommit producer 在这个
module input boundary mock，没有伪造上游 Check pass 或 receipt。当前 finding owner
实际执行原检查得到 AssertionError，fresh Branch Architecture、两项资格和原 Branch
record/check/invoke 返回 `implementation_required`，产生 P2 `F464-postcommit-add-one`。
修成 `value+1` 后，fresh Architecture、两项资格、完整九维
`finding_fix_rerun` Check 返回 `passed`；原 post-check pair guard 为 unchanged，
原 `finding_fix_commit` prepare/invoke 创建修复提交 `85a6de2`，只提交 calc.py。
finding owner 亲自读修复 diff 并实际执行三断言后作 transient closure；不同 reviewer
重新读取完整 `239b450...85a6de2` 的27路径，实际执行检查并消费本轮 fresh Branch
Architecture/两项资格，原 `fresh_final_review` recorder/checker/invoke 正式返回
`passed`，零 open finding，原 Check/Branch checkpoint 正常退休。
该 reviewer 未参与本次 bug setup、修复或 closure；曾参与被复制的前序 fixture
文档构建。此证据证明从实际 Branch finding 开始的修复/复审路径，不证明初始
Planning→Commit 或远端全链。closure 无 artifact，没有为 lineage 创建空提交。

## 未验证边界

未运行独立 Codex CLI native eval；上面的 current AI 回放和
post-owner 模块证据分层陈述。Completion 的 pytest suite 因 managed runtime 没有
`pytest` 未运行，不能记 PASS；原 Completion wrapper 的三次实际调用结果如上。
远端 push/PR/merge/Issue mutation、官方 update 与完整累计多平台 Upgrade/Release
matrix 均未验证；本 ordinary Issue 不承担完整矩阵或 Release 证明。
