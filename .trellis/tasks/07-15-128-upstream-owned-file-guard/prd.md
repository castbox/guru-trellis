# #128 建立 Trellis upstream ownership 清单与禁止新增覆盖门禁

## 目标

在删除 legacy preset overlay 之前，建立一套机器可验证的 ownership 冻结合同。该合同必须完整登记当前 43 个 overlay，阻止新增 upstream-owned patch、legacy 集合扩张、既有 payload 漂移和缺失迁移责任人，同时保持现有运行时调用语义不变。

## 来源与已确认事实

- 主需求来源是 [GitHub issue #128](https://github.com/castbox/guru-trellis/issues/128)，该 issue 是 umbrella issue #127 的首个 architecture prerequisite。
- 官方 Trellis 文档把 `.trellis/workflow.md` 定义为 phase、skill routing 和 workflow-state 的 Markdown 控制面；hook/script 不拥有 AI 流程判断。
- 官方 Trellis `0.6.5` 使用 `.trellis/.template-hashes.json` 管理 generated file 的 update 冲突，并提供 overwrite、keep、`.new` 三类处理路径。
- 在 clean 临时仓库执行 `trellis init -y -u ownership-audit --claude --codex --cursor` 后，43 个 overlay 路径中有 37 个由当前 Trellis `0.6.5` 生成；6 个 `.codex/prompts/trellis-*` 与 `.codex/skills/trellis-*` 路径属于旧 Codex entry namespace，当前初装不再生成。
- 当前 installer 通过 `looks_like_trellis_generated_entry()` 识别 upstream entry，并由 `copy_overlay()` 替换已识别文件；未知本地改动写入 `.new`。
- 当前 dogfood drift check 只校验 overlay canonical 文件与同路径 dogfood copy 的字节一致性，尚未校验 ownership、迁移责任或冻结集合。
- `trellis/guru-team-extension.json.public_api.managed_paths` 同时声明 Guru namespace 与 legacy upstream namespace，必须纳入同一 ownership 分类检查。

## 需求

### R1 Durable ownership 合同

- 新增项目级 durable spec，定义 `upstream_owned`、`guru_owned`、`transitional_legacy`、`unclassified` 四个互斥类别。
- `unclassified` 必须导致 validator 非零退出。
- Durable spec 必须明确 Markdown/Skill 承担语义判断，validator 只处理结构化事实。

### R2 Machine-readable inventory 与 schema

- 新增严格 JSON schema 与 machine-readable inventory。
- Inventory 必须固定 Trellis CLI 基线 `0.6.5`、43 条 frozen legacy path、每条 base payload SHA-256 和 clean-init 生成状态。
- 每条 frozen legacy 记录必须包含 path、category、migration state、upstream producer、当前 Guru 行为、replacement owner、blocking issue、removal issue、update/upgrade 冲突语义、dogfood 状态、target business repo 状态。
- 当前 43 条记录必须全部为 `transitional_legacy` 且 migration state 为 `active`。
- 后续删除迁移必须保留 frozen path 审计记录，并把 path 转为 `upstream_owned` 与 migration state `removed`；不得通过删除审计记录隐藏历史。

### R3 No-new-upstream-patch validator

- 新增 source maintainer validator 与 Bash 入口，支持 `--repo` 和 `--json`。
- Validator 必须在任何 preset mutation 前执行。
- Validator 必须校验 schema、固定 key 集合、类别互斥、path 唯一性、43 条 frozen baseline、overlay 路径集合、active payload hash、replacement/removal 字段、extension manifest managed path 分类和 Guru namespace 规则。
- 新增 overlay、替换 frozen path、扩张 frozen 集合、修改 active payload、缺失 replacement owner、缺失 blocking/removal issue、出现 `unclassified`、新增 upstream-owned managed claim 时必须非零退出。
- `.trellis/guru-team/**`、`trellis/skills/guru-team/**`、active `guru-*` package 与声明平台的 `guru-*` discovery path 必须通过分类。
- Validator 不得判断 patch 的产品价值、语义设计质量、finding severity 或是否授权 scope expansion。

### R4 Gate 接入

- Preset apply 的 Python 主入口必须在创建目录、复制文件、写 manifest 之前执行 validator。
- `check-dogfood-overlay-drift.sh` 必须先执行 ownership validator，再比较 canonical/dogfood payload。
- `verify-throwaway-install.sh` 必须在 initial apply、`trellis update` 后、workflow/preset reapply 阶段留下 ownership gate 成功证据。
- Gate 不得进入 `.trellis/workflow.md`、用户 task runtime、既有 Skill 正向行为或 platform entry 调用链。

### R5 Positive/negative fixtures 与回归

- 新增结构化 fixture，覆盖 current baseline、Guru-owned managed path、Guru-owned discovery path、新 upstream overlay、legacy 集合扩张、payload 漂移、缺失 removal owner、`unclassified`。
- 单元测试必须证明 positive fixture 通过、negative fixture 非零失败且错误字段稳定。
- 现有 preset installer、skill package、dogfood drift 和 throwaway 验证必须继续通过。

### R6 文档与 public authoring contract

- 更新 `.trellis/spec/preset/**`、根 README、preset README、workflow authoring README。
- 文档必须说明 upstream update/upgrade ownership、legacy freeze、Guru namespace、validator 命令、迁移责任和 `.new`/`.bak` 边界。
- 文档不得把 active task、workspace journal 或业务私有规则写入 marketplace/spec template。

### R7 现有调用非回归

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 相对 base commit 必须无 diff。
- 43 个 overlay 的 path 与 payload 相对 base commit 必须无 diff。
- `guru-sync-base`、`guru-create-task-commit` 的 package、interface、runtime command、schema、typed exits 与 discovery copy 必须无行为变化。
- Trellis upstream `trellis-*` Skill、Agent、Command、Prompt、Hook、runtime agent 的 trigger、frontmatter、prompt、dispatch 与 invocation 语义必须无变化。
- 本 issue 不新增 mandatory Skill invocation。

## 非目标

- 不删除现有 overlay。
- 不修改现有 overlay payload。
- 不修改 canonical 或 dogfood workflow。
- 不实现 #129、#130、#131 的 closed-loop Skill。
- 不执行 #132 的 legacy cleanup 或 runtime routing integration。
- 不修改 Trellis upstream 源码、全局 npm 包或 `node_modules`。
- 不改变 #110、#98、#115 的业务行为。
- 不把 AI ownership 语义判断写进 Python 或 shell。

## 验收标准

- [ ] AC1：Inventory 恰好保留 43 条 frozen legacy 记录；当前 43 个 overlay 全部处于 `transitional_legacy/active`，无 `unclassified`。
- [ ] AC2：新增 upstream overlay、替换 frozen path、扩张 frozen 集合、修改 payload、缺失迁移责任字段时 validator 非零退出。
- [ ] AC3：`.trellis/guru-team/**`、canonical/installed `guru-*` package 与平台 `guru-*` discovery fixture 通过。
- [ ] AC4：initial apply、`trellis update` 后检查、preset reapply、dogfood drift 均执行 ownership gate，并在失败时阻止后续阶段。
- [ ] AC5：两个 workflow 文件、43 个 overlay path/payload、两个现有 public Skill package 及 upstream discovery smoke contract 相对 base commit保持不变。
- [ ] AC6：durable spec、根 README、preset README、workflow README 形成一致的 upstream update/upgrade ownership 说明。
- [ ] AC7：validator 输出只包含 path、hash、category、owner、prerequisite、manifest 与 schema 事实，不输出语义 pass 或 route 判断。
- [ ] AC8：Issue Scope Ledger 只把 #128 放入 `close_issues`；#127 保持关联，#129、#130、#131、#132 保持后续迁移范围。

## 阻塞问题

无。Issue #128 已给出边界、迁移顺序、非回归合同与关闭范围；仓库和官方文档已回答实现位置与 update/upgrade 事实。
