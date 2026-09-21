#!/usr/bin/env python3
"""Focused tests for the #452 platform inventory and installer CLI contract."""

from __future__ import annotations

import json
import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import apply_guru_team_trellis_preset as preset
import guru_platform_inventory as inventory

GURU_ROOT = preset.guru_root_from_script()
CANONICAL_MANIFEST = json.loads(
    (GURU_ROOT / "trellis/guru-team-extension.json").read_text(encoding="utf-8")
)


def successful_install_result(platforms: set[str]) -> dict[str, object]:
    return {
        "platforms": sorted(platforms),
        "installed": [],
        "unchanged": [],
        "new_copies": [],
        "replaced_overlays": [],
        "updated_managed": [],
        "managed_backups": [],
        "managed_transaction": {},
        "agents_principles": {},
        "codex_dispatch": {},
        "runtime_gitignore": {},
        "language_guidance": {},
        "extension_manifest": ".trellis/guru-team/extension.json",
        "guru_team_extension": {},
        "skill_packages": {"status": "ok"},
        "overlays": {"status": "ok"},
        "skill_source_validation": {},
        "upstream_ownership_validation": {},
        "skill_installed_validation": {"returncode": 0},
        "python_runtime": {},
    }


class PlatformInventoryTest(unittest.TestCase):
    def test_pinned_inventory_has_22_unique_ids_and_cli_flags(self) -> None:
        self.assertEqual(len(inventory.UPSTREAM_PLATFORMS), 22)
        self.assertEqual(len(inventory.PLATFORM_BY_UPSTREAM_ID), 22)
        self.assertEqual(len(inventory.PLATFORM_BY_FLAG), 22)
        self.assertEqual(
            inventory.PLATFORM_BY_UPSTREAM_ID["claude-code"].cli_flag,
            "claude",
        )
        self.assertEqual(inventory.PLATFORM_BY_FLAG["claude"].upstream_id, "claude-code")

    def test_manifest_binding_consumes_only_upstream_inventory(self) -> None:
        descriptors = inventory.validate_manifest_inventory(CANONICAL_MANIFEST)
        supported, default = preset.platform_capability_sets(CANONICAL_MANIFEST)

        self.assertEqual(descriptors, inventory.UPSTREAM_PLATFORMS)
        self.assertEqual(supported, inventory.PLATFORM_FLAGS)
        self.assertEqual(default, ("claude", "codex", "cursor"))
        capabilities = CANONICAL_MANIFEST["public_api"]["platform_capabilities"]
        self.assertNotIn("guru_supported_platforms", capabilities)
        self.assertNotIn("deferred_platforms", capabilities)
        self.assertEqual(
            capabilities["default_platforms"],
            ["claude", "codex", "cursor"],
        )
        self.assertNotIn("kilo", default)

    def test_manifest_inventory_drift_fails_closed(self) -> None:
        changed = json.loads(json.dumps(CANONICAL_MANIFEST))
        changed["public_api"]["platform_capabilities"]["upstream_platforms"][0][
            "cli_flag"
        ] = "claude-code"

        with self.assertRaisesRegex(SystemExit, "drift from the pinned inventory"):
            inventory.validate_manifest_inventory(changed)

    def test_selection_modes_are_exact_and_have_no_deferred_tier(self) -> None:
        self.assertEqual(
            inventory.select_platforms(None),
            {"claude", "codex", "cursor"},
        )
        self.assertEqual(
            inventory.select_platforms(["kilo", "opencode", "kilo"]),
            {"kilo", "opencode"},
        )

    def test_inventory_platforms_have_registry_bound_skill_projection_roots(self) -> None:
        roots = inventory.selected_skill_roots(inventory.PLATFORM_FLAGS)
        self.assertEqual(roots[0], Path(".agents/skills"))
        self.assertIn(Path(".codex/skills"), roots)
        self.assertIn(Path(".opencode/skills"), roots)
        self.assertIn(Path(".kilocode/skills"), roots)
        self.assertIn(Path(".github/skills"), roots)
        self.assertIn(Path(".snow/skills"), roots)
        self.assertEqual(len(roots), len(set(roots)))
        for descriptor in inventory.UPSTREAM_PLATFORMS:
            self.assertTrue(descriptor.skill_roots)
            self.assertTrue(set(descriptor.skill_roots).intersection(roots))

    def test_managed_projection_covers_every_native_root_without_public_tests(self) -> None:
        repo = Path("/tmp/guru-platform-projection-fixture")
        projections = preset.managed_source_projections(
            repo,
            repo / ".trellis/guru-team",
            set(inventory.PLATFORM_FLAGS),
        )

        for skill_root in inventory.selected_skill_roots(inventory.PLATFORM_FLAGS):
            expected = skill_root / "guru-create-task-workspace/SKILL.md"
            self.assertIn(expected, projections)
        self.assertEqual(
            [
                path
                for path in projections
                if "/tests/" in path.as_posix()
                and not path.as_posix().startswith(".trellis/guru-team/skills/")
            ],
            [],
        )

    def test_overlay_inventory_is_descriptor_driven_not_dogfood_driven(self) -> None:
        self.assertEqual(
            len(preset.GURU_OVERLAY_ENTRY_PATHS),
            len(inventory.PLATFORM_FLAGS),
        )
        dogfood_entries = {
            preset.GURU_OVERLAY_ENTRY_PATHS[platform]
            for platform in inventory.DEFAULT_PLATFORM_FLAGS
        }
        self.assertEqual(len(dogfood_entries), 3)
        self.assertTrue(
            preset.overlay_selected(
                Path(".kilocode/workflows/guru-finish-work.md"), {"kilo"}
            )
        )
        self.assertTrue(
            preset.overlay_selected(
                Path(".opencode/commands/guru-finish-work.md"), {"opencode"}
            )
        )

    def test_installed_overlay_provenance_accepts_any_inventory_selection(self) -> None:
        manifest = {
            "overlays": {
                "schema_version": preset.GURU_OVERLAY_SCHEMA_VERSION,
                "status": "ok",
                "selected_platforms": sorted(inventory.PLATFORM_FLAGS),
                "files": [],
                "removals": [],
                "conflicts": [],
                "sidecars": [],
            }
        }

        _, _, valid, _ = preset.previous_overlay_hashes(manifest, {})
        self.assertTrue(valid)


