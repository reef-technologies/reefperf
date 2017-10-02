from abc import ABCMeta, abstractmethod
from io import StringIO

from paramiko import AutoAddPolicy, SSHClient
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

    def __init__(self, conn_cfg, hostname, username):
        priv_key_type = conn_cfg['keys']['keys_type']
        priv_key_str = conn_cfg['keys']['priv_key_str']
        priv_key_stream = StringIO(priv_key_str)
        priv_key = self.KEY_CLASSES[priv_key_type].from_private_key(
            priv_key_stream
        )
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.connect(hostname, username=username, pkey=priv_key)

    def exec_command(self, command_str):
        _, stdout, _ = self._client.exec_command(command_str)
        return stdout

    def scp_file(self, path_to_file):
        raise NotImplementedError()

    def close(self):
        self._client.close()


class NodeConnectionProvider(object):
    CONNECTION_CLASSES = {
        'paramiko': ParamikoConnection
    }

    @classmethod
    def create_connection(cls, connection_config, hostname, username):
        return cls.CONNECTION_CLASSES[
            connection_config['connection_class']
        ](connection_config, hostname, username)
