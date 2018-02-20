import logging
from abc import abstractmethod
from functools import lru_cache

import libcloud
from class_registry import ClassRegistry
from logfury.v0_1 import DefaultTraceAbstractMeta

from reefperf.cloud_node import LCCloudScaleNode
from reefperf.generators.ssh_key_generator import ParamikoRSAKeyGenerator


logger = logging.getLogger(__name__)


class CloudDriver(object, metaclass=DefaultTraceAbstractMeta):
    @abstractmethod
    def create_node(self, *args):
        pass


cloud_drivers = ClassRegistry()

# LC is a short for apache libcloud. It means that
# all classes with prefix LC using this libcloud for operating on cloud nodes


@cloud_drivers.register("LCCloudScaleDriver")
class LCCloudScaleDriver(CloudDriver):
    """
    This class is not threadsafe.
    """
    SSH_KEY_LENGTH = 4096

    def __init__(self, api_token):
        driver_cls = libcloud.get_driver(
            libcloud.DriverType.COMPUTE,
            libcloud.DriverType.COMPUTE.CLOUDSCALE,
        )
        self._driver = driver_cls(api_token)

    @property
    @lru_cache(maxsize=1)
    def images(self):
        return {image.id: image for image in self._driver.list_images()}

    @property
    @lru_cache(maxsize=1)
    def sizes(self):
        return {size.id: size for size in self._driver.list_sizes()}

    def create_node(self, name, size, image, deploy_command=None):
        keys = ParamikoRSAKeyGenerator.generate(self.SSH_KEY_LENGTH)
        lc_node_obj = self._driver.create_node(
            name=name,
            size=self.sizes[size],
            image=self.images[image],
            ex_create_attr={'ssh_keys': [keys['pub_key_str']]}
        )
        lc_node_obj.driver.wait_until_running((lc_node_obj,))
        return LCCloudScaleNode(lc_node_obj, name, keys, deploy_command)
