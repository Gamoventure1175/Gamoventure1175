#!/usr/bin/env python3
"""Generate the square and circular portraits used by the profile repository."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "assets" / "photos" / "profile.jpg"
SQUARE_OUTPUT_PATH = ROOT / "assets" / "photos" / "profile-avatar.jpg"
ROUND_OUTPUT_PATH = ROOT / "assets" / "photos" / "profile-avatar-round.png"

CROP_BOX = (56, 40, 706, 690)
OUTPUT_SIZE = (512, 512)
MASK_SCALE = 4


def create_round_mask() -> Image.Image:
    mask_size = tuple(dimension * MASK_SCALE for dimension in OUTPUT_SIZE)
    inset = 2 * MASK_SCALE
    mask = Image.new("L", mask_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse(
        (
            inset,
            inset,
            mask_size[0] - inset - 1,
            mask_size[1] - inset - 1,
        ),
        fill=255,
    )
    return mask.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    with Image.open(SOURCE_PATH) as source:
        if source.width < CROP_BOX[2] or source.height < CROP_BOX[3]:
            raise RuntimeError("The source portrait is too small for the approved crop")

        portrait = source.convert("RGB").crop(CROP_BOX)
        portrait = portrait.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
        portrait.save(
            SQUARE_OUTPUT_PATH,
            format="JPEG",
            quality=92,
            optimize=True,
            progressive=True,
        )

        round_portrait = portrait.convert("RGBA")
        round_portrait.putalpha(create_round_mask())
        round_portrait.save(ROUND_OUTPUT_PATH, format="PNG", optimize=True)

    with Image.open(SQUARE_OUTPUT_PATH) as generated:
        if generated.size != OUTPUT_SIZE or generated.mode != "RGB":
            raise RuntimeError(
                "The generated square portrait has unexpected properties"
            )

    with Image.open(ROUND_OUTPUT_PATH) as generated:
        alpha = generated.getchannel("A")
        if generated.size != OUTPUT_SIZE or generated.mode != "RGBA":
            raise RuntimeError("The generated round portrait has unexpected properties")
        if alpha.getpixel((0, 0)) != 0 or alpha.getpixel((256, 256)) != 255:
            raise RuntimeError("The generated round portrait has an invalid alpha mask")

    print(f"generated {SQUARE_OUTPUT_PATH.relative_to(ROOT)}")
    print(f"generated {ROUND_OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
