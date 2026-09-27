import os
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import generate_task_date_prefix


class TaskDateTests(unittest.TestCase):
    def test_official_date_uses_process_timezone(self):
        script = (
            "from paths import generate_task_date_prefix; "
            "print(generate_task_date_prefix())"
        )
        root = Path(__file__).resolve().parent
        env = {**os.environ, "TZ": "Asia/Shanghai"}
        before = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%m-%d")
        output = subprocess.check_output(
            [sys.executable, "-c", script], cwd=root, env=env, text=True,
        ).strip()
        after = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%m-%d")
        self.assertIn(output, {before, after})


if __name__ == "__main__":
    unittest.main()
