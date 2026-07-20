from pathlib import Path
import json


def test_action_examples() -> None:
    root = Path(__file__).resolve().parents[1]
    initial = json.loads((root / "examples/action-initial-input.json").read_text())
    completed = json.loads((root / "examples/action-completed-output.json").read_text())
    assert initial["profile"] == "initial"
    assert completed["exit_id"] == "completed"
