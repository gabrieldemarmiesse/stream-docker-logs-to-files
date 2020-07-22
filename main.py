import os
import pathlib
import sys
import time

import docker

from stream_docker_logs.container_log_forward import ContainerLogForward
from stream_docker_logs.forwarders.text_file_forwarder import TextFileForwarder


def main():
    try:
        folder = os.getenv("LOG_FOLDER")
        refresh_period_seconds: int = int(os.getenv("REFRESH_PERIOD_SECONDS", 1))
        if folder is None:
            raise ValueError("Logs folder has to be specified")
    except (ValueError, IndexError):
        sys.exit(-1)

    docker_client = docker.from_env()
    directory = pathlib.Path(folder)
    directory.mkdir(exist_ok=True)

    container_log_forward = ContainerLogForward(
        docker_client.containers.list(), [TextFileForwarder(directory)]
    )
    container_log_forward.start()

    while 1:
        container_log_forward.containers_updated(docker_client.containers.list())
        time.sleep(refresh_period_seconds)


if __name__ == "__main__":
    main()
