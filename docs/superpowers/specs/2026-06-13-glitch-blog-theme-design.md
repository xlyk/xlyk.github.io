# Glitch Blog Theme — Design Spec

Date: 2026-06-13
Status: Proposed (awaiting review)
Branch: `redesign/glitch-theme`

## Goal

Replace the Elegant theme with a custom, from-scratch Pelican theme in a **Glitch /
CRT / datamosh** aesthetic, applied at full intensity across the whole site
including body text and code. Keep full feature parity with what the site
generates today, and keep the build green against the existing CI checks.

The approved visual direction is the Glitch mockup produced during brainstorming.
Reference copies live in `design-mockups/glitch.html` (full standalone page) and
`design-mockups/glitch.fragment.html`.

## Decisions (locked during brainstorming)

- **Aesthetic:** Glitch — neon magenta/cyan on near-black, CRT scanlines,
  RGB channel-split headings, terminal-prompt chrome, datamosh card cuts.
- **Intensity:** Full glitch everywhere — monospace body, neon-on-black, scanlines
  over the whole surface, glitch animation on headings. A `prefers-reduced-motion`
  guard and minimum-contrast rules still apply (see Accessibility).
- **Scope:** Full parity — paginated home, article, standalone page, archives,
  category index + per-category pages, tag index + per-tag pages, author pages,
  404, Atom/RSS feeds, and client-side search.

## Design tokens

Carried verbatim from the approved mockup so the production theme is faithful.

| Token | Value |
|---|---|
| `--void` | `#08080d` (page base) |
| `--void2` | `#0a0a12` |
| `--mag` / `--mag2` | `#ff2079` / `#ff00c1` (magenta) |
| `--cyan` / `--cyan2` | `#05d9e8` / `#00fff7` |
| `--grn` | `#39ff14` (terminal/prompt accent) |
| `--wht` | `#f4f4ff` (primary text) |
| `--body-fg` | `#d8d8f0` (body copy — raised from mockup for contrast) |
| `--dim` | `#8a8aa8` (meta/secondary) |
| Display font | `VT323` (headings) |
| Body/UI/mono font | `Share Tech Mono` |

Fonts load from Google Fonts (`fonts.googleapis.com`) via a `<link>` in the head
with `rel=preconnect`, with a `ui-monospace, Consolas, monospace` fallback stack.
(Self-hosting the fonts is a possible later optimization, out of scope here.)

Signature effects, all pure CSS / inline SVG (no external assets):
- CRT scanline overlay (`repeating-linear-gradient` + slow drift animation).
- Vignette + subtle flicker.
- Low-opacity SVG `feTurbulence` noise data-URI overlay.
- RGB channel split on headings via `text-shadow` + a `::after` clip-path glitch
  keyframe.
- Neon card with a clip-path corner cut and an offset duplicate border.
- Terminal-prompt nav (`guest@xlyk:~$ > home > archive …`) with a blinking cursor.
- Neon "terminal window" code block (traffic-light dots + neon syntax).

## Theme architecture

New theme at `themes/glitch/` (a normal directory, **not** a submodule), selected
via `THEME` in `pelicanconf.py`. The Elegant submodule stays in the repo for now
but is no longer referenced; removing the submodule is a separate follow-up
(out of scope for this spec).

```
themes/glitch/
  templates/
    base.html              # <head>, scanline/noise overlays, nav, footer, blocks
    index.html             # paginated post list
    article.html           # single post: meta, TOC, content, code, table, quote
    page.html              # standalone page
    archives.html          # all posts grouped by year
    period_archives.html   # year/month archive pages (if enabled)
    categories.html        # category index
    category.html          # one category
    tags.html              # tag index
    tag.html               # one tag
    authors.html           # author index
    author.html            # one author
    search.html            # search UI (direct template)
    searchindex.html       # emits search-index.json (direct template)
    notfound.html          # rendered to /404.html
    _includes/
      head.html            # meta tags, fonts, CSS links
      nav.html             # terminal-prompt nav (macro/partial)
      footer.html          # scanline footer
      post_card.html       # macro: one article in a list
      pagination.html      # prev/next controls
  static/
    css/
      glitch.css           # the theme
      pygments-glitch.css  # Pygments token colors in the neon palette
    js/
      glitch.js            # reduced-motion handling + search
```

All templates extend `base.html`. `base.html` owns the browser-chrome-free
full-bleed glitch surface, the scanline/noise overlays, the terminal nav, the
footer, and the standard Pelican blocks (`title`, `head`, `content`).

### Pelican template variables used

Standard Pelican context, confirmed against the current theme:
`article.url`, `article.title`, `article.subtitle`, `article.summary`,
`article.content`, `article.date.isoformat()`, `article.locale_date`,
`article.category(.slug)`, `article.tags`, `article.author`; `page.*`;
`dates` (archives); `categories` (list of `(category, articles)`); `tags`
(list of `(tag, articles)`); and the paginator variables `articles_page`
(`.object_list`, `.has_previous`, `.has_next`) with `articles_previous_page` /
`articles_next_page`.

