"""Places Quick Start Guide pages onto the supplied blank brochure mockup.

Usage: python3 tools/make_qsg_mockup.py blank.png cover.png left.png right.png out_dir [--debug]

Each page is mapped onto its sheet following the curved top and bottom edges
of the paper, then multiplied with the mockup's own shading so
the folds, highlights and cast shadows of the photograph are preserved.
"""
import sys, os
import numpy as np, cv2
from PIL import Image

blank_p, cover_p, left_p, right_p, out = sys.argv[1:6]
blank = np.array(Image.open(blank_p).convert("RGBA")).astype(np.float32)
H, W = blank.shape[:2]
alpha = blank[..., 3]
S = W / 1175.0  # corner estimates below were measured on a 1175px-wide proof

def P(x, y): return np.array([x * S, y * S], np.float32)

paper = alpha > 250
def top_y(x):
    col = paper[:, int(round(x))]; return float(np.argmax(col))
def bot_y(x):
    col = paper[:, int(round(x))]; return float(H - 1 - np.argmax(col[::-1]))

# Corners (proof px): open spread
L_TL, L_BL = P(131, 293), P(219, 696)
SP_T, SP_B = P(447, 221), P(553, 617)
R_TR, R_BR = P(757, 148), P(882, 535)
# Cover sheet (its left part sits under the spread)
C = [P(646, 213), P(978, 206), P(1022, 618), P(690, 625)]

N = 40
def edge(a, b, fn, lo=None):
    pts = []
    for i in range(N + 1):
        t = i / N; x = a[0] + (b[0] - a[0]) * t
        y_lin = a[1] + (b[1] - a[1]) * t
        y = fn(x) if fn else y_lin
        pts.append([x, y])
    pts = np.array(pts, np.float32)
    pts[0], pts[-1] = a, b
    return pts

def right_bottom():
    # silhouette is only reliable until the cover sheet starts; finish in a straight line
    pts = edge(SP_B, R_BR, None)
    for i, (x, y) in enumerate(pts):
        if x < 680 * S: pts[i, 1] = bot_y(x)
    k = max(i for i, (x, _) in enumerate(pts) if x < 680 * S)
    for i in range(k, N + 1):
        t = (i - k) / max(1, N - k); pts[i] = pts[k] * (1 - t) + R_BR * t
    return pts

def warp_page(img, top, bot, canvas):
    """Smooth inverse mapping: every output pixel solves for its (u, v) on the
    sheet, where the sheet is the surface between the fitted top and bottom
    edge curves. No seams, no strip artefacts."""
    h, w = img.shape[:2]
    us = np.linspace(0, 1, N + 1)
    ty = np.poly1d(np.polyfit(us, top[:, 1], 7)); by = np.poly1d(np.polyfit(us, bot[:, 1], 7))
    tx0, dtx = top[0, 0], top[-1, 0] - top[0, 0]
    bx0, dbx = bot[0, 0], bot[-1, 0] - bot[0, 0]
    x0, x1 = int(min(top[:, 0].min(), bot[:, 0].min())) - 2, int(max(top[:, 0].max(), bot[:, 0].max())) + 3
    y0, y1 = int(top[:, 1].min()) - 4, int(bot[:, 1].max()) + 5
    X, Y = np.meshgrid(np.arange(x0, x1, dtype=np.float64), np.arange(y0, y1, dtype=np.float64))
    v = np.full_like(X, 0.5); u = np.full_like(X, 0.5)
    for _ in range(10):
        u = (X - (1 - v) * tx0 - v * bx0) / ((1 - v) * dtx + v * dbx)
        uc = np.clip(u, -0.05, 1.05)
        t, b = ty(uc), by(uc)
        v = (Y - t) / (b - t)
    inside = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)
    # feather one pixel so sheet edges stay smooth
    m = cv2.GaussianBlur(inside.astype(np.float32), (0, 0), 0.7)[..., None]
    # pre-filter the page to roughly its on-screen size to avoid aliasing
    scale = max(1.0, h / max(1.0, float(np.median(b - t))))
    if scale > 1.05:
        img = cv2.resize(img, (int(w / scale), int(h / scale)), interpolation=cv2.INTER_AREA); h, w = img.shape[:2]
    warped = cv2.remap(img, (np.clip(u, 0, 1) * (w - 1)).astype(np.float32), (np.clip(v, 0, 1) * (h - 1)).astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    region = canvas[y0:y1, x0:x1]
    region[:] = region * (1 - m) + np.clip(warped, 0, 255) * m

def load(p):
    return np.array(Image.open(p).convert("RGB")).astype(np.float32)

ink = np.full((H, W, 3), 255, np.float32)
# 1. cover (flat sheet: one perspective quad)
cov = load(cover_p); ch, cw = cov.shape[:2]
M = cv2.getPerspectiveTransform(np.array([[0, 0], [cw, 0], [cw, ch], [0, ch]], np.float32), np.array(C, np.float32))
wc = cv2.warpPerspective(cov, M, (W, H), flags=cv2.INTER_AREA, borderValue=(255, 255, 255))
cm = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(cm, np.array(C).astype(np.int32), 255, lineType=cv2.LINE_AA)
ink = ink * (1 - cm[..., None] / 255.0) + wc * (cm[..., None] / 255.0)
# 2. spread hides the cover beneath it
lt, lb = edge(L_TL, SP_T, top_y), edge(L_BL, SP_B, bot_y)
rt, rb = edge(SP_T, R_TR, top_y), right_bottom()
hide = np.zeros((H, W), np.uint8)
cv2.fillPoly(hide, [np.concatenate([lt, rt, rb[::-1], lb[::-1]]).astype(np.int32)], 255, lineType=cv2.LINE_AA)
ink = ink * (1 - hide[..., None] / 255.0) + 255 * (hide[..., None] / 255.0)
warp_page(load(left_p), lt, lb, ink)
warp_page(load(right_p), rt, rb, ink)

# multiply the artwork with the mockup's shading; keep the mockup's alpha (soft shadows)
rgb = blank[..., :3] * (ink / 255.0)
# lift the paper slightly towards white so the print does not look grey
paper_gain = np.where(paper[..., None], 1.045, 1.0)
rgb = np.clip(rgb * paper_gain, 0, 255)
res = Image.fromarray(np.dstack([rgb, alpha]).astype(np.uint8), "RGBA")
res = res.crop(res.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox())
os.makedirs(out, exist_ok=True)
for wd in (1400, 800):
    r = res.resize((wd, round(res.height * wd / res.width)), Image.LANCZOS)
    r.save(os.path.join(out, f"quick-start-mockup-{wd}.webp"), "WEBP", quality=86, alpha_quality=92, method=6)
r.save(os.path.join(out, "quick-start-mockup.png"), optimize=True)
print(res.size, "aspect %.4f" % (res.width / res.height))
