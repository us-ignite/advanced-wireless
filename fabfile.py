import functools
import os

from datetime import datetime
from fabric.api import local, env, lcd, task
from fabric.colors import yellow, red, green
from fabric.contrib import console

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
here = lambda *x: os.path.join(PROJECT_ROOT, *x)

DB_STRING = 'us_ignite'


@task
def production():
    """Connection details for the ``production`` app"""
    env.slug = 'production'
    env.url = 'https://us-ignite.org/'
    env.app = 'us-ignite'


@task
def staging():
    """Connection details for the ``production`` app"""
    env.slug = 'staging'
    env.url = 'https://us-ignite-staging.herokuapp.com/'
    env.app = 'us-ignite-staging'


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


def run_command(command):
    dj_heroku(command, env.app, env.slug)


def production_confirmation(function):
    """Ask for confirmation for commants in the production environment."""
    @functools.wraps(function)
    def wrapper(confirmation='', *args, **kwargs):
        confirmation = False if confirmation == 'False' else True
        SLUG = env.slug.upper()
        if env.slug not in ['production', 'staging']:
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


@task
@only_outside_vm
def syncdb():
    """Syncs the remote environment database."""
    print yellow('Syncing %s database.' % env.slug.upper())
    dj_heroku('syncdb --noinput', env.app, env.slug)
    dj_heroku('migrate --noinput', env.app, env.slug)


@task
@only_outside_vm
def collectstatic():
    """Collects the remote environment static assets."""
    print yellow('Collecting static assets.')
    dj_heroku('collectstatic --noinput '
              '--ignore=admin --ignore=tiny_mce '
              '--ignore=*.scss',
              env.app, env.slug)


@task
@only_outside_vm
def shell():
    """Open a shell in the given environment."""
    dj_heroku('shell', env.app, env.slug)


@task
@only_outside_vm
def buildwatson():
    """Build remote watson full-text search corpus."""
    dj_heroku('buildwatson', env.app, env.slug)


@task
@only_outside_vm
def backupdb(snapshot=False):
    """Downloads a backup from the remote DB."""
    if snapshot:
        print yellow('Generate DB snapshot.')
        run_heroku('pgbackups:capture', env.app, env.slug)
    print yellow('Downloading DB backup.')
    url = run_heroku('pgbackups:url', env.app, env.slug)
    filename = '%s.dump' % datetime.now().strftime('%Y%m%d-%H%M')
    local('wget -O %s "%s"' % (filename, url))
    print green('%s' % filename)


@task
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
        # Index the content
        buildwatson()
    print yellow('URL: %s' % env.url)
    print green('Done at %s' % datetime.now())


@task
@only_outside_vm
def migrate_apps(url):
    """Imports Mozilla Ignite apps to the remote environment."""
    confirmation = red(
        'You are about to import the Mozilla Ignite apps. Proceed?')
    if console.confirm(confirmation):
        dj_heroku('app_import %s' % url, env.app, env.slug)
        print green('Done at %s' % datetime.now())
    else:
        print yellow('Phew, aborted.')
        exit(1)


@task
@only_outside_vm
def load_fixtures():
    """Loads the initial fixtures in the remote environment."""
    confirmation = red('You are about to IRREVERSIBLY add fixtures to the'
                       ' remote database. Procceed?')
    if console.confirm(confirmation):
        dj_heroku('app_load_fixtures', env.app, env.slug)
        dj_heroku('awards_load_fixtures', env.app, env.slug)
        dj_heroku('common_load_fixtures', env.app, env.slug)
        dj_heroku('snippets_load_fixtures', env.app, env.slug)
        dj_heroku('events_load_fixtures', env.app, env.slug)
        dj_heroku('resources_load_fixtures', env.app, env.slug)
        dj_heroku('testbeds_load_fixtures', env.app, env.slug)
        dj_heroku('sections_load_fixtures', env.app, env.slug)
        dj_heroku('blog_import', env.app, env.slug)
        buildwatson()
    else:
        print yellow('Phew, aborted.')
        exit(1)


@task
@only_outside_vm
def create_superuser():
    """Create a superuser in the remote environment."""
    confirmation = yellow('Would you like to generate an admin user?')
    if console.confirm(confirmation):
        dj_heroku('createsuperuser', env.app, env.slug)


@task
@only_inside_vm
def test(apps=''):
    """Runs the test suite in the local environment."""
    local('django-admin.py test %s '
          '--settings=us_ignite.settings.testing' % apps)


@only_inside_vm
def drop_local_db(db_name=DB_STRING):
    """Removes the local development database."""
    print yellow('Droping and creating a new DB.')
    local('PGPASSWORD=%(db)s dropdb %(db_name)s -U %(db)s -h localhost'
          % {'db': DB_STRING, 'db_name': db_name})
    local("PGPASSWORD=%(db)s createdb %(db_name)s -T template0 "
          "-E UTF-8 -l en_US.UTF-8 -O %(db)s -U %(db)s -h localhost"
          % {'db': DB_STRING, 'db_name': db_name})


