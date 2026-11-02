# #718 D1 实施与验证计划

## 1. 输入与引用

输入为整体accepted_scope、同目录PRD、design第3节唯一来源设计处置、独立Architecture candidate_assessment，以及固定B `610a810d45bb30173906d55c77709389adf1cf31`。没有前序Delivery。

实施前读取 `.trellis/spec/{workflow,preset}/index.md` 及命中规范，尤其 companion-scripts、data-contracts、skill-package-contract、quality-guidelines的test-value/validation-scope/managed-Python、installer/upstream-ownership、subtraction-first-compatibility。官方Trellis workflow/marketplace文档已核；不改上游或全局安装。原 #556、#566 兼容承诺的处分只在design第3节。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、原owner与文件 | 改动和完成观察 |
| --- | --- | --- |
| I1 | 原环境owner；`trellis/skills/guru-team/runtime/{bootstrap.py,resolve-python.sh}`及必要同owner模块/命令 | 完成稳定cache发现、明确显式类别、按需求hint和独立check/repair；不安装的日常入口可启动无pointer worktree |
| I2 | I1；原installer/维护owner，managed_python_runtime、apply参数、upgrade-tools和原upgrade/rollback pointer快照消费者 | 区分默认与显式输入；只写目标选择，保留peer实际选择；新selection-v3.json单写、旧v2一次迁移且保留原文、原新旧载体快照回滚与目标自身验证可执行 |
| I3 | 原Git/Sync owner；sync-base、base_selection、其Interface/schema/commands | 加只读明确对象profile/输出，保留实际同步clean/ff；公开源文件读取能给真实Discovery提供固定tree内容 |
| I4 | I3；Discovery→Clarify→Wording→Readiness→原Create Issue/Task及prepare兼容consumer | 成套迁移base来源、5阶段transition及真实blob/history读取；草案独立绑定，原公开操作走到声明结果 |
| I5 | I1—I4；workflow/Skill/spec/docs原owners | canonical Markdown明确读/同步路由、输入输出、scope和迁移；MIGRATION-718给出精确schema/参数、版本边界、原consumer和退出；不复制步骤到launcher |
| I6 | 原RDT/Architecture owner | 隔离完整proposed当前单元和关系、真实contribution/ADR；独立Phase2 Architecture与candidate Check审完整候选后，原final_integration晋升，再重建candidate与final Check |
| I7 | matching源原upgrade-tools；目标仅本718checkout | 同步dogfood及声明投影；保留Task/session/非目标内容；解决原owner sidecar，跑drift与实际目标wrapper |
| I8 | 原Check→Commit→独立Branch Review→Delivery Review→Publish/Merge→Completion/Closure/Finish/Cleanup | 按当前完整候选和真实GitHub事实交付及收尾；Delivery PR只Refs #718，Closure按整体完成结果单独处置来源 |

代码工作由Trellis实现子Agent承担，主会话协调、维护规划与知识、执行原Git/生命周期owners。实现者只能写分派的canonical模块；不是独自在仓库，不得回退并行改动。跨owner差额先报告具体原因，由协调者接续原owner。3000行限制对触及的非生成代码执行；机械拆分保持职责和行为。

## 3. 验证入口、输入与预期观察

验证ID及对应验收以design第8节V1—V8为准。执行顺序：runtime/unit→原公开wrapper隔离因果对照→基线/来源完整consumer链→维护/rollback→source/installed与代表性安装→Agent路由→完整candidate Check。

