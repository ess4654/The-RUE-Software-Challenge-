#!/usr/bin/env python3
r"""Verify every full-page plate landed on a right-hand (odd) page.

Each plate macro writes \plateonpage{N} into the .aux file. A plate on an even
page would face the reader on the left-hand leaf, so any even N is a failure.
Exit status 1 on failure so the build stops.
"""
import re
import sys

aux = sys.argv[1] if len(sys.argv) > 1 else "main.aux"

try:
    text = open(aux, encoding="utf-8", errors="replace").read()
except OSError as exc:
    print(f"PLATE CHECK: cannot read {aux}: {exc}")
    sys.exit(1)

pages = [int(n) for n in re.findall(r"\\plateonpage\{(\d+)\}", text)]

if not pages:
    print(f"PLATE CHECK: no plate records found in {aux} -- macros not logging?")
    sys.exit(1)

bad = [n for n in pages if n % 2 == 0]

print(f"PLATE CHECK: {len(pages)} plates found in {aux}")
if bad:
    print(f"PLATE CHECK FAILED: {len(bad)} plate(s) on left-hand (even) pages: {bad}")
    sys.exit(1)

print("PLATE CHECK PASSED: every plate is on a right-hand (odd) page")
