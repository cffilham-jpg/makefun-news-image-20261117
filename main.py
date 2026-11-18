#!/usr/bin/env python3
"""Entry for make.fun news-image-20261117: copy the pre-rendered entry.png
(a 1024x1024 infographic summing up Tuesday 17 November 2026) into the
output directory. Standard library only; the output is deterministic.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy landed whole before reporting success.
    if os.path.getsize(dst) != os.path.getsize(src):
        print("entry.png copy incomplete", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
