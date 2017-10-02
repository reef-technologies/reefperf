from abc import ABCMeta, abstractmethod

from reefperf.node_connection_provider import NodeConnectionProvider


class CloudNode(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def connection(self):
        pass


# LC is a short for apache libcloud. It means that
# all classes with prefix LC using this libcloud for operating on cloud nodes


class CloudScaleUserNameNotFound(Exception):
    def ___init__(self, image_name):
        self._image_name = image_name

    def __str__(self):
        return f"Not found proper username for {self._image_name} image"


class LCCloudScaleNode(CloudNode):
    """
    This class is not threadsafe.
    """

    def __init__(self, lc_node_obj, conn_cfg):
        self._lc_node_obj = lc_node_obj
        self._possible_usernames = ['ubuntu', 'core', 'gentoo', 'centos', 'debian', 'arch', 'fedora']
        self._conn_cfg = conn_cfg
        self._connection_obj = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    @property
    def hostname(self):
        return self._lc_node_obj.public_ips[0]

    @property
    def username(self):
        for name in self._possible_usernames:
            if self._lc_node_obj.image.id.startswith(name):
                return name
        raise CloudScaleUserNameNotFound(self._lc_node_obj.image.id)

    @property
    def connection(self):
        if self._connection_obj is not None:
            return self._connection_obj
        self._connection_obj = NodeConnectionProvider.create_connection(self._conn_cfg, self.hostname, self.username)
        return self._connection_obj

    def destroy(self):
        if self._connection_obj:
            self._connection_obj.close()
        self._lc_node_obj.destroy()
