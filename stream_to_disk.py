import docker
from threading import Thread
import pathlib
import time

docker_client = docker.from_env()
directory = pathlib.Path("/logs")
directory.mkdir(exist_ok=True)

print("Waiting 15s for containers to start.")
time.sleep(15)


def stream_to_logs(container):
    print("Doing ", container.name)
    with open(directory / (container.name + ".txt"), "a+", buffering=1) as f:
        for line in container.logs(timestamps=True, stream=True):
            as_txt = line.decode()
            f.write(as_txt)


for container in docker_client.containers.list():
    t = Thread(target=stream_to_logs, args=(container,))
    t.start()


while 1:
    time.sleep(9999)