class InstallerPlatformCliTest(unittest.TestCase):
    def invoke(self, *arguments: str) -> tuple[int, dict[str, object], mock.Mock]:
        install = mock.Mock(
            side_effect=lambda _src, _dst, _repo, platforms: successful_install_result(platforms)
        )
        stdout = StringIO()
        with mock.patch("sys.argv", ["apply_guru_team_trellis_preset.py", *arguments]), mock.patch.object(
            preset, "load_extension_manifest", return_value=CANONICAL_MANIFEST
        ), mock.patch.object(
            preset, "repo_root_from_args", return_value=Path("/tmp/guru-platform-target")
        ), mock.patch.object(
            preset, "install_assets", install
        ), mock.patch("sys.stdout", stdout):
            exit_code = preset.main()
        return exit_code, json.loads(stdout.getvalue()), install

    def test_no_platform_flags_use_three_platform_default(self) -> None:
        exit_code, payload, install = self.invoke()

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["platforms"], ["claude", "codex", "cursor"])
        self.assertEqual(install.call_args.args[3], {"claude", "codex", "cursor"})

    def test_repeated_platform_flags_select_exact_deduplicated_subset(self) -> None:
        exit_code, payload, install = self.invoke(
            "--platform", "kilo", "--platform", "opencode", "--platform", "kilo"
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["platforms"], ["kilo", "opencode"])
        self.assertEqual(install.call_args.args[3], {"kilo", "opencode"})

    def test_unknown_platform_is_rejected_by_parser(self) -> None:
        with mock.patch(
            "sys.argv",
            ["apply_guru_team_trellis_preset.py", "--platform", "unknown-platform"],
        ), mock.patch.object(
            preset, "load_extension_manifest", return_value=CANONICAL_MANIFEST
        ):
            with self.assertRaises(SystemExit) as raised:
                preset.main()

        self.assertNotEqual(raised.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
