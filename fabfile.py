import functools
import os

from datetime import datetime
from fabric.api import local, env, lcd
from fabric.colors import yellow, red, green
from fabric.contrib import console

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.join(PROJECT_ROOT, *x)


def production():
    """Connection details for the ``production`` app"""
    env.slug = 'production'
    env.url = 'http://us-ignite.herokuapp.com/'
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
            print red('Command can only be OUTSIDE the VM.')
            return exit(1)
        return function(*args, **kwargs)
    return inner


def only_inside_vm(function):
    """Decorator to allow only ``outside`` VM commands"""
    @functools.wraps(function)
    def inner(*args, **kwargs):
        if not IS_VM:
            print red('Command can only be INSIDE the VM.')
            return exit(1)
        return function(*args, **kwargs)
    return inner


def dj_heroku(command, slug, capture=False):
    """Runs a given django management command in the given Heroku's app."""
    new_cmd = ('heroku run django-admin.py %s --settings=us_ignite.'
               'settings.%s --remote %s' % (command, slug, slug))
    return local(new_cmd, capture)


def run_heroku(cmd, slug, capture=True):
    """Runs a Heroku command with the given ``remote``"""
    return local('heroku %s --app %s' % (cmd, slug), capture=capture)


@only_outside_vm
def syncdb():
    print yellow('Syncing %s database.' % env.slug)
    dj_heroku('syncdb --noinput', env.slug)


@only_outside_vm
def shell():
    """Open a shell in the given environment."""
    dj_heroku('shell', env.slug)


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
        _validate_pushed_commits()
        local('git push %s master' % env.slug)
        syncdb()
    print yellow('URL: %s' % env.url)
    print red('Done! - %s' % datetime.now())


@only_inside_vm
def test(apps=''):
    """Runs the test suite."""
    local('django-admin.py test %s '
          '--settings=us_ignite.settings.testing' % apps)
