import markdown

from django.utils.encoding import force_text

from us_ignite.common.sanitizer import sanitize


def to_html(stream):
    """Transform an stream of markdown into safe HTML."""
    config = {
        'safe_mode': 'escape',
        'enable_attributes': False,
    }
    stream = force_text(stream)
    return sanitize(markdown.markdown(stream, ['nl2br'], **config))


def prepare_tags(tag_list):
    return [tag.lower() for tag in tag_list]
