from class_registry import RegistryPatcher

from reefperf.director import Actor
from reefperf.testing_tool_wrapper import testing_tools
from reefperf.tests.dummy_testing_tool_wrapper import DummyTestingToolWrapper


class TestActor(object):
    def test_actor(self):
        actor_config = {
            "role": [
                {
                    "testing_tool_class": "DummyTestingToolWrapper",
                    "parameters": {
                        "dummy_parameter": 1
                    }
                },
                {
                    "testing_tool_class": "DummyTestingToolWrapper",
                    "parameters": {
                        "dummy_parameter": 24
                    }
                },
                {
                    "testing_tool_class": "DummyTestingToolWrapper",
                    "parameters": {
                        "dummy_parameter": 145
                    }
                }
            ]
        }
        with RegistryPatcher(testing_tools, DummyTestingToolWrapper=DummyTestingToolWrapper):
            # app and node parameters are irrelevant for this test
            results = Actor(app=None, actor_config=actor_config, node=None).play()
            assert results == [
                "DummyTestingTool, parameter value: 1",
                "DummyTestingTool, parameter value: 24",
                "DummyTestingTool, parameter value: 145",
            ]
