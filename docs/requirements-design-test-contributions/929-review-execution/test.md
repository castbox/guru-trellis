# #929 验证记录

## 1. 对象、来源与观察截止

本记录对应 `929-review-startup-recovery/g0`、Delivery `166dac49-79f1-4190-82e3-fd51ca1915a0`，开发基线为 `63e71ffd72300dee4f5bfdc030c2a5f342b97f32`。当前 D1 Planning 的正式结果为 `planning-accepted:4bbcbb83-7315-49d6-a4c4-b806653eb240`。记录截至本轮实现及工程结果消费，尚未产生本 Task 的 committed candidate、Check 或 full_review 通过结果。

完整验收策略见 `proposed/docs/test/current/task-delivery-lifecycle.md#t929启动恢复与证据分层`。策略定义预期，不代表实际通过。下列命令均从本 Task 的 registered checkout 执行；使用仓库相对路径，不公开本机路径。已执行结果按实际适用性采用，本轮 RDT 维护不重复运行测试。

## 2. 已执行的 query 与恢复组件验证

通过 checkout 的 managed Python 运行：

```bash
TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" \
  .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-review-branch/tests/test_execution_facts.py

TRELLIS_DELIVERY_API_COMMON="$PWD/.trellis/scripts/common" \
  .trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-review-branch/tests/test_postcommit_review.py
```

query 原结果为 `Ran 10 tests in 23.099s / OK`。实际覆盖临时目录清理与既有内容保持、错误目录及 errno、首个写失败和后续清理失败的独立报告、query 不改正式结果、未绑定 final_plan 不写 session、缺 commit 的读取事实、不同合法 selection 保留及目的参数约束。首次 candidate_assessment 在 design/implement 尚不存在时可运行；final_plan 只检查实际 design，缺 design 时报告读取失败。

postcommit 原结果为 `Ran 11 tests in 104.100s / OK`。执行真实 Git、原 recorder/invoke 和 public Delivery 操作，覆盖同候选 check→full_review 及前驱、第一槽已完成时只补缺槽、checkpoint 退休后的同结果恢复、缺语义结果时拒绝补造 full_review、后继范围和 Planning rollback 等原行为。语义判断是 fixture。这些结果证明组件运输、正式写入及恢复逻辑，不证明真实 fresh Agent 完成独立 Review，也不证明平台注入问题已修复。

## 3. 真实 Codex sandbox 的 query 观察

载体为本机 Codex `sandbox -P review-query -c <本次 filesystem policy> -C <Task checkout>`，不写全局配置。query 为 canonical `trellis/skills/guru-team/packages/guru-review-branch/scripts/inspect-review-execution.sh`。实际输入使用本记录第1节 TaskRef/DeliveryKey，branch_review 的 `--base-ref` 与 `--head-ref` 均为固定 `63e71ffd72300dee4f5bfdc030c2a5f342b97f32`，并传 `--probe-writes`。这是执行能力样本，没有审查 diff 或生成语义结论。

| 样本 | 实际范围和入口 | 原观察 |
| --- | --- | --- |
| checkout 写入 | filesystem 为 `/` 只读、精确 Task checkout 和 `:tmpdir` 可写；purpose=branch_review | session 目录 `create_temporary_file` 为 `failed / PermissionError / errno=1`；Task、原 checkpoint 与临时目录写探测成功 |
| 精确 session 范围 | 在同配置中只增加 `<git-common-dir>/trellis/sessions` 可写 | 全部必要读取和四处目录探测为 available |
| 未绑定 final_plan | 使用第一种配置，调用期 context=`929-final-plan-unbound-query`；purpose=planning、planning-purpose=final_plan，仍传 probe-writes | session 不可写仍完成读取；仅有 Task/Delivery、checkout、selection、HEAD 和 design 读取事实，没有写 probe 或 not_probed 写项，没有创建此 context 的 session |

每组执行前调用原 `check-task-checkout-boundary.sh --json --task .trellis/tasks/11-25-929-review-startup-recovery`。采集者比较前后本 Task 的 task.json 和 session 目录中全部 JSON 字节，检查 query 临时前缀残留及上述未绑定 session 文件。三组均保持正式文件字节不变，没有残留探测项，也没有新建 final_plan 绑定。原终态为：

```text
Observed expected sandbox facts; Task/session bytes unchanged; no probe residues or final-plan binding created.
```

