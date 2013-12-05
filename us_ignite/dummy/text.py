from random import choice

from django.conf import settings


words = open(settings.WORDS_PATH, "r").readlines()


def random_words(total):
    return " ".join([choice(words).lower().rstrip() for i in range(total)])


def random_paragraphs(total, word_no=30):
    return ".\n\n".join([random_words(word_no) for i in range(total)])
