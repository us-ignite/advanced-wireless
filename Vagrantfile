require "yaml"

# Load up our vagrant config files -- vagrantconfig.yaml
_config = YAML.load(File.open(File.join(File.dirname(__FILE__), "vagrantconfig.yaml"), File::RDONLY).read)

CONF = _config
MOUNT_POINT = CONF['mount_point']

EXTRA_VARS = {
  hosts: "vagrant",
  host_user: "vagrant",
  username: CONF['username'],
  password: CONF['password'],
  server_name: CONF['server_name'],
  project_name: CONF['project_name'],
  project_path: MOUNT_POINT,
}


Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  if CONF['gui'] == true
    # config.vm.boot_mode = :gui
    config.vm.provider "virtualbox" do |vb|
      vb.gui = true
    end
  end


  config.vm.synced_folder ".", MOUNT_POINT, id: "project-root"

  # Virtualbox has issues with a large amount of shared files,
  # it is recommended to be mounted as NFS
  config.vm.provider :virtualbox do |v, override|
    if CONF['nfs'] == true
      override.vm.synced_folder ".", MOUNT_POINT, :nfs => true, id: "project-root"
    end
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/project-root", "1"]
  end

  # Add to /etc/hosts
  config.vm.network :private_network, ip: CONF['server_ip']
  config.vm.network :forwarded_port, guest: 80, host: 8000

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "vagrant.pp"
    if CONF['debug'] == true
      puppet.options = "--verbose --debug"
    end
    puppet.facter = EXTRA_VARS
  end
end
