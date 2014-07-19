class phantomjs(){
  include wget

  $packages = [
               "libfreetype6",
               "libfreetype6-dev",
               "fontconfig",
               "libfontconfig1",
               ]

  $phantomjs_version = "1.9.2"
  $phantomjs_file = "phantomjs-${phantomjs_version}-linux-x86_64.tar.bz2"
  $phantomjs_url = "https://phantomjs.googlecode.com/files/${phantomjs_file}"
  $phantomjs_zip_path = "/var/tmp/${phantomjs_file}"
  $install_dir_prefix = '/opt/phantomjs'
  $install_dir = "${install_dir_prefix}"

  package { $packages:
    ensure => present,
  }

  file { "${install_dir_prefix}":
    ensure  => directory,
  }

  file { "${install_dir_prefix}/current":
    ensure  => link,
    target  => "${install_dir}/phantomjs-${phantomjs_version}-linux-x86_64",
    require => File["${install_dir_prefix}"]
  }

  exec { 'download-phantomjs':
    command => "/usr/bin/wget --output-document ${phantomjs_zip_path} ${phantomjs_url}",
    unless  => "/usr/bin/test -f ${phantomjs_zip_path}"
  }

  exec { 'extract-phantomjs':
    command     => "tar xjf ${phantomjs_zip_path} -C ${install_dir}",
    subscribe   => Exec['download-phantomjs'],
    refreshonly => true,
    require     => File[$install_dir]
  }

  file { "/usr/bin/phantomjs":
    ensure => "link",
    target => "${install_dir_prefix}/current/bin/phantomjs",
    subscribe => Exec['extract-phantomjs'],
  }

}