@task
@only_inside_vm
def loaddb(db_name):
    message = red("This will irreversible destroy the database. Proceed?")
    if not console.confirm(message):
        print yellow('Phew, aborted.')
        return exit(1)
    with lcd(PROJECT_ROOT):
        drop_local_db()
        db_path = here(db_name)
        db_name = '%s' % DB_STRING
        conn = ('PGPASSWORD=%(db)s pg_restore -n public --no-acl '
                '--no-owner -h localhost -U %(db)s -d %(db_name)s'
                % {'db': DB_STRING, 'db_name': db_name})
        try:
            local('%s %s' % (conn, db_path))
        except Exception, e:
            print red('Failure while importing the DB. Check the output from'
                      ' the command.')
            exit(2)
    print green('Done')

@task
@only_inside_vm
def reset_local_db():
    """Resets the local development environment database.

    Check the database has the right UTF8 encoding before running this command.
    ``sudo -u postgres psql --listsudo -u postgres psql --list``
    """
    confirmation = red('You are about to IRREVERSIBLY clear the existing'
                       ' local database. Procceed?')
    if console.confirm(confirmation):
        drop_local_db()
        local('django-admin.py syncdb --noinput '
              '--settings=%s.settings.local' % DB_STRING)
        local('django-admin.py migrate --noinput '
              '--settings=%s.settings.local' % DB_STRING)
    else:
        print yellow('Phew, aborted.')
        exit(1)
    confirmation = yellow('Would you like to generate an admin user?')
    if console.confirm(confirmation):
        local('django-admin.py createsuperuser '
              '--settings=%s.settings.local' % DB_STRING)
    confirmation = red('Would you like to generate dummy fixtures?')
    if console.confirm(confirmation):
        local('django-admin.py dummy_generate_content --noinput '
              '--settings=%s.settings.local' % DB_STRING)


@task
@only_inside_vm
def build():
    """Runs any Front end task required by the build."""
    with lcd(here('.')):
        local('grunt sass')

@task
@only_outside_vm
def dummy_data():
    """Loads dummy data in the remote environment."""
    confirmation = yellow('Would you like to generate an admin user?')
    if console.confirm(confirmation):
        dj_heroku('createsuperuser', env.app, env.slug)
    confirmation = red('Would you like to generate dummy fixtures?')
    if console.confirm(confirmation):
        dj_heroku('dummy_generate_content', env.app, env.slug)
    print green('Done.')


ADMIN_APPS = {
    'apps': ['application', 'domain', 'feature', 'page'],
    'auth': ['user'],
    'awards': ['applicationaward', 'award', 'hubaward', 'useraward'],
    'blog': ['bloglink', 'post'],
    'challenges': ['challenge', 'entry'],
    'events': ['audience', 'event'],
    'hubs': ['hubactivity', 'hubrequest', 'hub'],
    'maps': ['category', 'location'],
    'news': ['article'],
    'organizations': ['organization'],
    'profiles': ['profile'],
    'resources': ['resourcetype', 'resource', 'sector'],
    'sections': ['sectionpage', 'sponsor'],
    'snippets': ['snippet'],
    'taggit': ['tag'],
    'testbeds': ['networkspeed', 'testbed'],
    'uploads': ['image', 'upload'],
}

def _get_path_urls(app, model_list):
    path_urls = []
    for model in model_list:
        prefix = '/admin/%s/%s' % (app, model)
        for p in ['/', '/add/']:
            path_urls.append('%s%s' % (prefix, p))
    return path_urls


def _get_admin_paths():
    path_list = []
    for app, model_list in ADMIN_APPS.items():
        path_list += _get_path_urls(app, model_list)
    return path_list


def _snapshot_path(path):
    path = '/home/' if path == '/' else path
    return 'snapshots/%s.png' % path[1:-1].replace('/', '--')


@task
@only_inside_vm
def generate_snapshots():
    """Generate several snapshots"""
    SITE_URL = 'http://local-us-ignite.org'
    _url = lambda p: '%s%s' % (SITE_URL, p)
    path_list = [
        '/',
        '/admin/',
        '/admin/auth/user/312/',
        '/about/what-is-us-ignite/',
        '/get-involved/involve-developers/',
        '/apps/',
        '/apps/add/',
        '/apps/MI-2/',
        '/apps/MI-2/edit/',
        '/apps/MI-2/membership/',
        '/apps/MI-2/hubs-membership/',
        '/admin/apps/application/168/',
        '/overview/',
        '/apps/stage/1/',
        '/hub/',
        '/hub/apply/',
        '/admin/hubs/hubrequest/4/',
        '/admin/hubs/hubrequest/approve/4/',
        '/testbed/',
        '/event/',
        '/challenges/',
        '/org/',
        '/resources/',
        '/resources/add/',
        '/blog/',
        '/people/a3BKDCioVuC57TckDt8Rob/',
        '/contact/a3BKDCioVuC57TckDt8Rob/',
        '/dashboard/',
        '/accounts/profile/',
    ] + _get_admin_paths()
    with lcd(here('.')):
        for path in path_list:
            local('phantomjs screenshots.js %s %s' %
                  (_url(path), _snapshot_path(path)))
