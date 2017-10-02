from io import StringIO
from pprint import pprint

import libcloud
import paramiko

from reefperf.cloud_driver import LCCloudScaleDriver

if __name__ == '__main__':
    credentials = {
        'api_token': 'token'
    }
    cloud_node_cfg = {
        'node_name': 'node1',
        'size': 'flex-2',
        'image': 'ubuntu-16.04',
        'connection': {
            'connection_class': 'paramiko'
        }
    }
    driver = LCCloudScaleDriver(credentials)
    node = driver.create_node(cloud_node_cfg)
    stdout_ = node.connection.exec_command('ls /')
    for line in stdout_.readlines():
        print(line)
    node.destroy()
