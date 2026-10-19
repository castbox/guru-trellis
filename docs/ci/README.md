# 三系统定向 CI

[Targeted native CI](../../.github/workflows/targeted-ci.yml) 在原生 Ubuntu 24.04、macOS 15、Windows 2025 上分别运行。PR 与 main push 在 `trellis/**`、`ci/**`、workflow、依赖、`.gitattributes` 或本说明变化时触发。PR 的 candidate 是真实 head SHA；driver 是 Actions checkout 的 SHA，两者单独记录。

每个目标先安装自身 hash-locked Python 依赖，运行自身 unittest，再独立构建自身 source lock 选定的 Trellis Fork，尝试 clean Codex CLI init 和本地目标 preset。Fork 使用其 `package.json` 中的 pnpm 版本及 frozen lock；核对 commit、tree、parents 和实际 CLI 版本。不使用全局 Trellis 或历史 tarball。Windows 使用原生 Python 和 Git for Windows Bash。驱动不调整目标换行或解释器 alias；专项编码子进程显式使用 `PYTHONUTF8=0`，并记录实际默认编码。

## 手动对照与定向选择

workflow 进入默认分支后可运行：

```bash
gh workflow run targeted-ci.yml --repo castbox/guru-trellis \
  -f baseline_ref=71f432f22acc78df7194a818c27b8e467ceb3048 \
  -f candidate_ref=<已发布的完整候选SHA> \
  -f tests=test_guru_platform_inventory.py
```

两个 ref 必须可由同仓库 Git fetch 解析。空 candidate 使用当前 run SHA，空 baseline 只运行 candidate。`tests` 接受文件路径、unittest ID，以及 `文件.py::类.方法`。文件路径和模块选择保持原语义；裸文件名相对于目标的 `trellis/presets/guru-team/scripts/python/`。以下选择只执行指定包级用例，不执行同文件的其他测试：

```text
trellis/skills/guru-team/packages/guru-sync-base/tests/test_contract.py::BaseSyncPackageContractTests.test_porcelain_z_parser_keeps_registered_worktree_records_separate
```

CLI 调用包含空格的路径时，将完整的 `文件.py::类.方法` 作为一个 argv 传递。断言来自目标 checkout；旧目标没有文件或用例时保持失败，不复制候选产品实现。导入错误、缺少用例和零用例不能算缺陷命中或通过。

如需验证具体缺陷，同时传 `expected_test` 和 `expected_message`。两者分别精确匹配 unittest failure ID 与 assertion message。ImportError、unittest error、依赖失败和无关 assertion 不算命中。仅当基线的失败全部命中、其余阶段正常且 candidate 全部通过时，报告对照成立。未指定、未命中或两目标相同结果均如实报告。skip、expected failure、零用例不能算完整通过。

## 报告与定位

Actions job summary 显示两个目标的 SHA、阶段及状态。`targeted-<OS>-<run>-<attempt>` artifact 保存14天，仅含明确的诊断：`report.json`、`summary.md`、各阶段命令/原始退出码/日志和 unittest outcome。报告记录镜像、Python/Git/Bash/Node/pnpm、实际依赖、locale、UTF-8 模式以及 Git 换行配置。它不收集完整环境变量、凭据、`.git` 或目标工作树。

每个目标的 `runtime-diagnostic.json` 单独记录 bootstrap capability fixture 的实际调用。诊断驱动来自本次 driver，`bootstrap_check`、runtime 资产和依赖环境来自被测目标。它只观察 manifest 已声明的公开 wrapper 用例，保留原 argv、输入、编码、返回码和输出；不替换产品代码或修改 active pointer。报告用于定位正常安装的底层失败，不是产品修复通过证明。

原 fixture 遇到首个失败时会停止。诊断器在原临时视图仍存在时，另行执行尚未运行的 manifest 用例，并标记 `supplemental=true`。补充调用沿用原 wrapper、工作目录和环境；原首个失败及 fixture 异常继续保留，不能将补充调用当作原 fixture 已继续或已通过。

