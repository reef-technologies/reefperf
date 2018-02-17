import libcloud
import os


if __name__ == '__main__':
    driver_cls = libcloud.get_driver(
        libcloud.DriverType.COMPUTE,
        libcloud.DriverType.COMPUTE.CLOUDSCALE,
    )
    driver = driver_cls(os.environ["api_token"])
    for node in driver.list_nodes():
        driver.destroy_node(node)
