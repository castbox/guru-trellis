# D3 Python 与路径脚本验收收敛实施计划

## 1. 输入与引用

整体根PRD第4–7节、本批PRD DR1–DR4/DA1–DA3和design第3节为当前约束。采用实际candidate_assessment；Architecture .103与constitution-v1保持。RDT完整单元定位见design第4节；实施与审核须读取其当前完整正文和唯一Test。起点为D2实际head cf07d082，已交付PR #634/#639不重做。

## 2. 有依赖顺序的步骤与文件责任

S1：完成Wording、final_plan、Approval、Activation后，主会话作为原RDT owner修改三份 docs/{requirements,design,test}/current/native-compatibility.md。同步新scope，保留旧Git定义与T630-08撤销状态，不改历史requirement/design贡献。

S2：实施Agent负责docs/ci/README.md和docs/requirements-design-test-contributions/630-native-compatibility/test.md。将实际Codex入口表述为显式诊断，当前Test采用成功事实并追加D2合并、Windows600秒失败及本次范围变化，保留历史记录。主会话核对写入，正式执行RDT task_impact_sync。

S3：独立Architecture Phase2和质量owner完成Check；只执行design V3的新文档检查，采用仍适用的V2证据。主会话按精确文件提交；独立完整Review后发布/合并D3，再执行整个Task的Completion、Closure、Finish及精确资源清理。

## 3. 验证入口、输入与预期观察

V1：从已回读Issue和accepted根PRD逐条检查当前RDT；新义务一致，旧Agent义务仅在可定位历史中保留。

V2：读取唯一Test、PR #634/#639及原run报告。成功工程事实采用而非重跑；Windows实际会话仍未完成。不得用CLI0或Actions绿色覆盖实际失败。

V3：执行git diff --check、检查当前diff中的本地Markdown链接及文件清单；返回0/链接存在且无产品代码变化。Check和Branch Review独立判断语义，命令返回0不代替审查。

## 4. 停止条件与适用回退点

源Issue或整体scope变更回原Clarify；候选机制变化回Author/Architecture；发现实际文档遗漏回原writer修正。未解决的真实finding保留，不通过重新运行已成功测试掩盖。无产品发布、DB或运行配置修改，故没有数据回滚协议。只stage本批精确文件，保留并行改动。

## 5. Delivery Policy（唯一）

full：本批完整交付当前验收及文档收敛，覆盖整体剩余AC7/AC10文档差额；本批无延期责任。D1/D2已交付runtime、路径、安装与维护能力。独立完成条件为DA1–DA3及正式Check/Review，无需真实Agent或GPU。整体Task仍由Completion核对AC1–AC10、实际Delivery及证据后决定，不由本批合并自动完成。

## 6. Docs SSOT Plan（唯一）

strategy=ssot_first。主会话原RDT writer定向直接同步当前native完整单元与旧Git边界；实施Agent只写CI说明和唯一Test，不写共享authority。R630-06/BEH630-06→D630-06的现有关系保持；T630-01..07支持当前脚本义务，T630-08明确撤销历史义务。实际执行结果只保留在唯一Test。直接consumer为Check、完整Review与Completion，RDT在最终Phase2前完成task_impact_sync，原Architecture判断影响，不新增全局版本集或空贡献。官方软件发行不属于本Task。
