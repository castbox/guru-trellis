# #377 对齐 guru-clarify-requirements 公开 invocation 合同

## 1. 目标

修复 `guru-clarify-requirements` 的 public invocation 断链：调用方按公开
invocation schema 提交合法 envelope 时，runtime 不应再要求 schema 未声明的
`typed_output` 字段，标准 Intake 必须能够从 Discovery 的 `context_ready`
继续到 Clarification 的 `clear`，并将结果交给下游 wording consumer。

## 2. 当前问题

- `semantic-owner.schema.json` 使用 `additionalProperties=false`，没有声明
  `typed_output`。
- `runtime/invoke.py` 却无条件读取 `envelope.typed_output` 并在缺失时失败。
- 现有正向测试直接手填 `typed_output`，没有验证完整 envelope 与公开 schema
  的一致性，因此掩盖了断链。

## 3. 验收标准

1. 明确唯一 public invocation 合同，并使 Skill、interface、schema、runtime、
   eval 与生成安装副本一致。
2. 正常调用方只提交声明的 producer output、transition、owner context/result；
   不手填未声明字段，也不读取上游私有结果。
3. 真实 public wrapper 回归覆盖 `context_ready -> clear -> wording`。
4. 测试验证 envelope 先通过声明 schema，再验证实际 typed exit 与下游 DTO。
5. 覆盖 current、stale target、错误出口和声明外字段；保留 live target、
   duplicate snapshot、语义结果及出口一致性校验。
6. canonical、installed、Shared/Codex/Claude/Cursor 投影一致，且现有 package
   contract suite 继续通过。

## 4. 非目标

- 不新增 Skill、phase、route、wrapper、adapter、dual-read/dual-write 或 legacy
  fallback。
- 不修改 upstream Trellis、业务仓库、Issue 内容或现有语义门禁。
- 不执行完整多平台 Release/upgrade 矩阵；只做本 Issue 所需的代表性 clean
  throwaway 与定向安装/drift 验证。

## 5. Issue 范围

Primary/close issue：`castbox/guru-trellis#377`。

