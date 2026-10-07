"""Prep a photo for ASCII conversion: cut out the subject, boost local
contrast, and keep the cut-out mask as alpha.

    python scripts/prep_photo.py source-photo.jpg   # writes source-prepped.png
"""
import io
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "source-prepped.png"


def main(src: str) -> None:
    raw = Path(src).read_bytes()
    # 1. Background removal -> RGBA with the subject isolated.
    cut = Image.open(io.BytesIO(remove(raw))).convert("RGBA")

    # 2. CLAHE on the luminance gives a flatly-lit face real highlights/shadows.
    gray = np.array(cut.convert("L"))
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # 3. Keep the mask as alpha so the background maps to spaces.
    Image.merge("LA", (Image.fromarray(gray, "L"), cut.split()[-1])).save(OUT)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/prep_photo.py <photo>")
    main(sys.argv[1])
