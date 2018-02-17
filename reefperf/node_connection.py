import os
import logging
from abc import abstractmethod
from io import StringIO
from logfury.v0_1 import DefaultTraceAbstractMeta

from paramiko import AutoAddPolicy, SSHClient
from paramiko.rsakey import RSAKey

logger = logging.getLogger(__name__)


class NodeConnection(object, metaclass=DefaultTraceAbstractMeta):
    @abstractmethod
    def exec_command(self, command_str):
        pass

    @abstractmethod
    def scp_file(self, path_to_file):
        pass


class ParamikoConnection(NodeConnection):
    KEY_SIZE = 4096
    KEY_CLASSES = {'rsa': RSAKey}

    def __init__(self, keys, hostname, username):
        priv_key_type = keys['keys_type']
        priv_key_str = keys['priv_key_str']
        priv_key_stream = StringIO(priv_key_str)
        self.priv_key = self.KEY_CLASSES[priv_key_type].from_private_key(priv_key_stream)
        self._hostname = hostname
        self._username = username
        self._client = None

    @property
    def client(self):
        if self._client is not None:
            return self._client
        self._client = SSHClient()
        self._client.set_missing_host_key_policy(AutoAddPolicy())
        self._client.connect(self._hostname, username=self._username, pkey=self.priv_key)
        return self._client

    def exec_command(self, command_str):
        _, stdout, _ = self.client.exec_command(command_str)
        stdout.channel.recv_exit_status()
        return stdout

    def scp_file(self, path_to_file):
        raise NotImplementedError()

    def dump_private_key_to_file(self, node_name):
        key_path = f'/tmp/reef-perf-key-{node_name}-{os.getpid()}'
        if os.path.isfile(key_path):
            os.remove(key_path)
        with open(key_path, 'w') as key_file:
            self.priv_key.write_private_key(key_file)
        os.chmod(key_path, 0o400)
        return key_path

    def close(self):
        self.client.close()
