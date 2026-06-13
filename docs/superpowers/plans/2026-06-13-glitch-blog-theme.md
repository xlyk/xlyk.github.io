# Glitch Blog Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Elegant theme with a custom, from-scratch Pelican theme in a full-intensity Glitch/CRT aesthetic, at full feature parity, with the build staying green throughout.

**Architecture:** A new theme at `themes/glitch/` selected via `THEME`. `base.html` owns the full-bleed glitch surface (scanline/noise/vignette overlays, terminal nav, footer, head). All pages extend it. The complete visual language lives in one `static/css/glitch.css` (the class-name contract), ported from the already-committed `design-mockups/glitch.fragment.html`; real Markdown→Pygments code is styled by a separate `pygments-glitch.css`. Search is dependency-free: a direct template emits `search-index.json`, and `glitch.js` filters it client-side. Templates are created as build-green stubs first, then fleshed out one at a time so every task ends in a clean `pelican` build.

**Tech Stack:** Pelican (Jinja2 templates), Python config (`pelicanconf.py`/`publishconf.py`), Pygments (`codehilite`), vanilla CSS + JS, Google Fonts (Share Tech Mono, VT323). Tooling: `uv`, `ruff`.

---

## Conventions for every task

- **Build (dev):** `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
- **Build (prod parity):** `PYTHONPATH=. uv run pelican content -o output -s publishconf.py --delete-output-directory`
- **Lint (only when a `.py` file changed):** `uv run ruff check .` and `uv run ruff format --check .`
- `themes/` and `output/` are excluded from ruff (`extend-exclude` in `pyproject.toml`), so template/CSS/JS edits never need linting — only `pelicanconf.py` / `publishconf.py` edits do.
- Commit at the end of each task with the shown message.
- All asset/links in templates use absolute-capable `{{ SITEURL }}/...` so `/404.html` works when served from any path on GitHub Pages.

## File structure

```
themes/glitch/
  templates/
    base.html              # head, overlays, terminal nav, footer, blocks
    index.html             # paginated post list
    article.html           # single post: meta, reading time, TOC, content
    page.html              # standalone page
    archives.html          # all posts by year
    categories.html        # category index (chips + counts)
    category.html          # one category's posts
    tags.html              # tag index
    tag.html               # one tag's posts
    authors.html           # author index
    author.html            # one author's posts
    search.html            # search UI (direct template -> search.html)
    searchindex.html       # emits search-index.json (direct template)
    notfound.html          # rendered to /404.html
    _includes/
      nav.html             # terminal-prompt nav partial
      footer.html          # scanline footer partial
      macros.html          # post_card(article) + pagination(page) macros
  static/
    css/
      glitch.css           # the theme (class-name contract)
      pygments-glitch.css  # Pygments token colors in neon palette
    js/
      glitch.js            # reduced-motion handling + client-side search
```

Theme source of truth for the visual language: `design-mockups/glitch.fragment.html` (already committed). The class names below are the de-scoped production contract.

### Class-name contract (used across all templates)

| Mockup class (scoped `.mk-glitch …`) | Production class | Applies to |
|---|---|---|
| `.screen` | `body` | full-bleed glitch surface |
| `.noise` | `.fx-noise` | turbulence overlay (fixed) |
| (scanlines were `.screen::before`) | `.fx-scanlines` | scanline overlay (fixed) |
| `.topbar` | `.status-bar` | status strip |
| `.hero h1` / channel-split | `.glitch-title[data-txt]` | any channel-split heading |
| `nav.term` | `nav.term` | terminal nav |
| `.card` | `.card` | one post in a list |
| `.term-win` | `.code-window` wrapper; real code is `.post-content div.highlight` | code blocks |
| `.toc` | `.post-content .toc` | Pelican `[TOC]` output |
| `blockquote.pull` | `.post-content blockquote` | pull quotes |
| `table.gx` | `.post-content table` | tables |
| `footer.scr` | `footer.site-foot` | footer |

---

### Task 1: Theme skeleton that builds green

**Files:**
- Create: `themes/glitch/templates/base.html`
- Create: `themes/glitch/templates/_includes/nav.html`
- Create: `themes/glitch/templates/_includes/footer.html`
- Create: `themes/glitch/templates/_includes/macros.html`
- Create stubs: `themes/glitch/templates/{index,article,page,archives,categories,category,tags,tag,authors,author}.html`
- Create: `themes/glitch/static/css/glitch.css`
- Create: `themes/glitch/static/js/glitch.js`
- Modify: `pelicanconf.py`

- [ ] **Step 1: Create `base.html`**

```jinja
<!DOCTYPE html>
<html lang="{{ DEFAULT_LANG }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}{{ SITENAME|striptags }}{% endblock %}</title>
  <meta name="description" content="{% block description %}{{ SITESUBTITLE|default('Notes on AI engineering, code, and the tools in between.') }}{% endblock %}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=VT323&display=swap">
  <link rel="stylesheet" href="{{ SITEURL }}/theme/css/glitch.css">
  <link rel="stylesheet" href="{{ SITEURL }}/theme/css/pygments-glitch.css">
  {% if FEED_ALL_ATOM %}<link rel="alternate" type="application/atom+xml" title="{{ SITENAME }} Atom" href="{{ SITEURL }}/{{ FEED_ALL_ATOM }}">{% endif %}
  {% block extra_head %}{% endblock %}
