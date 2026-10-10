"""Replay native continuation from genuinely completed Wording commands.

The executing AI supplies reviewed, actually generated seed results and judges
the resulting transcript. This runner neither authors a gate nor grades it.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from runtime.io import project_intermediate_receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--completed", choices=("checker", "record-check"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    args = parser.parse_args()
    root, evidence = args.root.resolve(), args.evidence.resolve()
    relative = evidence.relative_to(root).as_posix()
    schemas = root / ".trellis/guru-team/skills/schemas"
    project_intermediate_receipt(json.loads((evidence / "checker-stdout.json").read_text()), schemas)
    if args.completed == "record-check":
        project_intermediate_receipt(json.loads((evidence / "recorder-stdout.json").read_text()), schemas)
        completed = "recorder 与 checker 已成功执行，真实 stdout 在 recorder-stdout.json 与 checker-stdout.json。"
    else:
        json.loads((evidence / "owner-result.json").read_text())
        completed = "checker 已成功执行，真实 stdout 在 checker-stdout.json；当前调用保留的 owner result 在 owner-result.json。"
    prompt = (
        "请接续这个业务仓的当前规划 Wording 步骤。" + completed
        + f" public-input.json 是当前 caller input。上述文件都在 {relative}/。公共 invoke 尚未执行。"
        "读取当前安装 Skill、合同、所需 workflow 路由与业务源 docs/source.md，先准确报告已完成的阶段，"
        "再按当前合法合同继续到该 Skill 的正式出口并消费其唯一路由。映射到下一 owner 时读取 entry contract；"
        "本次交付止于该接续边界。保留实际命令及 stdout；不制造产品决定或修改业务文件。"
        "当前执行不涉及 commit、push、PR。"
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
