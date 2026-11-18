#!/usr/bin/env python3
"""news-image-20261117 (v3): one image summing up Tuesday 17 November 2026.

The entry is the pre-rendered 1024x1024 editorial infographic in
``entry.png`` (four large illustrated stories, redesigned for legibility
at ~300px): Ukraine's second strike on the Crimea bridge, Iranian drones
targeting a U.S. radar in Bahrain, Trump in Manila for the ASEAN summit,
and China condemning U.S. AI chip curbs.

This program only copies that image into the output directory. It uses
the standard library only (os, shutil, sys) because the grader runs it
in a pinned image where nothing else is installed.

Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output), byte-identical
on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

MAX_BYTES = 1048576  # 1 MiB


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    # Copy-integrity check: the copy must be exactly as large as the source.
    src_size = os.path.getsize(SOURCE)
    size = os.path.getsize(dest)
    if size != src_size:
        print("ERROR: copy incomplete (%d of %d bytes)"
              % (size, src_size), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dest, size))
    if size > MAX_BYTES:
        print("ERROR: output exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
