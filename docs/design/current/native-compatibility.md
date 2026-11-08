# #630 三系统兼容设计责任增量

导航别名：`RDT-DES-NATIVE`；`R630/BEH630`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

状态：current；继承RDT .111、Architecture .102及本Task已审设计；实现/采用状态与知识接受分开。需求由[当前需求](../../requirements/current/native-compatibility.md)单写，测试关系由[追踪](../../requirements-design-test-contributions/630-native-compatibility/traceability.md)定位。

| Identity | 原owner、输入→行为→输出及边界 |
| --- | --- |
| D630-01 | shared runtime base_selection拥有Git root/authority/worktree事实读取，以本机Path比较并按Git UTF8协议读结果；schema owner按标准本地file URI转换读取相对引用，不新增远端schema能力。 |
| D630-02 | bootstrap capability owner选择并验证原生Bash，使用POSIX路径与--invocation -的同JSON stdin进入现有公开wrapper；只调整内部fixture，公开inline输入保留。Python激活owner继续先probe/真实wrapper/staged installed validation后激活，失败保留旧pointer。 |
| D630-03 | TaskCommit原executor按UTF8候选字节写入、读回与验证最终commit，继续真实hook、transaction index/tree/live ref检查。index物化参数仅在正常fixture证明必要后采用；不通过旁路提交绕过这些检查。 |
| D630-04 | installer原owner维护canonical和target scoped attributes及文本copy/generate；bounded block保留用户块外字节，更深规则冲突明确失败。精确EOL恢复仅限声明文本与已知受管来源，恢复后原raw validator验实际字节；不增加第二manifest/hash authority。完整细则由canonical spec/preset/installer.md、upstream-ownership.md及本Task必要ADR拥有。 |
| D630-05 | 来源owner按唯一canonical source lock选择当前固定Fork（#630 当时为castbox/Trellis #53交付commit/.5，本轮采用关系见D687-01）；按所选源码声明pnpm frozen lock正常workspace build及marker验证；原native update/maintain/workflow/recovery接口采用该实际build后Guru reapply。Guru不管理上游entry。 |
| D630-06 | 原CI driver负责目标隔离/环境/执行事实，target负责产品实现；诊断观察目标已声明cases与其真实transport，supplemental保持同target transport且保留首失败。原expected unittest matcher及安装失败状态不弱化。实际验收使用命令行Python脚本及公开wrapper，工程脚本不生成AI语义结果。已交付的windows_codex_session入口保留为维护者显式诊断工具；其独立配置、正常启动及真实结果单独报告，不成为本Task必需验收。 |

没有公共Skill/exit/Task数据模型变更，没有业务DB迁移。受管文本LF/恢复改变原raw-only更新判定的窄条件，由原Architecture独立Phase2和晋升合同承接；其他原owner不变。具体实现、验证与采用状态以真实候选/测试证据为准，本单元的知识接受不证明实现或采用已完成。

