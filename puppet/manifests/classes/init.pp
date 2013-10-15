# Commands to run before all others in puppet.
class init {
  $packages = ["python-software-properties", "build-essential"]
  group { "puppet":
    ensure => "present",
  }

  exec { "update_apt":
    command => "sudo apt-get update",
  }

  package { $packages:
    ensure => present,
    require => [
                Exec['update_apt'],
                ];
  }
}
