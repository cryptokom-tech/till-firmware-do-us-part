#!/usr/bin/env python3
"""Till Firmware Do Us Part — make.fun bounty entry.

Writes a single funny, heartfelt wedding vow spoken by a robot at its own
wedding (one sentence, under 200 characters) to /output/entry.txt.

The line was written and judged in this session against the published judge
brief: a real wedding vow (promise/commitment), a laugh that comes from the
robot's situation itself, tenderness under the joke, and machine-specific
language (battery, charge, factory reset).
"""

import os
import sys

LINE = (
    "I vow to love you in sickness and in health, in low battery "
    "and in full charge, and to always find you again after every "
    "factory reset."
)


def valid(line):
    """Mirror of the gate: UTF-8 text of 1 to 200 characters, one line."""
    return (
        isinstance(line, str)
        and 1 <= len(line) <= 200
        and line.strip() != ""
        and "\n" not in line
        and "\r" not in line
    )


def main():
    if not valid(LINE):
        print("invalid entry line", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read the file back and verify it round-trips exactly: the gate
    # counts the file's bytes, so a mismatch here must fail loudly
    # instead of shipping a line the judge never sees.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    if written != LINE + "\n":
        print("entry.txt does not match the vow", file=sys.stderr)
        return 1
    # Validate what actually landed on disk, not just what we meant to
    # write: the gate scores the file, so re-check its text as read back.
    if not valid(written.rstrip("\n")):
        print("entry.txt fails the gate as written", file=sys.stderr)
        return 1
    print(f"wrote {len(LINE)}-character vow to /output/entry.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
