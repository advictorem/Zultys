# Z 23W product page: WordPress integration notes

Staged page: `phone/z-23w-ip-phone/index.html` (mirrors the WordPress URL `/phone/z-23w-ip-phone/`).

## What ships to WordPress

| File | Purpose | Ship? |
| --- | --- | --- |
| `assets/z23w/css/z23w.css` | All page styles, scoped to `.z23w` | Yes |
| `assets/z23w/js/z23w.js` | Reveal, Show More, carousel, video dialog (no dependencies) | Yes |
| `assets/z23w/js/vendor/zultys-wave.js` | Dotted wave behind the carousel. Identical to the site's `assets/redesign/homepage-wave.js` | Only if that file is not already enqueued on the page; load it before `z23w.js` |
| `assets/z23w/img/*` | Optimised WebP + fallbacks | Yes (upload to Media or the theme) |
| `assets/z23w/icons/pdf.png`, `download.svg`, `play.svg`, `arrow.svg`, `caret-navy.svg`, `zultys-mark-outline.svg` | Button and form icons and the Request a Quote logo mark, referenced by the CSS | Yes |
| `assets/z23w/css/staging-shell.css` | Stand-in header, announcement bar and footer | **No** |
| Other files in `assets/z23w/icons/` | Used only by the staging shell | No |

## Steps

1. **Enqueue** `z23w.css` and `z23w.js` only on the Z 23W phone post (for example in the child theme `zultys-main`, alongside the other `assets/redesign/*` files, behind `is_single( 3105 )`).
2. **Markup:** copy everything inside `<div class="z23w">` from the hero's `.z23w-hero__inner` through the end of `<main>` into the page (an Elementor HTML widget per module works, or a template part). Keep the `.z23w` wrapper: every selector depends on it.
3. **Header and footer:** delete the two blocks marked `STAGING SHELL` and use the shared Elementor shell template (ID 3419) instead. The hero expects the navigation to sit on top of its gradient, the same way the ZAC and Education heroes do: place the nav slot inside `.z23w-hero`, above `.z23w-hero__inner`.
4. **Asset paths:** the HTML uses root-relative `/assets/z23w/...` URLs. Search and replace that prefix with the theme or uploads URL. Inside `z23w.css` the icon URLs are relative (`../icons/`), so they keep working as long as the `css/` and `icons/` folders stay siblings.
5. **Request a Quote:** replace the staging `<form class="z23w-form">` with the existing Gravity Form: `[gravityform id="1" title="false" description="false" ajax="true"]`. That brings back the real fields, validation, honeypot, reCAPTCHA and submission handling. The staging form mirrors that form's fields and `input_*` names, but it is presentation only.
   - Gravity Forms outputs its own markup, so add a short skin that maps `.gform_wrapper` fields to the look of `.z23w-field` (white inputs, 8px radius, white labels) and gives `.gform_button` the gradient pill. The redesign's `button-interactions.css` already targets `.gform_wrapper .gform_button`.
6. **Fonts:** the page uses Proxima Nova from the Adobe Fonts kit the site already loads (`use.typekit.net/gid7nhu.css`). In WordPress remove the `<link>` from the page; the theme provides it.
7. **Design tokens:** `z23w.css` declares the `--z26-*` colour tokens with the same names and values as `design-system-tokens.css`. To follow Elementor global colours instead, delete those declarations from the `.z23w` rule so the page inherits the live values.
8. **Hero entrance:** copy the one-line inline `<script>` from the page `<head>` (it adds `z23w-hero-anim` to `<html>`) so the phone is hidden before first paint and can fade in. Without it the page still works; the phone just appears without the entrance.
9. **Remove from the old page** (per the brief): ZAC Phone Integration card, vertical phone sidebar, green headings, old buttons.

## Things to confirm

- **Spec sheet link.** The hero button uses the data sheet URL from the build brief (`96-35323-Zultys-Z23W-Flyer_vSep2026.pdf`). The outline document lists the Quick Start Guide URL next to "[Product Flyer]", which looks like a paste error.
- **Video.** The dialog plays the tutorial already on the current page (`/wp-content/uploads/2026/05/Z23W_Tutorialz.mp4`, 8 min, 53 MB). The card shows the Z 23W product image; a frame from the video is used only as the player's poster.
- **Quick Start Guide artwork** is the supplied blank brochure mockup with pages 1 to 3 of the PDF mapped onto it (`tools/make_qsg_mockup.py`).
- **Carousel wave.** It animates only while the section is on screen, has a pause button, and shows a still frame on phones and for reduced-motion or data-saver visitors, the same rules the ZAC page uses.
- **Color Display image** was supplied at 600 x 400 px, so it is slightly soft on high-density screens. A larger original would fix that.
- **Product images** arrived as transparent PNGs already; they were trimmed, edge-cleaned and given a soft ground shadow by `tools/process_assets.py`. Product pixels were not altered.

## Regenerating

- `python3 tools/build_z23w_page.py` rebuilds `phone/z-23w-ip-phone/index.html` from `tools/z23w-page.template.html`.
- `python3 tools/process_assets.py <source_dir> assets/z23w/img` rebuilds the images from the original uploads (not stored in the repo).
