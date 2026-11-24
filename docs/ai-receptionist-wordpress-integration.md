# AI Receptionist page: WordPress integration notes

Staged page: `zultys-ai-receptionist/index.html` (mirrors `/zultys-ai-receptionist/`).
Same approach as the Z 23W page; see `docs/z23w-wordpress-integration.md` for the general steps.

## What ships

| File | Purpose | Ship? |
| --- | --- | --- |
| `assets/ai-receptionist/css/zair.css` | All page styles, scoped to `.zair` | Yes |
| `assets/ai-receptionist/js/zair.js` | Hero phone entrance + parallax, scroll reveal, coverage wave | Yes |
| `assets/ai-receptionist/js/vendor/zultys-wave.js` | Same as the site's `assets/redesign/homepage-wave.js` | Only if not already enqueued; load before `zair.js` |
| `assets/ai-receptionist/img/*` | Optimised WebP + JPEG fallbacks | Yes |
| `assets/ai-receptionist/icons/pdf.png`, `check.svg`, `zultys-mark-outline.svg` | Referenced by the CSS | Yes |
| `assets/ai-receptionist/css/staging-shell.css`, other icons | Stand-in header/footer | No |

Copy the one-line inline `<script>` from the page `<head>` (adds `zair-hero-anim` to `<html>`) so the hero can fade in without a flash.

## Content and assets

- **Copy** is the current zultys.com page, verbatim. Headings were changed from all caps to title case, and two small grammar fixes were made: "Requires different levels of users" → "Require…", "customer-critical need" → "…needs".
- **Hero phone** is HTML/CSS (no image): a black device with an Android-style green chat (sent bubbles green, caller bubbles grey). The conversation extends the old hero example ("Northbridge Outfitters"); the return-policy answer, "Read more" link and timestamps are illustrative copy for a fictional business, and the link is not clickable because the phone is decorative (`aria-hidden`).
- **Icons from the redesign homepage**: `ai-sparkle.svg` (homepage `d3d29.svg`, the spotlight list bullet) replaces the checkmarks in the Organizations list; `stars-5.svg` (homepage `9311e.svg`, survey stars) sits above the logo-strip headline.

- **Organizations composition**: person cutout from Pexels photo 5717729 (background removed with `rembg`), with HTML product UI around it. Stats, menu items and caller details in that UI are illustrative.
- **Hero "AI at work" layer** (`.zair-ops`, behind the phone): decorative, `aria-hidden` wireframe panels (transcription bars, approved sources, intent, instructions, routing, sentiment). All names, extensions and percentages are illustrative, not product data. Animations are CSS-only and stop under `prefers-reduced-motion`.
- **Results** shows four of the original five bullets ("voice or DTMF digit entry" was removed at review). The card titles are new copy.
- **Customer logo strip**: headline "Businesses Rely on Zultys" and the supporting line are new copy. Logos are the homepage testimonial logos in full colour (white or pale lettering recoloured to dark slate so it reads on white; see `tools/process_logos.py`).
- **Voice demos section** (after the two call-example images): headline "Hear Zultys AI Receptionist Take the Call", intro line and the three card descriptions are new copy; check the descriptions against the recordings. Industry icons (`healthcare`, `education`, `automotive` in `ICONS`) follow the page's blue-and-green line style; the five-bar voice wave animates in CSS (faster while that card plays) and holds still under reduced motion. **The recordings are not on zultys.com yet.** Set each URL in `VOICE_DEMOS` (`tools/build_ai_page.py`) and rebuild; with no URL the card shows "Recording coming soon" and its play button and slider are disabled. In WordPress, render each player with the recording's Media Library URL in `<audio preload="metadata" src="…">` inside `.zair-player`, add `data-ready`, and drop the `disabled` attributes; `zair.js` handles play/pause, seeking, the time display and one-at-a-time playback. Seeking needs a server that supports HTTP range requests (WP Engine does). Format: MP3 (or M4A), ideally 128 kbps mono, under ~2 MB each.
- **FAQ** questions and answers are placeholder copy and must be replaced before launch.
- **Call example images** are the two product images from the current page (`Image_Modiule4-copy.jpg`, `Image_Modiule4.jpg`).
- **Icons** are inline SVG, redrawn in the ZAC page line style (blue `#003CDA`, green accent `#4BA541`). They are defined in `tools/build_ai_page.py`.
- **Stock photos** (Pexels License, free for commercial use, no attribution required):
  - Organizations (cutout): https://www.pexels.com/photo/5717729/
  - Minimize Risk: https://www.pexels.com/photo/7163400/
- **Links:** Get a Demo → `/AI-Receptionist-demo-request/`; Product Flyer → the July 2026 PDF; closing card → `/request-demo/` and `/get-a-quote/` (same targets as the current page).

## Regenerating

- `python3 tools/build_ai_page.py` rebuilds the HTML.
- `python3 tools/process_ai_assets.py <source_dir> assets/ai-receptionist/img` rebuilds the images from the originals listed in that script.

## Accessibility note

The logo strip scrolls continuously. It pauses on hover and keyboard focus and is static for visitors with reduced motion turned on, but it has no visible pause button (removed at review). WCAG 2.2.2 expects a pause control for motion lasting more than 5 seconds; add one back if a strict AA audit is required.
