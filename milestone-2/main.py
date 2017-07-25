# Manual
# 1. Create account on https://control.cloudscale.ch/signup
# 2. Get directory content from https://github.com/reef-technologies/reefperf/tree/libcloud-examples/milestone-2
# 3. Visit https://control.cloudscale.ch/user/api-tokens to generate api access token
# 4. Generate new pair ssh keys
# 5. Customize config-template.json
# 4. python main.py path-to-config

from pprint import pprint

import itertools
import json
import libcloud
import os
import sys
import time
import paramiko

ID_USER_MAPPING = {
	'ubuntu-16.10': 'ubuntu'
}

def load_config(path_to_config):
	return json.loads(open(path_to_config).read())

def create_node(driver, node_name, public_ssh_key_path):
	ssh_pub_key = open(public_ssh_key_path).read()
	return driver.create_node(
	    name=node_name,
	    size=driver.list_sizes()[0],
	    image=driver.list_images()[0],
	    ex_create_attr=dict(
	        ssh_keys=[ssh_pub_key],
	    )
	)

def put_and_run_script_on_instance(
	node, priv_ssh_key_path, deploy_script_path, deploy_command, script_args, is_test
):
	key = paramiko.RSAKey.from_private_key_file(priv_ssh_key_path)
	node_ipv4 = node.public_ips[0]
	node_user = ID_USER_MAPPING[node.image.id]
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(node_ipv4, username=node_user, pkey=key)
	sftp = client.open_sftp()
	sftp.put(deploy_script_path, deploy_script_path)
	sftp.close()
	client.exec_command('chmod u+x ' + deploy_script_path)
	_, stdout, _ = client.exec_command(deploy_command + ' ' + ' '.join(script_args))
	if is_test:
		for line in stdout:
			print(line.strip('\n'))
	client.close()
	port = 8000
	return (node_ipv4, port)

if __name__ == '__main__':

	config = load_config(sys.argv[1])
	cls = libcloud.get_driver(
	    libcloud.DriverType.COMPUTE,
	    libcloud.DriverType.COMPUTE.CLOUDSCALE
	)
	driver = cls(config['cloudscale_token'])
	
	print("Creating app instance")
	app_node = create_node(driver, 'app-node', config['pub_ssh_key_path'])
	print('App instance was created with IPv4: {}'.format(app_node.public_ips[0]))

	print('Deploying app on app-node')
	ip, port = put_and_run_script_on_instance(
		app_node, config["priv_ssh_key_path"], config["deploy_script_path"],
		config["deploy_command"], [], False
	)
	print('App deployed successfully. Check {}:{}'.format(ip, port))

	print("Creating test instance")
	test_node = create_node(driver, 'test-node', config['pub_ssh_key_path'])
	print('Test instance was created with IPv4: {}'.format(test_node.public_ips[0]))

	print('Running test')
	put_and_run_script_on_instance(
		test_node, config['priv_ssh_key_path'], config['test_script_path'],
		config['test_command'], [str(ip), str(port)], True
	)
	print("Test finished successfully")


	print("To destroy instances press enter")
	sys.stdin.readline()

	print("Destroy app instance")
	driver.ex_stop_node(app_node)
	time.sleep(20)
	driver.destroy_node(app_node)
	print("Destroyed app instance")

	print("Destroy test instance")
	driver.ex_stop_node(test_node)
	time.sleep(20)
	driver.destroy_node(test_node)
	print("Destroyed test instance")
