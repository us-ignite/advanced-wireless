import bleach

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'p',
    'br',
    'h3',
    'h4',
    'h5',
    'h6',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
}

ALLOWED_STYLES = []


def sanitize(text):
    """Cleans the HTML received."""
    cleaned_text = bleach.clean(
        text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES, strip=True)
    return cleaned_text