</head>
<body>
  <div class="fx-scanlines" aria-hidden="true"></div>
  <div class="fx-noise" aria-hidden="true"></div>
  <a class="skip-link" href="#main">skip to content</a>
  {% include '_includes/nav.html' %}
  <main id="main" class="wrap">
    {% block content %}{% endblock %}
  </main>
  {% include '_includes/footer.html' %}
  <script src="{{ SITEURL }}/theme/js/glitch.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Create `_includes/nav.html`**

```jinja
<header class="site-head">
  <div class="status-bar">
    <span class="hex">0x4B59 // 01001011</span>
    <span class="sig">▓ SIGNAL_LOST :: reacquiring…</span>
    <span class="ok">● CRT_LINK OK</span>
  </div>
  <nav class="term" aria-label="Primary">
    <span class="ps1">guest@xlyk:~$</span>
    <a href="{{ SITEURL }}/">home</a>
    <a href="{{ SITEURL }}/{{ ARCHIVES_SAVE_AS|default('archives.html') }}">archive</a>
    <a href="{{ SITEURL }}/{{ CATEGORIES_SAVE_AS|default('categories.html') }}">categories</a>
    <a href="{{ SITEURL }}/{{ TAGS_SAVE_AS|default('tags.html') }}">tags</a>
    <a href="{{ SITEURL }}/search.html">search</a>
    <span class="cur" aria-hidden="true"></span>
  </nav>
</header>
```

- [ ] **Step 3: Create `_includes/footer.html`**

```jinja
<footer class="site-foot">
  <span><span class="glitchtxt">©</span> {{ CURRENT_YEAR|default(2026) }} {{ AUTHOR }} — built with Pelican</span>
  <span class="links">
    {% if FEED_ALL_ATOM %}<a href="{{ SITEURL }}/{{ FEED_ALL_ATOM }}">RSS</a>{% endif %}
    <a href="https://github.com/xlyk" rel="me">GitHub</a>
  </span>
</footer>
```

- [ ] **Step 4: Create `_includes/macros.html`** (used from Task 2 on; defined now so it exists)

```jinja
{% macro post_card(article) %}
<article class="card">
  <div class="pmeta">
    <span class="ts">{{ article.locale_date }}</span>
    {% if article.category %}<span class="cat">{{ article.category }}</span>{% endif %}
  </div>
  <h2 class="card-title glitch-title" data-txt="{{ article.title|striptags }}"><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></h2>
  {% if article.summary %}<p class="sum">{{ article.summary|striptags }}</p>{% endif %}
  {% if article.tags %}<div class="chips">{% for tag in article.tags %}<a class="chip" href="{{ SITEURL }}/{{ tag.url }}">{{ tag }}</a>{% endfor %}</div>{% endif %}
</article>
{% endmacro %}

{% macro pagination(page) %}
{% if page and (page.has_previous or page.has_next) %}
<nav class="pager" aria-label="Pagination">
  {% if page.has_previous %}<a class="pager-prev" href="{{ SITEURL }}/{{ articles_previous_page.url }}">&larr; newer</a>{% endif %}
  <span class="pager-pos">page {{ page.number }} / {{ page.paginator.num_pages }}</span>
  {% if page.has_next %}<a class="pager-next" href="{{ SITEURL }}/{{ articles_next_page.url }}">older &rarr;</a>{% endif %}
</nav>
{% endif %}
{% endmacro %}
```

- [ ] **Step 5: Create the 10 stub templates** — identical pattern, one file each. Each is a placeholder body so the build is green; fleshed out in later tasks.

