from django.utils.text import Truncator


def truncatewords(value, length):
    """Truncates the given sequence of words with the given length."""
    return Truncator(value).words(length, truncate=' ...')
