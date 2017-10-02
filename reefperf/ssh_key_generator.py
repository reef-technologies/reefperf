from abc import ABCMeta, abstractmethod
from io import StringIO

from paramiko.rsakey import RSAKey


class AbstractKeyGenerator(object):
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def generate_pair(self, length):
        pass


class ParamikoRSAKeyGenerator(AbstractKeyGenerator):
    @classmethod
    def generate_pair(cls, length):
        priv_key = RSAKey.generate(bits=length)
        priv_key_stream = StringIO()
        priv_key.write_private_key(priv_key_stream)
        priv_key_str = priv_key_stream.getvalue()
        pub_key_str = '{} {}'.format(
            priv_key.get_name(),
            priv_key.get_base64()
        )
        return {
            'keys_type': 'rsa',
            'priv_key_str': priv_key_str,
            'pub_key_str': pub_key_str
        }
