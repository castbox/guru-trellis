"""Normal review objects; acceptance expectations are held by the observing owner."""
from __future__ import annotations

ARCHITECTURE = """# Architecture authority

This local Python library has HTTP, CLI and optional CSV adapters. Pure domain
functions own invoice rules. Adapters must preserve domain values. There is no
database, network deployment, concurrency or security change in this candidate.
Review local functions against requirements.md. Public API configuration permits
ROUND_HALF_UP and offset-aware ISO timestamps. No universal preference for a
different rounding mode or zero-offset input applies.
"""

REQUIREMENTS = """# Invoice contract

R1 page(rows, offset, limit) returns the requested slice and total number of all
matching rows. offset is nonnegative and limit positive, supplied by adapters.
R2 cancel(jobs, id) changes only that queued job to cancelled; another job is
unaffected. The supplied identifier exists and identifies a queued job.
R3 Every adapter emits timestamps as UTC ISO strings ending Z. Input timestamps
are offset-aware. Converting to UTC must retain the instant.
R4 money(value) uses configured Decimal ROUND_HALF_UP to two decimal places.
This is an accepted option; no other rounding mode is required.
R5 HTTP and CLI expose the same timestamp and amount. If a CSV adapter is present,
its header is id,amount,timestamp and it uses those same values in that order.
"""

DOMAIN = '''from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

def page(rows, offset, limit):
    selected = rows[offset:offset + limit]
    return {"items": selected, "total": len(selected)}

def cancel(jobs, identifier):
    for job in jobs:
        job["status"] = "cancelled"
    return jobs

def format_stamp(value):
    stamp = datetime.fromisoformat(value)
    return stamp.replace(tzinfo=None).isoformat() + "Z"

def money(value):
    return str(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
'''

ADAPTERS = '''from domain import format_stamp, money

def http_invoice(row):
    return {"id": row["id"], "amount": money(row["amount"]),
            "timestamp": format_stamp(row["timestamp"])}

def cli_invoice(row):
    return " ".join([row["id"], money(row["amount"]), format_stamp(row["timestamp"])])
'''

TESTS = '''import unittest
from domain import page, cancel, format_stamp, money
from adapters import http_invoice, cli_invoice

class InvoiceTests(unittest.TestCase):
    def test_page(self):
        self.assertEqual(page([1, 2, 3], 1, 1), {"items": [2], "total": 3})
    def test_cancel(self):
        jobs = [{"id": "a", "status": "queued"}, {"id": "b", "status": "queued"}]
        self.assertEqual(cancel(jobs, "a")[1]["status"], "queued")
    def test_offset(self):
        self.assertEqual(format_stamp("2026-01-01T09:00:00+08:00"), "2026-01-01T01:00:00Z")
    def test_rounding(self):
        self.assertEqual(money("1.005"), "1.01")
    def test_adapters(self):
        row = {"id": "a", "amount": "1.005", "timestamp": "2026-01-01T09:00:00+08:00"}
        self.assertEqual(http_invoice(row)["timestamp"], "2026-01-01T01:00:00Z")
        self.assertIn("1.01", cli_invoice(row))
'''

CSV = '''from domain import format_stamp, money

def csv_invoice(row):
    return "id,timestamp,amount\\n" + ",".join([
        row["id"], format_stamp(row["timestamp"]), money(row["amount"])])
'''


