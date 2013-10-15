class locales($default="en_US.UTF-8", $available=["en_US.UTF-8 UTF-8"]) {
  package { locales:
    ensure => present,
  }

  file { "/etc/locale.gen":
    content => inline_template('<%= available.join("\n") + "\n" %>'),
  }

  file { "/etc/default/locale":
    content => inline_template('LANG=<%= default + "\n" %>'),
  }

  exec { "locale-gen":
    subscribe => [File["/etc/locale.gen"], File["/etc/default/locale"]],
    refreshonly => true,
  }

  exec { "update-locale":
    subscribe => [File["/etc/locale.gen"], File["/etc/default/locale"]],
    refreshonly => true,
  }

  Package[locales] -> File["/etc/locale.gen"] -> File["/etc/default/locale"]
  -> Exec["locale-gen"] -> Exec["update-locale"]
}