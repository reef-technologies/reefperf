import json
from pathlib import Path
from class_registry import RegistryPatcher

from reefperf.director import Director
from reefperf.testing_tool_wrapper import testing_tools
from reefperf.cloud_driver import cloud_drivers

from reefperf.tests.dummy_driver import DummyCloudDriver
from reefperf.tests.dummy_testing_tool_wrapper import DummyTestingToolWrapper


class TestDirector(object):
    @classmethod
    def setup_class(cls):
        script_path = Path(__file__)
        test_files_dir = script_path.parent.joinpath('test_files')
        with open(test_files_dir.joinpath("test_app_deployment.json"), "rb") as config_file:
            cls.app_deployment_config = json.load(config_file)
        with open(test_files_dir.joinpath("test_node_types_config.json"), "rb") as config_file:
            cls.node_types_config = json.load(config_file)
        with open(test_files_dir.joinpath("test_spectacle_config.json"), "rb") as config_file:
            cls.spectacle_config = json.load(config_file)

    def test_director(self):
        with RegistryPatcher(testing_tools, DummyTestingToolWrapper=DummyTestingToolWrapper):
            with RegistryPatcher(cloud_drivers, DummyCloudDriver=DummyCloudDriver):
                director = Director(
                    self.app_deployment_config,
                    self.node_types_config,
                    self.spectacle_config,
                )
                test_results = director.run_test()
                assert sorted(test_results) == [
                    "DummyTestingTool, parameter value: 1",
                    "DummyTestingTool, parameter value: 2",
                    "DummyTestingTool, parameter value: 3",
                    "DummyTestingTool, parameter value: 4",
                    "DummyTestingTool, parameter value: 4",
                ]
