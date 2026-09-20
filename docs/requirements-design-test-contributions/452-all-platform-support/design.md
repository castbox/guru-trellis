# #452 All Platform Support Design contribution

状态：`reviewed_promoted`。采用 `target_native`，已提升到
`current-main-0.6.17-guru.58`；关联的 Architecture contribution
`architecture-contribution-452-all-platform-projection-v1` 保持 `reviewed_candidate`，
Architecture shared current 仍为 `.57/active`。以下设计尚待实现与验证。

- `D452-01`：preset 保存一个 pinned `upstream_platforms` inventory，记录 source identity、inventory identity/digest，以及每个平台的 canonical `AITool` id、唯一 public `cliFlag`、template/root、native destination、entry form 和 projection descriptor。inventory 当前完整 cardinality 为 22，解析器不从文件夹存在性推导平台能力。
- `D452-02`：目标仓库 manifest/provenance 保存以 registry `cliFlag` 表示的排序、去重、非空 `selected_platforms`；每个值必须唯一映射回一个 `AITool` id。install、skill package、platform projection 与 ownership records 必须指向同一 exact selection；任何 section 缺失或不一致均 fail closed。
- `D452-03`：installer 只公开 repeated `--platform <cli-flag>`。显式 repeated flags 形成 exact subset，无 flag 才选择 `default_platforms=[claude,codex,cursor]`；parser 不声明 `--all-platforms`，manifest 与 JSON output 不记录 `all_platforms` 状态。
- `D452-04`：selection resolver 在所有文件 mutation 前完成 inventory binding、unknown/duplicate/empty 检查、projection descriptor 完整性检查与模式选择。参数冲突、inventory drift 或 projection 缺失返回确定性错误，并保持目标仓库零写入。
- `D452-05`：upgrade resolver 只从目标仓库 current installed manifest/provenance 读取 selection，验证各 manifest section 一致后，将 exact ordered set 投影为重复 `--platform` 参数。它不读取 source checkout dogfood 文件来替代目标 selection，也不把默认集合或完整 inventory 当作升级 fallback。
- `D452-06`：`guru-trellis` dogfood apply/reapply 显式传入 Claude、Codex、Cursor；drift checker 从 dogfood manifest 读取同一 selected set，只检查 shared assets 与这三个平台的 installed projection，同时独立验证 canonical inventory/ownership 的全平台完整性。
- `D452-07`：OpenCode descriptor 声明 `.opencode` native discovery、command/skill destination 与 actual-load adapter。OpenCode 与其它 21 个平台共享 inventory/selection/ownership 合同，但各平台按自身 native surface 投影，不要求同构目录或相同 overlay cardinality。
- `D452-08`：ownership inventory 由 shared managed paths、完整 canonical platform descriptors 和 target-selected installed paths分层计算。reapply/update 复用 previous managed hash、`.new`/`.bak` 与 removal provenance；unknown local edits 保留并报告冲突，不静默覆盖。
- `D452-09`：public package projection 排除 package-private `tests/`，并校验 canonical、installed 与各 selected native surface 的 bytes、mode、manifest mapping 和 managed ownership。任一显式选择平台缺失 required projection 时安装失败，不允许 deferred success。
- `D452-10`：验证分层为 inventory/argument unit tests、exact-selection upgrade fixtures、canonical/installed/platform parity、ownership/reapply/update/drift、代表性 clean throwaway，以及 OpenCode representative native actual-load。production workflow 继续保持 #434 未激活；release/tag 与外部生产验证保留为未验证边界。

实施还必须遵守 touched non-generated code file 的 3000 行上限。当前接近阈值的 installer、compatibility matrix 与 installer test 主文件在增加 #452 行为前先做机械拆分或小型解耦，拆分本身保持行为等价并由现有测试覆盖。

设计只定义可实现机制，不把文件存在、静态内容相等或脚本返回值替代为 native actual-load、
Architecture/RDT semantic review 或正式 Release Gate。
