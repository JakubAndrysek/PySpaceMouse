#!/usr/bin/env python3
"""Bump semantic version tags for tag-based versioning workflows."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys


SEMVER_RE = re.compile(r"^(?P<prefix>v?)(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


def _run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _latest_semver_tag() -> tuple[str, int, int, int]:
    try:
        tags = _run_git(["tag", "--list", "--sort=-v:refname"]).splitlines()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Failed to list git tags: {exc}") from exc

    for tag in tags:
        match = SEMVER_RE.match(tag.strip())
        if match:
            return (
                match.group("prefix"),
                int(match.group("major")),
                int(match.group("minor")),
                int(match.group("patch")),
            )

    return "v", 0, 0, 0


def _bump(part: str, major: int, minor: int, patch: int) -> tuple[int, int, int]:
    if part == "major":
        return major + 1, 0, 0
    if part == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump semantic git tag")
    parser.add_argument("part", choices=["patch", "minor", "major"], help="Version part to bump")
    parser.add_argument("--create", action="store_true", help="Create the new git tag")
    args = parser.parse_args()

    prefix, major, minor, patch = _latest_semver_tag()
    next_major, next_minor, next_patch = _bump(args.part, major, minor, patch)
    next_tag = f"{prefix}{next_major}.{next_minor}.{next_patch}"

    if not args.create:
        print(next_tag)
        return 0

    try:
        _run_git(["tag", next_tag])
    except subprocess.CalledProcessError as exc:
        print(f"Failed to create tag {next_tag}: {exc}", file=sys.stderr)
        return 1

    print(next_tag)
    print("Created tag. Push it with: git push --tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
