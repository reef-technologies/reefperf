# Manual
# 1. Create account on https://control.cloudscale.ch/signup
# 2. Visit https://control.cloudscale.ch/user/api-tokens to generate api access token
#     and set it as CLOUDSCALE_TOKEN environment variable
# 3. Generate new pair ssh keys
# 4. python create_instance.py path-to-generated-public-key

import libcloud
import os
import sys
import time

print("Creating instance")
cls = libcloud.get_driver(
    libcloud.DriverType.COMPUTE,
    libcloud.DriverType.COMPUTE.CLOUDSCALE
)
driver = cls(os.environ['CLOUDSCALE_TOKEN'])

size = driver.list_sizes()[0]
image = driver.list_images()[0]

ssh_pub_key = open(sys.argv[1]).read()
node = driver.create_node(
    name='node1',
    size=size,
    image=image,
    ex_create_attr=dict(
        ssh_keys=[ssh_pub_key],
    )
)

# do some stuff with instance
# you can ssh on machine using command: ssh -i path-to-ssh-pub-key ubuntu@instance-ip
# to get ipv4 address of instance: new_node.public_ips[0]
time.sleep(30)

print("To destroy instance press enter")
sys.stdin.readline()

print("Destroy instance")
driver.ex_stop_node(node)
time.sleep(30)
driver.destroy_node(node)
