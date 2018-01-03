from functools import lru_cache
from reefperf.cloud_driver import cloud_drivers
from reefperf.utils import Singleton


class DriverManager(object):
    __metaclass__ = Singleton

    @lru_cache(maxsize=None)
    def get_driver(self, cloud_name, *args):
        return cloud_drivers.get(cloud_name, *args)
