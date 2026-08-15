from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import owner


def _task_dir(root: Path, value: str | None) -> Path:
    if value:
        raw = Path(value)
        candidates = (raw, root / raw, root / ".trellis/tasks" / raw)
    else:
        process = owner.run([sys.executable, "./.trellis/scripts/task.py", "current"], cwd=root, check=False)
        candidates = (root / process.stdout.strip(),) if process.returncode == 0 and process.stdout.strip() else ()
    for candidate in candidates:
        resolved = candidate if candidate.is_absolute() else root / candidate
        if resolved.is_dir() and not resolved.is_symlink():
            return resolved.resolve()
    raise owner.WorkflowError("Could not resolve current Trellis task.", exit_code=2)


def _repo(root: Path, config: dict) -> str:
    configured = str(config.get("github_repo") or "").strip()
    if configured:
        return configured.casefold()
    process = owner.run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    match = re.search(r"github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?$", process.stdout.strip())
    if not match:
        raise owner.WorkflowError("GitHub repository must be an explicit owner/repository identity.", exit_code=2)
    return f"{match.group(1)}/{match.group(2)}".casefold()


def run(args: argparse.Namespace) -> dict:
    root = owner.repo_root(Path(args.root or Path.cwd()))
    task_dir = _task_dir(root, args.task)
    ledger = json.loads((task_dir / "issue-scope-ledger.json").read_text(encoding="utf-8"))
    primary = int(args.primary_issue or ledger.get("primary_issue", {}).get("number") or 0)
    dispositions = [item.get("number") for bucket in ("close_issues", "related_issues", "followup_issues") for item in ledger.get(bucket, []) if isinstance(item, dict)]
    if primary <= 0 or dispositions.count(primary) != 1:
        raise owner.WorkflowError("Issue Scope Ledger primary issue disposition is invalid.", exit_code=2)
    task = json.loads((task_dir / "task.json").read_text(encoding="utf-8"))
    base = str(args.base_branch or task.get("base_branch") or "").removeprefix("origin/")
    head = str(args.head_branch or owner.run(["git", "branch", "--show-current"], cwd=root).stdout.strip())
    summary = str(args.summary or task.get("title") or task.get("name") or "").strip()
    summary = re.sub(rf"^(?:完成：\s*)?#{primary}\s*", "", summary).strip()
    if not re.search(r"[\u3400-\u9fff]", summary):
        title = next((str(item.get("title") or "") for item in ledger.get("close_issues", []) if item.get("number") == primary), "")
        summary = title if re.search(r"[\u3400-\u9fff]", title) else f"完成 {summary or f'#{primary}'}"
    pull_request = args.pull_request or "<pull_request>"
    expected_head = owner.run(["git", "rev-parse", "HEAD"], cwd=root).stdout.strip()
    subject = f"chore(merge): #{pull_request} 合并 #{primary} {summary}"
    body = f"合并：\n合入 `{head}` 到 `{base}`，保留 PR 内部提交历史。\n\n范围：\n本次 PR 完成 #{primary}：{summary}。\n\n审计：\nTrellis task archive、review gate、finish-summary 和 readiness 提交保留在 PR 分支历史中，用于审计任务过程。\n\nPR: #{pull_request}\nRefs #{primary}\n"
    repo = _repo(root, owner.load_config(root))
    body_hint = args.body_file_hint
    merge = {"ready": bool(args.pull_request and str(args.pull_request).isdigit()), "subject": subject, "body": body, "body_file_hint": body_hint, "expected_head": expected_head, "command": ["gh", "pr", "merge", str(pull_request), "--repo", repo, "--match-head-commit", expected_head, "--merge", "--subject", subject, "--body-file", body_hint], "errors": []}
    return {"status": "ok", "primary_issue": primary, "pull_request": pull_request, "base_branch": base, "head_branch": head, "summary": summary, **merge, "merge_commit": merge}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Format the reviewed task PR merge commit payload.")
    parser.add_argument("--root")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--task")
    parser.add_argument("--primary-issue", type=int)
    parser.add_argument("--pull-request")
    parser.add_argument("--summary")
    parser.add_argument("--head-branch")
    parser.add_argument("--base-branch")
    parser.add_argument("--title", help=argparse.SUPPRESS)
    parser.add_argument("--body-file-hint", default="<merge-body-file>")
    args = parser.parse_args(argv)
    try:
        payload = run(args)
    except (OSError, ValueError, json.JSONDecodeError, owner.WorkflowError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return getattr(exc, "exit_code", 2)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