`index.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
{% for article in articles %}<p><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></p>{% endfor %}
{% endblock %}
```
`article.html`:
```jinja
{% extends 'base.html' %}
{% block title %}{{ article.title|striptags }} — {{ super() }}{% endblock %}
{% block content %}
<article class="post"><h1>{{ article.title }}</h1><div class="post-content">{{ article.content }}</div></article>
{% endblock %}
```
`page.html`:
```jinja
{% extends 'base.html' %}
{% block title %}{{ page.title|striptags }} — {{ super() }}{% endblock %}
{% block content %}
<article class="post"><h1>{{ page.title }}</h1><div class="post-content">{{ page.content }}</div></article>
{% endblock %}
```
`archives.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
{% for article in dates %}<p>{{ article.locale_date }} — <a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></p>{% endfor %}
{% endblock %}
```
`categories.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
{% for category, articles in categories %}<p><a href="{{ SITEURL }}/{{ category.url }}">{{ category }}</a> ({{ articles|length }})</p>{% endfor %}
{% endblock %}
```
`category.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
<h1>{{ category }}</h1>
{% for article in articles %}<p><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></p>{% endfor %}
{% endblock %}
```
`tags.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
{% for tag, articles in tags %}<p><a href="{{ SITEURL }}/{{ tag.url }}">{{ tag }}</a> ({{ articles|length }})</p>{% endfor %}
{% endblock %}
```
`tag.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
<h1>{{ tag }}</h1>
{% for article in articles %}<p><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></p>{% endfor %}
{% endblock %}
```
`authors.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
{% for author, articles in authors %}<p><a href="{{ SITEURL }}/{{ author.url }}">{{ author }}</a> ({{ articles|length }})</p>{% endfor %}
{% endblock %}
```
`author.html`:
```jinja
{% extends 'base.html' %}
{% block content %}
<h1>{{ author }}</h1>
{% for article in articles %}<p><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></p>{% endfor %}
{% endblock %}
```

- [ ] **Step 6: Create `static/css/glitch.css`** — port from the committed mockup, de-scoped to the contract above, plus the new global/accessibility/pagination/search blocks.

Porting instructions (source: `design-mockups/glitch.fragment.html` `<style>`):
1. Delete the browser-chrome rules: every selector containing `.frame`, `.bar`, `.dots`, `.url`, `.seg`, and the `.screen` wrapper itself.
2. Re-target the remaining component rules by stripping the `.mk-glitch ` prefix and mapping per the contract table: `.screen` → `body`; `.view` padding → `.wrap`; `.art …` content rules → `.post-content …`; `.term-win` → `.code-window`; keep `.status-bar` (was `.topbar`), `nav.term`, `.card`, `.chips/.chip`, `.toc`, `blockquote.pull` → `.post-content blockquote`, `table.gx` → `.post-content table`, `footer.scr` → `footer.site-foot`.
3. Keep all `@keyframes` (mk-scan, mk-flicker, mk-glitch, mk-slice, mk-blink) and the `--void/--mag/--cyan/--grn/--wht/--dim` custom properties; add `--body-fg:#d8d8f0`.

Then append these NET-NEW blocks verbatim:

```css
:root{ --void:#08080d; --void2:#0a0a12; --mag:#ff2079; --mag2:#ff00c1; --cyan:#05d9e8; --cyan2:#00fff7; --grn:#39ff14; --wht:#f4f4ff; --body-fg:#d8d8f0; --dim:#8a8aa8; --mono:'Share Tech Mono',ui-monospace,Consolas,monospace; --disp:'VT323','Share Tech Mono',monospace; }
*,*::before,*::after{ box-sizing:border-box; }
html,body{ margin:0; }
body{ background:radial-gradient(120% 90% at 50% 0%,#10101e 0%,var(--void2) 45%,var(--void) 100%) fixed; color:var(--body-fg); font-family:var(--mono); font-size:16px; line-height:1.7; min-height:100vh; }
.wrap{ max-width:820px; margin:0 auto; padding:28px 24px 0; }
a{ color:var(--cyan); }
.skip-link{ position:absolute; left:-9999px; }
.skip-link:focus{ left:8px; top:8px; z-index:50; background:var(--void); color:var(--cyan); padding:8px 12px; border:1px solid var(--cyan); }

/* Fixed CRT overlays (real browser — position:fixed is fine here) */
.fx-scanlines{ position:fixed; inset:0; pointer-events:none; z-index:60; opacity:.5; background:repeating-linear-gradient(to bottom,rgba(0,0,0,0) 0 2px,rgba(0,0,0,.28) 3px,rgba(0,0,0,0) 4px); animation:mk-scan 9s linear infinite; }
.fx-noise{ position:fixed; inset:0; pointer-events:none; z-index:1; opacity:.05; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>"); }

/* Reading time + post meta */
.reading-time{ color:var(--grn); }

/* Pagination */
.pager{ display:flex; align-items:center; justify-content:space-between; gap:14px; margin:30px 0 40px; font-size:14px; }
.pager a{ text-decoration:none; border:1px solid rgba(5,217,232,.4); padding:7px 14px; color:var(--cyan); }
.pager a:hover{ border-color:var(--mag); color:var(--cyan2); text-shadow:1px 0 var(--mag),-1px 0 var(--cyan); }
.pager-pos{ color:var(--dim); font-size:12px; letter-spacing:.1em; }

/* Search */
.search-box{ display:flex; align-items:center; gap:8px; border:1px solid rgba(57,255,20,.3); border-left:3px solid var(--grn); background:rgba(57,255,20,.04); padding:12px 14px; margin:18px 0; }
.search-box .ps1{ color:var(--mag); }
.search-box input{ flex:1; background:transparent; border:0; color:var(--wht); font-family:var(--mono); font-size:16px; outline:none; }
.search-status{ color:var(--dim); font-size:13px; margin:0 0 18px; }

/* Accessibility */
:focus-visible{ outline:2px solid var(--cyan2); outline-offset:2px; }
@media (prefers-reduced-motion: reduce){
  *{ animation:none !important; transition:none !important; }
  .fx-scanlines{ opacity:.18; }
  .glitch-title::after{ display:none; }
}
```

