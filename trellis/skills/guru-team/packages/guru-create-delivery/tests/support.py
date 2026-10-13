"""Reuse the one installed-upstream fixture; never substitute its model."""
import importlib.util
import sys
from pathlib import Path

KERNEL = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KERNEL))


def installed_fixture(test):
    path = KERNEL / "runtime/delivery_projection/tests/test_installed_projection.py"
    spec = importlib.util.spec_from_file_location("planning_installed_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fixture = module.InstalledProjectionTests("test_uninstalled_dependency_does_not_use_source_fallback")
    fixture.setUp()
    test.addCleanup(fixture.doCleanups)
    return fixture


def owner_module(package, filename="invoke.py"):
    directory = package / "runtime"
    sys.path.insert(0, str(directory))
    sys.modules.pop("common", None)
    spec = importlib.util.spec_from_file_location(package.name.replace("-", "_") + "_" + filename.replace(".", "_"), directory / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
