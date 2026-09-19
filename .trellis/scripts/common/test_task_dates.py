import os
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

from paths import generate_task_archive_month, generate_task_date, generate_task_date_prefix


class TaskDateTests(unittest.TestCase):
    def test_fixed_instant_uses_shanghai_date_at_utc_midnight_boundary(self):
        before_midnight = datetime(2026, 9, 18, 15, 59, 59, tzinfo=timezone.utc)
        after_midnight = datetime(2026, 9, 18, 16, 0, 0, tzinfo=timezone.utc)

        self.assertEqual("09-18", generate_task_date_prefix(before_midnight))
        self.assertEqual("2026-09-18", generate_task_date(before_midnight))
        self.assertEqual("09-19", generate_task_date_prefix(after_midnight))
        self.assertEqual("2026-09-19", generate_task_date(after_midnight))

    def test_archive_month_uses_same_business_timezone(self):
        instant = datetime(2026, 9, 30, 16, 30, tzinfo=timezone.utc)
        self.assertEqual("2026-10", generate_task_archive_month(instant))

    def test_process_timezone_does_not_change_business_date(self):
        script = (
            "from paths import generate_task_date, generate_task_date_prefix; "
            "print(generate_task_date_prefix()); print(generate_task_date())"
        )
        root = Path(__file__).resolve().parent
        outputs = []
        for tz in ("UTC", "Asia/Shanghai"):
            env = os.environ.copy()
            env["TZ"] = tz
            outputs.append(
                subprocess.check_output(
                    [sys.executable, "-c", script],
                    cwd=root,
                    env=env,
                    text=True,
                ).splitlines()
            )
        self.assertEqual(outputs[0], outputs[1])


if __name__ == "__main__":
    unittest.main()