- [ ] **Step 7: Create a minimal `static/js/glitch.js`** (search filled in Task 10)

```js
(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
  }
})();
```

- [ ] **Step 8: Wire `pelicanconf.py`** — change the theme and add author-index parity. Replace the `THEME` / `CUSTOM_CSS` lines:

```python
THEME = "themes/glitch"

# Glitch theme generates an author index for parity
DIRECT_TEMPLATES = ["index", "categories", "authors", "tags", "archives"]
```
Leave `DEFAULT_PAGINATION = 10`, `MARKDOWN`, `STATIC_PATHS`, `EXTRA_PATH_METADATA` unchanged. Remove the `CUSTOM_CSS = "static/custom.css"` line (the theme is self-contained); keep the `extra/custom.css` copy mapping in `EXTRA_PATH_METADATA` as a harmless override hook.

- [ ] **Step 9: Build (dev) and verify green**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Expected: completes with `Done: ... articles, ... pages` and no traceback. Then:
Run: `ls output/index.html output/archives.html output/categories.html output/tags.html output/authors.html output/mastering-prompt-chaining-with-dspy.html`
Expected: all exist.

- [ ] **Step 10: Lint (pelicanconf.py changed)**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: no errors.

- [ ] **Step 11: Commit**

```bash
git add themes/glitch pelicanconf.py
git commit -m "feat(theme): glitch theme skeleton — base, stubs, css, config"
```

---

### Task 2: Paginated home + post-card macro

**Files:**
- Modify: `themes/glitch/templates/index.html`

- [ ] **Step 1: Replace `index.html` with the full paginated version**

```jinja
{% extends 'base.html' %}
{% from '_includes/macros.html' import post_card, pagination with context %}
{% block content %}
<section class="hero">
  <h1 class="glitch-title" data-txt="{{ SITENAME|striptags }}">{{ SITENAME }}</h1>
  <p class="tag">{{ SITESUBTITLE|default('Notes on AI engineering, code, and the tools in between.') }}</p>
  <p class="auth">authored_by <b>{{ AUTHOR }}</b> &nbsp;|&nbsp; uplink stable<span class="grn">_</span></p>
</section>
<p class="sectionlabel">LATEST_TRANSMISSIONS{% if articles_paginator %} — page {{ articles_page.number }} / {{ articles_paginator.num_pages }}{% endif %}</p>
{% for article in (articles_page.object_list if articles_page else articles) %}
{{ post_card(article) }}
{% endfor %}
{{ pagination(articles_page) }}
{% endblock %}
```

- [ ] **Step 2: Build and verify pagination output**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Expected: green build. With only 2 posts and pagination 10, there is one page; confirm `output/index.html` exists and contains `class="card"`:
Run: `grep -c 'class="card"' output/index.html`
Expected: `2`.

- [ ] **Step 3: Commit**

```bash
git add themes/glitch/templates/index.html
git commit -m "feat(theme): paginated home with post cards"
```

---

### Task 3: Full article page (meta, reading time, TOC, content)

**Files:**
- Modify: `themes/glitch/templates/article.html`

- [ ] **Step 1: Replace `article.html`**

```jinja
{% extends 'base.html' %}
{% block title %}{{ article.title|striptags }} — {{ super() }}{% endblock %}
{% block description %}{{ article.summary|striptags|truncate(160) }}{% endblock %}
{% block content %}
{% set words = article.content|striptags|wordcount %}
{% set rt = ((words / 200) | round(0, 'ceil') | int) or 1 %}
<article class="post">
  <h1 class="glitch-title" data-txt="{{ article.title|striptags }}">{{ article.title }}</h1>
  <p class="am00">
    <b>{{ article.locale_date }}</b>
    {% if article.category %}<span class="t2">·</span> {{ article.category }}{% endif %}
    <span class="t2">·</span> <span class="reading-time">{{ rt }} min read</span>
    {% if article.tags %}<span class="t2">·</span> tags: {% for tag in article.tags %}{{ tag }}{% if not loop.last %}, {% endif %}{% endfor %}{% endif %}
  </p>
  <div class="post-content">
    {{ article.content }}
  </div>
</article>
{% endblock %}
```

