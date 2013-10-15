# Testing settings for us_ignite
from us_ignite.settings import *


SECRET_KEY = 'c!lizso+53#4dhm*o2qyh9t(n14p#wr5!+%1bfjtrqa#vsc$@h'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'us-ignite-test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


INSTALLED_APPS += (
    'django_nose',
)

EXCLUDED_APPS = (
    'south',
)

INSTALLED_APPS = filter(lambda a: a not in EXCLUDED_APPS, INSTALLED_APPS)


NOSE_ARGS = [
    '-s',
    '--failed',
    '--stop',
    '--nocapture',
    '--failure-detail',
    '--with-progressive',
    '--logging-filter=-south',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# ignore South
SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Faster tests with the MD5hasher.
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
