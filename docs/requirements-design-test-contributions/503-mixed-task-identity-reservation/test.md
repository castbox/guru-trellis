# #503 风险匹配测试贡献

状态：source 与代表性 clean-installed 定向验收通过；当前 task-owned reviewed candidate。共享 current .75、软件发布、业务仓安装与部署不由本结果宣称完成。

| 测试 identity | 实际观察 | 结果 |
| --- | --- | --- |
| T503-CREATE / S503-CREATE | 正式 public record_plan/create/ensure/bind/ref-id resolution 在 current checkout 与 registered 历史 mixed header 共存时创建并唯一解析全新 gen0/planning task；未 mock Fork writer | PASS |
| T503-RESERVE / S503-RESERVE | exact/casefold id、occupied ref/空目录、branch history、unresolved ledger 拒绝；资源数量不变 | PASS |
| T503-REJECT / S503-REJECT | 无关 source/generation/status/未知非身份字段不影响占用；selected目标严格current校验；活动坏JSON/非object/缺失非法id具体拒绝。create stop携带field_path/remediation；identity公共输出仍仅reason_code，直接reader验证具体诊断 | PASS |
| T503-PRESERVE / S503-PRESERVE | 成功/拒绝前后历史bytes/modes及其它checkout Git状态不变；same-result recovery不重复mutation；inventory/migration完整分类保持 | PASS |
| T503-INSTALLED / S503-INSTALLED | 精确Fork source-lock/build、source与clean preset实际安装入口通过；canonical/dogfood/platform/schema/stop consumer/drift/reapply/sidecar检查通过 | PASS |

## 真实验证

生命周期 runtime suite：156 PASS。guru-create-task contract suite：22 PASS、零SKIP，覆盖 source 与代表性 clean-installed 同一正式入口。独立检查复跑相同两suite通过；移除无生产consumer bool wrapper后本会话再复跑两suite仍为156/22 PASS。

复跑入口（从本task checkout）：

```sh
bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/runtime/task_lifecycle/tests -q
TRELLIS_FIXED_FORK_SOURCE=<精确source-lock且已正式构建的Fork路径> bash trellis/skills/guru-team/runtime/resolve-python.sh . trellis/skills/guru-team/runtime -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task/tests -p test_contract.py -q
```

source-lock/upgrade contract：73 PASS；official projection：9 PASS，actual dogfood 183文件/hash/.version PASS；Shared/Claude/Codex/Cursor installed entry：2 PASS。source/installed package validator PASS。official reapply与preset reapply零剩余改动，drift PASS，无未处理sidecar。无consumer wrapper移除后的preset首次apply生成的唯一preimage备份已核对并可恢复保留于临时目录；重apply成功。

正式Fork绑定5c760463680ffc10a3f26957b330c57a4b0c3ff8，parents为cc5f9a30652be29cffee9acc7e14d5dc5daaf04c与a776a97cd5699f6324582ae57245542f80576a6c；tree为9f044e4233edc90fd2b3169442ea13e5d1951780，成功main CI 37735554354。CLI 0.7.0-castbox.3 / pnpm 10.32.1；精确来源clean build与build marker验证通过。

## 未验证边界

Backend #378现场失败仅是根因证据。clean-installed fixture证明本候选的实际安装行为，不证明Backend原仓升级、#378正式intake恢复或#379漏洞修复。完整Release/远端升级矩阵、业务安装和部署另属各owner；本次不新增攻击、竞态或fault-injection测试。独立 committed Branch Review、shared-current promotion与Delivery仍是后续阶段。
