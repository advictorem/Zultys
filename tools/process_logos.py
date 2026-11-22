"""Customer logo strip for the AI Receptionist page.

Usage: python3 tools/process_logos.py <logo_dir> <out_dir>

Source logos are the customer/partner testimonial logos on the redesign
homepage (assets/redesign/meeting-support/*.webp and inett-figma.png). They
mix colour, white-on-transparent and logos on white or black squares, so each
is reduced to a one-colour silhouette (Nextiva-style grey strip):
ink = alpha x distance from the logo's own background colour.
"""
import sys, os
import numpy as np
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
INK = (95, 104, 122)  # neutral slate grey, ~4.6:1 on white
H = 120               # export height (2x for a 60px display height)

LOGOS = [
    ("battle-creek-family-care.webp", "Battle Creek Family Care"),
    ("brandywine-communities.webp", "Brandywine Communities"),
    ("desert-senita.webp", "Desert Senita Community Health Center"),
    ("encompass-church.webp", "Encompass Church"),
    ("lawall-prosthetic-orthotic.webp", "Lawall Prosthetics & Orthotics"),
    ("outdoor-lighting-perspectives.webp", "Outdoor Lighting Perspectives"),
    ("prosper-isd.webp", "Prosper ISD"),
    ("show-me-real-estate.webp", "Show-Me Real Estate"),
    ("sports-and-imports-autos.webp", "Sports and Imports Autos"),
    ("tate-law-group.webp", "Tate Law Group"),
    # wires-inc.webp is left out: blue artwork on a black square does not survive as a one-colour mark.
    ("inett.png", "i-NETT"),
]

for fname, name in LOGOS:
    im = Image.open(os.path.join(SRC, fname)).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] / 255.0
    corners = np.array([a[2, 2], a[2, -3], a[-3, 2], a[-3, -3]])
    if corners[:, 3].min() > 200:  # opaque square background: key it out
        bg = np.median(corners[:, :3], axis=0)
        dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2))
        ink = np.clip((dist - 18) / 70, 0, 1) * al
    else:
        ink = al
    ink = (ink * 255).astype(np.uint8)
    mask = Image.fromarray(ink, "L")
    bbox = mask.point(lambda v: 255 if v > 24 else 0).getbbox()
    mask = mask.crop(bbox)
    w = round(mask.width * H / mask.height)
    if w > 520:  # very wide logos are capped so the strip stays even
        w = 520
        h = round(mask.height * w / mask.width)
    else:
        h = H
    mask = mask.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", mask.size, INK + (0,))
    out.putalpha(mask)
    slug = os.path.splitext(fname)[0]
    out.save(os.path.join(OUT, f"{slug}.png"), optimize=True)
    print(f"{slug}.png", out.size, name)
