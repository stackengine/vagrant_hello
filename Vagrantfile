# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # This is the location of the machine image on your workstation. You can
  # use a  box_url, however you will then always be pulling it from the 
  # internet for each project. Better to keep it locally.
  config.vm.box = 
    '~/vagrant_boxes/precise-server-cloudimg-amd64-vagrant-disk1.box' 

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network 'private_network', ip: '10.7.1.2'

  # DEVELOPER MAGIC HAPPENS HERE
  # The directory where you are actively developing (~/code/vagrant_hello)
  # is now mounted to the guest at the web root expected by Nginx 
  # See the NGINXBLOCK below.  
  config.vm.synced_folder '~/code/vagrant_hello', '/var/www/html/hello'

  # Set some things specific to Virtualbox. In this case we want to 
  # limit memory to a 1GB.  
  config.vm.provider 'virtualbox' do |vb|
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ['modifyvm', :id, '--memory', '1024']
  end

  # This script is run on the machine right after boot time. If you i
  # are familiar with AWS ec2 userdata as a concept that is a good 
  # way to think of it.
$installscript = <<INSTALLSCRIPT
    sudo apt-get update && sudo apt-get upgrade 
    sudo apt-get install --assume-yes nginx golang
    sudo mkdir -p /var/www/html/hello
INSTALLSCRIPT
  
  # This serves as a rudimentary template for the nginx server block 
  # (same as an Apache httpd virutal host).
$nginxblock = <<NGINXBLOCK
server {
    listen   80; 

    root /var/www/html/hello; 
    index index.html index.htm;

    server_name 10.7.1.2;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINXBLOCK

  # After setting up the server block, we will enable it, remove the 
  # pre-installed default block and restart the server
$setupscript = <<SETUPSCRIPT
    sudo ln -sv /etc/nginx/sites-available/hello /etc/nginx/sites-enabled/hello
    sudo rm /etc/nginx/sites-available/default
    sudo service nginx restart 
SETUPSCRIPT

  # Install nginx first
  config.vm.provision :shell, 
    inline: $installscript

  # Write out the nginx block as a configuration
  config.vm.provision :shell, 
    inline: "echo -e '#{$nginxblock}' >> /etc/nginx/sites-available/hello"

  # This is the actual line that calls the script.
  config.vm.provision :shell, 
    inline: $setupscript

end
