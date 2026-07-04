#!/usr/bin/env python3
"""Focused tests for Codex workflow-state hook dispatch banner."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load_hook_module():
    path = Path(__file__).with_name("inject-workflow-state.py")
    spec = importlib.util.spec_from_file_location("inject_workflow_state", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load hook module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CodexModeBannerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hook = load_hook_module()

    def test_missing_config_defaults_to_sub_agent_banner(self) -> None:
        banner = self.hook._codex_mode_banner({})
        self.assertIn("<codex-mode>sub-agent:", banner)
        self.assertIn("Trellis sub-agents", banner)

    def test_invalid_config_defaults_to_sub_agent_banner(self) -> None:
        banner = self.hook._codex_mode_banner({"codex": {"dispatch_mode": "disabled"}})
        self.assertIn("<codex-mode>sub-agent:", banner)

    def test_explicit_inline_banner_is_respected(self) -> None:
        banner = self.hook._codex_mode_banner({"codex": {"dispatch_mode": "inline"}})
        self.assertIn("<codex-mode>inline:", banner)
        self.assertIn("do not dispatch", banner)


if __name__ == "__main__":
    unittest.main()
