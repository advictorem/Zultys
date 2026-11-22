# AI Receptionist page: WordPress integration notes

Staged page: `zultys-ai-receptionist/index.html` (mirrors `/zultys-ai-receptionist/`).
Same approach as the Z 23W page; see `docs/z23w-wordpress-integration.md` for the general steps.

## What ships

| File | Purpose | Ship? |
| --- | --- | --- |
| `assets/ai-receptionist/css/zair.css` | All page styles, scoped to `.zair` | Yes |
| `assets/ai-receptionist/js/zair.js` | Hero entrance + parallax, scroll reveal, Results wave | Yes |
| `assets/ai-receptionist/js/vendor/zultys-wave.js` | Same as the site's `assets/redesign/homepage-wave.js` | Only if not already enqueued; load before `zair.js` |
| `assets/ai-receptionist/img/*` | Optimised WebP + JPEG fallbacks | Yes |
| `assets/ai-receptionist/icons/pdf.png`, `check.svg`, `zultys-mark-outline.svg` | Referenced by the CSS | Yes |
| `assets/ai-receptionist/css/staging-shell.css`, other icons | Stand-in header/footer | No |

Copy the one-line inline `<script>` from the page `<head>` (adds `zair-hero-anim` to `<html>`) so the hero can fade in without a flash.

## Content and assets

- **Copy** is the current zultys.com page, verbatim. Headings were changed from all caps to title case, and two small grammar fixes were made: "Requires different levels of users" → "Require…", "customer-critical need" → "…needs".
- **Hero phone** is HTML/CSS (no image), using the example conversation from the old hero graphic ("Northbridge Outfitters").
- **Call example images** are the two product images from the current page (`Image_Modiule4-copy.jpg`, `Image_Modiule4.jpg`).
- **Icons** are inline SVG, redrawn in the ZAC page line style (blue `#003CDA`, green accent `#4BA541`). They are defined in `tools/build_ai_page.py`.
- **Stock photos** (Pexels License, free for commercial use, no attribution required):
  - Hero: https://www.pexels.com/photo/11396926/ (yi lu)
  - Organizations: https://www.pexels.com/photo/10375878/
  - Minimize Risk: https://www.pexels.com/photo/6812429/
- **Links:** Get a Demo → `/AI-Receptionist-demo-request/`; Product Flyer → the July 2026 PDF; closing card → `/request-demo/` and `/get-a-quote/` (same targets as the current page).

## Regenerating

- `python3 tools/build_ai_page.py` rebuilds the HTML.
- `python3 tools/process_ai_assets.py <source_dir> assets/ai-receptionist/img` rebuilds the images from the originals listed in that script.
