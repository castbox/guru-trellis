# #532 实施与验证计划

当前仅规划；激活后按以下单一路径执行。

## 1. Fresh 核验与合同先行

重新读取 #532、task lifecycle、HEAD/base、dirty paths、canonical Check、Task Commit/retirement/reconciliation 消费者及 current authority。来源、设计、scope 或架构边界发生实质变化时回到最早受影响 owner，不沿用旧结果。

读取 trellis-before-dev 与当前工程 specs。修改 canonical SKILL.md、references/contract.md 明确空集/非空集两个分支，保留完整九维审查和三 qualifier 的非空合同。同步示例中的真实零候选：删除虚构 no-defect 项，单独保留实际非空全 rejected 的场景。

## 2. 修改原 schema/runtime

在 phase2-check.schema.json 去除 candidate_classifications 的非空下界；在 runtime/common.py 将类型拒绝与空数组分开，保留 uniqueness、finding/scope refs 校验，禁止空集早退跳过其它 gate。

不修改 public schema、checkpoint 版本、token 算法、exit/consumer、execution retirement 或 qualifier 内部逻辑。检查每个 touched 非生成代码文件长度；达到 3000 行时先做机械拆分判断，不重构无关历史文件。

## 3. Package 定向测试和 eval

使用 package/tests/test_contract.py、test_runtime.py、test_execution_consumption.py 的现有入口，增加能检测原缺口的行为用例：
- 原 schema 与生产 validator 接受真实空 list，非 list 继续失败。
- 非空 rejected 与 qualified candidates 的既有行为、唯一 refs 和引用一致性保持；空 candidates 有 findings/scope refs 时仍失败。
- 四 public profiles 的消费者投影与原生命周期：passed 保留 Check checkpoint/匹配执行结果退休；非passed、stale 不退休执行恢复状态；reconciliation 保持原私有结果及 target projection。
- 用正常内容变化证明 freshness，不改 digest/state 构造防伪测试。

更新 package evals 的 semantic_authoring 与 post_owner 场景；分别报告，禁止用 fixture 预填 passed 宣称真实语义审查。命令集合与具体 fixture 按当前测试定义解析，不新增常量自比较或无消费者测试。

## 4. 真实公开调用链

使用原 recorder → checker → public initial_check，取得实际正式结果：
1. 完整当前轮真实无候选，所有前置满足，空 classifications 得到原 passed。
2. 真实候选完整资格判断后全部 rejected，保留分类，无 findings。
3. 当前范围有效 finding 完成资格判断和真实引用后走原 implementation_required；真实规划缺口使用原 planning_stale。
4. 正常缺失 required evidence/Architecture 走原阻塞/回程；正常受审内容 drift 由原 checker 拒绝。

每个结果写入唯一 Test 的实际层级、入口、观察与未验证边界，不保留重复审查历史或 tracked gate。未跑、环境不足或前置缺失标记 unverified/blocked，不能称 passed。

## 5. Canonical、dogfood、installed 同步

通过 canonical preset 执行受控 apply，再运行
`trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 与
`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
检查 changed projections 与全部新 .new/.bak；不覆盖现有用户改动。重应用后再检查 package/discovery 与 drift。若命令需要非已授权资源副作用，先展示精确目标。

一个代表性干净 Codex installed 环境安装完整 runtime，不只拷贝 Skill 文件；用真实 task/规划/正常 session/control state 经其公开 Check 入口验证。临时环境的创建与清理按精确副作用边界执行，清理不隐含。保留本 task 工作区和其它 task。

官方 update 检查只覆盖本修改的受管来源、projection、template hash/sidecar 与 reapply 可恢复性；完整多平台 clean/existing/update/workflow-switch/release-candidate matrix 由专门 owner 承担，本 task 不扩张该职责。

## 6. Docs 和质量门禁

RDT task-owned contribution requirement/design/traceability 承接本增量；test.md 记录上述实际验证、首次失败和剩余边界。共享 current 必须经原 RDT owner promotion，promotion 差额重做受影响 gates。Architecture 按其实际 impact route 承接，若 no-impact 则不制造 contribution/ADR。

完成实现后 fresh Architecture Phase2 + 完整 guru-check-task。后续 Task Commit、独立完整 base-to-HEAD Branch Review、Publication、merge/release/closure 均由原 owner 与各自副作用边界承接；本计划不把规划批准或单元通过当作交付完成。

## 交付定义与未验证边界

一份 Delivery 覆盖 PRD R1–R5 和 AC1–AC8，独立于 #531 完成；task 无剩余内部 slice。#292 恢复、#530 验收、#531 迁移、正式版本发布、业务部署、完整 matrix 均保留给原 owner。当前尚未改代码、执行 package tests、公开 Check 或 installed 验证；本阶段只判断规划的充分性。
