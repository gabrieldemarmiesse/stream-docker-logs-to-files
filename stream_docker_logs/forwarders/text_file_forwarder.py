import multiprocessing
import pathlib

from docker.models.containers import Container
from multiprocessing.context import Process

from stream_docker_logs.forwarders.log_forwarder import LogForwarder


class TextFileForwarder(LogForwarder):
    def __init__(self, log_folder: pathlib.Path):
        self._log_folder = log_folder

    def start(self, container: Container) -> Process:
        logging_process = multiprocessing.Process(
            target=write_to_txt_file, args=(container, self._log_folder)
        )
        logging_process.start()
        return logging_process


def write_to_txt_file(container: Container, log_folder: pathlib.Path):
    print(
        f"Writing log of container {container.name} to {log_folder}/{container.name}.txt"
    )
    with open(log_folder / (container.name + ".txt"), "a+", buffering=1) as f:
        for line in container.logs(timestamps=True, stream=True):
            as_txt = line.decode()
            f.write(as_txt)
