#!/usr/bin/env python3
"""Focused tests for workflow phase platform selection."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.workflow_phase import resolve_effective_platform


class CodexDispatchModeTest(unittest.TestCase):
    def test_missing_codex_config_defaults_to_sub_agent(self) -> None:
        self.assertEqual(resolve_effective_platform("codex", {}), "codex-sub-agent")

    def test_invalid_codex_dispatch_mode_defaults_to_sub_agent(self) -> None:
        self.assertEqual(
            resolve_effective_platform("codex", {"codex": {"dispatch_mode": "disabled"}}),
            "codex-sub-agent",
        )

    def test_explicit_inline_is_respected(self) -> None:
        self.assertEqual(
            resolve_effective_platform("codex", {"codex": {"dispatch_mode": "inline"}}),
            "codex-inline",
        )

    def test_non_codex_platform_is_unchanged(self) -> None:
        self.assertEqual(resolve_effective_platform("cursor", {}), "cursor")


if __name__ == "__main__":
    unittest.main()
