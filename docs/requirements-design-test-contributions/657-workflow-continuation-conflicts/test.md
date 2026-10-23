# #657 测试与证据

状态：本批工程、分发及所需 installed/native 验证已完成。本文是本批实际结果和证据限制的唯一 RDT 记录，不保留逐轮审查历史或授权。

## 工程定向验证

固定环境为 matching Trellis `e9fb95fd2eb0fb8441153e77384a9dfd3ea3358f` 的公开 Python scripts/common、CLI/Core `0.7.0-castbox.5`，Guru managed Python。各 suite 在独立进程运行，提供 `PYTHONPATH=trellis/skills/guru-team`、`GURU_UPSTREAM_DELIVERY_SCRIPTS` 和命中 suite 的 `TRELLIS_DELIVERY_API_COMMON`；未将条件跳过计入通过。

| 入口 | 实际结果 | 对应范围 |
| --- | --- | --- |
| Create Delivery `tests/test_contract.py` | 7项通过；新增同一测试逐阶段实际公共转换至planning/implementing/checking/reviewing/publishing，再select/recover，核同key/root/phase/results/candidate/内容 | V11确定性层；实际AI consumer另见native |
| Clarify `tests/test_delivery_scope.py` | 6项通过；新增有/无current Delivery×三种scope_action，经原Author→acceptance→原stage rework/withdrawal或Completion的6分支 | V3/V12原owner传输/公共操作层，不是native语义判断 |
| Bind `tests/test_runtime.py` + `tests/test_portable_recovery.py` | 12项通过 | V4/V5普通dirty resume、binding/ownership/checkout/stale及独立common-dir恢复 |
| Create Task `tests/test_delivery_chain.py` | 2项通过 | V6当前Task/Delivery创建链 |
| task_lifecycle `CompositionTests` 的 existing_primary recovery、adopt_linked、三种provision ownership、missing-session recovery | 6项通过 | V6初始创建与原结果恢复保持；没有放宽初始validator |
| Check `DeliveryFlow` 的 readiness_and_no_delivery_required_completion、readiness_refresh_requires_original_publication_rework | 2项通过 | V9真实schema2 full_review/readiness及原Publication合法回程，无旧Task status |
| Verifier standalone Interface、closed current I/O、non_source rejected before executor | 3项通过 | V10源入口/shape及非源拒绝；另增1项原parser对照通过：旧verification_required返回明确standalone迁移诊断，合法current输入实际准入 |

上述加上原parser对照共39项测试方法通过，0 SKIP。六分支和逐phase是subtest/同方法内观察，不重复计成独立方法。

## 分发与所需机械检查

canonical package source校验通过：40个active packages、124个commands；136是声明测试文件数，不是实际执行用例数。358个Guru Python文件完成in-memory syntax检查；Bash syntax、marketplace JSON和git diff --check通过。Task官方validate通过，提示两份超出注入长度的context；本批主/子Agent均实际完整读取writing与workflow，未依赖截断注入作判断。

普通full apply真实触发 `upstream_delivery_migration_required` 并在写前停止；原因是本仓保留的旧归档。没有为通过本任务批量转换旧Task或手改.version。随后由原 `guru-upgrade-tools` 执行同一checkout的正式tools-only local_candidate install及第二次reapply，两次均返回tools_upgraded。公共工具字节原已匹配e9，Guru assets由正式installer生成；Task和session在reapply前后bytes/modes一致。该路线明确保留 `unverified=[formal_fork_source_lock]`，不宣称尚未提交源码是formal_guru_source。

三平台Claude/Codex/Cursor dogfood workflow/spec/overlay drift及upstream ownership校验通过。installed packages校验通过：40 packages、124 commands、10152 managed files，0 conflict/removal/sidecar，无private tests泄入安装。最终Planning义务澄清后再次由同一正式tools-only owner成套reapply，返回tools_upgraded；当前workflow/spec及三平台投影再次核验。官方phase、1.1、2.1、3.5及installed discovery入口读取成功。Changed verifier test再次完成syntax检查。普通full apply的失败与tools-only成功各自保留，不重标为同一成功。

## installed/native实际Agent

只使用一个 matching Codex clean目标A，真实CLI init及完整canonical apply，无conflict/sidecar。独立clone B未复制A私有runtime/session/created；实际Identity、Establish、Rebind及同结果恢复、Ensure、Bind、Selection均完成，binding revision从0到1。同Task native-657/generation0及D1保持，实际Author在B写Delivery PRD并返回requirements_ready。A通过官方task.py创建no_issue样本；不将该setup宣称为完整Guru Intake/Creation门禁。

原Discovery在B实际record/check/invoke返回context_ready，使用原Sync synced事实及当前TaskId/generation/binding/checkout。其Git与GH均为明确受控本地provider：Git remote-helper执行真实git-upload-pack读取A，GH只读adapter读取空Issue fixture。最初url.insteadOf造成公开remote身份与exact-url不符，真实停止；改用同一受控provider的exact-url helper后通过，没有伪造Git输出或将空fixture称为真实GitHub搜索。

Planning中已有当前approved时，原Selection保持三文档；真实consumer按最终workflow直接进入原Activation，没有重跑initial Author。进入implementing后，Selection和原Creation recover_creation保持同key、phase、planning_root及适用结果。原实施owner实际写normalize.py与test_normalize.py，使用value.strip()，目标installed managed Python先运行4项测试通过。这是V1/V2/V4/V11的实际消费与写入，不只是DTO观察。

随后公开源requirements.md真实新增R4/AC5，要求U+3000首尾移除且内部保留。原Clarify返回不含task_key的pre-Author scope_ready2.0，此时accepted_scope不变；scope-only Author写实际根PRD并返回scope_requirements_ready；只有原Clarify task_scope_requirements_acceptance执行accept_scope并返回含TaskKey的post-Author scope_ready2.0。原implementation对同D1执行合法rework回planning，清除四项受影响gate，原Author更新Delivery PRD。已有代码和规划历史由本地Git保留，没有空Delivery、旧clear/profile或创建结果重建。

独立Architecture首次指出样本旧知识只覆盖R1–R3/四观察，正式返回contract_incomplete。原Planning writer补齐六份task-owned完整Architecture/RDT提案后，fresh candidate返回baseline_current/no_architecture_impact。原design/implement实际更新，使用delta_first保留真实知识差额及后续整合义务；shared current未提前写入。原Wording record/check/invoke、独立final_plan、原Approval及原Activation依次完成。最终实际phase为implementing，Task/generation/D1和binding revision1保持；原checkout boundary为status=ok、errors=[]。原实施owner新增test_ideographic_space，目标installed managed Python unittest共5项全部通过；normalize机制保持strip。该完整闭环覆盖V3/V12实际Agent层，另外六分支scope fixture与多phase选择fixture分别提供定向层证据。

样本B通过原guru-upgrade-tools正式tools-only更新至最终matching源码，24个受保护Task/docs/session文件bytes/modes相等。原生样本只到受影响规划门禁、重新Activation、写前boundary及测试，不执行样本自身完整Check、知识晋升、远端发布或再次Finish；这些并非本Issue的样本验收要求。

## 未验证边界

完整多平台Release矩阵、业务留白修复、现场升级/采用、生产和真实GitHub外部效果不在本批；本仓Task的正式Delivery/Completion/Closure/Finish仍由后续各原owner实际执行。规划、静态检查或知识晋升不能代替上述仍待完成的验收。
