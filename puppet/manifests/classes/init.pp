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

  package { $packages:
    ensure => present,
  }

}
