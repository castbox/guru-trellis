# #408 Test 增量

状态：`draft`。以下为验收合同，不替代各owner的当前检查；具体命令与实际结果分别从当前task执行计划及运行证据取得。

| Identity | 必须证明的结果 |
| --- | --- |
| T408-01 | commit/CI/run/head/success与本地build marker、CLI/core版本一致；普通stale来源不接受 |
| T408-02 | 官方生成+Guru reapply后的source、dogfood、installed身份和ownership/drift一致 |
| T408-03 | 真实six-step public stdout经正常authoring到创建、双端mapping、boundary、受控激活，再primary→linked-task→primary；同session四入口一致，foreign session不借用 |
| T408-04 | 实际Agent入口脚本/示例可达，正常语义输入不预填recorder私有派生字段；缺AI判断/普通stale内容被拒绝；native Agent按合同完成原链；23/97/78与retired边界保持 |
| T408-05 | 普通自动异常被如实报告，不转no_task、不自修复、不虚报完成 |
| T408-06 | commit/push/PR/merge/closure/tagRelease/cleanup按独立操作确认，未确认后项不执行 |
| T408-07 | 手动成功不改写Guru完成状态，结果与workflow residue分离 |
| T408-08 | 一个真实focused installed使用目标build；缺失的外部/Agent/远端验证标UNVERIFIED |

当前已取得固定Fork构建/TypeCheck、canonical与dogfood session回归、三平台Guru投影，以及一个本地candidate Codex focused installed的两轮update/reapply证据。它不构成远端exact-ref发布或predecessor完整升级矩阵证明。

D408-05已补齐正常authoring到激活的验证：相关四包82项、Planning 22项现有测试通过；installed六步stdout链及24个出口族通过，四份mapping、boundary、空上下文拒绝、受控激活和双端四次hook检查通过；三个退役数据profile的workspace集成测试通过。旧fixture直接复用当前创建链，重复派生算法和旧helper测试已删除，不恢复退役scope或补mapping路径。

native Agent在具备正常项目基线的隔离fixture中，按安装后的合同实际完成六步、Architecture/Planning门禁、受控start及双端current/context/四次hook调用，任务进入`in_progress`。该证据来自文档澄清和正常输入更正后的执行，不是零提示首次通过；Planning未预填私有token。GitHub/fetch为mock，直接hook调用不证明宿主自动分发，亦不证明真实远端mutation或Release矩阵。

T408-06/07 的命令效果由 [stateful test](../../../trellis/skills/guru-team/tests/test_manual_git_fallback_stateful.py) 覆盖：真实临时Git/bare remote及内存fake provider分别核对单项副作用、后项零执行、unknown读取与residue字节保持。该测试不包含AI授权函数；对话选择由读取当前canonical合同的native只读演练独立检验。这两类证据单独不证明Agent判断到实际执行的连接，连接证据见下段。

连接证据使用同一隔离fixture中的native连续演练，实际驱动本地commit、push及内存provider的PR创建，核验未进入后项时零执行与residue保持。该证据仅属于测试环境，不证明实机 `gh`、真实GitHub权限或发布结果；对话内容不写入本贡献或runtime产物。

静态合同测试只是文案投影证明。Agent行为fixture、真实installed-mode与远端mutation必须分别披露，不能互相替代；完整累计发布矩阵不由本task自动扩张执行。
