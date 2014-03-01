class update {

  exec { "update_apt":
    command => "apt-get update",
  }

  exec { "dist_upgrade_apt":
    command => "apt-get -y dist-upgrade",
    require => Exec["update_apt"],
  }


}
