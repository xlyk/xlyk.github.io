"""Set newer/older neighbor links on each article (vendored, no external dep)."""

from pelican import signals


def add_neighbors(generator):
    articles = generator.articles  # newest-first
    count = len(articles)
    for i, article in enumerate(articles):
        article.newer_article = articles[i - 1] if i > 0 else None
        article.older_article = articles[i + 1] if i + 1 < count else None


def register():
    signals.article_generator_finalized.connect(add_neighbors)
