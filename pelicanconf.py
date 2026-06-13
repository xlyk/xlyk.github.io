AUTHOR = "Kyle Hanks"
SITENAME = "Kyle's blog"
SITEURL = "https://xlyk.github.io"

PATH = "content"
TIMEZONE = "UTC"
DEFAULT_LANG = "en"

DEFAULT_PAGINATION = 10

# Markdown extensions (optional)
MARKDOWN = {
    "extensions": [
        "extra",  # tables, etc.
        "codehilite",  # syntax highlighting
        "toc",  # table of contents
    ],
    "extension_configs": {
        "codehilite": {"css_class": "highlight"},
        "toc": {"permalink": True},
    },
}

# Static files
STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    # Example: if you add a custom domain, place CNAME in content/extra/CNAME
    # "extra/CNAME": {"path": "CNAME"},
    "extra/custom.css": {"path": "static/custom.css"},
}

THEME = "themes/glitch"  # Custom Glitch theme (plain directory, not a submodule)

# Direct (non-article) templates the Glitch theme renders.
DIRECT_TEMPLATES = [
    "index",
    "categories",
    "authors",
    "tags",
    "archives",
    "search",
    "searchindex",
    "notfound",
]
SEARCH_SAVE_AS = "search.html"
SEARCHINDEX_SAVE_AS = "search-index.json"
NOTFOUND_SAVE_AS = "404.html"

# Dev convenience
RELATIVE_URLS = True
