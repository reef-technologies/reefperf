import logging
from reefperf.test_runner import TestRunner

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    results = TestRunner(
        "examples/sample_wrk/app_deployment_config.json",
        "examples/sample_wrk/node_types_config.json",
        "examples/sample_wrk/spectacle_config.json",
    ).run()
    for result in results:
        for line in result:
            print(line)
        print()
