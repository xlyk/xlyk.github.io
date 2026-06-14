"""Tag Pygments code blocks with their source fence language.

Pelican's codehilite emits ``<div class="highlight">`` with no language hint.
This reads the content source, pulls the ordered list of fenced-code languages,
and injects ``data-lang`` into each highlight block -- but only when the counts
line up, so a mismatch never mislabels a block.
"""

import re

from pelican import signals

FENCE_LANG = re.compile(r"^[ \t]*(?:```|~~~)[ \t]*([A-Za-z0-9_+-]+)\s*$", re.M)
HIGHLIGHT = re.compile(r'<div class="highlight">')


def add_lang_labels(instance):
    content = getattr(instance, "_content", None)
    source = getattr(instance, "source_path", None)
    if not content or not source or 'class="highlight"' not in content:
        return
    try:
        with open(source, encoding="utf-8") as handle:
            langs = FENCE_LANG.findall(handle.read())
    except OSError:
        return
    if not langs or len(langs) != len(HIGHLIGHT.findall(content)):
        return  # ambiguous -- leave every block unlabeled rather than risk a mislabel
    seq = iter(langs)
    instance._content = HIGHLIGHT.sub(
        lambda _match: f'<div class="highlight" data-lang="{next(seq)}">', content
    )


def register():
    signals.content_object_init.connect(add_lang_labels)
