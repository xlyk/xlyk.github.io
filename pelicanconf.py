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
        "extra",        # tables, etc.
        "codehilite",   # syntax highlighting
        "toc",          # table of contents
    ],
    "extension_configs": {
        "codehilite": {"css_class": "highlight"},
        "toc": {"permalink": True},
    },
}

# Static files
STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    # Example: add a robots.txt by placing it in content/extra/robots.txt
    # "extra/robots.txt": {"path": "robots.txt"},
    # Example: if you add a custom domain, place CNAME in content/extra/CNAME
    # "extra/CNAME": {"path": "CNAME"},
}

THEME = "themes/elegant"  # Using Elegant theme

# Dev convenience
RELATIVE_URLS = True