def files(case: str) -> dict[str, str]:
    if case in {"B", "E"}:
        domain = DOMAIN
        tests = TESTS
        if case == "E":
            domain = domain.replace('"total": len(selected)', '"total": len(rows)')
            domain = domain.replace('        job["status"] = "cancelled"',
                                    '        if job["id"] == identifier:\n            job["status"] = "cancelled"')
            domain = domain.replace('stamp.replace(tzinfo=None).isoformat() + "Z"',
                                    'stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")')
            tests = tests.replace('self.assertEqual(cancel(jobs, "a")[1]["status"], "queued")',
                                  'self.assertEqual(cancel(jobs, "a"), [{"id": "a", "status": "cancelled"}, '
                                  '{"id": "b", "status": "queued"}])')
            tests = tests.replace('self.assertEqual(http_invoice(row)["timestamp"], "2026-01-01T01:00:00Z")',
                                  'self.assertEqual(http_invoice(row), {"id": "a", "amount": "1.01", '
                                  '"timestamp": "2026-01-01T01:00:00Z"})')
            tests = tests.replace('self.assertIn("1.01", cli_invoice(row))',
                                  'self.assertEqual(cli_invoice(row), "a 1.01 2026-01-01T01:00:00Z")')
        return {"requirements.md": REQUIREMENTS, "architecture.md": ARCHITECTURE,
                "domain.py": domain, "adapters.py": ADAPTERS, "test_invoice.py": tests}
    if case == "A":
        return {"issue.md": """# Issue draft: 异步账单导出

管理员在账单页选择筛选条件后提交异步 CSV 导出，完成时向收件人发邮件。
后台从账单集合生成文件；任务排队期间用户仍能修改账单或筛选条件。
系统有账户管理员和普通成员两种角色。管理员可管理账户内全部成员；
普通成员只能查看自己的账单。导出入口向两种角色开放。
提交者可以填写收件邮箱，页面提供取消任务按钮。取消必须有可观察的结果，
避免用户反复点击。文件编码由调用方明确选择 UTF-8 或带 BOM 的 UTF-8；
两种配置都属于本项支持范围。验收覆盖正常导出、邮件接收以及取消操作。
""", "repository-facts.md": """# Current repository facts

这是尚未实现的本地 Issue 草稿。仓库没有历史导出实现、收件策略或取消状态约定。
原始需求全文在 issue.md。本次只审核需求，不创建 Issue、Task，不修改正文。
"""}
    if case == "C":
        return {"source.md": """# Accepted source

提交订单成功写入后才发通知。只有 queued 状态允许取消。
重试配置 max_attempts 表示包括首次调用在内的总尝试次数。
供应商的展示字体链接仅为可选阅读资料，不控制上述行为。
""", "design.md": """# Order design

规范性来源是 source.md 的完整正文。先发通知，随后提交订单。
任何状态均允许取消。max_attempts 代表总尝试次数。
展示字体可选资料：vendor-font-guide.md；缺失时不影响本地订单与取消规则。
""", "implement.md": """# Order implementation plan

先提交订单，成功后发通知。只有 queued 状态允许取消。
max_attempts 代表首次调用失败后额外重试的次数。
本次只审核 design.md 和 implement.md 的合同语义和措辞，不编辑文件。
"""}
    if case == "D":
        return {"architecture.md": ARCHITECTURE, "requirements.md": """# Report contract

R1 total(values) sums every supplied integer value.
R2 vendor_stamp(value) must match the external vendor timestamp contract at
vendor-contract.md. That required document has not been supplied in this checkout.
No local source fixes the vendor's actual format. The local sum rule is independent.
""", "report.py": '''def total(values):
    return sum(values[:-1])

def vendor_stamp(value):
    return str(value)
''', "test_report.py": '''import unittest
from report import total
class ReportTests(unittest.TestCase):
    def test_all_values(self):
        self.assertEqual(total([3, 4]), 7)
'''}
    raise ValueError("Unknown review object")


def request(case: str) -> str:
    if case == "A":
        return ("使用 guru-clarify-requirements 的 standard_intake，审核 issue.md 这份 Issue 草稿的需求、"
                "范围与验收是否完整。按原前置先取得实际 Discovery context；未满足时沿原 owner恢复。"
                "本次只审查，在当前对话列出具体未决项及建议，不能编造我的答复或改文件、创建资源。")
    if case == "C":
        return ("使用 guru-review-contract-wording 的 explicit_paths，独立只读审核明确选定的 "
                "design.md 和 implement.md 全文的语义与措辞，必要来源是 source.md。"
                "不要改写文件。返回当前审核发现、已查范围及局限；不是正式 Planning Approval。")
    return ("使用 guru-review-change，以 working_tree 原公开入口独立只读审核当前目录候选的"
            "需求实现、代码和测试；范围为根目录提供的 requirements.md、architecture.md、Python文件。"
            "遵守原三名独立子Agent与架构先读要求。只审核，不修改文件或推进任何Task/Delivery。"
            "输出本次实际完整报告和原公开入口的最终出口。")


FOLLOWUPS = [
    "候选文件已更新。请按同一原入口复审当前完整增量及其影响，并承接仍有效的既有覆盖；只读。",
    "候选自上次没有变化。请据当前证据结束这次只读审核并给出完整当前结论。",
]
