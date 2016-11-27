FROM python

MAINTAINER Jason Harmon <jason.harmon@gmail.com>

RUN apt-get update && apt-get install python-pip

VOLUME ["/config"]
WORKDIR /config

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8124
ENTRYPOINT ["python", "server.py"]
