from reefperf.testing_tool_wrapper import TestingToolWrapper


class DummyTestingToolWrapper(TestingToolWrapper):
    def __init__(self, dummy_parameter):
        self._dummy_parameter = dummy_parameter

    def run_tool(self, node, app):
        return f"DummyTestingTool, parameter value: {self._dummy_parameter}"
