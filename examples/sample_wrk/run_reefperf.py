from reefperf.test_runner import TestRunner

if __name__ == '__main__':
    test_runner = TestRunner(
        "examples/sample_wrk/app_deployment_config.json",
        "examples/sample_wrk/node_types_config.json",
        "examples/sample_wrk/spectacle_config.json"
    ).run()
