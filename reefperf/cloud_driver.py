from abc import abstractmethod, ABCMeta
from reefperf.cloud_node import LCCloudScaleNode
from reefperf.ssh_key_generator import ParamikoRSAKeyGenerator
import libcloud


class CloudDriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_node(self, cloud_node_cfg):
        pass

# LC is a short for apache libcloud. It means that
# all classes with prefix LC using this libcloud for operating on cloud nodes


class LCCloudScaleDriver(CloudDriver):
    SSH_KEY_LENGHT = 4096

    def __init__(self, credentials):
        driver_cls = libcloud.get_driver(
            libcloud.DriverType.COMPUTE,
            libcloud.DriverType.COMPUTE.CLOUDSCALE
        )
        self._driver = driver_cls(credentials['api_token'])
        self._images = {
            image.id: image for image in self._driver.list_images()
        }
        self._sizes = {
            size.id: size for size in self._driver.list_sizes()
        }

    def create_node(self, cloud_node_cfg):
        keys = ParamikoRSAKeyGenerator.generate_pair(self.SSH_KEY_LENGHT)
        lc_node_obj = self._driver.create_node(
            name=cloud_node_cfg['node_name'],
            size=self._sizes[cloud_node_cfg['size']],
            image=self._images[cloud_node_cfg['image']],
            ex_create_attr={
                'ssh_keys': [keys['pub_key_str']]
            }
        )
        cloud_node_cfg['connection']['keys'] = keys
        return LCCloudScaleNode(lc_node_obj, cloud_node_cfg['connection'])


DRIVER_CLASSES = {
    "LCCloudScaleDriver": LCCloudScaleDriver
}
