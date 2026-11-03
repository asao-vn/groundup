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
    m1 = sub.add_parser("m1", help="milestone M1: the reaction D + H2 -> HD + H, from quantum mechanics to k(T)")
    m1.add_argument("--basis", default="cc-pvtz", help="Gaussian basis set for layer 0 (default: cc-pvtz)")
    m1.add_argument("--workers", type=int, default=None, help="parallel processes for layer-0 H3 points")
    m1.add_argument("--out", default="results/m1_dh2.json", help="where to write the JSON result")
    args = parser.parse_args(argv)

    if args.command == "m0":
        from .pipelines.m0_h2 import run

        result = run(basis=args.basis, out_path=args.out)
        return 0 if result["passed"] else 1
    if args.command == "m1":
        from .pipelines.m1_dh2 import run as run_m1

        result = run_m1(basis=args.basis, out_path=args.out, workers=args.workers)
        return 0 if result["passed"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
