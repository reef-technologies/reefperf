import itertools

from threading import Thread
from queue import Queue

from reefperf.testing_tool_wrapper import testing_tools
from reefperf.theater import Theater


class Director(object):
    def __init__(self, app_deployment_config, node_types_config, spectacle_config):
        self._app_deployment_config = app_deployment_config
        self._node_types_config = node_types_config
        self._spectacle_config = spectacle_config

    def run_test(self):
        with Theater(self._node_types_config, self._app_deployment_config) as theater:
            app = theater.deploy_app()
            return Spectacle(theater, self._spectacle_config, app).play()


class Spectacle(object):
    def __init__(self, theater, spectacle_config, app):
        self._theater = theater
        self._spectacle_config = spectacle_config
        self._app = app

    def play(self):
        results = ()
        for act_config in self._spectacle_config["acts"]:
            act_results = Act(self._theater, act_config, self._app).play()
            results = itertools.chain(results, act_results)
        return results


class Act(object):
    def __init__(self, theater, act_config, app):
        self._theater = theater
        self._act_config = act_config
        self._app = app
        self._results_queue = Queue()
        self._threads = []

    def play(self):
        node_types = self._get_node_types()
        test_nodes = self._theater.create_test_nodes(node_types)
        for node, scene_config in zip(test_nodes, self._act_config["scenes"]):
            thread = Thread(target=self._worker, args=(node, scene_config, self._app,), daemon=True)
            self._threads.append(thread)
            thread.start()
        self._join_threads()
        self._theater.destroy_test_nodes(test_nodes)
        return self._collect_results()

    def _get_node_types(self):
        return (
            scene_config["node_type"] for scene_config in self._act_config["scenes"]
        )

    def _worker(self, node, scene_config, app):
        test_results = Scene(node, scene_config, app).play()
        self._results_queue.put(test_results)

    def _join_threads(self):
        for thread in self._threads:
            thread.join()

    def _collect_results(self):
        results = ()
        while not self._results_queue.empty():
            scene_results = self._results_queue.get()
            results = itertools.chain(results, scene_results)
        return results


class Scene(object):
    def __init__(self, node, scene_config, app):
        self._node = node
        self._scene_config = scene_config
        self._app = app

    def play(self):
        results = ()
        for actor_config in self._scene_config["actors"]:
            results = itertools.chain(results, Actor(self._node, actor_config, self._app).play())
        return results


class Actor(object):
    def __init__(self, node, actor_config, app):
        self._node = node
        self._actor_config = actor_config
        self._app = app

    def play(self):
        test_results = []
        for testing_tool_config in self._actor_config["role"]:
            tool_class = testing_tool_config["testing_tool_class"]
            tool_parameters = testing_tool_config["parameters"]
            testing_tool = testing_tools.get(tool_class, **tool_parameters)
            result = testing_tool.run_tool(self._node, self._app)
            test_results.append(result)
        return test_results
