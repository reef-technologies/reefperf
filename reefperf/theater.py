from collections import defaultdict

from reefperf.cloud_driver import DRIVER_CLASSES


class Theater(object):
    def __init__(self, node_types_config, app_deployment_config):
        self._node_types_config = node_types_config
        self._app_deployment_config = app_deployment_config
        self._app_nodes = self._create_app_nodes()
        self._test_nodes = defaultdict(list)

    def _create_app_nodes(self):
        nodes = defaultdict(list)
        for node_deploy_config in self._app_deployment_config["app-deployment"]["nodes"]:
            node_type = node_deploy_config["type"]
            node_config = self._node_types_config["app-node-types"][node_type]
            node_config["name"] = node_deploy_config["name"]
            driver_class = DRIVER_CLASSES[node_config["driver-class"]]
            driver = driver_class()
            node = driver.create_node(node_config)
            nodes[node_deploy_config["type"]].append(node)
        return nodes
