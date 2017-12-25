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
            cls.node_types_config = json.load(config_file)

    def test_create_app_nodes(self):
        with RegistryPatcher(cloud_drivers, DummyCloudDriver=DummyCloudDriver):
            theater = Theater(
                self.node_types_config,
                self.app_deployment_config,
            )
            app_nodes = theater._create_app_nodes()
            self.check_nodes_usernames(app_nodes["http"], ["http_ubuntu"])
            self.check_nodes_usernames(app_nodes["cache"], 2 * ["cache_ubuntu"])
            self.check_nodes_usernames(app_nodes["database"], ["database_ubuntu"])
            self.check_nodes_deploy_command(app_nodes["http"], ["./client_name/http/deploy.sh"])
            self.check_nodes_deploy_command(app_nodes["cache"], 2 * ["./client_name/cache/deploy.sh"])
            self.check_nodes_deploy_command(
                app_nodes["database"], ["./client_name/database/deploy.sh"]
            )

    def test_create_test_node(self):
        with RegistryPatcher(cloud_drivers, DummyCloudDriver=DummyCloudDriver):
            theater = Theater(
                self.node_types_config,
                self.app_deployment_config,
            )
            selenium_node = theater._create_test_node("selenium")
            assert selenium_node.username == "selenium_ubuntu"
            tsung_node = theater._create_test_node("tsung")
            assert tsung_node.username == "tsung_ubuntu"

    @classmethod
    def check_nodes_usernames(cls, app_nodes, expected_usernames):
        assert sorted(node.username for node in app_nodes) == expected_usernames

    @classmethod
    def check_nodes_deploy_command(cls, app_nodes, expected_commands):
        assert sorted(node.deploy_command for node in app_nodes) == expected_commands
