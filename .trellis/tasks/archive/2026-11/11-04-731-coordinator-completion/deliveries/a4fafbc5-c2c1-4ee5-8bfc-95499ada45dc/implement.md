# D1 实施与验证计划

## 1. 输入与引用

读取本批 prd、design（第3节为唯一来源设计处置）、整体 accepted_scope、Issue #731、共享方法和两完整 Skill/调度合同。实施前加载 .trellis/spec/workflow/clear-technical-writing.md、workflow-contract、skill-package-contract、quality-guidelines 的测试价值/范围、subtraction-first-compatibility，以及 preset installer/ownership 适用条款。历史事实见 research/historical-observations.md。无前序。

## 2. 有依赖顺序的步骤与文件责任

1. 原 Author/实施协调先完成历史刷新和隔离验证载体调查。保留修改前方法，在当前已定 V1 输入记录baseline，不预填失败。实施 Agent负责共享方法、两包 SKILL/local contract/必要examples/forward cases；只修改实际受影响文字。
2. 原实施 Agent将目标责任、主动调查/商讨/质疑、结果再判断、等待有效性、合法后续和终局阻塞收敛至共享方法，更新心跳及两调度消费。保持public接口及调度边界。
3. 测试实施 Agent负责同一package tests内可复用的两入口隔离事实provider/真实Agent验证载体，host-only场景审核标准与结果分离。不得把语义决策写进 fixture；需要自然语言处置时由真实Agent承担。输出置外部临时目录，不新建生产调度器。完成 V1..V4 并由独立review核中立性与轨迹，不凭exit/count判定充分。
4. 原 RDT owner负责 task-owned proposed/requirements、proposed/design、proposed/test 的完整 issue-orchestration 单元，先保持 shared current 未变；并与原 Architecture/候选Check完成质量链。
5. 原 guru-upgrade-tools 负责目标wt的canonical→installed/dogfood同步；精确preview/prepare后执行，选目标实际平台与现有CLI/Core0.7.0-castbox.6，local_candidate边界显式保留。定向reapply、drift、mode/sidecar及Task/session保持验。
6. 原实施协调构造全内容candidate、begin_check；独立Architecture和candidate Check覆盖代码+隔离Docs。实际candidate_checked后原RDT final_integration晋升，重绑最终candidate再做最终Architecture/Check、TaskCommit、完整Branch Review、Delivery Review和Publication/Merge。随后Task Completion、Closure、Finish及有界Cleanup。

## 3. 验证入口、输入与预期观察

V1..V4 按 design 第8节从真实显式Skill入口执行，保留baseline/候选的完整原始trace、实际模型与宿主版本、实际操作与子Agent结果，外部临时保存。只给合成目标/事实/约束；provider无推荐、无自动下一指令/semantic gate。成功至终点、等待至变化承接、阻塞至安全收口；如本轮出现实际缺陷修正后定向重验。

V5 使用原 discover-skill-contract/源包validator与已有相关分发测试，JSON解析、必要Python内存编译、官方Task validate、git diff --check；验证命令按当前help选精确参数。V6使用原tools owner和 check-dogfood-overlay-drift.sh，核三类投影、可执行位与递归sidecar。一次同候选定向reapply足以本项；不跑完整多平台throwaway矩阵。

原native provider只是隔离行为层；真实app编排/生产外部效果未验证，不把fixture事实称为生产或live GitHub。

## 4. 停止条件与适用回退点

来源/整体范围变化回Clarify；机制变化回当前资格/Architecture；语义测试失败由原实施owner调查并修正，保留首失败，不改oracle迎合。未知副作用先回读原操作。支持入口缺失先调查原公开入口/owner支持修正，不能制造gate或替必需producer。真实缺外部条件停受影响工作，继续独立必要工作。无数据迁移或版本发布，因此无生产回滚协议；不revert他人改动或清理无关资源。

## 5. Delivery Policy（唯一）

full：本D1交付R1..R9和AC1..AC9，包含合同、真实Agent多轮验证、历史边界、知识与实际投影。无延期切片。代码/静态/安装/行为证据分层；任何必需行为未验证都不能宣称本项完整完成。合并不替Task Completion。原Task整体owner保留未完成责任，失败返工保持本D1，不删建identity。无新增临时能力限制。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原 guru-maintain-requirements-design-test-ssot writer形成3个task-owned proposed完整单元，目标 docs/requirements/current/issue-orchestration.md、docs/design/current/issue-orchestration.md、docs/test/current/issue-orchestration.md（实际测试目录以当前authority核定）。每个单元有稳定identity/必要关系，分别直接服务后续需求、设计和验证维护。原owner candidate review→candidate Check→final_integration读前像/写入/读回，所有actual写入重绑candidate并最终Check。遵守current-knowledge与#711独立导航，不改共享根注册文件。无Architecture决策变化，不创建contribution/ADR。运行方法spec投影由原安装owner维护，历史原记录不回写。
