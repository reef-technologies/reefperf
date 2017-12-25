from functools import lru_cache
from reefperf.cloud_driver import cloud_drivers


class DriverManager(object):
    INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = DriverManager()
        return cls.INSTANCE

    @lru_cache(maxsize=None)
    def get_driver(self, cloud_name, *args):
        return cloud_drivers.get(cloud_name, *args)
