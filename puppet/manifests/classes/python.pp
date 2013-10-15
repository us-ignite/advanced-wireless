# Install python and compiled modules for project
class python ($project_path){
  $packages = [
               "python2.7-dev",
               "python2.7",
               "python-setuptools",
               "python2.7-imaging",
               "python2.7-wsgi-intercept",
               "python2.7-lxml",
               'python2.7-psycopg2',
               'libmemcached-dev',
               'zlib1g-dev',
               'libssl-dev',
               'libevent-dev',
               'libjpeg8',
               'libjpeg8-dev',
               ]
  package { $packages:
    ensure => installed,
  }

  exec { "pip":
    command => "easy_install pip",
    require => Package[$packages],
  }

  exec { "virtualenvwrapper":
    command => "pip install virtualenv virtualenvwrapper",
    require => Exec["pip"];
  }

  exec { "pip-install":
    cwd => "$project_path",
    command => "pip install -r $project_path/requirements.txt",
    timeout => 10000,
    require => Exec["virtualenvwrapper"];
  }

  exec { "pip-install-dev":
    cwd => "$project_path",
    command => "pip install -r $project_path/requirements_development.txt",
    timeout => 10000,
    require => Exec["virtualenvwrapper"];
  }

  exec { "install-project":
    cwd => "$project_path",
    command => "python $project_path/setup.py develop",
    require => Exec["pip-install"],
  }
}
