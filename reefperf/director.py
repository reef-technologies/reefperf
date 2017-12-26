import itertools

from threading import Thread
from queue import Queue

from reefperf.testing_tool_wrapper import testing_tools


class Director(object):
    def __init__(self, theater, spectacle_config):
        self._theater = theater
        self._spectacle_config = spectacle_config


class Spectacle(object):
    def __init__(self, theater, spectacle_config):
        self._theater = theater
        self._spectacle_config = spectacle_config

    def play(self):
        pass


class Act(object):
    def __init__(self, theater, act_config, app):
        self._theater = theater
        self._act_config = act_config
        self._app = app
        self._results_queue = Queue()

    def play(self):
        pass

    def worker(self, node, scene_config, app):
        with node as node:
            test_results = Scene(node, scene_config, app).play()
            self._results_queue.put(test_results)


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
