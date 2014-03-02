# Commands to run before all others in puppet.
class init {
  $packages = [
               "python-software-properties",
               "build-essential",
               "libffi-dev",
               ]

  group { "puppet":
    ensure => "present",
  }

  exec { "update_apt":
    command => "apt-get update",
  }

  exec { "dist_upgrade_apt":
    command => "apt-get -y dist-upgrade",
    require => Exec["update_apt"],
  }

  package { $packages:
    ensure => present,
    require => Exec["update_apt"],
  }

}
