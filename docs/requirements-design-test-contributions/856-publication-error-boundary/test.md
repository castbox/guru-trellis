# #856 test 拟写

状态：integrated_pending_review。完整拟写见 `proposed/docs/test/current/task-delivery-lifecycle.md`，其相对引用按最终 current 位置解析。适用前驱：Git `4f3d9069e0720ec94e39d1079154d2f7a7058935` 的 `docs/test/current/task-delivery-lifecycle.md`。

差额是末尾 T856 小节；原完整单元和未替代条件保持。原 owner 已将完整拟写整合至 current 并读回；尚未发生独立 committed Review。

## 本轮工程观察

观察对象是本 Task 的未提交 canonical Publish package after；事实由本批 implementation owner 的实际命令结果承接。最终 package 全套通过本 checkout managed resolver 执行，采用已核对 Fork e3793251fad8bd261d0c370d408c7675b9f6a140 的 public common：56 tests，97.924s，exit 0，无 skip。shared test_io 为13 tests、test_command_receipts 为3 tests，均通过。source package validator 为43 packages／126 commands，通过；Python语法、bash -n 和 git diff --check 通过。原公共 wrapper、直接入口、unknown70／known4安全输出、migration分类、内部 reprepare 及原 stateful 同事务恢复均在本轮集合内。

首次 wrapper 运行有两项产品断言失败及一项空调用日志 fixture 错误，后续修正。首次全套缺 public common 路径跳过23项；最终已实际全部执行。test_command_receipts 首次在resolver前置返回exit 2，未进入测试；相同命令顺序重试通过，未修改runtime。上述首失败不改写为首次通过。

RDT 首次整合观察时尚未执行 tools 写入，当时的 installed/native、drift、sidecar/mode 未验证边界保留为该观察截止。后续原 tools owner 已完成同一冻结操作的成套重装，实际出口 tools_upgraded，installed_version 为 0.7.0-guru.9，仍明确 unverified=[formal_fork_source_lock]。未另行发起独立 reapply operation。

目标 installed validator 通过：43 active packages、126 commands，conflict/sidecar/removal 均为0。目标自身 managed resolver 执行 native get_context 成功；本人 Task/gen/D1、accepted scope、Planning accepted/applicable和implementing phase保持。installed Publish wrapper 三例分别返回缺readiness的schema_mismatch/input.readiness_result_id/2、closing_keyword_forbidden/input.pr_body/3、invalid_json/input/2，stderr均空。dogfood drift通过，实际claude/codex/cursor、workflow/spec匹配。

实际10105项source projections除原用户config外，内容和installer预期mode匹配。invoke-stage0-skill.sh 的source644→installed755符合原ensure_companion_modes合同及既有Git mode，未为此更改源码或断言。212项public actions前后bytes/mode一致；581项peer/common pointer文件独立比对保持，246项peer runtime观察由原executor核同。无.new/.bak，Guru用户配置保留；原操作phase complete且无failure，Task/session不在工具写集。实际工具差额是12项产品投影及原installer生成的extension manifest。

正式source_locked采用、真实GitHub写入、历史G10／旧Draft重放、生产验证、完整Release矩阵、TaskCommit和独立committed Review仍未执行。本次工程与安装事实不等于Check、readiness、Publication或Task Completion通过。
