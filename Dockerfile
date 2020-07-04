FROM python:3.7

RUN pip install docker
COPY stream_to_disk.py /

CMD python -u /stream_to_disk.py
