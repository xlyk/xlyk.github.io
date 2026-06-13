# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is a Pelican-powered static blog hosted on GitHub Pages at https://xlyk.github.io. The site uses the Elegant theme (installed as a git submodule) and is automatically built and deployed via GitHub Actions when changes are pushed to the main branch. Python 3.13+ is required (`.python-version`, `requires-python` in `pyproject.toml`).

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
- `themes/elegant` - Theme submodule providing templates and styling

### Build Pipeline
1. GitHub Actions workflow (`.github/workflows/pelican.yml`) triggers on push to main branch
2. Installs pinned dependencies with `uv sync --frozen` (from `uv.lock`)
3. Runs `ruff` lint/format checks, then builds the site using `publishconf.py` settings
4. Deploys output directory to GitHub Pages

### Theme Management
The Elegant theme is included as a git submodule. To update:
```bash
git submodule update --remote themes/elegant
```

### Markdown Configuration
The site uses enhanced Markdown processing with:
- `extra` extension for tables and additional formatting
- `codehilite` for syntax highlighting in code blocks
- `toc` for automatic table of contents generation with permalinks

### Static File Handling
Files in `STATIC_PATHS` (`images/`, `extra/`) are copied directly to output. Use `EXTRA_PATH_METADATA` in pelicanconf.py to control output paths for special files like CNAME or robots.txt.

Site styling overrides live in `content/extra/custom.css`, copied to `static/custom.css` and pulled in by the theme via `CUSTOM_CSS`. Put CSS tweaks there rather than editing the theme submodule.

### Production-only settings
Sitemap generation (`pelican.plugins.sitemap`) and Atom feeds (`FEED_ALL_ATOM`, `CATEGORY_FEED_ATOM`) are defined only in `publishconf.py`. A dev build with `pelicanconf.py` produces neither — build with `publishconf.py` to exercise them locally.

## Gotchas

- **`publishconf.py` needs the repo root importable.** It begins with `from pelicanconf import *`, so building with it requires the repo root on `PYTHONPATH`. From the repo root locally this usually resolves; CI sets `PYTHONPATH=$GITHUB_WORKSPACE` and passes an absolute path to `publishconf.py`. A `ModuleNotFoundError: pelicanconf` means the import path is wrong, not a missing dependency.
- **Initialize the theme submodule after cloning.** Run `git submodule update --init --recursive`, or the build fails because `themes/elegant` is empty.
- **Deployment serves the `output/` artifact, not the repo root.** The stray root-level `index.html` is vestigial and never published — editing it has no effect on the live site.
