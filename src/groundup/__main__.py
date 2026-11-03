"""Command line: ``python -m groundup m0``."""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="groundup")
    sub = parser.add_subparsers(dest="command", required=True)
    m0 = sub.add_parser("m0", help="milestone M0: H2 from quantum mechanics to classical atoms")
    m0.add_argument("--basis", default="cc-pvtz", help="Gaussian basis set for layer 0 (default: cc-pvtz)")
    m0.add_argument("--out", default="results/m0_h2.json", help="where to write the JSON result")
    args = parser.parse_args(argv)

    if args.command == "m0":
        from .pipelines.m0_h2 import run

        result = run(basis=args.basis, out_path=args.out)
        return 0 if result["passed"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
