#!/usr/bin/env python3
"""
Fix mojibake (e.g. the checkmark ✓ shown as âœ", the em-dash — shown as
Ã¢â‚¬â) that was baked into the HTML files when they were re-saved through a
Windows-1252 misread of UTF-8 bytes. Some characters were corrupted more than
once, so we use ftfy, which detects and undoes multi-level mojibake while
leaving already-correct text alone.

Usage:
    python fix_mojibake.py [files...]            # dry-run (shows changes)
    python fix_mojibake.py [files...] --write    # apply the fix

With no file arguments, processes every .html file except those under backups/.
"""
import sys
import glob
import os

import ftfy

# Windows console is cp1252; make sure we can print the recovered glyphs.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def process(path: str, write: bool) -> int:
    with open(path, "r", encoding="utf-8", newline="") as f:
        original = f.read()
    fixed = ftfy.fix_text(original)
    if fixed == original:
        return 0

    orig_lines = original.splitlines()
    fixed_lines = fixed.splitlines()
    changed = 0
    samples = []
    for i, (o, n) in enumerate(zip(orig_lines, fixed_lines), 1):
        if o != n:
            changed += 1
            if len(samples) < 8:
                samples.append((i, o.strip()[:90], n.strip()[:90]))

    print(f"\n=== {path}  ({changed} lines changed) ===")
    for ln, o, n in samples:
        print(f"  line {ln}")
        print(f"    BEFORE: {o}")
        print(f"    AFTER : {n}")

    if write:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(fixed)
    return changed


def main():
    write = "--write" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        targets = args
    else:
        targets = [
            p for p in glob.glob("**/*.html", recursive=True)
            if "backups" + os.sep not in p and not p.startswith("backups" + os.sep)
        ]

    total_files = 0
    total_lines = 0
    for path in targets:
        c = process(path, write)
        if c:
            total_files += 1
            total_lines += c

    mode = "WRITTEN" if write else "DRY-RUN (no files changed)"
    print(f"\n--- {mode}: {total_files} files, {total_lines} lines affected ---")


if __name__ == "__main__":
    main()
