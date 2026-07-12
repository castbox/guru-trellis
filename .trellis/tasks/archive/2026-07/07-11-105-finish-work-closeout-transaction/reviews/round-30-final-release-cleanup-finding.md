# Issue #105 Round 30 最终放行审查报告

## 审查身份

- technical agent：`/root/final_release_review_105_round30_cleanup`
- 逻辑角色：最终放行审查代理
- reuse_decision：`new-agent`
- reviewed_head：`6c6f9fde848a4fd11500f33550ee4b2fd0da0f9d`
- base：`origin/main@3dec302206783fe4ac1296066e9a1789c995d58b`
- 完整范围：18 commits、62 files，`16282 insertions / 6570 deletions`
- 执行边界：本轮只读，未修改文件，未运行 recorder/review gate，未 commit、push、创建 PR、archive 或关闭 issue。

## Findings

### P1：减法后的唯一执行器与 PR body 来源未完成需求和 Docs SSOT 收敛

证据：

- `prd.md:77` 仍要求“`publish-pr` 保持内部 executor”，但同文件 R9 又要求 `trellis-finish-work` 是唯一生产实现、`publish-pr.sh` 只能阻断，两条 requirement 直接冲突。
- `README.md:502` 仍公开允许 `--body-artifact`，并称 generated body 可进入 draft/preview。
- `.trellis/spec/workflow/workflow-contract.md:569` 仍将 `--body-file | --body-artifact` 定义为当前合同，并保留 readiness artifact 相对 `body_file` 的解析规则。
- `.trellis/spec/workflow/companion-scripts.md:316` 同样允许 `--body-artifact` 和 generated draft/preview body。
- 实现已是另一合同：`validate_publish_invocation` 无条件阻断 `publish-pr`；`resolve_closeout_reviewed_body` 拒绝 `--body-artifact` 并只接受当前 task-local `pr-body.md`。旧 body generator/resolver 已删除。
- `design.md:242` 明确要求 README 和 companion specs 全部改为兼容性阻断路径，因此不是无关历史措辞。
- Live #105 范围纠偏 comment 明确要求 finish-work 唯一实现、publish-pr 只阻断。

影响：

- clean install 用户按 README 或 durable spec 操作会稳定得到 exit 2。
- 项目 SSOT 仍授权刚删除的备用 body/publish 合同，后续实现者可能据此恢复第二套路径。
- 违反 #105 的 canonical/dogfood/README/durable specs 同步验收，当前 Phase 2 的 `docs_ssot=true` 语义结论不成立。

修复要求：

- 将 PRD R7 改为 `publish-pr` 仅是兼容性阻断入口。
- 将 README、workflow contract、companion spec 统一为：closeout 只能使用当前 task-local `pr-body.md`；不得接受 `--body-artifact`、generated fallback 或 readiness-relative body resolver。
- 增加文本合同回归，禁止这些文件重新出现允许 `--body-artifact` 或 generated publish body 的肯定语义。
- 修复属于 non-metadata Docs/规划变更，必须重新执行 Phase 2、closure review，再派发 fresh final reviewer。

## 删减与调用图

- cleanup 全部 16 files：`+159/-3882`，净 `-3723`。
- cleanup `trellis/**` 7 files：`+101/-2862`，净 `-2761`。
- canonical production：`+3/-959`；canonical tests：`+74/-1874`；installed closeout smoke 未删除。
- 删除 14 个顶层函数：13 个旧 publish/recovery/summary-tail 专属 helper，加无生产调用的 `resolve_closeout_state`。
- 删除 43 个 dormant/self-proving tests，新增 0 个替代内部状态测试。
- 相对 `origin/main` 新增 88 个顶层函数，88/88 全部从 `cmd_finish_work` 可达。
- 当前 `cmd_publish_pr` 闭包仅含 blocker 与自身；当前 12 个 main 不可达函数全部在 base 已存在。

## 运行与测试证据

- canonical/installed `publish-pr.sh` 使用无效 root/task/repo 调用均固定 exit 2，并指向 `trellis-finish-work`。
- `--from-finish-work`、`--recovery-after-finish-work` 均由真实 parser 拒绝；测试不存在隐藏 Namespace 字段。
- closeout：`75/75`；canonical full：`383/383`；preset：`36/36`。
- `format-merge-commit` 生成 ready merge payload，包含中文 subject/body、`PR #105`、`Refs #105`。
- Python compile、Bash syntax、`git diff --check` 通过。
- canonical/dogfood Python、workflow、config 一致；overlay drift 为 0；无 `.new/.bak`。
- public marketplace sample + 当前分支 local preset 的 throwaway initial #105、update/reapply #106 均通过 draft/archive/ready、fresh binding、mixed-case URL、hook/symlink preflight、clean tree和三方 HEAD。

## 生命周期与范围

- 新 Phase 2 记录 HEAD `963c3f3` 和 16 个 dirty paths；路径集合与 cleanup commit 精确一致。
- `validate_phase2_check(..., allow_committed_head=True)` 对当前 HEAD 返回零错误；当前 non-metadata dirty paths 为 0。
- 18/18 commit message 合规；Round 1-29 raw report path/digest/size 全部匹配 assignment。
- 旧 Round 29 gate 对当前 HEAD 已正确 stale，不能复用。
- close：`[105]`；related：`[53,96,97,100]`；follow-up：`[98,99,101]`。
- 未发现通用 resolver、通用 symlink、remote transport framework、schema、索引或时间框架新增扩张。

## 安全与部署

未发现 secret、token、credential、签名 URL 或客户数据泄漏。没有 CI/CD、Docker/Compose、K8s/Kustomize、Helm、database migration 或 Makefile 变化，无服务部署或配置迁移影响。

## 观察项

- `v0.6.5-guru.3` 本地和远端 tag 均不存在，默认 stable-tag throwaway 按预期无法安装。
- current branch 远端不存在，当前分支 remote marketplace 与真实 GitHub E2E 尚未验证，必须由 publish-time fail-closed verifier 承接。
- public marketplace sample 验证不等于当前分支 remote marketplace 验证。

## 后续候选

无新增 scope follow-up；本 P1 属于当前 #105 的 Docs SSOT 收敛。

## 结论

- P0：`0`
- P1：`1`
- P2：`0`
- P3：`0`
- findings_count：`1`
- 最终结论：`FAIL，Branch Review Gate 阻塞`
