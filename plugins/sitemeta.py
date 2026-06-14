"""Expose site stats (post count, last-updated date) as template globals."""

from pelican import signals


def set_site_meta(generator):
    articles = generator.articles
    generator.context["POST_COUNT"] = len(articles)
    generator.context["LAST_UPDATED"] = (
        max(articles, key=lambda a: a.date).date.strftime("%Y-%m-%d") if articles else ""
    )
    # settings["SITEURL"] keeps the absolute value even when RELATIVE_URLS relativizes
    # the SITEURL template global to "." in dev.
    generator.context["SITE_HOST"] = (
        generator.settings.get("SITEURL", "").split("://")[-1].rstrip("/")
    )


def register():
    signals.article_generator_finalized.connect(set_site_meta)
