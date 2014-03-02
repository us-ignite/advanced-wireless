class frontend {

  $packages = [
               "sass",
               "compass",
               ]

  package { $packages:
    ensure => "installed",
    provider => "gem",
  }

}