旧目标的裸 Bash、内联 JSON 与新目标的绝对 Bash、stdin JSON 均按目标自身实现执行。新 transport 的补充调用使用该目标的 `wrapper_call`，不会借用候选实现修补基线。

`native-compatibility.json` 保存独立 driver 对所选目标的真实 Git/root/worktree、中文空格 URI/相对 schema、bootstrap wrapper 和 TaskCommit 中文消息/hook/索引结果。driver 从本次 checkout 读取测试 fixture，通过 `GURU_NATIVE_TARGET_ROOT` 导入各自目标产品。旧目标不需要包含新测试文件；依赖或 import 错误继续为执行失败。Windows 默认代码页与 `PYTHONUTF8=0` 的实际条件单独核对，不能用 UTF-8 默认环境替代。

`native-eol.json` 使用刚完成 clean CLI init 的实际 upstream scripts/version，另建真实安装 fixture，经正常 commit 及 `core.autocrlf=true/false` clone，检查受管 LF、raw installed validation 和 reapply。它不手工生成 manifest，也不替代前序 clean CLI 安装证据。旧目标的换行漂移必须由具体 raw 字节/validator 结果确认，不能把缺少新 helper 的 import 错误算作复现。

clean 安装后，原 driver 继续以独立进程执行 `update --dry-run/--skip-all`、同 provider 的 workflow `--create-new/--force`、`maintain tools_install` 的 prepare/preview/apply，以及原 `recovery_ref` 的 recover/resume。随后重新应用目标 Guru preset、执行 installed validation 并检查 sidecar。Windows 上游命令串使用 `py -3`；Guru `--python` 仍只接收单个 executable 路径。维护链路失败保留其原阶段和非零结果，不算完成。

`installed-wrapper.json` 和 `maintenance-installed-wrapper.json` 分别记录初装后及维护后在实际目标上执行的两项 manifest wrapper case。调用读取目标已有 active pointer；不会创建替代 pointer 或退回 CI Python。维护后还按生成的 Codex hook 命令执行非敏感 fixture，以验证原生解释器/argv 可执行。该 hook 结果只证明脚本入口，不证明实际 Agent 会话。

诊断收集完成和 fixture 产品失败是不同结果。collector 的启动、依赖或执行缺口保持为环境/执行失败；fixture 的返回码与异常保留为产品观察。测试或诊断失败后仍尝试原 clean 安装。原安装失败继续保留非零，不因取得诊断而变成通过；`expected_test/expected_message` 的精确 unittest 匹配规则保持。

```bash
gh run list --repo castbox/guru-trellis --workflow targeted-ci.yml
gh run view <run-id> --repo castbox/guru-trellis
gh run download <run-id> --repo castbox/guru-trellis --dir <诊断目录>
gh run rerun <run-id> --repo castbox/guru-trellis
```

先查看失败阶段的原始日志。checkout、Python 依赖、Fork 下载/构建或命令启动错误属于环境/执行问题；产品测试 assertion 与安装入口失败保留原结果，由维护者依据具体日志归因。安装失败不会自动被称为 #630。测试失败仍尝试安装，基线失败仍运行候选，一个系统失败不取消另两个系统。候选或基础设施失败保持非零。取消、未执行、缺少报告或上传失败均未完成，不能声明通过。

## 证据边界

本地驱动集成测试只证明目标隔离、结果收集和失败继续。真实 PR、main push、dispatch 的三系统 run 及自然失败 artifact 需要在 Actions 实际取得；合并前不能声称 main/dispatch 已验证。运行记录由维护者在对应 Issue/PR 引用实际 run 链接，不在此放占位成功记录。

