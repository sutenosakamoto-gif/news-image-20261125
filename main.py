#!/usr/bin/env python3
"""World News - 25 November 2026, in one image.

Entry point for the make.fun bounty "Sum up 25 November's world news
in one image". The finished front page was rendered during the build
session (see render.py, which drew it with real fonts from the
structured content in content.py) and is shipped in this repository
as page.png. This program only copies that image to the output path,
so it is deterministic by construction: every run writes the same
bytes. Standard library only, no network.
"""

import os
import shutil
import sys

PAGE = "page.png"


def output_path():
    """Where the entry image goes: $MAKEFUN_OUTPUT_DIR, else /output,
    else the directory next to this script."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else \
            os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, PAGE)
    if not os.path.isfile(src):
        print(f"missing {PAGE} next to main.py", file=sys.stderr)
        return 1
    dst = output_path()
    shutil.copyfile(src, dst)
    # Sanity-check the copy: a whole PNG, 1024x1024, at most 1 MiB.
    with open(dst, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        print("copied file is not a PNG", file=sys.stderr)
        return 1
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    size = os.path.getsize(dst)
    if (width, height) != (1024, 1024) or size > 1048576:
        print(f"bad image: {width}x{height}, {size} bytes",
              file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
