#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261121 entry.

Copies the pre-drawn summary image (entry.png, built locally by
generate.py) to the grader's output directory as entry.png.

Standard library only, no network, no randomness: both graded runs write
the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT_DIR, "entry.png")

if not os.path.isfile(SRC):
    raise SystemExit("entry.png missing next to main.py")
os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
if os.path.getsize(DST) != os.path.getsize(SRC):
    raise SystemExit("copied entry.png has the wrong size")
print("wrote entry.png (%d bytes)" % os.path.getsize(DST))
