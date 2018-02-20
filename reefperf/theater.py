import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from frozendict import frozendict
from logfury.v0_1 import DefaultTraceMeta

from reefperf.driver_manager import DriverManager
from reefperf.generators.parameters_generator import CreateNodeParametersGenerator


logger = logging.getLogger(__name__)


class Theater(object, metaclass=DefaultTraceMeta):
    EMPTY_DICT = frozendict()
    MAX_WORKERS = 10

    def __init__(self, node_types_config, app_deployment_config):
        self._node_types_config = node_types_config
        self._app_deployment_config = app_deployment_config
        self._driver_manager = DriverManager()
        self._parameter_generator = CreateNodeParametersGenerator()
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
        ready_parameters = self._parameter_generator.generate(
            node_type,
            self._node_types_config["app_node_types"][node_type]["create_node_parameters"],
            node_deploy_config,
        )
        return driver.create_node(**ready_parameters)

    def _get_driver(self, node_type, app_node):
        node_category = "test_node_types"
        if app_node:
            node_category = "app_node_types"
        node_type_config = self._node_types_config[node_category][node_type]
        driver_class = node_type_config["driver_class"]
        driver_parameters = node_type_config.get("create_driver_parameters", self.EMPTY_DICT)
        return self._driver_manager.get_driver(driver_class, **driver_parameters)

    def _create_test_node(self, node_type):
        driver = self._get_driver(node_type, app_node=False)
        ready_parameters = self._parameter_generator.generate(
            node_type,
            self._node_types_config["test_node_types"][node_type]["create_node_parameters"],
        )
        return driver.create_node(**ready_parameters)

    def create_test_nodes(self, node_types):
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            return list(executor.map(self._create_test_node, node_types))

    def destroy_test_nodes(self, test_nodes):
        for node in test_nodes:
            node.destroy()

    def deploy_app(self):
        app = Application()
        for app_nodes in self._app_nodes.values():
            for app_node in app_nodes:
                node_resources = app_node.deploy()
                app.add_node_resources(node_resources)
        return app

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for app_nodes in self._app_nodes.values():
            for app_node in app_nodes:
                app_node.destroy()


class Application(object):
    """
    Represents all resources offered by deployed application.
    Eg. http application url, database url, cache etc.
    Sample application resources: {
        "http": "http://localhost/app",
        "database_url": "postgres://user:password@hostname:port/database-name",
    }
    """
    def __init__(self):
        self._resources = {}

    @property
    def resources(self):
        return self._resources

    def add_node_resources(self, node_resources):
        self._resources.update(node_resources)

    def get_app_resource(self, resource_name):
        return self._resources[resource_name]