- [ ] **Step 2: Build and verify article output**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Expected: green. Then confirm meta + TOC + code render:
Run: `grep -o 'reading-time\|class="toc"\|class="highlight"' output/mastering-prompt-chaining-with-dspy.html | sort -u`
Expected: includes `class="highlight"`, `class="toc"`, and `reading-time`.

- [ ] **Step 3: Commit**

```bash
git add themes/glitch/templates/article.html
git commit -m "feat(theme): full article page with meta, reading time, TOC"
```

---

### Task 4: Pygments neon stylesheet

**Files:**
- Create: `themes/glitch/static/css/pygments-glitch.css`

- [ ] **Step 1: Create `pygments-glitch.css`** mapping Pygments token classes to the neon palette. (Already linked by `base.html` in Task 1.)

```css
.post-content div.highlight{ border:1px solid rgba(5,217,232,.4); background:#06060f; box-shadow:0 0 22px rgba(5,217,232,.12); margin:0 0 22px; }
.post-content div.highlight pre{ margin:0; padding:14px 16px; overflow-x:auto; font-family:var(--mono); font-size:14px; line-height:1.7; color:var(--body-fg); }
.post-content .highlight .hll{ background:rgba(255,32,121,.15); }
.post-content .highlight .c, .post-content .highlight .c1, .post-content .highlight .cm, .post-content .highlight .cs{ color:var(--dim); font-style:italic; }
.post-content .highlight .k, .post-content .highlight .kn, .post-content .highlight .kd, .post-content .highlight .kc, .post-content .highlight .kp, .post-content .highlight .kr, .post-content .highlight .ow{ color:var(--mag); }
.post-content .highlight .s, .post-content .highlight .s1, .post-content .highlight .s2, .post-content .highlight .sb, .post-content .highlight .sd, .post-content .highlight .se, .post-content .highlight .sh, .post-content .highlight .sx, .post-content .highlight .dl{ color:#ffd166; }
.post-content .highlight .nf, .post-content .highlight .fm{ color:var(--grn); }
.post-content .highlight .nc, .post-content .highlight .nn, .post-content .highlight .ne, .post-content .highlight .bp{ color:var(--cyan2); }
.post-content .highlight .nb, .post-content .highlight .nv, .post-content .highlight .vc, .post-content .highlight .vg, .post-content .highlight .vi{ color:var(--cyan); }
.post-content .highlight .mi, .post-content .highlight .mf, .post-content .highlight .mh, .post-content .highlight .mo, .post-content .highlight .il{ color:#ffd166; }
.post-content .highlight .o, .post-content .highlight .p{ color:var(--cyan); }
.post-content .highlight .nd{ color:var(--grn); }
.post-content .highlight .err{ color:var(--wht); background:rgba(255,32,121,.3); }
```

- [ ] **Step 2: Build and confirm the stylesheet is copied + referenced**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `test -f output/theme/css/pygments-glitch.css && grep -c 'pygments-glitch.css' output/mastering-prompt-chaining-with-dspy.html`
Expected: file exists and grep returns `1`.

- [ ] **Step 3: Commit**

```bash
git add themes/glitch/static/css/pygments-glitch.css
git commit -m "feat(theme): neon pygments stylesheet for code blocks"
```

---

### Task 5: Standalone page template

**Files:**
- Modify: `themes/glitch/templates/page.html`

- [ ] **Step 1: Replace `page.html`**

```jinja
{% extends 'base.html' %}
{% block title %}{{ page.title|striptags }} — {{ super() }}{% endblock %}
{% block content %}
<article class="post">
  <h1 class="glitch-title" data-txt="{{ page.title|striptags }}">{{ page.title }}</h1>
  <div class="post-content">
    {{ page.content }}
  </div>
</article>
{% endblock %}
```

- [ ] **Step 2: Build green**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Expected: green build (no pages exist yet, so nothing to assert beyond no error).

- [ ] **Step 3: Commit**

```bash
git add themes/glitch/templates/page.html
git commit -m "feat(theme): standalone page template"
```

---

### Task 6: Archives page

**Files:**
- Modify: `themes/glitch/templates/archives.html`

- [ ] **Step 1: Replace `archives.html`** (group posts by year as terminal log lines)

```jinja
{% extends 'base.html' %}
{% block title %}Archives — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="ARCHIVE">ARCHIVE</h1>
<p class="sectionlabel">{{ dates|length }} TRANSMISSIONS LOGGED</p>
<ul class="archive-list">
  {% set ns = namespace(year=0) %}
  {% for article in dates %}
  {% if article.date.year != ns.year %}{% set ns.year = article.date.year %}
  <li class="archive-year">{{ ns.year }}</li>
  {% endif %}
  <li class="archive-item"><span class="ts">{{ article.locale_date }}</span> <a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></li>
  {% endfor %}
</ul>
{% endblock %}
```

