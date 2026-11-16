# D1 工程验证

本记录供本次 committed Review 与 whole-Task Completion 消费。观察截止于本次工程验证；不预告独立审核、合并或完成。

## 原 public wrapper 与真实绑定回归

实现 Agent 运行 test_runtime.py 的 test_git_object_record_diagnoses_authoring_before_evidence_and_recovers：1/1通过。普通误填背景 issue_refs 返回 schema_mismatch，字段 owner_result.live_change.issue_binding；按原流程纠正后，相关 terms 和 null 保留，check/invoke 实际 context_ready。原 test_contract.py 绑定 schema 定向用例1/1通过。内存 Python compile 404文件通过，git diff --check通过。

完整 test_contract.py 为6/9通过。独立固定B=e33ecf82d47fba88c95d74f298d55d0616cbb1a4的git archive临时副本重跑同样6/9，三项相同既有漂移为 supplemented出口、envelope2.0与旧1.0期望、consumer authoring seed。未把失败改成通过，也未扩大本次修复。

## 当前 checkout 采用

原guru-upgrade-tools同操作正式返回tools_upgraded，installed_version=0.7.0-guru.10；本次为local_candidate，unverified=[formal_fork_source_lock]。原调用等待超时后，实际原操作已complete且无failure；以同recovery_ref恢复结果，无新prepare或重复安装。

实现 Agent 执行原check-skill-packages的source/installed模式：均passed，errors=[]；installed检查9938 managed文件，声明claude/codex/cursor投影一致，conflict/sidecar/overlay_sidecar均0。原check-dogfood-overlay-drift.sh通过；受管字节与executable mode无漂移。Task validate指定当前Delivery后通过；首次未指定返回delivery_selection_required。长context注入警告不代表正文已读，必需正文另按原方法完整读取。主会话实际目标resolve-python执行成功。

## 实际 native caller

新独立Agent从改后installed指引出发，处理一份尚无同内容Issue绑定、以#795作背景的新草稿。Agent自行选择issue_refs=[]，terms保留#795及主题，issue_binding=null。它实际调用原Sync read/main固定B，完成duplicate、当前Docs/code/tests、history语义审查与AI Gate；history返回20候选，#795按terms命中rank1/score802，选中并完整读取其summary与prd。该分数仅为本次观察，不是terms/issue_refs等价或排名承诺。

原record code0；check code0/status=passed/typed_exit=context_ready；原invoke code0/exit_id=context_ready，stderr为空。完整调用输出由实际caller在当前会话保留。该观察与fixture区分，不由模板/预填pass产生。曾有一次并行reader返回runtime_dependency_missing，顺序原reader重试成功；保留首错，未repair runtime或修改digest/state。另有本地变量ReferenceError及过早解析空stdout，均在调用者原装配内恢复。

## 知识与证明边界

原RDT phase2返回ssot_current：本次仅澄清canonical精确字段；现有local-fix-intake三层责任与关系无差额，不创建空贡献。Planning Architecture无影响，独立committed Architecture与完整Review仍待执行。

本次建立原Discovery公开边界内的指引、普通纠正、绑定兼容及目标采用证据；未进入下游Clarify/Readiness或真实Issue创建。未验证业务现场外部采用、生产效果、formal_fork_source_lock和完整多平台安装/升级/Release矩阵；这些不属于AC872-01。
