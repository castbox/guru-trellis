# #408 Test 增量

状态：`draft`。以下为验收合同，不替代各owner的当前检查；具体命令与实际结果分别从当前task执行计划及运行证据取得。

| Identity | 必须证明的结果 |
| --- | --- |
| T408-01 | commit/CI/run/head/success与本地build marker、CLI/core版本一致；普通stale来源不接受 |
| T408-02 | 官方生成+Guru reapply后的source、dogfood、installed身份和ownership/drift一致 |
| T408-03 | 正常primary→linked-task→primary，同session四个入口解析同一task；foreign session不借用 |
| T408-04 | 旧完整package/finish-family/installed链与23 Skills/97 exits/78 commands保持，无retired依赖重现 |
| T408-05 | 普通自动异常被如实报告，不转no_task、不自修复、不虚报完成 |
| T408-06 | commit/push/PR/merge/closure/tagRelease/cleanup按独立操作确认，未确认后项不执行 |
| T408-07 | 手动成功不改写Guru完成状态，结果与workflow residue分离 |
| T408-08 | 一个真实focused installed使用目标build；缺失的外部/Agent/远端验证标UNVERIFIED |

当前已取得固定Fork构建/TypeCheck、canonical与dogfood session回归、三平台Guru投影，以及一个本地candidate Codex focused installed的两轮update/reapply证据。它不构成远端exact-ref发布或predecessor完整升级矩阵证明。

T408-06/07 的命令效果由 [stateful test](../../../trellis/skills/guru-team/tests/test_manual_git_fallback_stateful.py) 覆盖：真实临时Git/bare remote及内存fake provider分别核对单项副作用、后项零执行、unknown读取与residue字节保持。该测试不包含AI授权函数；对话选择由读取当前canonical合同的native只读演练独立检验。这两类证据单独不证明Agent判断到实际执行的连接，连接证据见下段。

连接证据使用同一隔离fixture中的native连续演练，实际驱动本地commit、push及内存provider的PR创建，核验未进入后项时零执行与residue保持。该证据仅属于测试环境，不证明实机 `gh`、真实GitHub权限或发布结果；对话内容不写入本贡献或runtime产物。

静态合同测试只是文案投影证明。Agent行为fixture、真实installed-mode与远端mutation必须分别披露，不能互相替代；完整累计发布矩阵不由本task自动扩张执行。
