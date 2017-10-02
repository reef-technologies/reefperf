from abc import ABCMeta, abstractmethod
from io import StringIO

from paramiko import AutoAddPolicy, SSHClient
from paramiko.client import MissingHostKeyPolicy
from paramiko.rsakey import RSAKey


class NodeConnection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def exec_command(self, command_str):
        pass

    @abstractmethod
    def scp_file(self, path_to_file):
        pass


class ParamikoConnection(NodeConnection):
    KEY_SIZE = 4096
    KEY_CLASSES = {
        'rsa': RSAKey
    }

    def __init__(self, conn_cfg, ipv4, username):
        priv_key_type = conn_cfg['keys']['keys_type']
        priv_key_str = conn_cfg['keys']['priv_key_str']
        priv_key_stream = StringIO(priv_key_str)
        priv_key = self.KEY_CLASSES[priv_key_type].from_private_key(
            priv_key_stream
        )
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.connect(ipv4, username=username, pkey=priv_key)

    def exec_command(self, command_str):
        _, stdout_, _ = self._client.exec_command(command_str)
        return stdout_

    def close(self):
        self._client.close()


class NodeConnectionProvider(object):
    CONNECTION_CLASSES = {
        'paramiko': ParamikoConnection
    }

    @classmethod
    def create_connection(cls, conn_cfg, ipv4, username):
        return cls.CONNECTION_CLASSES[
            conn_cfg['connection_class']
        ](conn_cfg, ipv4, username)
