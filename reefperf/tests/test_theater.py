import json
from pathlib import Path

from mock import patch

from reefperf.tests.dummy_driver import DummyCloudDriver
from reefperf.theater import Theater


class TestTheater(object):
    @classmethod
    def setup_class(cls):
        script_path = Path(__file__)
        test_files_dir = script_path.parent.joinpath('test_files')
        with open(test_files_dir.joinpath("test_app_deployment.json"), "rb") as config_file:
            cls.app_deployment_config = json.load(config_file)
        with open(test_files_dir.joinpath("test_node_types_config.json"), "rb") as config_file:
            cls.theater_config = json.load(config_file)

    @patch.dict(
        "reefperf.cloud_driver.DRIVER_CLASSES",
        {"TestCloudDriver": DummyCloudDriver}
    )
    def test_create_app_nodes(self):
        theater = Theater(
            self.theater_config,
            self.app_deployment_config,
        )
        assert len(theater._app_nodes) == 3
        self.check_node_names(theater._app_nodes, "http", ["http"])
        self.check_node_names(theater._app_nodes, "cache", ["cache1", "cache2"])
        self.check_node_names(theater._app_nodes, "database", ["database"])
        http_node = theater._app_nodes["http"][0]
        assert http_node.ssh_data == {
            "host": "10.10.10.0",
            "port": "22",
            "private-key-path": "~/.ssh/http/id_rsa",
            "username": "ubuntu",

        }

    def check_node_names(self, app_nodes,  node_type, expected_names):
        assert sorted(node.node_name for node in app_nodes[node_type]) == expected_names
