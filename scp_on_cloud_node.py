from reefperf.cloud_driver import LCCloudScaleDriver
import paramiko
from pprint import pprint
import libcloud
import paramiko
from io import StringIO

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
    node.connection.exec_command('ls /')
    node.destroy()