- V1/V3复用已建立的隔离旧安装：原bootstrap checkout-local、普通Git linked、实际installed invoke的before为`runtime_not_bootstrapped`。在相同需求及入口上更新后须成功，物理venv与cache数量证明复用；不能通过另行逐位置activate完成验收。
- runtime单测与原真实`verify-managed-python-runtime.sh`按新语义改造；稳定identity、lock/API/layout漂移、显式失配、缺seed/依赖来源、失败不改原环境/选择、真实Draft202012 wrapper均保留。fixture cache隔离，不改source pointer来构造失败。
- Git/Phase0 targeted suites从真实新只读公开输出开始，使用正式record/check/invoke到原声明结果。模拟GitHub仅隔离外部provider；不能手写上游pass、补偿产生者输出或发布产品Issue。独立检查真实Sync拒绝和草案/基线身份。
- 维护验收经原source-loaded `guru-upgrade-tools` prepare/invoke和原rollback；保留同一public operation，执行目标自身native/installed/resolver。比较非目标工具/Task/session/新旧选择bytes及实际解析值。补充同一位置canonical新resolver与旧installed guard共存，`--print-active-pointer`定位新writer；新载体存在但无效时拒绝，不能回退旧v2。
- 至多一个代表性clean安装；同一样本承接reapply与声明投影。完整多平台/Release矩阵不运行，也不记为本项失败。运行命中的source/installed package validator、`check-upstream-ownership.sh`、`check-dogfood-overlay-drift.sh`、可执行mode和recursive sidecar检查。
- 按quality-guidelines的固定源范围执行内存Python syntax check、受影响Bash的`bash -n`、JSON/schema和`git diff --check`、official context与Task validate。工程命令结果只是事实，不能替代原owner语义Check/Review。
- V8由实际Agent读取当前workflow/公开合同，使用草案与固定Git来源调用原链；保存该Agent实际观察的最小Test结果。文本/分发通过不冒充Agent行为。

每项验收在唯一Test当前单元记录实际入口、观察及证据边界；行为等价场景共享事实，不复制测试矩阵或完整命令历史。缺前置记具体blocked/SKIP，不冒充pass。

## 4. 停止条件与适用回退点

缺可用CPython3、锁定依赖来源、matching公共维护API、目标工具冲突或公开consumer能力时，只停其依赖动作，保留实际诊断并继续独立必要工作。实质scope/authority/owner/持久化变化回原Clarify/Author/Architecture；普通实现修复沿当前Phase2。

环境构建或真实wrapper失败不提前替换可用cache/选择。tools安装中断/回滚沿原同operation恢复，不造第二备份或转换Task。未知用户修改和sidecar由原owner审查，不能手工覆盖受管副本来冒充同步。保留其他worktree及本次范围外文件。

Git/GitHub交付动作由原owner预览并审查精确当前文件、HEAD与目标，再执行其当前对话副作用边界；不将授权写入任何artifact。远端结果不明时先读实际状态，不重复push/建PR/merge。

## 5. Delivery Policy（唯一）

`full`。D1覆盖现行R1—R11和A1—A8，无预定后续切片或转交业务仓的验收。Completion条件为实际实现、必要拒绝、迁移/回滚、真实入口/直接consumer、投影和Agent行为均有本仓证据；不是“全部现有Delivery已合并”即完成。

本项不承担完整Release矩阵、跨平台真实Agent全量执行或业务仓采用。它们是既有独立边界，不是本Task内部延期责任。若某项A1—A8不满足，仍属于本Task待完成义务，不能靠标记deferred完成。

## 6. Docs SSOT Plan（唯一）

strategy=`delta_first`。原RDT owner维护环境/基线这一完整当前能力单元及必要R/D/T关系：拟落点 `docs/{requirements,design,test}/current/runtime-location.md`，保留原stable alias与明确替代范围；原Architecture owner维护命中职责/集成完整单元、ADR-027的窄替代和新ADR。导航仅增加实际identity/locator/关系，不能追加业务摘要链或全局版本号。

候选阶段写本Task隔离proposed定义和有内容contribution；尚未晋升时不改共享CURRENT。直接consumer是日常wrapper/环境恢复、原只读Intake及维护/审核owners。独立Architecture及candidate Check覆盖完整实现和所有proposed内容；只有其实际出口进入final_integration。原owners核真实目标与intervening delta，晋升完整定义后读取实际写入，再重建包含所有body/关系/导航差额的candidate，重新begin_check、final Architecture/Check、Commit和独立完整Branch Review。

public README、MIGRATION-718和命中managed spec由各原源码owner维护并随matching preset分发；旧历史设计/原始失败保留历史身份。源码同步、安装通过与软件发布分别报告。
