from reefperf.cloud_node import CloudNode


class DummyCloudNode(CloudNode):
    def __init__(self, config):
        self._config = config

    @property
    def ipv4(self):
        return self._config["ipv4"]

    @property
    def username(self):
        return self._config["username"]

    @property
    def ssh_data(self):
        return {
            "host": self.ipv4,
            "port": "22",
            "private-key-path": self._config["private-key-path"],
            "username": self.username,
        }

    @property
    def node_name(self):
        return self._config["name"]

    @property
    def connection(self):
        raise NotImplementedError()
