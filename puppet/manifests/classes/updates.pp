class updates {

  exec { "updates_apt_update":
    command => "apt-get update",
    logoutput   => 'on_failure',
    refreshonly => true,
    timeout => 10000,
  }

  exec { "updates_dist_upgrade":
    command => "apt-get -y dist-upgrade",
    logoutput => 'on_failure',
    refreshonly => true,
    notify => Exec["updates_apt_update"],
    timeout => 10000,
  }

}
