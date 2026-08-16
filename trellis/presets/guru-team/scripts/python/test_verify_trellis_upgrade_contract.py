from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
VERIFIER = REPO / "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
SCHEMAS = REPO / "trellis/skills/guru-team/schemas"
EXTENSION = REPO / "trellis/guru-team-extension.json"


class VerifyTrellisUpgradeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = VERIFIER.read_text(encoding="utf-8")

    def test_cli_install_and_upgrade_stay_in_disposable_prefix(self) -> None:
        self.assertIn('TRELLIS_CLI_PREFIX="$WORK_DIR/trellis-cli-prefix"', self.text)
        self.assertIn(
            'npm_config_prefix="$TRELLIS_CLI_PREFIX" npm install -g "$TRELLIS_PRE_UPGRADE_PACKAGE"',
            self.text,
        )
        self.assertIn('export npm_config_prefix="$TRELLIS_CLI_PREFIX"', self.text)
        self.assertIn('TRELLIS_CLI_BIN="$TRELLIS_CLI_PREFIX/bin/trellis"', self.text)
        self.assertIn('trellis upgrade --tag "$TRELLIS_UPGRADE_TAG"', self.text)
        self.assertIn('trellis-version-before-upgrade.txt', self.text)
        self.assertIn('trellis-version-after-upgrade.txt', self.text)
        self.assertIn('trellis upgrade escaped the isolated npm prefix', self.text)

    def test_initial_install_upgrade_update_preview_and_reapply_order_is_closed(self) -> None:
        initial = self.text.index("trellis init -y --claude --codex --cursor")
        upgrade = self.text.index('trellis upgrade --tag "$TRELLIS_UPGRADE_TAG"')
        dry_run = self.text.index("trellis update --dry-run 2>&1", upgrade)
        migrate_branch = self.text.index('if grep -Fq "MIGRATION REQUIRED"', dry_run)
        migrate = self.text.index("trellis update --migrate", migrate_branch)
        normal_update = self.text.index("    trellis update\n", migrate)
        preview = self.text.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --create-new',
            normal_update,
        )
        switch = self.text.index(
            'trellis workflow --marketplace "$WORKFLOW_SOURCE" --template guru-team --force',
            preview,
        )
        reapply = self.text.index(
            'apply_guru_team_trellis_preset.py" \\\n  --repo "$TARGET"',
            switch,
        )
        self.assertLess(initial, upgrade)
        self.assertLess(upgrade, dry_run)
        self.assertLess(dry_run, migrate_branch)
        self.assertLess(migrate_branch, migrate)
        self.assertLess(migrate, normal_update)
        self.assertLess(normal_update, preview)
        self.assertLess(preview, switch)
        self.assertLess(switch, reapply)
        primary_update_segment = self.text[upgrade:reapply]
        self.assertNotIn("trellis update --force", primary_update_segment)
        self.assertIn('printf \'%s\\n\' "migrate" >"$WORK_DIR/trellis-update-mode.txt"', primary_update_segment)
        self.assertIn('printf \'%s\\n\' "update" >"$WORK_DIR/trellis-update-mode.txt"', primary_update_segment)

    def test_post_reapply_gate_checks_ownership_and_recursive_sidecars(self) -> None:
        self.assertIn('ownership_checkpoint "post-preset-reapply-before-final-checks"', self.text)
        self.assertIn(
            'FINAL_SIDECARS="$(find "$TARGET" -type f \\( -name \'*.new\' -o -name \'*.bak\' \\) -print)"',
            self.text,
        )
        self.assertIn("Unexpected .new/.bak sidecars after preview, switch, update, and preset reapply", self.text)

    def test_embedded_installed_schema_inventory_matches_canonical_source(self) -> None:
        inventory_anchor = 'skills_root = root / ".trellis/guru-team/skills"'
        assertion_start = self.text.index("assert {", self.text.index(inventory_anchor))
        literal_start = self.text.index("} == {", assertion_start) + len("} == ")
        literal_end = self.text.index("\n}\nfor artifact", literal_start) + 2
        embedded_inventory = ast.literal_eval(self.text[literal_start:literal_end])
        canonical_inventory = {path.name for path in SCHEMAS.iterdir() if path.is_file()}

        self.assertEqual(embedded_inventory, canonical_inventory)

    def test_embedded_installed_public_api_expectations_match_canonical_source(self) -> None:
        contract_anchor = 'assert api["skill_contracts"]["contract_manifests"] == '
        contract_start = self.text.index(contract_anchor) + len(contract_anchor)
        contract_end = self.text.index(
            '\nassert api["skill_evals"]["schema_id"]',
            contract_start,
        )
        embedded_contracts = ast.literal_eval(self.text[contract_start:contract_end])

        run_schemas_anchor = 'assert api["skill_evals"]["run_schema_ids"] == '
        run_schemas_start = self.text.index(run_schemas_anchor) + len(run_schemas_anchor)
        run_schemas_end = self.text.index("\n", run_schemas_start)
        embedded_run_schemas = ast.literal_eval(
            self.text[run_schemas_start:run_schemas_end]
        )

        public_api = json.loads(EXTENSION.read_text(encoding="utf-8"))["public_api"]
        self.assertEqual(
            embedded_contracts,
            public_api["skill_contracts"]["contract_manifests"],
        )
        self.assertEqual(
            embedded_run_schemas,
            public_api["skill_evals"]["run_schema_ids"],
        )
        self.assertIn(
            'test -f "$TARGET/.trellis/guru-team/skills/contracts/production-current-4.0.json"',
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
