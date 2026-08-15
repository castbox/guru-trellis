"""Validate throwaway-verifier Python routing and managed runtime identity."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any


class RoutingError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RoutingError(f"invalid JSON file: {path}") from exc
    if not isinstance(payload, dict):
        raise RoutingError(f"expected JSON object: {path}")
    return payload


def canonical_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def repository_state_root(repo: Path) -> Path:
    marker = repo / ".git"
    if marker.is_dir():
        return marker.resolve() / "guru-team/python"
    if marker.is_file() and not marker.is_symlink():
        text = marker.read_text(encoding="utf-8").strip()
        if not text.startswith("gitdir: "):
            raise RoutingError(f"invalid gitfile: {marker}")
        git_dir = Path(text.removeprefix("gitdir: ").strip())
        if not git_dir.is_absolute():
            git_dir = repo / git_dir
        git_dir = git_dir.resolve()
        common_dir = git_dir
        commondir = git_dir / "commondir"
        if commondir.is_file() and not commondir.is_symlink():
            common_value = commondir.read_text(encoding="utf-8").strip()
            if common_value:
                common_dir = Path(common_value)
                if not common_dir.is_absolute():
                    common_dir = git_dir / common_dir
                common_dir = common_dir.resolve()
        worktree_root = git_dir / "guru-team/python"
        if (worktree_root / "active.json").is_file():
            return worktree_root
        return common_dir / "guru-team/python"
    return repo / ".trellis/.runtime/guru-team/python"


def runtime_checkpoint(
    repo: Path,
    runtime_assets: Path,
    label: str,
    *,
    bootstrap_json: Path | None = None,
) -> dict[str, Any]:
    repo = repo.resolve()
    runtime_assets = runtime_assets.resolve()
    pointer_path = repository_state_root(repo) / "active.json"
    pointer = load_json(pointer_path)
    runtime_id = pointer.get("runtime_id")
    interpreter_text = pointer.get("interpreter")
    if not isinstance(runtime_id, str) or not re.fullmatch(r"[0-9a-f]{24}", runtime_id):
        raise RoutingError(f"{label}: invalid active runtime id")
    if not isinstance(interpreter_text, str):
        raise RoutingError(f"{label}: invalid active interpreter")
    interpreter = Path(interpreter_text)
    expected_suffixes = (
        f"/{runtime_id}/venv/bin/python",
        f"/{runtime_id}/venv/Scripts/python.exe",
    )
    if not any(interpreter.as_posix().endswith(suffix) for suffix in expected_suffixes):
        raise RoutingError(f"{label}: interpreter is outside the active runtime identity")
    try:
        interpreter_stat = interpreter.stat()
    except OSError as exc:
        raise RoutingError(f"{label}: managed interpreter is missing") from exc
    if not stat.S_ISREG(interpreter_stat.st_mode) or not os.access(interpreter, os.X_OK):
        raise RoutingError(f"{label}: managed interpreter is not an executable regular file")

    actual_executable = Path(sys.executable)
    actual_resolved = actual_executable.resolve()
    expected_resolved = interpreter.resolve()
    if actual_resolved != expected_resolved:
        raise RoutingError(
            f"{label}: sys.executable mismatch: {actual_resolved} != {expected_resolved}"
        )

    runtime_root = interpreter.parent.parent.parent
    metadata = load_json(runtime_root / "metadata.json")
    identity = metadata.get("identity")
    if metadata.get("runtime_id") != runtime_id or not isinstance(identity, dict):
        raise RoutingError(f"{label}: runtime metadata identity mismatch")
    if canonical_digest(identity)[:24] != runtime_id:
        raise RoutingError(f"{label}: runtime id does not match metadata identity")

    manifest = load_json(runtime_assets / "python-runtime.json")
    lock_file = manifest.get("lock_file")
    if not isinstance(lock_file, str):
        raise RoutingError(f"{label}: runtime manifest lock_file is invalid")
    lock_path = runtime_assets / lock_file
    try:
        lock_sha256 = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    except OSError as exc:
        raise RoutingError(f"{label}: dependency lock is missing") from exc
    if identity.get("lock_sha256") != lock_sha256:
        raise RoutingError(f"{label}: dependency lock identity mismatch")

    bootstrap_identity: dict[str, Any] | None = None
    if bootstrap_json is not None:
        bootstrap_identity = load_json(bootstrap_json)
        bootstrap_interpreter = bootstrap_identity.get("interpreter")
        if (
            bootstrap_identity.get("runtime_identity") != runtime_id
            or not isinstance(bootstrap_interpreter, str)
            or Path(bootstrap_interpreter).resolve() != expected_resolved
        ):
            raise RoutingError(f"{label}: bootstrap result was not consumed by this runner")

    return {
        "status": "ok",
        "checkpoint": label,
        "repo": str(repo),
        "runtime_id": runtime_id,
        "sys_executable": str(actual_executable),
        "sys_executable_resolved": str(actual_resolved),
        "interpreter": str(interpreter),
        "interpreter_resolved": str(expected_resolved),
        "pointer": str(pointer_path),
        "metadata": str(runtime_root / "metadata.json"),
        "dependency_lock": str(lock_path),
        "dependency_lock_sha256": lock_sha256,
        "bootstrap_consumed": bootstrap_identity is not None,
    }


def parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    return {
        child: node
        for node in ast.walk(tree)
        for child in ast.iter_child_nodes(node)
    }


def lexical_scope(
    node: ast.AST, parents: dict[ast.AST, ast.AST]
) -> ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda | ast.ClassDef:
    current = node
    while current in parents:
        current = parents[current]
        if isinstance(
            current,
            (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef),
        ):
            return current
    if isinstance(current, ast.Module):
        return current
    raise RoutingError("Python caller has no lexical scope")


def lexical_scope_chain(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> list[ast.AST]:
    scopes: list[ast.AST] = []
    current = node
    if isinstance(current, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
        scopes.append(current)
    while current in parents:
        current = parents[current]
        if isinstance(
            current,
            (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef),
        ):
            scopes.append(current)
    scopes.reverse()
    return scopes


def lexical_bindings(
    tree: ast.AST,
    node: ast.AST,
    parents: dict[ast.AST, ast.AST] | None = None,
    assignment_index: dict[
        ast.AST, list[tuple[tuple[int, int], str, ast.AST]]
    ]
    | None = None,
) -> dict[str, ast.AST]:
    known_parents = parent_map(tree) if parents is None else parents
    scopes = lexical_scope_chain(node, known_parents)
    position = (
        getattr(node, "lineno", sys.maxsize),
        getattr(node, "col_offset", sys.maxsize),
    )
    if assignment_index is None:
        assignment_index = lexical_assignment_index(tree, known_parents)
    bindings: dict[str, ast.AST] = {}
    for scope in scopes:
        for candidate_position, name, value in assignment_index.get(scope, []):
            if candidate_position >= position:
                break
            bindings[name] = value
    return bindings


def lexical_assignment_index(
    tree: ast.AST, parents: dict[ast.AST, ast.AST] | None = None
) -> dict[ast.AST, list[tuple[tuple[int, int], str, ast.AST]]]:
    known_parents = parent_map(tree) if parents is None else parents
    assignments: dict[
        ast.AST, list[tuple[tuple[int, int], str, ast.AST]]
    ] = {}
    for candidate in ast.walk(tree):
        if not isinstance(candidate, (ast.Assign, ast.AnnAssign)):
            continue
        if candidate.value is None:
            continue
        scope = lexical_scope(candidate, known_parents)
        candidate_position = (
            getattr(candidate, "lineno", sys.maxsize),
            getattr(candidate, "col_offset", sys.maxsize),
        )
        targets = (
            candidate.targets
            if isinstance(candidate, ast.Assign)
            else [candidate.target]
        )
        for target in targets:
            if isinstance(target, ast.Name):
                assignments.setdefault(scope, []).append(
                    (candidate_position, target.id, candidate.value)
                )
    for rows in assignments.values():
        rows.sort(key=lambda row: (row[0], row[1]))
    return assignments


def python_runtime_aliases(tree: ast.AST) -> dict[str, set[str]]:
    aliases = {"modules": {"sys"}, "executables": set()}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == "sys":
                    aliases["modules"].add(name.asname or name.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "sys":
            for name in node.names:
                if name.name == "executable":
                    aliases["executables"].add(name.asname or name.name)
    return aliases


def is_sys_executable(
    node: ast.AST, aliases: dict[str, set[str]] | None = None
) -> bool:
    known = {"modules": {"sys"}, "executables": set()} if aliases is None else aliases
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id in known["modules"]
        and node.attr == "executable"
    ) or (isinstance(node, ast.Name) and node.id in known["executables"])


def expression_contains_sys_executable(
    node: ast.AST, aliases: dict[str, set[str]] | None = None
) -> bool:
    return any(is_sys_executable(child, aliases) for child in ast.walk(node))


def managed_python_expression(
    node: ast.AST,
    bindings: dict[str, ast.AST],
    resolving: frozenset[str] = frozenset(),
    aliases: dict[str, set[str]] | None = None,
) -> bool:
    if is_sys_executable(node, aliases):
        return True
    if isinstance(node, ast.Name) and node.id in bindings:
        if node.id in resolving:
            raise RoutingError(f"cyclic Python launcher binding: {node.id}")
        return managed_python_expression(
            bindings[node.id], bindings, resolving | {node.id}, aliases
        )
    if isinstance(node, ast.Call) and len(node.args) == 1 and not node.keywords:
        if isinstance(node.func, ast.Name) and node.func.id in {"str", "Path"}:
            return managed_python_expression(node.args[0], bindings, resolving, aliases)
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr == "fspath"
        ):
            return managed_python_expression(node.args[0], bindings, resolving, aliases)
    if (
        isinstance(node, ast.Call)
        and not node.args
        and not node.keywords
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"absolute", "resolve"}
    ):
        return managed_python_expression(node.func.value, bindings, resolving, aliases)
    if expression_contains_sys_executable(node, aliases):
        raise RoutingError(
            "unsupported sys.executable launcher expression: "
            + ast.unparse(node)
        )
    return False


def literal_python_launcher(
    node: ast.AST,
    bindings: dict[str, ast.AST],
    resolving: frozenset[str] = frozenset(),
) -> str | None:
    if isinstance(node, ast.Name) and node.id in bindings:
        if node.id in resolving:
            raise RoutingError(f"cyclic Python launcher binding: {node.id}")
        return literal_python_launcher(
            bindings[node.id], bindings, resolving | {node.id}
        )
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        name = Path(node.value).name.lower()
        if name in {"python", "python3", "python.exe", "python3.exe"} or name.startswith("python3."):
            return node.value
        if re.search(
            r"(?:^|[\s;&|()])(?:[^\s;&|()]*/)?python(?:3(?:\.\d+)?)?(?:\.exe)?(?:\s|$)",
            node.value,
            re.IGNORECASE,
        ):
            return node.value
    if isinstance(node, ast.Call) and node.args:
        is_path_wrapper = isinstance(node.func, ast.Name) and node.func.id == "Path"
        is_which_wrapper = (
            isinstance(node.func, ast.Attribute) and node.func.attr == "which"
        )
        if is_path_wrapper or is_which_wrapper:
            return literal_python_launcher(node.args[0], bindings, resolving)
    static_value = static_string_expression(node, bindings)
    if static_value is not None and static_value != getattr(node, "value", None):
        return literal_python_launcher(ast.Constant(value=static_value), {}, resolving)
    for child in ast.walk(node):
        if child is node:
            continue
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            embedded = literal_python_launcher(child, {}, resolving)
            if embedded is not None:
                return embedded
    return None


def scalar_python_launcher(
    node: ast.AST,
    bindings: dict[str, ast.AST] | None = None,
    runtime_aliases: dict[str, set[str]] | None = None,
) -> str | None:
    known = {} if bindings is None else bindings
    if managed_python_expression(node, known, aliases=runtime_aliases):
        return "sys.executable"
    return literal_python_launcher(node, known)


def sequence_python_launcher(
    node: ast.AST | None,
    bindings: dict[str, ast.AST] | None = None,
    resolving: frozenset[str] = frozenset(),
    runtime_aliases: dict[str, set[str]] | None = None,
) -> str | None:
    if node is None:
        return None
    known = {} if bindings is None else bindings
    if isinstance(node, ast.Name) and node.id in known:
        if node.id in resolving:
            raise RoutingError(f"cyclic Python command binding: {node.id}")
        return sequence_python_launcher(
            known[node.id], known, resolving | {node.id}, runtime_aliases
        )
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_managed_validation_command"
        and len(node.args) == 1
        and not node.keywords
    ):
        return "managed dynamic sys.executable"
    if not isinstance(node, (ast.List, ast.Tuple)) or not node.elts:
        if expression_contains_sys_executable(node, runtime_aliases):
            raise RoutingError(
                "unsupported sys.executable command expression: "
                + ast.unparse(node)
            )
        return None
    launcher = scalar_python_launcher(node.elts[0], known, runtime_aliases)
    if launcher is not None:
        return launcher
    first = static_string_expression(node.elts[0], known)
    if first is not None and Path(first).name in {"sh", "bash"}:
        for index, element in enumerate(node.elts[1:], start=1):
            if static_string_expression(element, known) == "-c" and index + 1 < len(node.elts):
                return scalar_python_launcher(
                    node.elts[index + 1], known, runtime_aliases
                )
    return None


def process_aliases(tree: ast.AST) -> dict[str, set[str]]:
    aliases = {
        "subprocess_modules": {"subprocess"},
        "subprocess_functions": set(),
        "os_modules": {"os"},
        "os_functions": set(),
        "asyncio_modules": {"asyncio"},
        "asyncio_functions": set(),
    }
    subprocess_names = {
        "run", "Popen", "call", "check_call", "check_output",
        "getoutput", "getstatusoutput",
    }
    os_names = {"system", "popen"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == "subprocess":
                    aliases["subprocess_modules"].add(name.asname or name.name)
                elif name.name == "os":
                    aliases["os_modules"].add(name.asname or name.name)
                elif name.name == "asyncio":
                    aliases["asyncio_modules"].add(name.asname or name.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            for name in node.names:
                if name.name in subprocess_names:
                    aliases["subprocess_functions"].add(name.asname or name.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "os":
            for name in node.names:
                if name.name.startswith(("exec", "spawn")) or name.name in os_names:
                    aliases["os_functions"].add(name.asname or name.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "asyncio":
            for name in node.names:
                if name.name.startswith("create_subprocess_"):
                    aliases["asyncio_functions"].add(name.asname or name.name)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)) or node.value is None:
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            source_name = None
            if isinstance(node.value, ast.Attribute) and isinstance(node.value.value, ast.Name):
                if (
                    node.value.value.id in aliases["subprocess_modules"]
                    and node.value.attr in subprocess_names
                ):
                    source_name = "subprocess_functions"
                elif (
                    node.value.value.id in aliases["os_modules"]
                    and (
                        node.value.attr.startswith(("exec", "spawn"))
                        or node.value.attr in os_names
                    )
                ):
                    source_name = "os_functions"
                elif (
                    node.value.value.id in aliases["asyncio_modules"]
                    and node.value.attr.startswith("create_subprocess_")
                ):
                    source_name = "asyncio_functions"
            elif isinstance(node.value, ast.Name):
                for family in (
                    "subprocess_functions", "os_functions", "asyncio_functions"
                ):
                    if node.value.id in aliases[family]:
                        source_name = family
                        break
            if source_name is None:
                continue
            for target in targets:
                if isinstance(target, ast.Name) and target.id not in aliases[source_name]:
                    aliases[source_name].add(target.id)
                    changed = True
    return aliases


def process_command_node(
    call: ast.Call, aliases: dict[str, set[str]]
) -> tuple[bool, ast.AST | None]:
    subprocess_call = (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id in aliases["subprocess_modules"]
        and call.func.attr in {"run", "Popen", "call", "check_call", "check_output"}
    )
    imported_subprocess_call = (
        isinstance(call.func, ast.Name)
        and call.func.id in aliases["subprocess_functions"]
    )
    asyncio_call = (
        (
            isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id in aliases["asyncio_modules"]
            and call.func.attr.startswith("create_subprocess_")
        )
        or (
            isinstance(call.func, ast.Name)
            and call.func.id in aliases["asyncio_functions"]
        )
    )
    local_run_call = (
        isinstance(call.func, ast.Name) and call.func.id in {"run", "run_stdout"}
    )
    delegated_run_call = (
        isinstance(call.func, ast.Attribute)
        and call.func.attr in {"run", "run_stdout"}
    )
    os_process_call = (
        (
            isinstance(call.func, ast.Attribute)
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id in aliases["os_modules"]
            and (
                call.func.attr.startswith(("exec", "spawn"))
                or call.func.attr in {"system", "popen"}
            )
        )
        or (
            isinstance(call.func, ast.Name)
            and call.func.id in aliases["os_functions"]
        )
    )
    if os_process_call:
        name = call.func.attr if isinstance(call.func, ast.Attribute) else call.func.id
        launcher_index = 1 if name.startswith("spawn") else 0
        return True, call.args[launcher_index] if len(call.args) > launcher_index else None
    if not (
        subprocess_call
        or imported_subprocess_call
        or asyncio_call
        or local_run_call
        or delegated_run_call
    ):
        return False, None
    if call.args:
        return True, call.args[0]
    for keyword in call.keywords:
        if keyword.arg in {"args", "command", "executed_command"}:
            return True, keyword.value
    return True, None


def subprocess_python_launcher(
    call: ast.Call,
    bindings: dict[str, ast.AST] | None = None,
    aliases: dict[str, set[str]] | None = None,
    runtime_aliases: dict[str, set[str]] | None = None,
) -> str | None:
    known_aliases = process_aliases(ast.Module(body=[], type_ignores=[])) if aliases is None else aliases
    is_process, command = process_command_node(call, known_aliases)
    if not is_process or command is None:
        return None
    if isinstance(command, (ast.List, ast.Tuple, ast.Name, ast.Call)):
        return sequence_python_launcher(
            command, bindings, runtime_aliases=runtime_aliases
        )
    return scalar_python_launcher(command, bindings, runtime_aliases)


def normalized_shell_anchor(lines: list[str], index: int) -> str:
    parts = [lines[index].strip()]
    cursor = index
    while parts[-1].endswith("\\") and cursor + 1 < len(lines):
        cursor += 1
        parts.append(lines[cursor].strip())
    return " ".join(" ".join(parts).split())


def shell_line_invokes_unmanaged_python(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    return re.search(
        r'(?:^|[;&|()]\s*)'
        r'(?:(?:exec|command)\s+|(?:[^\s;&|()]*/)?env(?:\s+[A-Za-z_][A-Za-z0-9_]*=[^\s]+)*\s+)?'
        r'(?:[^\s;&|()]*/)?python(?:3(?:\.\d+)?)?(?:\.exe)?(?:\s|$)',
        stripped,
        re.IGNORECASE,
    ) is not None


def shell_caller_kind(anchor: str) -> str:
    if "bootstrap.py" in anchor and anchor.startswith("python3 "):
        return "bootstrap_seed"
    if "resolve-python.sh" in anchor or "SOURCE_RUNTIME_RESOLVER" in anchor:
        return "shell_wrapper_second_hop"
    if re.search(r"(?:^| )-c(?: |$)", anchor):
        return "inline_c"
    if re.search(r"(?:^| )-m(?: |$)", anchor):
        return "module"
    if ".py" in anchor:
        return "python_file"
    return "inline_stdin"


def discover_shell_callers(verifier_text: str, owner: str) -> list[dict[str, Any]]:
    lines = verifier_text.splitlines()
    discovered: list[tuple[str, str, str]] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("python3 ") and "runtime/bootstrap.py" in stripped:
            anchor = normalized_shell_anchor(lines, index)
            discovered.append(("bootstrap_seed", "PATH python3", anchor))
            continue
        if stripped.startswith('"$SOURCE_RUNTIME_RESOLVER"'):
            anchor = normalized_shell_anchor(lines, index)
            discovered.append(("source_managed", "source resolve-python.sh", anchor))
            continue
        if stripped.startswith('exec "$SOURCE_RUNTIME_RESOLVER"'):
            anchor = normalized_shell_anchor(lines, index)
            discovered.append(
                ("source_managed", "source python3 PATH bridge", anchor)
            )
            continue
        if stripped.startswith('"$installed_repo/.trellis/guru-team/runtime/resolve-python.sh"'):
            anchor = normalized_shell_anchor(lines, index)
            discovered.append(("installed_managed", "installed resolve-python.sh", anchor))
            continue
        if re.search(r"\bsource_python\b", line) and not re.match(r"\s*source_python\(\)", line):
            anchor = normalized_shell_anchor(lines, index)
            discovered.append(("source_managed", "source_python", anchor))
        if re.search(r"\binstalled_python\b", line) and not re.match(r"\s*installed_python\(\)", line):
            anchor = normalized_shell_anchor(lines, index)
            discovered.append(("installed_managed", "installed_python", anchor))

    rows: list[dict[str, Any]] = []
    seen: dict[tuple[str, str, str], int] = {}
    for classification, launcher, anchor in discovered:
        key = (classification, launcher, anchor)
        ordinal = seen.get(key, 0) + 1
        seen[key] = ordinal
        digest = hashlib.sha256(anchor.encode()).hexdigest()
        suffix = f"-{ordinal}" if ordinal > 1 else ""
        rows.append(
            {
                "id": f"verifier-{classification}-{digest[:12]}{suffix}",
                "owner": owner,
                "kind": shell_caller_kind(anchor),
                "classification": classification,
                "expected_launcher": launcher,
                "anchor_sha256": digest,
                "ordinal": ordinal,
            }
        )
    return rows


def heredoc_body_lines(shell_text: str, owner: str) -> set[int]:
    lines = shell_text.splitlines()
    body_lines: set[int] = set()
    heredoc_pattern = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
    index = 0
    while index < len(lines):
        match = heredoc_pattern.search(lines[index])
        if match is None:
            index += 1
            continue
        delimiter = match.group(2)
        body_start = index + 1
        body_end = body_start
        while body_end < len(lines) and lines[body_end].strip() != delimiter:
            body_end += 1
        if body_end >= len(lines):
            raise RoutingError(f"unterminated heredoc in {owner}: line {index + 1}")
        body_lines.update(range(body_start + 1, body_end + 1))
        index = body_end + 1
    return body_lines


def discover_referenced_shell_helpers(verifier_text: str) -> list[dict[str, str]]:
    path_pattern = re.compile(
        r'["\']?\$(?:\{)?(REPO_ROOT|TARGET)(?:\})?["\']?/'
        r'(trellis/(?:workflows/guru-team|presets/guru-team)/scripts/bash/'
        r'|\.trellis/guru-team/scripts/bash/)'
        r'([^"\'\s/]+\.sh)'
    )
    inline_body_lines = heredoc_body_lines(verifier_text, "throwaway verifier")
    discovered: dict[tuple[str, str], dict[str, str]] = {}
    for number, line in enumerate(verifier_text.splitlines(), start=1):
        if number in inline_body_lines or line.lstrip().startswith("#"):
            continue
        stripped = line.strip()
        if re.match(r"^(?:!\s+)?(?:test|grep|cmp)\b", stripped):
            continue
        for match in path_pattern.finditer(stripped):
            root_name, _, name = match.groups()
            classification = (
                "source_managed" if root_name == "REPO_ROOT" else "installed_managed"
            )
            owner = (
                f"trellis/workflows/guru-team/scripts/bash/{name}"
                if root_name == "TARGET"
                else f"{match.group(2)}{name}"
            )
            discovered[(owner, classification)] = {
                "owner": owner,
                "classification": classification,
            }
    return [discovered[key] for key in sorted(discovered)]


def discover_shell_python_helpers(
    repo_root: Path, verifier_text: str
) -> list[dict[str, Any]]:
    def route_for(owner: str, seen: frozenset[str] = frozenset()) -> list[str]:
        if owner in seen:
            raise RoutingError(f"shell helper route cycle: {owner}")
        source = (repo_root / owner).read_text(encoding="utf-8")
        if any(shell_line_invokes_unmanaged_python(line) for line in source.splitlines()):
            raise RoutingError(f"bare PATH Python in shell helper: {owner}")
        route = [owner]
        if "resolve-python.sh" in source:
            if not re.search(r'exec "\$[^"\n]+/resolve-python\.sh"', source):
                raise RoutingError(f"shell helper managed launcher drift: {owner}")
            return route + ["trellis/skills/guru-team/runtime/resolve-python.sh"]

        package_match = re.search(
            r'skills/guru-team/packages/([^"\n]+/scripts/[^"\n]+\.sh)',
            source,
        )
        if package_match is not None:
            if 'exec "$TARGET" "$@"' not in source:
                raise RoutingError(f"shell helper package route drift: {owner}")
            package_wrapper = (
                "trellis/skills/guru-team/packages/" + package_match.group(1)
            )
            package_source = (repo_root / package_wrapper).read_text(encoding="utf-8")
            if any(
                shell_line_invokes_unmanaged_python(line)
                for line in package_source.splitlines()
            ):
                raise RoutingError(f"bare PATH Python in package wrapper: {package_wrapper}")
            if (
                'source "$LAUNCHER"' not in package_source
                or "runtime/launch.sh" not in package_source
            ):
                raise RoutingError(f"package wrapper launcher drift: {package_wrapper}")
            launcher = "trellis/skills/guru-team/runtime/launch.sh"
            launcher_source = (repo_root / launcher).read_text(encoding="utf-8")
            if (
                any(
                    shell_line_invokes_unmanaged_python(line)
                    for line in launcher_source.splitlines()
                )
                or not re.search(
                    r'exec "\$SKILLS_ROOT/runtime/resolve-python\.sh"',
                    launcher_source,
                )
            ):
                raise RoutingError(f"managed runtime launcher drift: {launcher}")
            return route + [
                package_wrapper,
                launcher,
                "trellis/skills/guru-team/runtime/resolve-python.sh",
            ]

        nested_matches = re.findall(
            r'\$REPO_ROOT/(trellis/(?:workflows/guru-team|presets/guru-team)'
            r'/scripts/bash/[^"\n]+\.sh)',
            source,
        )
        nested = list(dict.fromkeys(nested_matches))
        if len(nested) != 1:
            raise RoutingError(f"shell helper managed route is ambiguous: {owner}")
        return route + route_for(nested[0], seen | {owner})

    discovered: dict[tuple[str, str], dict[str, Any]] = {}
    for reference in discover_referenced_shell_helpers(verifier_text):
        owner = reference["owner"]
        classification = reference["classification"]
        name = Path(owner).name
        route = route_for(owner)
        key = (owner, classification)
        discovered[key] = {
            "id": f"shell-helper-{classification.removesuffix('_managed')}-{name.removesuffix('.sh')}",
            "owner": owner,
            "kind": "shell_wrapper_second_hop",
            "classification": classification,
            "expected_launcher": (
                "source resolve-python.sh"
                if classification == "source_managed"
                else "installed resolve-python.sh"
            ),
            "route": route,
        }
    return [discovered[key] for key in sorted(discovered)]


def expression_uses_name(node: ast.AST, name: str) -> bool:
    return any(isinstance(child, ast.Name) and child.id == name for child in ast.walk(node))


def managed_shebang_names(
    tree: ast.AST, aliases: dict[str, set[str]] | None = None
) -> set[str]:
    names: set[str] = set()
    assignments: list[tuple[list[ast.expr], ast.AST]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            assignments.append((node.targets, node.value))
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            assignments.append(([node.target], node.value))
    changed = True
    while changed:
        changed = False
        for targets, value in assignments:
            binds_sys_executable = (
                any(
                    isinstance(child, ast.Constant)
                    and isinstance(child.value, str)
                    and "#!" in child.value
                    for child in ast.walk(value)
                )
                and expression_contains_sys_executable(value, aliases)
            )
            derives_managed_shebang = binds_sys_executable or any(
                expression_uses_name(value, name) for name in names
            )
            if not derives_managed_shebang:
                continue
            for target in targets:
                if isinstance(target, ast.Name) and target.id not in names:
                    names.add(target.id)
                    changed = True
    return names


def static_string_expression(
    node: ast.AST,
    bindings: dict[str, ast.AST],
    resolving: frozenset[str] = frozenset(),
) -> str | None:
    if isinstance(node, ast.Name) and node.id in bindings:
        if node.id in resolving:
            raise RoutingError(f"cyclic generated-file binding: {node.id}")
        return static_string_expression(
            bindings[node.id], bindings, resolving | {node.id}
        )
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Constant) and isinstance(node.value, bytes):
        try:
            return node.value.decode("utf-8")
        except UnicodeDecodeError:
            return None
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "encode"
        and not node.args
        and not node.keywords
    ):
        return static_string_expression(node.func.value, bindings, resolving)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = static_string_expression(node.left, bindings, resolving)
        right = static_string_expression(node.right, bindings, resolving)
        if left is not None and right is not None:
            return left + right
    if isinstance(node, (ast.List, ast.Tuple)):
        values = [static_string_expression(value, bindings, resolving) for value in node.elts]
        if all(value is not None for value in values):
            return "".join(value for value in values if value is not None)
    if isinstance(node, ast.JoinedStr) and all(
        isinstance(value, ast.Constant) and isinstance(value.value, str)
        for value in node.values
    ):
        return "".join(value.value for value in node.values)
    return None


def expression_contains_shebang_marker(node: ast.AST) -> bool:
    return any(
        isinstance(child, ast.Constant)
        and isinstance(child.value, str)
        and "#!" in child.value
        for child in ast.walk(node)
    )


def process_wrapper_parameters(
    tree: ast.AST, aliases: dict[str, set[str]]
) -> dict[str, tuple[int, str, ast.AST | None]]:
    wrappers: dict[str, tuple[int, str, ast.AST | None]] = {}
    for function in ast.walk(tree):
        if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        positional = [*function.args.posonlyargs, *function.args.args]
        parameters = [*positional, *function.args.kwonlyargs]
        parameter_index = {parameter.arg: index for index, parameter in enumerate(parameters)}
        defaults: dict[str, ast.AST | None] = {
            parameter.arg: None for parameter in parameters
        }
        for parameter, default in zip(
            positional[-len(function.args.defaults):] if function.args.defaults else [],
            function.args.defaults,
        ):
            defaults[parameter.arg] = default
        for parameter, default in zip(function.args.kwonlyargs, function.args.kw_defaults):
            defaults[parameter.arg] = default
        matches: set[tuple[int, str]] = set()
        for node in ast.walk(function):
            if not isinstance(node, ast.Call):
                continue
            is_process, command = process_command_node(node, aliases)
            if is_process and isinstance(command, ast.Name) and command.id in parameter_index:
                matches.add((parameter_index[command.id], command.id))
        if len(matches) == 1:
            index, name = next(iter(matches))
            wrappers[function.name] = (index, name, defaults[name])
    return wrappers


def wrapper_command_node(
    call: ast.Call, wrappers: dict[str, tuple[int, str, ast.AST | None]]
) -> ast.AST | None:
    if isinstance(call.func, ast.Name):
        wrapper_name = call.func.id
    elif isinstance(call.func, ast.Attribute):
        wrapper_name = call.func.attr
    else:
        return None
    if wrapper_name not in wrappers:
        return None
    index, name, default = wrappers[wrapper_name]
    call_index = index - 1 if isinstance(call.func, ast.Attribute) and index > 0 else index
    if len(call.args) > call_index:
        return call.args[call_index]
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return default


def normalized_python_anchor(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node)
    if segment is None:
        raise RoutingError("Python caller has no stable source anchor")
    return " ".join(segment.split())


def discover_secondary_callers(
    source: str,
    owner: str,
    *,
    classification: str = "installed_managed",
    id_namespace: str = "helper",
    anchor_prefix: str = "",
) -> list[dict[str, Any]]:
    tree = ast.parse(source, filename=owner)
    parents = parent_map(tree)
    assignments = lexical_assignment_index(tree, parents)
    aliases = process_aliases(tree)
    runtime_aliases = python_runtime_aliases(tree)
    wrappers = process_wrapper_parameters(tree, aliases)
    shebang_names = managed_shebang_names(tree, runtime_aliases)
    discovered: list[tuple[str, str, str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            bindings = lexical_bindings(tree, node, parents, assignments)
            returned = node.value
            returned_process_call = (
                isinstance(returned, ast.Call)
                and process_command_node(returned, aliases)[0]
            )
            if returned_process_call:
                launcher = None
            elif isinstance(returned, ast.Tuple) and returned.elts:
                launcher = sequence_python_launcher(
                    returned.elts[0], bindings, runtime_aliases=runtime_aliases
                )
            else:
                launcher = sequence_python_launcher(
                    returned, bindings, runtime_aliases=runtime_aliases
                )
            if launcher == "sys.executable":
                anchor = anchor_prefix + normalized_python_anchor(source, node)
                discovered.append(
                    ("python_argv_second_hop", classification, "sys.executable", anchor)
                )
                continue
        if not isinstance(node, ast.Call):
            continue
        bindings = lexical_bindings(tree, node, parents, assignments)
        launcher = subprocess_python_launcher(
            node, bindings, aliases, runtime_aliases
        )
        wrapper_command = wrapper_command_node(node, wrappers)
        if launcher is None and wrapper_command is not None:
            launcher = sequence_python_launcher(
                wrapper_command, bindings, runtime_aliases=runtime_aliases
            )
        if launcher in {"sys.executable", "managed dynamic sys.executable"}:
            anchor = anchor_prefix + normalized_python_anchor(source, node)
            discovered.append(
                (
                    "dynamic_python_subprocess_second_hop"
                    if launcher == "managed dynamic sys.executable"
                    else "python_subprocess_second_hop",
                    classification,
                    launcher,
                    anchor,
                )
            )
        elif launcher is not None:
            raise RoutingError(f"unmanaged Python subprocess in {owner}: {launcher}")
        if isinstance(node.func, ast.Name) and node.func.id == "write_executable":
            content = node.args[1] if len(node.args) > 1 else None
        elif (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in aliases["os_modules"]
            and node.func.attr == "write"
        ):
            content = node.args[1] if len(node.args) > 1 else None
        elif isinstance(node.func, ast.Attribute) and node.func.attr in {
            "write_text",
            "write_bytes",
            "write",
            "writelines",
        }:
            content = node.args[0] if node.args else next(
                (
                    keyword.value
                    for keyword in node.keywords
                    if keyword.arg in {"data", "s", "text", "content"}
                ),
                None,
            )
        elif (
            isinstance(node.func, ast.Name)
            and node.func.id == "print"
            and any(keyword.arg == "file" for keyword in node.keywords)
        ):
            content = ast.List(elts=list(node.args), ctx=ast.Load())
        else:
            content = None
        static_content = (
            static_string_expression(content, bindings) if content is not None else None
        )
        if static_content is not None and re.search(
            r"(?m)^#![^\n]*\bpython(?:3(?:\.\d+)?)?\b", static_content
        ):
            raise RoutingError(f"unmanaged generated Python shebang in {owner}")
        managed_shebang = content is not None and (
            (
                expression_contains_shebang_marker(content)
                and expression_contains_sys_executable(content, runtime_aliases)
            )
            or any(expression_uses_name(content, name) for name in shebang_names)
        )
        if managed_shebang:
            anchor = anchor_prefix + normalized_python_anchor(source, node)
            discovered.append(
                ("generated_shebang", classification, "sys.executable resolved shebang", anchor)
            )

    rows = []
    seen: dict[tuple[str, str, str, str], int] = {}
    for kind, classification, launcher, anchor in discovered:
        key = (kind, classification, launcher, anchor)
        ordinal = seen.get(key, 0) + 1
        seen[key] = ordinal
        digest = hashlib.sha256(anchor.encode()).hexdigest()
        suffix = f"-{ordinal}" if ordinal > 1 else ""
        rows.append(
            {
                "id": f"{id_namespace}-{kind}-{digest[:12]}{suffix}",
                "owner": owner,
                "kind": kind,
                "classification": classification,
                "expected_launcher": launcher,
                "anchor_sha256": digest,
                "ordinal": ordinal,
            }
        )
    return rows


def discover_inline_python_blocks(
    verifier_text: str, owner: str
) -> list[dict[str, Any]]:
    lines = verifier_text.splitlines()
    blocks: list[dict[str, Any]] = []
    index = 0
    heredoc_pattern = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
    while index < len(lines):
        match = heredoc_pattern.search(lines[index])
        if match is None:
            index += 1
            continue
        start = index
        while start > 0 and lines[start - 1].rstrip().endswith("\\"):
            start -= 1
        command = " ".join(" ".join(lines[start : index + 1]).split())
        classification = None
        if re.search(r"\bsource_python\b", command):
            classification = "source_managed"
        elif re.search(r"\binstalled_python\b", command):
            classification = "installed_managed"
        delimiter = match.group(2)
        body_start = index + 1
        body_end = body_start
        while body_end < len(lines) and lines[body_end].strip() != delimiter:
            body_end += 1
        if body_end >= len(lines):
            raise RoutingError(f"unterminated heredoc in {owner}: line {index + 1}")
        if classification is not None:
            blocks.append(
                {
                    "command": command,
                    "classification": classification,
                    "body": "\n".join(lines[body_start:body_end]) + "\n",
                    "line": index + 1,
                    "body_start_line": body_start + 1,
                    "body_end_line": body_end,
                }
            )
        index = body_end + 1
    return blocks


def discover_inline_secondary_callers(
    verifier_text: str, owner: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for block in discover_inline_python_blocks(verifier_text, owner):
        rows.extend(
            discover_secondary_callers(
                block["body"],
                owner,
                classification=block["classification"],
                id_namespace="verifier-inline",
                anchor_prefix=block["command"] + " ",
            )
        )
    return rows


def discover_nested_verifier_entries(
    source: str,
    owner: str,
) -> list[dict[str, Any]]:
    tree = ast.parse(source, filename=owner)
    parents = parent_map(tree)
    assignments = lexical_assignment_index(tree, parents)
    rows: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        if not (
            isinstance(node.func, ast.Name)
            and node.func.id == "run"
            and isinstance(node.args[0], (ast.List, ast.Tuple))
            and node.args[0].elts
        ):
            continue
        first = node.args[0].elts[0]
        if not (
            isinstance(first, ast.Call)
            and isinstance(first.func, ast.Name)
            and first.func.id == "str"
            and len(first.args) == 1
            and isinstance(first.args[0], ast.Name)
        ):
            continue
        bindings = lexical_bindings(tree, node, parents, assignments)
        binding = bindings.get(first.args[0].id)
        if binding is None or not any(
            isinstance(child, ast.Constant)
            and child.value == "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh"
            for child in ast.walk(binding)
        ):
            continue
        anchor = owner + " " + normalized_python_anchor(source, node)
        digest = hashlib.sha256(anchor.encode()).hexdigest()
        rows.append(
            {
                "id": f"nested-verifier-entry-{digest[:12]}",
                "owner": owner,
                "kind": "nested_verifier_entry",
                "classification": "child_bootstrap_seed",
                "expected_launcher": "verify-throwaway-install.sh",
                "anchor_sha256": digest,
                "ordinal": 1,
                "route": [
                    owner,
                    "trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh",
                ],
            }
        )
    return rows


def discover_package_runtime_closure(
    repo_root: Path, closure: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    root_text = closure.get("root")
    pattern = closure.get("glob")
    classification = closure.get("classification")
    expected_launcher = closure.get("expected_launcher")
    if (
        not isinstance(root_text, str)
        or not isinstance(pattern, str)
        or classification != "installed_managed"
        or expected_launcher != "sys.executable"
    ):
        raise RoutingError("package runtime closure contract is invalid")
    root = repo_root / root_text
    if not root.is_dir() or root.is_symlink():
        raise RoutingError("package runtime closure root is unavailable")
    paths = sorted(path for path in root.glob(pattern) if path.is_file())
    if not paths:
        raise RoutingError("package runtime closure contains no Python files")

    secondary: list[dict[str, Any]] = []
    nested_verifiers: list[dict[str, Any]] = []
    scanned: list[str] = []
    for path in paths:
        if path.is_symlink():
            raise RoutingError(f"package runtime Python file is a symlink: {path}")
        relative = path.relative_to(repo_root).as_posix()
        source = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^#!.*\bpython(?:3(?:\.\d+)?)?\b", source):
            raise RoutingError(f"PATH Python shebang in package runtime: {relative}")
        scanned.append(relative)
        secondary.extend(
            discover_secondary_callers(
                source,
                relative,
                classification=classification,
                id_namespace="package-runtime",
                anchor_prefix=relative + " ",
            )
        )
        nested_verifiers.extend(discover_nested_verifier_entries(source, relative))
    return (
        {
            "root": root_text,
            "glob": pattern,
            "classification": classification,
            "expected_launcher": expected_launcher,
            "python_files": scanned,
            "python_file_count": len(scanned),
            "secondary_caller_count": len(secondary),
            "nested_verifier_count": len(nested_verifiers),
        },
        secondary,
        nested_verifiers,
    )


def check_inventory(repo_root: Path, inventory_path: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    inventory = load_json(inventory_path)
    if inventory.get("schema_version") != "1.0":
        raise RoutingError("caller inventory schema_version must be 1.0")
    verifier_spec = inventory.get("verifier")
    package_runtime_spec = inventory.get("package_runtime_closure")
    registered_nested_verifiers = inventory.get("nested_verifier_entries")
    helpers = inventory.get("python_helpers")
    transitive_helpers = inventory.get("transitive_python_helpers")
    registered_shell_helpers = inventory.get("shell_python_helpers")
    registered_callers = inventory.get("callers")
    registered_secondary = inventory.get("secondary_callers")
    if (
        not isinstance(verifier_spec, dict)
        or not isinstance(package_runtime_spec, dict)
        or not isinstance(registered_nested_verifiers, list)
        or not isinstance(helpers, list)
        or not isinstance(transitive_helpers, list)
        or not isinstance(registered_shell_helpers, list)
        or not isinstance(registered_callers, list)
        or not isinstance(registered_secondary, list)
    ):
        raise RoutingError("caller inventory structure is invalid")

    verifier = repo_root / str(verifier_spec.get("path", ""))
    text = verifier.read_text(encoding="utf-8")
    seed_pattern = re.compile(
        r"(?m)^python3 \"\$REPO_ROOT/trellis/skills/guru-team/runtime/bootstrap\.py\" \\\n"
    )
    if len(seed_pattern.findall(text)) != 1:
        raise RoutingError("verifier must contain exactly one bootstrap_seed")
    seed_match = seed_pattern.search(text)
    assert seed_match is not None
    seed_line = text[: seed_match.start()].count("\n") + 1
    seed_end = text.find('> "$WORK_DIR/source-managed-runtime.json"', seed_match.end())
    if seed_end < 0:
        raise RoutingError("bootstrap_seed output is not source-managed-runtime.json")
    seed_end_line = text[:seed_end].count("\n") + 1
    poison_token = ': >"$GURU_TEAM_VERIFY_PATH_PYTHON_POISON_FILE"'
    poison_offset = text.find(poison_token, seed_end)
    bridge_assignment = 'PYTHON_BRIDGE_DIR="$WORK_DIR/source-managed-python-path"'
    bridge_assignment_offset = text.find(bridge_assignment, seed_end)
    bridge_start = 'cat >"$PYTHON_BRIDGE_DIR/python3" <<EOF'
    bridge_start_offset = text.find(bridge_start, seed_end)
    bridge_exec = (
        'exec "$SOURCE_RUNTIME_RESOLVER" "$REPO_ROOT" '
        '"$SOURCE_RUNTIME_ASSETS" "\\$@"'
    )
    bridge_exec_offset = text.find(bridge_exec, seed_end)
    bridge_chmod = 'chmod +x "$PYTHON_BRIDGE_DIR/python3"'
    bridge_chmod_offset = text.find(bridge_chmod, seed_end)
    bridge_path_export = 'export PATH="$PYTHON_BRIDGE_DIR:$PATH"'
    bridge_path_export_offset = text.find(bridge_path_export, seed_end)
    trellis_python_binding = "export TRELLIS_PYTHON_CMD=python3"
    trellis_python_binding_offset = text.find(trellis_python_binding, seed_end)
    bootstrap_consumer = 'source_python "$PYTHON_ROUTING_HELPER" checkpoint'
    consumer_offset = text.find(bootstrap_consumer, seed_end)
    first_trellis_call_offset = text.find("trellis init ", seed_end)
    if (
        poison_offset < 0
        or bridge_assignment_offset < 0
        or bridge_start_offset < 0
        or bridge_exec_offset < 0
        or bridge_chmod_offset < 0
        or bridge_path_export_offset < 0
        or trellis_python_binding_offset < 0
        or consumer_offset < 0
        or first_trellis_call_offset < 0
        or not (
            seed_end
            < poison_offset
            < bridge_assignment_offset
            < bridge_start_offset
            < bridge_exec_offset
            < bridge_chmod_offset
            < bridge_path_export_offset
            < trellis_python_binding_offset
            < consumer_offset
            < first_trellis_call_offset
        )
    ):
        raise RoutingError(
            "PATH Python poison and source-managed Python bridge must follow bootstrap "
            "and precede source-managed consumption and every Trellis call"
        )
    poison_line = text[:poison_offset].count("\n") + 1
    bridge_line = text[:bridge_start_offset].count("\n") + 1
    trellis_python_binding_line = text[:trellis_python_binding_offset].count("\n") + 1
    inline_body_lines = {
        number
        for block in discover_inline_python_blocks(text, str(verifier))
        for number in range(block["body_start_line"], block["body_end_line"] + 1)
    }
    allowed_bridge_mentions = {
        bridge_line,
        text[:bridge_chmod_offset].count("\n") + 1,
        trellis_python_binding_line,
    }
    bare_after_seed = [
        number
        for number, line in enumerate(text.splitlines(), start=1)
        if number > seed_end_line
        and number not in inline_body_lines
        and number not in allowed_bridge_mentions
        and shell_line_invokes_unmanaged_python(line)
    ]
    if bare_after_seed:
        raise RoutingError(f"bare PATH python after bootstrap: lines {bare_after_seed}")
    if re.search(r"#!\s*/usr/bin/env\s+python(?:3(?:\.\d+)?)?\b", text):
        raise RoutingError("verifier generates or embeds a PATH Python shebang")

    verifier_relative = str(verifier_spec.get("path"))
    discovered_callers = discover_shell_callers(text, verifier_relative)
    if discovered_callers != registered_callers:
        registered_ids = {
            row.get("id") for row in registered_callers if isinstance(row, dict)
        }
        discovered_ids = {row["id"] for row in discovered_callers}
        raise RoutingError(
            "verifier caller inventory drift: "
            f"missing={sorted(discovered_ids - registered_ids)} "
            f"stale={sorted(registered_ids - discovered_ids)}"
        )

    discovered_shell_helpers = discover_shell_python_helpers(repo_root, text)
    if discovered_shell_helpers != registered_shell_helpers:
        registered_ids = {
            row.get("id") for row in registered_shell_helpers if isinstance(row, dict)
        }
        discovered_ids = {row["id"] for row in discovered_shell_helpers}
        raise RoutingError(
            "shell helper inventory drift: "
            f"missing={sorted(discovered_ids - registered_ids)} "
            f"stale={sorted(registered_ids - discovered_ids)}"
        )

    source_calls = [
        number for number, line in enumerate(text.splitlines(), start=1)
        if re.search(r"\bsource_python\b", line) and not re.match(r"\s*source_python\(\)", line)
    ]
    installed_calls = [
        number for number, line in enumerate(text.splitlines(), start=1)
        if re.search(r"\binstalled_python\b", line) and not re.match(r"\s*installed_python\(\)", line)
    ]
    if not source_calls or not installed_calls:
        raise RoutingError("verifier must exercise both source and installed managed runners")

    expected_helper_paths = set()
    helper_facts = []
    discovered_secondary = discover_inline_secondary_callers(text, verifier_relative)
    for row in [*helpers, *transitive_helpers]:
        if not isinstance(row, dict):
            raise RoutingError("python helper inventory row must be an object")
        path_text = row.get("path")
        if not isinstance(path_text, str) or path_text in expected_helper_paths:
            raise RoutingError("python helper inventory contains a missing or duplicate path")
        expected_helper_paths.add(path_text)
        path = repo_root / path_text
        source = path.read_text(encoding="utf-8")
        if source.startswith("#!") or "#!/usr/bin/env python3" in source:
            raise RoutingError(f"PATH Python shebang is forbidden: {path_text}")
        if row in helpers:
            direct_token = f'installed_python "$TARGET" "$REPO_ROOT/{path_text}"'
            if direct_token not in text:
                raise RoutingError(f"registered helper is not launched by installed_python: {path_text}")
        else:
            launch_owner = row.get("launch_owner")
            launch_token = row.get("launch_token")
            if not isinstance(launch_owner, str) or not isinstance(launch_token, str):
                raise RoutingError(f"transitive helper launch contract is invalid: {path_text}")
            launch_source = (repo_root / launch_owner).read_text(encoding="utf-8")
            if launch_token not in launch_source:
                raise RoutingError(f"transitive helper managed launcher drift: {path_text}")
        tree = ast.parse(source, filename=path_text)
        helper_secondary = discover_secondary_callers(source, path_text)
        sys_executable_calls = sum(
            row["kind"] == "python_subprocess_second_hop"
            for row in helper_secondary
        )
        expected_sys_calls = row.get("sys_executable_subprocesses")
        if sys_executable_calls != expected_sys_calls:
            raise RoutingError(
                f"sys.executable subprocess inventory drift in {path_text}: "
                f"{sys_executable_calls} != {expected_sys_calls}"
            )
        expected_bindings = row.get("managed_shebang_bindings")
        actual_bindings = len(
            managed_shebang_names(tree, python_runtime_aliases(tree))
        )
        if actual_bindings != expected_bindings:
            raise RoutingError(
                f"managed shebang inventory drift in {path_text}: "
                f"{actual_bindings} != {expected_bindings}"
            )
        helper_facts.append(
            {
                "id": row.get("id"),
                "path": path_text,
                "classification": "installed_managed",
                "launcher": row.get("expected_launcher"),
                "sys_executable_subprocesses": sys_executable_calls,
                "managed_shebang_bindings": actual_bindings,
            }
        )
        discovered_secondary.extend(helper_secondary)

    package_runtime_closure, package_runtime_secondary, nested_verifier_entries = (
        discover_package_runtime_closure(repo_root, package_runtime_spec)
    )
    discovered_secondary.extend(package_runtime_secondary)
    if nested_verifier_entries != registered_nested_verifiers:
        registered_ids = {
            row.get("id") for row in registered_nested_verifiers if isinstance(row, dict)
        }
        discovered_ids = {row["id"] for row in nested_verifier_entries}
        raise RoutingError(
            "nested verifier inventory drift: "
            f"missing={sorted(discovered_ids - registered_ids)} "
            f"stale={sorted(registered_ids - discovered_ids)}"
        )

    if discovered_secondary != registered_secondary:
        registered_ids = {
            row.get("id") for row in registered_secondary if isinstance(row, dict)
        }
        discovered_ids = {row["id"] for row in discovered_secondary}
        raise RoutingError(
            "secondary caller inventory drift: "
            f"missing={sorted(discovered_ids - registered_ids)} "
            f"stale={sorted(registered_ids - discovered_ids)}"
        )

    discovered_helpers = {
        match.group(1)
        for match in re.finditer(
            r'installed_python \"\$TARGET\" \"\$REPO_ROOT/([^\"]+\.py)\"', text
        )
        if match.group(1).startswith("trellis/presets/guru-team/scripts/python/verify_installed_")
    }
    expected_direct_helper_paths = {str(row.get("path")) for row in helpers}
    if discovered_helpers != expected_direct_helper_paths:
        raise RoutingError(
            "direct helper inventory drift: "
            f"registered={sorted(expected_direct_helper_paths)} discovered={sorted(discovered_helpers)}"
        )

    return {
        "status": "ok",
        "inventory": str(inventory_path.resolve()),
        "bootstrap_seed": {"count": 1, "line": seed_line},
        "poison_activation": {"count": 1, "line": poison_line},
        "trellis_python_path_bridge": {
            "count": 1,
            "line": bridge_line,
            "trellis_python_cmd": "python3",
            "trellis_python_cmd_line": trellis_python_binding_line,
        },
        "callers": discovered_callers,
        "source_managed_calls": source_calls,
        "installed_managed_calls": installed_calls,
        "python_helpers": helper_facts,
        "shell_python_helpers": discovered_shell_helpers,
        "package_runtime_closure": package_runtime_closure,
        "nested_verifier_entries": nested_verifier_entries,
        "secondary_callers": discovered_secondary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    checkpoint_parser = subparsers.add_parser("checkpoint")
    checkpoint_parser.add_argument("--repo", required=True)
    checkpoint_parser.add_argument("--runtime-assets", required=True)
    checkpoint_parser.add_argument("--label", required=True)
    checkpoint_parser.add_argument("--bootstrap-json")
    checkpoint_parser.add_argument("--json", action="store_true")
    inventory_parser = subparsers.add_parser("check-inventory")
    inventory_parser.add_argument("--repo-root", required=True)
    inventory_parser.add_argument("--inventory", required=True)
    inventory_parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "checkpoint":
            result = runtime_checkpoint(
                Path(args.repo),
                Path(args.runtime_assets),
                args.label,
                bootstrap_json=Path(args.bootstrap_json) if args.bootstrap_json else None,
            )
        else:
            result = check_inventory(Path(args.repo_root), Path(args.inventory))
    except (OSError, RoutingError, SyntaxError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
