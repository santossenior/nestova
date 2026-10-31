"""
compress_static_images.py
Converts heavy JPG/PNG static images to optimised WebP files.
Run from the project root: python compress_static_images.py
"""
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Run: pip install pillow")
    sys.exit(1)

# Folders to scan (relative to project root)
SCAN_DIRS = [
    "static/assets/img/real-estate",
    "static/assets/img",
]

QUALITY = 82          # WebP quality (82 is visually lossless for photos)
MAX_WIDTH = 1920      # Downscale any image wider than this
EXTENSIONS = {".jpg", ".jpeg", ".png"}

def compress_image(src_path: str) -> None:
    base, ext = os.path.splitext(src_path)
    if ext.lower() not in EXTENSIONS:
        return

    dst_path = base + ".webp"
    orig_size = os.path.getsize(src_path)

    try:
        with Image.open(src_path) as img:
            # Convert palette/RGBA to RGB for JPEG-like images
            if img.mode in ("P", "RGBA"):
                img = img.convert("RGBA")  # keep transparency for WebP
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Downscale very large images
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_size = (MAX_WIDTH, int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)

            img.save(dst_path, "WEBP", quality=QUALITY, method=6, optimize=True)

        new_size = os.path.getsize(dst_path)
        saving_pct = 100 * (1 - new_size / orig_size)
        print(f"  {os.path.basename(src_path):45s}  {orig_size//1024:>6}KB -> {new_size//1024:>5}KB  ({saving_pct:.0f}% smaller)")
    except Exception as e:
        print(f"  ERROR {src_path}: {e}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    total_before = 0
    total_after = 0
    count = 0

    for rel_dir in SCAN_DIRS:
        scan_dir = os.path.join(base_dir, rel_dir)
        if not os.path.isdir(scan_dir):
            print(f"Skipping (not found): {scan_dir}")
            continue

        print(f"\n=== Scanning: {scan_dir} ===")
        for fname in os.listdir(scan_dir):
            fpath = os.path.join(scan_dir, fname)
            _, ext = os.path.splitext(fname)
            if ext.lower() not in EXTENSIONS:
                continue

            orig_size = os.path.getsize(fpath)
            compress_image(fpath)
            dst = os.path.join(scan_dir, os.path.splitext(fname)[0] + ".webp")
            if os.path.exists(dst):
                new_size = os.path.getsize(dst)
                total_before += orig_size
                total_after += new_size
                count += 1

    print(f"\n{'='*60}")
    print(f"Compressed {count} images")
    print(f"Total before: {total_before//1024:,} KB")
    print(f"Total after:  {total_after//1024:,} KB")
    if total_before:
        print(f"Saved:        {(total_before - total_after)//1024:,} KB  ({100*(1-total_after/total_before):.0f}%)")
    print("Done. Update template <img> src attributes from .jpg/.png -> .webp")


if __name__ == "__main__":
    main()
