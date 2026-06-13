# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is a Pelican-powered static blog hosted on GitHub Pages at https://xlyk.github.io. The site uses a custom `Glitch` theme at `themes/glitch/` (a plain directory, not a submodule) and is automatically built and deployed via GitHub Actions when changes are pushed to the main branch. Python 3.13+ is required (`.python-version`, `requires-python` in `pyproject.toml`).

There is no test suite. "Verification" means the three checks CI runs: `ruff check .`, `ruff format --check .`, and a clean `pelican` build with `publishconf.py`.

## Essential Commands

### Development Environment Setup
Dependencies are managed with [uv](https://docs.astral.dev/uv/) (`pyproject.toml` + `uv.lock`).
```bash
# Create the virtual environment and install pinned dependencies
uv sync
```

### Linting
Linting and formatting use [ruff](https://docs.astral.sh/ruff/) (config in `pyproject.toml`).
```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run ruff check --fix .    # auto-fix lint issues
```
CI runs `ruff check .` **and** `ruff format --check .` — the build fails on unformatted code, so run `ruff format .` before pushing. The `themes/` and `output/` directories are excluded from linting (`extend-exclude` in `pyproject.toml`).

### Content Development
Prefix commands with `uv run` to use the project environment.
```bash
# Generate site with development settings (includes relative URLs)
uv run pelican content -o output -s pelicanconf.py

# Generate site with production settings (absolute URLs for GitHub Pages)
uv run pelican content -o output -s publishconf.py

# Run local development server
uv run pelican --listen --port 8000

# Auto-regenerate on file changes during development
uv run pelican --autoreload --listen

# Clean output directory before rebuilding
uv run pelican content -o output -s pelicanconf.py --delete-output-directory
```

### Content Management
- Blog posts go in `content/posts/` as Markdown files
- Static assets (images) go in `content/images/`
- Extra files (CNAME, robots.txt, etc.) go in `content/extra/`

### Markdown Post Format
Posts should include metadata headers:
```markdown
Title: Your Post Title
Date: YYYY-MM-DD HH:MM
Category: Category Name
Tags: tag1, tag2
Slug: url-friendly-slug
Summary: Brief description of the post

Post content goes here...
```

## Architecture & Configuration

### Key Files
- `pelicanconf.py` - Development configuration with relative URLs and local settings
- `publishconf.py` - Production configuration that imports from pelicanconf and overrides for GitHub Pages deployment
- `content/` - Source content directory containing all posts, pages, and static files
- `output/` - Generated static site (gitignored, auto-generated)
- `themes/glitch/` - Custom Glitch theme: `templates/` (Jinja2) + `static/css/` (`glitch.css`, `pygments-glitch.css`) + `static/js/glitch.js`. Vendored in-repo, not a submodule.

### Build Pipeline
1. GitHub Actions workflow (`.github/workflows/pelican.yml`) triggers on push to main branch
2. Installs pinned dependencies with `uv sync --frozen` (from `uv.lock`)
3. Runs `ruff` lint/format checks, then builds the site using `publishconf.py` settings
4. Deploys output directory to GitHub Pages

### Theme Management
The `Glitch` theme is a plain directory at `themes/glitch/` — no submodule, no init step. Edit templates in `themes/glitch/templates/` and styles in `themes/glitch/static/css/` directly. The full visual language lives in `static/css/glitch.css` (the class-name contract shared across templates); `static/css/pygments-glitch.css` maps Pygments token classes to the neon palette; `static/js/glitch.js` handles the `prefers-reduced-motion` guard and the client-side search. Search is dependency-free: the `searchindex` direct template emits `search-index.json`, and `glitch.js` filters it. The design spec and implementation plan are under `docs/superpowers/`; the original aesthetic mockups are in `design-mockups/`.

### Markdown Configuration
The site uses enhanced Markdown processing with:
- `extra` extension for tables and additional formatting
- `codehilite` for syntax highlighting in code blocks
- `toc` for automatic table of contents generation with permalinks

### Static File Handling
Files in `STATIC_PATHS` (`images/`, `extra/`) are copied directly to output. Use `EXTRA_PATH_METADATA` in pelicanconf.py to control output paths for special files like CNAME or robots.txt.

Site styling lives in the theme's `themes/glitch/static/css/glitch.css` and `pygments-glitch.css` — edit those for visual tweaks. (`content/extra/custom.css` is still copied to `static/custom.css` as an optional override hook but is not linked by the theme.)

### Production-only settings
Sitemap generation (`pelican.plugins.sitemap`) and Atom feeds (`FEED_ALL_ATOM`, `CATEGORY_FEED_ATOM`) are defined only in `publishconf.py`. A dev build with `pelicanconf.py` produces neither — build with `publishconf.py` to exercise them locally.

## Gotchas

- **`publishconf.py` needs the repo root importable.** It begins with `from pelicanconf import *`, so building with it requires the repo root on `PYTHONPATH`. From the repo root locally this usually resolves; CI sets `PYTHONPATH=$GITHUB_WORKSPACE` and passes an absolute path to `publishconf.py`. A `ModuleNotFoundError: pelicanconf` means the import path is wrong, not a missing dependency.
- **The theme is vendored in-repo.** `themes/glitch/` is a normal directory — no `git submodule` init needed after cloning. (The old Elegant submodule may still be referenced in `.gitmodules`; it is no longer used by the build.)
- **Direct templates need registering.** Non-article pages (search, the JSON search index, the 404) are Pelican `DIRECT_TEMPLATES` with matching `*_SAVE_AS` settings in `pelicanconf.py`. Adding a new standalone page means adding both the template and its `DIRECT_TEMPLATES` entry, or Pelican won't render it.
- **Deployment serves the `output/` artifact, not the repo root.**
