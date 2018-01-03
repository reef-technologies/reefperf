from collections import defaultdict
from frozendict import frozendict

from reefperf.driver_manager import DriverManager
from reefperf.generators.parameters_generator import CreateNodeParametersGenerator


class Theater(object):
    EMPTY_DICT = frozendict()

    def __init__(self, node_types_config, app_deployment_config):
        self._node_types_config = node_types_config
        self._app_deployment_config = app_deployment_config
        self._driver_manager = DriverManager()
        self._parameter_generator = CreateNodeParametersGenerator()
        self._app_nodes = self._create_app_nodes()

    def app_nodes_by_type(self, node_type):
        return self._app_nodes[node_type]

    def _create_app_nodes(self):
        nodes = defaultdict(list)
        for node_type, node_deploy_config in self._app_deployment_config["app_deployment"]["nodes"].items():
            node_num = node_deploy_config.get("count", 1)
            for _ in range(node_num):
                node = self._create_node(node_type)
                nodes[node_type].append(node)
        return nodes

    def _create_node(self, node_type):
        node_deploy_config = self._app_deployment_config["app_deployment"]["nodes"][node_type]
        driver_class = self._node_types_config["app_node_types"][node_type]["driver_class"]
        driver_parameters = self._node_types_config["app_node_types"][node_type].get(
            "create_driver_parameters", self.EMPTY_DICT
        )
        driver = self._driver_manager.get_driver(driver_class, **driver_parameters)
        ready_parameters = self._parameter_generator.generate(
            node_type,
            self._node_types_config["app_node_types"][node_type]["create_node_parameters"],
            node_deploy_config
        )
        return driver.create_node(**ready_parameters)
