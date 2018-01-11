from abc import ABCMeta, abstractmethod

from reefperf.node_connection import ParamikoConnection


class CloudNode(object, metaclass=ABCMeta):
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

    def __init__(self, lc_node_obj, ssh_keys, deploy_command):
        self._lc_node_obj = lc_node_obj
        self._possible_usernames = ['ubuntu', 'core', 'gentoo', 'centos', 'debian', 'arch', 'fedora']
        self._ssh_keys = ssh_keys
        self._deploy_command = deploy_command
        self._connection = None

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
        if self._connection is not None:
            return self._connection
        self._connection = ParamikoConnection(self._ssh_keys, self.hostname, self.username)
        return self._connection

    def destroy(self):
        if self._connection:
            self._connection.close()
        self._lc_node_obj.destroy()

    def deploy(self):
        pass

