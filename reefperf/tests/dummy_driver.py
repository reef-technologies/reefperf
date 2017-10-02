from ipaddress import IPv4Network

from reefperf.cloud_driver import CloudDriver
from reefperf.tests.dummy_node import DummyCloudNode


class DummyCloudDriver(CloudDriver):
    IP_POOL = (str(ip_addr) for ip_addr in IPv4Network('10.10.10.0/24'))

    def create_node(self, node_config):
        node_config = node_config.copy()
        ip_addr = next(self.IP_POOL)
        node_config["ipv4"] = ip_addr
        node_name = node_config["name"]
        node_config["private-key-path"] = f"~/.ssh/{node_name}/id_rsa"
        return DummyCloudNode(node_config)
