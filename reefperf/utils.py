CAPTURE_BEGIN = '<<<<<'
CAPTURE_END = '>>>>>'
SEPARATOR = '='


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


def get_node_resources(deploy_script_output):
    node_resources = {}
    capture_line = False
    for line in deploy_script_output.decode('utf-8').split('\n'):
        line = line.rstrip("\n")
        if line == CAPTURE_BEGIN:
            capture_line = True
            continue
        if line == CAPTURE_END:
            capture_line = False
        if capture_line:
            service_name, _, service = line.partition(SEPARATOR)
            node_resources[service_name] = service
    return node_resources


def is_valid_deploy_command(deploy_command):
    #TODO validate logic
    return True


class InvalidDeployCommand(Exception):
    pass
