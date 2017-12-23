import os
from reefperf.cloud_driver import LCCloudScaleDriver

if __name__ == '__main__':
    driver = LCCloudScaleDriver(api_token=os.environ["api_token"])
    with driver.create_node(name="ls-node", size="flex-2", image="ubuntu-16.04") as node:
        stdout = node.connection.exec_command('ls /')
        for line in stdout.readlines():
            print(line)
