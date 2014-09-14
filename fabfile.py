from fabric.api import *

# It is necessary to find the ssh key file that Vagrant uses for Vagrant ssh and 
# tell fabric about it. 
def vagrant():
    result = local('vagrant ssh-config | grep IdentityFile | head -1', 
            capture=True)
    env.key_filename = result.split()[1]

# Define the cluster roles for better output
env.roledefs = {
        'all': ['vagrant@127.0.0.1:2222','vagrant@127.0.0.1:2200',
            'vagrant@127.0.0.1:2201','vagrant@127.0.0.1:2202'],
        'client': ['vagrant@127.0.0.1:2202'],
        'follower': ['vagrant@127.0.0.1:2200','vagrant@127.0.0.1:2201'],
        'leader': ['vagrant@127.0.0.1:2202'],
}

# Run Hello world
def hellocluster():
    run('/var/www/html/hello/hello')

