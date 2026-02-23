#!/usr/bin/env python3
"""Helper to write GitHub Actions step outputs from the utils directory."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--set",
        dest="items",
        action="append",
        default=[],
        help="key=value pair to append to GITHUB_OUTPUT (can be repeated)",
    )
    return parser.parse_args()


def write_outputs(pairs: list[str]) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        sys.stderr.write("GITHUB_OUTPUT not set; nothing written\n")
        return

    path = Path(output_path)
    with path.open("a", encoding="utf-8") as handle:
        for pair in pairs:
            if "=" not in pair:
                sys.stderr.write(f"Ignoring invalid output (expected key=value): {pair}\n")
                continue
            key, value = pair.split("=", 1)
            handle.write(f"{key}={value}\n")


def main() -> int:
    args = parse_args()
    if not args.items:
        sys.stderr.write("No outputs provided; nothing to do\n")
        return 0

    write_outputs(args.items)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