首失败使用 `permissions.review-query.filesystem={":minimal"="read",":project_roots"="write",":tmpdir"="write"}`，managed launcher 返回 `runtime_dependency_missing / exit 2`，没有进入 query 目标行为。纠正为 `/` 可读并显式指定 checkout 可写后，才得到上述实际 session 权限失败及精确范围成功。另一次将整个 checkout 也设为只读的尝试同样停在 managed runtime；它不能作为 final_plan 行为结果。

首个 command 注册将 entrypoint 直接设为 execution_facts.py，被现 schema 的 entrypoint 白名单拒绝。随后由原 check.py 分发，保持公共 schema。source validator 首次拒绝带连字符的 Interface schema inventory id，纠正为 execution_facts_output 后通过。这两次装配失败保留为原首次失败，不算首次正确执行。

## 4. Bind 诊断和工程检查

原 Bind/adapter 实施方报告：runtime 15、contract 3、portable 2、control 19、composition 20 项通过。当前 RDT owner采用本轮协调者传回的执行结果；未自行重跑，也不从计数推断每个诊断分支、真实 sandbox 或独立审查已通过。精确命令及原输出由该实施方和协调者的原运行记录承接；本记录不编造缺少的 argv。

本 query 实施方实际执行：

```bash
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
  --root . --mode source --json
bash -n trellis/skills/guru-team/packages/guru-review-branch/scripts/inspect-review-execution.sh
git diff --check
```

source validator 原 stdout 为：

```json
{"active_packages":41,"commands":122,"complete_package_commands":39,"instruction_only_packages":2,"mode":"source","package_test_count":192,"public_projections":0,"status":"passed"}
```

按 quality-guidelines 的 Python Syntax Check 对 Guru runtime、packages 及 preset installer 进行内存 compile，原结果为 `Syntax checked 411 Guru Python files.`；changed JSON、Bash syntax 和 diff 检查通过。协调者另报告主方同范围语法411及 source validator 通过。静态和包装检查只证明其实际范围，不是 Check、Architecture 或独立 Review 通过。

## 5. 历史样本与未验证边界

规划阶段已观察 Codex0.172.0 同 sessions 目录仅 workspace 写失败 PermissionError errno1，加入精确目录后临时项成功删除；fresh CLI 在最小额外 session 范围完成原 Identity/Ensure/Bind/Selection 与独立 candidate_assessment。这只证明其当时对象和阶段，不证明修复后完整 Branch Review。native fork_context=false 额外委托报告和错误 prompt 误读保留原失败边界。

- V1：本轮真实 linked-worktree query/sandbox 与 final_plan 只读例外已有上述证据；预检不是质量 pass或未来写入承诺。
- V2：Bind/adapter 组件结果按第4节来源采用；它们不替代真实 sandbox 或 Agent 判断。
- V3：端到端真实 fresh Agent 的完整独立 Review 及其原正式 check/full_review 结果尚未验证。只需正常 owner 准备的最小 Task/Delivery/B..H，不能扩大成整个临时 Intake 链；fixture semantic pass 不计此项。
- V4：11 项原 postcommit 测试提供组件级同候选补缺/结果恢复证据；真实 Agent coverage 延续仍需对应实际行为。
- V5：平台额外委托注入的具体环节、嵌套 worker 无响应底因，以及修复后真实 Agent 的直接执行/历史正确读取和中性新旧方法对照尚未验证。现有失败与局部接续不改记为通过，不声称通用成本降幅。
- V6：本轮 source 检查已通过；matching tools 同步、installed、受影响平台、drift/sidecar/mode 与 preservation 仍等待原 tools owner 的实际终态。源码存在不证明安装完成。完整多平台 Release 矩阵、正式 source-lock 采用与业务后端修复不由本记录推定。

## 6. Tools 成功后的整合截止

原 tools owner 的正式 stdout 已读回：tools_upgraded，installed_version=0.7.0-guru.12，recovery_ref=11c2a4b6-51e5-411f-9e47-bd0c8657ac2e，unverified=[formal_fork_source_lock]。本轮 RDT owner 实际读取了该次 invoke.stdout.json、verification-results.json 和 final-preservation.json 原结果。它们位于该 tools 调用的本机临时目录，公开正文不复制本机绝对路径。

