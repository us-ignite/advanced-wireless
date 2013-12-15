import functools
import os

from datetime import datetime
from fabric.api import local, env, lcd
from fabric.colors import yellow, red, green
from fabric.contrib import console

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.join(PROJECT_ROOT, *x)

DB_STRING = 'us_ignite'


def production():
    """Connection details for the ``production`` app"""
    env.slug = 'production'
    env.url = 'https://us-ignite.herokuapp.com/'
    env.app = 'us-ignite'


def is_vm():
    """Determines if the script is running in a VM"""
    return os.environ['USER'] == 'vagrant'

IS_VM = is_vm()


def only_outside_vm(function):
    """Decorator to allow only ``inside`` VM commands """
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if IS_VM:
            print red('Command can only be executed OUTSIDE the VM.')
            return exit(1)
        return function(*args, **kwargs)
    return inner


def only_inside_vm(function):
    """Decorator to allow only ``outside`` VM commands"""
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if not IS_VM:
            print red('Command can only be executed INSIDE the VM.')
            return exit(1)
        return function(*args, **kwargs)
    return inner


def dj_heroku(command, slug, environment, capture=False):
    """Runs a given django management command in the given Heroku's app."""
    new_cmd = ('heroku run django-admin.py %s --settings=us_ignite.'
               'settings.%s --app %s' % (command, environment, slug))
    return local(new_cmd, capture)


def run_heroku(cmd, slug, capture=True):
    """Runs a Heroku command with the given ``remote``"""
    return local('heroku %s --app %s' % (cmd, slug), capture=capture)


@only_outside_vm
def syncdb():
    print yellow('Syncing %s database.' % env.slug.upper())
    dj_heroku('syncdb --noinput', env.app, env.slug)


@only_outside_vm
def collectstatic():
    print yellow('Collecting static assets.')
    dj_heroku('collectstatic --noinput', env.app, env.slug)


@only_outside_vm
def shell():
    """Open a shell in the given environment."""
    dj_heroku('shell', env.app, env.slug)


def production_confirmation(function):
    """Production confirmation."""
    @functools.wraps(function)
    def wrapper(confirmation='', *args, **kwargs):
        confirmation = False if confirmation == 'False' else True
        SLUG = env.slug.upper()
        if env.slug not in ['production']:
            print red('Invaid destination: %s.' % SLUG)
            exit(3)
        if confirmation and env.slug == 'production':
            msg = red('You are about to DEPLOY %s to Heroku. Procceed?' % SLUG)
            if not console.confirm(msg):
                print yellow('Phew, aborted.')
                exit(2)
        return function(confirmation, *args, **kwargs)
    return wrapper


def _validate_pushed_commits():
    with lcd(PROJECT_ROOT):
        result = local('git log --pretty=format:"%h %s" origin/master..HEAD',
                       capture=True)
        if not result:
            return True
        print red('FAILURE: There are unpushed commits to origin/master.')
        print yellow('Make sure these commits are pushed before '
                     'deploying to heroku:')
        print yellow(result)
        exit(4)


@only_outside_vm
@production_confirmation
def deploy(confirmation):
    """Deploys the given build."""
    SLUG = env.slug.upper()
    print yellow('Deploying to %s. Because you said so.' % SLUG)
    with lcd(PROJECT_ROOT):
        print yellow('Pushing changes to %s in Heroku.' % SLUG)
        # Make sure the remote and Heroku are in sync:
        _validate_pushed_commits()
        local('git push %s master' % env.slug)
        # Sync database:
        syncdb()
        # Collect any static assets:
        collectstatic()
    print yellow('URL: %s' % env.url)
    print green('Done at %s' % datetime.now())


@only_inside_vm
def test(apps=''):
    """Runs the test suite."""
    local('django-admin.py test %s '
          '--settings=us_ignite.settings.testing' % apps)


@only_inside_vm
def drop_local_db():
    """Removes the local development database."""
    print yellow('Droping and creating a new DB.')
    local('PGPASSWORD=%(db)s dropdb %(db)s -U %(db)s -h localhost'
          % {'db': DB_STRING})
    local("PGPASSWORD=%(db)s createdb %(db)s -T template0 -E UTF-8 "
          "-l en_US.UTF-8 -O %(db)s -U %(db)s -h localhost"
          % {'db': DB_STRING})


@only_inside_vm
def reset_local_db():
    """Resets the local development DB
    Check the database has the right UTF8 encoding before running this command.
    sudo -u postgres psql --listsudo -u postgres psql --list
    """
    confirmation = red('You are about to IRREVERSIBLY clear the existing'
                       ' local database. Procceed?')
    if console.confirm(confirmation):
        drop_local_db()
        local('django-admin.py syncdb --noinput '
              '--settings=%s.settings.local' % DB_STRING)
        # local('django-admin.py migrate --noinput '
        #       '--settings=%s.settings.local' % DB_STRING)
    else:
        print yellow('Phew, aborted.')
        exit(1)


@only_inside_vm
def docs():
    """Generates Sphinx documentation."""
    with lcd(here('docs')):
        local('make html')


@only_outside_vm
def load_fixtures():
    confirmation = red('You are about to IRREVERSIBLY add fixtures to the'
                       ' remote database. Procceed?')
    if console.confirm(confirmation):
        dj_heroku('app_load_fixtures', env.app, env.slug)
        dj_heroku('awards_load_fixtures', env.app, env.slug)
        dj_heroku('common_load_fixtures', env.app, env.slug)
    else:
        print yellow('Phew, aborted.')
        exit(1)

