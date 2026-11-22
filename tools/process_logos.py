"""Customer logo strip for the AI Receptionist page (full colour).

Usage: python3 tools/process_logos.py <logo_dir> <out_dir>

Source logos are the customer/partner testimonial logos on the redesign
homepage (assets/redesign/meeting-support/*.webp and inett-figma.png). They
are kept in their brand colours. Two fixes make them read on a white strip:
- logos on an opaque white square have that square keyed out;
- white or very pale grey lettering (artwork made for dark backgrounds) is
  recoloured to dark slate. Coloured parts are left untouched.
Wires, Inc. keeps its own black badge.
"""
import sys, os
import numpy as np
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
INK = np.array([52, 60, 78], np.float32)  # dark slate for pale lettering
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
    ("wires-inc.webp", "Wires, Inc."),
    ("inett.png", "i-NETT"),
]

for fname, name in LOGOS:
    im = Image.open(os.path.join(SRC, fname)).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3] / 255.0
    corners = np.array([a[2, 2], a[2, -3], a[-3, 2], a[-3, -3]])
    keep_badge = corners[:, :3].max() < 30 and corners[:, 3].min() > 200  # dark badge: keep as is
    if not keep_badge:
        if corners[:, 3].min() > 200:  # opaque light square: key it out
            bg = np.median(corners[:, :3], axis=0)
            dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2))
            al = np.clip((dist - 18) / 70, 0, 1) * al
        mx, mn = rgb.max(axis=2), rgb.min(axis=2)
        sat = (mx - mn) / np.maximum(mx, 1)
        pale = np.clip((mn - 175) / 50, 0, 1) * np.clip((0.22 - sat) / 0.12, 0, 1)
        rgb = rgb * (1 - pale[..., None]) + INK * pale[..., None]
    rgba = np.dstack([rgb, al * 255]).clip(0, 255).astype(np.uint8)
    im = Image.fromarray(rgba, "RGBA")
    bbox = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()
    im = im.crop(bbox)
    w = round(im.width * H / im.height)
    if w > 520:  # very wide logos are capped so the strip stays even
        w = 520
        h = round(im.height * w / im.width)
    else:
        h = H
    out = im.resize((w, h), Image.LANCZOS)
    slug = os.path.splitext(fname)[0]
    out.save(os.path.join(OUT, f"{slug}.png"), optimize=True)
    print(f"{slug}.png", out.size, name)
