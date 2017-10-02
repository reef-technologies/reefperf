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
    with driver.create_node(cloud_node_cfg) as node:
        stdout = node.connection.exec_command('ls /')
        for line in stdout.readlines():
            print(line)
