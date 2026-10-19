"""LF policy for declared Guru text, with exact previous-byte recovery."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

START = b"# guru-team-managed-text:start"
END = b"# guru-team-managed-text:end"
TEXT_SUFFIXES = frozenset({".md", ".py", ".sh", ".json", ".yml", ".yaml", ".toml", ".txt"})


def declared_text(path: Path) -> bool:
    return path.suffix in TEXT_SUFFIXES and path.name not in {"extension.json", "trellis-source.json"}


def canonical_bytes(source: Path) -> bytes:
    content = source.read_bytes()
    return content.replace(b"\r\n", b"\n") if declared_text(source) else content


def equivalent_lf(current: bytes, source: Path, previous_hash: str | None = None) -> bytes:
    """Return LF only when canonical or a recorded managed preimage proves it."""
    if not declared_text(source) or b"\r\n" not in current:
        return current
    normalized = current.replace(b"\r\n", b"\n")
    if normalized == canonical_bytes(source) or (
        previous_hash and hashlib.sha256(normalized).hexdigest() == previous_hash
    ):
        return normalized
    return current


def policy_patterns(paths: set[Path]) -> list[str]:
    patterns: set[str] = set()
    for path in paths:
        if not declared_text(path):
            # Exact identity and lock files retain raw checkout bytes.
            patterns.add(f"/{path.as_posix()} -text")
            continue
        parts = path.parts
        if parts[:2] == (".trellis", "guru-team"):
            pattern = f"/.trellis/guru-team/**/*{path.suffix}"
        elif "skills" in parts and any(part.startswith("guru-") for part in parts):
            index = next(i for i, part in enumerate(parts) if part.startswith("guru-"))
            pattern = "/" + "/".join(parts[:index]) + f"/guru-*/**/*{path.suffix}"
        else:
            pattern = "/" + path.as_posix()
        patterns.add(f"{pattern} text eol=lf")
    # Exceptions follow namespace patterns so Git applies their raw-byte rule.
    return sorted(p for p in patterns if not p.endswith(" -text")) + sorted(
        p for p in patterns if p.endswith(" -text")
    )


def render_attributes(original: bytes, paths: set[Path]) -> bytes:
    lines = original.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if START in line]
    ends = [i for i, line in enumerate(lines) if END in line]
    block = START + b"\n" + "\n".join(policy_patterns(paths)).encode("utf-8") + b"\n" + END + b"\n"
    if not starts and not ends:
        return original + (b"\n" if original and not original.endswith(b"\n") else b"") + block
    if (len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]
            or lines[starts[0]].rstrip(b"\r\n") != START
            or lines[ends[0]].rstrip(b"\r\n") != END):
        raise SystemExit("managed_text_attributes_conflict: malformed Guru .gitattributes block")
    return b"".join(lines[:starts[0]]) + block + b"".join(lines[ends[0] + 1:])


def prepare_attributes(repo: Path, staging: Path, paths: set[Path]) -> dict[str, str]:
    """Check staged attributes using the target's real Git/config/info rules."""
    target = repo / ".gitattributes"
    if target.is_symlink() or (staging / ".gitattributes").is_symlink():
        raise SystemExit("managed_text_attributes_conflict: .gitattributes must be a regular file")
    original = target.read_bytes() if target.exists() else b""
    updated = render_attributes(original, paths)
    (staging / ".gitattributes").write_bytes(updated)
    # A deeper attributes file has precedence over the root managed block.
    ancestors = {parent / ".gitattributes" for path in paths for parent in path.parents if parent != Path(".")}
    for relative in ancestors:
        source = repo / relative
        if source.is_file():
            destination = staging / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    gitdir = subprocess.run(["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"], capture_output=True)
    if gitdir.returncode == 0:
        command = ["git", "--git-dir", gitdir.stdout.decode("utf-8").strip(), "--work-tree", str(staging),
                   "check-attr", "-z", "--stdin", "text", "eol"]
        completed = subprocess.run(command, input=b"\0".join(p.as_posix().encode("utf-8") for p in sorted(paths)) + b"\0", capture_output=True)
        if completed.returncode:
            raise SystemExit("managed_text_attributes_conflict: " + completed.stderr.decode("utf-8"))
        fields = completed.stdout.split(b"\0")
        for i in range(0, len(fields) - 1, 3):
            path, attribute, value = fields[i:i + 3]
            text = declared_text(Path(path.decode("utf-8")))
            expected = b"set" if attribute == b"text" and text else b"lf" if text else b"unset"
            if (text or attribute == b"text") and value != expected:
                raise SystemExit("managed_text_attributes_conflict: " + path.decode("utf-8") + " " + attribute.decode() + "=" + value.decode())
    return {"path": ".gitattributes", "action": "unchanged" if original == updated else "updated_managed"}
