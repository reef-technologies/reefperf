import logging
import os
from reefperf.cloud_driver import LCCloudScaleDriver

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    driver = LCCloudScaleDriver(api_token=os.environ["api_token"])
    deploy_command = "./examples/sample_wrk/http_deploy.sh"
    with driver.create_node(name="lsnode", size="flex-2", image="ubuntu-16.04", deploy_command=deploy_command) as node:
        resources = node.deploy()
        print(resources)
        input("Deployed app on node. Press enter for delete node")
