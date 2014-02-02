# Project specific setup
class application ($project_path, $project_name){

  file { "$project_path/$project_name/settings/local.py":
    ensure => file,
    source => "$project_path/$project_name/settings/local.py-dist",
    replace => false;
  }

  exec { "syncdb":
    cwd => "$project_path",
    command => "django-admin.py syncdb --noinput --settings=$project_name.settings.local",
    require => File["$project_path/$project_name/settings/local.py"];
  }

  # exec { "migratedb":
  #   cwd => "$project_path",
  #   command => "django-admin.py migrate --noinput --settings=$project_name.settings.local",
  #   require => Exec["syncdb"];
  # }

  exec { "installwatson":
    cwd => "$project_path",
    command => "django-admin.py installwatson --settings=$project_name.settings.local",
    require => Exec["syncdb"];
  }

}