本次代表性 clean Codex 安装不证明 Agent 自动加载或全部平台/历史版本的 Release Gate。[#630](https://github.com/castbox/guru-trellis/issues/630) 的三系统验收聚焦命令行 Python runtime、目录相关脚本和实际公开 wrapper。macOS、Linux、Windows 均不要求真实 Codex 或其他 Agent 会话，也不要求 OpenAI 账号、模型推理或 GPU。已有成功脚本证据可在适用性核对后采用，无需为补充 Agent 证据重跑。

维护者可通过 dispatch 的 `windows_codex_session=true` 显式启用额外的 Windows Codex 会话诊断，复用 candidate 的实际安装及原 artifact。正常 PR 不执行此诊断；安装不成功时诊断保持失败。该入口不承担 #630 必需验收，已有会话失败不阻塞该 Task 完成。如需判断诊断中的实际自动加载、Skill 调用、hooks 启用和环境结果，仍须逐项核对原始事件，不能由静态配置、直接 hook 或 wrapper 代替。

该会话使用官方 Codex CLI 0.163.0、Ollama 0.40.6 和本地 `qwen3.5:9b`，不需要 OpenAI 账号或 API 凭据。独立 `CODEX_HOME` 不复制维护者登录状态。模型须在当前 Agent 中实际读取所选 Skill 及完整合同，完成语义判断并调用公开 wrapper；Skill 名不是 Agent 类型。模型执行总预算为 600 秒，依赖安装和模型下载另计。超时会终止 Windows 子进程树，并保留原始会话、rollout、命令与失败状态。CLI 正常退出也只表示执行结束，仍由 Task owner 核对实际加载与调用证据。

模型通过官方 `ollama pull qwen3.5:9b --runner llamacpp` 下载到隔离缓存。采集器以 `FROM qwen3.5:9b` 和 `PARAMETER num_ctx 65536` 创建临时 `guru630-windows-validation:latest`，供 Codex 实际推理。Modelfile 不覆盖温度或 presence_penalty，不添加 system prompt 或语义答案。Codex 两轮均使用 `model_context_window=65536`、`tool_output_token_limit=32768` 和 `model_reasoning_effort=none`。每轮真实 argv 保存在报告中。`session.Modelfile` 保存实际创建输入；`report.json` 记录源 tag、会话 tag、真实 show 的格式/runner/参数及结束前 `/api/ps` 的加载上下文。配置和本地预检不能证明真实 Windows 会话成功。

启动前，采集器在临时安装目录写入真实请求草稿 `.guru-validation-request.md`，artifact 中的 `request-draft.md` 保存同一输入。草稿只提出候选问题，不提供语义决策。若安装目录没有 HEAD，采集器通过命令局部 Git 身份创建空初始提交，不消费已暂存文件，也不创建活动 Task。准备命令及退出码进入原报告；准备失败时停止会话。

固定两轮程序先通过 `codex exec` 加载 startup、完整合同和实际路径观察，再以初轮真实 `thread.started` 身份执行 `codex exec resume`，由模型独立判断、实际调用 wrapper 并自审一致性。两轮共用同一截止时间，第二轮只使用剩余预算。脚本不解析语义结果或判断其是否充分。Windows 保留默认 PowerShell，提示使用其原生语法及绝对 Git Bash 路径，不依赖 `shell` 参数重新发现的裸 Bash。两轮提示、events、stderr 和真实退出码均保留，由 Task owner 核对。

完整读取按单文件请求输出预算 32768；出现截断时按行分块补读缺失内容。首轮报告实际观察及真实程序错误，不称为资格通过。末轮独立判断并通过 stdin 实际调用 wrapper，再按完整 Skill 定义自审真实结果的一致性。发现错误时由模型自行修正并重新调用；最终报告实际退出码、stdout 和证据限制。

解释器可见性、非 UTF-8、LF/CRLF、路径脚本及公开 wrapper 的证据由 [#630](https://github.com/castbox/guru-trellis/issues/630) 承接；实际 Agent 会话只作额外诊断。上游 [Trellis#53](https://github.com/castbox/Trellis/issues/53) 的结果只证明其前置修复。控制解释器可见性须使用真实解释器/launcher 并验证子进程解析，不能用 runner 其他 Python 掩盖条件。