本单元修订：`630-script-validation-2026-10-20`。当前验收以 [Issue #630](https://github.com/castbox/guru-trellis/issues/630) 的脚本范围为准。前驱定义见 [cf07d082固定正文](https://github.com/castbox/guru-trellis/blob/cf07d082c046b8e5e3c5050a603f22285821b215/docs/design/current/native-compatibility.md)；其真实Agent会话义务仅在该历史版本成立。本次直接修订当前完整单元，不改历史贡献或全局RDT版本入口。

## #687 当前固定来源采用责任

适用完整前驱为 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea:docs/design/current/native-compatibility.md`。本节承接[当前需求](../../requirements/current/native-compatibility.md) R687-01..03；公开 Architecture identity 及原 source/installer/maintenance owners 不变。

| Identity | 原 owner、输入→行为→输出及边界 |
| --- | --- |
| D687-01 / CON687-SOURCE | 原 source owner 通过唯一 canonical trellis-source.json 采用 `17015f987166f4106034f115d23212446f16d536` / `0.7.0-castbox.6`，同步原 manifest 与精确版本检查及受管 source 投影。正常同源 Core→CLI build 和原 marker 验证保持；历史 .5 来源和已发布 Guru .6 配对不回写。 |
| D687-02 / CON687-TOOLS | 原 guru-upgrade-tools 的 install/source_locked 消费完整、干净、匹配 source/build，沿原 preview→prepare→invoke 执行 tools-only 维护并使用原恢复入口。public maintenance owner 更新官方工具；原 preset 更新 Guru 资产。实际目标 API/字节/mode 与 Task/session/用户内容/peer 保留分别核对；不新增 Guru converter 或来源协议。 |
| D687-03 / CON687-STOP | stop 由所选固定 Fork Core 和匹配 Python 实现。Guru 保持 PR-only 声明及原阶段 owner，通过已安装公开入口消费合法保留的 manual/local_commit 与所需 evidence，核对 stopped、selection、peer/history 和匹配 retry；不修改上游生成资产或以 stop 生成 Completion/Closure。原 D657-03 的生命周期分工保持。 |

测试策略由[当前 Test](../../test/current/native-compatibility.md) T687-01..05 定义，实际采用观察由 [#687 Test](../../requirements-design-test-contributions/687-adopt-castbox6/test.md) 拥有。#630 原 .5 构建及三系统观察保持历史身份。本轮无新 API、持久化字段、Task 数据迁移或 ADR；原严格 source_locked、mode、所有权、解释器、用户编辑和恢复条件保持。

## Current-schema Task 副本迁移责任

本节承接[当前 Requirements](../../requirements/current/native-compatibility.md) R752-01..05。完整前驱为 Git `2ab135ed2d3908966785bb23ad42ada0790f0c81:docs/design/current/native-compatibility.md`。原 Architecture `guru-trellis-architecture`、ADR-024/017 及 source/installer/maintenance owners 保持；上文 #687 的来源选择是其历史采用，不覆盖本节 successor。

| Identity | 原 owner、输入→行为→输出及边界 |
| --- | --- |
| D752-01 / CON752-INVENTORY | Guru 原 prepare_inventory 读取全部 eligible registered project roots、Task/artifact/session raw snapshots 和现有 C4 binding；semantic owner 选择 dispositions。原 binding 仅投影 task_id、lifecycle_generation、source，不添加 target branch/path。Fork migrate2 独占完整 inventory、binding freshness 与唯一实际 bound checkout 校验。 |
| D752-02 / CON752-CURRENT-PEER | Fork 的 mixed Plan2 使用 authority `disposition=current`（无 source_task_schema selector）与 peer `disposition=defer, source_task_schema=2.0`（原 RawSnapshot、无 target record）。public parseTaskRecordV2 解析 peer，并与唯一 projected authority 做完整 parsed record 等价校验；合法格式/key顺序差异可保留原字节。selector2 只属于 mixed defer，不生成额外模型、Delivery 或 migration 资产。 |
| D752-03 / CON752-PRIVATE | Guru 透传原完整 core_plan，不复制 Fork group/equality 算法。原 private migration 仅接收其 selected workspace 中 projected current/convert_active/convert_archive Task；defer peer 永不进入 owner_migrations。普通内容/generation/source/binding/checkout mismatch 或非唯一 authority 由 preview 阻止写入，不合并、删除或重建用户数据。 |
| D752-04 / CON752-RECOVERY | 原 Upgrade begin 冻结同一 source/Fork candidates、Plan2、写集、所有 workspace/common/local session 的 bytes/modes 与原业务/topology anchors。依次执行 Core、原私有 owners、旧 Guru retirement、完整 preset 和实际 activated installed validation。resume 只续原阶段；rollback 检查 managed postimage 与原业务/topology后恢复原preimages、删除本次新增路径，不刷新anchors、不reset Git。 |
| D752-05 / CON752-SOURCE | 原 source owner 固定 R752-05 的精确 merge/parents/tree/main CI；正常 pnpm frozen-lock Core→CLI build 和 build marker 与该 commit 匹配。canonical source lock、dogfood tools-only与实际安装分别取证。正式 source_locked 使用干净已提交 Guru source 及精确 Fork build；旧冻结计划保留其原 package pair，不换包续跑，不发布同版本 npm replacement或修改不可变 tag。 |

采用原 defer selector2 的理由是复用已有 preserve、session 和恢复路径，并由公共 schema/executor 承担唯一 group authority。过滤 registered roots、伪装 legacy 或在 Guru 复制 copy 模型都会违反 R752-01/02 的真实输入与职责。该方案的必要维护成本为完整 source pair 同步、原 public parser/group 回归和 Guru consumer/installed 回归；不增加永久状态、锁或兼容双读。若公共 source schema、binding/checkout authority 或 private projected-task 合同改变，原 Author/Architecture 重新评估该机制。

测试策略由[当前 Test](../../test/current/native-compatibility.md) T752-01..05 单写，实际执行由 [#752 Test](../../requirements-design-test-contributions/752-current-task-worktree-copies/test.md) 记录。#630、#687 的历史构建和采用观察保留原义；当前来源、组件通过与真实目标采用互不替代。无公共 Guru DTO、Task schema 或 Delivery API 版本变化；Plan2 wire 的窄 selector 扩展归 Fork。知识晋升仍沿完整 proposed→独立 Architecture/候选 Check→原 final_integration/readback→actual-after 重绑及最终质量链。
