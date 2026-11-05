# D1 实施与验证计划

## 1. 输入与引用

读取整体 PRD、D1 prd/design，design 第3节是唯一来源设计处置。加载 quality-guidelines Test And Validation Value、root contract、Author planning-body 与两个模板、Phase2 §2.1、当前 RDT/Architecture authority 及必要关联条件。首次 D1，无前序结果。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | owner、文件与行为 | 完成观察 |
| --- | --- | --- |
| I1 | implement worker：canonical quality-guidelines、root contract/SKILL、Author planning-body/两个模板、Phase2 workflow 与 Check/Branch 必要引用 | 一套统一方法，原 owner/接口保留，无重复标准 |
| I2 | eval worker：现有 package tests/evals 下定向事实案例与真实执行 collector | V1–V6 实际输入/动作/输出采集；host 判断与被测输入隔离 |
| I3 | 原 RDT owner：docs/requirements-design-test-contributions/735-behavior-causal-validation 下完整 proposed 单元及关系 | 当前规范差额可被候选 Check 阅读；共享 current 未提前写 |
| I4 | root tools maintenance：完整当前 canonical source 更新本 Task checkout 受管副本 | actual native/installed/source/projection/reapply/drift 证据，Task/session 保持 |
| I5 | 原 Architecture/Check：完整候选与 proposed RDT；通过后原 maintenance final integration | 实际完整定义写入、读回并重绑 candidate，最终 Check 覆盖全部 after |
| I6 | root：TaskCommit、完整 committed Review、Delivery Review/Publish/Merge、Completion/Closure/Finish/Cleanup | 通过原 typed exits 完成实际交付和归档，不从合并推定整体完成 |

## 3. 验证入口、输入与预期观察

执行 design V1–V6 的真实原入口事实评估，逐例保存输入、实际工具/输出及 AI 判断到本 Delivery validation 正文，原始运行记录放外部临时目录，不写授权/过程台账。采集器只搬运事实；不能关键词或固定 exit 代替语义判断。使用适用 managed Python 执行 root/Author contract/runtime 及新增 collector 定向检查。

V7 使用 source/installed package validators、guru-upgrade-tools local_candidate、本 checkout native 入口、check-dogfood-overlay-drift.sh 与 recursive sidecar 核对；workflow 原 phase extractor 与 git diff --check、task context validate 和规定 JSON/Bash/Python syntax 检查。顺序由实际依赖决定，规划不预填 pass。完整多平台 clean/update/release matrix 与 formal Fork source-lock 未覆盖，不成为本普通 Issue 的验收。

## 4. 停止条件与适用回退点

来源/范围变化交原 Clarify；机制/owner 扩张先停扩张写入，经原资格与 Architecture。必要测试失败保持缺口，依据具体问题修复；已充分的验证不因阶段/执行者改变重跑。语义评估设施失败先判能否修装配或用等效观察；不能无限扩大设施工作，也不能把受影响验收写通过。安装冲突按原 maintenance 恢复，不覆盖用户改动。没有 DB/生产部署，无额外回滚协议。

## 5. Delivery Policy（唯一）

full：D1 覆盖 R1–R4/S1–S6/AC1–AC7，范围内没有延期工作。独立交付条件为统一方法及全部必要消费者、真实语义评估和受管采用均有证据；语义、确定性和安装分别判断。剩余整体责任仅为本批正式交付及 Task Completion/Closure/Finish，不借一个 Delivery merged 宣称完成。未验证完整平台矩阵和外部项目采用不在本次 accepted scope。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原 RDT owner 将方法差额准备为 task-owned 完整 proposed 叶单元，映射 requirement/behavior→design/contract→test/scenario。质量规范仍单写测试方法，叶单元引用而不复制完整规则。candidate Architecture/Check 后 final integration 晋升 docs/{requirements,design,test}/current/behavior-validation-method.md 或原 owner 查明的真实所属单元；不预建空贡献，不改共享总导航/无关版本。Architecture 若 no impact 不建贡献/ADR；有实际影响按原 owner 当前结果处理。最终 Check 与 committed Review 覆盖实际晋升。
