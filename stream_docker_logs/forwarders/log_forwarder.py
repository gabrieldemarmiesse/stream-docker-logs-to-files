from multiprocessing.context import Process

from docker.models.containers import Container


class LogForwarder:
    def start(self, container: Container) -> Process:
        pass
