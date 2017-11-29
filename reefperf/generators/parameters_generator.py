import itertools

from reefperf.generators.registry import generators_registry


class CreateNodeParametersGenerator(object):
    VALUE = 'value'
    GENERATOR = 'generator-class'
    GEN_PARAMS = 'generator-parameters'

    @classmethod
    def generate(cls, node_type_params, node_deploy_params):
        all_params = itertools.chain(node_deploy_params.items(), node_type_params.items())
        ready_params = {}
        for param_name, param_config in all_params:
            if cls.VALUE in param_config:
                ready_params[param_name] = param_config[cls.VALUE]
            else:
                generator_cls_name = param_config[cls.GENERATOR]
                generator_cls = generators_registry.get_class(generator_cls_name)
                generator_params = param_config[cls.GEN_PARAMS]
                ready_params[param_name] = generator_cls.generate(**generator_params)
        return ready_params
