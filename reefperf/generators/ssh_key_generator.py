from abc import ABCMeta, abstractmethod
from io import StringIO

from paramiko.rsakey import RSAKey


class AbstractKeyGenerator(object):
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def generate(cls, length):
        pass


class ParamikoRSAKeyGenerator(AbstractKeyGenerator):
    @classmethod
    def generate(cls, length=2048):
        priv_key = RSAKey.generate(bits=length)
        priv_key_stream = StringIO()
        priv_key.write_private_key(priv_key_stream)
        priv_key_str = priv_key_stream.getvalue()
        pub_key_str = f"{priv_key.get_name()} {priv_key.get_base64()}"
        return {
            'keys_type': 'rsa',
            'priv_key_str': priv_key_str,
            'pub_key_str': pub_key_str,
        }
