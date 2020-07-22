build:
	docker build . -t 766281746212.dkr.ecr.eu-west-1.amazonaws.com/gabrieldemarmiesse/stream-docker-logs-to-files

run-local:
	LOG_FOLDER=./logs python main.py

start: build
	docker run --rm --name stream-docker-logs-to-files 766281746212.dkr.ecr.eu-west-1.amazonaws.com/gabrieldemarmiesse/stream-docker-logs-to-files

prepare:
	pip install -e ./
