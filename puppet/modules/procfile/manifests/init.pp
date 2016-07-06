class procfile ($project_path, $project_name) {

  $packages = [
               'thor',
               'dotenv',
               'foreman',
               ]

  package { $packages:
    ensure => 'latest',
    provider => 'gem',
  }

  package { [ 'ruby1.9.1', 'ruby1.9.1-dev']:
    ensure => installed
  }

  file { "/etc/gunicorn":
    ensure => "directory",
    owner  => "root",
    group  => "root",
    mode   => 755,
    require => Package[$packages];
  }

  file { "procfile":
    path => "/etc/gunicorn/Procfile",
    mode => 0644,
    owner => root,
    group => root,
    ensure => file,
    require => File["/etc/gunicorn"],
    content => template("procfile/Procfile.local"),
  }

  exec { 'install-upstart':
    cwd => "$project_path",
    command => "foreman export -a $project_name -t $project_path/puppet/modules/procfile/templates/master.conf.erb -d $project_path -u vagrant -f /etc/gunicorn/Procfile upstart /etc/init",
    require => File["procfile"],
    environment => "HOME=/home/vagrant",
  }

  service { $project_name:
    ensure => running,
    enable => true,
    provider => upstart,
    subscribe => Exec['install-upstart'],
  }

}
