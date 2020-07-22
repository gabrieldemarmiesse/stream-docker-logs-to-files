from multiprocessing.context import Process
from typing import List

from docker.models.containers import Container

from stream_docker_logs.forwarders.log_forwarder import LogForwarder


class ContainerLogForward:
    def __init__(
        self, containers: List[Container], forwarders: List[LogForwarder],
    ):
        self._containers = containers
        self.threads_by_container = {}
        self.forwarders = forwarders

    def start(self):
        for container in self._containers:
            self._forward_log_in_thread(container)

    def _forward_log_in_thread(self, container) -> List[Process]:
        logging_processes: List[Process] = []
        for forwarder in self.forwarders:
            logging_process = forwarder.start(container)

            self.threads_by_container[container.name] = logging_process
            logging_processes.append(logging_process)
        return logging_processes

    def containers_updated(self, updated_containers: List[Container]):
        self.add_missing_containers(updated_containers)
        self.remove_removed_containers(updated_containers)

    def remove_removed_containers(self, updated_containers: List[Container]):
        removed_containers: List[Container] = [
            container
            for container in self._containers
            if container not in updated_containers
        ]
        for removed_container in removed_containers:
            print(f"Removing container {removed_container.name}")
            process: Process = self.threads_by_container.pop(
                removed_container.name, None
            )
            self._containers = [
                container
                for container in self._containers
                if container.name != removed_container.name
            ]
            if process is not None and process.is_alive():
                process.terminate()

    def add_missing_containers(self, updated_containers: List[Container]):
        updated_container: List[Container] = [
            container
            for container in updated_containers
            if container.name not in self.containers_name()
        ]

        for container in updated_container:
            self._containers.append(container)
            self._forward_log_in_thread(container)

    def containers_name(self) -> List[str]:
        return [container.name for container in self._containers]
