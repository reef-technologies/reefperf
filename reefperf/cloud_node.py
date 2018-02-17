import logging
import subprocess
from abc import abstractmethod
from logfury.v0_1 import DefaultTraceAbstractMeta

from reefperf.node_connection import ParamikoConnection
from reefperf import utils

logger = logging.getLogger(__name__)


class CloudNode(object, metaclass=DefaultTraceAbstractMeta):
    @property
    @abstractmethod
    def connection(self):
        pass

    @property
    @abstractmethod
    def deploy_command(self):
        pass

    @property
    @abstractmethod
    def ssh_data(self):
        pass

    def deploy(self):
        deploy_command = f"{self._deploy_command} {self.ssh_data}"
        if not utils.is_valid_deploy_command(deploy_command):
            raise utils.InvalidDeployCommand()
        completed = subprocess.run([deploy_command], shell=True, stdout=subprocess.PIPE)
        return utils.get_node_resources(completed.stdout)

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

    def __init__(self, lc_node_obj, name, ssh_keys, deploy_command=None):
        self._lc_node_obj = lc_node_obj
        self._possible_usernames = ['ubuntu', 'core', 'gentoo', 'centos', 'debian', 'arch', 'fedora']
        self._ssh_keys = ssh_keys
        self._deploy_command = deploy_command
        self._connection = None
        self._name = name

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

    @property
    def deploy_command(self):
        return self._deploy_command

    @property
    def ssh_data(self):
        key_file = self.connection.dump_private_key_to_file(self._name)
        return f"{self.username} {self.hostname} 22 {key_file}"

    def destroy(self):
        if self._connection:
            self._connection.close()
        self._lc_node_obj.destroy()
