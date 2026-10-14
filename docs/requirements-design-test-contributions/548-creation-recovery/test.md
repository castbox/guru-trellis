# #548 唯一验证与支持边界

状态：task-owned validation，2026-10-14 当前实现已执行下列定向验证；shared promotion及后续开发gates由原owners独立承接。

| Test / scenario | 可观察结果与层级 |
| --- | --- |
| T548-01 | 真正Guru Create → root Author/Clarify → D1 Creation/Author/Wording/Architecture/Approval/Activation，key/no-key两条，同Task/gen/单UUID；semantic fixture只证明transport |
| T548-02 | 同operation丢输出/recover、实际Author消费退休；规划、dirty/untracked、并行Task/session与Git resources保留 |
| T548-03 | current/no-current、不同合法route、stale gen/错误key、terminal和新session原owner行为；无session fallback |
| T548-04 | 真实官方0.6.17 old writer创建untracked Task；matching current public Plan2完整legacy/defer preview保留bytes/modes/refs，明确缺HEAD identity，不称恢复成功 |
| T548-05 | 一个成套installed样本保留真实当前Codex context，复用首次失败D1/pending，native current/continuation与正式Planning读回；fixture与当前host分层 |
| T548-06 | source/canonical包、受影响平台projection、preset reapply/drift/sidecar/mode；主完整legacy安装不半升级 |

固定当前CLI tar SHA256：5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916；Core：45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967，版本0.7.0-castbox.3。该matching local candidate不冒充正式source-lock或Release。

首次baseline：Create23、Author chain3、clean-installed1通过；真实Codex当前controlled创建/rebind到同Task。随后无context原D1正式Creation返回blocked/context_required，原Task/D1/pending保留。旧0.6.17探测中原Task1转换fixture不匹配，不能计通过；新增完整legacy/defer回归证明逐记录保留。

## 当前执行结果

| 入口 / 层级 | 实际结果 |
| --- | --- |
| Guru Create包，含新增joint | 25 PASS；真正Guru创建、scope Author/Clarify、原D1 Creation/recovery、两次Architecture/Wording/Approval/Activation完整transport，key/no-key两项新回归各保持同Task/gen/单D1。owner语义payload为fixture，不冒充native AI批准 |
| 原Author包 | 12 PASS；复用Planning helper，补approved运输；原第二Task fixture明确建立官方route后调用Creation |
| Approval / Wording | 25 / 32 PASS，原公共input与per-Delivery root保持 |
| Activation / Creation / Bind | 6 / 6 / 12 PASS，原结果恢复、session保护与explicit mode仍使用原owner |
| Architecture包 | 32 PASS，完整隔离source snapshot使用已有managed3.12 runtime；原checkout的common runtime旧pointer导致首轮环境失败，未修改主pointer或runtime lock/cache |
| 公共Projection | installed10 PASS + scope revision定向3 PASS；后者使用managed Python的PATH执行真实apply/reapply。首次select conflict揭示明确选择与Creation自动恢复的差异，保留官方明确select切换；仅Creation创建/恢复不静默覆盖current |
| old untracked / 原Upgrade preview + real Plan2 | 新回归1 PASS；官方0.6.17 writer真实创建planning Task且HEAD无其record，完整legacy inventory逐记录defer。preview preserve bytes/modes、五规划、普通dirty/untracked、HEAD/refs/worktrees，零写；preset边界沿既有fixture stub，不是完整Guru升级或恢复 |
| source package validation | PASS：38 active packages / 114 commands；registry及public I/O未新增，注册两项新test |
| representative installed reapply | 首轮受管replacement产生.bak，零unknown-edit conflict；原installer再次重应用返回ok，installed validation PASS、零sidecar。后续内容修订均以matching reapply和原受管backup恢复处理 |
| Claude / Codex / Cursor投影 | shared与三个native skill roots逐字节比较PASS；installer验证受管file hash/mode及匹配selection，不是完整平台矩阵 |

## 本次真实context及原失败对象

受控同源样本 `guru548-real-create-20261014-a`：实际Codex context正式C6创建example-task/gen0；原无key首次C7失败时D1为45e72a91-a66a-4b6b-85a2-f9d4fe10fb98。
更新匹配preset后，原Creation以该失败operation的明确key执行selection恢复；无key原Author实际返回requirements_ready，原producer retirement端口消费pending。Task record逐字节等价、同UUID、一个D1；没有新Task/branch/worktree或Planning gate。
真实本次Codex context随后明确选择同D1，官方task.py current与get_context --json均读回同Task/gen/current planning、原planning_root，全部public gates仍missing。get_context --mode continuation读取实际selected workspace的唯一continuation合同，current/planning指原Author/Wording/Architecture/Approval；此文本读取本身不是native客户端自动注入证明。
该native sample按来源允许停在恢复后的Planning入口。完整Approval/Activation链由上述joint fixtures证明transport；不声称native完整AI审批、自动hook注入、原CMS会话或业务安装恢复通过。

环境/fixture首次失败独立保留：matching Task1前驱不可得；系统Python缺依赖与旧common pointer不计通过；首次joint把dirty内容放在C3 acquisition前得到zero_validated_candidates，已在正确创建后验证恢复保留；旧nonterminal按真实planning状态保留，不改状态假造已激活。

原CMS会话、原业务安装/恢复/部署、Task1 castbox3匹配前驱转换、完整平台/Release矩阵未验证且排除。主/开发dogfood保持完整legacy；它只执行本Task开发，不证明current Task2组合。
