# D5 来源准备实施

## 唯一 Delivery Policy

policy=partial。本批独立交付canonical精确Fork lock与当前来源文档，形成clean committed来源，供D6原source_locked维护消费。D6尚需匹配工具安装、目标native/peer保留验证、已冻结before→after和真实Guru PR链集成。公开candidate_content_ref对immutable snapshot重复hash仍由原上游公开owner承接；其完成并复验前，整体#589不得完成/关闭。

## Docs SSOT Plan

strategy=ssot_first。canonical source lock、根/workflow/presetREADME与现有项目.trellis/spec/docs/public-docs.md是当前来源authority；D5不更新本Task安装投影；D6从clean source经原source_locked tools-only同步，历史archive保持。历史版本/前驱/D1–D4证据保持。无业务需求/接口变化，原RDT owner判定影响，不新增平行authority；Architecture原owner负责final/Phase2/Branch/Publication及Completion适用入口。

## 执行顺序

1. 原Author修订候选→独立candidate→当前方案→Wording→fresh final_plan→八维Approval→Activation。
2. 仅改canonical lock精确commit/parents/tree/CI及当前映射；正常built Fork做validate_fork_source，source lock version轴不变。
3. source/现有installed-package/ownership/三平台drift及mode定向验证；现有installed验证不证明新源安装。原apply.sh --repo .首次因historical archive迁移预检失败且零写入，保留结果；不迁移、不绕过。无历史Task代表target可经原apply验证新source投影，逐个核对sidecar。本Task Guru投影/receipt与upstream脚本均留给D6原source_locked tools-only，本批不使用tools-only。
4. Docs/RDT影响核对、fresh Phase2 Architecture和完整Check；精确TaskCommit后按实际B..HEAD重新建立candidate/currentCheck，再独立完整BranchReview、Readiness、Refs-onlyPublish/Merge。
5. 原Completion按实际D5事实判additional_delivery_required，建立D6承接真实clean source；不提前使用D5dirty来源做formal tools维护，不把source-only准备宣称安装/性能完成。

## 直接工程资料

performance-contract.md及外部raw14组before已先于source修改冻结，D6消费，不作本批after通过宣称。原失败和未验证层级保留；完整Release矩阵归#575。
