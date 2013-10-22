# Production settings for us_ignite
import os

from us_ignite.settings import *

# Sensitive values are saved as env variables:
env = os.getenv
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# settings is one directory up now
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)

SITE_URL = 'http://us-ignite.herokuapp.com'

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')

# Basic authentication for Heroku
BASIC_WWW_AUTHENTICATION_USERNAME = env('WWW_USERNAME')
BASIC_WWW_AUTHENTICATION_PASSWORD = env('WWW_PASSWORD')
BASIC_WWW_AUTHENTICATION = False

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# Settings to use the filesystem

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'
