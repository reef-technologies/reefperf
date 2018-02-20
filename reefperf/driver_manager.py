from reefperf.cloud_driver import cloud_drivers
from reefperf.utils import Singleton


class DriverManager(object, metaclass=Singleton):
    def get_driver(self, cloud_name, **kwargs):
        return cloud_drivers.get(cloud_name, **kwargs)
