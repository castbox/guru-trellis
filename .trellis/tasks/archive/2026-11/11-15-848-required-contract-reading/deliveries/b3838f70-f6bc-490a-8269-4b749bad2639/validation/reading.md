# D1 实际验证观察

## V1 / V3：同形 transport 与跨调用补显

输入固定为 Git `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa` 中的四份公开原文：`clear-technical-writing.md`，以及 `guru-review-change` 的 `references/contract.md`、`references/review-method.md`、`interface.json`。按规划分为写作规范一组、其余三份一组。

真实 `functions.exec` 首行请求外层24,000，每条 `exec_command` 请求内层20,000，输出 `.output`。两份内层结果均退出0，无内层截断；工具估算分别为8,548和10,599 token，合计19,147。合并的模型可见返回仍在中间显示缺失7,159 token。**原合并显示未通过完整性观察**；未据请求参数推断宿主有效容量或限制原因。

原调用先将两份完整结果保留在平台既有 store。下一独立 `functions.exec` 只从第一次的原 store 取出10,599 token那组并显示，没有执行新的读取命令；该组从 contract 首行至 interface 最后括号完整可见。写作规范组在初返回已完整显示，包含 E13 文件尾。此次补显完成了四份原材料的完整获得，不能表述为合并场景一次显示成功。消费后已释放两份原结果的 store 引用。

## V2：内层缺失与连续范围回退

固定同一历史 `references/contract.md`，原量4,781 token、303行。真实内层请求2,000、外层4,000时，内层返回保留了缺失2,781 token的截断标记。随后将同一原内层返回在外层24,000的独立调用中显示，缺失标记及缺失量保持；增加外层不能恢复内层已遗漏文字。

实际重新读取该 Git 原文的连续范围1—150和151—303，覆盖从文件首行至最后一句及末尾换行，两段均完整显示。没有更换短材料或增加任意长度压力矩阵。内层受限原结果的 store 引用在观察后已释放。

## V5 / V6：当前已执行的定向分发与源码检查

- 原 `test_clear_technical_writing.py -v` 使用 managed Python 和 `PlatformOverlayInstallerTest`，执行实际资产安装及 reapply。扩展后的测试在同一临时仓库解析22个 native entry payload，核对 AGENTS、workflow Phase Index/continuation/caller、source/installed 及声明平台独立 Review 入口的同源短节和先后顺序；核用户原始 CRLF 字节保留、reapply 幂等及零 `.new/.bak`。最终1个测试通过，用时92.754秒。原 fixture 替代 managed Python runtime 创建，资产 writer 和 installed package validation 实际执行；这不是 fresh CLI init、当前 checkout tools 采用或完整多平台矩阵证明。
- 首次尝试采用全局 Trellis 包时，fixture 缺 public Delivery 模块，在安装前失败。改用实际构建的 `@mindfoldhq/trellis@0.7.0-castbox.6` 的 `dist/templates/trellis/scripts` 后进入实际测试。
- 实际首轮分发测试暴露既有测试假设与当前合同不符：它假设所有 Skill 都用绝对写作规范引用，且所有平台都有 Codex 专用 orchestration 包。修正测试，使其接受原 provider-relative/installed 短名导航，并按 registry 声明的平台支持检查存在或缺席；没有修改这些 Skill 或 installer 的选择逻辑。首轮失败保留，后续成功来自完整重跑。
- `check-skill-packages.sh --root . --mode source --json` 返回 passed：43个 active packages、126 commands、2个 instruction-only packages。
- `check-upstream-ownership.sh --repo . --json` 返回 ok：22个 descriptors、22个 canonical overlays、三平台 dogfood selection，无错误。此结果不是当前 dogfood 已同步的证明。
- 按原 quality-guidelines 在内存编译400个 Guru Python 文件，含本次变更的 installer/test；全部通过。22个 overlay 中 JSON/TOML 用标准 parser 解析通过。`git diff --check` 通过。

## V5：本 checkout 实际采用

