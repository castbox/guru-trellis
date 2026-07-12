# Issue #105 Round 31 问题闭环审查报告

## 审查身份

- technical agent：`/root/final_release_review_105_round30_cleanup`
- 逻辑角色：问题闭环审查代理
- reuse_decision：`reuse-for-closure`
- reviewed_head：`1f177cd4a0542191ab645b3107a1502851493a29`
- base：`origin/main@3dec302206783fe4ac1296066e9a1789c995d58b`
- 边界：仅闭环 Round 30 唯一 P1；全程只读，未修改文件，未运行 recorder/review gate，未 commit、push、PR、archive 或关闭 issue。

## Round 30 P1 闭环状态

原 P1 的文档正文已关闭：

- `prd.md` 已明确 `publish-pr` 仅为兼容性阻断入口，publish/recovery 只由 `trellis-finish-work` 执行。
- `README.md`、`workflow-contract.md`、`companion-scripts.md` 均规定当前 task-local `pr-body.md` 是唯一 body 来源，并明确拒绝 `--body-artifact`、generated fallback 与 readiness-relative `body_file`。
- 四处现存 legacy token 均处于明确拒绝语义，不再存在旧授权正文。

## 新 Finding

### P2：文本合同检测器按整段 rejection 短路，混合授权回归仍可漏检

`legacy_body_source_violations` 先按有限标点拆分 clause，再在 clause 内遇到任意 rejection token 时跳过整个 clause，没有判断 rejection 是否修饰同一个 legacy source。现有两个混合授权反例恰好被 `, but` 和中文分号拆开，不能证明其他标点组合。

只读变体探针均错误返回 `[]`：

```text
Formal closeout accepts --body-artifact and rejects generated body.
Formal closeout 支持 --body-artifact，同时拒绝 generated body。
Formal closeout 支持 --body-artifact。Generated body 不可用于 closeout。
```

影响：当前文档正文和 runtime 安全，但后续文档可以在测试仍通过时重新授权 `--body-artifact`，形成测试门禁假绿。

修复要求：

- rejection 必须与同一个 legacy source 局部绑定，不能由 clause 内任意拒绝词短路全部授权。
- 覆盖英文 `and`、中文“同时”、中文句号无空格三类反例。
- 优先改成每份文档的确定性 canonical contract 断言，删除自然语言 matcher，不扩展通用 NLP parser。
- 修复后由本 technical identity 继续 closure，不得直接进入 fresh final review。

## Phase 2 与提交证据

- commit `1f177cd` 精确修改 4 个 non-metadata paths：README、两份 durable spec 和 canonical test。
- 4 个路径与 Phase 2 `dirty_paths` 中 non-metadata 集合一致；`allow_committed_head=True` postcommit 校验无错误。
- commit history `19/19` 通过；现有合同 class `5/5` 通过，但不能覆盖本轮新反例。
- closeout `75/75`、canonical `386/386`、preset `36/36` 通过。
- runtime、installer、workflow overlay 与 installed smoke driver bytes 未变，Round 30 initial #105/update #106 evidence 仍 fresh。

## Docs SSOT、Scope、安全与部署

Docs SSOT 正文已对齐，但测试保护不完整。Scope 保持 close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`。未修改 production runtime、schema、workflow、overlay、installer 或 smoke driver，未新增 resolver、symlink、transport、索引或时间框架。未发现敏感信息；无 CI/CD、容器、K8s、Helm、migration 或 Makefile 影响。

## 结论

- Round 30 原 P1 文档正文：`closed`
- P0：`0`
- P1：`0`
- P2：`1`
- P3：`0`
- findings_count：`1`
- closure_status：`fail`
- 最终结论：`Round 31 问题闭环被新 P2 测试合同缺口阻塞`
