"""Image pipeline for the AI Receptionist page.

Usage: python3 tools/process_ai_assets.py <source_dir> <out_dir>

Sources (not stored in the repo):
  px-11396926.jpg  Pexels photo 11396926 (yi lu), hero caller
  person-on-call-*.webp/png come from Pexels photo 5717729 with the background
                   removed (rembg, isnet-general-use model); see docs.
  px-6812429.jpg   Pexels photo 6812429, dental clinic front desk
  phone-approved-sources.jpg / phone-transfer.jpg  product images from the
                   current zultys.com page (Image_Modiule4-copy.jpg / Image_Modiule4.jpg)
Pexels photos are free to use under the Pexels License.
"""
import sys, os
from PIL import Image, ImageEnhance

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# name: (file, crop box as fractions (l, t, r, b) or None, widths)
JOBS = {
    "hero-caller": ("px-11396926.jpg", (0.10, 0.0, 0.80, 1.0), [1400, 900, 600]),
    "front-desk": ("px-6812429.jpg", (0.0, 0.0, 1.0, 1.0), [1400, 800]),
    "phone-approved-sources": ("phone-approved-sources.jpg", None, [1000, 640]),
    "phone-transfer": ("phone-transfer.jpg", None, [1000, 640]),
}

for name, (src, box, widths) in JOBS.items():
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    if box:
        w, h = im.size
        im = im.crop((round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h)))
    for wd in widths:
        wd = min(wd, im.width)
        r = im.resize((wd, round(im.height * wd / im.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, f"{name}-{wd}.webp"), "WEBP", quality=80, method=6)
    fb = im.resize((widths[1] if len(widths) > 1 else widths[0], round(im.height * (widths[1] if len(widths) > 1 else widths[0]) / im.width)), Image.LANCZOS)
    fb.save(os.path.join(OUT, f"{name}.jpg"), quality=80, optimize=True, progressive=True)
    print(name, im.size, fb.size)
