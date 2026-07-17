#!/usr/bin/env python3
"""Generate the square portrait used by the profile README."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "assets" / "photos" / "profile.jpg"
OUTPUT_PATH = ROOT / "assets" / "photos" / "profile-avatar.jpg"

CROP_BOX = (56, 40, 706, 690)
OUTPUT_SIZE = (512, 512)


def main() -> None:
    with Image.open(SOURCE_PATH) as source:
        if source.width < CROP_BOX[2] or source.height < CROP_BOX[3]:
            raise RuntimeError("The source portrait is too small for the approved crop")

        portrait = source.convert("RGB").crop(CROP_BOX)
        portrait = portrait.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
        portrait.save(
            OUTPUT_PATH,
            format="JPEG",
            quality=92,
            optimize=True,
            progressive=True,
        )

    with Image.open(OUTPUT_PATH) as generated:
        if generated.size != OUTPUT_SIZE or generated.mode != "RGB":
            raise RuntimeError("The generated portrait has unexpected properties")

    print(f"generated {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
