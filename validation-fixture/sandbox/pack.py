"""#154 隔离验证使用的当前 pack CLI。"""

import argparse
import sys
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(prog="pack", description="构建本地包。")
    parser.add_argument("--output", metavar="DIR", default="dist", help=argparse.SUPPRESS)
    return parser


def build(output):
    target = Path(output)
    if target.exists():
        raise FileExistsError(f"目标已存在：{target}")
    target.mkdir(parents=True)
    (target / "package.txt").write_text("package\n", encoding="utf-8")
    return target


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        target = build(args.output)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"已构建：{target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
