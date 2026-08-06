#!/usr/bin/env python3
"""Focused tests for Codex workflow-state hook dispatch banner."""

from __future__ import annotations

import importlib.util
import unittest
from types import SimpleNamespace
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

    def test_missing_config_defaults_to_inline_banner(self) -> None:
        banner = self.hook._codex_mode_banner({})
        self.assertIn("<codex-mode>inline:", banner)
        self.assertIn("do not dispatch", banner)

    def test_invalid_config_defaults_to_inline_banner(self) -> None:
        banner = self.hook._codex_mode_banner({"codex": {"dispatch_mode": "disabled"}})
        self.assertIn("<codex-mode>inline:", banner)

    def test_explicit_inline_banner_is_respected(self) -> None:
        banner = self.hook._codex_mode_banner({"codex": {"dispatch_mode": "inline"}})
        self.assertIn("<codex-mode>inline:", banner)
        self.assertIn("do not dispatch", banner)

    def test_no_task_workflow_state_routes_through_thin_intake_graph(self) -> None:
        root = Path(__file__).resolve().parents[2]
        templates = self.hook.load_breadcrumbs(root)
        breadcrumb = self.hook.build_breadcrumb(None, "no_task", templates)

        self.assertIn("Status: no_task", breadcrumb)
        self.assertIn("Repo-changing work starts", breadcrumb)
        self.assertIn("guru-sync-base", breadcrumb)
        self.assertIn("automatically consumes mapped exits", breadcrumb)
        self.assertNotIn("check-env.sh", breadcrumb)
        self.assertNotIn("prepare-task", breadcrumb)

    def test_completed_workflow_state_routes_through_canonical_finish_entry(self) -> None:
        root = Path(__file__).resolve().parents[2]
        templates = self.hook.load_breadcrumbs(root)
        breadcrumb = self.hook.build_breadcrumb("example-task", "completed", templates)

        self.assertIn("Task: example-task (completed)", breadcrumb)
        self.assertIn("Use canonical guru-finish-work", breadcrumb)
        self.assertIn("publication, verification, resume, and reprepare exits", breadcrumb)
        self.assertNotIn("review-gate.json", breadcrumb)


class CodexSessionStartNoTaskTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = Path(__file__).with_name("session-start.py")
        spec = importlib.util.spec_from_file_location("codex_session_start", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load hook module: {path}")
        cls.session_start = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.session_start)

    def test_no_task_fallback_remains_official_and_has_no_guru_prepare_route(self) -> None:
        original_resolver = self.session_start._resolve_active_task
        try:
            self.session_start._resolve_active_task = lambda _trellis_dir, _hook_input: SimpleNamespace(task_path=None)
            status = self.session_start._get_task_status(Path(".trellis"), {})
        finally:
            self.session_start._resolve_active_task = original_resolver

        self.assertIn("Status: NO ACTIVE TASK", status)
        self.assertIn("ask for task-creation consent before creating any Trellis task", status)
        self.assertNotIn("check-env.sh", status)
        self.assertNotIn("prepare-task", status)


class CursorSessionStartNoTaskTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = Path(__file__).resolve().parents[2] / ".cursor/hooks/session-start.py"
        spec = importlib.util.spec_from_file_location("cursor_session_start", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load hook module: {path}")
        cls.session_start = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.session_start)

    def test_no_task_fallback_remains_official_and_has_no_guru_prepare_route(self) -> None:
        original_resolver = self.session_start._resolve_active_task
        try:
            self.session_start._resolve_active_task = lambda _trellis_dir, _hook_input: SimpleNamespace(task_path=None)
            status = self.session_start._get_task_status(Path(".trellis"), {})
        finally:
            self.session_start._resolve_active_task = original_resolver

        self.assertIn("Status: NO ACTIVE TASK", status)
        self.assertIn("Classify the current turn before creating any Trellis task", status)
        self.assertIn("Simple conversation / small task", status)
        self.assertNotIn("check-env.sh", status)
        self.assertNotIn("prepare-task", status)


if __name__ == "__main__":
    unittest.main()
