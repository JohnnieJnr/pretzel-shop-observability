#!/usr/bin/env python3
"""Discover Docker build targets for the workflow matrix."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


SKIP_DIRS = {".git", ".github", "__pycache__", ".venv", "venv", "node_modules"}


def slugify(value: str) -> str:
    """Convert a relative path into a docker-friendly image suffix."""
    normalized = value.strip()
    if normalized in {"", "."}:
        normalized = "root"

    slug = normalized.lower().replace("/", "-")
    slug = re.sub(r"[^a-z0-9._-]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "image"


def discover_targets(repo_root: Path) -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for current_root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if "Dockerfile" not in files:
            continue

        context = Path(current_root)
        rel_context = context.relative_to(repo_root).as_posix()
        if rel_context == ".":
            rel_context = "."

        rel_dockerfile = (context / "Dockerfile").relative_to(repo_root).as_posix()
        key = (rel_context, rel_dockerfile)
        if key in seen:
            continue
        seen.add(key)

        targets.append(
            {
                "name": slugify(rel_context),
                "context": rel_context,
                "dockerfile": rel_dockerfile,
            }
        )

    targets.sort(key=lambda item: item["context"])
    return targets


def write_github_outputs(path: Path, matrix: dict[str, list[dict[str, str]]]) -> None:
    target_count = len(matrix["include"])
    with path.open("a", encoding="utf-8") as output:
        output.write(f"matrix={json.dumps(matrix, separators=(',', ':'))}\n")
        output.write(f"has_targets={'true' if target_count else 'false'}\n")
        output.write(f"target_count={target_count}\n")


def append_summary(path: Path, targets: list[dict[str, str]]) -> None:
    with path.open("a", encoding="utf-8") as summary:
        summary.write("## Docker discovery\n")
        summary.write(f"- Scanned root: `{Path.cwd().as_posix()}`\n")
        summary.write(f"- Targets found: `{len(targets)}`\n")
        if targets:
            summary.write("- Build contexts:\n")
            for target in targets:
                summary.write(
                    f"  - `{target['context']}` (`{target['dockerfile']}`)\n"
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root to scan (default: current directory).",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Print resulting matrix JSON to stdout.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    targets = discover_targets(repo_root)
    matrix = {"include": targets}

    if args.print_json:
        print(json.dumps(matrix, indent=2))

    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        write_github_outputs(Path(github_output), matrix)

    github_step_summary = os.getenv("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        append_summary(Path(github_step_summary), targets)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
