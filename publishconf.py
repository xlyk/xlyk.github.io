from pelicanconf import *  # noqa: F401,F403

SITEURL = "https://xlyk.github.io"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True

PLUGINS = ["pelican.plugins.sitemap"]
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.7, "pages": 0.5, "indexes": 0.5},
    "changefreqs": {"articles": "weekly", "pages": "monthly", "indexes": "daily"},
}