原 source-owned `guru-upgrade-tools` 完成唯一 prepare/invoke，实际返回 `tools_upgraded`、安装版本 `0.7.0-guru.9`、`unverified=[formal_fork_source_lock]`。使用当前 canonical 工作树和 CLI/Core `0.7.0-castbox.6` 的 local_candidate；未将其标为正式 source_locked 采用。

- 目标自己的 `resolve-python.sh` 返回可用 managed interpreter。
- installed `check-skill-packages.sh` 返回 passed：43个 active packages、126 commands，selected platforms 为 Claude/Codex/Cursor，package/overlay conflict、removal、sidecar 均为0。
- `check-dogfood-overlay-drift.sh` 返回 ok：workflow、三平台投影及 spec copies 与 canonical 匹配。
- 原生 `get_context.py --mode continuation` 成功提取新增短方法导航；public Delivery current 仍为同一 key、generation 0、implementing，accepted scope/Planning 结果保持。
- 逐一对照冻结 public plan 的212项 target，实际 bytes/mode 全匹配。AGENTS Guru 区块外字节、`.trellis/config.yaml`、Guru config、gitignore 和 gitattributes 保留；原 transaction 范围没有遗留 `.new/.bak`。
- 原 owner 完成807项 peer/pointer/runtime 观察的 preservation 校验，checkpoint 为 complete、无 failure。另行直接复核其中569个 common/peer pointer 文件的 bytes/mode（包括原缺失项仍缺失），全部一致；其余238项为原 peer 自身 runtime owner 的原生观察。未修改 peer tools 或 common runtime default。

以上是实际安装和目标检查；不是 V4 Agent 采用或正式 Check/Review 的替代。

## V4：无继承新 Agent 的实际入口采用

固定目标为未修改的 `trellis/presets/guru-team/scripts/python/guru_platform_inventory.py`。新 generic Agent 使用 `fork_turns=none`；启动请求仅给实际 installed `guru-review-change` 入口、该文件及只读范围。

已从该新 Agent 的本轮原生工具事件核对首次实际读取：先用 `rg` 定位 installed Reading Required Contracts In Full，再读 `companion-scripts.md` 第1—130行，覆盖短方法及少量相邻正文，没有先读整本文件。随后真实调用采用内层20,000、外层首行24,000，输出 `.output`，读取完整写作规范和实际 Skill；后续按其必需材料选择显式预算和分段。此次观察不是由初始请求注入读取顺序或参数得到。

首次回应将自己误作单视角 worker；澄清其最终独立 owner 职责后，它沿原入口执行 capture、三个不同独立视角、语义整合和最终 invoke，实际返回 `{"exit_id":"reviewed"}`。首读方法及首次长文预算行为在这次职责澄清前已发生。原首轮职责误解保留，不描述为所有步骤一次成功。

该独立只读审核报告未发现可行动问题，并说明其目标验证的实际层级和未验证边界。它证明本次 installed 原入口启动及读取采用；不是本 Task 的 formal Check、Branch Review、readiness 或 Completion，也不证明全部模型、平台或业务安装采用。没有因该样本修改目标文件或扩大本 Task 范围。

## 尚未完成的阶段

原 RDT owner 已完成 candidate_ready 与 final_integration，实际写入并完整读回三份 `docs/{requirements,design,test}/current/required-contract-reading.md`，公开返回 ssot_current。贡献状态为 integrated_pending_review，不代表独立质量通过；未修改共享 README/index 或全局版本。

官方 `task.py validate` 对本 Delivery 的两份8条 context manifest 均通过，同时报告长规范超过既有32,768-byte injection limit的告警。本轮按实际需要另行读取完整正文或完整适用小节，没有把截断注入当作已读，也没有修改 hook、注入器或全局容量设置。

TaskCommit、committed Check/独立完整 Review、readiness、Publication、Delivery merge、whole-Task Completion、Closure 和 Finish 尚未完成。`formal_fork_source_lock`、完整多平台升级/Release矩阵和宿主内部显示限制原因保持未验证边界。
