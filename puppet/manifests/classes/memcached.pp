class memcached {
  package { "memcached":
    ensure => installed;
  }

  service { "memcached":
    ensure => running,
    enable => true,
    require => Package['memcached'];
  }
}
