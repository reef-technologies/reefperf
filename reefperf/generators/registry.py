from class_registry import ClassRegistry

from reefperf.generators.ssh_key_generator import ParamikoRSAKeyGenerator

generators_registry = ClassRegistry()
generators_registry._register("ParamikoRSAKeyGenerator", ParamikoRSAKeyGenerator)
