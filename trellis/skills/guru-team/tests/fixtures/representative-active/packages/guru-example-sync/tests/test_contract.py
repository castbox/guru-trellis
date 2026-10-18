from pathlib import Path
import json


def test_sync_example() -> None:
    root = Path(__file__).resolve().parents[1]
    assert json.loads((root / "examples/sync-output.json").read_text())["exit_id"] == "synced"
