from haikunator import Haikunator

from reefperf.generators.registry import generators_registry


class NodeNameGenerator(object):
    @classmethod
    def generate(cls, node_type):
        return f"{node_type}-{Haikunator.haikunate(0)}"


class CreateNodeParametersGenerator(object):
    VALUE = 'value'
    GENERATOR = 'generator-class'
    GEN_PARAMS = 'generator-parameters'
    TYPE = 'type'
    NAME = 'name'
    COUNT = 'count'
    NAME_GENERATOR_CLS = NodeNameGenerator

    @classmethod
    def generate(cls, node_type, node_type_params, node_deploy_params):
        ready_params = {}
        for param_name, param_config in node_type_params.items():
            if cls.VALUE in param_config:
                ready_params[param_name] = param_config[cls.VALUE]
            else:
                generator_cls_name = param_config[cls.GENERATOR]
                generator_cls = generators_registry.get_class(generator_cls_name)
                generator_params = param_config[cls.GEN_PARAMS]
                ready_params[param_name] = generator_cls.generate(**generator_params)
        ready_params.update(node_deploy_params)
        if cls.COUNT in ready_params:
            ready_params.pop(cls.COUNT)
        node_name = cls.NAME_GENERATOR_CLS.generate(node_type)
        ready_params[cls.NAME] = node_name
        return ready_params
