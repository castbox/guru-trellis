# 三系统定向 CI

[Targeted native CI](../../.github/workflows/targeted-ci.yml) 在原生 Ubuntu 24.04、macOS 15、Windows 2025 上分别运行。PR 与 main push 在 `trellis/**`、`ci/**`、workflow、依赖、`.gitattributes` 或本说明变化时触发。PR 的 candidate 是真实 head SHA；driver 是 Actions checkout 的 SHA，两者单独记录。

每个目标先安装自身 hash-locked Python 依赖，运行自身 unittest，再独立构建自身 source lock 选定的 Trellis Fork，尝试 clean Codex CLI init 和本地目标 preset。Fork 使用其 `package.json` 中的 pnpm 版本及 frozen lock；不使用全局 Trellis 或历史 tarball。Windows 使用原生 Python 和 Git for Windows Bash。驱动不调整目标换行、系统编码或解释器 alias。

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

本次代表性 clean Codex 安装不证明 Agent 自动加载或全部平台/历史版本的 Release Gate。Windows 解释器可见性、非 UTF-8 和真实 Agent 专属回归继续由 [#630](https://github.com/castbox/guru-trellis/issues/630) 与 [Trellis#53](https://github.com/castbox/Trellis/issues/53) 承接。未来控制解释器可见性的用例须使用真实解释器/launcher 并验证子进程解析，不能用 runner 其他 Python 掩盖条件；编码用例不能被默认 UTF-8 掩盖。
