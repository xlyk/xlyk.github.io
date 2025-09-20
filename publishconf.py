import os
from pelicanconf import *  # noqa: F401,F403

SITEURL = "https://xlyk.github.io"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

# Production-only settings can go here (analytics, sitemaps, etc.)
# Example for sitemap plugin if added later:
# PLUGIN_PATHS = ["pelican-plugins"]
# PLUGINS = ["sitemap"]
# SITEMAP = {"format": "xml"}
