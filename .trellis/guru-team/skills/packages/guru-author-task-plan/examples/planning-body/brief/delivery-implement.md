# full D1 pack 帮助实施与验证（教学正文）

## 1. 输入与引用

先读 [source 全文](source.md)、[Task PRD](task-prd.md)、[D1 PRD](delivery-prd.md)、[design 第3–8节](delivery-design.md#3-来源设计处置)。当前无前序，本批是完整help修复。真实实现须读取当前源码及规格，不用教学快照替代live事实。

## 2. 有依赖顺序的步骤与文件责任

I1：实施在cli.py的build_parser仅替换output的help参数，保留default/metavar/解析及build；人工diff可核对没有改默认值。I2依赖I1，在usage.md补用途、默认dist及不覆盖行为，不加入新能力。I3依赖I1/I2，在test_cli.py补实际help可见/无产物观察，运行原行为回归。I4依赖真实结果，由原docs owners处理所需差额，再由原Check检查完整本批。

## 3. 验证入口、输入与预期观察

示例对应仓库计划用 `python -m unittest discover -s tests -p test_cli.py`。V1在临时目录调用真实 `python -m pack --help`，观察--output、用途、默认dist、exit0、无构建产物；V2执行原默认/显式/目标已存在用例，保持原结果；V3由原审核owner比较usage与实际help、核对参数和执行diff。映射design V1–V3/AC1–AC3。Guru扩展源仓库并无这个pack项目；这里未运行，不生成通过声明。

## 4. 停止条件与适用回退点

实际默认/覆盖口径不可查或冲突时停依赖写作，回Clarify处理真正选择。技术细化由Author/Architecture完成。发现I1误改执行默认值则恢复本批该处并重验，保留并行工作。没有数据迁移、服务部署或发布，无DB回滚协议。Git/GitHub副作用仍归原边界。

## 5. Delivery Policy（唯一）

选择full。本批承担R1–R3/AC1–AC3，无计划剩余切片。完成须实际help和原行为验证及原审核；不能用合并或remaining work为空代替整体Completion。

## 6. Docs SSOT Plan（唯一）

选择ssot_first。原RDT writer按source §2定位真实requirement/design/test authority，维护help可见性及唯一测试的实际差额，直接consumer为原docs维护及Check/Review。Architecture owner按实际边界不变判断，无真实贡献不创建空ledger。共享写入与晋升沿原owner/expected-current合同在最终Phase2前完成，不由本教学模板直接写导航。usage是本批产品文档，并非第二份测试权威。
