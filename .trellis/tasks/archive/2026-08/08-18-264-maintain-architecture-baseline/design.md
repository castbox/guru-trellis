# 设计：guru-maintain-architecture-baseline

## 1. 公共合同

新增 stable skill id `guru-maintain-architecture-baseline`，`judgment_mode=semantic`，Interface 1.4。四个 profile 的输入只包含 caller、repo/issue/task locator、baseline locator（若存在）、适用 scope、当前 transition/freshness token 与 profile-specific contribution；输出按 exit 独立定义：

- `baseline_current`：active/draft locator、baseline version/status、applicability scope、最小 freshness identity。
- `sync_required`：baseline locator/version、命中的 contribution scope、唯一 promotion/repair consumer。
- `baseline_incomplete`：baseline locator/status 与唯一 Bootstrap/repair consumer。
- `architecture_conflict` / `contract_incomplete`：当前 task-owned scope、baseline identity 与 Planning/design consumer。
- `fitness_regression`：受影响 scope、fitness fact locator 与 implementation/check consumer。
- `blocked`：稳定阻塞码与 fail-closed remediation。

完整扫描、决策历史、Git snapshot、hash bundle、review narrative、授权和 recorder 状态保持 owner-private runtime；consumer 只读上述 projection。

## 2. Authority 模型

目标仓库的 `docs/architecture/` 由 README、foundation/current/target/domains/integrations/gaps/governance/plans/adr/templates/evidence 分区组成。FOUNDATION 选择横向技术栈基线 identity/version/scope/exception；项目 baseline 记录 CURRENT、TARGET、DOMAIN、INTEGRATION、GAP、GOVERNANCE、PLAN、ADR、EVIDENCE 的状态和 locator。状态转换由 AI 判断，脚本只校验目录、链接、版本、引用、diff、测试与 fitness facts。

`bootstrap_foundation` 可恢复 draft/incomplete；`promotion` 只把已 review 的 task-owned contribution 投影到当前 active baseline；`repair` 处理 stale/incomplete/index/迁移问题。promotion 前重读 live baseline，普通 stale/conflict 只阻塞当前 contribution，不使其它 task evidence stale。

## 3. 实现边界

canonical package 提供 interface、schemas、runtime、scripts、tests、evals。共享 registry/discovery/installation 读取当前 graph；workflow 只增加必要 markers 和薄 projection。preset installer 通过 package inventory 同步 canonical、安装副本和平台 overlay，dogfood 通过 apply.sh/reapply 保持一致。不得新增第二套 resolver、跨 task ledger 或 shared tracked handoff。

## 4. 验证策略

单元/contract/eval 覆盖四 profile、状态误判、ADR projection、typed exits、projection 最小性、freshness/stale、不同 task contribution 隔离及正常 conflict。安装验证覆盖 clean throwaway current-version install、existing update、workflow preview/switch、preset reapply、平台 parity、drift、`.new/.bak`、executable mode；不宣称 v0.6.15。
