# Glitch theme — improvement tracker

From a performance + design review of the live preview on 2026-06-13.

**Legend:** `[ ]` todo · `[x]` done · 🤖 = autonomous · 🙋 = needs Kyle's input

Branch: `theme/perf-and-polish`. Everything below is browser-verified in the preview and passes the production (`publishconf`) build. **Only the OG image (§4) remains** — deferred by request.

---

## 1. Performance & animations

- [x] **Scanlines** → `transform: translateY()` on a pseudo-element (compositor-only). — `glitch.css`
- [x] **Body background** → `position: fixed` `body::before` layer; no more `background-attachment: fixed`. — `glitch.css`
- [x] **Noise** → baked to a 128×128 grayscale PNG (stdlib, no deps). — `glitch.css` + `static/img/noise.png`
- [x] **Dead `mk-flicker` keyframe** deleted. — `glitch.css`

## 2. Typography & readability

- [x] **Body prose font.** Body + card summaries now `IBM Plex Sans` (self-hosted); chrome, headings, and code stay mono. Verified: prose computes to IBM Plex Sans, code to Share Tech Mono. — `glitch.css` + `static/fonts/ibm-plex-sans-400.woff2`
- [x] **Chromatic-aberration dialed back on `h2`.** Now a single soft cyan glow; full channel-split kept on the hero/post H1. — `glitch.css`

## 3. Code presentation

- [x] **Copy-to-clipboard button on code blocks.** Verified: 8/8. — `glitch.js` + `glitch.css`
- [x] **Language label on code blocks.** A vendored local Pelican plugin (`code_lang_labels`, no external dep) injects `data-lang` from the source fences; `glitch.js` renders the label. Verified: 8 labels (text/json/bash). — `plugins/code_lang_labels.py` + `glitch.js`/`glitch.css`

## 4. Sharing / SEO / head

- [x] **Open Graph + Twitter Card meta.** — `base.html` / `article.html`
- [ ] 🙋 **Per-post OG image.** *Deferred by request.* Static default vs auto-generated cards — the only remaining decision; unblocks the `og:image` tag.
- [x] **Canonical URL per page.** — `base.html` / `article.html`
- [x] **JSON-LD `BlogPosting`.** — `article.html`
- [x] **Favicon (SVG) + `theme-color`.** — `static/img/favicon.svg` + `base.html`

## 5. Fonts / loading

- [x] **Self-host fonts.** Share Tech Mono + VT323 + IBM Plex Sans vendored; zero Google requests; preload all three. — `base.html` / `glitch.css` + `static/fonts/`

## 6. Details & polish

- [x] **Article tags as clickable chips.** — `article.html` / `glitch.css`
- [x] **Active nav state.** Pathname → `aria-current` in `glitch.js`. — `glitch.js` / `glitch.css`
- [x] **Prev/next post links.** A vendored local `neighbors` plugin (no external dep) sets newer/older; rendered at the article foot. Verified: older → DSPy post. — `plugins/neighbors.py` + `article.html` / `glitch.css`
- [x] **Image styling** + `content/images/`. — `glitch.css`
- [x] **Print stylesheet.** — `glitch.css`
- [x] **Mobile status-bar overflow fix.** — `glitch.css`
- [x] **Status-bar flavor text.** "SIGNAL_LOST :: reacquiring…" → "SIGNAL_ACQUIRED". — `nav.html`

---

## Already solid — no action

- **Contrast** passes WCAG AA across the board (body 14.3:1, links 11.5:1, lowest accent 5.46:1).
- Skip-link, `lang`, `:focus-visible`, `prefers-reduced-motion`, RSS/Atom, code-block horizontal scroll, computed reading-time.

## Still open

1. **Per-post OG image** (§4) — static default vs auto-generated cards.
