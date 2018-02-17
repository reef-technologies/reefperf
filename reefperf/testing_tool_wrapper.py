import time
import logging

from logfury.v0_1 import DefaultTraceAbstractMeta
from abc import abstractmethod

from class_registry import ClassRegistry

logger = logging.getLogger(__name__)


class TestingToolWrapper(object, metaclass=DefaultTraceAbstractMeta):
    @abstractmethod
    def run_tool(self, node, app):
        pass

    @property
    @abstractmethod
    def supported_resources(self):
        pass


class NotFoundSupportedResource(Exception):
    pass


testing_tools = ClassRegistry()


@testing_tools.register("SleepWrapper")
class SleepWrapper(TestingToolWrapper):
    def __init__(self, sleep_length):
        self._sleep_length = sleep_length

    @property
    def supported_resources(self):
        return ()

    def run_tool(self, node, app):
        # TODO: sleep on cloud node
        time.sleep(self._sleep_length)
        return f"Slept for {self._sleep_length} seconds"


@testing_tools.register("WrkWrapper")
class WrkWrapper(TestingToolWrapper):
    def __init__(self, threads, connections, duration):
        self._threads = threads
        self._connections = connections
        self._duration = duration

    def set_up(self, test_node):
        test_node.connection.exec_command("sudo apt-get update && sudo apt-get -y install wrk")

    @property
    def supported_resources(self):
        return 'https', 'http'

    def get_resource_location(self, app):
        for resource_name in self.supported_resources:
            if resource_name in app.resources:
                return app.get_app_resource(resource_name)
        raise NotFoundSupportedResource()

    def run_tool(self, test_node, app):
        self.set_up(test_node)
        resource_location = self.get_resource_location(app)
        command = f'wrk --threads {self._threads} --connections {self._connections}\
            --duration {self._duration}s {resource_location}'
        stream = test_node.connection.exec_command(command)
        result = stream.readlines()
        return result
