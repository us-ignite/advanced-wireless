# Django settings for us_ignite project.
import os
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# settings is one directory up now
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)


# Heroku DB requirements
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = here('..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    here('assets'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_browserid.context_processors.browserid',
    'us_ignite.common.context_processors.settings_available',
)

ROOT_URLCONF = 'us_ignite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'us_ignite.wsgi.application'

TEMPLATE_DIRS = (
    here('templates'),
)

# Authentication:
AUTHENTICATION_BACKENDS = (
    'us_ignite.profiles.backends.authentication.EmailModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django_browserid',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'registration',
    'taggit',
    'us_ignite.common',
    'us_ignite.profiles',
    'us_ignite.people',
    'us_ignite.apps',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'heroku': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'us_ignite.common': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Storage settings, filesystem by default:
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'

# Message storage:
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Email settings:
EMAIL_SUBJECT_PREFIX = '[US Ignite] '
SEND_BROKEN_LINK_EMAILS = True
DEFAULT_FROM_EMAIL = 'info@us-ignite.org'

ALLOWED_HOSTS = [
    'local-us-ignite.org',
    'us-ignite.herokuapp.com',
]


# Account settings:
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = '/'
LOGOUT_REDIRECT_URL = '/'

# Paginator:
PAGINATOR_PAGE_SIZE = 10
