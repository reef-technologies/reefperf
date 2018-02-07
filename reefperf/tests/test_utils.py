from reefperf.utils import get_node_resources


class TestUtils(object):
    def test_get_node_resources(self):
        output = b'Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-109-generic x86_64)\n\n\
            * Documentation:  https://help.ubuntu.com\n * Management:     https://landscape.canonical.com\n\
            * Support:        https://ubuntu.com/advantage\n\n\
            Get cloud support with Ubuntu Advantage Cloud Guest:\n\
            http://www.ubuntu.com/business/services/cloud\n\n0 packages can be updated.\n\
            0 updates are security updates.\n\n\n<<<<<\nhttp=http://5.102.147.22:8000\n>>>>>\n'
        assert get_node_resources(output) == {'http': 'http://5.102.147.22:8000'}
