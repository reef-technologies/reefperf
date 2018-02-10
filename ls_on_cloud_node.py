import logging
import os
from reefperf.cloud_driver import LCCloudScaleDriver
from reefperf.testing_tool_wrapper import WrkWrapper

if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    driver = LCCloudScaleDriver(api_token=os.environ["api_token"])
    deploy_command = "./examples/sample_wrk/http_deploy.sh"
    with driver.create_node(name="lsnode", size="flex-2", image="ubuntu-16.04", deploy_command=deploy_command) as node:
        resources = node.deploy()
        print(resources)
        with driver.create_node(name="wrknode", size="flex-2", image="ubuntu-16.04", deploy_command=None) as test_node:
            app = resources
            results = WrkWrapper(1, 1, 1).run_tool(test_node, app)
            for line in results.readlines():
                print(line)
        input("Deployed app on node and made tests. Press enter for delete nodes")
