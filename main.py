"""Entrypoint: copy the pre-rendered meme into the output directory.

Standard library only (os + shutil): the grader runs this file with
`python3 -P -s main.py` in a read-only directory, so it must not import
anything third-party, use fonts or the network, or write into its own
directory. All rendering lives in render.py, which the grader never
executes; entry.png is rendered in advance and shipped in the repo.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote {} ({} bytes)".format(dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
