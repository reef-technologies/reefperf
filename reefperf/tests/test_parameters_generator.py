from class_registry import RegistryPatcher

from reefperf.generators.parameters_generator import CreateNodeParametersGenerator
from reefperf.generators.registry import generators_registry


class DummyConnection(object):
    @classmethod
    def generate(cls, length):
        return {
            "key-length": length,
            "priv-key-str": "priv-key",
            "pub-key-str": "pub-key",
        }


class TestCreateNodeParametersGenerator(object):
    def test_crate_node_parameters_generator(self):
        node_deploy_params = {
            "type": "cache",
            "deploy-command": "./client-name/cache/deploy.sh",
        }
        node_type_params = {
            "size": {
                "value": "flex-2",
            },
            "image": {
                "value": "ubuntu-16.04",
            },
            "connection": {
                "generator-class": "DummyConnection",
                "generator-parameters": {
                    "length": 2048,
                },
            },
        }
        expected_params = {
            "deploy-command": "./client-name/cache/deploy.sh",
            "size": "flex-2",
            "image": "ubuntu-16.04",
            "connection": {
                "key-length": 2048,
                "priv-key-str": "priv-key",
                "pub-key-str": "pub-key",
            },
        }
        with RegistryPatcher(generators_registry, DummyConnection=DummyConnection):
            generated_params = CreateNodeParametersGenerator.generate(node_type_params, node_deploy_params)
            assert expected_params.items() <= generated_params.items()
