"""Replay native continuation from actual Readiness command facts.

The executing AI supplies reviewed, actually generated seed results and judges
the resulting transcript. This runner neither authors a gate nor grades it.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--completed", choices=(
        "readiness-error", "readiness-missing",
    ), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    args = parser.parse_args()
    root, evidence = args.root.resolve(), args.evidence.resolve()
    relative = evidence.relative_to(root).as_posix()
    inputs = {name: json.loads((evidence / name).read_text()) for name in (
        "source.json", "public-input.json", "owner-result.json", "producer-output.json",
    )}
    profile = inputs["public-input.json"]["profile"]
    (evidence / "initial-error.txt").read_text()
    prompt = (
        f"请接续当前 {profile} 的 Readiness 调用。"
        + f"实际 source、caller input、失败 consumer owner result、最后实际 producer 公共输出和命令错误都在 {relative}/，"
        "分别是 source.json、public-input.json、owner-result.json、producer-output.json 和 initial-error.txt。"
        "业务源在 docs/source.md。读取当前安装 Skill、合同和所需路由，准确说明当前可用事实，"
        "独立完成当前适用的 readiness 语义审查，并按合法合同恢复或如实停止。保留实际命令及 stdout；"
        "到达正式出口后读取唯一下一 owner 的 entry contract，本次交付止于该接续边界。"
        "同范围的 consumer 参数修正由你接续；不要修改 producer 输出或业务源，"
        "不要创建 Issue、Task、branch、worktree，不执行 commit、push、PR。"
    )
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "prompt.txt").write_text(prompt)
    argv = [args.codex, "exec", "--ignore-user-config", "--ephemeral", "--json",
            "-C", str(root), "-s", "workspace-write", "-o", str(args.output / "final.txt"), "-"]
    with (args.output / "transcript.jsonl").open("w") as stdout, (args.output / "stderr.log").open("w") as stderr:
        process = subprocess.run(argv, input=prompt, text=True, stdout=stdout, stderr=stderr)
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