- [ ] **Step 2: Add archive list styling to `glitch.css`** (append)

```css
.archive-list{ list-style:none; padding:0; margin:18px 0 40px; }
.archive-year{ color:var(--mag); font-family:var(--disp); font-size:30px; margin:24px 0 8px; text-shadow:2px 0 var(--mag),-2px 0 var(--cyan); }
.archive-item{ display:flex; gap:14px; padding:6px 0; border-bottom:1px dashed rgba(5,217,232,.18); }
.archive-item .ts{ color:var(--grn); white-space:nowrap; font-size:13px; }
.archive-item a{ text-decoration:none; }
.archive-item a:hover{ color:var(--cyan2); text-shadow:1px 0 var(--mag),-1px 0 var(--cyan); }
```

- [ ] **Step 3: Build and verify**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `grep -c 'archive-item' output/archives.html`
Expected: `2`.

- [ ] **Step 4: Commit**

```bash
git add themes/glitch/templates/archives.html themes/glitch/static/css/glitch.css
git commit -m "feat(theme): archives page"
```

---

### Task 7: Category index + per-category pages

**Files:**
- Modify: `themes/glitch/templates/categories.html`
- Modify: `themes/glitch/templates/category.html`

- [ ] **Step 1: Replace `categories.html`**

```jinja
{% extends 'base.html' %}
{% block title %}Categories — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="CATEGORIES">CATEGORIES</h1>
<div class="chips chips-index">
  {% for category, arts in categories %}
  <a class="chip" href="{{ SITEURL }}/{{ category.url }}">{{ category }} <span class="count">{{ arts|length }}</span></a>
  {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 2: Replace `category.html`**

```jinja
{% extends 'base.html' %}
{% from '_includes/macros.html' import post_card with context %}
{% block title %}{{ category }} — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="{{ category|striptags }}">{{ category }}</h1>
<p class="sectionlabel">CATEGORY :: {{ articles|length }} posts</p>
{% for article in articles %}{{ post_card(article) }}{% endfor %}
{% endblock %}
```

- [ ] **Step 3: Add index-chip styling to `glitch.css`** (append)

```css
.chips-index{ margin:20px 0 40px; gap:12px; }
.chips-index .chip{ font-size:14px; padding:6px 12px; }
.chip .count{ color:var(--grn); margin-left:4px; }
```

- [ ] **Step 4: Build and verify**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `grep -c 'chip' output/categories.html && ls output/category/*.html`
Expected: chips present; per-category pages exist under `output/category/`.

- [ ] **Step 5: Commit**

```bash
git add themes/glitch/templates/categories.html themes/glitch/templates/category.html themes/glitch/static/css/glitch.css
git commit -m "feat(theme): category index and per-category pages"
```

---

### Task 8: Tag index + per-tag pages

**Files:**
- Modify: `themes/glitch/templates/tags.html`
- Modify: `themes/glitch/templates/tag.html`

- [ ] **Step 1: Replace `tags.html`**

```jinja
{% extends 'base.html' %}
{% block title %}Tags — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="TAGS">TAGS</h1>
<div class="chips chips-index">
  {% for tag, arts in tags|sort %}
  <a class="chip" href="{{ SITEURL }}/{{ tag.url }}">{{ tag }} <span class="count">{{ arts|length }}</span></a>
  {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 2: Replace `tag.html`**

```jinja
{% extends 'base.html' %}
{% from '_includes/macros.html' import post_card with context %}
{% block title %}#{{ tag }} — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="#{{ tag|striptags }}">#{{ tag }}</h1>
<p class="sectionlabel">TAG :: {{ articles|length }} posts</p>
{% for article in articles %}{{ post_card(article) }}{% endfor %}
{% endblock %}
```

- [ ] **Step 3: Build and verify**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `grep -c 'chip' output/tags.html && ls output/tag/*.html`
Expected: chips present; per-tag pages exist under `output/tag/`.

- [ ] **Step 4: Commit**

```bash
git add themes/glitch/templates/tags.html themes/glitch/templates/tag.html
git commit -m "feat(theme): tag index and per-tag pages"
```

---

### Task 9: Author index + per-author pages

**Files:**
- Modify: `themes/glitch/templates/authors.html`
- Modify: `themes/glitch/templates/author.html`

- [ ] **Step 1: Replace `authors.html`**

```jinja
{% extends 'base.html' %}
{% block title %}Authors — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="AUTHORS">AUTHORS</h1>
<div class="chips chips-index">
  {% for author, arts in authors %}
  <a class="chip" href="{{ SITEURL }}/{{ author.url }}">{{ author }} <span class="count">{{ arts|length }}</span></a>
  {% endfor %}
</div>
{% endblock %}
```

- [ ] **Step 2: Replace `author.html`**

```jinja
{% extends 'base.html' %}
{% from '_includes/macros.html' import post_card with context %}
{% block title %}{{ author }} — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="{{ author|striptags }}">{{ author }}</h1>
<p class="sectionlabel">AUTHOR :: {{ articles|length }} posts</p>
{% for article in articles %}{{ post_card(article) }}{% endfor %}
{% endblock %}
```

- [ ] **Step 3: Build and verify**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `ls output/author/*.html`
Expected: a per-author page exists.

- [ ] **Step 4: Commit**

```bash
git add themes/glitch/templates/authors.html themes/glitch/templates/author.html
git commit -m "feat(theme): author index and per-author pages"
```

---

### Task 10: Client-side search

**Files:**
- Create: `themes/glitch/templates/searchindex.html`
- Create: `themes/glitch/templates/search.html`
- Modify: `themes/glitch/static/js/glitch.js`
- Modify: `pelicanconf.py`

- [ ] **Step 1: Create `searchindex.html`** (emits JSON; no extends)

```jinja
[{% for a in articles %}{"title": {{ a.title|striptags|tojson }}, "url": {{ a.url|tojson }}, "summary": {{ a.summary|striptags|truncate(220)|tojson }}, "category": {{ (a.category.name if a.category else "")|tojson }}, "tags": [{% for t in a.tags %}{{ t.name|tojson }}{% if not loop.last %}, {% endif %}{% endfor %}], "date": {{ a.locale_date|tojson }}}{% if not loop.last %},{% endif %}{% endfor %}]
```

- [ ] **Step 2: Create `search.html`**

```jinja
{% extends 'base.html' %}
{% block title %}Search — {{ super() }}{% endblock %}
{% block content %}
<h1 class="glitch-title" data-txt="SEARCH">SEARCH</h1>
<div class="search-box">
  <span class="ps1">guest@xlyk:~$ grep</span>
  <input id="q" type="search" autocomplete="off" placeholder="query…" aria-label="Search posts">
  <span class="cur" aria-hidden="true"></span>
</div>
<p id="search-status" class="search-status" aria-live="polite">type to search {{ articles|length }} posts</p>
<div id="search-results" class="search-results"></div>
{% endblock %}
```

- [ ] **Step 3: Replace `static/js/glitch.js`** with reduced-motion + search

```js
(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('reduced-motion');
  }

  var input = document.getElementById('q');
  if (!input) return;

  var statusEl = document.getElementById('search-status');
  var resultsEl = document.getElementById('search-results');
  var index = [];

  fetch('search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; })
    .catch(function () { if (statusEl) statusEl.textContent = 'search index unavailable'; });

  function score(item, terms) {
    var hay = (item.title + ' ' + item.tags.join(' ') + ' ' + item.summary + ' ' + item.category).toLowerCase();
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      if (item.title.toLowerCase().indexOf(terms[i]) !== -1) s += 3;
      if (hay.indexOf(terms[i]) !== -1) s += 1; else return 0;
    }
    return s;
  }

  function render(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { resultsEl.innerHTML = ''; statusEl.textContent = 'type to search ' + index.length + ' posts'; return; }
    var hits = index.map(function (it) { return { it: it, s: score(it, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s; });
    statusEl.textContent = hits.length + ' match' + (hits.length === 1 ? '' : 'es');
    resultsEl.innerHTML = hits.map(function (x) {
      var it = x.it;
      var chips = it.tags.map(function (t) { return '<span class="chip">' + t + '</span>'; }).join('');
      return '<article class="card"><div class="pmeta"><span class="ts">' + it.date + '</span>' +
        (it.category ? '<span class="cat">' + it.category + '</span>' : '') + '</div>' +
        '<h2 class="card-title"><a href="' + it.url + '">' + it.title + '</a></h2>' +
        '<p class="sum">' + it.summary + '</p><div class="chips">' + chips + '</div></article>';
    }).join('');
  }

  input.addEventListener('input', function () { render(input.value); });
})();
```

- [ ] **Step 4: Register the direct templates in `pelicanconf.py`** — replace the `DIRECT_TEMPLATES` line and add save-as settings:

```python
DIRECT_TEMPLATES = ["index", "categories", "authors", "tags", "archives", "search", "searchindex"]
SEARCH_SAVE_AS = "search.html"
SEARCHINDEX_SAVE_AS = "search-index.json"
```

- [ ] **Step 5: Build and verify search artifacts**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `test -f output/search.html && python3 -c "import json; json.load(open('output/search-index.json')); print('valid json,', len(json.load(open('output/search-index.json'))), 'items')"`
Expected: `search.html` exists; prints `valid json, 2 items`.

- [ ] **Step 6: Lint (pelicanconf.py changed)**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: no errors.

- [ ] **Step 7: Commit**

```bash
git add themes/glitch/templates/searchindex.html themes/glitch/templates/search.html themes/glitch/static/js/glitch.js pelicanconf.py
git commit -m "feat(theme): dependency-free client-side search"
```

---

### Task 11: Custom 404

**Files:**
- Create: `themes/glitch/templates/notfound.html`
- Modify: `pelicanconf.py`

- [ ] **Step 1: Create `notfound.html`**

```jinja
{% extends 'base.html' %}
{% block title %}404 — {{ super() }}{% endblock %}
{% block content %}
<section class="notfound">
  <p class="status-bar"><span class="sig">▓ SIGNAL_LOST :: 404</span></p>
  <h1 class="glitch-title" data-txt="404">404</h1>
  <p>This page dropped off the wire.</p>
  <p><a href="{{ SITEURL }}/">&larr; return home</a> &nbsp;·&nbsp; <a href="{{ SITEURL }}/search.html">search the archive</a></p>
</section>
{% endblock %}
```

- [ ] **Step 2: Register in `pelicanconf.py`** — add `notfound` to direct templates and set its save-as. Update the `DIRECT_TEMPLATES` line and add the setting:

```python
DIRECT_TEMPLATES = ["index", "categories", "authors", "tags", "archives", "search", "searchindex", "notfound"]
NOTFOUND_SAVE_AS = "404.html"
```

- [ ] **Step 3: Build and verify**

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory`
Run: `test -f output/404.html && grep -c 'SIGNAL_LOST' output/404.html`
Expected: `output/404.html` exists; grep returns `1`.

- [ ] **Step 4: Lint (pelicanconf.py changed)**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add themes/glitch/templates/notfound.html pelicanconf.py
git commit -m "feat(theme): glitch 404 page"
```

---

### Task 12: Production build parity + docs + final verification

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Production build parity** — confirm the prod settings build everything (feeds, sitemap, the new direct templates) with absolute URLs.

Run: `PYTHONPATH=. uv run pelican content -o output -s publishconf.py --delete-output-directory`
Expected: green build. Then:
Run: `ls output/index.html output/404.html output/search.html output/search-index.json output/feeds/all.atom.xml output/sitemap.xml output/archives.html output/categories.html output/tags.html output/authors.html`
Expected: all exist.
Run: `grep -c 'https://xlyk.github.io/theme/css/glitch.css' output/404.html`
Expected: `1` (404 references absolute asset URLs so it works when served from any path).

- [ ] **Step 2: Visual confirmation** — run the dev server and eyeball.

Run: `uv run pelican content -o output -s pelicanconf.py --delete-output-directory && uv run pelican --listen --port 8000` (then open http://localhost:8000)
Check: home (cards, pagination label, hero channel-split), the DSPy article (neon code block, TOC box, table, blockquote, reading time), `/search.html` (type "dspy" → 1 result), `/404.html`, `/archives.html`, `/categories.html`, `/tags.html`. Then toggle OS "reduce motion" and reload — animations stop, scanlines dim, text stays readable. Stop the server when done.

- [ ] **Step 3: Update `CLAUDE.md`** — replace the Elegant references so docs match reality. Change the intro line and the theme/gotcha sections:
  - Intro: "The site uses the Elegant theme (installed as a git submodule)" → "The site uses a custom `Glitch` theme at `themes/glitch/` (plain directory, not a submodule)."
  - Theme Management section: replace the submodule-update instructions with: "The theme is a plain directory at `themes/glitch/`. Edit templates in `themes/glitch/templates/` and styles in `themes/glitch/static/css/` directly."
  - Static File Handling: note that site styling now lives in the theme's `glitch.css` / `pygments-glitch.css`; `content/extra/custom.css` remains an optional override hook.
  - Gotchas: replace "Initialize the theme submodule after cloning" with a note that the theme is vendored in-repo (no submodule init needed); keep the `publishconf.py` PYTHONPATH gotcha.

- [ ] **Step 4: Lint (CLAUDE.md is not Python, but confirm nothing else regressed)**

Run: `uv run ruff check . && uv run ruff format --check .`
Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: point CLAUDE.md at the new glitch theme"
```

---

## Self-review notes

- **Spec coverage:** base/overlays/nav/footer (T1); design tokens + ported CSS (T1); paginated home (T2); article w/ meta+reading-time+TOC+content (T3); Pygments neon (T4); page (T5); archives (T6); categories+category (T7); tags+tag (T8); authors+author (T9); dependency-free search (T10); 404 (T11); prod parity + a11y/reduced-motion + docs (T1 CSS + T12). All spec sections map to a task.
- **Reduced-motion / contrast / focus:** shipped in the CSS net-new block in T1, exercised in T12 Step 2.
- **No new dependencies:** reading time and search are in-template / vanilla JS; confirmed against CLAUDE.md's "ask before adding dependencies."
- **Build-green invariant:** stubs in T1 satisfy Pelican's required-template set (article/page/category/tag/author + default direct templates), so every later task rebuilds clean.
