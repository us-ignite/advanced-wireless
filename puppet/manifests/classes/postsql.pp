class postsql ($project_name, $username, $password) {
  class { 'postgresql':
    version => '9.1',
  }
  class { 'postgresql::server':
    version => '9.1',
    locale => 'en_US.UTF-8',
  }
  pg_user { $username:
    ensure     => present,
    password   => $password,
    createdb   => true,
    createrole => true,
  }
  pg_database { $project_name:
    owner => $username,
    ensure   => present,
    locale => 'en_US.UTF-8',
    require  => Pg_user[$username],
  }
}
