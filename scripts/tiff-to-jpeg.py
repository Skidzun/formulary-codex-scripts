"""
Convert all .tif/.tiff files in project/data to .jpg files in project/output.

Expected layout:
    project/
    ├── data/     (input .tif files)
    ├── output/   (created automatically, receives .jpg files)
    └── src/      (this script lives here)

Requires: pip install pillow
"""

from pathlib import Path

from PIL import Image

# Resolve paths relative to this file, so it works no matter where it's started from
SRC_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SRC_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"


def to_rgb(img: Image.Image) -> Image.Image:
    """Convert an image to 8-bit RGB, which is what JPEG supports."""
    # 16-bit / 32-bit grayscale: scale down to 8 bit first
    if img.mode in ("I;16", "I;16B", "I;16L", "I"):
        img = img.point(lambda p: p * (1 / 256)).convert("L")

    # Transparency: paste onto a white background
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        rgba = img.convert("RGBA")
        background = Image.new("RGB", rgba.size, (255, 255, 255))
        background.paste(rgba, mask=rgba.split()[-1])
        return background

    return img.convert("RGB")


def main() -> None:
    if not DATA_DIR.is_dir():
        raise SystemExit(f"Input directory not found: {DATA_DIR}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    tif_files = sorted(
        p for p in DATA_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".tif", ".tiff"}
    )

    if not tif_files:
        print(f"No .tif files found in {DATA_DIR}")
        return

    converted = 0
    for tif_path in tif_files:
        jpg_path = OUTPUT_DIR / f"{tif_path.stem}.jpg"
        try:
            with Image.open(tif_path) as img:  # multi-page TIFFs: first page only
                to_rgb(img).save(jpg_path, "JPEG", quality=95)
            print(f"Converted: {tif_path.name} -> {jpg_path.name}")
            converted += 1
        except Exception as exc:
            print(f"FAILED:    {tif_path.name} ({exc})")

    print(f"\nDone. {converted}/{len(tif_files)} files converted to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()