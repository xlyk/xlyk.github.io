# Glitch theme — improvement tracker

From a performance + design review of the live preview on 2026-06-13.

**Legend:** `[ ]` todo · `[x]` done · 🤖 = autonomous (no input needed) · 🙋 = needs Kyle's input

Branch: `theme/perf-and-polish`. All 🤖 items below are implemented and browser-verified in the preview.

---

## 1. Performance & animations

- [x] 🤖 **Scanlines: stop animating `background-position`.** Now a `transform: translateY()` on `.fx-scanlines::before` (compositor-only). Verified: `mk-scan` animates `transform`, not `background-position`. — `glitch.css`
- [x] 🤖 **Body background: drop `background-attachment: fixed`.** Gradient moved to a `position: fixed` `body::before` layer. Verified: `background-attachment: scroll`. — `glitch.css`
- [x] 🤖 **Bake the `feTurbulence` noise to a static raster tile.** Replaced with a 128×128 grayscale PNG (generated via stdlib, no new deps). — `glitch.css` + `static/img/noise.png`
- [x] 🤖 **Delete the dead `mk-flicker` keyframe.** — `glitch.css`

## 2. Typography & readability

- [ ] 🙋 **Body prose font.** Everything is `Share Tech Mono`; long-form + mobile (~6 words/line) suffer. Proposal: keep mono for chrome/code/headings, set body prose in a readable sans or screen serif. **Needs:** go/no-go + which family.
- [ ] 🙋 **Tone down chromatic-aberration on in-article `h2`/`h3`.** Keep the channel-split on the hero/post H1. **Needs:** how far to dial back (taste).

## 3. Code presentation

- [x] 🤖 **Copy-to-clipboard button on code blocks.** Injected by `glitch.js`, shown on hover. Verified: 8/8 blocks. — `glitch.js` + `glitch.css`
- [ ] 🙋 **Language label on code blocks.** *Reclassified:* Pelican's `codehilite` doesn't emit the language in the markup, so a clean label needs a Markdown-processor change (likely `pymdownx`, a dependency). **Needs:** approval to change the Markdown config / add the dependency.

## 4. Sharing / SEO / head

- [x] 🤖 **Open Graph + Twitter Card meta.** Generic on the site, article-specific on posts (`og:type=article`, published_time, tags). — `base.html` / `article.html`
- [ ] 🙋 **Per-post OG image.** Static default vs auto-generated cards. **Needs:** which approach. (The `og:image` tag is the only OG field still missing.)
- [x] 🤖 **Canonical URL per page.** Absolute URL on articles. — `base.html` / `article.html`
- [x] 🤖 **JSON-LD `BlogPosting`.** Verified valid JSON. — `article.html`
- [x] 🤖 **Favicon (SVG) + `theme-color`.** On-brand `>_` glyph. — `static/img/favicon.svg` + `base.html`

## 5. Fonts / loading

- [x] 🤖 **Self-host fonts.** Vendored `Share Tech Mono` + `VT323` woff2, dropped Google CDN + preconnects, `@font-face` + preload. Verified: zero `gstatic`/`googleapis` requests, both fonts load. — `base.html` / `glitch.css` + `static/fonts/`

## 6. Details & polish

- [x] 🤖 **Article tags as clickable chips.** At the post foot. Verified: 5 chips. — `article.html` / `glitch.css`
- [x] 🤖 **Active nav state.** Done in `glitch.js` (pathname → `aria-current`), styled in CSS — cleaner than Jinja include-scoping. Verified: "home" active on `/`. — `glitch.js` / `glitch.css`
- [ ] 🙋 **Prev/next post links.** *Reclassified:* needs the `pelican.plugins.neighbors` plugin to populate neighbors — a dependency. **Needs:** approval to add it.
- [x] 🤖 **Image styling.** `max-width:100%`, `<figure>`/`<figcaption>`; created `content/images/`. — `glitch.css`
- [x] 🤖 **Print stylesheet.** Strips CRT chrome for print/PDF. — `glitch.css`
- [x] 🤖 **Mobile status-bar overflow fix.** Stacks vertically under 680px. — `glitch.css`
- [ ] 🙋 **Status-bar flavor text.** "SIGNAL_LOST :: reacquiring…" implies the link is *down*. **Needs:** what it should convey.

---

## Already solid — no action

- **Contrast** passes WCAG AA across the board (body 14.3:1, links 11.5:1, lowest accent 5.46:1).
- Skip-link, `lang`, `:focus-visible`, `prefers-reduced-motion`, RSS/Atom, code-block horizontal scroll, computed reading-time.

## Needs Kyle's input (the remaining 6)

1. **Body prose font** — go/no-go + family (§2)
2. **Chromatic-aberration** dial-back on `h2`/`h3` (§2)
3. **Per-post OG image** approach (§4) — unblocks the `og:image` tag
4. **Status-bar flavor text** (§6)
5. **Language label** on code blocks (§3) — needs a Markdown-config change / dependency
6. **Prev/next post links** (§6) — needs the `neighbors` plugin (dependency)
