import json

from reefperf.director import Director


class TestRunner(object):
    def __init__(self, app_deployment_path, node_types_path, spectacle_path):
        self._app_deployment_config = self._load_config_from_file(app_deployment_path)
        self._node_types_config = self._load_config_from_file(node_types_path)
        self._spectacle_config = self._load_config_from_file(spectacle_path)

    @classmethod
    def _load_config_from_file(cls, path):
        with open(path, "rb") as config_file:
            return json.load(config_file)

    def run(self):
        return Director(
            self._app_deployment_config,
            self._node_types_config,
            self._spectacle_config,
        ).run_test()
