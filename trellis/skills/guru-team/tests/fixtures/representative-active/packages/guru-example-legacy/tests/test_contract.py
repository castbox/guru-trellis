from pathlib import Path
import json


def test_legacy_example() -> None:
    root = Path(__file__).resolve().parents[1]
    assert json.loads((root / "examples/legacy-result.json").read_text())["status"] == "completed"