source/installed、ownership、drift、native、query-help 和 diff 检查结果为 rc0；installed 平台选择为 claude/codex/cursor，sidecar_count=0。final preservation 实际检查106个root，changed_roots=[]、sidecars=[]，source_and_peer_check=passed；原checkpoint为complete、public_phase=applied。mode9951无非预期及graph4通过由协调者读原结果后传回，不伪称本RDT owner另行执行。

verification-results保留首次target-resolver的runtime_dependency_missing/rc2；final-preservation中sequential_resolver_rc=0。失败底因未知，不写为已定位的并发或权限根因。原non_executable_script_count=209包含按模块加载的Python文件，单凭此数不判mode失败；本RDT owner未据此改文件。协调者另传回首次platform参数claude-code被拒绝且未生成plan，改用原CLI flag claude后成功；保留首次失败。

本次原维护按final_integration将三份完整proposal整合到真实current，并逐份readback；既有完整正文和稳定身份保留，仅增加R929/D929/T929及必要整合状态说明。状态为integrated_pending_review，尚待TaskCommit和committed independent Review。V3、V5仍保持第5节观察截止；正在进行的对照不在本次结果中提前记通过。正式源锁、完整Release矩阵和业务采用仍未验证。


## 7. V5 中性方法对照的终结观察

本节补充第5/6节之后取得的实际结果，不改写此前观察截止，不重复已完成的RDT promotion。原执行者使用同一 session binding 诊断设计摘录、固定B的三份Architecture authority及旧源码，在独立中性副本中运行相同只读请求；模型/配置为cpa/gpt6.1sol、medium、read-only。评价方先盲读实际输出和工具轨迹，再揭示方法映射：cedar为本批方法，birch为B方法。两次均turn.completed，进程exit0，均未执行正式invoke；这些终态不是正式审查通过。

原证据为本次本机临时目录guru-method-owmanx71内的cedar.jsonl、birch.jsonl和request.txt。本RDT owner实际读取request及必要原轨迹/最终输出，核对下列item顺序；模型配置、盲评后映射、进程exit0和早期装配失败由本次对照执行方结果承接。公开正文不复制本机绝对路径，也不将本次静态设计意见作为当前实现finding或修复授权。

| 中性副本与方法 | 实际工具顺序 | 观察及适用边界 |
| --- | --- | --- |
| cedar：本批方法 | item_4读取Skill；item_5即cat candidate/design-facts.md；item_7起读取完整contract，item_14才读取三份authority并继续补全文 | 最终输出主动承认首次读取提前看候选，未严格满足authority-first；不能充当合规的正式首次独立assessment |
| birch：B方法 | 先读取authority并补足全文，item_20才cat candidate/design-facts.md | 该样本保持authority-first读序；不是正式Task/Delivery评审或完整交付通过 |

两个样本均未把合法design_facts或其他Task历史pass误判为当前污染，也没有递归转派同职责。这只支持这两个普通只读设计样本的观察，不能推广为所有载体或正常正式Review均已修复。

本次未提供精确Task/Delivery，没有执行query或probe；副本没有.git也是较晚才由git rev-parse失败暴露。因此，“执行条件在大规模读取前发现”的场景未充分触发。没有真实无反馈条件，不证明无反馈诊断或恢复。native prelude采集不完整，不证明正式独立性。平台额外委托注入环节及内部worker无响应底因仍未知。V3的真实完整独立Review及正式双槽结果仍未由此建立。

本次已读Skill原本明确要求authority-first。cedar在读取完整contract之前就cat候选；单一样本不能证明新增preflight措辞导致这次顺序失守，也不能支持“新方法改善或修复成功”的结论。不据此新增重复规则、门禁、runner或测试义务。两份输出中的静态设计建议针对本次摘录及旧实现，不直接判定当前候选存在同一缺陷。

早期尝试保留为设施/材料失败：attempt1遗漏query脚本及技术基线引用；attempt2共享材料不全而中止；另有一次启动前FileExistsError。这些没有形成可比较的方法执行结果，不计方法效果，也不由后续成功终态覆盖。

V5结论仍为未通过、证据不充分：已观察合法设计/历史处理和无递归；本批样本出现authority-first失守，执行条件提前发现、正式独立性、无反馈恢复及平台注入修复均未获充分证据。未追加实验、未重跑测试、未改current/proposal/canonical，原ssot_current仅保持此前整合事实。
