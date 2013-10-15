class versioning {
  $packages = ["git-core", "subversion", "mercurial"]
  package { $packages:
    ensure => installed;
  }

}
