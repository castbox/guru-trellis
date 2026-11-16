# D1 实施与验证计划

## 1. 输入与引用

读取整体 .trellis/tasks/11-16-872-discovery-reference-binding/prd.md、本批prd.md、design.md全文（§3为唯一来源处置），当前#872完整正文。原Discovery合同/schema/common和既有测试是实施前必要输入。共享读取/写作、skill-package和测试有效性spec按实际层加载。独立Architecture candidate_assessment已返回no-impact，不代替final_plan或Approval。

## 2. 有依赖顺序的步骤与文件责任

I1：原Author完成计划与JSONL；独立Architecture final_plan后原Approval/Activation。
I2：implement worker只改canonical Discovery SKILL.md、references/contract.md、tests/test_runtime.py。按design §4就地补规则/导航/普通恢复及实际public wrapper断言，不改schema/runtime/DTO/权重，不手改受管副本。
I3：运行V1/V2，检查原合同条件与结果，保留首错。主协调者通过原tools owner把完整source同步本checkout；读回实际installed和声明平台投影，执行V4。
I4：独立native caller按改后installed指引执行V3，主会话只给场景和合法边界，不给其组装结果或预写pass。记录最小实际结果供当前Review/Completion使用。
I5：原RDT/Architecture完成必要知识处理/读回。TaskCommit覆盖全部canonical、受管与Task元数据后构造完整固定B..H candidate，begin_check；随后一次独立完整committed Review、Delivery Review/readiness、Publish/Merge、whole Completion/Closure/Finish/Cleanup。

## 3. 验证入口、输入与预期观察

V1/V2：用repo managed Python，在PYTHONDONTWRITEBYTECODE=1与必要PYTHONPATH下执行Discovery tests/test_runtime.py中的Git-object recovery定向用例以及test_contract.py；原public wrappers被实际调用，误填失败与纠正context_ready、terms/null独立观察。实际选择的命令与结果记最小verification正文；失败不能预填通过。
V3：改后installed Skill/contract的实际native调用方，关联已有Issue作为背景、无同内容绑定的新草稿；原Sync/read及Discovery语义/Gate/record/check/invoke。不得真实创建业务Issue，无需下游就绪。
V4：canonical/installed package checker、目标自身resolver和native continuation、dogfood overlay drift、声明Claude/Codex/Cursor投影bytes/mode、sidecar、内存Pythoncompile、Taskvalidate与git diff --check。只有源差额和受影响回归，不扩完整多平台矩阵。

## 4. 停止条件与回退点

来源或范围实质变化回Clarify；新增机制/接口影响回Author及原Architecture；测试失败先定位是否到达产品断言，不把依赖装配失败当产品反证。安装冲突回原tools同操作恢复，不能覆盖用户或peer。验证充分后停止可选实验。无数据/线上配置迁移，不造回滚协议；保留未提交差额可供原writer修订，既有Git/GitHub事务按原owner恢复。

## 5. Delivery Policy（唯一）

full：D1完整覆盖R1—R4/S1—S3/AC872-01，无延期后继范围。独立交付条件是指引正确、public wrapper合同保持、实际Agent可完成Discovery、当前目标投影一致及必要质量结果真实。验证止于组件公开结果；未覆盖外部业务采用、formal_fork_source_lock或完整安装升级发布矩阵。Task保whole Completion/Closure/Finish责任，Delivery合并不等于整体已完成。

## 6. Docs SSOT Plan（唯一）

strategy=ssot_first：原step-local Discovery canonical contract是精确字段与恢复规则唯一正文，先就地补清后验证/受管同步；不复制规则到workflow/README导航。原RDT owner在phase2评估local-fix-intake完整三层关系，若精确package澄清未改变其义务则no-change，不造贡献、版本或共享索引；有真实差额沿原isolated proposal/final_integration在TaskCommit前整合读回。Architecture候选无影响，最终结论与后续适用性由原owner判断。当前结果只写必要Task验证摘要供committed Review与Completion直接消费，不建审核/授权ledger。
