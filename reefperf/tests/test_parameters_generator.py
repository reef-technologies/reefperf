from reefperf.parameters_generator import CreateNodeParametersGenerator


class TestCreateNodeParametersGenerator(object):
    def test_crate_node_parameters_generator(self):
        node_deploy_params = {
            "name": {
                "value": "cache",
            },
            "deploy-command": {
                "value": "./client-name/cache/deploy.sh",
            },
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
            },
        }
        expected_params = {
            "name": "cache",
            "deploy_command": "./client-name/cache/deploy.sh",
            "size": "flex-2",
            "image": "ubuntu-16.04",
            "connection": {
                "key-type": "rsa",
                "priv-key-str": "priv-key",
                "pub-key-str": "pub-key",
            },
        }
        generated_params = CreateNodeParametersGenerator.generate(node_type_params, node_deploy_params)
        assert expected_params == generated_params
