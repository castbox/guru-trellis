from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("verify_throwaway_python_routing.py")
SPEC = importlib.util.spec_from_file_location("verify_throwaway_python_routing", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
ROUTING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROUTING)


class ThrowawayPythonRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.verifier_path = Path("trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh")
        source_root = MODULE_PATH.parents[5]
        inventory = json.loads(
            (source_root / "trellis/presets/guru-team/tests/throwaway-python-callers.json").read_text()
        )
        verifier_text = (source_root / self.verifier_path).read_text(encoding="utf-8")
        self.helper_paths = tuple(Path(row["path"]) for row in inventory["python_helpers"])
        self.transitive_paths = tuple(
            Path(row["path"]) for row in inventory["transitive_python_helpers"]
        )
        self.shell_paths = tuple(
            Path(row["owner"]) for row in inventory["shell_python_helpers"]
        )
        self.shell_route_paths = tuple(
            Path(path)
            for row in inventory["shell_python_helpers"]
            for path in row.get("route", [])
        )
        runtime_spec = inventory["package_runtime_closure"]
        self.package_runtime_paths = tuple(
            path.relative_to(source_root)
            for path in sorted(
                (source_root / runtime_spec["root"]).glob(runtime_spec["glob"])
            )
            if path.is_file()
        )
        referenced_shell_paths = tuple(
            Path(row["owner"])
            for row in ROUTING.discover_referenced_shell_helpers(verifier_text)
        )
        launch_owners = tuple(
            Path(row["launch_owner"]) for row in inventory["transitive_python_helpers"]
        )
        for relative in dict.fromkeys(
            (
                self.verifier_path,
                *self.helper_paths,
                *self.transitive_paths,
                *self.shell_paths,
                *self.shell_route_paths,
                *referenced_shell_paths,
                *launch_owners,
                *self.package_runtime_paths,
            )
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((source_root / relative).read_bytes())
        self.inventory_path = self.root / "callers.json"
        self.inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def check(self) -> dict[str, object]:
        return ROUTING.check_inventory(self.root, self.inventory_path)

    def load_inventory(self) -> dict[str, object]:
        return json.loads(self.inventory_path.read_text(encoding="utf-8"))

    def write_inventory(self, inventory: dict[str, object]) -> None:
        self.inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

    def refresh_secondary_inventory(self) -> None:
        inventory = self.load_inventory()
        verifier_text = (self.root / self.verifier_path).read_text(encoding="utf-8")
        secondary = ROUTING.discover_inline_secondary_callers(
            verifier_text, str(self.verifier_path)
        )
        helper_rows = [
            *inventory["python_helpers"],
            *inventory["transitive_python_helpers"],
        ]
        for row in helper_rows:
            path = Path(row["path"])
            source = (self.root / path).read_text(encoding="utf-8")
            discovered = ROUTING.discover_secondary_callers(source, str(path))
            row["sys_executable_subprocesses"] = sum(
                item["kind"] == "python_subprocess_second_hop"
                for item in discovered
            )
            row["managed_shebang_bindings"] = len(
                ROUTING.managed_shebang_names(
                    ROUTING.ast.parse(source),
                    ROUTING.python_runtime_aliases(ROUTING.ast.parse(source)),
                )
            )
            secondary.extend(discovered)
        runtime_spec = inventory["package_runtime_closure"]
        for path in sorted(
            (self.root / runtime_spec["root"]).glob(runtime_spec["glob"])
        ):
            if not path.is_file():
                continue
            relative = path.relative_to(self.root)
            secondary.extend(
                ROUTING.discover_secondary_callers(
                    path.read_text(encoding="utf-8"),
                    relative.as_posix(),
                    classification=runtime_spec["classification"],
                    id_namespace="package-runtime",
                    anchor_prefix=relative.as_posix() + " ",
                )
            )
        inventory["secondary_callers"] = secondary
        self.write_inventory(inventory)

    def insert_managed_heredoc(self, statement: str) -> None:
        path = self.root / self.verifier_path
        marker = 'installed_python "$TARGET" - "$TARGET" "$label" <<\'PY\'\n'
        text = path.read_text(encoding="utf-8")
        self.assertIn(marker, text)
        path.write_text(
            text.replace(
                marker,
                marker + "import subprocess\nimport sys\n" + statement + "\n",
                1,
            ),
            encoding="utf-8",
        )

    def test_current_inventory_passes(self) -> None:
        result = self.check()
        self.assertEqual(result["status"], "ok")
        self.assertEqual(
            result["package_runtime_closure"]["python_file_count"],
            len(self.package_runtime_paths),
        )

    def test_package_runtime_path_python_subprocess_fails(self) -> None:
        path = self.root / Path(
            "trellis/skills/guru-team/packages/guru-review-task-publication/runtime/owner.py"
        )
        path.write_text(
            path.read_text(encoding="utf-8")
            + '\nsubprocess.run(["python3", "-V"])\n',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "unmanaged Python subprocess"):
            self.check()

    def test_package_runtime_managed_subprocess_requires_inventory(self) -> None:
        path = self.root / Path(
            "trellis/skills/guru-team/packages/guru-review-task-publication/runtime/owner.py"
        )
        path.write_text(
            path.read_text(encoding="utf-8")
            + '\nsubprocess.run([sys.executable, "-V"])\n',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "secondary caller inventory drift"):
            self.check()
        self.refresh_secondary_inventory()
        self.assertEqual(self.check()["status"], "ok")

    def test_package_runtime_path_shebang_fails(self) -> None:
        path = self.root / self.package_runtime_paths[0]
        path.write_text("#!/usr/bin/env python3\n" + path.read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ROUTING.RoutingError, "PATH Python shebang"):
            self.check()

    def test_package_runtime_dynamic_python_policy_drift_fails(self) -> None:
        path = self.root / Path(
            "trellis/skills/guru-team/packages/guru-reconcile-task-base/runtime/execute.py"
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn("subprocess.run(executed_command", text)
        path.write_text(
            text.replace(
                "executed_command=_managed_validation_command(command)",
                "executed_command=command",
                1,
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "secondary caller inventory drift"):
            self.check()

    def test_finalizer_provenance_python_launcher_drift_fails(self) -> None:
        path = self.root / Path(
            "trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py"
        )
        text = path.read_text(encoding="utf-8")
        marker = "                    sys.executable,\n                    str(apply_script),"
        self.assertIn(marker, text)
        path.write_text(
            text.replace(marker, "                    str(apply_script),", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "secondary caller inventory drift"):
            self.check()

    def test_nested_verifier_entry_is_registered(self) -> None:
        nested = self.check()["nested_verifier_entries"]
        self.assertEqual(len(nested), 1)
        self.assertEqual(nested[0]["classification"], "child_bootstrap_seed")
        self.assertEqual(
            nested[0]["route"][-1],
            "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh",
        )

    def test_nested_verifier_entry_drift_fails(self) -> None:
        path = self.root / Path(
            "trellis/skills/guru-team/packages/guru-verify-extension-installation/runtime/owner.py"
        )
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace(
                "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh",
                "trellis/presets/guru-team/scripts/bash/unknown-verifier.sh",
                1,
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "nested verifier inventory drift"):
            self.check()

    def test_delegated_run_and_exec_launchers_are_checked(self) -> None:
        for source in (
            'owner.run(["python3", "-V"])',
            'os.execv("python3", ["python3", "-V"])',
        ):
            with self.subTest(source=source):
                with self.assertRaisesRegex(
                    ROUTING.RoutingError, "unmanaged Python subprocess"
                ):
                    ROUTING.discover_secondary_callers(source, "runtime/example.py")

    def test_normal_python_caller_forms_are_not_missed(self) -> None:
        managed_cases = {
            "keyword-managed": (
                "import subprocess,sys\n"
                'subprocess.run(args=[sys.executable,"-V"])'
            ),
            "import-alias": (
                "from subprocess import run as execute\nimport sys\n"
                'execute([sys.executable,"-V"])'
            ),
            "module-alias": (
                "import subprocess,sys\npy=sys.executable\n"
                'def launch(): return subprocess.run([py,"-V"])'
            ),
            "write-bytes": (
                "from pathlib import Path\nimport sys\n"
                'Path("x").write_bytes(f"#!{sys.executable}\\n".encode())'
            ),
        }
        for label, source in managed_cases.items():
            with self.subTest(label=label):
                self.assertTrue(
                    ROUTING.discover_secondary_callers(source, "memory.py")
                )

        unmanaged_cases = {
            "keyword-path": (
                "import subprocess\n"
                'subprocess.run(args=["python3","-V"])'
            ),
            "delegated-wrapper": (
                "import subprocess\n"
                "def launch(command): return subprocess.run(command)\n"
                'launch(["python3","-V"])'
            ),
            "shell-string": (
                "import subprocess\n"
                'subprocess.run("python3 -V", shell=True)'
            ),
            "sh-c": (
                "import subprocess\n"
                'subprocess.run(["sh","-c","python3 -V"])'
            ),
            "open-write": 'open("x","w").write("#!/usr/bin/env python3\\n")',
        }
        for label, source in unmanaged_cases.items():
            with self.subTest(label=label):
                with self.assertRaisesRegex(
                    ROUTING.RoutingError,
                    "unmanaged (Python subprocess|generated Python shebang)",
                ):
                    ROUTING.discover_secondary_callers(source, "memory.py")

    def test_poison_activation_before_bootstrap_fails(self) -> None:
        path = self.root / self.verifier_path
        poison = ': >"$GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE"'
        seed = 'python3 "$REPO_ROOT/trellis/skills/guru-team/runtime/bootstrap.py"'
        text = path.read_text(encoding="utf-8").replace(poison, "# poison moved", 1)
        path.write_text(text.replace(seed, poison + "\n" + seed, 1), encoding="utf-8")
        with self.assertRaisesRegex(ROUTING.RoutingError, "poison and source-managed"):
            self.check()

    def test_poison_activation_after_bootstrap_consumer_fails(self) -> None:
        path = self.root / self.verifier_path
        poison = ': >"$GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE"'
        text = path.read_text(encoding="utf-8").replace(poison, "# poison moved", 1)
        path.write_text(text + "\n" + poison + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ROUTING.RoutingError, "poison and source-managed"):
            self.check()

    def test_trellis_python_path_bridge_missing_fails(self) -> None:
        path = self.root / self.verifier_path
        guard = 'export PATH="$PYTHON_BRIDGE_DIR:$PATH"'
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(guard), 1)
        path.write_text(text.replace(guard, "# guard removed", 1), encoding="utf-8")
        with self.assertRaisesRegex(ROUTING.RoutingError, "source-managed Python bridge"):
            self.check()

    def test_trellis_python_path_bridge_before_poison_fails(self) -> None:
        path = self.root / self.verifier_path
        guard = 'export PATH="$PYTHON_BRIDGE_DIR:$PATH"'
        seed = 'python3 "$REPO_ROOT/trellis/skills/guru-team/runtime/bootstrap.py"'
        text = path.read_text(encoding="utf-8").replace(guard, "# guard moved", 1)
        path.write_text(text.replace(seed, guard + "\n" + seed, 1), encoding="utf-8")
        with self.assertRaisesRegex(ROUTING.RoutingError, "source-managed Python bridge"):
            self.check()

    def test_trellis_python_path_bridge_resolver_drift_fails(self) -> None:
        path = self.root / self.verifier_path
        managed_exec = (
            'exec "$SOURCE_RUNTIME_RESOLVER" "$REPO_ROOT" '
            '"$SOURCE_RUNTIME_ASSETS" "\\$@"'
        )
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(managed_exec), 1)
        path.write_text(
            text.replace(managed_exec, 'exec "$SOURCE_RUNTIME_RESOLVER" "\\$@"', 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "source-managed Python bridge"):
            self.check()

    def test_inherited_trellis_python_override_is_pinned_to_bridge(self) -> None:
        path = self.root / self.verifier_path
        binding = "export TRELLIS_PYTHON_CMD=python3"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(binding), 1)
        path.write_text(
            text.replace(binding, "export TRELLIS_PYTHON_CMD=python", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "source-managed Python bridge"):
            self.check()

    def test_secondary_inventory_does_not_depend_on_ast_dump(self) -> None:
        with mock.patch.object(
            ROUTING.ast,
            "dump",
            side_effect=AssertionError("AST serialization is not a stable caller identity"),
        ):
            self.assertEqual(self.check()["status"], "ok")

    def test_new_bare_python_after_seed_fails(self) -> None:
        for launcher in ("python", "python3", "python3.12", "/usr/bin/env python3"):
            with self.subTest(launcher=launcher):
                path = self.root / self.verifier_path
                original = path.read_text()
                path.write_text(original + f"\n{launcher} -c 'print(1)'\n")
                with self.assertRaisesRegex(ROUTING.RoutingError, "bare PATH python"):
                    self.check()
                path.write_text(original)

    def test_new_path_python_shebang_fails(self) -> None:
        path = self.root / self.helper_paths[0]
        path.write_text("#!/usr/bin/env python3\n" + path.read_text())
        with self.assertRaisesRegex(ROUTING.RoutingError, "PATH Python shebang"):
            self.check()

    def test_unregistered_python_subprocess_fails(self) -> None:
        path = self.root / self.helper_paths[1]
        path.write_text(
            path.read_text()
            + "\n\ndef unregistered():\n    return subprocess.run(['python3', '-V'])\n"
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "unmanaged Python subprocess"):
            self.check()

    def test_variable_built_python_subprocess_fails(self) -> None:
        path = self.root / self.helper_paths[1]
        path.write_text(
            path.read_text()
            + "\n\ndef variable_built():\n"
            + "    command = ['python3', '-V']\n"
            + "    return subprocess.run(command)\n"
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "unmanaged Python subprocess"):
            self.check()

    def test_unmanaged_python_subprocess_inside_managed_heredoc_fails(self) -> None:
        self.insert_managed_heredoc('subprocess.run(["python3", "-V"])')
        with self.assertRaisesRegex(ROUTING.RoutingError, "unmanaged Python subprocess"):
            self.check()

    def test_managed_python_subprocess_inside_heredoc_requires_inventory(self) -> None:
        self.insert_managed_heredoc('subprocess.run([sys.executable, "-V"])')
        with self.assertRaisesRegex(ROUTING.RoutingError, "secondary caller inventory drift"):
            self.check()

    def test_registered_managed_python_subprocess_inside_heredoc_passes(self) -> None:
        self.insert_managed_heredoc('subprocess.run([sys.executable, "-V"])')
        self.refresh_secondary_inventory()
        self.assertEqual(self.check()["status"], "ok")

    def test_wrapped_dynamic_sys_executable_launcher_is_discovered(self) -> None:
        path = self.root / self.helper_paths[1]
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n\ndef wrapped_dynamic():\n"
            + '    command = [str(Path(sys.executable)), "-V"]\n'
            + "    return subprocess.run(command)\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            ROUTING.RoutingError, "sys.executable subprocess inventory drift"
        ):
            self.check()
        self.refresh_secondary_inventory()
        self.assertEqual(self.check()["status"], "ok")

    def test_unsupported_sys_executable_expression_fails_closed(self) -> None:
        self.insert_managed_heredoc(
            'subprocess.run([f"{sys.executable}-suffix", "-V"])'
        )
        with self.assertRaisesRegex(
            ROUTING.RoutingError, "unsupported sys.executable launcher expression"
        ):
            self.check()

    def test_unregistered_direct_helper_fails(self) -> None:
        path = self.root / self.verifier_path
        path.write_text(
            path.read_text()
            + '\ninstalled_python "$TARGET" "$REPO_ROOT/trellis/presets/guru-team/scripts/python/verify_installed_extra.py"\n'
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "verifier caller inventory drift"):
            self.check()

    def test_transitive_path_python_shebang_fails(self) -> None:
        path = self.root / self.transitive_paths[1]
        path.write_text("#!/usr/bin/env python3\n" + path.read_text())
        with self.assertRaisesRegex(ROUTING.RoutingError, "PATH Python shebang"):
            self.check()

    def test_transitive_managed_launcher_drift_fails(self) -> None:
        path = self.root / self.transitive_paths[0]
        path.write_text(
            path.read_text().replace(
                'return [sys.executable, command, "--request"',
                'return [command, "--request"',
                1,
            )
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "transitive helper managed launcher drift"):
            self.check()

    def test_transitive_generated_path_shebang_fails(self) -> None:
        path = self.root / self.transitive_paths[0]
        path.write_text(
            path.read_text().replace(
                'MANAGED_PYTHON_SHEBANG = f"#!{Path(sys.executable).resolve()}\\n"',
                'MANAGED_PYTHON_SHEBANG = "#!/usr/bin/env python3\\n"',
                1,
            )
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "PATH Python shebang"):
            self.check()

    def test_direct_managed_generated_shebang_requires_inventory(self) -> None:
        path = self.root / self.helper_paths[0]
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\nwrite_executable(Path('direct.py'), f\"#!{Path(sys.executable).resolve()}\\n\")\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "secondary caller inventory drift"):
            self.check()

    def test_concatenated_path_python_shebang_fails(self) -> None:
        path = self.root / self.helper_paths[0]
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\nwrite_executable(Path('path.py'), '#!' + '/usr/bin/env ' + 'python3\\n')\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            ROUTING.RoutingError, "unmanaged generated Python shebang"
        ):
            self.check()

    def test_shell_wrapper_path_python_fails(self) -> None:
        path = self.root / Path(
            "trellis/workflows/guru-team/scripts/bash/finish-work.sh"
        )
        for launcher in ("python", "python3"):
            with self.subTest(launcher=launcher):
                original = path.read_text()
                path.write_text(original + f"\n{launcher} -V\n")
                with self.assertRaisesRegex(
                    ROUTING.RoutingError, "bare PATH Python in shell helper"
                ):
                    self.check()
                path.write_text(original)

    def test_shell_wrapper_reference_syntaxes_are_discovered(self) -> None:
        path = '"$TARGET/.trellis/guru-team/scripts/bash/check-env.sh"'
        cases = (
            f"{path} --json",
            f"env FOO=1 {path} --json",
            f"command {path} --json",
            f"result=$(env FOO=1 {path} --json)",
            f"WRAPPER={path}\n\"$WRAPPER\" --json",
        )
        for source in cases:
            with self.subTest(source=source):
                rows = ROUTING.discover_referenced_shell_helpers(source)
                self.assertEqual(len(rows), 1)
                self.assertEqual(
                    rows[0]["owner"],
                    "trellis/workflows/guru-team/scripts/bash/check-env.sh",
                )

    def test_shell_helper_fixture_and_assertion_are_not_callers(self) -> None:
        source = (
            "cat >fixture <<'EOF'\n"
            '"$TARGET/.trellis/guru-team/scripts/bash/not-installed.sh"\n'
            "EOF\n"
            'test ! -e "$TARGET/.trellis/guru-team/scripts/bash/removed.sh"\n'
            '! grep -q "old-helper.sh" "$TARGET/.trellis/workflow.md"\n'
        )
        self.assertEqual(ROUTING.discover_referenced_shell_helpers(source), [])

    def test_non_python_command_data_does_not_count_as_python_launcher(self) -> None:
        source = (
            "import subprocess\n"
            'subprocess.run(["git", "commit", "-m", "Document python3 runtime"])\n'
        )
        self.assertEqual(ROUTING.discover_secondary_callers(source, "memory.py"), [])

    def test_nested_preset_shell_wrapper_path_python_fails(self) -> None:
        path = self.root / Path(
            "trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh"
        )
        path.write_text(
            '#!/usr/bin/env bash\npython3 "$SCRIPT_DIR/../python/validate_upstream_ownership.py" "$@"\n',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "bare PATH Python in shell helper"):
            self.check()

    def test_package_shell_routes_are_registered(self) -> None:
        routes = {
            row["id"]: row["route"]
            for row in self.check()["shell_python_helpers"]
        }
        self.assertEqual(
            routes["shell-helper-source-check-dogfood-overlay-drift"],
            [
                "trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh",
                "trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh",
                "trellis/skills/guru-team/runtime/resolve-python.sh",
            ],
        )
        self.assertEqual(
            routes["shell-helper-installed-check-env"],
            [
                "trellis/workflows/guru-team/scripts/bash/check-env.sh",
                "trellis/skills/guru-team/packages/guru-select-workflow-mode/scripts/check-env.sh",
                "trellis/skills/guru-team/runtime/launch.sh",
                "trellis/skills/guru-team/runtime/resolve-python.sh",
            ],
        )
        self.assertEqual(
            routes["shell-helper-installed-version"],
            [
                "trellis/workflows/guru-team/scripts/bash/version.sh",
                "trellis/skills/guru-team/packages/guru-verify-extension-installation/scripts/version.sh",
                "trellis/skills/guru-team/runtime/launch.sh",
                "trellis/skills/guru-team/runtime/resolve-python.sh",
            ],
        )

    def test_package_route_workflow_wrapper_drift_fails(self) -> None:
        for relative in (
            Path("trellis/workflows/guru-team/scripts/bash/check-env.sh"),
            Path("trellis/workflows/guru-team/scripts/bash/version.sh"),
        ):
            with self.subTest(path=relative):
                original = (self.root / relative).read_text(encoding="utf-8")
                (self.root / relative).write_text(
                    original.replace('exec "$TARGET" "$@"', '"$TARGET" "$@"', 1),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ROUTING.RoutingError, "package route drift"):
                    self.check()
                (self.root / relative).write_text(original, encoding="utf-8")

    def test_package_route_wrapper_drift_fails(self) -> None:
        for relative in (
            Path(
                "trellis/skills/guru-team/packages/guru-select-workflow-mode/scripts/check-env.sh"
            ),
            Path(
                "trellis/skills/guru-team/packages/guru-verify-extension-installation/scripts/version.sh"
            ),
        ):
            with self.subTest(path=relative):
                original = (self.root / relative).read_text(encoding="utf-8")
                (self.root / relative).write_text(
                    original.replace('source "$LAUNCHER"', '"$LAUNCHER"', 1),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ROUTING.RoutingError, "package wrapper launcher drift"):
                    self.check()
                (self.root / relative).write_text(original, encoding="utf-8")

    def test_shared_runtime_launcher_drift_fails(self) -> None:
        relative = Path("trellis/skills/guru-team/runtime/launch.sh")
        path = self.root / relative
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                'exec "$SKILLS_ROOT/runtime/resolve-python.sh"',
                '"$SKILLS_ROOT/runtime/resolve-python.sh"',
                1,
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "managed runtime launcher drift"):
            self.check()

    def test_unregistered_shell_wrapper_fails(self) -> None:
        helper = self.root / Path(
            "trellis/workflows/guru-team/scripts/bash/extra-python-hop.sh"
        )
        helper.write_text(
            '#!/usr/bin/env bash\nexec "$RUNTIME_ASSETS/resolve-python.sh" "$@"\n'
        )
        verifier = self.root / self.verifier_path
        verifier.write_text(
            verifier.read_text()
            + '\n"$TARGET/.trellis/guru-team/scripts/bash/extra-python-hop.sh"\n'
        )
        with self.assertRaisesRegex(ROUTING.RoutingError, "shell helper inventory drift"):
            self.check()


if __name__ == "__main__":
    unittest.main()
