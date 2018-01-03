import itertools
from haikunator import Haikunator

from reefperf.generators.registry import generators_registry
from reefperf.utils import Singleton


class NodeNameGenerator(object):
    def __init__(self):
        self.counter = itertools.count()

    def generate(self, node_type):
        return f"{node_type}-{Haikunator.haikunate(0)}-{next(self.counter)}"


class CreateNodeParametersGenerator(object, metaclass=Singleton):
    VALUE = 'value'
    GENERATOR = 'generator-class'
    GEN_PARAMS = 'generator-parameters'
    TYPE = 'type'
    NAME = 'name'
    COUNT = 'count'

    def __init__(self):
        self._node_name_generator = NodeNameGenerator()

    def generate(self, node_type, node_type_params, node_deploy_params=None):
        """
        This method returns dict with parameters for
        create_node method call in CloudDriver subclass, based on
        node_deploy_params (single entrance from "nodes" in app_deployment config)
        and node_type_params (single "crate_node_parameters" value from node types config).
        """
        ready_params = {}
        for param_name, param_config in node_type_params.items():
            if self.VALUE in param_config:
                ready_params[param_name] = param_config[self.VALUE]
            else:
                generator_cls_name = param_config[self.GENERATOR]
                generator_cls = generators_registry.get_class(generator_cls_name)
                generator_params = param_config[self.GEN_PARAMS]
                ready_params[param_name] = generator_cls.generate(**generator_params)
        if node_deploy_params is not None:
            ready_params.update(node_deploy_params)
        if self.COUNT in ready_params:
            ready_params.pop(self.COUNT)
        node_name = self._node_name_generator.generate(node_type)
        ready_params[self.NAME] = node_name
        return ready_params
