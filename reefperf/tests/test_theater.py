import json
from pathlib import Path
from class_registry import RegistryPatcher


from reefperf.tests.dummy_driver import DummyCloudDriver
from reefperf.theater import Theater
from reefperf.cloud_driver import cloud_drivers


class TestTheater(object):
    @classmethod
    def setup_class(cls):
        script_path = Path(__file__)
        test_files_dir = script_path.parent.joinpath('test_files')
        with open(test_files_dir.joinpath("test_app_deployment.json"), "rb") as config_file:
            cls.app_deployment_config = json.load(config_file)
        with open(test_files_dir.joinpath("test_node_types_config.json"), "rb") as config_file:
            cls.theater_config = json.load(config_file)

    def test_create_app_nodes(self):
        with RegistryPatcher(cloud_drivers, DummyCloudDriver=DummyCloudDriver):
            theater = Theater(
                self.theater_config,
                self.app_deployment_config,
            )
            self.check_node_usernames(theater.app_nodes_by_type("http"), ["http_ubuntu"])
            self.check_node_usernames(theater.app_nodes_by_type("cache"), 2 * ["cache_ubuntu"])
            self.check_node_usernames(theater.app_nodes_by_type("database"), ["database_ubuntu"])
            self.check_node_deploy_command(theater.app_nodes_by_type("http"), ["./client_name/http/deploy.sh"])
            self.check_node_deploy_command(theater.app_nodes_by_type("cache"), 2 * ["./client_name/cache/deploy.sh"])
            self.check_node_deploy_command(
                theater.app_nodes_by_type("database"), ["./client_name/database/deploy.sh"]
            )

    @classmethod
    def check_node_usernames(cls, app_nodes, expected_usernames):
        assert sorted(node.username for node in app_nodes) == expected_usernames

    @classmethod
    def check_node_deploy_command(cls, app_nodes, expected_commands):
        assert sorted(node.deploy_command for node in app_nodes) == expected_commands
