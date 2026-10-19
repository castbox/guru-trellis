"""Native Bash and stdin transport for the declared bootstrap wrapper fixture."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def native_bash() -> Path:
    if os.name != "nt":
        executable = shutil.which("bash")
        if not executable:
            raise ValueError("Bash is required for the public wrapper runtime check.")
        return Path(executable).resolve()

    candidates = []
    git = shutil.which("git")
    if git:
        for parent in Path(git).resolve().parents:
            candidates.append(parent / "bin/bash.exe")
    for name in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
        root = os.environ.get(name)
        if root:
            candidates.append(Path(root) / ("Programs/Git/bin/bash.exe" if name == "LOCALAPPDATA" else "Git/bin/bash.exe"))
    for candidate in dict.fromkeys(candidates):
        if not candidate.is_file():
            continue
        result = subprocess.run(
            [str(candidate), "-c", "uname -s"], text=True, encoding="utf-8",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if result.returncode == 0 and result.stdout.strip().startswith(("MINGW", "MSYS")):
            return candidate.resolve()
    raise ValueError("Git for Windows Bash (MINGW/MSYS) is required for the public wrapper runtime check.")


def wrapper_call(bash: Path, wrapper: Path, arguments: list[str]) -> tuple[list[str], str | None]:
    """Carry the fixed manifest invocation unchanged through the stdin API."""
    arguments = list(arguments)
    payload = None
    if "--invocation" in arguments:
        index = arguments.index("--invocation") + 1
        payload = arguments[index]
        arguments[index] = "-"
    return [str(bash), wrapper.as_posix(), *arguments], payload
