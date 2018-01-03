from reefperf.cloud_driver import CloudDriver
from reefperf.cloud_node import CloudNode


class DummyCloudNode(CloudNode):
    def __init__(self, name, username, deploy_command=None):
        self._name = name
        self._username = username
        self._deploy_command = deploy_command

    @property
    def node_name(self):
        return self._name

    @property
    def username(self):
        return self._username

    @property
    def deploy_command(self):
        return self._deploy_command

    @property
    def connection(self):
        raise NotImplementedError()

    def destroy(self):
        pass


class DummyCloudDriver(CloudDriver):
    def create_node(self, name, username, deploy_command=None):
        return DummyCloudNode(name, username, deploy_command)
