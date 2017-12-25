from collections import defaultdict

from reefperf.driver_manager import DriverManager
from reefperf.generators.parameters_generator import CreateNodeParametersGenerator


class Theater(object):
    def __init__(self, node_types_config, app_deployment_config):
        self._node_types_config = node_types_config
        self._app_deployment_config = app_deployment_config
        self._app_nodes = self._create_app_nodes()

    def _create_app_nodes(self):
        nodes = defaultdict(list)
        for node_type, node_deploy_config in self._app_deployment_config["app_deployment"]["nodes"].items():
            node_num = node_deploy_config.get("count", 1)
            for _ in range(node_num):
                node = self._create_app_node(node_type)
                nodes[node_type].append(node)
        return nodes

    def _create_app_node(self, node_type):
        node_deploy_config = self._app_deployment_config["app_deployment"]["nodes"][node_type]
        driver = self._get_driver(node_type, app_node=True)
        ready_parameters = CreateNodeParametersGenerator.generate(
            node_type,
            self._node_types_config["app_node_types"][node_type]["create_node_parameters"],
            node_deploy_config,
        )
        return driver.create_node(**ready_parameters)

    def _get_driver(self, node_type, app_node):
        node_category = "test_node_types"
        if app_node:
            node_category = "app_node_types"
        driver_manager = DriverManager.get_instance()
        node_type_config = self._node_types_config[node_category][node_type]
        driver_class = node_type_config["driver_class"]
        driver_parameters = node_type_config["create_driver_parameters"]
        return driver_manager.get_driver(driver_class, **driver_parameters)

    def _create_test_node(self, node_type):
        driver = self._get_driver(node_type, app_node=False)
        ready_parameters = CreateNodeParametersGenerator.generate(
            node_type,
            self._node_types_config["test_node_types"][node_type]["create_node_parameters"],
        )
        return driver.create_node(**ready_parameters)
