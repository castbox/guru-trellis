# 实施计划：#264

## 交付顺序

1. 读取官方 Trellis custom workflow/marketplace 文档，复核当前 registry/interface/installer 结构与现有同类 semantic Skill。
2. 建立 canonical `guru-maintain-architecture-baseline` package：SKILL.md、interface、profile schemas、errors、runtime dispatch、确定性 recorder/checker、tests/evals。
3. 将 package 注册到 `trellis/skills/guru-team/registry.json`、production-current inventory、discovery/validation fixtures，并生成/同步 Codex、Claude、Cursor 平台副本。
4. 在 workflow 中增加 Skill 的 mandatory marker、最小调用输入和唯一 typed-exit consumers；在 preset manifest/ownership/README 中加入安装资产。
5. 同步 dogfood 安装副本，定义架构 authority 的可复用模板/索引规则但不复制业务正文。
6. 运行 task check：Python/Bash/schema/contract/eval、现有 task index/history/Docs SSOT/base reconciliation/Planning/Phase 2/Branch Review/commit/publication/Finish 回归。
7. 运行 clean current-version install/update/reapply/workflow-switch/platform parity/drift/.new/.bak/executable-mode 验证，记录未覆盖边界。

## 受控文件分区

- `trellis/skills/guru-team/`：canonical package、registry、production inventory、runtime tests/evals。
- `trellis/workflows/guru-team/`：全局 mandatory invocation/consumer projection。
- `trellis/presets/guru-team/`：manifest、ownership、installer、README、平台 overlay。
- `.trellis/guru-team/`、`.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/`：安装/dogfood 副本，均由 canonical/apply.sh 同步。
- `.trellis/spec/`：仅写 baseline 摘要、索引、读取/更新规则，不复制架构正文。

## 风险与门禁

公共 skill id、schema、exit、consumer mapping 视为 API；所有改动需当前 HEAD 全 diff 的 semantic review。未通过 clean install/update/reapply 或出现 `.new/.bak`、模式漂移、平台不一致时 fail closed。不得提交、push、建 PR、merge、release，直到对应独立门禁与用户确认。
