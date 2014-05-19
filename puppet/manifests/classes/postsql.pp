class postsql ($project_name, $username, $password) {

  include apt
  apt::ppa { 'ppa:ubuntugis':}

  package {'postgresql-9.1-postgis':
    ensure  => present,
    require => [Apt::Ppa['ppa:ubuntugis'], Class['postgresql']],
  }

  class { 'postgresql':
    version => '9.1',
  }
  class { 'postgresql::server':
    version => '9.1',
    locale => 'en_US.UTF-8',
  }

  # Setup the postgis_template:
  exec { 'create_template_db':
    command => '/usr/bin/createdb template_postgis -E UTF-8 -l en_US.UTF-8 --template=template0',
    unless  => "/usr/bin/psql -c --quiet -A -t -c \"select 1 from pg_database where datname = 'postgis';\"",
    cwd     => '/var/lib/postgresql',
    group   => 'postgres',
    user    => 'postgres',
    require => [Service['postgresql'], Package['postgresql-9.1-postgis']],
  }
  exec { 'create_template_sql':
    command => '/usr/bin/psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql',
    cwd     => '/var/lib/postgresql',
    group   => 'postgres',
    user    => 'postgres',
    refreshonly => true,
    require => Exec['create_template_db'],
  }
  exec { 'create_template_sys_sql':
    command => '/usr/bin/psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql',
    cwd     => '/var/lib/postgresql',
    group   => 'postgres',
    user    => 'postgres',
    refreshonly => true,
    require => Exec['create_template_sql'],
  }
  exec { 'make_template_public':
    command => '/usr/bin/psql -d postgres -c "update pg_database set datistemplate=true where datname=\'template_postgis\';"',
    cwd     => '/var/lib/postgresql',
    group   => 'postgres',
    user    => 'postgres',
    refreshonly => true,
    require => Exec['create_template_sys_sql'],
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
    require  => [Pg_user[$username], Exec['make_template_public']],
    template => 'template_postgis',
  }
}
