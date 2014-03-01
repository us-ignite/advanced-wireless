import "classes/*.pp"

Exec {
  path => [
           "/usr/local/sbin",
           "/usr/local/bin",
           "/usr/sbin",
           "/usr/bin",
           "/sbin",
           "/bin",
           "/opt/vagrant_ruby/bin",
           "/opt/ruby/bin",
           ]
}

class dev {

  class {
    update: ;

  }

  class { "init":
    require => Class[update],
  }

  class { "memcached":
    require => Class[update],
  }

  class { "locales":
    require => Class[update],
  }

  class { "versioning":
    require => Class[update],
  }

  class { "nodejs":
    project_path => $project_path,
  }

  class { "postsql":
    require => Class[versioning],
    username => $username,
    password => $password,
    project_name => $project_name;
  }

  class { "python":
    require => Class[postsql],
    project_path => $project_path;
  }

  class { "certificates":
    require => Class[python],
    server_name => $server_name;
  }

  class { "nginx":
    require => Class[certificates],
    server_name => $server_name,
    project_name => $project_name,
    project_path => $project_path;
  }

  class { "application":
    require => Class[nginx],
    project_path => $project_path,
    project_name => $project_name,
  }

  class { "procfile":
    require => Class[application],
    project_name => $project_name,
    project_path => $project_path;
  }

  class { "custom":
    require => Class[procfile],
    project_path => $project_path,
    project_name => $project_name;
  }

}

include dev
