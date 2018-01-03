import time

from abc import ABCMeta, abstractmethod

from class_registry import ClassRegistry


class TestingToolWrapper(object, metaclass=ABCMeta):
    @abstractmethod
    def run_tool(self, node, app):
        pass


testing_tools = ClassRegistry()


@testing_tools.register("SleepWrapper")
class SleepWrapper(object):
    def __init__(self, sleep_length):
        self._sleep_length = sleep_length

    def run_tool(self, node, app):
        # TODO: sleep on cloud node
        time.sleep(self._sleep_length)
        return f"Slept for {self._sleep_length} seconds"
