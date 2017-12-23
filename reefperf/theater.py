from collections import defaultdict

from reefperf.driver_manager import DriverManager
from reefperf.generators.parameters_generator import CreateNodeParametersGenerator


class Theater(object):
    def __init__(self, node_types_config, app_deployment_config):
        self._node_types_config = node_types_config
        self._app_deployment_config = app_deployment_config
        self._app_nodes = self._create_app_nodes()

    def app_nodes_by_type(self, node_type):
        return self._app_nodes[node_type]

    def _create_app_nodes(self):
        nodes = defaultdict(list)
        for node_type, node_deploy_config in self._app_deployment_config["app_deployment"]["nodes"].items():
            node_num = node_deploy_config.get("count", 1)
            driver_manager = DriverManager.get_instance()
            driver_class = self._node_types_config["app_node_types"][node_type]["driver_class"]
            driver_parameters = self._node_types_config["app_node_types"][node_type]["create_driver_parameters"]
            driver = driver_manager.get_driver(driver_class, **driver_parameters)
            ready_parameters = CreateNodeParametersGenerator.generate(
                node_type,
                self._node_types_config["app_node_types"][node_type]["create_node_parameters"],
                node_deploy_config
            )
            for _ in range(node_num):
                node = driver.create_node(**ready_parameters)
                nodes[node_type].append(node)
        return nodes
