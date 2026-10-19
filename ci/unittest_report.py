"""Run target-owned unittest assertions and retain machine-readable outcomes."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import unittest


class Result(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outcomes = []

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.outcomes.append({"id": test.id(), "kind": "failure", "message": str(err[1])})

    def addError(self, test, err):
        super().addError(test, err)
        self.outcomes.append({"id": test.id(), "kind": "error", "message": str(err[1])})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.outcomes.append({"id": test.id(), "kind": "skip", "message": reason})

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.outcomes.append({"id": subtest.id(),
                                  "kind": "failure" if isinstance(err[1], test.failureException) else "error",
                                  "message": str(err[1])})


def load_selection(loader, selection, root):
    filename, separator, name = selection.partition("::")
    if separator:
        path = Path(filename)
        if not path.is_absolute():
            path = path.resolve() if path.is_file() else root / path
        # Keep the real module name so existing exact failure IDs still match.
        try:
            spec = importlib.util.spec_from_file_location(path.stem, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[path.stem] = module
            sys.path.insert(0, str(path.parent))
            spec.loader.exec_module(module)
            return loader.loadTestsFromName(name, module)
        except Exception as exc:
            def import_error(error=exc):
                raise error
            return unittest.TestSuite([unittest.FunctionTestCase(import_error)])
    if selection.endswith(".py"):
        path = Path(selection)
        if not path.is_absolute():
            path = path.resolve() if path.is_file() else root / path
        return loader.discover(str(path.parent), pattern=path.name)
    return loader.loadTestsFromName(selection)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("tests", nargs="+")
    args = parser.parse_args()
    sys.path.insert(0, str(args.root))
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for selection in args.tests:
        suite.addTests(load_selection(loader, selection, args.root))
    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
    report = {"tests_run": result.testsRun, "failures": len(result.failures),
              "errors": len(result.errors), "skips": len(result.skipped),
              "expected_failures": len(result.expectedFailures),
              "unexpected_successes": len(result.unexpectedSuccesses),
              "outcomes": result.outcomes}
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0 if (result.wasSuccessful() and result.testsRun and not result.skipped
                 and not result.expectedFailures) else 1


if __name__ == "__main__":
    sys.exit(main())
