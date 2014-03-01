class nodejs ($project_path){

  $node_modules_dir = "/home/vagrant/node_modules"


  exec { "node-repo" :
    command => "/usr/bin/add-apt-repository -y ppa:chris-lea/node.js",
    notify => Exec["dist_upgrade_apt"],
    creates => "/etc/apt/sources.list.d/chris-lea-node_js-precise.list"
  }

  package { "nodejs":
    ensure => latest,
  }

  file { $node_modules_dir:
    ensure => "directory",
    mode => 777,
  }

  file { "${project_path}/node_modules":
    ensure => "link",
    target => $node_modules_dir,
    require => File[$node_modules_dir],
  }

  exec { "node-grunt-cli":
    command => "/usr/bin/npm install -g grunt-cli",
    require => Package["nodejs"],
    creates => "/usr/bin/grunt",
  }

  exec { "node-bower":
    command => "/usr/bin/npm install -g bower",
    require => Package["nodejs"],
    creates => "/usr/bin/bower",
  }

  exec { "node-install-package":
    cwd => "${project_path}",
    command => "/usr/bin/npm install .",
    require => Exec["node-grunt-cli"],
  }

}

