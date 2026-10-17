# D5 来源准备结果

本批只准备 canonical Fork lock 和当前来源说明；目标 tools、Guru 投影/receipt、after 与完整 Guru PR 链仍由后继 D6 验证。整体 #589 未完成。

精确来源为 castbox/Trellis@c7bd746b42d75f73534c85e263cd6b51fe0e5287，tree 02c6ec8688920d8acb56d1467d6725b03012c0e0，ordered parents b0d87f952043058e21001a002b661bf2db56b1fa / bf8130fedceee907836bd0a2215854b38a8bf891，成功 main CI38994652194。CLI/Core 0.7.0-castbox.3 与 pnpm10.32.1 保持。

原 validate_fork_source 对独立干净完整 checkout 的正常 build 与 source stamp、commit/tree/parents、live CI、CLI/Core、package manager、212 templates 验证通过。发布附件 SHA256SUMS 全通过；独立 source build 与发布包 Core272项一致，CLI736项仅两个Python模板 bytes相同但mode分别755/644，因此后续正式source_locked采用source-built成对package roots，不调整包mode伪造匹配。

现有 source/installed package validator、upstream ownership（40skills）、Claude/Codex/Cursor dogfood overlay drift、当前文档映射、mode 与 diff hygiene 通过。这里 installed 验证只覆盖原安装内容，不证明新Fork已采用。原 test_fork_preparation 四项测试通过：当前README来源一致、构建准备正常失败即停止、同版本stale build拒绝、缺Guru绑定诊断。未新增镜像测试或执行完整Release矩阵。

原 apply.sh --repo . 首次执行在写前返回 upstream_delivery_migration_required：当前checkout保留的historical legacy archives不满足普通安装预检。没有投影写入、没有sidecar；2535份tracked上游脚本和Task preimage保持。本批不迁移archive、不绕过预检、不手工patch脚本。原Check返回planning_stale后，原Author将需clean source的完整目标安装/投影留给D6 source_locked tools-only。当前.trellis/guru-team/trellis-source.json仍为其原安装来源，此处不声明parity。

public-docs真实落点为项目spec .trellis/spec/docs/public-docs.md；不存在preset canonical spec/docs映射。本批直接更新原项目文档，不新增第二来源或installer映射。RDT原owner核对既有来源采用合同覆盖配置变化，无共享authority增量。稳定.3 lock、D1-D4历史结果及peer Task保持。

上游normal local_commit性能证据不能替代Guru pull_request链。公开candidate_content_ref在immutable snapshot上对相同blob物化路径重复hash的AC06残余仍由上游公开owner承接；原技术探针3/30paths、uniqueOID1对应4/31次SHA256构造（含aggregate一次）、oracle摘要一致，只证明该技术路径，不冒称live provider链。D6消费本Delivery performance-contract.md与此前冻结14组before；不放宽门槛，不将D5来源准备计为after收益。完整Release矩阵由#575承担。
