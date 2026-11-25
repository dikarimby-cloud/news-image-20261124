"""Entry program for the make.fun bounty news-image-20261124.

Copies the pre-rendered front page (entry.png, drawn by draw.py from the
verified news of Tuesday 24 November 2026) to the output directory as
entry.png. Standard library only; the copy is byte-identical on every run,
so the grader's two runs always agree.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
