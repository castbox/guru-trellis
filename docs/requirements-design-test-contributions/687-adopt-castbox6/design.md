# #687 固定 .6 来源采用：设计差额

状态：proposed；适用完整前驱为 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea:docs/design/current/native-compatibility.md`。继承公开 Architecture `guru-trellis-architecture / docs/architecture/README.md / 7718d129bcb2055d77c7f43d0e4edca9aee313ea / active`；本 Task 的三处 Architecture 差额由其原 owner 独立维护，无新 ADR。

完整拟生效责任由 [proposed Design](./proposed/docs/design/current/native-compatibility.md) 单写。D630-05 保留原 native update/maintain/workflow/recovery、正常 build/marker 和 Guru reapply；D687-01..03 对应来源映射、严格工具维护和公开 stop。canonical source lock 仍是唯一来源 authority，installed source 文件仍是受管投影；不存在新 API、数据字段、状态机或 Task 数据迁移。

#630 当时 .5 / #53 来源和实际观察保留为历史。当前 .6 采用不重写该观察，也不替代原工具维护 Skill 的完整合同。生命周期 R657-03 / D657-03 和原阶段 owner 的 stop/release 责任保持；本轮只验证已保留的 manual/local_commit 可通过原公开入口停止。

[traceability](./traceability.md) 定位完整前驱、拟生效正文、原合同和测试关系。候选 Check 后才由原 RDT owner 执行 final_integration，并由 implementation 重绑实际候选后进入最终 Check。本文不声明 promotion、采用或交付已完成。
