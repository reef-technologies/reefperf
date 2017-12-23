from class_registry import RegistryPatcher
from collections import defaultdict

from reefperf.cloud_driver import cloud_drivers_registry


class Theater(object):
    def __init__(self, node_types_config, app_deployment_config):
        self._node_types_config = node_types_config
        self._app_deployment_config = app_deployment_config
        self._app_nodes = self._create_app_nodes()
        self._test_nodes = defaultdict(list)

    def app_nodes_by_type(self, node_type):
        pass

    def _create_app_nodes(self):
        nodes = defaultdict(list)
        for node_deploy_config in self._app_deployment_config["app-deployment"]["nodes"]:
            pass
        return nodes