## Page-by-page design

- **Home (`index.html`)** — Hero (site title with channel-split + tagline +
  `SIGNAL_LOST` status strip), terminal nav, then a paginated list of post cards
  (`post_card` macro): date, category, channel-split title link, summary, `#tag`
  chips. Prev/next pagination at the bottom (driven by `DEFAULT_PAGINATION = 10`).
- **Article (`article.html`)** — Channel-split title, meta line (date · category ·
  reading time · tags), where reading time is computed in-template
  (`article.content | striptags | wordcount` ÷ ~200 wpm) — no plugin/dependency.
  A TOC box (the existing `[TOC]` marker / Pelican `toc`
  extension), then `article.content` styled by `glitch.css`: neon headings,
  full-glitch body, neon terminal code blocks (Pygments), neon tables, pull
  blockquotes. Footer.
- **Standalone page (`page.html`)** — Same content styling, no post meta.
- **Archives (`archives.html`)** — Posts grouped by year as terminal "log lines."
- **Categories / Tags (`categories.html`, `tags.html`)** — Index of terms with
  counts as chips; `category.html` / `tag.html` list that term's posts using the
  same `post_card` macro.
- **Authors (`authors.html`, `author.html`)** — Minimal parity pages (one author
  today); same card styling.
- **404 (`notfound.html` → `/404.html`)** — A "SIGNAL LOST / 404" CRT panel with a
  link home and the search box. GitHub Pages serves `/404.html` automatically.

## Search

Dependency-free, on-brand client-side search (no lunr/tipue):

1. `searchindex.html` is registered as a direct template that emits a JSON array
   of `{title, url, summary, category, tags, date}` for all `articles`, saved to
   `search-index.json` via `SEARCHINDEX_SAVE_AS`.
2. `search.html` is a direct template (`SEARCH_SAVE_AS = 'search.html'`) rendering
   a terminal-prompt input.
3. `glitch.js` fetches `search-index.json`, tokenizes the query, scores matches
   over title/tags/summary, and renders results as glitch cards. ~60 lines, no
   build step, no dependency.

This is lighter than Elegant's lunr+tipue setup and matches the terminal motif.

## Code highlighting

Pelican's `codehilite` emits Pygments token classes (`.k`, `.s`, `.c1`, `.nf`,
`.nc`, …) inside `div.highlight > pre`. The theme ships `pygments-glitch.css`
mapping those tokens to the neon palette (keywords magenta, strings amber,
classes/functions cyan/green, comments dim). The mockup's hand-rolled spans are
replaced by real Pygments output so every code block in every post is styled
consistently.

## Motion & accessibility

- **`prefers-reduced-motion: reduce`** — disable scanline drift, flicker, the
  heading glitch keyframes, and card hover jitter; keep the static neon look.
- **Contrast** — body copy uses `--body-fg` (`#d8d8f0`) on `--void`; links/headings
  use cyan/white at high contrast. Magenta is reserved for large text and accents,
  not small body text, to stay readable.
- **Focus-visible** — visible neon focus outlines on links, buttons, and the
  search input.
- **Semantics** — preserve heading hierarchy, `nav`/`article`/`footer` landmarks,
  `alt` text passthrough, and a visually-hidden skip/summary where useful.

## Configuration changes

`pelicanconf.py`:
- `THEME = "themes/glitch"`
- `DIRECT_TEMPLATES = ["index", "categories", "tags", "archives", "authors", "search", "searchindex", "notfound"]`
- `SEARCH_SAVE_AS = "search.html"`
- `SEARCHINDEX_SAVE_AS = "search-index.json"`
- `NOTFOUND_SAVE_AS = "404.html"`
- Keep `DEFAULT_PAGINATION = 10`, `MARKDOWN` (extra/codehilite/toc), `STATIC_PATHS`.
- `CUSTOM_CSS` override hook retained (optional; theme is self-contained).

`publishconf.py`: no structural change — it imports `*` and keeps feeds + sitemap.
Verify the new direct templates and `search-index.json` build under production
settings too.

## Verification

The repo has no test suite; "done" means the three CI checks pass plus a visual
confirmation:
1. `uv run ruff check .` and `uv run ruff format --check .` — clean.
2. `uv run pelican content -o output -s publishconf.py` — clean build with the new
   theme; confirm `output/` contains index (paginated), the article, archives,
   category/tag pages, `search.html`, `search-index.json`, `404.html`, and feeds.
3. `uv run pelican --listen` and eyeball home + the DSPy article (code, TOC, table,
   blockquote), search, and a 404, including a `prefers-reduced-motion` pass.

## Out of scope (non-goals)

- Removing the Elegant submodule (separate cleanup follow-up).
- Self-hosting fonts (later performance optimization).
- New content, comments, applause, analytics, or social integrations.
- Light-mode / theme toggle — Glitch is dark by nature.

## Open questions

None outstanding. Body-text intensity, scope, and search approach are all decided
above.
