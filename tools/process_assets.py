"""Asset pipeline for the Z 23W product page.

Usage: python3 tools/process_assets.py <source_dir> <out_dir>

Takes the supplied source imagery (transparent product PNGs, lifestyle JPEGs),
trims the products to their silhouette, adds a soft ground shadow that follows
the device footprint, and writes responsive WebP (+ PNG/JPEG fallback) files.
The product pixels themselves are never recoloured or retouched.
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

PRODUCTS = {  # out name: (source file, widths)
    "z23w-hero": ("Module1-Z23-PhoneHero.png", [1800, 1200, 760]),
    "zip-49ga": ("Module_6_-_ZIP49GA.png", [1200, 720]),
    "zip-47ge": ("Module_6_-_ZIP_47GE.png", [1200, 720]),
    "zip-45w": ("Module_6_-_ZIP_45W.png", [1200, 720]),
    "z-22g": ("Module_6_-_Z22G.png", [1200, 720]),
    "z-21i": ("Module_6_-_Z21i.png", [1200, 720]),
}
PHOTOS = {
    "module2-lifestyle": ("Module_2.jpg", [1400, 800], None),
    "feature-hd-audio": ("Module_4_-_Remarkable_Audio.jpg", [1100, 640], None),
    "feature-headset": ("Module_4_-_Wireless_Heaset_Support.jpg", [1100, 640], None),
    "feature-display": ("Module_4_-_Color_Display_and_Ease_of_Use.jpg", [600], None),
    "feature-deployment": ("Module_4_-_Simplified_Deployment.jpg", [1100, 640], None),
    "video-poster": ("video-poster.jpg", [1400, 800], None),
    "quick-start-cover": ("quick-start-cover.png", [520], None),
}


def clean_edges(im):
    """Remove white fringe: un-premultiply semi-transparent edge pixels that
    were matted against white so they do not glow on dark backgrounds."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:4] / 255.0
    edge = (al > 0.02) & (al < 0.98)
    # colour = (observed - (1-a)*white)/a  when the export baked white into the fringe
    est = (rgb - (1 - al) * 255.0) / np.clip(al, 0.02, 1)
    bright = rgb.min(axis=2, keepdims=True) > 200
    rgb = np.where(edge & bright, np.clip(est, 0, 255), rgb)
    out = np.concatenate([rgb, al * 255.0], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def with_shadow(im):
    """Add a soft, diffused ground shadow under the device footprint."""
    w, h = im.size
    pad_x, pad_b, pad_t = int(w * 0.06), int(h * 0.12), int(h * 0.02)
    W, H = w + 2 * pad_x, h + pad_t + pad_b
    alpha = im.getchannel("A")
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # footprint: silhouette flattened onto the ground plane
    fh = int(h * 0.2)
    foot = alpha.resize((int(w * 0.97), fh), Image.LANCZOS)
    def layer(blur, opacity, dy):
        m = Image.new("L", (W, H), 0)
        m.paste(foot, (pad_x + int(w * 0.015), pad_t + h - fh + dy))
        m = m.filter(ImageFilter.GaussianBlur(blur))
        m = m.point(lambda v: int(v * opacity))
        sh = Image.new("RGBA", (W, H), (2, 8, 30, 0)); sh.putalpha(m)
        return sh
    canvas = Image.alpha_composite(canvas, layer(w * 0.035, 0.30, int(h * 0.035)))
    canvas = Image.alpha_composite(canvas, layer(w * 0.012, 0.22, int(h * 0.012)))
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fg.paste(im, (pad_x, pad_t))
    return Image.alpha_composite(canvas, fg)


for name, (src, widths) in PRODUCTS.items():
    im = Image.open(os.path.join(SRC, src)).convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    im = with_shadow(clean_edges(im))
    for wd in widths:
        r = im.resize((wd, round(im.height * wd / im.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, f"{name}-{wd}.webp"), "WEBP", quality=88, alpha_quality=95, method=6)
    r = im.resize((widths[-1] if name != "z23w-hero" else 1200,) * 1 + (round(im.height * (widths[-1] if name != "z23w-hero" else 1200) / im.width),), Image.LANCZOS)
    r.save(os.path.join(OUT, f"{name}.png"), optimize=True)
    print(name, im.size, "aspect %.4f" % (im.width / im.height))

for name, (src, widths, _) in PHOTOS.items():
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    for wd in widths:
        wd = min(wd, im.width)
        r = im.resize((wd, round(im.height * wd / im.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, f"{name}-{wd}.webp"), "WEBP", quality=80, method=6)
    r.save(os.path.join(OUT, f"{name}.jpg"), quality=80, optimize=True, progressive=True)
    print(name, im.size)
