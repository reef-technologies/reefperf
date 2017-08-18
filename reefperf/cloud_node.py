from abc import abstractmethod, ABCMeta
from reefperf.node_connection_provider import NodeConnectionProvider

class CloudNode(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_connection(self):
        pass

# LC is a short for apache libcloud. It means that
# all classes with prefix LC using this libcloud for operating on cloud nodes

class LCCloudScaleNode(CloudNode):
    def __init__(self, lc_node_obj, conn_cfg):
        self._lc_node_obj = lc_node_obj
        self._possible_usernames = [
            'ubuntu', 'core', 'gentoo', 'centos',
            'debian', 'arch', 'fedora'
        ] 
        self._conn_cfg = conn_cfg
        self._connection_obj = None

    @property
    def ipv4(self):
        return self._lc_node_obj.public_ips[0]

    @property
    def username(self):
        for name in self._possible_usernames:
            if self._lc_node_obj.image.id.startswith(name):
                return name

    @property
    def connection(self):
        if self._connection_obj is None:
            self._connection_obj = NodeConnectionProvider.create_connection(
                self._conn_cfg, self.ipv4, self.username
            )
        return self._connection_obj

    def destroy(self):
        if self._connection_obj:
            self._connection_obj.close()
        self._lc_node_obj.destroy()
