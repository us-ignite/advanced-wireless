from random import choice

from django.conf import settings
from django.utils.encoding import smart_text


words = open(settings.WORDS_PATH, "r").readlines()


def random_words(total):
    return u" ".join([smart_text(choice(words).lower().rstrip()) for i in range(total)])


def random_paragraphs(total, word_no=30):
    return u".\n\n".join([random_words(word_no) for i in range(total)])
